from nicegui import ui, app
from datetime import datetime
from fastapi import Request
import time  # THÊM THƯ VIỆN TIME

# ==============================================================
# BIẾN TOÀN CỤC & DỮ LIỆU
# ==============================================================
danh_sach_log = []
thong_ke = {'red': 0, 'green': 0, 'blue': 0}
hang_doi_esp32 = []
thoi_gian_ping = 0   # Biến đếm thời gian sống của ESP32

# ==============================================================
# CỔNG API GIAO TIẾP VỚI ESP32
# ==============================================================
# Cổng 1: Nhận màu sắc


@app.post('/api/sensor')
async def nhan_du_lieu_esp32(request: Request):
    try:
        data = await request.json()
        hang_doi_esp32.append(data)
        global thoi_gian_ping
        thoi_gian_ping = time.time()  # Khi nhận dữ liệu cũng tính là còn sống
        return {"status": "success"}
    except Exception as e:
        return {"status": "error"}

# Cổng 2: Nhận "Nhịp tim" (Ping) để biết hệ thống online


@app.get('/api/ping')
def nhan_ping():
    global thoi_gian_ping
    thoi_gian_ping = time.time()  # Cập nhật thời gian mỗi khi ESP32 nhá máy
    return {"status": "online"}

# ==============================================================
# GIAO DIỆN CHÍNH
# ==============================================================


@ui.page('/dashboard')
def dashboard_page():
    # --- CSS TÙY CHỈNH ---
    ui.add_head_html('''
        <style>
            .glass-card {
                background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.4); box-shadow: 0 10px 30px -10px rgba(0, 100, 200, 0.15);
                transition: transform 0.4s ease, box-shadow 0.4s ease;
            }
            .glass-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px -10px rgba(0, 100, 200, 0.25); }
            @keyframes heartbeat {
                0%, 100% { transform: scale(1); filter: drop-shadow(0 0 15px rgba(34,197,94,0.6)); }
                50% { transform: scale(1.15); filter: drop-shadow(0 0 30px rgba(34,197,94,1)); }
            }
            .animate-heartbeat { animation: heartbeat 1.5s ease-in-out infinite; }
            .terminal-crt { position: relative; overflow: hidden; }
            .terminal-crt::after {
                content: " "; display: block; position: absolute; top: 0; left: 0; bottom: 0; right: 0;
                background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
                z-index: 2; background-size: 100% 4px, 6px 100%; pointer-events: none;
            }
        </style>
    ''')

    ui.query('body').classes(
        'bg-gradient-to-br from-slate-100 to-blue-50 min-h-screen p-4 md:p-8 font-sans text-gray-900 m-0')
    card_style = 'glass-card w-full rounded-3xl p-6 md:p-8'

    with ui.row().classes('w-full justify-between items-center mb-8 glass-card p-4 px-8 rounded-full'):
        with ui.row().classes('items-center gap-2'):
            ui.icon('precision_manufacturing',
                    size='md').classes('text-blue-600')
            ui.label('ROBOT ARM MONITOR').classes(
                'text-2xl font-extrabold text-gray-900 tracking-tight')
        with ui.row().classes('items-center gap-4'):
            status_badge = ui.badge('ĐANG CHẠY', color='green').classes(
                'bg-[#4CAF50] text-white text-sm px-4 py-2 font-black shadow-md rounded-full')
            ui.button('Đăng xuất', icon='logout', on_click=lambda: ui.navigate.to('/login')).props(
                'flat text-color=red').classes('font-bold hover:bg-red-50 rounded-full transition-colors')

    with ui.row().classes('w-full items-stretch gap-6 flex-wrap lg:flex-nowrap'):
        with ui.column().classes('w-full lg:w-[45%] gap-6 flex-1'):

            # --- KHỐI GIÁM SÁT KẾT NỐI (Đã có thể đổi màu) ---
            with ui.card().classes(card_style):
                ui.label('Giám Sát Kết Nối').classes(
                    'text-sm font-extrabold text-gray-400 tracking-widest uppercase mb-4')
                with ui.row().classes('w-full items-center justify-start p-6 bg-slate-900 rounded-2xl relative overflow-hidden border border-slate-700 shadow-2xl'):
                    bg_glow = ui.element('div').classes(
                        'absolute -right-10 -top-10 w-40 h-40 bg-red-500/30 blur-[50px] rounded-full transition-colors duration-1000')
                    status_icon = ui.icon('wifi_off', size='4rem').classes(
                        'text-red-500 z-10 mr-4')
                    with ui.column().classes('gap-1 z-10'):
                        status_text = ui.label(
                            'OFFLINE - MẤT KẾT NỐI').classes('text-xl font-black text-white tracking-wide')
                        status_subtext = ui.label('Đang chờ phần cứng khởi động...').classes(
                            'text-red-300 font-medium text-sm')

            with ui.card().classes(card_style):
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Nhật Ký Quét Màu').classes(
                        'text-sm font-extrabold text-gray-400 tracking-widest uppercase')
                    ui.icon('radar', size='1.5rem').classes(
                        'text-blue-500 animate-pulse')

                color_log = ui.log(max_lines=15).classes(
                    'terminal-crt w-full h-64 bg-slate-950 text-emerald-400 p-5 rounded-2xl font-mono text-sm shadow-inner border border-slate-800 tracking-wide leading-relaxed')

                # =======================================================
                # BỘ QUÉT TỰ ĐỘNG (Xử lý dữ liệu & kiểm tra trạng thái ESP)
                # =======================================================
                def cap_nhat_man_hinh():
                    # 1. Cập nhật dữ liệu màu
                    while len(hang_doi_esp32) > 0:
                        data = hang_doi_esp32.pop(0)
                        c_name, c_key = data.get(
                            'color_name', 'KHÔNG RÕ'), data.get('color_key', '')
                        r, g, b = data.get('r', 0), data.get(
                            'g', 0), data.get('b', 0)

                        time_str = datetime.now().strftime('%H:%M:%S')
                        color_log.push(
                            f"[{time_str}] 🤖 ESP32: Khối {c_name} | RGB({r},{g},{b})")
                        if c_key in thong_ke:
                            thong_ke[c_key] += 1
                            badge_red.set_text(str(thong_ke['red']))
                            badge_green.set_text(str(thong_ke['green']))
                            badge_blue.set_text(str(thong_ke['blue']))

                    # 2. KIỂM TRA NHỊP TIM ESP32 (Đã tăng thời gian chờ lên 15 giây)
                    if time.time() - thoi_gian_ping > 15:
                        # MẤT KẾT NỐI (ĐỔI SANG MÀU ĐỎ)
                        status_icon.name = 'wifi_off'  # Lệnh chuẩn để đổi hình icon
                        status_icon.classes(
                            replace='text-red-500', remove='text-green-400 animate-heartbeat')
                        bg_glow.classes(replace='bg-red-500/30',
                                        remove='bg-green-500/30')
                        status_text.set_text('OFFLINE - MẤT KẾT NỐI')
                        status_subtext.classes(replace='text-red-300', remove='text-green-300').set_text(
                            'Robot đang bận gắp vật hoặc mất mạng')
                    else:
                        # ONLINE (ĐỔI SANG MÀU XANH)
                        status_icon.name = 'settings_input_antenna'  # Lệnh chuẩn để đổi hình icon
                        status_icon.classes(
                            replace='text-green-400 animate-heartbeat', remove='text-red-500')
                        bg_glow.classes(replace='bg-green-500/30',
                                        remove='bg-red-500/30')
                        status_text.set_text('ONLINE - SẴN SÀNG HOẠT ĐỘNG')
                        status_subtext.classes(
                            replace='text-green-300', remove='text-red-300').set_text('Đang kết nối với phần cứng')

                ui.timer(0.5, cap_nhat_man_hinh)

        with ui.column().classes('w-full lg:w-[55%] gap-6 flex-1'):
            with ui.card().classes(card_style):
                ui.label('Thông Số Khớp Động Cơ (Servo Angles)').classes(
                    'text-sm font-extrabold text-gray-400 tracking-widest uppercase mb-6')
                with ui.row().classes('w-full justify-around items-center flex-wrap gap-y-8'):
                    for val, color, label in [(85, 'blue', '1 (Đế)'), (165, 'teal', '2 (Vai)'), (180, 'orange', '3 (Khuỷu)'), (120, 'rose', '4 (Cổ tay)'), (110, 'purple', 'Kẹp')]:
                        with ui.column().classes('items-center'):
                            ui.knob(value=val, min=0, max=180, show_value=True, track_color=f'{color}-50').props(
                                f'readonly size=75px color={color}-500 thickness=0.3')
                            ui.label(f'Trục {label}').classes(
                                'mt-3 font-extrabold text-gray-700 text-sm')

            with ui.card().classes(card_style):
                ui.label('Tổng Quan Sản Lượng').classes(
                    'text-sm font-extrabold text-gray-400 tracking-widest uppercase mb-6')
                with ui.column().classes('w-full gap-5 text-base font-bold'):
                    with ui.row().classes('w-full justify-between items-center pb-4 border-b border-gray-100'):
                        with ui.row().classes('items-center gap-3'):
                            ui.element('div').classes(
                                'w-4 h-4 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.6)]')
                            ui.label('Phân loại màu Đỏ')
                        badge_red = ui.badge('0', color='red').classes(
                            'text-lg px-4 py-1.5 rounded-lg shadow-sm')
                    with ui.row().classes('w-full justify-between items-center pb-4 border-b border-gray-100'):
                        with ui.row().classes('items-center gap-3'):
                            ui.element('div').classes(
                                'w-4 h-4 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.6)]')
                            ui.label('Phân loại màu Xanh lá')
                        badge_green = ui.badge('0', color='green').classes(
                            'text-lg px-4 py-1.5 rounded-lg shadow-sm')
                    with ui.row().classes('w-full justify-between items-center'):
                        with ui.row().classes('items-center gap-3'):
                            ui.element('div').classes(
                                'w-4 h-4 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.6)]')
                            ui.label('Phân loại màu Xanh dương')
                        badge_blue = ui.badge('0', color='blue').classes(
                            'text-lg px-4 py-1.5 rounded-lg shadow-sm')

            with ui.card().classes('w-full rounded-3xl p-6 bg-[#1e232d] shadow-2xl border-0'):
                def reset_du_lieu():
                    thong_ke['red'] = thong_ke['green'] = thong_ke['blue'] = 0
                    badge_red.set_text('0')
                    badge_green.set_text('0')
                    badge_blue.set_text('0')
                    color_log.clear()
                    color_log.push(
                        f"[{datetime.now().strftime('%H:%M:%S')}] HỆ THỐNG: Đã xóa toàn bộ dữ liệu.")
                ui.button('RESET TOÀN BỘ DỮ LIỆU', icon='delete', on_click=reset_du_lieu).classes(
                    'w-full py-3 rounded-xl font-black bg-[#5b9bd5] hover:bg-blue-400 text-white shadow-lg transition-all')
