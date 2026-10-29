"""
reset_admin.py  -  ตั้งรหัสผ่านแอดมินใหม่ (กรณีลืมรหัส)
วิธีใช้: ปิดโปรแกรมร้าน (project.py) และ DB Browser ก่อน แล้วกด Run ไฟล์นี้ใน VS Code
ไฟล์นี้ต้องอยู่โฟลเดอร์เดียวกับ coffee2_shop.db
"""
import hashlib
import os
import sqlite3
from datetime import datetime

from database import PASSWORD_HINT, password_problem     # กติการหัสผ่านเดียวกับในโปรแกรม

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coffee2_shop.db")


def hash_password(password):          # ต้องตรงกับ hash_password ใน project.py
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt.hex() + "$" + h.hex()


def main():
    if not os.path.exists(DB_PATH):
        print("ไม่พบไฟล์", DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS admins (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL, name TEXT NOT NULL, created_at TEXT NOT NULL)""")
    admins = conn.execute("SELECT username, name FROM admins ORDER BY admin_id").fetchall()

    print("=== ตั้งรหัสผ่านแอดมินใหม่ ===")
    if admins:
        print("บัญชีแอดมินที่มีอยู่:")
        for u, n in admins:
            print(f"  - {u}  ({n})")
    else:
        print("ยังไม่มีบัญชีแอดมิน จะสร้างบัญชีใหม่ให้")

    username = input("ชื่อผู้ใช้แอดมิน: ").strip().lower()
    if not username:
        print("ยกเลิก")
        return
    exists = any(u == username for u, _ in admins)
    if not exists:
        if input(f"ไม่มีชื่อผู้ใช้ '{username}' ต้องการสร้างใหม่ไหม (y/n): ").strip().lower() != "y":
            print("ยกเลิก")
            return

    while True:
        pw = input(f"รหัสผ่านใหม่ ({PASSWORD_HINT}, ระวังแป้นภาษาไทย): ")
        problem = password_problem(pw)
        if problem:
            print(f"  {problem} ลองใหม่")
            continue
        if input("พิมพ์รหัสผ่านใหม่อีกครั้ง: ") != pw:
            print("  รหัสสองครั้งไม่ตรงกัน ลองใหม่")
            continue
        break

    if exists:
        conn.execute("UPDATE admins SET password_hash = ? WHERE username = ?",
                     (hash_password(pw), username))
    else:
        name = input("ชื่อแอดมิน: ").strip() or username
        conn.execute("INSERT INTO admins (username, password_hash, name, created_at) VALUES (?, ?, ?, ?)",
                     (username, hash_password(pw), name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"\nเรียบร้อย! ใช้ชื่อผู้ใช้ '{username}' กับรหัสใหม่เข้าสู่ระบบแอดมินได้เลย")


if __name__ == "__main__":
    main()
