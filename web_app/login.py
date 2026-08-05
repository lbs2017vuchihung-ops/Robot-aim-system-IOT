from nicegui import ui
import database

# Khởi tạo Database an toàn
try:
    database.init_db()
except Exception as e:
    print(f"Lỗi khởi tạo Database: {e}")


@ui.page('/login')
def login_page():
    ui.query('body').classes(
        'bg-gradient-to-br from-blue-50 to-teal-50 min-h-screen flex items-center justify-center font-sans m-0')

    def try_login():
        try:
            user = username_input.value.strip() if username_input.value else ""
            pwd = password_input.value if password_input.value else ""

            if not user or not pwd:
                ui.notify('Vui lòng nhập đầy đủ thông tin!',
                          type='warning', position='top')
                return

            if database.verify_login(user, pwd):
                # Vẫn ghi lịch sử nhưng không dùng storage_secret nữa nên không bao giờ lỗi
                database.log_user_login(user)

                ui.notify('Đăng nhập thành công!',
                          type='positive', position='top')
                ui.navigate.to('/dashboard')
            else:
                ui.notify('Sai tên đăng nhập hoặc mật khẩu!',
                          type='negative', position='top')

        except Exception as e:
            ui.notify(
                f'Lỗi hệ thống: {str(e)}', type='negative', position='top', multi_line=True)

    def google_login_mock():
        ui.notify('Tính năng đang kết nối với Google API...',
                  type='info', position='top')

    with ui.card().classes('mt-6 w-full max-w-md p-10 flex flex-col items-center shadow-2xl rounded-2xl bg-white/90 backdrop-blur-sm mx-4 border border-gray-100'):
        ui.icon('precision_manufacturing', size='4rem').classes(
            'text-blue-600 mb-2')
        ui.label('Robot Control OS').classes(
            'text-3xl font-extrabold text-gray-900 tracking-tight mb-6')

        with ui.column().classes('w-full gap-4'):
            username_input = ui.input('Tên đăng nhập').classes(
                'w-full text-lg').props('outlined')
            password_input = ui.input('Mật khẩu', password=True, password_toggle_button=True).classes(
                'w-full text-lg').props('outlined')

        ui.space().classes('h-2')
        ui.button('ĐĂNG NHẬP', on_click=try_login).classes(
            'w-full py-3.5 rounded-xl text-base font-bold shadow-md hover:scale-[1.02] transition-transform duration-200 bg-blue-600 text-white')

        with ui.row().classes('w-full items-center gap-4 my-2'):
            ui.element('div').classes('flex-1 h-px bg-gray-200')
            ui.label('HOẶC').classes(
                'text-xs font-bold text-gray-400 tracking-widest')
            ui.element('div').classes('flex-1 h-px bg-gray-200')

        ui.button('Đăng nhập bằng Google', icon='login', on_click=google_login_mock) \
            .props('outline color=black') \
            .classes('w-full py-3.5 rounded-xl text-base font-bold hover:bg-gray-50 transition-colors text-gray-800 border-gray-300')

        ui.link('← Quay lại trang chủ', '/').classes(
            'mt-6 text-sm text-gray-500 font-medium hover:text-blue-600 transition')


@ui.page('/register')
def register_page():
    ui.query('body').classes(
        'bg-gradient-to-br from-blue-50 to-teal-50 min-h-screen flex items-center justify-center font-sans m-0')

    def try_register():
        try:
            user = reg_username_input.value.strip() if reg_username_input.value else ""
            pwd = reg_password_input.value if reg_password_input.value else ""
            confirm_pwd = reg_confirm_password_input.value

            if not user or not pwd or not confirm_pwd:
                ui.notify('Vui lòng nhập đầy đủ thông tin!',
                          type='warning', position='top')
                return

            if pwd != confirm_pwd:
                ui.notify('Mật khẩu xác nhận không khớp!',
                          type='negative', position='top')
                return

            success = database.add_user(user, pwd)

            if success:
                ui.notify('Đăng ký thành công! Đang chuyển đến Đăng nhập...',
                          type='positive', position='top')
                ui.navigate.to('/login')
            else:
                ui.notify('Tên tài khoản đã tồn tại! Vui lòng chọn tên khác.',
                          type='negative', position='top')
        except Exception as e:
            ui.notify(f'Lỗi hệ thống: {str(e)}',
                      type='negative', position='top')

    with ui.card().classes('mt-10 w-full max-w-md p-10 flex flex-col items-center shadow-2xl rounded-2xl bg-white/90 backdrop-blur-sm mx-4 border border-gray-100'):
        ui.icon('person_add', size='4rem').classes('text-blue-600 mb-2')
        ui.label('Đăng Ký Tài Khoản').classes(
            'text-3xl font-extrabold text-gray-900 tracking-tight mb-6')

        with ui.column().classes('w-full gap-4'):
            reg_username_input = ui.input('Tên đăng nhập').classes(
                'w-full text-lg').props('outlined')
            reg_password_input = ui.input('Mật khẩu', password=True, password_toggle_button=True).classes(
                'w-full text-lg').props('outlined')
            reg_confirm_password_input = ui.input(
                'Xác nhận lại Mật khẩu', password=True, password_toggle_button=True).classes('w-full text-lg').props('outlined')

        ui.space().classes('h-2')

        ui.button('ĐĂNG KÝ NGAY', on_click=try_register).classes(
            'w-full py-3.5 rounded-xl text-base font-bold shadow-md hover:scale-[1.02] transition-transform duration-200 bg-emerald-600 text-white')

        ui.link('← Đã có tài khoản? Quay lại Đăng nhập', '/login').classes(
            'mt-6 text-sm text-gray-500 font-medium hover:text-blue-600 transition')
        ui.link('← Quay lại trang chủ', '/').classes(
            'text-sm text-gray-500 font-medium hover:text-blue-600 transition')
