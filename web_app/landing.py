from nicegui import ui


@ui.page('/')
def landing_page():
    ui.page_title('Robot ESP32 | Đồ án phân loại màu')

    # CSS Animation cho bức ảnh lơ lửng
    ui.add_head_html('''
        <style>
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
                100% { transform: translateY(0px); }
            }
            .animate-float {
                animation: float 4s ease-in-out infinite;
            }
        </style>
    ''')

    # Ép xóa lề trắng của trang để ảnh tràn viền tuyệt đối
    ui.query('body').classes(
        'bg-white text-gray-900 font-sans scroll-smooth m-0 p-0')
    ui.query('.q-page').style('padding: 0 !important; min-height: 100vh;')

    # ==============================================================
    # 1. THANH ĐIỀU HƯỚNG (NAVBAR)
    # ==============================================================
    with ui.row().classes('w-full justify-between items-center px-6 py-4 bg-gray-950/80 backdrop-blur-md fixed top-0 z-50 border-b border-gray-800'):
        with ui.row().classes('items-center gap-2 cursor-pointer'):
            ui.icon('precision_manufacturing',
                    size='md').classes('text-cyan-400')
            ui.label('Robot Control OS').classes(
                'text-2xl font-bold tracking-tight text-white')

        with ui.row().classes('hidden md:flex gap-8 text-sm font-medium text-gray-300'):
            ui.link('Sản phẩm', '#').classes(
                'hover:text-cyan-400 no-underline transition')
            ui.link('Về chúng tôi', '#').classes(
                'hover:text-cyan-400 no-underline transition')
            ui.link('Tài liệu', '#').classes(
                'hover:text-cyan-400 no-underline transition')
            ui.link('Liên hệ', '#').classes(
                'hover:text-cyan-400 no-underline transition')

        with ui.row().classes('items-center gap-4'):
            ui.button('Đăng nhập', on_click=lambda: ui.navigate.to('/login')) \
                .props('flat').classes('text-white font-bold hover:text-cyan-400')

            ui.button('Đăng ký', on_click=lambda: ui.navigate.to('/register')) \
                .classes('bg-cyan-500 hover:bg-cyan-400 text-gray-900 font-extrabold rounded-full px-6 py-2 transition shadow-lg shadow-cyan-500/30')

    # ==============================================================
    # 2. PHẦN NỘI DUNG CHÍNH (HERO SECTION)
    # ==============================================================
    bg_image_url = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=2000&auto=format&fit=crop"

    with ui.element('div').classes('relative w-full min-h-screen flex items-center pt-24 pb-32 m-0') \
            .style(f'background-image: url("{bg_image_url}"); background-size: cover; background-position: center;'):

        ui.element('div').classes('absolute inset-0 bg-gray-950/85 z-0')

        with ui.row().classes('w-full max-w-7xl mx-auto px-6 items-center justify-between gap-12 flex-wrap lg:flex-nowrap z-10'):

            with ui.column().classes('max-w-2xl flex-1'):
                with ui.row().classes('items-center gap-2 border border-cyan-500/30 bg-cyan-500/10 backdrop-blur-sm rounded-full px-4 py-1.5 mb-6'):
                    ui.icon('circle', size='10px').classes('text-cyan-400')
                    ui.label('Nền tảng điều khiển Cánh tay Robot').classes(
                        'text-cyan-300 text-xs font-bold tracking-wide')

                ui.html('''
                    <h1 style="font-size: 4.5rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 24px; color: #ffffff;">
                        Phân loại & điều khiển <br>
                        <span style="color: #06b6d4;">Robot Aim</span> của bạn
                    </h1>
                ''')

                ui.label('Theo dõi real-time, nhận diện màu sắc thông minh, và điều khiển trực tiếp qua giao diện Web. Ứng dụng công nghệ IoT ESP32 tối ưu hóa quá trình phân loại.') \
                  .classes('text-gray-300 text-lg mb-12 leading-relaxed font-medium max-w-xl')

                # THAY ĐỔI: Nhóm các nút vào một cột (column) có chiều rộng vừa vặn (w-fit)
                with ui.column().classes('gap-4 mb-10 w-fit'):

                    # Hàng 1: Chứa 2 nút đầu tiên
                    with ui.row().classes('gap-4 items-center flex-wrap justify-center'):
                        ui.button('ĐĂNG NHẬP HỆ THỐNG', on_click=lambda: ui.navigate.to('/login')) \
                          .classes('bg-cyan-500 hover:bg-cyan-400 text-gray-900 rounded-full px-8 py-3.5 font-extrabold shadow-lg shadow-cyan-500/40 transition-all tracking-wide')

                        ui.button('Hiểu hơn về chúng tôi', on_click=lambda: ui.run_javascript('document.getElementById("about-us").scrollIntoView({behavior: "smooth"})')) \
                          .props('flat') \
                          .classes('border-2 border-gray-400 hover:bg-white/10 text-white rounded-full px-8 py-3.5 font-bold transition-all')

                    # Hàng 2: Chứa nút thứ 3, dùng w-full và justify-center để căn chính giữa 2 nút trên
                    with ui.row().classes('w-full justify-center'):
                        ui.button('Xem cách hoạt động', on_click=lambda: ui.run_javascript('document.getElementById("how-it-works").scrollIntoView({behavior: "smooth"})')) \
                          .props('flat') \
                          .classes('border-2 border-gray-400 hover:bg-white/10 text-white rounded-full px-8 py-3.5 font-bold transition-all')

            with ui.column().classes('flex-1 w-full flex justify-center lg:justify-end mt-10 lg:mt-0 relative'):
                ui.element('div').classes(
                    'absolute inset-0 bg-cyan-500/30 blur-[100px] rounded-full scale-110 z-0')

                ui.image('assets/RobotAimimg.jpg').classes(
                    'animate-float object-cover h-[450px] w-full max-w-[500px] z-10 '
                    'rounded-2xl border-2 border-white/10 shadow-[0_0_50px_rgba(6,182,212,0.4)]'
                )

    # ==============================================================
    # 3. SECTION VỀ CHÚNG TÔI (ABOUT US)
    # ==============================================================
    with ui.element('div').classes('w-full bg-slate-50 py-24').props('id="about-us"'):
        with ui.row().classes('w-full max-w-7xl mx-auto px-6 gap-12 flex-wrap lg:flex-nowrap items-center'):

            # CỘT TRÁI: Text & Thông tin
            with ui.column().classes('w-full lg:w-1/2 gap-6'):
                ui.label('VỀ ĐỘI NGŨ PHÁT TRIỂN').classes(
                    'text-cyan-600 font-bold tracking-widest text-sm uppercase mb-[-10px]')
                ui.label('Khám phá những người đứng sau Robot Aim').classes(
                    'text-4xl md:text-5xl font-extrabold text-gray-900 leading-tight')

                ui.label('Dự án được nghiên cứu và chế tạo bởi nhóm 2 sinh viên năm 2 đến từ trường Đại học Bách Khoa TP.HCM: Vũ Chí Hưng và Đặng Hồng Anh. Với niềm đam mê mãnh liệt dành cho Robotics và IoT, chúng tôi mang đến một giải pháp tự động hóa thông minh, kết hợp trơn tru giữa phần cứng ESP32, vi điều khiển cơ khí và nền tảng quản lý Web hiện đại.') \
                  .classes('text-gray-600 text-lg leading-relaxed mt-4')

                # Các Icon
                with ui.row().classes('w-full gap-10 mt-6 justify-start flex-wrap'):
                    with ui.column().classes('items-center gap-2'):
                        ui.icon('hardware', size='2.5rem').classes(
                            'text-cyan-500')
                        ui.label('Phần Cứng').classes(
                            'font-bold text-gray-800 text-sm')

                    with ui.column().classes('items-center gap-2'):
                        ui.icon('webhook', size='2.5rem').classes(
                            'text-cyan-500')
                        ui.label('IoT & Web').classes(
                            'font-bold text-gray-800 text-sm')

                    with ui.column().classes('items-center gap-2'):
                        ui.icon('auto_awesome_motion', size='2.5rem').classes(
                            'text-cyan-500')
                        ui.label('Tự Động Hóa').classes(
                            'font-bold text-gray-800 text-sm')

            # CỘT PHẢI: Khung ghép 3 bức ảnh (ĐÃ FIX: Dùng thẻ <img> thuần HTML)
            with ui.element('div').classes('w-full lg:w-1/2 relative h-[500px] md:h-[550px] mt-10 lg:mt-0'):

                # Ảnh 1 (Trên cùng bên phải) - Đổi link ảnh trong thuộc tính src=""
                ui.element('img').props('src="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80"') \
                    .classes('absolute z-10 shadow-2xl transition-transform duration-300 hover:scale-[1.02]') \
                    .style('top: 0; right: 0; width: 60%; height: 260px; object-fit: cover; border-radius: 1.5rem; border: 6px solid white;')

                # Ảnh 2 (Ở giữa bên trái) - Đổi link ảnh trong thuộc tính src=""
                ui.element('img').props('src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=600&q=80"') \
                    .classes('absolute z-20 shadow-2xl transition-transform duration-300 hover:scale-[1.02]') \
                    .style('top: 20%; left: 0; width: 65%; height: 280px; object-fit: cover; border-radius: 1.5rem; border: 6px solid white;')

                # Ảnh 3 (Dưới cùng bên phải) - Đổi link ảnh trong thuộc tính src=""
                ui.element('img').props('src="https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=600&q=80"') \
                    .classes('absolute z-30 shadow-2xl transition-transform duration-300 hover:scale-[1.02]') \
                    .style('bottom: 0; right: 10%; width: 70%; height: 240px; object-fit: cover; border-radius: 1.5rem; border: 6px solid white;')

    # ==============================================================
    # 4. SECTION CÁCH HOẠT ĐỘNG
    # ==============================================================
    steps_data = [
        {
            "id": 1, "icon": "sensors", "title": "Quét Cảm Biến Màu", "step": "01 / 04",
            "desc": "Cảm biến màu TCS3200 (hoặc Camera) quét qua vật thể trên băng chuyền để thu thập thông số RGB chính xác của sản phẩm.",
            "media_type": "video",
            "media_url": "assets/video_test_mau.mp4"
        },
        {
            "id": 2, "icon": "memory", "title": "Xử Lý Qua ESP32", "step": "02 / 04",
            "desc": "Vi điều khiển ESP32 đọc dữ liệu thô, lọc nhiễu và phân tích mã màu (Đỏ, Xanh, Vàng...) với độ trễ cực thấp.",
            "media_type": "image",
            "media_url": "assets/anh_adruino.png"
        },
        {
            "id": 3, "icon": "dashboard", "title": "Cập Nhật Real-time", "step": "03 / 04",
            "desc": "Dữ liệu được đẩy ngay lập tức lên Web Dashboard qua WebSocket, hiển thị trạng thái và thông số hệ thống trực quan.",
            "media_type": "image",
            "media_url": "assets/anh_web.png"
        },
        {
            "id": 4, "icon": "precision_manufacturing", "title": "Điều Khiển Servo", "step": "04 / 04",
            "desc": "Hệ thống tự động tính toán tọa độ, gửi lệnh điều khiển các động cơ Servo xoay cánh tay robot gắp và thả vật vào đúng khay.",
            "media_type": "video",
            "media_url": "assets/video_test_servo.mp4"
        }
    ]

    active_step = steps_data[0]

    with ui.element('div').classes('w-full bg-white py-24').props('id="how-it-works"'):

        with ui.column().classes('w-full max-w-6xl mx-auto px-6 mb-16 items-center text-center gap-3'):
            ui.label('QUY TRÌNH HỆ THỐNG').classes(
                'text-cyan-600 font-bold tracking-widest text-sm uppercase')
            ui.label('Cách Cánh Tay Robot Vận Hành').classes(
                'text-4xl font-extrabold text-gray-900')
            ui.label('Từ cảm biến nhận diện màu sắc đến việc phối hợp điều khiển các động cơ Servo — một quy trình khép kín, tự động và thời gian thực.').classes(
                'text-gray-500 max-w-2xl text-lg')

        @ui.refreshable
        def render_interactive_steps():
            with ui.row().classes('w-full max-w-6xl mx-auto px-6 gap-8 flex-wrap lg:flex-nowrap items-stretch'):

                with ui.column().classes('w-full lg:w-[35%] gap-4'):
                    for step in steps_data:
                        is_active = (step['id'] == active_step['id'])
                        bg_style = 'bg-gray-900 text-white shadow-xl scale-[1.02]' if is_active else 'bg-transparent text-gray-500 hover:bg-gray-100'
                        icon_style = 'text-cyan-400' if is_active else 'text-gray-400'

                        with ui.row().classes(f'relative w-full items-center p-5 rounded-2xl cursor-pointer transition-all duration-300 {bg_style}').on('click', lambda s=step: change_step(s)):
                            ui.icon(step['icon'], size='sm').classes(
                                f'mr-3 {icon_style}')
                            ui.label(step['title']).classes(
                                'font-bold text-base md:text-lg')

                            if is_active:
                                ui.element('div').classes(
                                    'absolute right-4 top-1/2 -translate-y-1/2 w-1.5 h-6 bg-cyan-400 rounded-full')

                with ui.column().classes('w-full lg:w-[65%]'):
                    with ui.card().classes('w-full h-full rounded-3xl shadow-2xl border-0 p-8 md:p-10 bg-white flex flex-col justify-between'):

                        with ui.row().classes('items-center gap-4 mb-6'):
                            with ui.element('div').classes('p-3 rounded-2xl bg-cyan-50 text-cyan-600'):
                                ui.icon(active_step['icon'], size='md')
                            with ui.column().classes('gap-0'):
                                ui.label(active_step['step']).classes(
                                    'text-xs font-bold text-gray-400 font-mono tracking-widest')
                                ui.label(active_step['title']).classes(
                                    'text-2xl md:text-3xl font-extrabold text-gray-900 tracking-tight')

                        ui.label(active_step['desc']).classes(
                            'text-gray-600 text-lg leading-relaxed mb-10')

                        with ui.element('div').classes('w-full h-[350px] bg-gray-50 rounded-2xl flex items-center justify-center relative overflow-hidden border border-gray-100 shadow-inner'):

                            media_type = active_step.get('media_type', '')
                            media_url = active_step.get('media_url', '')

                            if media_type == 'video' and media_url:
                                # Đã thay object-cover thành object-contain
                                ui.video(media_url, autoplay=True, loop=True, muted=True).classes(
                                    'w-full h-full object-contain rounded-2xl')
                            elif media_type == 'image' and media_url:
                                # Đã thay object-cover thành object-contain
                                ui.image(media_url).classes(
                                    'w-full h-full object-contain rounded-2xl')
                            else:
                                with ui.column().classes('items-center justify-center gap-3'):
                                    ui.icon('smart_toy', size='4rem').classes(
                                        'text-gray-300')
                                    ui.label(
                                        'Khu Vực Chèn Sơ Đồ / Ảnh').classes('text-gray-400 font-medium')

        def change_step(new_step):
            nonlocal active_step
            active_step = new_step
            render_interactive_steps.refresh()

        render_interactive_steps()
