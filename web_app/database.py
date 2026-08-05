import sqlite3
import hashlib

DB_NAME = 'robot_data.db'


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Bảng 1: Lưu thông tin tài khoản
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Bảng 2: (MỚI) Lưu lịch sử đăng nhập
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login_time DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # Tạo sẵn tài khoản admin nếu chưa có
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', hash_password('123456'), 'admin'))

    conn.commit()
    conn.close()


def verify_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_pw = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()

    return user is not None

# Hàm MỚI: Ghi nhận lịch sử mỗi lần đăng nhập


def log_user_login(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO login_logs (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

# Hàm thêm người dùng mới (Dành cho chức năng Đăng ký)


def add_user(username, password, role='user'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Lưu tên và mật khẩu (đã được mã hóa) vào DB
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hash_password(password), role))
        conn.commit()
        return True  # Đăng ký thành công
    except sqlite3.IntegrityError:
        return False  # Lỗi: Trùng tên đăng nhập
    finally:
        conn.close()
