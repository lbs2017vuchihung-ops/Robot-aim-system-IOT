from nicegui import ui

import landing
import login
import dashboard

if __name__ in {"__main__", "__mp_main__"}:
    # BẮT BUỘC PHẢI CÓ DÒNG NÀY THÌ MỚI ĐĂNG NHẬP ĐƯỢC
    ui.run(storage_secret='chuyen_nganh_iot_k2', port=8080)
