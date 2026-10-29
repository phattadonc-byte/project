"""
admin.py  -  ไฟล์ระบบแอดมิน / หลังร้าน (ไฟล์ 4 จาก 4) ของ Meme Beans Coffee

หน้าที่: บัญชีแอดมิน ภาพรวมร้าน คิวหลังร้าน (แจ้งสถานะออเดอร์ให้ลูกค้า) จัดการออเดอร์
         การชำระเงิน (ตรวจสลิปโอนเงิน) เมนู สมาชิก
         รายงานยอดขาย (ส่งออก Excel) และหน้าจอทั้งหมดของแอดมิน
ประกอบด้วย: ส่วนที่ 6 (ข้อมูลของแอดมิน) และส่วนที่ 20 (หน้าจอแอดมิน)
เชื่อมกับไฟล์อื่น: ดึงข้อมูลจาก database.py, รูปแบบเงินจาก receipt.py,
                  ปุ่ม การ์ด ฟอนต์ โลโก้จาก project.py
                  project.py เปิดหน้าแอดมินจากไฟล์นี้ตอนกด "เข้าสู่ระบบแอดมิน"
หมายเหตุ: project.py โหลดไฟล์นี้ตอนกดเข้าหน้าแอดมิน (ไม่ใช่ตอนเริ่มโปรแกรม)
          เพราะไฟล์นี้ใช้ปุ่ม/ฟอนต์จาก project.py จึงต้องรอให้ project.py โหลดเสร็จและเลือกฟอนต์ก่อน
เปิดโปรแกรมด้วยไฟล์ project.py
"""

import sqlite3
from datetime import date, datetime, timedelta
import os
import threading
import time
import zipfile
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox

# จากไฟล์ฐานข้อมูล: เชื่อมต่อฐานข้อมูล ค่าตั้งต้น และฟังก์ชันที่ใช้ร่วมกับฝั่งลูกค้า
from database import (
    BAHT_PER_POINT, BASE_DIR, DEFAULT_STOCK, IMAGE_DIR, LOW_STOCK_LEVEL, MAX_CUPS_PER_MENU,
    PAYMENT_METHODS, PREP_ACTIVE, PREP_LABEL, SHOP_NAME, TIERS, VAT_LABEL, VAT_RATE,
    fill_prep_details, get_categories, get_conn, get_slip_image, hash_password, mark_order_paid,
    order_amounts, prep_queue, redeemed_total, stock_status, thai_now, thai_today, tier_for,
    tier_progress, vat_split, verify_password, PASSWORD_HINT, password_problem, cancel_reset_code,
)

# จากไฟล์ใบเสร็จ: รูปแบบเงิน เลขออเดอร์ และวันที่
from receipt import (
    explain_email_error, fmt_datetime, fmt_price, money_rows, order_code, send_receipt_email,
)

# จากไฟล์หลัก: ฟอนต์ ปุ่ม การ์ด ช่องกรอก และโลโก้ (หน้าตาชุดเดียวกับฝั่งลูกค้า)
from project import (
    AVATAR_TYPES_PIL, AVATAR_TYPES_TK, DRINK_CARD, FONT, HAS_PIL, TIER_COLORS, aa_oval, bg_of,
    CustomerWindow, drink_color, icon_cup, LinkButton, load_product_image, logo_canvas,
    make_menu_png, member_initial, Pill, PillButton, png_photo_fit, rounded_rect, RoundEntry,
    RoundFrame, ScrollFrame, slip_photo,
)


# =====================================================================
# ส่วนที่ 6: ระบบแอดมิน (ฐานข้อมูล)
#   ประกอบด้วย: admin_exists, create_admin, login_admin, รายชื่อ/ลบแอดมิน (admin_list_admins, delete_admin),
#              change_admin_password, admin_stats, admin_list_orders,
#              admin_cancel_order, รูปเมนู (admin_save_product_image เก็บรูปเดิมไว้ที่ images/old_menu_images),
#              คิวหลังร้าน (admin_kitchen_orders, admin_kitchen_summary,
#              admin_set_prep_status, admin_call_customer, admin_toggle_item_done), การชำระเงิน/ตรวจสลิป (admin_list_slips, admin_approve_slip, admin_reject_slip,
#              admin_payment_summary, admin_list_payments), admin_list_products, admin_save_product, admin_add_category,
#              สต็อกสินค้า (admin_stock_alerts, admin_add_stock, admin_set_stock),
#              รูปเมนู (menu_image_stem, admin_save_product_image, เปลี่ยนชื่อเมนูแล้วเปลี่ยนชื่อไฟล์รูปตาม),
#              admin_list_members, แบนสมาชิก (admin_ban_member, admin_unban_member), admin_adjust_points,
#              ลบบัญชีสมาชิก (admin_member_delete_info, admin_delete_member),
#              ลบเมนู (admin_product_delete_info, admin_delete_product: เคยขายแล้ว = ซ่อนถาวร ยอดขายไม่หาย),
#              รายงานยอดขาย (admin_sales_report, export_report_xlsx, write_xlsx)
#   แก้ที่นี่เมื่อ: แก้กติกาของแอดมิน (บัญชีแอดมินเก็บในตาราง admins แยกจากสมาชิก) หรือรายงานยอดขาย
# บรรทัด 49 - 1133
# =====================================================================
_admin_fail = {"count": 0, "until": 0.0}      # กันเดารหัสแอดมิน: ผิด 5 ครั้งต้องรอ 30 วินาที
ADMIN_MAX_FAILS = 5
ADMIN_LOCK_SECONDS = 30


def admin_exists():
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0]
    conn.close()
    return n > 0


USERNAME_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789_.-"     # ตัวอักษรที่ใช้ในชื่อผู้ใช้แอดมินได้


def create_admin(username, password, name):
    """สร้างบัญชีแอดมิน คืนค่า (สำเร็จไหม, ข้อความ)"""
    username, name = username.strip().lower(), name.strip()
    if not name:
        return False, "กรุณากรอกชื่อแอดมิน"
    if len(username) < 3 or any(ch not in USERNAME_CHARS for ch in username):
        return False, "ชื่อผู้ใช้ต้องมีอย่างน้อย 3 ตัว เป็น a-z ตัวเลข _ . - เท่านั้น"
    problem = password_problem(password)        # กติกาเดียวกับสมาชิก (database.py)
    if problem:
        return False, problem
    conn = get_conn()
    try:
        conn.execute("INSERT INTO admins (username, password_hash, name, created_at) "
                     "VALUES (?, ?, ?, ?)",
                     (username, hash_password(password), name,
                      thai_now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True, "สร้างบัญชีแอดมินเรียบร้อย"
    except sqlite3.IntegrityError:
        return False, "ชื่อผู้ใช้นี้ถูกใช้แล้ว"
    finally:
        conn.close()


def login_admin(username, password):
    """ล็อกอินแอดมิน คืนค่า (ข้อมูลแอดมิน หรือ None, ข้อความ)"""
    now = time.time()
    if now < _admin_fail["until"]:
        return None, f"ลองผิดหลายครั้ง กรุณารออีก {int(_admin_fail['until'] - now) + 1} วินาที"
    conn = get_conn()
    row = conn.execute("SELECT admin_id, username, name, password_hash FROM admins "
                       "WHERE username = ?", (username.strip().lower(),)).fetchone()
    conn.close()
    # เผื่อคัดลอกรหัสมาแล้วติดช่องว่างหัว/ท้าย
    if row and (verify_password(password, row[3]) or
                (password.strip() != password and verify_password(password.strip(), row[3]))):
        _admin_fail["count"] = 0
        return {"admin_id": row[0], "username": row[1], "name": row[2]}, ""
    _admin_fail["count"] += 1
    if _admin_fail["count"] >= ADMIN_MAX_FAILS:
        _admin_fail["count"] = 0
        _admin_fail["until"] = now + ADMIN_LOCK_SECONDS
        return None, f"ลองผิดหลายครั้ง ระบบล็อก {ADMIN_LOCK_SECONDS} วินาที"
    return None, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"


def admin_list_admins():
    """รายชื่อแอดมินทั้งหมด (เรียงตามลำดับที่สร้าง)"""
    conn = get_conn()
    rows = conn.execute("SELECT admin_id, username, name, created_at FROM admins ORDER BY admin_id").fetchall()
    conn.close()
    return [{"admin_id": r[0], "username": r[1], "name": r[2], "created_at": r[3]} for r in rows]


def delete_admin(admin_id, current_admin_id):
    """ลบบัญชีแอดมิน คืนค่า (สำเร็จไหม, ข้อความ)  ลบตัวเองไม่ได้ และต้องเหลือแอดมินอย่างน้อย 1 คน"""
    if admin_id == current_admin_id:
        return False, "ลบบัญชีของตัวเองไม่ได้"
    conn = get_conn()
    try:
        if conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0] <= 1:
            return False, "ต้องมีแอดมินอย่างน้อย 1 คน"
        row = conn.execute("SELECT name FROM admins WHERE admin_id = ?", (admin_id,)).fetchone()
        if row is None:
            return False, "ไม่พบแอดมินคนนี้ (อาจถูกลบไปแล้ว)"
        conn.execute("DELETE FROM admins WHERE admin_id = ?", (admin_id,))
        conn.commit()
        return True, f"ลบแอดมิน {row[0]} แล้ว"
    finally:
        conn.close()


def change_admin_password(admin_id, old_password, new_password):
    problem = password_problem(new_password)
    if problem:
        return False, problem
    conn = get_conn()
    try:
        row = conn.execute("SELECT password_hash FROM admins WHERE admin_id = ?",
                           (admin_id,)).fetchone()
        if not row or not verify_password(old_password, row[0]):
            return False, "รหัสผ่านปัจจุบันไม่ถูกต้อง"
        conn.execute("UPDATE admins SET password_hash = ? WHERE admin_id = ?",
                     (hash_password(new_password), admin_id))
        conn.commit()
        return True, "เปลี่ยนรหัสผ่านเรียบร้อย"
    finally:
        conn.close()


def admin_stats():
    """ตัวเลขสรุปสำหรับหน้าภาพรวม (ยอดขายนับเฉพาะออเดอร์ที่ชำระแล้ว หลังหักส่วนลด ไม่นับภาษีที่บวกเพิ่ม)"""
    conn = get_conn()
    one = lambda sql, p=(): conn.execute(sql, p).fetchone()[0]
    day = lambda d: one("SELECT COALESCE(SUM(total_price - discount), 0) FROM orders "
                        "WHERE status = 'paid' AND substr(COALESCE(paid_at, order_date), 1, 10) = ?", (d,))
    today = thai_now().date()
    s = {
        "today_sales": day(today.isoformat()),
        "today_orders": one("SELECT COUNT(*) FROM orders WHERE status = 'paid' AND "
                            "substr(COALESCE(paid_at, order_date), 1, 10) = ?", (today.isoformat(),)),
        "members": one("SELECT COUNT(*) FROM members"),
        "total_sales": one("SELECT COALESCE(SUM(total_price - discount), 0) FROM orders WHERE status = 'paid'"),
        "paid_orders": one("SELECT COUNT(*) FROM orders WHERE status = 'paid'"),
        "total_discount": one("SELECT COALESCE(SUM(discount), 0) FROM orders WHERE status = 'paid'"),
        "products": one("SELECT COUNT(*) FROM products WHERE is_deleted = 0"),
        "unavailable": one("SELECT COUNT(*) FROM products WHERE is_available = 0 AND is_deleted = 0"),
        "unused_coupons": one("SELECT COUNT(*) FROM coupons WHERE status = 'unused'"),
    }
    s["last7"] = [((today - timedelta(days=i)).isoformat(), day((today - timedelta(days=i)).isoformat()))
                  for i in range(6, -1, -1)]
    s["top_products"] = [tuple(r) for r in conn.execute(
        "SELECT p.name, SUM(oi.quantity) AS qty, SUM(oi.quantity * oi.unit_price) AS money "
        "FROM order_items oi JOIN orders o ON o.order_id = oi.order_id "
        "JOIN products p ON p.product_id = oi.product_id WHERE o.status = 'paid' "
        "GROUP BY p.product_id ORDER BY qty DESC, p.product_id LIMIT 5").fetchall()]
    conn.close()
    return s


def admin_list_orders(status=None, limit=300):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    sql = ("SELECT o.order_id, o.order_date, o.paid_at, o.total_price, o.discount, o.vat, "
           "o.paid_total, o.status, o.prep_status, "
           "o.payment_method, m.name AS member_name, m.phone AS member_phone, "
           "(SELECT s.status FROM payment_slips s WHERE s.order_id = o.order_id "
           " ORDER BY s.slip_id DESC LIMIT 1) AS slip_status "
           "FROM orders o LEFT JOIN members m ON m.member_id = o.member_id ")
    params = []
    if status:
        sql += "WHERE o.status = ? "
        params.append(status)
    sql += "ORDER BY o.order_id DESC LIMIT ?"
    rows = [dict(r) for r in conn.execute(sql, params + [limit]).fetchall()]
    conn.close()
    return rows


def admin_cancel_order(order_id):
    """ยกเลิกออเดอร์ที่ยังรอชำระเท่านั้น (ออเดอร์ที่ชำระแล้วไม่แตะ เพราะมีแต้ม/ส่วนลดเกี่ยวข้อง)"""
    conn = get_conn()
    cur = conn.execute("UPDATE orders SET status = 'cancelled' "
                       "WHERE order_id = ? AND status = 'pending'", (order_id,))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def admin_cancel_all_pending():
    """ยกเลิกออเดอร์ค้างชำระทั้งหมด (ยกเว้นออเดอร์ที่ลูกค้าส่งสลิปแล้วและรอตรวจ)"""
    conn = get_conn()
    cur = conn.execute("UPDATE orders SET status = 'cancelled' WHERE status = 'pending' AND order_id NOT IN "
                       "(SELECT order_id FROM payment_slips WHERE status = 'waiting')")
    conn.commit()
    conn.close()
    return cur.rowcount


# ---------- คิวหลังร้าน: เปลี่ยนสถานะออเดอร์ที่ชำระแล้ว ลูกค้าเห็นทันทีและได้รับแจ้งเตือน ----------
# ทุกครั้งที่สถานะเปลี่ยน (หรือกด "เรียกลูกค้าอีกครั้ง") prep_seq จะเพิ่ม 1 ฝั่งลูกค้าเห็นเลขเปลี่ยนก็เด้งแจ้งเตือน
def admin_kitchen_orders():
    """ออเดอร์ที่ยังไม่จบ (รอคิว / กำลังทำ / พร้อมรับ) เรียงตามคิว พร้อมรายการแก้ว ชื่อ/เบอร์ลูกค้า
    และคิวก่อนหน้า (ดู fill_prep_details)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(
        "SELECT o.order_id, COALESCE(o.paid_at, o.order_date) AS paid_at, o.prep_status, o.prep_seq, "
        "o.prep_at, o.prep_by, o.ready_at, o.prep_calls, o.payment_method, "
        "COALESCE(o.paid_total, o.total_price - o.discount) AS paid, "
        "m.name AS member_name, m.phone AS member_phone "
        "FROM orders o LEFT JOIN members m ON m.member_id = o.member_id "
        "WHERE o.status = 'paid' AND o.prep_status IN ('queued', 'making', 'ready') "
        "ORDER BY COALESCE(o.paid_at, o.order_date), o.order_id").fetchall()]
    fill_prep_details(conn, rows)
    conn.close()
    return rows


def admin_kitchen_summary():
    """ตัวเลขบนหน้าคิวหลังร้าน: {queued, making, ready, picked_today, cups_waiting}"""
    conn = get_conn()
    counts = dict(conn.execute("SELECT prep_status, COUNT(*) FROM orders WHERE status = 'paid' "
                               "AND prep_status IN ('queued', 'making', 'ready') GROUP BY prep_status").fetchall())
    picked = conn.execute("SELECT COUNT(*) FROM orders WHERE prep_status = 'picked_up' "
                          "AND substr(picked_up_at, 1, 10) = ?", (thai_today().isoformat(),)).fetchone()[0]
    cups = sum(left for _, _, left in prep_queue(conn))
    conn.close()
    return {"queued": counts.get("queued", 0), "making": counts.get("making", 0),
            "ready": counts.get("ready", 0), "picked_today": picked, "cups_waiting": cups}


def admin_set_prep_status(order_id, status, admin_name=None):
    """เปลี่ยนสถานะหลังร้าน (เลื่อนไปขั้นถัดไป หรือย้อนกลับเมื่อกดผิด) แล้วแจ้งลูกค้า
    พร้อมรับ = ติ๊กทุกแก้วว่าเสร็จ  คืนค่า (สำเร็จไหม, ข้อความ)"""
    if status not in PREP_LABEL:
        return False, "สถานะไม่ถูกต้อง"
    conn = get_conn()
    try:
        row = conn.execute("SELECT status, prep_status FROM orders WHERE order_id = ?", (order_id,)).fetchone()
        if row is None or row[0] != "paid":
            return False, "ออเดอร์นี้ยังไม่ได้ชำระเงิน"
        if row[1] == status:
            return False, f"ออเดอร์นี้{PREP_LABEL[status]}อยู่แล้ว"
        now = thai_now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("UPDATE orders SET prep_status = ?, prep_at = ?, prep_by = ?, prep_seq = prep_seq + 1, "
                     "ready_at = CASE WHEN ? = 'ready' THEN ? WHEN ? IN ('queued', 'making') THEN NULL "
                     "ELSE ready_at END, "
                     "picked_up_at = CASE WHEN ? = 'picked_up' THEN ? ELSE NULL END, "
                     "prep_calls = CASE WHEN ? = 'ready' THEN 0 ELSE prep_calls END WHERE order_id = ?",
                     (status, now, admin_name, status, now, status, status, now, status, order_id))
        if status in ("ready", "picked_up"):
            conn.execute("UPDATE order_items SET done = 1 WHERE order_id = ?", (order_id,))
        elif status == "queued":
            conn.execute("UPDATE order_items SET done = 0 WHERE order_id = ?", (order_id,))
        conn.commit()
        return True, f"{order_code(order_id)}: {PREP_LABEL[status]}"
    finally:
        conn.close()


def admin_call_customer(order_id, admin_name=None):
    """เรียกลูกค้าอีกครั้ง (ออเดอร์ที่พร้อมรับแล้วแต่ลูกค้ายังไม่มารับ) คืนค่า (สำเร็จไหม, ข้อความ)"""
    conn = get_conn()
    cur = conn.execute("UPDATE orders SET prep_seq = prep_seq + 1, prep_calls = prep_calls + 1, "
                       "prep_at = ?, prep_by = ? WHERE order_id = ? AND status = 'paid' "
                       "AND prep_status = 'ready'",
                       (thai_now().strftime("%Y-%m-%d %H:%M:%S"), admin_name, order_id))
    conn.commit()
    conn.close()
    if not cur.rowcount:
        return False, "เรียกได้เฉพาะออเดอร์ที่พร้อมรับแล้ว"
    return True, f"เรียกลูกค้าออเดอร์ {order_code(order_id)} อีกครั้งแล้ว"


def admin_toggle_item_done(item_id, admin_name=None):
    """ติ๊ก/เอาติ๊กออก ว่าเครื่องดื่มรายการนี้ทำเสร็จแล้ว (ลูกค้าเห็นว่าเสร็จแล้วกี่แก้ว)
    ติ๊กแก้วแรกของออเดอร์ที่ยังรอคิว = เริ่มทำออเดอร์นั้นให้อัตโนมัติ (แจ้งลูกค้าว่ากำลังทำ)
    คืนค่า done ใหม่ (0/1) หรือ None ถ้าแก้ไม่ได้"""
    conn = get_conn()
    try:
        row = conn.execute("SELECT oi.order_id, oi.done, o.status, o.prep_status FROM order_items oi "
                           "JOIN orders o ON o.order_id = oi.order_id WHERE oi.item_id = ?", (item_id,)).fetchone()
        if row is None or row[2] != "paid" or row[3] not in ("queued", "making"):
            return None
        order_id, done = row[0], 0 if row[1] else 1
        conn.execute("UPDATE order_items SET done = ? WHERE item_id = ?", (done, item_id))
        if done and row[3] == "queued":
            conn.execute("UPDATE orders SET prep_status = 'making', prep_at = ?, prep_by = ?, "
                         "prep_seq = prep_seq + 1 WHERE order_id = ?",
                         (thai_now().strftime("%Y-%m-%d %H:%M:%S"), admin_name, order_id))
        conn.commit()
        return done
    finally:
        conn.close()


# ---------- การชำระเงิน: ตรวจสลิปโอนเงิน (QR พร้อมเพย์) + รายการรับชำระ ----------
# ลูกค้าจ่ายด้วย QR -> แนบสลิป (payment_slips สถานะ waiting) -> แอดมินตรวจที่หน้า "การชำระเงิน"
#   ยืนยันรับเงิน -> mark_order_paid (ตัดสต็อก ให้แต้ม ใช้ส่วนลด) เหมือนลูกค้าจ่ายเงินสด
#   สลิปไม่ผ่าน   -> ลูกค้าเห็นเหตุผลในโปรแกรม แล้วแนบสลิปใหม่หรือยกเลิกออเดอร์ได้
_SLIP_SELECT = ("SELECT s.slip_id, s.order_id, s.amount, s.coupon_id, s.email, s.status, s.note, "
                "s.submitted_at, s.checked_at, s.checked_by, o.status AS order_status, "
                "o.total_price, m.name AS member_name, m.phone AS member_phone, "
                "c.percent AS coupon_percent "
                "FROM payment_slips s JOIN orders o ON o.order_id = s.order_id "
                "LEFT JOIN members m ON m.member_id = o.member_id "
                "LEFT JOIN coupons c ON c.coupon_id = s.coupon_id ")


def admin_list_slips(status="waiting", limit=200):
    """สลิปโอนเงิน (ไม่รวมรูป) status=None = ทุกสถานะ  สลิปรอตรวจเรียงตามคิว (ส่งก่อนอยู่บน)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    if status == "waiting":
        sql = _SLIP_SELECT + "WHERE s.status = 'waiting' AND o.status = 'pending' ORDER BY s.slip_id LIMIT ?"
        params = [limit]
    elif status:
        sql = _SLIP_SELECT + "WHERE s.status = ? ORDER BY s.slip_id DESC LIMIT ?"
        params = [status, limit]
    else:
        sql = _SLIP_SELECT + "ORDER BY s.slip_id DESC LIMIT ?"
        params = [limit]
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def admin_get_slip(slip_id):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute(_SLIP_SELECT + "WHERE s.slip_id = ?", (slip_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def admin_order_slips(order_id):
    """สลิปทุกใบของออเดอร์ (ใบล่าสุดก่อน)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(_SLIP_SELECT + "WHERE s.order_id = ? ORDER BY s.slip_id DESC",
                                          (order_id,)).fetchall()]
    conn.close()
    return rows


def admin_approve_slip(slip_id, admin_name):
    """ยืนยันรับเงินตามสลิป: บันทึกการชำระเงิน (ตัดสต็อก ให้แต้ม ใช้ส่วนลดที่ลูกค้าเลือก) แล้วปิดสลิป
    คืนค่า (ผลจาก mark_order_paid, ออเดอร์, อีเมลที่ลูกค้าขอใบเสร็จ)  ทำไม่ได้จะ raise ValueError"""
    slip = admin_get_slip(slip_id)
    if slip is None:
        raise ValueError("ไม่พบสลิปนี้")
    if slip["status"] != "waiting":
        raise ValueError("สลิปนี้ตรวจไปแล้ว")
    result = mark_order_paid(slip["order_id"], dict(PAYMENT_METHODS)["qr"], slip["coupon_id"])
    conn = get_conn()
    conn.execute("UPDATE payment_slips SET status = 'approved', checked_at = ?, checked_by = ? "
                 "WHERE slip_id = ?", (thai_now().strftime("%Y-%m-%d %H:%M:%S"), admin_name, slip_id))
    conn.commit()
    conn.close()
    return result, slip["order_id"], slip["email"]


def admin_reject_slip(slip_id, note, admin_name):
    """แจ้งสลิปไม่ผ่าน พร้อมเหตุผล (ลูกค้าเห็นเหตุผลนี้ในโปรแกรม)  ทำไม่ได้จะ raise ValueError"""
    note = " ".join((note or "").split())
    if not note:
        raise ValueError("กรุณาระบุเหตุผลที่สลิปไม่ผ่าน")
    conn = get_conn()
    cur = conn.execute("UPDATE payment_slips SET status = 'rejected', note = ?, checked_at = ?, "
                       "checked_by = ? WHERE slip_id = ? AND status = 'waiting'",
                       (note[:200], thai_now().strftime("%Y-%m-%d %H:%M:%S"), admin_name, slip_id))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise ValueError("สลิปนี้ตรวจไปแล้ว")


def admin_payment_summary(day=None):
    """ยอดรับชำระของวัน (ค่าเริ่มต้น = วันนี้) แยกตามวิธีชำระ + สลิปที่รอตรวจ"""
    day = (day or thai_now().date()).isoformat()
    conn = get_conn()
    by_method = {}
    for method, n, money in conn.execute(
            f"SELECT o.payment_method, COUNT(*), COALESCE(SUM({_PAID_AMOUNT}), 0) FROM orders o "
            f"WHERE o.status = 'paid' AND {_PAID_DAY} = ? GROUP BY o.payment_method", (day,)):
        by_method[method or "-"] = (n, money)
    waiting = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(s.amount), 0) FROM payment_slips s "
        "JOIN orders o ON o.order_id = s.order_id WHERE s.status = 'waiting' AND o.status = 'pending'").fetchone()
    conn.close()
    return {"by_method": by_method, "count": sum(n for n, _ in by_method.values()),
            "total": sum(v for _, v in by_method.values()), "waiting": tuple(waiting)}


def admin_list_payments(limit=150):
    """รายการรับชำระเงินล่าสุด (ออเดอร์ที่ชำระแล้ว) + เลขสลิปที่ยืนยัน (ถ้าจ่ายด้วย QR)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(
        f"SELECT o.order_id, o.paid_at, o.order_date, o.payment_method, o.vat, {_PAID_AMOUNT} AS paid, "
        "m.name AS member_name, "
        "(SELECT s.slip_id FROM payment_slips s WHERE s.order_id = o.order_id AND s.status = 'approved' "
        " ORDER BY s.slip_id DESC LIMIT 1) AS slip_id "
        "FROM orders o LEFT JOIN members m ON m.member_id = o.member_id WHERE o.status = 'paid' "
        "ORDER BY COALESCE(o.paid_at, o.order_date) DESC, o.order_id DESC LIMIT ?", (limit,)).fetchall()]
    conn.close()
    return rows


def admin_list_products():
    """ทุกเมนู (ไม่รวมที่ลบแล้ว) + สต็อกคงเหลือ + ขายแล้ว (แก้ว) ทั้งหมด/วันนี้ (นับเฉพาะออเดอร์ที่ชำระแล้ว)
    + status: "ok" / "low" ใกล้หมด / "out" หมดแล้ว"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT p.product_id, p.category_id, c.name AS category, p.name, p.description, "
        "p.price, p.is_available, p.stock, "
        "COALESCE(SUM(CASE WHEN o.status = 'paid' THEN oi.quantity END), 0) AS sold, "
        "COALESCE(SUM(CASE WHEN o.status = 'paid' AND "
        "substr(COALESCE(o.paid_at, o.order_date), 1, 10) = ? THEN oi.quantity END), 0) AS sold_today "
        "FROM products p JOIN categories c ON c.category_id = p.category_id "
        "LEFT JOIN order_items oi ON oi.product_id = p.product_id "
        "LEFT JOIN orders o ON o.order_id = oi.order_id "
        "WHERE p.is_deleted = 0 "
        "GROUP BY p.product_id ORDER BY c.category_id, p.product_id",
        (thai_today().isoformat(),)).fetchall()
    conn.close()
    products = [dict(r) for r in rows]
    for p in products:
        p["status"] = stock_status(p["stock"])
    return products


def admin_stock_alerts():
    """เมนูที่เปิดขายอยู่แต่สต็อกใกล้หมด/หมดแล้ว (เรียงจากเหลือน้อยสุด)
    คืนค่า {"out": [ชื่อเมนู, ...], "low": [(ชื่อเมนู, คงเหลือ), ...]}"""
    conn = get_conn()
    rows = conn.execute("SELECT name, stock FROM products WHERE is_available = 1 AND is_deleted = 0 "
                        "AND stock <= ? "
                        "ORDER BY stock, product_id", (LOW_STOCK_LEVEL,)).fetchall()
    conn.close()
    return {"out": [name for name, stock in rows if stock <= 0],
            "low": [(name, stock) for name, stock in rows if stock > 0]}


def _stock_number(text, low, high, what):
    """แปลงจำนวนแก้วที่พิมพ์เป็นเลขจำนวนเต็ม คืนค่า (ตัวเลข, None) หรือ (None, ข้อความผิดพลาด)"""
    text = str(text).replace(",", "").strip()
    if not text.lstrip("-").isdigit():
        return None, f"{what}ต้องเป็นตัวเลขจำนวนเต็ม"
    n = int(text)
    if n < low or n > high:
        return None, f"{what}ต้องอยู่ระหว่าง {low:,} - {high:,} แก้ว"
    return n, None


def admin_add_stock(product_id, amount):
    """เติมสต็อกเพิ่ม amount แก้ว คืนค่า (สำเร็จไหม, สต็อกใหม่ หรือข้อความผิดพลาด)"""
    amount, err = _stock_number(amount, 1, 10000, "จำนวนที่เติม")
    if err:
        return False, err
    conn = get_conn()
    try:
        cur = conn.execute("UPDATE products SET stock = stock + ? WHERE product_id = ?", (amount, product_id))
        if cur.rowcount == 0:
            return False, "ไม่พบเมนูนี้"
        conn.commit()
        return True, conn.execute("SELECT stock FROM products WHERE product_id = ?",
                                  (product_id,)).fetchone()[0]
    finally:
        conn.close()


def admin_set_stock(product_id, value):
    """ตั้งจำนวนคงเหลือใหม่ (เช่น นับของจริงแล้วไม่ตรง) คืนค่า (สำเร็จไหม, สต็อกใหม่ หรือข้อความ)"""
    value, err = _stock_number(value, 0, 100000, "จำนวนคงเหลือ")
    if err:
        return False, err
    conn = get_conn()
    try:
        cur = conn.execute("UPDATE products SET stock = ? WHERE product_id = ?", (value, product_id))
        if cur.rowcount == 0:
            return False, "ไม่พบเมนูนี้"
        conn.commit()
        return True, value
    finally:
        conn.close()


# ---------- รูปเมนู: ไฟล์ images/<ชื่อเมนู>.png ไฟล์เดียวกับที่หน้าลูกค้าใช้แสดงบนการ์ดเมนู ----------
MENU_IMAGE_OLD_DIR = "old_menu_images"           # รูปเดิมที่ถูกเปลี่ยน ย้ายมาเก็บไว้ที่ images/old_menu_images
_BAD_FILE_CHARS = set('\\/:*?"<>|')


def menu_image_stem(name, product_id):
    """ชื่อไฟล์รูปเมนู (ไม่รวมนามสกุล) = ชื่อเมนู  ถ้าชื่อมีตัวอักษรที่ตั้งเป็นชื่อไฟล์ไม่ได้ ใช้เลข product_id แทน
    (หน้าลูกค้าหารูปจากทั้ง 2 ชื่อนี้)"""
    name = (name or "").strip()
    if not name or name.endswith(".") or any(ch in _BAD_FILE_CHARS for ch in name):
        return str(product_id)
    return name


def admin_save_product_image(product_id, png):
    """บันทึกรูปเมนู (PNG) ให้หน้าลูกค้าใช้ทันที  รูปเดิมย้ายไปเก็บที่ images/old_menu_images
    คืนค่า (สำเร็จไหม, ที่อยู่ไฟล์ หรือข้อความผิดพลาด)"""
    if not png or not png.startswith(b"\x89PNG"):
        return False, "ไฟล์รูปไม่ถูกต้อง"
    conn = get_conn()
    row = conn.execute("SELECT name FROM products WHERE product_id = ?", (product_id,)).fetchone()
    conn.close()
    if row is None:
        return False, "ไม่พบเมนูนี้"
    stem = menu_image_stem(row[0], product_id)
    path = os.path.join(IMAGE_DIR, stem + ".png")
    try:
        os.makedirs(IMAGE_DIR, exist_ok=True)
        if os.path.exists(path):
            old_dir = os.path.join(IMAGE_DIR, MENU_IMAGE_OLD_DIR)
            os.makedirs(old_dir, exist_ok=True)
            os.replace(path, os.path.join(old_dir, f"{stem}_{thai_now():%Y%m%d_%H%M%S}.png"))
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(png)
        os.replace(tmp, path)
    except OSError as e:
        return False, f"บันทึกรูปไม่สำเร็จ: {e}"
    return True, path


def _rename_menu_image(product_id, old_name, new_name):
    """เปลี่ยนชื่อเมนูแล้ว เปลี่ยนชื่อไฟล์รูปตามด้วย (รูปจะได้ไม่หายจากหน้าลูกค้า)"""
    old_stem, new_stem = menu_image_stem(old_name, product_id), menu_image_stem(new_name, product_id)
    if old_stem == new_stem:
        return
    for ext in (".png", ".gif"):
        old, new = os.path.join(IMAGE_DIR, old_stem + ext), os.path.join(IMAGE_DIR, new_stem + ext)
        try:
            if os.path.exists(old) and not os.path.exists(new):
                os.replace(old, new)
        except OSError:
            pass


def admin_save_product(product_id, category_id, name, description, price, available, stock=None, image=None):
    """เพิ่ม (product_id=None) หรือแก้ไขเมนู คืนค่า (สำเร็จไหม, ข้อความ)
    stock = สต็อกเริ่มต้นของเมนูใหม่ (ไม่ระบุ = DEFAULT_STOCK)  เมนูเดิมเติมสต็อกด้วยปุ่ม "+ เติมสต็อก"
    image = รูปเมนูใหม่ (PNG จาก make_menu_png) ไม่ระบุ = ใช้รูปเดิม"""
    name = name.strip()
    if not name:
        return False, "กรุณากรอกชื่อเมนู"
    try:
        price = float(str(price).replace(",", "").strip())
    except ValueError:
        return False, "ราคาต้องเป็นตัวเลข"
    if price < 0:
        return False, "ราคาต้องไม่ติดลบ"
    if product_id is None:
        stock, err = _stock_number(DEFAULT_STOCK if stock in (None, "") else stock, 0, 100000, "สต็อกเริ่มต้น")
        if err:
            return False, err
    conn = get_conn()
    try:
        if conn.execute("SELECT 1 FROM products WHERE lower(name) = lower(?) AND product_id IS NOT ? "
                        "AND is_deleted = 0",
                        (name, product_id)).fetchone():
            return False, "มีเมนูชื่อนี้อยู่แล้ว"
        old_name = None
        if product_id is None:
            cur = conn.execute("INSERT INTO products (category_id, name, description, price, is_available, stock) "
                               "VALUES (?, ?, ?, ?, ?, ?)",
                               (category_id, name, description.strip(), price, 1 if available else 0, stock))
            product_id = cur.lastrowid
        else:
            row = conn.execute("SELECT name FROM products WHERE product_id = ?", (product_id,)).fetchone()
            old_name = row[0] if row else None
            conn.execute("UPDATE products SET category_id = ?, name = ?, description = ?, price = ?, "
                         "is_available = ? WHERE product_id = ?",
                         (category_id, name, description.strip(), price, 1 if available else 0, product_id))
        conn.commit()
    finally:
        conn.close()
    if old_name and old_name != name:
        _rename_menu_image(product_id, old_name, name)
    if image is not None:
        ok, err = admin_save_product_image(product_id, image)
        if not ok:
            return True, f"บันทึกเมนูแล้ว แต่{err}"
    return True, "บันทึกเมนูเรียบร้อย"


def admin_set_available(product_id, available):
    conn = get_conn()
    conn.execute("UPDATE products SET is_available = ? WHERE product_id = ?",
                 (1 if available else 0, product_id))
    conn.commit()
    conn.close()


def admin_add_category(name):
    name = name.strip()
    if not name:
        return False, "กรุณากรอกชื่อหมวดหมู่"
    conn = get_conn()
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        return True, "เพิ่มหมวดหมู่เรียบร้อย"
    except sqlite3.IntegrityError:
        return False, "มีหมวดหมู่นี้อยู่แล้ว"
    finally:
        conn.close()


# ---------- ลบเมนู ----------
# เมนูที่ยังไม่เคยมีใครสั่ง = ลบแถวทิ้งจริง
# เมนูที่เคยถูกสั่งแล้ว = ซ่อนถาวร (is_deleted = 1, ปิดขาย, สต็อก 0) แถวยังอยู่ ประวัติออเดอร์ ใบเสร็จ
#   คิวหลังร้าน และรายงานยอดขายจึงยังแสดงชื่อเมนูนี้ได้ ยอดขายไม่เปลี่ยน
# ลบไม่ได้ถ้ายังมีออเดอร์ที่ยังไม่ชำระเงิน (กำลังชำระ/รอตรวจสลิป) สั่งเมนูนี้อยู่
# รูปเมนูย้ายไปเก็บที่ images/old_menu_images ชื่อเมนูเดิมจึงใช้ตั้งเมนูใหม่ได้
def _pending_orders_with(conn, product_id):
    """จำนวนออเดอร์ที่ยังไม่ชำระเงินที่มีเมนูนี้"""
    return conn.execute("SELECT COUNT(DISTINCT o.order_id) FROM order_items oi "
                        "JOIN orders o ON o.order_id = oi.order_id "
                        "WHERE oi.product_id = ? AND o.status = 'pending'", (product_id,)).fetchone()[0]


def admin_product_delete_info(product_id):
    """ข้อมูลก่อนลบเมนู: ชื่อ สต็อก เคยถูกสั่งไหม แก้วที่ขายแล้ว ออเดอร์ที่ยังไม่ชำระ/อยู่ในคิวหลังร้าน
    ไม่พบ (หรือลบไปแล้ว) คืนค่า None"""
    conn = get_conn()
    try:
        row = conn.execute("SELECT name, stock FROM products WHERE product_id = ? AND is_deleted = 0",
                           (product_id,)).fetchone()
        if row is None:
            return None
        one = lambda sql, p=(): conn.execute(sql, (product_id,) + p).fetchone()[0]
        return {
            "name": row[0],
            "stock": row[1],
            "lines": one("SELECT COUNT(*) FROM order_items WHERE product_id = ?"),
            "sold": one("SELECT COALESCE(SUM(oi.quantity), 0) FROM order_items oi "
                        "JOIN orders o ON o.order_id = oi.order_id "
                        "WHERE oi.product_id = ? AND o.status = 'paid'"),
            "pending": _pending_orders_with(conn, product_id),
            "in_queue": one("SELECT COUNT(DISTINCT o.order_id) FROM order_items oi "
                            "JOIN orders o ON o.order_id = oi.order_id WHERE oi.product_id = ? "
                            f"AND o.status = 'paid' AND o.prep_status IN ({','.join('?' * len(PREP_ACTIVE))})",
                            tuple(PREP_ACTIVE)),
        }
    finally:
        conn.close()


def _archive_menu_image(product_id, name):
    """ย้ายรูปของเมนูที่ถูกลบไปเก็บที่ images/old_menu_images (ไม่ลบทิ้ง)"""
    stamp = thai_now().strftime("%Y%m%d_%H%M%S")
    for stem in dict.fromkeys((menu_image_stem(name, product_id), str(product_id))):
        for ext in (".png", ".gif"):
            path = os.path.join(IMAGE_DIR, stem + ext)
            try:
                if os.path.exists(path):
                    old_dir = os.path.join(IMAGE_DIR, MENU_IMAGE_OLD_DIR)
                    os.makedirs(old_dir, exist_ok=True)
                    os.replace(path, os.path.join(old_dir, f"{stem}_ลบเมนู_{stamp}{ext}"))
            except OSError:
                pass


def admin_delete_product(product_id):
    """ลบเมนู คืนค่า (สำเร็จไหม, ข้อความ)"""
    conn = get_conn()
    try:
        with conn:
            row = conn.execute("SELECT name FROM products WHERE product_id = ? AND is_deleted = 0",
                               (product_id,)).fetchone()
            if row is None:
                return False, "ไม่พบเมนูนี้ (อาจถูกลบไปแล้ว)"
            name = row[0]
            pending = _pending_orders_with(conn, product_id)
            if pending:
                return False, (f"ยังลบไม่ได้ มีออเดอร์ที่ยังไม่ชำระเงินสั่ง {name} อยู่ {pending} ออเดอร์ "
                               "รอให้ชำระเสร็จหรือยกเลิกที่หน้าออเดอร์ก่อน")
            used = conn.execute("SELECT 1 FROM order_items WHERE product_id = ? LIMIT 1",
                                (product_id,)).fetchone() is not None
            if used:
                conn.execute("UPDATE products SET is_deleted = 1, is_available = 0, stock = 0 "
                             "WHERE product_id = ?", (product_id,))
            else:
                conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    finally:
        conn.close()
    _archive_menu_image(product_id, name)
    return True, f"ลบเมนู {name} แล้ว" + (" (ยอดขายเดิมยังอยู่ในรายงาน)" if used else "")


def admin_list_members():
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT m.member_id, m.name, m.phone, m.email, m.points, m.tier, m.joined_date, "
        "m.banned, m.ban_reason, m.banned_at, m.banned_by, "
        "(SELECT COUNT(*) FROM orders o WHERE o.member_id = m.member_id AND o.status = 'paid') AS orders, "
        "(SELECT COALESCE(SUM(COALESCE(o.paid_total, o.total_price - o.discount)), 0) FROM orders o "
        " WHERE o.member_id = m.member_id AND o.status = 'paid') AS spent, "
        "(SELECT COUNT(*) FROM coupons c WHERE c.member_id = m.member_id AND c.status = 'unused') AS coupons, "
        "m.points + (SELECT COALESCE(-SUM(ph.points), 0) FROM point_history ph "
        " WHERE ph.member_id = m.member_id AND ph.type = 'redeem') AS lifetime "      # แต้มสะสมทั้งหมด (ใช้วัดระดับ)
        "FROM members m ORDER BY m.member_id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def admin_ban_member(member_id, reason, admin_name):
    """แบนสมาชิก: เข้าสู่ระบบและสั่งซื้อไม่ได้ (ข้อมูล/แต้ม/ประวัติยังอยู่ครบ ยกเลิกการแบนได้)
    ต้องระบุเหตุผล (สมาชิกจะเห็นตอนเข้าสู่ระบบ) คืนค่า (สำเร็จไหม, ข้อความ)"""
    reason = " ".join((reason or "").split())
    if not reason:
        return False, "กรุณาระบุเหตุผลที่แบน"
    conn = get_conn()
    cur = conn.execute("UPDATE members SET banned = 1, ban_reason = ?, banned_at = ?, banned_by = ? "
                       "WHERE member_id = ?",
                       (reason[:200], thai_now().strftime("%Y-%m-%d %H:%M:%S"), admin_name, member_id))
    conn.commit()
    conn.close()
    return (True, "แบนสมาชิกแล้ว") if cur.rowcount else (False, "ไม่พบสมาชิกคนนี้")


def admin_unban_member(member_id):
    conn = get_conn()
    conn.execute("UPDATE members SET banned = 0, ban_reason = NULL, banned_at = NULL, banned_by = NULL "
                 "WHERE member_id = ?", (member_id,))
    conn.commit()
    conn.close()
    return True, "ยกเลิกการแบนแล้ว สมาชิกเข้าสู่ระบบได้ตามปกติ"


def admin_adjust_points(member_id, delta):
    """เพิ่ม/ลดแต้มสมาชิก (แต้มไม่ต่ำกว่า 0) บันทึกประวัติเป็น 'adjust' คืนค่า (สำเร็จไหม, แต้มใหม่หรือข้อความ)"""
    conn = get_conn()
    try:
        row = conn.execute("SELECT points FROM members WHERE member_id = ?", (member_id,)).fetchone()
        if row is None:
            return False, "ไม่พบสมาชิก"
        new = max(0, row[0] + delta)
        real = new - row[0]
        tier = tier_for(new + redeemed_total(conn, member_id))
        conn.execute("UPDATE members SET points = ?, tier = ? WHERE member_id = ?", (new, tier, member_id))
        if real:
            conn.execute("INSERT INTO point_history (member_id, order_id, points, type, created_at) "
                         "VALUES (?, NULL, ?, 'adjust', ?)",
                         (member_id, real, thai_now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True, new
    finally:
        conn.close()


# ---------- ลบบัญชีสมาชิก ----------
# ลบถาวร: ชื่อ เบอร์ อีเมล รหัสผ่าน รูปโปรไฟล์ แต้ม คูปอง ประวัติแต้ม (ออเดอร์ที่ยังไม่ชำระถูกยกเลิก)
# เก็บไว้: ออเดอร์ที่ชำระแล้ว + สลิปของออเดอร์นั้น (ไม่ผูกกับสมาชิกแล้ว แสดงเป็น "ลูกค้าทั่วไป")
#          ยอดขายในรายงานจึงไม่เปลี่ยน  เลขสมาชิกไม่ถูกนำกลับมาใช้ซ้ำ (AUTOINCREMENT)
def admin_member_delete_info(member_id):
    """ข้อมูลประกอบการลบบัญชี: สิ่งที่จะหาย สิ่งที่ยังอยู่ และงานที่ยังค้าง  คืนค่า dict หรือ None ถ้าไม่พบสมาชิก
    waiting_slips / in_queue มากกว่า 0 = ยังลบไม่ได้ (ต้องตรวจสลิปหรือส่งเครื่องดื่มให้เสร็จก่อน)"""
    conn = get_conn()
    try:
        m = conn.execute("SELECT name, phone, points FROM members WHERE member_id = ?",
                         (member_id,)).fetchone()
        if m is None:
            return None

        def one(sql):
            return conn.execute(sql, (member_id,)).fetchone()[0]

        return {
            "name": m[0], "phone": m[1], "points": m[2],
            "coupons": one("SELECT COUNT(*) FROM coupons WHERE member_id = ? AND status = 'unused'"),
            "paid_orders": one("SELECT COUNT(*) FROM orders WHERE member_id = ? AND status = 'paid'"),
            "spent": one("SELECT COALESCE(SUM(COALESCE(paid_total, total_price - discount)), 0) "
                         "FROM orders WHERE member_id = ? AND status = 'paid'"),
            "unpaid": one("SELECT COUNT(*) FROM orders WHERE member_id = ? AND status = 'pending'"),
            "waiting_slips": one("SELECT COUNT(*) FROM payment_slips s JOIN orders o ON o.order_id = s.order_id "
                                 "WHERE o.member_id = ? AND o.status = 'pending' AND s.status = 'waiting'"),
            "in_queue": one("SELECT COUNT(*) FROM orders WHERE member_id = ? AND status = 'paid' "
                            "AND prep_status IN ('queued', 'making', 'ready')"),
        }
    finally:
        conn.close()


def admin_delete_member(member_id, confirm_phone):
    """ลบบัญชีสมาชิกถาวร ต้องพิมพ์เบอร์โทรของสมาชิกให้ตรงเพื่อยืนยัน  คืนค่า (สำเร็จไหม, ข้อความ)
    ลบไม่ได้ถ้ายังมีสลิปรอตรวจ หรือออเดอร์ที่ชำระแล้วยังอยู่ในคิวหลังร้าน"""
    info = admin_member_delete_info(member_id)
    if info is None:
        return False, "ไม่พบสมาชิกคนนี้ (อาจถูกลบไปแล้ว)"
    if (confirm_phone or "").strip() != info["phone"]:
        return False, "เบอร์โทรที่พิมพ์ไม่ตรงกับเบอร์ของสมาชิก"
    if info["waiting_slips"] or info["in_queue"]:
        return False, "ยังลบไม่ได้: มีสลิปรอตรวจหรือออเดอร์ในคิวหลังร้าน ให้จัดการให้เสร็จก่อน"
    conn = get_conn()
    try:
        with conn:                  # ทำทุกขั้นพร้อมกัน ถ้าขั้นไหนผิดพลาด ข้อมูลย้อนกลับเหมือนเดิมทั้งหมด
            conn.execute("UPDATE orders SET status = 'cancelled' WHERE member_id = ? AND status = 'pending'",
                         (member_id,))
            # สลิปของออเดอร์ที่ไม่ได้ชำระ (ถูกปฏิเสธ/ยกเลิก) ลบทิ้ง  สลิปของออเดอร์ที่ชำระแล้วเก็บไว้เป็นหลักฐาน
            conn.execute("DELETE FROM payment_slips WHERE order_id IN "
                         "(SELECT order_id FROM orders WHERE member_id = ? AND status <> 'paid')", (member_id,))
            conn.execute("UPDATE payment_slips SET email = NULL WHERE order_id IN "
                         "(SELECT order_id FROM orders WHERE member_id = ?)", (member_id,))
            conn.execute("DELETE FROM point_history WHERE member_id = ?", (member_id,))
            conn.execute("DELETE FROM coupons WHERE member_id = ?", (member_id,))
            conn.execute("UPDATE orders SET member_id = NULL WHERE member_id = ?", (member_id,))
            conn.execute("DELETE FROM members WHERE member_id = ?", (member_id,))
    finally:
        conn.close()
    cancel_reset_code(member_id)            # รหัสลืมรหัสผ่านที่ค้างอยู่ใช้ไม่ได้แล้ว
    return True, f"ลบบัญชี {info['name']} ({info['phone']}) แล้ว"


# ---------- รายงานยอดขาย ----------
REPORT_DIR = os.path.join(BASE_DIR, "reports")      # โฟลเดอร์เริ่มต้นสำหรับไฟล์รายงานที่ส่งออก
_PAID_DAY = "substr(COALESCE(o.paid_at, o.order_date), 1, 10)"     # วันที่ขาย (ใช้วันที่ชำระเงิน)
_PAID_AMOUNT = "COALESCE(o.paid_total, o.total_price - o.discount)"  # เงินที่ลูกค้าจ่ายจริง (รวมภาษี)


def first_sale_date():
    """วันที่มียอดขายวันแรก (YYYY-MM-DD) ยังไม่มียอดขายคืนค่าวันนี้"""
    conn = get_conn()
    d = conn.execute(f"SELECT MIN({_PAID_DAY}) FROM orders o WHERE o.status = 'paid'").fetchone()[0]
    conn.close()
    return d or thai_today().isoformat()


def admin_sales_report(date_from, date_to, group="day"):
    """สรุปยอดขายตั้งแต่ date_from ถึง date_to (YYYY-MM-DD รวมทั้งสองวัน) นับเฉพาะออเดอร์ที่ชำระแล้ว
    group = "day" (รายวัน) หรือ "month" (รายเดือน)
    คืนค่า dict: summary, periods, products, payments, hours"""
    where = f"o.status = 'paid' AND {_PAID_DAY} BETWEEN ? AND ?"
    rng = (date_from, date_to)
    n = 10 if group == "day" else 7
    conn = get_conn()
    try:
        orders, gross, disc, vat, paid = conn.execute(
            f"SELECT COUNT(*), COALESCE(SUM(o.total_price), 0), COALESCE(SUM(o.discount), 0), "
            f"COALESCE(SUM(o.vat), 0), COALESCE(SUM({_PAID_AMOUNT}), 0) "
            f"FROM orders o WHERE {where}", rng).fetchone()
        cups = conn.execute(
            f"SELECT COALESCE(SUM(oi.quantity), 0) FROM order_items oi "
            f"JOIN orders o ON o.order_id = oi.order_id WHERE {where}", rng).fetchone()[0]
        cups_by = dict(conn.execute(
            f"SELECT substr({_PAID_DAY}, 1, {n}) AS period, SUM(oi.quantity) FROM order_items oi "
            f"JOIN orders o ON o.order_id = oi.order_id WHERE {where} GROUP BY period", rng).fetchall())
        periods = [(k, cnt, cups_by.get(k, 0), g, d, nv, v, pd) for k, cnt, g, d, nv, v, pd in conn.execute(
            f"SELECT substr({_PAID_DAY}, 1, {n}) AS period, COUNT(*), SUM(o.total_price), "
            f"SUM(o.discount), SUM(o.total_price - o.discount), SUM(o.vat), SUM({_PAID_AMOUNT}) "
            f"FROM orders o WHERE {where} GROUP BY period ORDER BY period", rng).fetchall()]
        products = conn.execute(
            f"SELECT p.name, SUM(oi.quantity) AS qty, SUM(oi.quantity * oi.unit_price) AS money "
            f"FROM order_items oi JOIN orders o ON o.order_id = oi.order_id "
            f"JOIN products p ON p.product_id = oi.product_id WHERE {where} "
            f"GROUP BY p.product_id ORDER BY qty DESC, money DESC, p.name", rng).fetchall()
        payments = conn.execute(
            f"SELECT COALESCE(o.payment_method, '-'), COUNT(*), SUM(o.total_price - o.discount) "
            f"FROM orders o WHERE {where} GROUP BY 1 ORDER BY 3 DESC", rng).fetchall()
        hours = conn.execute(
            f"SELECT substr(COALESCE(o.paid_at, o.order_date), 12, 2) AS hh, COUNT(*), "
            f"SUM(o.total_price - o.discount) FROM orders o WHERE {where} "
            f"GROUP BY hh ORDER BY hh", rng).fetchall()
    finally:
        conn.close()

    # เติมวัน/เดือนที่ไม่มียอดขายเป็น 0 ให้ตารางต่อเนื่อง (ช่วงไม่ยาวเกินไป)
    found = {r[0]: r for r in periods}
    keys = []
    d0, d1 = date.fromisoformat(date_from), date.fromisoformat(date_to)
    if group == "day" and 0 <= (d1 - d0).days <= 92:
        keys = [(d0 + timedelta(days=i)).isoformat() for i in range((d1 - d0).days + 1)]
    elif group == "month" and d0 <= d1 and (d1.year - d0.year) * 12 + d1.month - d0.month <= 60:
        y, m = d0.year, d0.month
        while (y, m) <= (d1.year, d1.month):
            keys.append(f"{y:04d}-{m:02d}")
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    if keys:
        periods = [found.get(k, (k, 0, 0, 0, 0, 0, 0, 0)) for k in keys] + \
                  [r for r in periods if r[0] not in set(keys)]
    net = gross - disc
    return {
        "from": date_from, "to": date_to, "group": group,
        "summary": {"orders": orders, "cups": cups, "gross": gross, "discount": disc, "net": net,
                    "vat": vat, "paid": paid, "avg": (net / orders) if orders else 0},
        # (ช่วง, ออเดอร์, แก้ว, ก่อนลด, ส่วนลด, สุทธิ, ภาษี, รับชำระรวมภาษี)
        "periods": [tuple(r) for r in periods],
        "products": [tuple(r) for r in products],       # (เมนู, แก้ว, ยอดก่อนลด)
        "payments": [tuple(r) for r in payments],       # (วิธีชำระ, ออเดอร์, ยอดสุทธิ)
        "hours": [tuple(r) for r in hours],             # (ชั่วโมง "08", ออเดอร์, ยอดสุทธิ)
    }


def fmt_period(key):
    """'2026-10-02' -> '02/10/2026'   '2026-10' -> '10/2026'"""
    parts = key.split("-")
    return "/".join(reversed(parts)) if len(parts) in (2, 3) else key


def report_tables(r):
    """แปลงรายงานเป็นตาราง (ใช้ทำไฟล์ Excel)
    คืนค่า [(ชื่อตาราง, หัวคอลัมน์, แถวข้อมูล, แถวรวมหรือ None)]"""
    s = r["summary"]
    unit = "วันที่" if r["group"] == "day" else "เดือน"
    periods = [(fmt_period(k), o, c, round(g, 2), round(d, 2), round(nv, 2), round(v, 2), round(pd, 2))
               for k, o, c, g, d, nv, v, pd in r["periods"]]
    total_net = s["net"] or 1
    return [
        ("สรุป", ["หัวข้อ", "ค่า"],
         [("ยอดขายก่อนส่วนลด (บาท)", round(s["gross"], 2)), ("ส่วนลดรวม (บาท)", round(s["discount"], 2)),
          ("ยอดขายสุทธิ (บาท)", round(s["net"], 2)), (f"{VAT_LABEL} (บาท)", round(s["vat"], 2)),
          ("เงินที่รับชำระรวม VAT (บาท)", round(s["paid"], 2)), ("จำนวนออเดอร์", s["orders"]),
          ("จำนวนแก้ว", s["cups"]), ("ยอดเฉลี่ยต่อออเดอร์ (บาท)", round(s["avg"], 2))], None),
        ("รายวัน" if r["group"] == "day" else "รายเดือน",
         [unit, "ออเดอร์", "แก้ว", "ยอดก่อนส่วนลด", "ส่วนลด", "ยอดสุทธิ", f"VAT {VAT_RATE:g}%", "รับชำระรวม VAT"],
         periods,
         ("รวม", s["orders"], s["cups"], round(s["gross"], 2), round(s["discount"], 2), round(s["net"], 2),
          round(s["vat"], 2), round(s["paid"], 2))),
        ("เมนูขายดี", ["อันดับ", "เมนู", "จำนวนแก้ว", "ยอดขาย (ก่อนส่วนลด)"],
         [(i, name, q, round(m, 2)) for i, (name, q, m) in enumerate(r["products"], 1)], None),
        ("วิธีชำระเงิน", ["วิธีชำระ", "ออเดอร์", "ยอดสุทธิ", "สัดส่วน (%)"],
         [(m, o, round(v, 2), round(v * 100 / total_net, 1)) for m, o, v in r["payments"]], None),
        ("ช่วงเวลา", ["ช่วงเวลา", "ออเดอร์", "ยอดสุทธิ"],
         [(f"{h}:00 - {h}:59", o, round(v, 2)) for h, o, v in r["hours"]], None),
    ]


def export_report_xlsx(r, path):
    """บันทึกรายงานเป็นไฟล์ Excel (.xlsx) แยกแต่ละตารางเป็นชีต"""
    sheets = []
    for title, head, rows, total in report_tables(r):
        body = [("title", [f"รายงานยอดขาย {SHOP_NAME} - {title}"]),
                ("note", [f"ช่วงวันที่ {fmt_period(r['from'])} - {fmt_period(r['to'])}  "
                          f"(ออกรายงานเมื่อ {thai_now().strftime('%d/%m/%Y %H:%M')})"]),
                ("note", []), ("head", head)]
        body += [("row", list(x)) for x in rows]
        if total:
            body.append(("total", list(total)))
        widths = [max(12, min(40, max(len(str(v)) for v in [h] + [x[i] for x in rows]) + 4))
                  for i, h in enumerate(head)]
        sheets.append((title, widths, body))
    write_xlsx(path, sheets)
    return path


def write_xlsx(path, sheets):
    """เขียนไฟล์ Excel (.xlsx) ด้วยไลบรารีมาตรฐานของ Python (ไม่ต้องติดตั้งอะไรเพิ่ม)
    sheets = [(ชื่อชีต, [ความกว้างคอลัมน์], [(แบบแถว, [ค่า...])])]
    แบบแถว: "title" หัวเรื่อง, "note" ข้อความเล็ก, "head" หัวตาราง, "row" ข้อมูล, "total" แถวรวม (ตัวหนา)
    ไฟล์ .xlsx คือไฟล์ zip ที่ข้างในเป็นเอกสารหลายชิ้น แต่ละชิ้นสร้างด้วย ElementTree
    (สร้างเป็นออบเจกต์ Python แล้วให้ ElementTree แปลงเป็นไฟล์ ไม่ต้องเขียนแท็กเอง)"""
    NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    NS_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
    NS_TYPES = "http://schemas.openxmlformats.org/package/2006/content-types"
    CT = "application/vnd.openxmlformats-officedocument.spreadsheetml"

    def add(parent, tag, text=None, **attrs):
        """เพิ่มชิ้นส่วนลูกใต้ parent พร้อมคุณสมบัติ (ค่าตัวเลขแปลงเป็นข้อความให้)"""
        node = ET.SubElement(parent, tag, {k: str(v) for k, v in attrs.items()})
        node.text = text
        return node

    def to_bytes(root):
        return ET.tostring(root, encoding="UTF-8", xml_declaration=True)

    def col(i):
        """เลขคอลัมน์ -> ตัวอักษร Excel: 0 -> A, 25 -> Z, 26 -> AA"""
        name = ""
        i += 1
        while i:
            i, rem = divmod(i - 1, 26)
            name = chr(65 + rem) + name
        return name

    def clean(v):
        """ตัดอักขระควบคุมที่ Excel อ่านไม่ได้ออก (เหลือ tab กับขึ้นบรรทัดใหม่)"""
        return "".join(ch for ch in str(v) if ch in "\t\n" or ord(ch) >= 32)

    # รูปแบบเซลล์ (ลำดับตรงกับ XF ด้านล่าง)
    TEXT, HEAD, MONEY, INT, TITLE, B_MONEY, B_TEXT, B_INT, NOTE = range(9)

    # ---- แต่ละชีต ----
    sheet_files = []
    for _, widths, body in sheets:
        ws = ET.Element("worksheet", xmlns=NS_MAIN)
        cols = add(ws, "cols")
        for i, w in enumerate(widths, 1):
            add(cols, "col", min=i, max=i, width=w, customWidth=1)
        data = add(ws, "sheetData")
        for r_i, (kind, values) in enumerate(body, 1):
            row = add(data, "row", r=r_i)
            if kind in ("title", "head"):
                row.set("ht", "24")
                row.set("customHeight", "1")
            for c_i, v in enumerate(values):
                ref = f"{col(c_i)}{r_i}"
                if isinstance(v, (int, float)) and not isinstance(v, bool) and kind != "head":
                    st = ((B_INT if kind == "total" else INT) if isinstance(v, int)
                          else (B_MONEY if kind == "total" else MONEY))
                    add(add(row, "c", r=ref, s=st), "v", str(v))
                else:
                    st = {"title": TITLE, "head": HEAD, "total": B_TEXT, "note": NOTE}.get(kind, TEXT)
                    cell = add(row, "c", r=ref, t="inlineStr", s=st)
                    add(add(cell, "is"), "t", clean(v), **{"xml:space": "preserve"})
        sheet_files.append(to_bytes(ws))

    # ---- ฟอนต์ สีพื้น เส้นขอบ และรูปแบบเซลล์ ----
    st = ET.Element("styleSheet", xmlns=NS_MAIN)
    fonts = add(st, "fonts", count=4)
    for bold, size, color in ((False, 11, None), (True, 11, None), (True, 14, None), (False, 10, "FF666666")):
        font = add(fonts, "font")
        if bold:
            add(font, "b")
        add(font, "sz", val=size)
        if color:
            add(font, "color", rgb=color)
        add(font, "name", val="Tahoma")
    fills = add(st, "fills", count=3)
    add(add(fills, "fill"), "patternFill", patternType="none")
    add(add(fills, "fill"), "patternFill", patternType="gray125")
    yellow = add(add(fills, "fill"), "patternFill", patternType="solid")       # พื้นเหลืองหัวตาราง
    add(yellow, "fgColor", rgb="FFFFD43B")
    add(yellow, "bgColor", indexed=64)
    borders = add(st, "borders", count=2)
    for top_line in (False, True):                                            # ไม่มีเส้น / เส้นบน (แถวรวม)
        border = add(borders, "border")
        for side in ("left", "right", "top", "bottom", "diagonal"):
            if side == "top" and top_line:
                add(border, side, style="thin")
            else:
                add(border, side)
    add(add(st, "cellStyleXfs", count=1), "xf", numFmtId=0, fontId=0, fillId=0, borderId=0)
    # (รูปแบบตัวเลข, ฟอนต์, สีพื้น, เส้นขอบ) เรียงตาม TEXT, HEAD, MONEY, INT, TITLE, B_MONEY, B_TEXT, B_INT, NOTE
    # รูปแบบตัวเลข 0 = ทั่วไป, 3 = #,##0, 4 = #,##0.00
    XF = [(0, 0, 0, 0), (0, 1, 2, 0), (4, 0, 0, 0), (3, 0, 0, 0), (0, 2, 0, 0),
          (4, 1, 0, 1), (0, 1, 0, 1), (3, 1, 0, 1), (0, 3, 0, 0)]
    xfs = add(st, "cellXfs", count=len(XF))
    for num, font, fill, border in XF:
        xf = add(xfs, "xf", numFmtId=num, fontId=font, fillId=fill, borderId=border, xfId=0)
        for flag, used in (("applyNumberFormat", num), ("applyFont", font),
                           ("applyFill", fill), ("applyBorder", border)):
            if used:
                xf.set(flag, "1")
    add(add(st, "cellStyles", count=1), "cellStyle", name="Normal", xfId=0, builtinId=0)

    # ---- รายชื่อชีต (ชื่อห้ามซ้ำ ห้ามมี []:*?/\ และยาวไม่เกิน 31 ตัว) ----
    n = len(sheets)
    names = []
    for title, _, _ in sheets:
        name = "".join(" " if ch in "[]:*?/\\" else ch for ch in title)[:31] or "Sheet"
        while name in names:
            name = name[:28] + f" {len(names)}"
        names.append(name)
    wb = ET.Element("workbook", {"xmlns": NS_MAIN, "xmlns:r": NS_DOC})
    sheet_list = add(wb, "sheets")
    for i, nm in enumerate(names, 1):
        add(sheet_list, "sheet", name=clean(nm), sheetId=i, **{"r:id": f"rId{i}"})

    # ---- ความเชื่อมโยงระหว่างไฟล์ข้างใน และชนิดของแต่ละไฟล์ ----
    wb_rels = ET.Element("Relationships", xmlns=NS_PKG)
    for i in range(1, n + 1):
        add(wb_rels, "Relationship", Id=f"rId{i}", Type=f"{NS_DOC}/worksheet",
            Target=f"worksheets/sheet{i}.xml")
    add(wb_rels, "Relationship", Id=f"rId{n + 1}", Type=f"{NS_DOC}/styles", Target="styles.xml")
    root_rels = ET.Element("Relationships", xmlns=NS_PKG)
    add(root_rels, "Relationship", Id="rId1", Type=f"{NS_DOC}/officeDocument", Target="xl/workbook.xml")
    types = ET.Element("Types", xmlns=NS_TYPES)
    add(types, "Default", Extension="rels",
        ContentType="application/vnd.openxmlformats-package.relationships+xml")
    add(types, "Default", Extension="xml", ContentType="application/xml")
    add(types, "Override", PartName="/xl/workbook.xml", ContentType=f"{CT}.sheet.main+xml")
    for i in range(1, n + 1):
        add(types, "Override", PartName=f"/xl/worksheets/sheet{i}.xml", ContentType=f"{CT}.worksheet+xml")
    add(types, "Override", PartName="/xl/styles.xml", ContentType=f"{CT}.styles+xml")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", to_bytes(types))
        z.writestr("_rels/.rels", to_bytes(root_rels))
        z.writestr("xl/workbook.xml", to_bytes(wb))
        z.writestr("xl/_rels/workbook.xml.rels", to_bytes(wb_rels))
        z.writestr("xl/styles.xml", to_bytes(st))
        for i, data in enumerate(sheet_files, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", data)
    return path


# =====================================================================
# ส่วนที่ 20: ระบบแอดมิน (หน้าจอ)
#   ประกอบด้วย: AdminLoginPage (ล็อกอิน/ตั้งรหัสครั้งแรก), ปุ่ม "Main Menu" (เปิดหน้าลูกค้าเป็นหน้าต่างแยก),
#              AdminPage (เมนูแอดมิน: ภาพรวม / คิวหลังร้าน / ออเดอร์ / การชำระเงิน /
#              เมนูและสต็อก (การ์ดเมนูมีรูป เปลี่ยนรูป/อัปโหลดรูปเมนู เติมสต็อก) / สมาชิก / รายงานยอดขาย /
#              บัญชีแอดมิน),
#              แจ้งเตือนสต็อกใกล้หมด/หมด, แจ้งเตือนสลิปรอตรวจ (เช็กทุก 3 วินาที),
#              คิวหลังร้าน (page_kitchen: รอคิว/กำลังทำ/พร้อมรับ ติ๊กแก้วที่เสร็จ กดแจ้งลูกค้า),
#              หน้าต่างย่อย (รายละเอียดออเดอร์, ตรวจสลิปโอนเงิน, แก้เมนู, เติมสต็อก, รายละเอียดสมาชิก,
#              ยืนยันลบบัญชีสมาชิก open_delete_member_dialog, ยืนยันลบเมนู open_delete_product_dialog)
#   แก้ที่นี่เมื่อ: แก้หน้าตาหรือหน้าที่ของหน้าแอดมิน (ธีม AD_* แยกจากธีมลูกค้า เพื่อให้ดูต่างกันชัดเจน)
# บรรทัด 1136 - 3680
# =====================================================================
AD_SIDE = "#1E2A38"        # แถบเมนูซ้าย (น้ำเงินเข้ม)
AD_SIDE_HOVER = "#2C3B4E"
AD_BG = "#F2F4F7"          # พื้นหลังเนื้อหา
AD_CARD = "#FFFFFF"
AD_ACCENT = "#E8A317"      # เหลืองอำพัน
AD_TEXT = "#1F2933"
AD_MUTED = "#566170"
AD_LINE = "#D9DEE5"
AD_OK = "#2F855A"
AD_WARN = "#B7791F"
AD_BAD = "#C0392B"

ORDER_STATUS_TH = {"paid": "ชำระแล้ว", "pending": "รอชำระ", "cancelled": "ยกเลิก"}
STOCK_TH = {"ok": "พร้อมขาย", "low": "ใกล้หมด", "out": "หมดแล้ว"}
STOCK_COLOR = {"ok": AD_OK, "low": AD_WARN, "out": AD_BAD}
ORDER_STATUS_COLOR = {"paid": AD_OK, "pending": AD_WARN, "cancelled": AD_BAD}
SLIP_STATUS_TH = {"waiting": "รอตรวจสลิป", "approved": "สลิปผ่าน", "rejected": "สลิปไม่ผ่าน"}
SLIP_STATUS_COLOR = {"waiting": AD_WARN, "approved": AD_OK, "rejected": AD_BAD}
SLIP_REJECT_REASONS = ("ยอดเงินไม่ตรง", "สลิปไม่ชัด อ่านไม่ได้", "ไม่พบยอดโอนเข้าบัญชีร้าน", "สลิปซ้ำ/เคยใช้แล้ว")


def order_status_text(o):
    """ข้อความสถานะออเดอร์ (ออเดอร์รอชำระที่ส่งสลิปแล้วบอกสถานะสลิปแทน
    ออเดอร์ที่ชำระแล้วแต่ลูกค้ายังไม่ได้รับ บอกสถานะหลังร้านต่อท้าย เช่น "ชำระแล้ว • กำลังทำ")"""
    if o["status"] == "pending" and o.get("slip_status") in ("waiting", "rejected"):
        return SLIP_STATUS_TH[o["slip_status"]]
    if o["status"] == "paid" and o.get("prep_status") in PREP_ACTIVE:
        return f"{ORDER_STATUS_TH['paid']} • {PREP_LABEL[o['prep_status']]}"
    return ORDER_STATUS_TH.get(o["status"], o["status"])
PAY_TH = {"cash": "เงินสด", "qr": "QR", "card": "บัตร"}


AD_BUTTONS = {"primary": (AD_SIDE, "white", AD_SIDE_HOVER, ""),
              "accent": (AD_ACCENT, AD_SIDE, "#F0B93A", ""),
              "danger": (AD_BAD, "white", "#A93226", ""),
              "ok": (AD_OK, "white", "#276749", ""),
              "ghost": (AD_CARD, AD_TEXT, "#E9EDF2", AD_LINE),
              "side": (AD_SIDE, "#C9D3DF", AD_SIDE_HOVER, "#3A4B61")}


def ad_button(parent, text, command, kind="primary", height=38):
    """ปุ่มของหน้าแอดมิน (มุมมนน้อยกว่าฝั่งลูกค้า ให้ดูเป็นหน้าทำงาน)"""
    return PillButton(parent, text, command, colors=AD_BUTTONS[kind], height=height,
                      size=10, radius=10, padx=16)


def ad_entry(parent, show=None, width=None):
    """ช่องกรอกของแอดมิน คืนค่ากรอบ (RoundEntry) ใช้ .entry เพื่ออ่าน/เขียนข้อความ"""
    return RoundEntry(parent, show=show, height=38, size=11, fill="white", border=AD_LINE,
                      focus=AD_ACCENT, fg=AD_TEXT, width=width, radius=10)


def ad_field(parent, label, show=None, bg=AD_BG):
    tk.Label(parent, text=label, bg=bg, fg=AD_TEXT, font=(FONT, 11, "bold"),
             anchor="w").pack(fill="x", pady=(10, 4))
    box = ad_entry(parent, show=show)
    box.pack(fill="x")
    return box.entry


def ad_chip(parent, text, color):
    return Pill(parent, text, color, "white", size=9, height=24)


def ad_make_table(parent, columns, rows, on_double=None, height=14):
    """ตารางแบบ Treeview  columns = [(หัวข้อ, ความกว้าง, ชิดซ้าย/ขวา)]  rows = [(id, (ค่าแต่ละช่อง...))]"""
    from tkinter import ttk
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Admin.Treeview", background="white", fieldbackground="white",
                    foreground=AD_TEXT, rowheight=32, font=(FONT, 11), borderwidth=0,
                    relief="flat")
    style.layout("Admin.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
    style.configure("Admin.Treeview.Heading", background="#EEF1F5", foreground=AD_MUTED,
                    font=(FONT, 11, "bold"), relief="flat", borderwidth=0, padding=(8, 7))
    style.map("Admin.Treeview.Heading", background=[("active", "#E3E8EE")])
    style.map("Admin.Treeview", background=[("selected", "#FCE9B8")],
              foreground=[("selected", AD_TEXT)])
    card = RoundFrame(parent, fill="white", border=AD_LINE, radius=12, padx=6, pady=6)
    frame = card.inner
    cols = [f"c{i}" for i in range(len(columns))]
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=height,
                        style="Admin.Treeview", selectmode="browse")
    for cid, (title_text, width, anchor) in zip(cols, columns):
        tree.heading(cid, text=title_text)
        tree.column(cid, width=width, anchor=anchor, stretch=True)
    sb = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    tree.tag_configure("odd", background="#F8F9FB")
    for n, (rid, values) in enumerate(rows):
        tree.insert("", "end", iid=str(rid), values=values, tags=("odd",) if n % 2 else ())
    if on_double:
        tree.bind("<Double-1>", lambda e: on_double())
    return card, tree


def ad_dialog(parent, title_text, w, h):
    """หน้าต่างย่อยกลางจอ ล็อกโฟกัสไว้จนกว่าจะปิด"""
    win = tk.Toplevel(parent)
    win.title(title_text)
    win.configure(bg=AD_BG)
    win.resizable(False, False)
    x = parent.winfo_rootx() + max((parent.winfo_width() - w) // 2, 0)
    y = parent.winfo_rooty() + max((parent.winfo_height() - h) // 2, 0)
    win.geometry(f"{w}x{h}+{x}+{y}")
    win.transient(parent.winfo_toplevel())
    try:
        win.grab_set()
    except tk.TclError:
        pass
    return win


def baht(v):
    return f"฿{fmt_price(v)}"


# ---------------- หน้าล็อกอินแอดมิน / ตั้งรหัสครั้งแรก ----------------
class AdminLoginPage(tk.Frame):
    def __init__(self, app, on_success, on_back):
        super().__init__(app, bg=AD_SIDE)
        self.app = app
        self.on_success = on_success
        self.on_back = on_back
        self.first_run = not admin_exists()

        card = RoundFrame(self, fill=AD_BG, radius=22, padx=36, pady=32)
        card.place(relx=0.5, rely=0.5, anchor="center", width=430)
        body = card.inner

        head = tk.Frame(body, bg=AD_BG)
        head.pack(anchor="w", pady=(0, 10))
        logo_canvas(head, 56).pack(side="left", padx=(0, 12))
        brand = tk.Frame(head, bg=AD_BG)
        brand.pack(side="left")
        Pill(brand, "ADMIN CONSOLE", AD_ACCENT, AD_SIDE, size=9, height=24, padx=12).pack(anchor="w")
        tk.Label(brand, text=f"{SHOP_NAME}", bg=AD_BG, fg=AD_TEXT,
                 font=(FONT, 11)).pack(anchor="w", pady=(4, 0))
        if self.first_run:
            tk.Label(body, text="ตั้งค่าบัญชีแอดมิน", bg=AD_BG, fg=AD_TEXT,
                     font=(FONT, 20, "bold")).pack(anchor="w")
            tk.Label(body, text="ยังไม่มีบัญชีแอดมิน กรุณาสร้างบัญชีแรกของคุณ",
                     bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w")
            self.f_name = ad_field(body, "ชื่อแอดมิน")
            self.f_user = ad_field(body, "ชื่อผู้ใช้ (a-z ตัวเลข อย่างน้อย 3 ตัว)")
            self.f_pass = ad_field(body, f"รหัสผ่าน ({PASSWORD_HINT})", show="•")
            self.f_pass2 = ad_field(body, "ยืนยันรหัสผ่าน", show="•")
            first = self.f_name
        else:
            tk.Label(body, text="เข้าสู่ระบบแอดมิน", bg=AD_BG, fg=AD_TEXT,
                     font=(FONT, 20, "bold")).pack(anchor="w")
            tk.Label(body, text="สำหรับผู้ดูแลระบบเท่านั้น", bg=AD_BG, fg=AD_MUTED,
                     font=(FONT, 11)).pack(anchor="w")
            self.f_user = ad_field(body, "ชื่อผู้ใช้")
            self.f_pass = ad_field(body, "รหัสผ่าน", show="•")
            first = self.f_user

        # แสดงรหัสผ่าน (ช่วยตรวจว่าพิมพ์ถูก / ไม่ได้เปิดแป้นภาษาไทยค้างไว้)
        self.show_pw = tk.BooleanVar(value=False)

        def toggle_pw():
            ch = "" if self.show_pw.get() else "•"
            self.f_pass.config(show=ch)
            if self.first_run:
                self.f_pass2.config(show=ch)

        tk.Checkbutton(body, text="แสดงรหัสผ่าน", variable=self.show_pw, command=toggle_pw,
                       bg=AD_BG, activebackground=AD_BG, fg=AD_MUTED, font=(FONT, 11), bd=0,
                       highlightthickness=0, cursor="hand2").pack(anchor="w", pady=(6, 0))

        self.msg = tk.Label(body, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 11),
                            wraplength=330, justify="left")
        self.msg.pack(anchor="w", pady=(8, 0))
        ad_button(body, "สร้างบัญชีและเข้าสู่ระบบ" if self.first_run else "เข้าสู่ระบบ",
                  self.submit, "accent", height=44).pack(fill="x", pady=(8, 8))
        ad_button(body, "กลับหน้าลูกค้า", self.on_back, "ghost", height=42).pack(fill="x")
        if not self.first_run:
            LinkButton(body, "ลืมรหัสผ่านแอดมิน?", self.forgot, fg=AD_MUTED,
                       hover=AD_TEXT).pack(anchor="e", pady=(12, 0))
        first.focus()
        app.bind("<Return>", lambda e: self.submit())

    def forgot(self):
        messagebox.showinfo(
            "ลืมรหัสผ่านแอดมิน",
            "เพื่อความปลอดภัย หน้านี้จะไม่ให้เปลี่ยนรหัสโดยไม่ยืนยันตัวตน\n\n"
            "วิธีตั้งรหัสใหม่ (ทำได้เฉพาะคนที่เข้าถึงเครื่องนี้):\n"
            "1. ปิดโปรแกรมนี้\n"
            "2. เปิดไฟล์ reset_admin.py ใน VS Code (อยู่โฟลเดอร์เดียวกับ project.py) แล้วกด Run\n"
            "3. พิมพ์ชื่อผู้ใช้แอดมิน และรหัสผ่านใหม่ในหน้าต่าง Terminal\n"
            "4. เปิด project.py แล้วเข้าสู่ระบบด้วยรหัสใหม่", parent=self)

    def submit(self):
        if self.first_run:
            if self.f_pass.get() != self.f_pass2.get():
                self.msg.config(text="รหัสผ่านทั้งสองช่องไม่ตรงกัน")
                return
            ok, text = create_admin(self.f_user.get(), self.f_pass.get(), self.f_name.get())
            if not ok:
                self.msg.config(text=text)
                return
        admin, text = login_admin(self.f_user.get(), self.f_pass.get())
        if admin is None:
            self.msg.config(text=text)
            self.f_pass.delete(0, "end")
            return
        self.on_success(admin)


# ---------------- หน้าต่างย่อย: รายละเอียดออเดอร์ ----------------
def open_order_detail(parent, order_id, on_change):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    o = conn.execute(
        "SELECT o.*, m.name AS member_name, m.phone AS member_phone "
        "FROM orders o LEFT JOIN members m ON m.member_id = o.member_id WHERE o.order_id = ?",
        (order_id,)).fetchone()
    items = conn.execute(
        "SELECT p.name, oi.quantity, oi.unit_price, oi.options FROM order_items oi "
        "JOIN products p ON p.product_id = oi.product_id WHERE oi.order_id = ?",
        (order_id,)).fetchall()
    conn.close()
    if o is None:
        messagebox.showerror("ไม่พบออเดอร์", "ไม่พบออเดอร์นี้", parent=parent)
        return
    slips = admin_order_slips(order_id)
    prep = o["prep_status"] if o["status"] == "paid" else None      # สถานะหลังร้าน (ชำระแล้วเท่านั้น)
    win = ad_dialog(parent, f"ออเดอร์ {order_code(order_id)}", 580, (700 if slips else 660) + (26 if prep else 0))
    body = tk.Frame(win, bg=AD_BG, padx=26, pady=22)
    body.pack(fill="both", expand=True)

    head = tk.Frame(body, bg=AD_BG)
    head.pack(fill="x")
    tk.Label(head, text=order_code(order_id), bg=AD_BG, fg=AD_TEXT,
             font=(FONT, 18, "bold")).pack(side="left")
    ad_chip(head, ORDER_STATUS_TH.get(o["status"], o["status"]),
            ORDER_STATUS_COLOR.get(o["status"], AD_MUTED)).pack(side="left", padx=10)

    who = "ลูกค้าทั่วไป" if not o["member_name"] else f"{o['member_name']}  ({o['member_phone']})"
    info = [("สมาชิก", who),
            ("สั่งเมื่อ", fmt_datetime(o["order_date"])),
            ("ชำระเมื่อ", fmt_datetime(o["paid_at"]) if o["paid_at"] else "-"),
            ("ช่องทางชำระ", PAY_TH.get(o["payment_method"], o["payment_method"] or "-")),
            ("ส่งใบเสร็จอีเมล", "ส่งแล้ว" if o["receipt_sent"] else "ยังไม่ได้ส่ง")]
    if slips:
        info.append(("สลิปโอนเงิน", f"{SLIP_STATUS_TH[slips[0]['status']]}  (ส่ง {len(slips)} ครั้ง)"))
    if prep:
        by = f"  (โดย {o['prep_by']})" if o["prep_by"] else ""
        info.append(("สถานะหลังร้าน", PREP_LABEL.get(prep, prep) + by))
    info_card = RoundFrame(body, fill="white", border=AD_LINE, radius=12, padx=16, pady=10)
    info_card.pack(fill="x", pady=(12, 10))
    grid = info_card.inner
    for i, (k, v) in enumerate(info):
        tk.Label(grid, text=k, bg="white", fg=AD_MUTED, font=(FONT, 11), anchor="w",
                 width=15).grid(row=i, column=0, sticky="w", pady=2)
        tk.Label(grid, text=v, bg="white", fg=AD_TEXT, font=(FONT, 11, "bold"),
                 anchor="w").grid(row=i, column=1, sticky="w", pady=2)

    rows = [(i, (r["name"] + (f"  ({r['options']})" if r["options"] else ""),
                 r["quantity"], fmt_price(r["unit_price"]),
                 fmt_price(r["quantity"] * r["unit_price"])))
            for i, r in enumerate(items)]
    frame, _ = ad_make_table(body, [("รายการ", 280, "w"), ("จำนวน", 55, "center"),
                                    ("ราคา", 70, "e"), ("รวม", 80, "e")], rows, height=7)
    frame.pack(fill="both", expand=True, pady=(4, 8))

    total = tk.Frame(body, bg=AD_BG)
    total.pack(fill="x", padx=4)
    amounts = order_amounts(o)
    lines = [(k, v, False) for k, v in money_rows(amounts)] or [("ราคาสินค้า", baht(o["total_price"]), False)]
    lines.append(("ยอดชำระ (รวม VAT)" if amounts["vat"] else "ยอดสุทธิ", baht(amounts["paid"]), True))
    for k, v, bold in lines:
        row = tk.Frame(total, bg=AD_BG)
        row.pack(fill="x")
        tk.Label(row, text=k, bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(side="left")
        tk.Label(row, text=v, bg=AD_BG, fg=AD_TEXT,
                 font=(FONT, 12 if bold else 10, "bold")).pack(side="right")

    btns = tk.Frame(body, bg=AD_BG)
    btns.pack(fill="x", pady=(14, 0))

    def cancel():
        if messagebox.askyesno("ยกเลิกออเดอร์", "ยืนยันยกเลิกออเดอร์นี้?", parent=win):
            if admin_cancel_order(order_id):
                win.destroy()
                on_change()
            else:
                messagebox.showinfo("ไม่สามารถยกเลิกได้", "ออเดอร์นี้ไม่ได้อยู่ในสถานะรอชำระ", parent=win)

    if o["status"] == "pending":
        ad_button(btns, "ยกเลิกออเดอร์", cancel, "danger").pack(side="left")
    ad_button(btns, "ปิด", win.destroy, "ghost").pack(side="right")
    if slips:
        def show_slip():
            win.destroy()
            open_slip_viewer(parent, slips[0]["slip_id"], on_change)
        ad_button(btns, "ดูสลิปโอนเงิน", show_slip, "accent").pack(side="right", padx=(0, 8))
    if prep in PREP_ACTIVE and hasattr(parent, "go"):
        def to_kitchen():
            win.destroy()
            parent.go("kitchen")
        ad_button(btns, "ไปที่คิวหลังร้าน", to_kitchen, "primary").pack(side="left")


# ---------------- หน้าต่างย่อย: ตรวจสลิปโอนเงิน ----------------
def open_slip_viewer(page, slip_id, on_change):
    """ดูสลิปขนาดใหญ่คู่กับข้อมูลออเดอร์ แล้วกด "ยืนยันรับเงิน" หรือ "สลิปไม่ผ่าน" (ระบุเหตุผล)
    page = AdminPage (ใช้ชื่อแอดมินที่ตรวจ และส่งใบเสร็จหลังยืนยัน)"""
    sl = admin_get_slip(slip_id)
    if sl is None:
        messagebox.showerror("ไม่พบสลิป", "ไม่พบสลิปนี้", parent=page)
        return
    code = order_code(sl["order_id"])
    h = min(700, page.winfo_screenheight() - 110)       # จอเตี้ยก็ยังเห็นปุ่มครบ
    win = ad_dialog(page, f"ตรวจสลิป {code}", 900, h)
    body = tk.Frame(win, bg=AD_BG, padx=24, pady=20)
    body.pack(fill="both", expand=True)

    # ซ้าย: รูปสลิป
    left = RoundFrame(body, fill="white", border=AD_LINE, radius=14, padx=12, pady=12)
    left.pack(side="left", fill="y")
    photo = slip_photo(get_slip_image(slip_id) or b"", 380, h - 80)
    if photo is not None:
        pic = tk.Label(left.inner, image=photo, bg="white", bd=0)
        pic.image = photo
    else:
        pic = tk.Label(left.inner, text="เปิดรูปสลิปไม่ได้", bg="white", fg=AD_MUTED,
                       font=(FONT, 11), width=30, height=10)
    pic.pack()

    # ขวา: ข้อมูลออเดอร์ + ปุ่มตรวจ
    right = tk.Frame(body, bg=AD_BG)
    right.pack(side="left", fill="both", expand=True, padx=(22, 0))
    head = tk.Frame(right, bg=AD_BG)
    head.pack(fill="x")
    tk.Label(head, text=code, bg=AD_BG, fg=AD_TEXT, font=(FONT, 20, "bold")).pack(side="left")
    ad_chip(head, SLIP_STATUS_TH[sl["status"]], SLIP_STATUS_COLOR[sl["status"]]).pack(side="left", padx=10)

    amount = RoundFrame(right, fill="white", border=AD_LINE, radius=12, padx=16, pady=12)
    amount.pack(fill="x", pady=(12, 0))
    tk.Label(amount.inner, text="ยอดที่ลูกค้าต้องโอน (รวม VAT)", bg="white", fg=AD_MUTED,
             font=(FONT, 11)).pack(anchor="w")
    tk.Label(amount.inner, text=baht(sl["amount"]), bg="white", fg=AD_OK,
             font=(FONT, 26, "bold")).pack(anchor="w")
    who = sl["member_name"] or "ลูกค้าทั่วไป"
    if sl["member_phone"]:
        who += f"  ({sl['member_phone']})"
    info = [("ลูกค้า", who), ("ส่งสลิปเมื่อ", fmt_datetime(sl["submitted_at"])),
            ("ส่วนลดที่เลือก", f"{sl['coupon_percent']}%" if sl["coupon_percent"] else "-"),
            ("ส่งใบเสร็จไปที่", sl["email"] or "ไม่ต้องส่ง")]
    if sl["checked_at"]:
        info.append(("ตรวจโดย", f"{sl['checked_by'] or '-'}  •  {fmt_datetime(sl['checked_at'])}"))
    if sl["status"] == "rejected":
        info.append(("เหตุผลที่ไม่ผ่าน", sl["note"] or "-"))
    grid = tk.Frame(amount.inner, bg="white")
    grid.pack(fill="x", pady=(8, 0))
    for i, (k, v) in enumerate(info):
        tk.Label(grid, text=k, bg="white", fg=AD_MUTED, font=(FONT, 11), anchor="w",
                 width=13).grid(row=i, column=0, sticky="nw", pady=2)
        tk.Label(grid, text=v, bg="white", fg=AD_TEXT, font=(FONT, 11, "bold"), anchor="w",
                 wraplength=250, justify="left").grid(row=i, column=1, sticky="w", pady=2)

    msg = tk.Label(right, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 11), wraplength=400, justify="left")
    btns = tk.Frame(right, bg=AD_BG)
    btns.pack(side="bottom", fill="x")
    ad_button(btns, "ปิด", win.destroy, "ghost").pack(side="right")
    if sl["status"] != "waiting" or sl["order_status"] != "pending":
        msg.pack(side="bottom", anchor="w", pady=(0, 8))
        if sl["status"] == "waiting":
            msg.config(text=f"ออเดอร์นี้{ORDER_STATUS_TH.get(sl['order_status'], '')}แล้ว จึงตรวจสลิปไม่ได้")
        return

    tk.Label(right, text="ตรวจชื่อบัญชีผู้รับ ยอดเงิน และวันเวลาบนสลิปให้ตรงก่อนกดยืนยัน", bg=AD_BG,
             fg=AD_MUTED, font=(FONT, 10), wraplength=400, justify="left").pack(anchor="w", pady=(12, 0))

    def approve():
        try:
            result, order_id, email = admin_approve_slip(slip_id, page.admin["name"])
        except ValueError as e:
            msg.config(text=str(e))
            return
        win.destroy()
        page.after_slip_checked(f"ยืนยันรับเงิน {code} แล้ว ({baht(result['paid_total'])})", True)
        if email:
            page.send_receipt_async(order_id, email)
        on_change()

    ad_button(right, "ยืนยันรับเงิน", approve, "accent", height=44).pack(fill="x", pady=(10, 0))

    rej = RoundFrame(right, fill="white", border=AD_LINE, radius=12, padx=14, pady=10)
    rej.pack(fill="x", pady=(14, 0))
    tk.Label(rej.inner, text="สลิปไม่ผ่าน: ระบุเหตุผล (ลูกค้าจะเห็นข้อความนี้)", bg="white", fg=AD_TEXT,
             font=(FONT, 11, "bold")).pack(anchor="w")
    box = ad_entry(rej.inner)
    box.pack(fill="x", pady=(6, 0))
    reason = box.entry
    chips = tk.Frame(rej.inner, bg="white")
    chips.pack(fill="x", pady=(6, 0))
    for i, text in enumerate(SLIP_REJECT_REASONS):
        PillButton(chips, text, lambda t=text: (reason.delete(0, "end"), reason.insert(0, t)),
                   colors=AD_BUTTONS["ghost"], height=28, size=9, radius=8,
                   padx=10).grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 6), pady=2)

    def reject():
        try:
            admin_reject_slip(slip_id, reason.get(), page.admin["name"])
        except ValueError as e:
            msg.config(text=str(e))
            return
        win.destroy()
        page.after_slip_checked(f"แจ้งลูกค้าว่าสลิป {code} ไม่ผ่านแล้ว", False)
        on_change()

    ad_button(rej.inner, "แจ้งสลิปไม่ผ่าน", reject, "danger").pack(anchor="e", pady=(8, 0))
    msg.pack(anchor="w", pady=(8, 0))


# ---------------- หน้าต่างย่อย: เพิ่ม/แก้ไขเมนู ----------------
def open_product_dialog(parent, product, on_change):
    """เพิ่มเมนูใหม่ (product=None) หรือแก้ไขเมนู: รูปเมนู (อัปโหลด/เปลี่ยน) ชื่อ หมวด ราคา คำอธิบาย
    สต็อกเริ่มต้น (เมนูใหม่) เปิด/ปิดขาย  รูปที่เลือกจะบันทึกตอนกด "บันทึก" พร้อมข้อมูลเมนู"""
    cats = get_categories()                      # [(category_id, name)]
    cat_names = [c[1] for c in cats]
    cat_id_by_name = {c[1]: c[0] for c in cats}
    h = min(640, parent.winfo_screenheight() - 90)
    win = ad_dialog(parent, "แก้ไขเมนู" if product else "เพิ่มเมนูใหม่", 780, h)
    body = tk.Frame(win, bg=AD_BG, padx=28, pady=22)
    body.pack(fill="both", expand=True)
    tk.Label(body, text="แก้ไขเมนู" if product else "เพิ่มเมนูใหม่", bg=AD_BG, fg=AD_TEXT,
             font=(FONT, 16, "bold")).pack(anchor="w")
    btns = tk.Frame(body, bg=AD_BG)
    btns.pack(fill="x", side="bottom")              # ปุ่มล่างได้พื้นที่ก่อน จอเตี้ยก็ไม่โดนตัด
    msg = tk.Label(body, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 11), wraplength=700, justify="left")
    msg.pack(side="bottom", anchor="w", pady=(0, 6))
    cols = tk.Frame(body, bg=AD_BG)
    cols.pack(fill="both", expand=True, pady=(10, 0))

    # ซ้าย: รูปเมนู (หน้าตาเหมือนการ์ดหน้าลูกค้า)
    left = tk.Frame(cols, bg=AD_BG, width=250)
    left.pack(side="left", fill="y", padx=(0, 22))
    tk.Label(left, text="รูปเมนู", bg=AD_BG, fg=AD_TEXT, font=(FONT, 11, "bold")).pack(anchor="w", pady=(10, 4))
    pic = tk.Canvas(left, width=250, height=262, bg=AD_BG, highlightthickness=0, cursor="hand2")
    pic.pack()
    state = {"png": None}
    pic_note = tk.Label(left, text="", bg=AD_BG, fg=AD_MUTED, font=(FONT, 9), wraplength=250, justify="left")

    def paint():
        draw_menu_pic(pic, product, None, state["png"])
        if state["png"]:
            pic_note.config(text="รูปใหม่ (บันทึกเมื่อกด \"บันทึก\")", fg=AD_OK)
        elif product and load_product_image(product, 40, 40) is not None:
            pic_note.config(text="รูปปัจจุบันบนหน้าลูกค้า", fg=AD_MUTED)
        else:
            pic_note.config(text="ยังไม่มีรูป หน้าลูกค้าจะแสดงรูปแก้ววาดแทน", fg=AD_MUTED)

    def choose():
        png = pick_menu_image(win, "เลือกรูปเมนู")
        if png is not None:
            state["png"] = png
            paint()
            undo.pack(anchor="w", pady=(4, 0))

    def keep_old():
        state["png"] = None
        undo.pack_forget()
        paint()

    pic.bind("<Button-1>", lambda e: choose())
    pic_btns = tk.Frame(left, bg=AD_BG)
    pic_btns.pack(fill="x", pady=(8, 0))
    ad_button(pic_btns, "เปลี่ยนรูป..." if product else "อัปโหลดรูป...", choose, "primary",
              height=34).pack(side="left", fill="x", expand=True)
    pic_note.pack(anchor="w", pady=(6, 0))
    undo = LinkButton(left, "ไม่เปลี่ยนรูป (ใช้รูปเดิม)" if product else "ไม่ใช้รูปนี้", keep_old, fg="#5B7DB1",
                      hover=AD_TEXT, size=9)
    tk.Label(left, text="แนะนำ PNG พื้นใส ขนาดประมาณ 372 x 392 (เหมือนรูปเดิมของร้าน)\n"
                        + ("ใช้ได้ทั้ง png / jpg / gif / bmp / webp" if HAS_PIL else "ใช้ได้เฉพาะ png และ gif"),
             bg=AD_BG, fg=AD_MUTED, font=(FONT, 9), wraplength=250, justify="left").pack(side="bottom", anchor="w")
    win.after_idle(paint)

    # ขวา: ข้อมูลเมนู
    right = tk.Frame(cols, bg=AD_BG)
    right.pack(side="left", fill="both", expand=True)
    name = ad_field(right, "ชื่อเมนู")
    tk.Label(right, text="หมวดหมู่", bg=AD_BG, fg=AD_TEXT, font=(FONT, 11, "bold"),
             anchor="w").pack(fill="x", pady=(10, 4))
    cat_var = tk.StringVar(value=(product["category"] if product else cat_names[0]))
    cat_menu = tk.OptionMenu(right, cat_var, *cat_names)
    cat_menu.config(bg="white", fg=AD_TEXT, activebackground="#F6F7F9", relief="flat",
                    bd=0, highlightthickness=1, highlightbackground=AD_LINE,
                    font=(FONT, 11), anchor="w", padx=12, pady=6, cursor="hand2")
    cat_menu["menu"].config(font=(FONT, 11), bg="white", activebackground=AD_ACCENT,
                            activeforeground=AD_SIDE)
    cat_menu.pack(fill="x")
    price = ad_field(right, "ราคา (บาท)")
    desc = ad_field(right, "คำอธิบาย")
    stock = None
    if product:                       # เมนูเดิม: ดูสต็อกได้ เติมด้วยปุ่ม "+ เติมสต็อก" บนการ์ดเมนู
        tk.Label(right, text=f"สต็อกคงเหลือ {product['stock']:,} แก้ว  (เติมด้วยปุ่ม \"+ เติมสต็อก\" บนการ์ดเมนู)",
                 bg=AD_BG, fg=STOCK_COLOR[stock_status(product["stock"])],
                 font=(FONT, 11, "bold"), anchor="w", wraplength=440, justify="left").pack(fill="x", pady=(12, 0))
    else:
        stock = ad_field(right, "สต็อกเริ่มต้น (แก้ว)")
        stock.insert(0, str(DEFAULT_STOCK))
    avail = tk.BooleanVar(value=bool(product["is_available"]) if product else True)
    tk.Checkbutton(right, text="เปิดขาย (ลูกค้าเห็นและสั่งได้)", variable=avail, bg=AD_BG,
                   activebackground=AD_BG, fg=AD_TEXT, font=(FONT, 11), bd=0,
                   highlightthickness=0, cursor="hand2").pack(anchor="w", pady=(12, 0))
    if product:
        name.insert(0, product["name"])
        price.insert(0, fmt_price(product["price"]))
        desc.insert(0, product["description"] or "")

    def save():
        ok, text = admin_save_product(product["product_id"] if product else None,
                                      cat_id_by_name[cat_var.get()], name.get(), desc.get(),
                                      price.get(), avail.get(), stock.get() if stock else None,
                                      image=state["png"])
        if ok and text.startswith("บันทึกเมนูแล้ว แต่"):            # เมนูบันทึกแล้ว แต่รูปบันทึกไม่ได้
            messagebox.showwarning("บันทึกรูปไม่สำเร็จ", text, parent=win)
        if ok:
            win.destroy()
            on_change()
        else:
            msg.config(text=text)

    ad_button(btns, "บันทึก", save, "accent", height=42).pack(side="left", fill="x", expand=True)
    ad_button(btns, "ยกเลิก", win.destroy, "ghost", height=42).pack(side="left", padx=(8, 0))
    name.focus()
    return win


# ---------------- หน้าต่างย่อย: ยืนยันลบเมนู ----------------
def open_delete_product_dialog(page, product, on_deleted):
    """ยืนยันการลบเมนู: บอกว่าอะไรจะหาย อะไรยังเก็บไว้ แล้วกด "ลบเมนูถาวร"
    ลบไม่ได้ถ้ายังมีออเดอร์ที่ยังไม่ชำระเงินสั่งเมนูนี้อยู่"""
    pid = product["product_id"]
    info = admin_product_delete_info(pid)
    if info is None:
        messagebox.showinfo("ลบเมนู", "ไม่พบเมนูนี้ (อาจถูกลบไปแล้ว)", parent=page)
        on_deleted(None)
        return
    name = info["name"]
    if info["pending"]:
        messagebox.showwarning(
            "ยังลบเมนูไม่ได้",
            f"มีออเดอร์ที่ยังไม่ชำระเงินสั่ง {name} อยู่ {info['pending']} ออเดอร์\n"
            "(ลูกค้ากำลังชำระเงิน หรือรอตรวจสลิป)\n\n"
            "รอให้ชำระเสร็จ หรือยกเลิกออเดอร์ที่หน้า \"ออเดอร์\" ก่อน แล้วค่อยลบเมนู", parent=page)
        return

    win = ad_dialog(page, "ลบเมนู", 540, 420)
    body = tk.Frame(win, bg=AD_BG, padx=26, pady=20)
    body.pack(fill="both", expand=True)
    tk.Label(body, text=f"ลบเมนู {name} ถาวร?", bg=AD_BG, fg=AD_BAD, font=(FONT, 16, "bold"),
             wraplength=480, justify="left").pack(anchor="w")
    tk.Label(body, text="ลบแล้วกู้คืนไม่ได้ ถ้าจะขายอีกต้องกด \"+ เพิ่มเมนู\" ใหม่ (ใช้ชื่อเดิมได้)",
             bg=AD_BG, fg=AD_MUTED, font=(FONT, 10)).pack(anchor="w", pady=(2, 10))

    def card(title_text, lines, color):
        rf = RoundFrame(body, fill=AD_CARD, border=AD_LINE, radius=12, padx=14, pady=10)
        rf.pack(fill="x", pady=(0, 8))
        tk.Label(rf.inner, text=title_text, bg=AD_CARD, fg=color, font=(FONT, 11, "bold")).pack(anchor="w")
        for line in lines:
            tk.Label(rf.inner, text="•  " + line, bg=AD_CARD, fg=AD_TEXT, font=(FONT, 10),
                     wraplength=440, justify="left").pack(anchor="w", pady=(2, 0))

    card("สิ่งที่จะถูกลบ",
         ["เมนูนี้หายจากหน้าลูกค้าและหน้าเมนูและสต็อกทันที",
          f"สต็อกคงเหลือ {info['stock']:,} แก้ว",
          f"รูปเมนู (ย้ายไปเก็บที่ images/{MENU_IMAGE_OLD_DIR})"], AD_BAD)
    if info["lines"]:
        keep = [f"ยอดขาย {info['sold']:,} แก้ว ยังนับในรายงานยอดขาย",
                "ประวัติออเดอร์และใบเสร็จเก่ายังแสดงชื่อเมนูนี้"]
        if info["in_queue"]:
            keep.append(f"ออเดอร์ในคิวหลังร้าน {info['in_queue']} ออเดอร์ ยังทำต่อได้ตามปกติ")
        card("สิ่งที่ยังเก็บไว้", keep, AD_OK)
    else:
        card("สิ่งที่ยังเก็บไว้", ["ยังไม่เคยมีใครสั่งเมนูนี้ จึงไม่มียอดขายหรือประวัติที่ต้องเก็บ"], AD_MUTED)
    msg = tk.Label(body, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 10), wraplength=480, justify="left")
    msg.pack(anchor="w", pady=(4, 0))

    def fit():
        """ความสูงหน้าต่างพอดีเนื้อหา (ฟอนต์แต่ละเครื่องสูงไม่เท่ากัน)"""
        win.update_idletasks()
        h = min(body.winfo_reqheight() + 4, win.winfo_screenheight() - 80)
        x = page.winfo_rootx() + max((page.winfo_width() - 540) // 2, 0)
        y = page.winfo_rooty() + max((page.winfo_height() - h) // 2, 0)
        win.geometry(f"540x{h}+{x}+{y}")

    def do_delete():
        ok, text = admin_delete_product(pid)
        if not ok:
            msg.config(text=text)
            fit()
            return
        win.destroy()
        on_deleted(text)

    btns = tk.Frame(body, bg=AD_BG)
    btns.pack(side="bottom", fill="x", pady=(10, 0))
    ad_button(btns, "ลบเมนูถาวร", do_delete, "danger", height=42).pack(side="left", fill="x", expand=True)
    ad_button(btns, "ยกเลิก", win.destroy, "ghost", height=42).pack(side="left", padx=(8, 0))
    fit()


# ---------------- หน้าต่างย่อย: เติมสต็อก ----------------
def open_stock_dialog(parent, product, on_change):
    """เติมสต็อก (บวกเพิ่ม) หรือตั้งจำนวนคงเหลือใหม่ของเมนู 1 รายการ"""
    win = ad_dialog(parent, f"สต็อก: {product['name']}", 470, 480)
    body = tk.Frame(win, bg=AD_BG, padx=26, pady=20)
    body.pack(fill="both", expand=True)
    tk.Label(body, text=product["name"], bg=AD_BG, fg=AD_TEXT, font=(FONT, 17, "bold")).pack(anchor="w")
    tk.Label(body, text=f"หมวด {product['category']}  •  ราคา {baht(product['price'])}", bg=AD_BG,
             fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w")

    stats = tk.Frame(body, bg=AD_BG)
    stats.pack(fill="x", pady=(12, 4))
    status = stock_status(product["stock"])
    for i, (label, value, color) in enumerate((
            ("คงเหลือ", f"{product['stock']:,} แก้ว", STOCK_COLOR[status]),
            ("ขายวันนี้", f"{product['sold_today']:,} แก้ว", AD_TEXT),
            ("ขายแล้วทั้งหมด", f"{product['sold']:,} แก้ว", AD_TEXT))):
        mini = RoundFrame(stats, fill="white", border=AD_LINE, radius=10, padx=10, pady=8)
        mini.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0))
        stats.grid_columnconfigure(i, weight=1, uniform="stock")
        tk.Label(mini.inner, text=label, bg="white", fg=AD_MUTED, font=(FONT, 9)).pack(anchor="w")
        tk.Label(mini.inner, text=value, bg="white", fg=color, font=(FONT, 13, "bold")).pack(anchor="w")
    tk.Label(body, text=f"สถานะ: {STOCK_TH[status]}  (ใกล้หมด = เหลือไม่เกิน {LOW_STOCK_LEVEL} แก้ว)",
             bg=AD_BG, fg=STOCK_COLOR[status], font=(FONT, 10, "bold")).pack(anchor="w", pady=(2, 0))

    mode = tk.StringVar(value="add")
    modes = tk.Frame(body, bg=AD_BG)
    modes.pack(fill="x", pady=(14, 0))
    for value, text in (("add", "เติมเพิ่ม (+)"), ("set", "ตั้งจำนวนคงเหลือใหม่")):
        tk.Radiobutton(modes, text=text, value=value, variable=mode, bg=AD_BG, activebackground=AD_BG,
                       fg=AD_TEXT, selectcolor="white", font=(FONT, 11), bd=0, highlightthickness=0,
                       cursor="hand2", command=lambda: update()).pack(side="left", padx=(0, 16))
    amount = ad_field(body, "จำนวน (แก้ว)")
    amount.insert(0, "20")
    quick = tk.Frame(body, bg=AD_BG)
    quick.pack(fill="x", pady=(8, 0))

    def bump(n):
        text = amount.get().replace(",", "").strip()
        current = int(text) if text.isdigit() else 0
        amount.delete(0, "end")
        amount.insert(0, str(current + n))
        update()

    for n in (10, 20, 50, 100):
        ad_button(quick, f"+{n}", lambda n=n: bump(n), "ghost", height=32).pack(side="left", padx=(0, 6))
    preview = tk.Label(body, text="", bg=AD_BG, fg=AD_TEXT, font=(FONT, 12, "bold"))
    preview.pack(anchor="w", pady=(12, 0))
    msg = tk.Label(body, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 11), wraplength=400, justify="left")
    msg.pack(anchor="w", pady=(4, 0))

    def update(*_):
        text = amount.get().replace(",", "").strip()
        if not text.isdigit():
            preview.config(text="")
            return
        after = product["stock"] + int(text) if mode.get() == "add" else int(text)
        preview.config(text=f"หลังบันทึก: เหลือ {after:,} แก้ว  ({STOCK_TH[stock_status(after)]})",
                       fg=STOCK_COLOR[stock_status(after)])

    def save():
        func = admin_add_stock if mode.get() == "add" else admin_set_stock
        ok, result = func(product["product_id"], amount.get())
        if not ok:
            msg.config(text=result)
            return
        win.destroy()
        on_change()

    amount.bind("<KeyRelease>", update)
    amount.bind("<Return>", lambda e: save())
    update()
    btns = tk.Frame(body, bg=AD_BG)
    btns.pack(fill="x", side="bottom")
    ad_button(btns, "บันทึกสต็อก", save, "accent", height=42).pack(side="left", fill="x", expand=True)
    ad_button(btns, "ยกเลิก", win.destroy, "ghost", height=42).pack(side="left", padx=(8, 0))
    amount.focus()
    amount.select_range(0, "end")


# ---------------- หน้าต่างย่อย: รายละเอียดสมาชิก ----------------
MEMBER_BAN_REASONS = ("สั่งแล้วไม่มารับบ่อยครั้ง", "ส่งสลิปปลอม", "พฤติกรรมไม่เหมาะสม")


def open_member_dialog(parent, member, on_change):
    mid = member["member_id"]
    banned = bool(member.get("banned"))
    win = ad_dialog(parent, f"สมาชิก: {member['name']}", 640, min(800, parent.winfo_screenheight() - 90))
    body = tk.Frame(win, bg=AD_BG, padx=26, pady=20)
    body.pack(fill="both", expand=True)
    title = tk.Frame(body, bg=AD_BG)
    title.pack(anchor="w")
    tk.Label(title, text=member["name"], bg=AD_BG, fg=AD_TEXT,
             font=(FONT, 18, "bold")).pack(side="left")
    if banned:
        ad_chip(title, "ถูกแบน", AD_BAD).pack(side="left", padx=10)

    def reopen():
        """ข้อมูลเปลี่ยน (แบน/ยกเลิกแบน): รีเฟรชหน้าสมาชิก แล้วเปิดหน้าต่างนี้ใหม่ด้วยข้อมูลล่าสุด"""
        win.destroy()
        on_change()
        fresh = next((m for m in admin_list_members() if m["member_id"] == mid), None)
        if fresh:
            open_member_dialog(parent, fresh, on_change)

    tk.Label(body, text=f"โทร {member['phone']}   •   อีเมล {member['email'] or '-'}",
             bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w")
    if banned:                                   # แถบแจ้งว่าถูกแบน + ปุ่มยกเลิกการแบน
        ban_card = RoundFrame(body, fill="#FDEDEC", border=AD_BAD, radius=12, padx=14, pady=10)
        ban_card.pack(fill="x", pady=(10, 0))
        bc = ban_card.inner

        def unban():
            if messagebox.askyesno("ยกเลิกการแบน", f"ให้ {member['name']} กลับมาใช้งานได้ตามปกติ?", parent=win):
                admin_unban_member(mid)
                reopen()

        ad_button(bc, "ยกเลิกการแบน", unban, "primary", height=34).pack(side="right")
        tk.Label(bc, text="บัญชีนี้ถูกแบน: เข้าสู่ระบบและสั่งซื้อไม่ได้", bg="#FDEDEC", fg=AD_BAD,
                 font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Label(bc, text=f"เหตุผล: {member.get('ban_reason') or '-'}", bg="#FDEDEC", fg=AD_TEXT,
                 font=(FONT, 10), wraplength=420, justify="left").pack(anchor="w")
        tk.Label(bc, text=f"โดย {member.get('banned_by') or '-'}  •  {fmt_datetime(member.get('banned_at'))}",
                 bg="#FDEDEC", fg=AD_MUTED, font=(FONT, 9)).pack(anchor="w")
    stats_row = tk.Frame(body, bg=AD_BG)
    stats_row.pack(fill="x", pady=(10, 4))
    stat_labels = {}
    for i, (key, title_text) in enumerate((("tier", "ระดับ"), ("points", "แต้ม"),
                                           ("orders", "ออเดอร์"), ("spent", "ยอดซื้อรวม"),
                                           ("coupons", "คูปองยังไม่ใช้"))):
        mini = RoundFrame(stats_row, fill="white", border=AD_LINE, radius=10, padx=10, pady=8)
        mini.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0))
        stats_row.grid_columnconfigure(i, weight=1, uniform="mini")
        tk.Label(mini.inner, text=title_text, bg="white", fg=AD_MUTED,
                 font=(FONT, 9)).pack(anchor="w")
        stat_labels[key] = tk.Label(mini.inner, text="-", bg="white", fg=AD_TEXT,
                                    font=(FONT, 12, "bold"))
        stat_labels[key].pack(anchor="w")
    tier_note = tk.Label(body, text="", bg=AD_BG, fg=AD_MUTED, font=(FONT, 10), anchor="w", justify="left",
                         wraplength=580)
    tier_note.pack(fill="x")
    hist_holder = tk.Frame(body, bg=AD_BG)

    def reload():
        fresh = next((m for m in admin_list_members() if m["member_id"] == mid), None)
        if fresh:
            t = tier_progress(fresh["lifetime"])
            nxt = (f"อีก {t['to_next']:,} แต้มถึง {t['next_tier']}" if t["next_tier"] else "ระดับสูงสุดแล้ว")
            tier_note.config(text=f"ระดับวัดจากแต้มสะสมทั้งหมด {fresh['lifetime']:,} แต้ม "
                                  f"(คงเหลือ {fresh['points']:,} + แลกส่วนลดไปแล้ว {fresh['lifetime'] - fresh['points']:,})"
                                  f"  •  {nxt}")
            stat_labels["tier"].config(text=t["tier"])
            stat_labels["points"].config(text=f"{fresh['points']:,}")
            stat_labels["orders"].config(text=f"{fresh['orders']}")
            stat_labels["spent"].config(text=baht(fresh["spent"]))
            stat_labels["coupons"].config(text=f"{fresh['coupons']}")
        for w in hist_holder.winfo_children():
            w.destroy()
        conn = get_conn()
        rows = conn.execute("SELECT history_id, created_at, type, points FROM point_history "
                            "WHERE member_id = ? ORDER BY history_id DESC LIMIT 100", (mid,)).fetchall()
        conn.close()
        kind = {"earn": "ได้รับแต้ม", "redeem": "แลกส่วนลด", "adjust": "แอดมินปรับแต้ม"}
        data = [(r[0], (fmt_datetime(r[1]), kind.get(r[2], r[2]), f"{r[3]:+d}")) for r in rows]
        frame, _ = ad_make_table(hist_holder, [("เวลา", 180, "w"), ("รายการ", 200, "w"),
                                               ("แต้ม", 80, "e")], data, height=6)
        frame.pack(fill="both", expand=True)

    reload()

    tools = tk.Frame(body, bg=AD_BG)
    tools.pack(fill="x", pady=8)
    tools.grid_columnconfigure(0, weight=1, uniform="tool")
    tools.grid_columnconfigure(1, weight=1, uniform="tool")
    box_card = RoundFrame(tools, fill=AD_CARD, border=AD_LINE, radius=12, padx=14, pady=12)
    box_card.grid(row=0, column=0, columnspan=2, sticky="nsew")
    box = box_card.inner
    tk.Label(box, text="ปรับแต้ม (เช่น 50 หรือ -20)", bg=AD_CARD, fg=AD_TEXT,
             font=(FONT, 11, "bold")).pack(anchor="w")
    row = tk.Frame(box, bg=AD_CARD)
    row.pack(fill="x", pady=(8, 0))
    delta_box = ad_entry(row, width=110)
    delta_box.pack(side="left")
    delta = delta_box.entry
    msg = tk.Label(body, text="", bg=AD_BG, fg=AD_MUTED, font=(FONT, 11), wraplength=560,
                   justify="left")

    def do_adjust():
        try:
            d = int(delta.get().strip())
        except ValueError:
            msg.config(text="กรุณาใส่จำนวนแต้มเป็นเลขจำนวนเต็ม", fg=AD_BAD)
            return
        ok, res = admin_adjust_points(mid, d)
        if ok:
            msg.config(text=f"ปรับแต้มแล้ว แต้มคงเหลือ {res}", fg=AD_OK)
            delta.delete(0, "end")
            reload()
            on_change()
        else:
            msg.config(text=res, fg=AD_BAD)

    ad_button(row, "ตกลง", do_adjust, "primary").pack(side="left", padx=8)


    if not banned:                               # แบนสมาชิก (ต้องใส่เหตุผล สมาชิกจะเห็นตอนเข้าสู่ระบบ)
        ban_card = RoundFrame(tools, fill=AD_CARD, border=AD_LINE, radius=12, padx=14, pady=12)
        ban_card.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        bc = ban_card.inner
        tk.Label(bc, text="แบนสมาชิก (เข้าสู่ระบบและสั่งซื้อไม่ได้ ข้อมูลและแต้มยังอยู่ ยกเลิกภายหลังได้)",
                 bg=AD_CARD, fg=AD_TEXT, font=(FONT, 11, "bold")).pack(anchor="w")
        row3 = tk.Frame(bc, bg=AD_CARD)
        row3.pack(fill="x", pady=(8, 0))
        reason_box = ad_entry(row3)
        reason_box.pack(side="left", fill="x", expand=True)
        reason = reason_box.entry

        def do_ban():
            text = reason.get()
            if not text.strip():
                msg.config(text="กรุณาระบุเหตุผลที่แบน (สมาชิกจะเห็นข้อความนี้)", fg=AD_BAD)
                return
            if not messagebox.askyesno("แบนสมาชิก", f"แบน {member['name']}?\nเหตุผล: {text.strip()}", parent=win):
                return
            ok, res = admin_ban_member(mid, text, getattr(parent, "admin", {}).get("name", "แอดมิน"))
            if not ok:
                msg.config(text=res, fg=AD_BAD)
                return
            reopen()

        ad_button(row3, "แบนสมาชิกนี้", do_ban, "danger").pack(side="left", padx=(8, 0))
        chips = tk.Frame(bc, bg=AD_CARD)
        chips.pack(anchor="w", pady=(6, 0))
        for text in MEMBER_BAN_REASONS:
            PillButton(chips, text, lambda t=text: (reason.delete(0, "end"), reason.insert(0, t)),
                       colors=AD_BUTTONS["ghost"], height=28, size=9, radius=8,
                       padx=10).pack(side="left", padx=(0, 6))
    msg.pack(anchor="w")

    def deleted(text):
        """ลบบัญชีสำเร็จ: ปิดหน้าต่างนี้ แล้วกลับไปหน้าสมาชิกพร้อมข้อความแจ้ง"""
        win.destroy()
        parent._members_flash = (text, True)
        on_change()

    bottom = tk.Frame(body, bg=AD_BG)
    bottom.pack(side="bottom", fill="x", pady=(10, 0))
    ad_button(bottom, "ปิด", win.destroy, "ghost").pack(side="right")
    ad_button(bottom, "ลบบัญชีสมาชิก", lambda: open_delete_member_dialog(win, parent, member, deleted),
              "danger").pack(side="left")
    tk.Label(body, text="ประวัติแต้มล่าสุด", bg=AD_BG, fg=AD_TEXT,
             font=(FONT, 11, "bold")).pack(anchor="w", pady=(6, 4))
    hist_holder.pack(fill="both", expand=True)


def member_logged_in(page, member_id):
    """สมาชิกคนนี้กำลังเข้าสู่ระบบอยู่ในโปรแกรมนี้ไหม (หน้าต่าง Main Menu หรือหน้าต่างหลัก)"""
    app = getattr(page, "app", None)
    for w in (getattr(app, "customer_window", None), app):
        try:
            if w is not None and w.winfo_exists() and \
                    (getattr(w, "current_member", None) or {}).get("member_id") == member_id:
                return True
        except tk.TclError:
            pass
    return False


def open_delete_member_dialog(owner, page, member, on_deleted):
    """ยืนยันการลบบัญชีสมาชิก: บอกว่าอะไรจะหาย อะไรยังเก็บไว้ แล้วให้พิมพ์เบอร์โทรของสมาชิกเพื่อยืนยัน
    ลบไม่ได้ถ้าสมาชิกกำลังเข้าสู่ระบบอยู่ หรือยังมีสลิปรอตรวจ/ออเดอร์ในคิวหลังร้าน"""
    mid, name = member["member_id"], member["name"]
    if member_logged_in(page, mid):
        messagebox.showwarning("ยังลบบัญชีไม่ได้", f"{name} กำลังเข้าสู่ระบบอยู่ที่หน้าลูกค้า\n"
                               "ให้ออกจากระบบก่อน แล้วค่อยลบบัญชี", parent=owner)
        return
    info = admin_member_delete_info(mid)
    if info is None:
        messagebox.showinfo("ลบบัญชีสมาชิก", "ไม่พบสมาชิกคนนี้ (อาจถูกลบไปแล้ว)", parent=owner)
        return
    if info["waiting_slips"] or info["in_queue"]:
        todo = []
        if info["waiting_slips"]:
            todo.append(f"สลิปรอตรวจ {info['waiting_slips']} ใบ (ตรวจที่หน้าการชำระเงิน)")
        if info["in_queue"]:
            todo.append(f"ออเดอร์ในคิวหลังร้าน {info['in_queue']} ออเดอร์ (ส่งเครื่องดื่มให้ลูกค้าก่อน)")
        messagebox.showwarning("ยังลบบัญชีไม่ได้", f"{name} ยังมีงานค้างอยู่:\n- " + "\n- ".join(todo) +
                               "\n\nจัดการให้เสร็จก่อน แล้วค่อยลบบัญชี", parent=owner)
        return

    win = ad_dialog(owner, "ลบบัญชีสมาชิก", 540, 540)
    body = tk.Frame(win, bg=AD_BG, padx=26, pady=20)
    body.pack(fill="both", expand=True)
    tk.Label(body, text=f"ลบบัญชี {name} ถาวร?", bg=AD_BG, fg=AD_BAD,
             font=(FONT, 16, "bold")).pack(anchor="w")
    tk.Label(body, text="ลบแล้วกู้คืนไม่ได้ ถ้าจะกลับมาใช้ สมาชิกต้องสมัครใหม่ด้วยเบอร์เดิมได้",
             bg=AD_BG, fg=AD_MUTED, font=(FONT, 10)).pack(anchor="w", pady=(2, 10))

    def card(title_text, lines, color):
        rf = RoundFrame(body, fill=AD_CARD, border=AD_LINE, radius=12, padx=14, pady=10)
        rf.pack(fill="x", pady=(0, 8))
        tk.Label(rf.inner, text=title_text, bg=AD_CARD, fg=color, font=(FONT, 11, "bold")).pack(anchor="w")
        for line in lines:
            tk.Label(rf.inner, text="•  " + line, bg=AD_CARD, fg=AD_TEXT, font=(FONT, 10),
                     wraplength=440, justify="left").pack(anchor="w", pady=(2, 0))

    gone = ["ชื่อ เบอร์โทร อีเมล รหัสผ่าน และรูปโปรไฟล์",
            f"แต้มคงเหลือ {info['points']:,} แต้ม และคูปองที่ยังไม่ใช้ {info['coupons']} ใบ",
            "ประวัติแต้มทั้งหมด"]
    if info["unpaid"]:
        gone.append(f"ออเดอร์ที่ยังไม่ชำระ {info['unpaid']} ออเดอร์ จะถูกยกเลิก")
    card("สิ่งที่จะถูกลบ", gone, AD_BAD)
    card("สิ่งที่ยังเก็บไว้",
         [f"ออเดอร์ที่ชำระแล้ว {info['paid_orders']} ออเดอร์ ยอด {baht(info['spent'])} ยังนับในรายงานยอดขาย",
          "หน้าออเดอร์และใบเสร็จจะแสดงชื่อเป็น \"ลูกค้าทั่วไป\""], AD_OK)

    tk.Label(body, text=f"พิมพ์เบอร์โทร {info['phone']} เพื่อยืนยัน", bg=AD_BG, fg=AD_TEXT,
             font=(FONT, 11, "bold")).pack(anchor="w", pady=(6, 4))
    phone_box = ad_entry(body)
    phone_box.pack(fill="x")
    phone = phone_box.entry
    msg = tk.Label(body, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 10), wraplength=480, justify="left")
    msg.pack(anchor="w", pady=(6, 0))

    def close():
        win.destroy()
        try:
            owner.grab_set()                     # คืนการล็อกโฟกัสให้หน้าต่างรายละเอียดสมาชิก
        except tk.TclError:
            pass

    def do_delete():
        ok, text = admin_delete_member(mid, phone.get())
        if not ok:
            msg.config(text=text)
            return
        win.destroy()
        on_deleted(text)

    btns = tk.Frame(body, bg=AD_BG)
    btns.pack(side="bottom", fill="x")
    ad_button(btns, "ลบบัญชีถาวร", do_delete, "danger", height=42).pack(side="left", fill="x", expand=True)
    ad_button(btns, "ยกเลิก", close, "ghost", height=42).pack(side="left", padx=(8, 0))
    win.protocol("WM_DELETE_WINDOW", close)
    phone.bind("<Return>", lambda e: do_delete())
    phone.focus_set()


# ---------------- หน้าหลักของแอดมิน ----------------
def draw_menu_pic(c, p, status, png=None):
    """กรอบรูปเมนูพื้นน้ำตาลดำแบบการ์ดหน้าลูกค้า + รูปเมนู (หรือรูปที่เพิ่งเลือก png) + ป้ายสถานะ
    ไม่มีรูป: วาดแก้วแทน พร้อมบอกให้กดเพื่ออัปโหลด"""
    c.delete("all")
    w, h = c.winfo_width(), c.winfo_height()
    if w < 20:
        w, h = int(c.cget("width")), int(c.cget("height"))
    rounded_rect(c, 0, 0, w, h, 12, fill=DRINK_CARD)
    photo = png_photo_fit(png, w - 24, h - 16) if png else load_product_image(p, w - 24, h - 16) if p else None
    if photo is not None:
        c.create_image(w / 2, h / 2, image=photo)
        c.photo = photo
    else:
        icon_cup(c, w / 2, h / 2 - 16, drink_color(p["name"]) if p else "#C9A47E")
        c.create_text(w / 2, h / 2 + 22, text="ยังไม่มีรูปเมนู", fill="#E8DCCB", font=(FONT, 11, "bold"))
        c.create_text(w / 2, h / 2 + 42, text="กดเพื่ออัปโหลดรูป", fill="#A8998A", font=(FONT, 9))
    chip = {"out": ("หมดแล้ว", AD_BAD), "low": ("ใกล้หมด", AD_WARN), "off": ("ปิดขาย", "#6B7785")}.get(status)
    if chip:
        tw = 16 + 9 * len(chip[0])
        rounded_rect(c, 8, 8, 8 + tw, 32, 12, fill=chip[1])
        c.create_text(8 + tw / 2, 20, text=chip[0], fill="white", font=(FONT, 9, "bold"))
    if p is not None and png is None:                      # บอกว่ากดรูปเพื่อเปลี่ยนได้
        rounded_rect(c, w - 84, h - 32, w - 8, h - 8, 12, fill="#3A322B")
        c.create_text(w - 46, h - 20, text="เปลี่ยนรูป", fill="white", font=(FONT, 9, "bold"))


def pick_menu_image(parent, title="เลือกรูปเมนู"):
    """เลือกไฟล์รูปเมนู แล้วแปลงเป็น PNG (make_menu_png)  ยกเลิก/เปิดไม่ได้คืนค่า None"""
    patterns = AVATAR_TYPES_PIL if HAS_PIL else AVATAR_TYPES_TK
    path = filedialog.askopenfilename(parent=parent, title=title,
                                      filetypes=[("รูปภาพ", " ".join(patterns)), ("ทุกไฟล์", "*.*")])
    if not path:
        return None
    try:
        return make_menu_png(path)
    except ValueError as e:
        messagebox.showerror("ใช้รูปนี้ไม่ได้", str(e), parent=parent)
        return None


def tier_bar(parent):
    """แถบเกณฑ์การเลื่อนระดับสมาชิก (หน้าสมาชิก): Silver 0+ / Gold 500+ / Platinum 1,500+ แต้มสะสมทั้งหมด"""
    card = RoundFrame(parent, fill=AD_CARD, border=AD_LINE, radius=12, padx=16, pady=10)
    row = tk.Frame(card.inner, bg=AD_CARD)
    row.pack(fill="x")
    tk.Label(row, text="เกณฑ์ระดับสมาชิก", bg=AD_CARD, fg=AD_TEXT, font=(FONT, 11, "bold")).pack(side="left")
    for name, need in sorted(TIERS, key=lambda t: t[1]):
        Pill(row, f"{name}  {need:,}+ แต้ม", TIER_COLORS.get(name, "#EEF1F5"), AD_SIDE, size=10,
             height=26, padx=12).pack(side="left", padx=(10, 0))
    note = tk.Label(card.inner, text=f"วัดจาก \"แต้มสะสมทั้งหมด\" ตั้งแต่สมัคร = แต้มคงเหลือ + แต้มที่แลกส่วนลดไปแล้ว "
                                     f"(แลกแต้มแล้วระดับไม่ลด)  •  ทุก {BAHT_PER_POINT} บาท ได้ 1 แต้ม  •  "
                                     f"เลื่อนระดับอัตโนมัติตอนชำระเงิน",
                    bg=AD_CARD, fg=AD_MUTED, font=(FONT, 10), anchor="w", justify="left")
    note.pack(fill="x", pady=(6, 0))
    card.inner.bind("<Configure>", lambda e: note.config(wraplength=max(200, e.width - 4)), add="+")
    return card


def flow_add(grid, card, min_w=200, max_cols=None):
    """ใส่การ์ดสรุปลงแถว จำนวนคอลัมน์ปรับตามความกว้างของหน้าต่าง
    (หน้าต่างแคบ เช่น แบ่งจอกับหน้าลูกค้า -> การ์ดขึ้นแถวใหม่ ตัวเลขไม่โดนตัด)"""
    if not hasattr(grid, "flow_cards"):
        grid.flow_cards, grid.flow_cols, grid.flow_opts = [], None, (min_w, max_cols)
        grid.bind("<Configure>", lambda e: _flow_layout(grid), add="+")
    grid.flow_cards.append(card)
    grid.flow_cols = None
    _flow_layout(grid)


def _flow_layout(grid):
    min_w, max_cols = grid.flow_opts
    cards = grid.flow_cards
    most = min(len(cards), max_cols or len(cards))
    w = grid.winfo_width()
    cols = most if w < 50 else max(1, min(most, w // min_w))
    if cols == grid.flow_cols:
        return
    grid.flow_cols = cols
    for i in range(len(cards)):
        grid.grid_columnconfigure(i, weight=1 if i < cols else 0, uniform="flow" if i < cols else "")
    for i, card in enumerate(cards):
        card.grid(row=i // cols, column=i % cols, sticky="nsew", padx=5, pady=5)


def kitchen_signature(orders):
    """สิ่งที่ต้องวาดหน้าคิวใหม่เมื่อเปลี่ยน: ออเดอร์ สถานะ ครั้งที่แจ้ง และแก้วที่ติ๊กแล้ว"""
    return tuple((o["order_id"], o["prep_status"], o["prep_seq"], o["cups_done"], o["prep_calls"])
                 for o in orders)


def draw_tick_box(c, done):
    """ช่องติ๊ก 24x24: เสร็จแล้ว = สีเขียวมีเครื่องหมายถูก"""
    c.delete("all")
    rounded_rect(c, 1, 1, 23, 23, 6, fill=AD_OK if done else "white", outline=AD_OK if done else "#AEB7C2",
                 width=2)
    if done:
        c.create_line(6.5, 12.5, 10.5, 16.5, 17.5, 8, fill="white", width=3, capstyle="round",
                      joinstyle="round")


def draw_progress(c, frac, color):
    """แถบความคืบหน้า (แก้วที่ทำเสร็จ / ทั้งหมด)"""
    c.delete("all")
    w, h = c.winfo_width(), c.winfo_height()
    if w < 10:
        return
    rounded_rect(c, 0, 0, w, h, h / 2, fill="#E6EAF0", outline="#E6EAF0")
    if frac > 0:
        rounded_rect(c, 0, 0, max(h, w * frac), h, h / 2, fill=color, outline=color)


class AdminNavItem(tk.Canvas):
    """เมนูด้านซ้ายของแอดมิน (แถบมุมมน + เส้นสีเหลืองบอกหน้าที่เปิดอยู่)"""

    def __init__(self, parent, text, command):
        super().__init__(parent, height=42, bg=AD_SIDE, highlightthickness=0, cursor="hand2")
        self.nav_text, self.nav_cmd = text, command
        self.nav_active = self.nav_hover = False
        self.badge = ("", AD_BAD)                 # ตัวเลขแจ้งเตือนด้านขวา (เช่น จำนวนเมนูใกล้หมด)
        self.bind("<Configure>", lambda e: self._paint())
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
        self.bind("<Button-1>", lambda e: self.nav_cmd())

    def _set_hover(self, on):
        self.nav_hover = on
        self._paint()

    def set_active(self, on):
        self.nav_active = on
        self._paint()

    def set_badge(self, text, color=AD_BAD):
        self.badge = (text, color)
        self._paint()

    def _paint(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 20:
            w, h = 230, 42
        if self.nav_active or self.nav_hover:
            rounded_rect(self, 12, 3, w - 12, h - 3, 10,
                         fill=AD_SIDE_HOVER if self.nav_active else "#26354A", outline="")
        if self.nav_active:
            rounded_rect(self, 12, 13, 16, h - 13, 2, fill=AD_ACCENT, outline=AD_ACCENT)
        self.create_text(30, h / 2, anchor="w", text=self.nav_text,
                         fill=AD_ACCENT if self.nav_active else ("white" if self.nav_hover else "#C9D3DF"),
                         font=(FONT, 11, "bold"))
        text, color = self.badge
        if text:
            bw = 14 + 8 * len(text)
            rounded_rect(self, w - 24 - bw, h / 2 - 11, w - 24, h / 2 + 11, 11, fill=color, outline=color)
            self.create_text(w - 24 - bw / 2, h / 2, text=text, fill="white", font=(FONT, 10, "bold"))


def parse_date(text):
    """อ่านวันที่ที่พิมพ์ เช่น 01/10/2026, 1/10/2569 (พ.ศ.), 2026-10-01  ผิดรูปแบบคืนค่า None"""
    parts = text.strip().replace(".", "/").replace("-", "/").split("/")
    if len(parts) != 3 or not all(x.isdigit() for x in parts):
        return None
    a, b, c = (int(x) for x in parts)
    d, m, y = (c, b, a) if a > 31 else (a, b, c)        # ปี-เดือน-วัน หรือ วัน/เดือน/ปี
    if y > 2400:                                          # ปี พ.ศ. -> ค.ศ.
        y -= 543
    try:
        return date(y, m, d)
    except ValueError:
        return None


class AdminPage(tk.Frame):
    NAV = [("dashboard", "ภาพรวม"), ("kitchen", "คิวหลังร้าน"), ("orders", "ออเดอร์"),
           ("payments", "การชำระเงิน"),
           ("products", "เมนูและสต็อก"), ("members", "สมาชิก"),
           ("report", "รายงานยอดขาย"), ("account", "บัญชีแอดมิน")]
    REPORT_PRESETS = [("today", "วันนี้"), ("7d", "7 วันล่าสุด"), ("month", "เดือนนี้"),
                      ("last_month", "เดือนที่แล้ว"), ("year", "ปีนี้"), ("all", "ทั้งหมด")]
    REPORT_TABS = [("products", "เมนูขายดี"), ("payments", "วิธีชำระเงิน"), ("hours", "ช่วงเวลาขายดี")]

    def __init__(self, app, admin, on_logout):
        super().__init__(app, bg=AD_BG)
        self.app = app
        self.admin = admin
        self.on_logout = on_logout
        self.nav_buttons = {}
        self.current_page = None
        self.order_filter = None
        # ตัวเลือกหน้ารายงาน (จำไว้ตอนสลับหน้า)
        self.report_state = {"preset": "month", "group": "day", "from": None, "to": None,
                             "tab": "products"}
        self.stock_filter = "all"                   # ตัวกรองหน้าเมนูและสต็อก (จำไว้ตอนสลับหน้า)
        self.product_search = ""                    # คำค้นหน้าเมนูและสต็อก
        self._products_flash = None                 # ข้อความหลังเติมสต็อก/เปลี่ยนรูป (ข้อความ, สำเร็จไหม, เวลา)
        self._product_sections = []                 # [(กรอบ grid, [การ์ด])] ไว้จัดคอลัมน์ใหม่ตอนหน้าต่างเปลี่ยนขนาด
        self._product_cols = 0
        self.member_filter = "all"                  # ตัวกรองหน้าสมาชิก: ทั้งหมด / ใช้งานได้ / ถูกแบน
        self._members_flash = None                  # ข้อความหลังลบบัญชีสมาชิก (ข้อความ, สำเร็จไหม)
        self._account_flash = None                  # ข้อความล่าสุดบนหน้าบัญชีแอดมิน (ข้อความ, สำเร็จไหม)
        self._pay_flash = None                      # ข้อความล่าสุดบนหน้าการชำระเงิน (ข้อความ, สำเร็จไหม)
        self._slip_ids = None                       # สลิปรอตรวจที่หน้าจอแสดงอยู่ (ไว้ดูว่ามีสลิปใหม่ไหม)
        self._slip_job = None
        self._kitchen_sig = None                    # ออเดอร์ในคิวหลังร้านที่หน้าจอแสดงอยู่ (ไว้ดูว่ามีอะไรเปลี่ยน)
        self._kitchen_counts = None                 # จำนวนรอคิว/กำลังทำ/พร้อมรับ (ตัวเลขที่เมนู + หน้าภาพรวม)
        self._kitchen_flash = None                  # ข้อความหลังกดปุ่มที่หน้าคิว (ข้อความ, สำเร็จไหม, ย้อนกลับ, เวลา)
        self._kitchen_timers = []                   # ป้าย "รอมาแล้ว N นาที" ที่อัปเดตทุกครั้งที่เช็กคิว
        self._kitchen_scroll = None                 # ตำแหน่งเลื่อนเดิมตอนวาดหน้าคิวใหม่

        side = tk.Frame(self, bg=AD_SIDE, width=230)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)
        head = tk.Frame(side, bg=AD_SIDE)
        head.pack(anchor="w", padx=22, pady=(26, 0))
        logo_canvas(head, 48).pack(side="left", padx=(0, 10))
        brand = tk.Frame(head, bg=AD_SIDE)
        brand.pack(side="left")
        Pill(brand, "ADMIN", AD_ACCENT, AD_SIDE, size=9, height=24, padx=12).pack(anchor="w")
        tk.Label(brand, text=SHOP_NAME, bg=AD_SIDE, fg="white",
                 font=(FONT, 15, "bold")).pack(anchor="w", pady=(2, 0))
        tk.Label(side, text="ระบบจัดการหลังร้าน", bg=AD_SIDE, fg="#9FB0C3",
                 font=(FONT, 11)).pack(anchor="w", padx=24, pady=(8, 14))
        tk.Label(side, text="เมนู", bg=AD_SIDE, fg="#7D8DA1",
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=26, pady=(0, 4))
        for key, label in self.NAV:
            b = AdminNavItem(side, label, lambda k=key: self.go(k))
            b.pack(fill="x")
            self.nav_buttons[key] = b
        bottom = tk.Frame(side, bg=AD_SIDE)
        bottom.pack(side="bottom", fill="x", pady=20, padx=18, before=head)   # จอเตี้ย: ปุ่มออกจากระบบยังเห็นเสมอ
        user = tk.Frame(bottom, bg=AD_SIDE)
        user.pack(fill="x", pady=(0, 10))
        av = tk.Canvas(user, width=34, height=34, bg=AD_SIDE, highlightthickness=0)
        av.pack(side="left")
        aa_oval(av, 1, 1, 33, 33, fill=AD_SIDE_HOVER, outline=AD_ACCENT, width=2)
        av.create_text(17, 17, text=member_initial(admin["name"]), fill="white",
                       font=(FONT, 11, "bold"))
        who = tk.Frame(user, bg=AD_SIDE)
        who.pack(side="left", padx=8)
        tk.Label(who, text=admin["name"], bg=AD_SIDE, fg="white",
                 font=(FONT, 11, "bold"), anchor="w").pack(anchor="w")
        tk.Label(who, text=f"@{admin['username']}", bg=AD_SIDE, fg="#9FB0C3",
                 font=(FONT, 9), anchor="w").pack(anchor="w")
        ad_button(bottom, "Main Menu", self.open_customer_window,          # เปิดหน้าลูกค้าเป็นหน้าต่างใหม่
                  "side").pack(fill="x", pady=(0, 8))
        ad_button(bottom, "ออกจากระบบแอดมิน", on_logout, "accent").pack(fill="x")

        self.content = tk.Frame(self, bg=AD_BG, padx=26, pady=22)
        self.content.pack(side="left", fill="both", expand=True)
        self.go("dashboard")
        self._slip_job = self.after(3000, self._poll_slips)

    def destroy(self):
        if self._slip_job:
            self.after_cancel(self._slip_job)
            self._slip_job = None
        super().destroy()

    # ---- สลับหน้า ----
    def go(self, key):
        if key == "stock":                      # หน้าสต็อกรวมอยู่ในหน้า "เมนูและสต็อก" แล้ว
            key = "products"
        self.current_page = key
        for k, b in self.nav_buttons.items():
            b.set_active(k == key)
        for w in self.content.winfo_children():
            w.destroy()
        self._slip_ids = tuple(s["slip_id"] for s in admin_list_slips("waiting"))
        self._kitchen_timers = []
        getattr(self, "page_" + key)()
        self._refresh_stock_badge()
        self._refresh_slip_badge()
        self._refresh_kitchen_badge()

    def _refresh_slip_badge(self):
        """ตัวเลขที่เมนู "การชำระเงิน" = จำนวนสลิปที่รอตรวจ"""
        n = len(self._slip_ids or ())
        self.nav_buttons["payments"].set_badge(str(n) if n else "", AD_WARN)

    def _poll_slips(self):
        """เช็กทุก 3 วินาที: สลิปใหม่จากลูกค้า และคิวหลังร้าน (ออเดอร์ใหม่ที่เพิ่งชำระ)
        อัปเดตตัวเลขที่เมนู และรีเฟรชหน้าภาพรวม / การชำระเงิน / คิวหลังร้าน เมื่อมีอะไรเปลี่ยน"""
        self._slip_job = None
        if not self.winfo_exists():
            return
        idle = not self.grab_current()             # ไม่รีเฟรชตอนมีหน้าต่างย่อยเปิดอยู่
        ids = tuple(s["slip_id"] for s in admin_list_slips("waiting"))
        counts = self._kitchen_count_tuple()
        if ids != self._slip_ids:
            if self.current_page in ("dashboard", "payments") and idle:
                self.go(self.current_page)
            else:
                self._slip_ids = ids
                self._refresh_slip_badge()
        if self.current_page == "kitchen" and idle:
            if kitchen_signature(admin_kitchen_orders()) != self._kitchen_sig:
                self._kitchen_refresh()
            else:
                self._tick_kitchen_timers()
        elif counts != self._kitchen_counts:
            if self.current_page == "dashboard" and idle:
                self.go("dashboard")
            else:
                self._refresh_kitchen_badge()
        self._slip_job = self.after(3000, self._poll_slips)

    def _kitchen_count_tuple(self):
        k = admin_kitchen_summary()
        return k["queued"], k["making"], k["ready"]

    def _refresh_kitchen_badge(self):
        """ตัวเลขที่เมนู "คิวหลังร้าน" = ออเดอร์ที่ยังต้องทำ (รอคิว + กำลังทำ)"""
        self._kitchen_counts = self._kitchen_count_tuple()
        n = self._kitchen_counts[0] + self._kitchen_counts[1]
        self.nav_buttons["kitchen"].set_badge(str(n) if n else "", AD_WARN)

    def open_customer_window(self):
        """ปุ่ม "Main Menu": เปิด "หน้าลูกค้า" เป็นหน้าต่างแยกแบบเต็มจอ (มีแถบชื่อ จัดวางคู่กับหน้าแอดมินเองได้)
        เปิดอยู่แล้วจะดึงหน้าต่างเดิมขึ้นมาแทนการเปิดซ้ำ (อยู่ตำแหน่งเดิมที่จัดไว้)"""
        w = getattr(self.app, "customer_window", None)
        if w is not None and w.winfo_exists():
            w.deiconify()
            w.lift()
            w.focus_force()
            return
        self.app.customer_window = CustomerWindow(self.app)

    def after_slip_checked(self, text, ok):
        self._pay_flash = (text, ok)

    def send_receipt_async(self, order_id, email):
        """ส่งใบเสร็จ PDF ให้ลูกค้าหลังยืนยันสลิป (ทำในเธรดแยก โปรแกรมไม่ค้าง แจ้งผลบนหน้าการชำระเงิน)"""
        code = order_code(order_id)
        holder = {}

        def work():
            try:
                send_receipt_email(order_id, email)
                holder["r"] = (True, "")
            except Exception as e:
                holder["r"] = (False, explain_email_error(e))

        def check():
            if not self.winfo_exists():
                return
            if "r" not in holder:
                self.after(300, check)
                return
            ok, err = holder["r"]
            self._pay_flash = ((f"ส่งใบเสร็จ {code} ไปที่ {email} แล้ว", True) if ok else
                               (f"ส่งใบเสร็จ {code} ไม่สำเร็จ: {err} (กดส่งใหม่ได้ที่รายละเอียดออเดอร์)", False))
            if self.current_page == "payments" and not self.grab_current():
                self.go("payments")

        threading.Thread(target=work, daemon=True).start()
        self.after(300, check)

    def _refresh_stock_badge(self):
        """ตัวเลขแดง/ส้มที่เมนู "เมนูและสต็อก" = จำนวนเมนูที่หมดหรือใกล้หมด"""
        alerts = admin_stock_alerts()
        n = len(alerts["out"]) + len(alerts["low"])
        self.nav_buttons["products"].set_badge(str(n) if n else "", AD_BAD if alerts["out"] else AD_WARN)

    def _kitchen_banner(self):
        """แถบแจ้งเตือนบนหน้าภาพรวม: มีออเดอร์ที่ต้องทำ / พร้อมรับแต่ลูกค้ายังไม่มารับ"""
        k = admin_kitchen_summary()
        if not (k["queued"] or k["making"] or k["ready"]):
            return
        card = RoundFrame(self.content, fill="#EEF4FB", border="#5B7DB1", radius=12, padx=16, pady=10)
        card.pack(fill="x", padx=5, pady=(0, 8))
        row = card.inner
        bg = bg_of(row)
        icon = tk.Canvas(row, width=30, height=30, bg=bg, highlightthickness=0)
        icon.pack(side="left", padx=(0, 12))
        aa_oval(icon, 1, 1, 29, 29, fill="#5B7DB1", outline="")
        icon.create_text(15, 15, text=str(k["queued"] + k["making"]), fill="white", font=(FONT, 12, "bold"))
        ad_button(row, "ไปที่คิวหลังร้าน", lambda: self.go("kitchen"), "primary", height=34).pack(side="right")
        tk.Label(row, text=f"ออเดอร์หลังร้าน: รอคิว {k['queued']}  •  กำลังทำ {k['making']}  •  "
                           f"พร้อมรับ {k['ready']}   (รวม {k['cups_waiting']} แก้วที่ยังต้องทำ)",
                 bg=bg, fg=AD_TEXT, font=(FONT, 11, "bold")).pack(side="left")

    def _slip_banner(self):
        """แถบแจ้งเตือนบนหน้าภาพรวม: มีสลิปโอนเงินรอตรวจ"""
        n, money = admin_payment_summary()["waiting"]
        if not n:
            return
        card = RoundFrame(self.content, fill="#FFF7E8", border=AD_WARN, radius=12, padx=16, pady=10)
        card.pack(fill="x", padx=5, pady=(0, 8))
        row = card.inner
        bg = bg_of(row)
        icon = tk.Canvas(row, width=30, height=30, bg=bg, highlightthickness=0)
        icon.pack(side="left", padx=(0, 12))
        aa_oval(icon, 1, 1, 29, 29, fill=AD_WARN, outline="")
        icon.create_text(15, 15, text="฿", fill="white", font=(FONT, 13, "bold"))
        ad_button(row, "ไปตรวจสลิป", lambda: self.go("payments"), "primary", height=34).pack(side="right")
        tk.Label(row, text=f"มีสลิปโอนเงินรอตรวจสอบ {n} รายการ (รวม {baht(money)})", bg=bg, fg=AD_TEXT,
                 font=(FONT, 11, "bold")).pack(side="left")

    def _stock_banner(self):
        """แถบแจ้งเตือนสต็อกบนหน้าภาพรวม (แสดงเมื่อมีเมนูหมด/ใกล้หมด)"""
        alerts = admin_stock_alerts()
        if not alerts["out"] and not alerts["low"]:
            return
        color = AD_BAD if alerts["out"] else AD_WARN
        card = RoundFrame(self.content, fill="#FFF7E8" if not alerts["out"] else "#FDEDEC",
                          border=color, radius=12, padx=16, pady=10)
        card.pack(fill="x", padx=5, pady=(0, 8))
        row = card.inner
        bg = bg_of(row)
        icon = tk.Canvas(row, width=30, height=30, bg=bg, highlightthickness=0)
        icon.pack(side="left", padx=(0, 12))
        aa_oval(icon, 1, 1, 29, 29, fill=color, outline="")
        icon.create_text(15, 15, text="!", fill="white", font=(FONT, 14, "bold"))
        ad_button(row, "ไปเติมสต็อก", lambda: self._show_stock("out" if alerts["out"] else "low"), "primary",
                  height=34).pack(side="right")
        texts = tk.Frame(row, bg=bg)
        texts.pack(side="left", fill="x", expand=True)
        tk.Label(texts, text="แจ้งเตือนสต็อกสินค้า", bg=bg, fg=AD_TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w")

        def names(items):
            more = f"  และอีก {len(items) - 4} เมนู" if len(items) > 4 else ""
            return ", ".join(items[:4]) + more

        if alerts["out"]:
            tk.Label(texts, text=f"หมดแล้ว {len(alerts['out'])} เมนู: {names(alerts['out'])}", bg=bg,
                     fg=AD_BAD, font=(FONT, 10, "bold")).pack(anchor="w")
        if alerts["low"]:
            low = [f"{n} (เหลือ {s})" for n, s in alerts["low"]]
            tk.Label(texts, text=f"ใกล้หมด {len(low)} เมนู: {names(low)}", bg=bg,
                     fg=AD_WARN, font=(FONT, 10, "bold")).pack(anchor="w")

    def _header(self, text, sub=""):
        head = tk.Frame(self.content, bg=AD_BG)
        head.pack(fill="x", pady=(0, 14))
        left = tk.Frame(head, bg=AD_BG)
        left.pack(side="left")
        tk.Label(left, text=text, bg=AD_BG, fg=AD_TEXT, font=(FONT, 20, "bold")).pack(anchor="w")
        actions = tk.Frame(head, bg=AD_BG)
        actions.pack(side="right")
        if sub:                                     # คำอธิบายยาว: ขึ้นบรรทัดใหม่ตามความกว้าง (ไม่โดนตัด)
            sub_label = tk.Label(left, text=sub, bg=AD_BG, fg=AD_MUTED, font=(FONT, 11), justify="left",
                                 anchor="w")
            sub_label.pack(anchor="w")
            head.bind("<Configure>", lambda e: sub_label.config(
                wraplength=max(240, e.width - actions.winfo_reqwidth() - 24)), add="+")
        return actions

    # ---- ภาพรวม ----
    def page_dashboard(self):
        s = admin_stats()
        actions = self._header("ภาพรวมร้าน",
                               f"ข้อมูล ณ {thai_now().strftime('%d/%m/%Y %H:%M')}")
        ad_button(actions, "รีเฟรช", lambda: self.go("dashboard"), "ghost").pack()
        self._kitchen_banner()
        self._slip_banner()
        self._stock_banner()

        # (หัวข้อ, ค่า, สีตัวเลข, สีจุดนำหน้า)
        cards = [("ยอดขายวันนี้", baht(s["today_sales"]), AD_OK, AD_OK),
                 ("ออเดอร์วันนี้", f"{s['today_orders']} ออเดอร์", AD_TEXT, AD_SIDE),
                 ("สมาชิกทั้งหมด", f"{s['members']} คน", AD_TEXT, "#5B7DB1"),
                 ("ยอดขายรวม", baht(s["total_sales"]), AD_OK, AD_OK),
                 ("ส่วนลดที่ให้ไปแล้ว", baht(s["total_discount"]), AD_TEXT, AD_ACCENT),
                 ("เมนูในระบบ", f"{s['products']} (ปิดขาย {s['unavailable']})",
                  AD_BAD if s["unavailable"] else AD_TEXT, AD_BAD if s["unavailable"] else AD_SIDE),
                 ("คูปองที่ยังไม่ใช้", f"{s['unused_coupons']} ใบ", AD_TEXT, "#8E6CC0")]
        grid = tk.Frame(self.content, bg=AD_BG)
        grid.pack(fill="x")
        for i, (label, value, color, dot) in enumerate(cards):
            card = RoundFrame(grid, fill=AD_CARD, border=AD_LINE, radius=14, padx=18, pady=14)
            flow_add(grid, card, 210, max_cols=4)
            head = tk.Frame(card.inner, bg=AD_CARD)
            head.pack(anchor="w")
            d = tk.Canvas(head, width=10, height=10, bg=AD_CARD, highlightthickness=0)
            aa_oval(d, 1, 1, 9, 9, fill=dot, outline="")
            d.pack(side="left", padx=(0, 6))
            tk.Label(head, text=label, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 11)).pack(side="left")
            tk.Label(card.inner, text=value, bg=AD_CARD, fg=color,
                     font=(FONT, 16, "bold")).pack(anchor="w", pady=(6, 0))

        lower = tk.Frame(self.content, bg=AD_BG)
        lower.pack(fill="both", expand=True, pady=(10, 0))
        chart_card = RoundFrame(lower, fill=AD_CARD, border=AD_LINE, radius=14, padx=18, pady=14)
        chart_card.pack(side="left", fill="both", expand=True, padx=(5, 6))
        chart_box = chart_card.inner
        tk.Label(chart_box, text="ยอดขาย 7 วันล่าสุด (บาท)", bg=AD_CARD, fg=AD_TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w")
        cv = tk.Canvas(chart_box, width=480, height=240, bg=AD_CARD, highlightthickness=0)
        cv.pack(fill="both", expand=True, pady=(6, 0))
        cv.bind("<Configure>", lambda e: self._draw_chart(cv, s["last7"]))

        top_card = RoundFrame(lower, fill=AD_CARD, border=AD_LINE, radius=14, padx=18, pady=14)
        top_card.pack(side="right", fill="y", padx=(0, 5), before=chart_card)   # ได้พื้นที่ก่อนกราฟ (จอแคบไม่โดนตัด)
        top_box = top_card.inner
        tk.Frame(top_box, bg=AD_CARD, width=260, height=1).pack()
        tk.Label(top_box, text="เมนูขายดี 5 อันดับ", bg=AD_CARD, fg=AD_TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w")
        if not s["top_products"]:
            tk.Label(top_box, text="ยังไม่มียอดขาย", bg=AD_CARD, fg=AD_MUTED,
                     font=(FONT, 11)).pack(anchor="w", pady=10)
        for n, (pname, qty, money) in enumerate(s["top_products"], 1):
            r = tk.Frame(top_box, bg=AD_CARD)
            r.pack(fill="x", pady=(10, 0))
            badge = tk.Canvas(r, width=28, height=28, bg=AD_CARD, highlightthickness=0)
            badge.pack(side="left", anchor="n")
            rounded_rect(badge, 0, 0, 28, 28, 8, fill=AD_ACCENT if n == 1 else "#EEF1F5",
                         outline="")
            badge.create_text(14, 14, text=str(n), fill=AD_SIDE, font=(FONT, 11, "bold"))
            t = tk.Frame(r, bg=AD_CARD)
            t.pack(side="left", padx=10)
            tk.Label(t, text=pname, bg=AD_CARD, fg=AD_TEXT, font=(FONT, 11, "bold"),
                     anchor="w").pack(anchor="w")
            tk.Label(t, text=f"ขายได้ {qty} แก้ว  •  {baht(money)}", bg=AD_CARD, fg=AD_MUTED,
                     font=(FONT, 11)).pack(anchor="w")

    def _draw_chart(self, cv, data):
        """กราฟแท่งยอดขาย (วาดใหม่ทุกครั้งที่ขนาดกรอบเปลี่ยน ให้แท่งครบ 7 วันเสมอ)"""
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 120 or h < 120:
            return
        top = max([v for _, v in data] + [1])
        left, bottom = 52, h - 28
        usable_h = bottom - 30
        n = len(data)
        slot = (w - left - 8) / n
        for frac in (0, 0.5, 1):
            y = bottom - usable_h * frac
            cv.create_line(left, y, w - 6, y, fill="#E6EAF0", dash=() if frac == 0 else (3, 3))
            cv.create_text(left - 8, y, text=fmt_price(top * frac), anchor="e",
                           fill=AD_MUTED, font=(FONT, 9))
        for i, (d, v) in enumerate(data):
            x0 = left + i * slot + slot * 0.24
            x1 = left + (i + 1) * slot - slot * 0.24
            y = bottom - usable_h * (v / top)
            col = AD_ACCENT if i == n - 1 else AD_SIDE
            if bottom - y >= 10:
                rounded_rect(cv, x0, y, x1, bottom, 6, fill=col, outline=col)
                cv.create_rectangle(x0, bottom - 6, x1, bottom, fill=col, outline=col)
            elif v:
                cv.create_rectangle(x0, bottom - 3, x1, bottom, fill=col, outline=col)
            if v:
                cv.create_text((x0 + x1) / 2, y - 10, text=fmt_price(v), fill=AD_TEXT,
                               font=(FONT, 9, "bold"))
            cv.create_text((x0 + x1) / 2, bottom + 14,
                           text="วันนี้" if i == n - 1 else d[8:10] + "/" + d[5:7],
                           fill=AD_TEXT if i == n - 1 else AD_MUTED,
                           font=(FONT, 9, "bold" if i == n - 1 else "normal"))

    # ---- คิวหลังร้าน: เปลี่ยนสถานะออเดอร์ แจ้งลูกค้า ----
    KITCHEN_COLUMNS = [("queued", "รอคิว", "#5B7DB1"), ("making", "กำลังทำ", AD_WARN), ("ready", "พร้อมรับ", AD_OK)]

    def page_kitchen(self):
        """ออเดอร์ที่ชำระแล้ว 3 ช่อง: รอคิว -> กำลังทำ -> พร้อมรับ
        ทุกปุ่ม (เริ่มทำ / พร้อมรับ / เรียกอีกครั้ง / ลูกค้ารับแล้ว / ย้อนกลับ) แจ้งลูกค้าทันที
        ติ๊กแก้วที่ทำเสร็จทีละรายการ ลูกค้าเห็นว่าเสร็จแล้วกี่แก้ว (ติ๊กแก้วแรก = เริ่มทำให้อัตโนมัติ)"""
        k = admin_kitchen_summary()
        orders = admin_kitchen_orders()
        self._kitchen_sig = kitchen_signature(orders)
        actions = self._header("คิวหลังร้าน", "กดปุ่มที่การ์ดเพื่อเปลี่ยนสถานะ ลูกค้าจะเห็นสถานะและได้รับแจ้งเตือนที่หน้าจอทันที "
                                             "(อัปเดตอัตโนมัติ)")
        ad_button(actions, "รีเฟรช", self._kitchen_refresh, "ghost").pack()
        flash = self._kitchen_flash
        if flash and time.time() - flash[3] < 30:
            text, ok, undo, _ = flash
            line = tk.Frame(self.content, bg=AD_BG)
            line.pack(fill="x", pady=(0, 8))
            tk.Label(line, text=text, bg=AD_BG, fg=AD_OK if ok else AD_BAD,
                     font=(FONT, 11, "bold")).pack(side="left")
            if undo:
                LinkButton(line, "ย้อนกลับ", lambda: self._prep(*undo), fg="#5B7DB1", hover=AD_TEXT,
                           size=10, bold=True).pack(side="left", padx=(12, 0))

        cards = [("รอคิว", f"{k['queued']} ออเดอร์", "#5B7DB1"),
                 ("กำลังทำ", f"{k['making']} ออเดอร์", AD_WARN),
                 ("พร้อมรับ (รอลูกค้ามารับ)", f"{k['ready']} ออเดอร์", AD_OK),
                 ("แก้วที่ยังต้องทำ", f"{k['cups_waiting']} แก้ว", AD_TEXT),
                 ("ลูกค้ารับแล้ววันนี้", f"{k['picked_today']} ออเดอร์", AD_MUTED)]
        grid = tk.Frame(self.content, bg=AD_BG)
        grid.pack(fill="x")
        for i, (label, value, color) in enumerate(cards):
            card = RoundFrame(grid, fill=AD_CARD, border=AD_LINE, radius=14, padx=16, pady=10)
            flow_add(grid, card, 200)
            tk.Label(card.inner, text=label, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 10)).pack(anchor="w")
            tk.Label(card.inner, text=value, bg=AD_CARD, fg=color, font=(FONT, 15, "bold")).pack(anchor="w")

        sf = ScrollFrame(self.content, AD_BG)
        sf.pack(fill="both", expand=True, pady=(8, 0))
        self._kitchen_sf = sf
        board = tk.Frame(sf.inner, bg=AD_BG)
        board.pack(fill="x")
        by_status = {key: [o for o in orders if o["prep_status"] == key] for key, _, _ in self.KITCHEN_COLUMNS}
        for col, (key, title, color) in enumerate(self.KITCHEN_COLUMNS):
            board.grid_columnconfigure(col, weight=1, uniform="kcol")
            column = tk.Frame(board, bg=AD_BG)
            column.grid(row=0, column=col, sticky="new", padx=5)
            head = tk.Frame(column, bg=AD_BG)
            head.pack(fill="x", pady=(6, 6))
            d = tk.Canvas(head, width=12, height=12, bg=AD_BG, highlightthickness=0)
            d.pack(side="left")
            aa_oval(d, 1, 1, 11, 11, fill=color, outline="")
            tk.Label(head, text=f"{title} ({len(by_status[key])})", bg=AD_BG, fg=AD_TEXT,
                     font=(FONT, 13, "bold")).pack(side="left", padx=(8, 0))
            if not by_status[key]:
                tk.Label(column, text={"queued": "ไม่มีออเดอร์รอคิว", "making": "ยังไม่มีออเดอร์ที่กำลังทำ",
                                       "ready": "ไม่มีออเดอร์รอลูกค้ามารับ"}[key],
                         bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w", pady=(8, 0))
            for o in by_status[key]:
                self._kitchen_card(column, o, color)
        if self._kitchen_scroll is not None:                      # วาดใหม่แล้วอยู่ตำแหน่งเดิม
            pos, self._kitchen_scroll = self._kitchen_scroll, None
            sf.update_idletasks()
            sf.canvas.yview_moveto(pos)

    def _kitchen_card(self, parent, o, color):
        """การ์ดออเดอร์ 1 ใบ: เลขออเดอร์ เวลารอ ลูกค้า รายการแก้ว (ติ๊กได้) ความคืบหน้า และปุ่มเปลี่ยนสถานะ"""
        st, oid = o["prep_status"], o["order_id"]
        card = RoundFrame(parent, fill=AD_CARD, border=color, radius=12, padx=14, pady=12)
        card.pack(fill="x", pady=(0, 10))
        c = card.inner
        top = tk.Frame(c, bg=AD_CARD)
        top.pack(fill="x")
        tk.Label(top, text=order_code(oid), bg=AD_CARD, fg=AD_TEXT, font=(FONT, 14, "bold")).pack(side="left")
        if st == "queued":
            ad_chip(top, f"คิวที่ {o['ahead_orders'] + 1}", "#5B7DB1").pack(side="left", padx=(8, 0))
        timer = tk.Label(top, bg=AD_CARD, font=(FONT, 10, "bold"))
        timer.pack(side="right")
        since = o["ready_at"] if st == "ready" and o["ready_at"] else o["paid_at"]
        self._kitchen_timers.append((timer, since, st))
        self._set_timer(timer, since, st)
        who = o["member_name"] or "ลูกค้าทั่วไป"
        if o["member_phone"]:
            who += f"  •  {o['member_phone']}"
        tk.Label(c, text=who, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 10), anchor="w").pack(fill="x")

        tickable = st in ("queued", "making")
        for it in o["items"]:
            row = tk.Frame(c, bg=AD_CARD, cursor="hand2" if tickable else "")
            row.pack(fill="x", pady=(8, 0))
            box = tk.Canvas(row, width=24, height=24, bg=AD_CARD, highlightthickness=0,
                            cursor="hand2" if tickable else "")
            box.pack(side="left", anchor="n", pady=(2, 0))
            draw_tick_box(box, it["done"])
            texts = tk.Frame(row, bg=AD_CARD)
            texts.pack(side="left", fill="x", expand=True, padx=(10, 0))
            name = tk.Label(texts, text=f"{it['quantity']} × {it['name']}", bg=AD_CARD,
                            fg=AD_MUTED if it["done"] else AD_TEXT, font=(FONT, 11, "bold"), anchor="w")
            name.pack(fill="x")
            parts = [name, box, row, texts]
            if it["options"]:
                opt = tk.Label(texts, text=it["options"], bg=AD_CARD, fg=AD_MUTED, font=(FONT, 9),
                               anchor="w", justify="left", wraplength=240)
                opt.pack(fill="x")
                texts.bind("<Configure>", lambda e, lb=opt: lb.config(wraplength=max(120, e.width - 4)), add="+")
                parts.append(opt)
            if tickable:
                for w in parts:
                    w.bind("<Button-1>", lambda e, i=it["item_id"]: self._toggle_item(i, o))

        bar = tk.Canvas(c, height=8, bg=AD_CARD, highlightthickness=0)
        bar.pack(fill="x", pady=(10, 2))
        frac = o["cups_done"] / o["cups"] if o["cups"] else 0
        bar.bind("<Configure>", lambda e, f=frac: draw_progress(e.widget, f, color))
        tk.Label(c, text=f"เสร็จแล้ว {o['cups_done']}/{o['cups']} แก้ว", bg=AD_CARD, fg=AD_MUTED,
                 font=(FONT, 10), anchor="w").pack(fill="x")

        btns = tk.Frame(c, bg=AD_CARD)
        btns.pack(fill="x", pady=(10, 0))
        if st == "queued":
            ad_button(btns, "เริ่มทำ", lambda: self._prep(oid, "making"), "accent", height=36).pack(side="left")
        elif st == "making":
            ad_button(btns, "พร้อมรับ • เรียกลูกค้า", lambda: self._prep(oid, "ready"), "ok",
                      height=36).pack(side="left")
            LinkButton(btns, "ย้อนกลับไปรอคิว", lambda: self._prep(oid, "queued"), fg=AD_MUTED, hover=AD_TEXT,
                       size=9).pack(side="right")
        else:
            ad_button(btns, "ลูกค้ารับแล้ว", lambda: self._prep(oid, "picked_up", undo=(oid, "ready")), "ok",
                      height=36).pack(side="left")
            ad_button(btns, "เรียกอีกครั้ง", lambda: self._call_again(oid), "accent",
                      height=36).pack(side="left", padx=(8, 0))
            LinkButton(btns, "ย้อนกลับ", lambda: self._prep(oid, "making"), fg=AD_MUTED, hover=AD_TEXT,
                       size=9).pack(side="right")
            if o["prep_calls"]:
                tk.Label(c, text=f"เรียกซ้ำแล้ว {o['prep_calls']} ครั้ง", bg=AD_CARD, fg=AD_WARN,
                         font=(FONT, 9, "bold"), anchor="w").pack(fill="x", pady=(4, 0))

    def _set_timer(self, label, since, status):
        """ป้ายเวลาที่มุมการ์ด: รอมาแล้วกี่นาที (นานเกิน 10/20 นาทีเปลี่ยนเป็นสีส้ม/แดง)"""
        try:
            mins = max(0, int((thai_now() - datetime.strptime(since, "%Y-%m-%d %H:%M:%S")).total_seconds() // 60))
        except (TypeError, ValueError):
            label.config(text="", fg=AD_MUTED)
            return
        if status == "ready":
            label.config(text=f"พร้อมแล้ว {mins} นาที" if mins else "เพิ่งพร้อม",
                         fg=AD_BAD if mins >= 10 else AD_OK)
        else:
            label.config(text=f"รอมาแล้ว {mins} นาที" if mins else "เพิ่งสั่ง",
                         fg=AD_BAD if mins >= 20 else AD_WARN if mins >= 10 else AD_MUTED)

    def _tick_kitchen_timers(self):
        for label, since, status in self._kitchen_timers:
            if label.winfo_exists():
                self._set_timer(label, since, status)

    def _kitchen_refresh(self):
        """วาดหน้าคิวใหม่โดยเลื่อนอยู่ตำแหน่งเดิม"""
        sf = getattr(self, "_kitchen_sf", None)
        if self.current_page == "kitchen" and sf is not None and sf.winfo_exists():
            self._kitchen_scroll = sf.canvas.yview()[0]
        self.go("kitchen")

    def _prep(self, order_id, status, undo=None):
        """เปลี่ยนสถานะหลังร้าน แล้วแจ้งลูกค้า (ลูกค้าเห็นแจ้งเตือนเด้งที่หน้าจอ)"""
        ok, msg = admin_set_prep_status(order_id, status, self.admin["name"])
        code = order_code(order_id)
        if ok:
            msg = {"queued": f"{code} ย้อนกลับไปรอคิวแล้ว",
                   "making": f"แจ้งลูกค้าแล้ว: {code} กำลังทำ",
                   "ready": f"เรียกลูกค้าแล้ว: {code} พร้อมรับ",
                   "picked_up": f"{code} ลูกค้ารับแล้ว"}[status]
        self._kitchen_flash = (msg, ok, undo if ok else None, time.time())
        self._kitchen_refresh()

    def _call_again(self, order_id):
        ok, msg = admin_call_customer(order_id, self.admin["name"])
        self._kitchen_flash = (msg, ok, None, time.time())
        self._kitchen_refresh()

    def _toggle_item(self, item_id, o):
        done = admin_toggle_item_done(item_id, self.admin["name"])
        if done and o["prep_status"] == "queued":
            self._kitchen_flash = (f"แจ้งลูกค้าแล้ว: {order_code(o['order_id'])} กำลังทำ", True, None, time.time())
        self._kitchen_refresh()

    # ---- การชำระเงิน: ตรวจสลิป + รายการรับชำระ ----
    def page_payments(self):
        s = admin_payment_summary()
        actions = self._header("การชำระเงิน", "ตรวจสลิปโอนเงินที่ลูกค้าแนบมาตอนจ่ายด้วย QR พร้อมเพย์ "
                                              "และดูรายการรับชำระทั้งหมด (อัปเดตอัตโนมัติ)")
        ad_button(actions, "รีเฟรช", lambda: self.go("payments"), "ghost").pack()
        if self._pay_flash:
            text, ok = self._pay_flash
            tk.Label(self.content, text=text, bg=AD_BG, fg=AD_OK if ok else AD_BAD,
                     font=(FONT, 11, "bold"), wraplength=900, justify="left").pack(anchor="w", pady=(0, 8))

        n_wait, wait_money = s["waiting"]
        cash = s["by_method"].get(dict(PAYMENT_METHODS)["cash"], (0, 0))
        qr = s["by_method"].get(dict(PAYMENT_METHODS)["qr"], (0, 0))
        cards = [("สลิปรอตรวจ", f"{n_wait} รายการ", f"รวม {baht(wait_money)}", AD_WARN if n_wait else AD_TEXT, AD_WARN),
                 ("รับชำระวันนี้", baht(s["total"]), f"{s['count']} บิล", AD_OK, AD_OK),
                 ("เงินสดวันนี้", baht(cash[1]), f"{cash[0]} บิล", AD_TEXT, AD_SIDE),
                 ("QR พร้อมเพย์วันนี้", baht(qr[1]), f"{qr[0]} บิล", AD_TEXT, "#5B7DB1")]
        grid = tk.Frame(self.content, bg=AD_BG)
        grid.pack(fill="x")
        for i, (label, value, sub, color, dot) in enumerate(cards):
            card = RoundFrame(grid, fill=AD_CARD, border=AD_LINE, radius=14, padx=18, pady=12)
            flow_add(grid, card, 200)
            head = tk.Frame(card.inner, bg=AD_CARD)
            head.pack(anchor="w")
            d = tk.Canvas(head, width=10, height=10, bg=AD_CARD, highlightthickness=0)
            aa_oval(d, 1, 1, 9, 9, fill=dot, outline="")
            d.pack(side="left", padx=(0, 6))
            tk.Label(head, text=label, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 11)).pack(side="left")
            tk.Label(card.inner, text=value, bg=AD_CARD, fg=color,
                     font=(FONT, 16, "bold")).pack(anchor="w", pady=(4, 0))
            tk.Label(card.inner, text=sub, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 10)).pack(anchor="w")

        lower = tk.Frame(self.content, bg=AD_BG)
        lower.pack(fill="both", expand=True, pady=(10, 0))
        refresh = lambda: self.go("payments")

        # ซ้าย: คิวสลิปรอตรวจ
        queue = RoundFrame(lower, fill=AD_CARD, border=AD_LINE, radius=14, padx=14, pady=12)
        queue.pack(side="left", fill="y", padx=(5, 6))
        qbox = queue.inner
        tk.Frame(qbox, bg=AD_CARD, width=360, height=1).pack()
        tk.Label(qbox, text=f"สลิปรอตรวจสอบ ({n_wait})", bg=AD_CARD, fg=AD_TEXT,
                 font=(FONT, 12, "bold")).pack(anchor="w")
        slips = admin_list_slips("waiting")
        if not slips:
            tk.Label(qbox, text="ยังไม่มีสลิปรอตรวจ\nลูกค้าที่จ่ายด้วย QR และแนบสลิปแล้วจะขึ้นที่นี่",
                     bg=AD_CARD, fg=AD_MUTED, font=(FONT, 11), justify="left").pack(anchor="w", pady=(10, 0))
        else:
            sf = ScrollFrame(qbox, AD_CARD)
            sf.pack(fill="both", expand=True, pady=(8, 0))
            for sl in slips:
                self._slip_item(sf.inner, sl, refresh)

        # ขวา: รายการรับชำระล่าสุด
        right = tk.Frame(lower, bg=AD_BG)
        right.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(right, text="รายการรับชำระล่าสุด  (ดับเบิลคลิกเพื่อดูรายละเอียด / สลิป)", bg=AD_BG,
                 fg=AD_TEXT, font=(FONT, 12, "bold")).pack(anchor="w", pady=(0, 6))
        pays = admin_list_payments()
        rows = [(p["order_id"], (fmt_datetime(p["paid_at"] or p["order_date"]), order_code(p["order_id"]),
                                 p["member_name"] or "ลูกค้าทั่วไป",
                                 PAY_TH.get(p["payment_method"], p["payment_method"] or "-"),
                                 fmt_price(p["paid"]), fmt_price(p["vat"] or 0),
                                 "มีสลิป" if p["slip_id"] else "-"))
                for p in pays]
        state = {}
        frame, tree = ad_make_table(right, [("ชำระเมื่อ", 135, "w"), ("ออเดอร์", 85, "w"),
                                            ("ลูกค้า", 170, "w"), ("วิธีชำระ", 110, "center"),
                                            ("ยอดรับ", 85, "e"), ("VAT", 70, "e"), ("สลิป", 70, "center")],
                                    rows, on_double=lambda: open_selected(), height=12)
        frame.pack(fill="both", expand=True)
        state["tree"] = tree

        def open_selected():
            sel = state["tree"].selection()
            if sel:
                open_order_detail(self, int(sel[0]), refresh)

    def _slip_item(self, parent, sl, on_change):
        """1 รายการในคิวสลิป: รูปย่อ + ออเดอร์/ลูกค้า/ยอด + ปุ่มตรวจสลิป"""
        row = tk.Frame(parent, bg=AD_CARD)
        row.pack(fill="x", pady=(0, 10))
        thumb = slip_photo(get_slip_image(sl["slip_id"]) or b"", 64, 100)
        th = tk.Canvas(row, width=66, height=102, bg=AD_CARD, highlightthickness=0, cursor="hand2")
        th.pack(side="left")
        rounded_rect(th, 0, 0, 66, 102, 8, fill="#EEF1F5", outline=AD_LINE)
        if thumb is not None:
            th.create_image(33, 51, image=thumb)
            th.photo = thumb
        open_it = lambda: open_slip_viewer(self, sl["slip_id"], on_change)
        th.bind("<Button-1>", lambda e: open_it())
        texts = tk.Frame(row, bg=AD_CARD)
        texts.pack(side="left", fill="x", expand=True, padx=(12, 0))
        tk.Label(texts, text=order_code(sl["order_id"]), bg=AD_CARD, fg=AD_TEXT,
                 font=(FONT, 12, "bold")).pack(anchor="w")
        tk.Label(texts, text=sl["member_name"] or "ลูกค้าทั่วไป", bg=AD_CARD, fg=AD_MUTED,
                 font=(FONT, 10)).pack(anchor="w")
        tk.Label(texts, text=f"ส่งเมื่อ {fmt_datetime(sl['submitted_at'])}", bg=AD_CARD, fg=AD_MUTED,
                 font=(FONT, 10)).pack(anchor="w")
        tk.Label(texts, text=baht(sl["amount"]), bg=AD_CARD, fg=AD_OK,
                 font=(FONT, 14, "bold")).pack(anchor="w")
        ad_button(texts, "ตรวจสลิป", open_it, "accent", height=32).pack(anchor="w", pady=(4, 0))

    # ---- ออเดอร์ ----
    def page_orders(self):
        actions = self._header("ออเดอร์", "ดับเบิลคลิกที่แถวเพื่อดูรายละเอียด")

        def cancel_all():
            n = len([o for o in admin_list_orders("pending") if o["slip_status"] != "waiting"])
            if not n:
                messagebox.showinfo("ไม่มีรายการ", "ไม่มีออเดอร์ค้างชำระ (ออเดอร์ที่ส่งสลิปแล้วไม่นับ)",
                                    parent=self)
            elif messagebox.askyesno("ยกเลิกออเดอร์ค้าง",
                                     f"ยกเลิกออเดอร์ที่รอชำระทั้งหมด {n} รายการ?", parent=self):
                admin_cancel_all_pending()
                self.go("orders")

        ad_button(actions, "ยกเลิกออเดอร์ที่ค้างทั้งหมด", cancel_all, "ghost").pack(side="left", padx=6)
        ad_button(actions, "รีเฟรช", lambda: self.go("orders"), "ghost").pack(side="left")

        bar = tk.Frame(self.content, bg=AD_BG)
        bar.pack(fill="x", pady=(0, 10))
        self.order_filter_var = tk.StringVar(value=self.order_filter or "all")
        chips = [("all", "ทั้งหมด"), ("pending", "รอชำระ"), ("paid", "ชำระแล้ว"),
                 ("cancelled", "ยกเลิก")]
        search_box = ad_entry(bar, width=260)
        search_box.pack(side="right")
        search = search_box.entry
        tk.Label(bar, text="ค้นหา:", bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(side="right", padx=6)
        holder = tk.Frame(self.content, bg=AD_BG)
        holder.pack(fill="both", expand=True)
        state = {"tree": None}

        def render(*_):
            for w in holder.winfo_children():
                w.destroy()
            st = self.order_filter_var.get()
            self.order_filter = None if st == "all" else st
            q = search.get().strip().lower()
            rows = []
            for o in admin_list_orders(None if st == "all" else st):
                code = order_code(o["order_id"])
                who = o["member_name"] or "ลูกค้าทั่วไป"
                if q and q not in (code + who + (o["member_phone"] or "")).lower():
                    continue
                amount = (order_amounts(o)["paid"] if o["status"] == "paid"      # จ่ายจริง (รวมภาษี)
                          else vat_split(o["total_price"] - o["discount"])[1])  # ยอดที่ต้องจ่าย
                rows.append((o["order_id"], (code, fmt_datetime(o["order_date"]), who,
                                             fmt_price(amount),
                                             PAY_TH.get(o["payment_method"], o["payment_method"] or "-"),
                                             order_status_text(o))))
            frame, tree = ad_make_table(
                holder, [("รหัส", 90, "w"), ("วันที่สั่ง", 150, "w"), ("สมาชิก", 200, "w"),
                         ("ยอดชำระ", 90, "e"), ("ชำระด้วย", 90, "center"),
                         ("สถานะ", 90, "center")], rows, on_double=open_selected, height=14)
            frame.pack(fill="both", expand=True)
            state["tree"] = tree
            tk.Label(holder, text=f"ทั้งหมด {len(rows)} รายการ", bg=AD_BG, fg=AD_MUTED,
                     font=(FONT, 11)).pack(anchor="w", pady=(6, 0))

        def open_selected():
            sel = state["tree"].selection() if state["tree"] else ()
            if sel:
                open_order_detail(self, int(sel[0]), lambda: self.go("orders"))

        chip_buttons = {}

        def pick(key):
            self.order_filter_var.set(key)
            for k, b in chip_buttons.items():
                b.btn_colors = ((AD_SIDE, "white", AD_SIDE, "") if k == key
                                else AD_BUTTONS["ghost"])
                b._paint()
            render()

        for key, label in chips:
            b = PillButton(bar, label, lambda k=key: pick(k), height=36, size=10, padx=16,
                           colors=((AD_SIDE, "white", AD_SIDE, "")
                                   if key == self.order_filter_var.get() else AD_BUTTONS["ghost"]))
            b.pack(side="left", padx=(0, 6))
            chip_buttons[key] = b
        search.bind("<KeyRelease>", render)
        render()

    # ---- เมนูและสต็อก: การ์ดทุกเมนู (รูปเดียวกับหน้าลูกค้า) + สต็อก + เติมสต็อก ----
    PRODUCT_FILTERS = [("all", "ทั้งหมด"), ("low", "ใกล้หมด"), ("out", "หมดแล้ว"), ("off", "ปิดขาย")]
    CARD_W = 236                  # ความกว้างการ์ดเมนูโดยประมาณ (จำนวนคอลัมน์ปรับตามความกว้างหน้าต่าง)

    def page_products(self):
        """เมนูและสต็อก: การ์ดเมนูแบ่งตามหมวด (รูป ชื่อ ราคา คงเหลือ ขายวันนี้/ทั้งหมด)
        กดรูป = เปลี่ยนรูปเมนู / "+ เติมสต็อก" / "แก้ไข" (ชื่อ ราคา หมวด รูป) / ปิด-เปิดขาย / ลบเมนู
        กรองได้: ทั้งหมด / ใกล้หมด / หมดแล้ว / ปิดขาย และค้นหาชื่อเมนู"""
        products = admin_list_products()
        actions = self._header("เมนูและสต็อก",
                               f"รูปเมนูตรงกับหน้าลูกค้า กดที่รูปเพื่อเปลี่ยน  •  สต็อกลดเองเมื่อลูกค้าชำระเงิน  •  "
                               f"ใกล้หมด = เหลือไม่เกิน {LOW_STOCK_LEVEL} แก้ว")
        ad_button(actions, "+ เพิ่มเมนู", lambda: open_product_dialog(self, None, self._products_done),
                  "accent").pack(side="left", padx=(0, 6))
        ad_button(actions, "+ หมวดหมู่", self._add_category, "ghost").pack(side="left", padx=(0, 6))
        ad_button(actions, "รีเฟรช", lambda: self.go("products"), "ghost").pack(side="left")

        grid = tk.Frame(self.content, bg=AD_BG)
        grid.pack(fill="x", pady=(0, 10))
        self._product_stats = []
        for i, label in enumerate(("เมนูที่เปิดขาย", "ใกล้หมด", "หมดแล้ว", "ขายวันนี้")):
            card = RoundFrame(grid, fill=AD_CARD, border=AD_LINE, radius=14, padx=16, pady=10)
            flow_add(grid, card, 200)
            tk.Label(card.inner, text=label, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w")
            value = tk.Label(card.inner, text="", bg=AD_CARD, font=(FONT, 16, "bold"))
            value.pack(anchor="w")
            self._product_stats.append(value)
        self._update_product_stats(products)

        bar = tk.Frame(self.content, bg=AD_BG)
        bar.pack(fill="x", pady=(0, 6))

        def pick(key):
            """เปลี่ยนตัวกรอง: เปลี่ยนสีปุ่มเดิม แล้วซ่อน/แสดงการ์ด (ไม่วาดหน้าใหม่)"""
            self.stock_filter = key
            for (k, _), b in zip(self.PRODUCT_FILTERS, chips.winfo_children()):
                b.btn_colors = (AD_SIDE, "white", AD_SIDE, "") if k == key else AD_BUTTONS["ghost"]
                b._paint()
            self._apply_product_filter(top=True)

        chips = self._chip_row(bar, self.PRODUCT_FILTERS, self.stock_filter, pick)
        chips.pack(side="left")
        search_box = ad_entry(bar, width=240)
        search_box.pack(side="right")
        search = search_box.entry
        search.insert(0, self.product_search)
        tk.Label(bar, text="ค้นหาเมนู:", bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(side="right", padx=(0, 6))
        info = tk.Frame(self.content, bg=AD_BG)
        info.pack(fill="x", pady=(0, 4))
        tk.Label(info, text=f"แต่ละเมนูลูกค้าสั่งได้ไม่เกิน {MAX_CUPS_PER_MENU} แก้วต่อออเดอร์  •  "
                            "\"ปิดขาย\" = ซ่อนเมนูจากลูกค้าชั่วคราว แม้ยังมีสต็อก",
                 bg=AD_BG, fg=AD_MUTED, font=(FONT, 10), anchor="w").pack(side="left")
        # ข้อความแจ้งผล (บันทึกสต็อก / ปิดขาย / เปลี่ยนรูป) อยู่บรรทัดเดิมเสมอ เนื้อหาด้านล่างจึงไม่ขยับ
        self._products_flash_label = tk.Label(info, text="", bg=AD_BG, font=(FONT, 10, "bold"), anchor="e")
        self._products_flash_label.pack(side="right")
        flash = self._products_flash
        if flash and time.time() - flash[2] < 8:
            self._show_products_flash(flash[0], flash[1], keep=False)

        sf = ScrollFrame(self.content, AD_BG)
        sf.pack(fill="both", expand=True)
        self._products_sf = sf
        holder = tk.Frame(sf.inner, bg=AD_BG)
        holder.pack(fill="x")

        self._products_holder = holder

        # สร้างการ์ดทุกเมนูครั้งเดียว (แบ่งตามหมวด) ตัวกรอง/ค้นหาแค่ซ่อนหรือแสดงการ์ด จึงลื่นไม่ต้องรอวาดใหม่
        self._product_sections, self._product_cols, self._product_cards = [], 0, {}
        cats = []
        for p in products:
            if not cats or cats[-1][0] != p["category_id"]:
                cats.append((p["category_id"], p["category"], []))
            cats[-1][2].append(p)
        for _, cat, items in cats:
            g = tk.Frame(holder, bg=AD_BG)
            g.head = tk.Label(holder, text=cat, bg=AD_BG, fg=AD_TEXT, font=(FONT, 13, "bold"))
            g.cat = cat
            section = (g, [])
            for p in items:
                card = self._product_card(g, p)
                card.product, card.section, card.visible = p, section, False
                section[1].append(card)
                self._product_cards[p["product_id"]] = card
            self._product_sections.append(section)
        self._products_empty = tk.Label(holder, text="", bg=AD_BG, fg=AD_MUTED, font=(FONT, 12))
        self._products_search = search

        search.bind("<KeyRelease>", lambda e: self._apply_product_filter(top=True))
        sf.canvas.bind("<Configure>", lambda e: self._layout_product_cards(), add="+")
        self._apply_product_filter()
        self._layout_product_cards()

    def _layout_product_cards(self):
        """จัดการ์ดเป็นตาราง จำนวนคอลัมน์ตามความกว้างหน้าจอ (ทำใหม่เฉพาะตอนจำนวนคอลัมน์เปลี่ยน)"""
        sf = getattr(self, "_products_sf", None)
        if sf is None or not sf.winfo_exists():
            return
        width = sf.canvas.winfo_width()
        cols = max(1, (width - 4) // (self.CARD_W + 12)) if width > 50 else 4
        if cols == self._product_cols:
            return
        self._product_cols = cols
        for g, cards in self._product_sections:
            for i in range(12):
                g.grid_columnconfigure(i, weight=1 if i < cols else 0, uniform="pcard" if i < cols else "")
            self._regrid_product_section(g, cards)

    def _product_card(self, parent, p):
        """การ์ดเมนู 1 ใบ: รูป (กดเพื่อเปลี่ยน) + ป้ายสถานะ / ชื่อ ราคา หมวด / คงเหลือ ขายแล้ว / ปุ่ม"""
        st = p["status"] if p["is_available"] else "off"
        border = {"out": AD_BAD, "low": AD_WARN}.get(st, AD_LINE)
        card = RoundFrame(parent, fill=AD_CARD, border=border, radius=14, padx=10, pady=10,
                          border_width=2 if st in ("out", "low") else 1)
        c = card.inner
        pic = tk.Canvas(c, height=176, bg=AD_CARD, highlightthickness=0, cursor="hand2")
        pic.pack(fill="x")
        pic.bind("<Configure>", lambda e: draw_menu_pic(pic, p, st))
        pic.bind("<Button-1>", lambda e: self._change_image(p))

        top = tk.Frame(c, bg=AD_CARD)
        top.pack(fill="x", pady=(8, 0))
        tk.Label(top, text=baht(p["price"]), bg=AD_CARD, fg=AD_TEXT, font=(FONT, 12, "bold")).pack(side="right")
        tk.Label(top, text=p["name"], bg=AD_CARD, fg=AD_MUTED if st == "off" else AD_TEXT, font=(FONT, 12, "bold"),
                 anchor="w", justify="left", wraplength=self.CARD_W - 90).pack(side="left", fill="x")
        stock = tk.Frame(c, bg=AD_CARD)
        stock.pack(fill="x", pady=(4, 0))
        tk.Label(stock, text=f"{p['stock']:,}", bg=AD_CARD, font=(FONT, 18, "bold"),
                 fg=STOCK_COLOR[p["status"]] if st != "off" else AD_MUTED).pack(side="left")
        tk.Label(stock, text="แก้วคงเหลือ", bg=AD_CARD, fg=AD_MUTED, font=(FONT, 10)).pack(side="left",
                                                                                         padx=(4, 0), pady=(6, 0))
        tk.Label(c, text=f"ขายวันนี้ {p['sold_today']:,}  •  ขายแล้วทั้งหมด {p['sold']:,} แก้ว", bg=AD_CARD,
                 fg=AD_MUTED, font=(FONT, 9), anchor="w").pack(fill="x")
        btns = tk.Frame(c, bg=AD_CARD)
        btns.pack(fill="x", pady=(8, 0))
        ad_button(btns, "+ เติมสต็อก", lambda: open_stock_dialog(self, p, lambda: self._stock_done(p)), "accent",
                  height=32).pack(side="left", fill="x", expand=True)
        ad_button(btns, "แก้ไข", lambda: open_product_dialog(
            self, p, lambda: self._update_product_card(p["product_id"], (f"บันทึกเมนู {p['name']} แล้ว", True))),
            "ghost", height=32).pack(side="left", padx=(6, 0))
        foot = tk.Frame(c, bg=AD_CARD)
        foot.pack(fill="x", pady=(6, 0))
        LinkButton(foot, "ปิดการขายชั่วคราว" if p["is_available"] else "เปิดขายอีกครั้ง",
                   lambda: self._toggle_available(p), fg=AD_MUTED if p["is_available"] else AD_OK,
                   hover=AD_BAD if p["is_available"] else AD_TEXT,
                   size=9).pack(side="left")
        LinkButton(foot, "ลบเมนู", lambda: open_delete_product_dialog(self, p, self._product_deleted),
                   fg=AD_MUTED, hover=AD_BAD, size=9).pack(side="right")
        return card

    def _show_stock(self, key):
        """ไปหน้าเมนูและสต็อกพร้อมกรองเฉพาะเมนูที่ใกล้หมด/หมดแล้ว"""
        self.stock_filter, self.product_search = key, ""
        self.go("products")

    def _products_refresh(self, flash=None):
        """วาดหน้าเมนูใหม่ เลื่อนอยู่ตำแหน่งเดิม (+ ข้อความแจ้งผลด้านบน)"""
        if flash:
            self._products_flash = (flash[0], flash[1], time.time())
        sf = getattr(self, "_products_sf", None)
        pos = sf.canvas.yview()[0] if sf is not None and sf.winfo_exists() else 0
        self.go("products")
        sf = self._products_sf
        sf.update_idletasks()
        sf.canvas.yview_moveto(pos)

    def _products_done(self):
        self._products_refresh(("บันทึกเมนูเรียบร้อย", True))

    def _stock_done(self, p):
        fresh = next((x for x in admin_list_products() if x["product_id"] == p["product_id"]), None)
        left = f" เหลือ {fresh['stock']:,} แก้ว" if fresh else ""
        self._update_product_card(p["product_id"], (f"บันทึกสต็อก {p['name']} แล้ว{left}", True))

    def _product_deleted(self, text):
        """ลบเมนูแล้ว: วาดหน้าเมนูใหม่ (การ์ดนั้นหายไป) พร้อมข้อความแจ้งผล"""
        self._products_refresh((text, True) if text else None)

    def _toggle_available(self, p):
        admin_set_available(p["product_id"], not p["is_available"])
        self._update_product_card(p["product_id"], (f"{'ปิด' if p['is_available'] else 'เปิด'}ขาย {p['name']} แล้ว",
                                                    True))

    # ---- อัปเดตทีละการ์ด (ไม่วาดทั้งหน้าใหม่ จึงไม่กระตุก และหน้าไม่เลื่อน) ----
    def _product_matches(self, p):
        """เมนูนี้ตรงกับตัวกรอง (ทั้งหมด / ใกล้หมด / หมดแล้ว / ปิดขาย) และคำค้นที่เลือกอยู่ไหม"""
        want, q = self.stock_filter, self.product_search.lower()
        return ((want == "all" or (want == "off" and not p["is_available"])
                 or (p["is_available"] and p["status"] == want))
                and (not q or q in p["name"].lower() or q in p["category"].lower()))

    def _update_product_stats(self, products):
        """ตัวเลขสรุป 4 ช่องด้านบน: เปิดขาย / ใกล้หมด / หมดแล้ว / ขายวันนี้"""
        selling = [p for p in products if p["is_available"]]
        low = sum(1 for p in selling if p["status"] == "low")
        out = sum(1 for p in selling if p["status"] == "out")
        values = [(f"{len(selling)} / {len(products)} เมนู", AD_TEXT),
                  (f"{low} เมนู", AD_WARN if low else AD_TEXT),
                  (f"{out} เมนู", AD_BAD if out else AD_TEXT),
                  (f"{sum(p['sold_today'] for p in products):,} แก้ว", AD_OK)]
        for label, (text, color) in zip(self._product_stats, values):
            label.config(text=text, fg=color)

    def _show_products_flash(self, text, ok, keep=True):
        """ข้อความแจ้งผลมุมขวา (หายเองใน 8 วินาที)"""
        label = getattr(self, "_products_flash_label", None)
        if label is None or not label.winfo_exists():
            return
        if keep:
            self._products_flash = (text, ok, time.time())
        label.config(text=text, fg=AD_OK if ok else AD_BAD)
        job = getattr(label, "clear_job", None)
        if job:
            label.after_cancel(job)
        label.clear_job = label.after(8000, lambda: label.winfo_exists() and label.config(text=""))

    def _update_product_card(self, product_id, flash=None):
        """เปลี่ยนเฉพาะการ์ดของเมนูนี้ + ตัวเลขสรุป + ตัวเลขที่เมนูซ้าย (ไม่วาดทั้งหน้าใหม่ จึงไม่กระตุก)
        การ์ดใหม่วาดทับที่เดิมเสร็จก่อนแล้วค่อยเอาใบเก่าออก จึงไม่กะพริบ  ถ้าเมนูไม่ตรงตัวกรองแล้ว
        (เช่น ดู "ปิดขาย" อยู่แล้วกดเปิดขาย) การ์ดจะถูกซ่อน ใบอื่นเลื่อนมาแทน  ย้ายหมวด = วาดทั้งหน้าใหม่"""
        old = getattr(self, "_product_cards", {}).get(product_id)
        products = admin_list_products()
        fresh = next((p for p in products if p["product_id"] == product_id), None)
        if (self.current_page != "products" or old is None or not old.winfo_exists() or fresh is None
                or fresh["category_id"] != old.product["category_id"]):
            self._products_refresh(flash)
            return
        g, cards = old.section
        new = self._product_card(g, fresh)
        new.product, new.section = fresh, old.section
        new.visible = self._product_matches(fresh)
        cards[cards.index(old)] = new
        self._product_cards[product_id] = new
        if new.visible and old.visible:                 # อยู่ช่องเดิม: วาดทับให้เสร็จก่อน แล้วค่อยเอาใบเก่าออก
            info = old.grid_info()
            new.grid(row=info["row"], column=info["column"], sticky="nsew", padx=6, pady=6)
            self.after(60, lambda: old.winfo_exists() and old.destroy())
        else:                                           # ตรง/ไม่ตรงตัวกรองเปลี่ยนไป: จัดการ์ดในหน้าใหม่
            old.destroy()
            self._apply_product_filter()
        self._update_product_stats(products)
        self._refresh_stock_badge()
        if flash:
            self._show_products_flash(*flash)

    def _regrid_product_section(self, g, cards):
        """วางการ์ดที่แสดงอยู่เรียงเป็นตาราง (การ์ดที่ถูกกรองออกซ่อนไว้ ไม่ทำลาย)"""
        cols = max(1, self._product_cols)
        k = 0
        for card in cards:
            if card.visible:
                card.grid(row=k // cols, column=k % cols, sticky="nsew", padx=6, pady=6)
                k += 1
            else:
                card.grid_remove()

    def _apply_product_filter(self, top=False):
        """แสดงเฉพาะการ์ดที่ตรงกับตัวกรอง/คำค้น (ซ่อนหมวดที่ไม่เหลือการ์ด)  top = เลื่อนกลับขึ้นบนสุด"""
        search = getattr(self, "_products_search", None)
        if search is not None and search.winfo_exists():
            self.product_search = search.get().strip()
        any_shown = False
        for g, cards in self._product_sections:
            g.head.pack_forget()
            g.pack_forget()
        self._products_empty.pack_forget()
        for g, cards in self._product_sections:
            for c in cards:
                c.visible = self._product_matches(c.product)
            shown = sum(c.visible for c in cards)
            if shown:
                any_shown = True
                g.head.config(text=f"{g.cat}  ({shown})")
                g.head.pack(anchor="w", pady=(10, 2), padx=6)
                g.pack(fill="x")
            self._regrid_product_section(g, cards)
        if not any_shown:
            q = self.product_search
            self._products_empty.config(text=f"ไม่พบเมนูที่ตรงกับ \"{q}\"" if q else "ไม่มีเมนูในกลุ่มนี้")
            self._products_empty.pack(anchor="w", pady=20)
        if top:
            self._products_sf.canvas.yview_moveto(0)

    def _change_image(self, p):
        """กดที่รูปบนการ์ด: เลือกรูปใหม่แล้วบันทึกทันที (รูปเดิมเก็บไว้ที่ images/old_menu_images)"""
        png = pick_menu_image(self, f"เลือกรูปเมนู {p['name']}")
        if png is None:
            return
        ok, result = admin_save_product_image(p["product_id"], png)
        self._update_product_card(p["product_id"], (f"เปลี่ยนรูป {p['name']} แล้ว (รูปเดิมเก็บไว้ที่ images/"
                                                    f"{MENU_IMAGE_OLD_DIR})" if ok else result, ok))

    def _add_category(self):
        win = ad_dialog(self, "เพิ่มหมวดหมู่", 380, 230)
        b = tk.Frame(win, bg=AD_BG, padx=24, pady=18)
        b.pack(fill="both", expand=True)
        e = ad_field(b, "ชื่อหมวดหมู่ใหม่")
        m = tk.Label(b, text="", bg=AD_BG, fg=AD_BAD, font=(FONT, 11))
        m.pack(anchor="w", pady=(6, 0))

        def ok():
            good, text = admin_add_category(e.get())
            if good:
                win.destroy()
                self._products_refresh((f"เพิ่มหมวดหมู่ {e.get().strip()} แล้ว", True))
            else:
                m.config(text=text)

        ad_button(b, "เพิ่ม", ok, "accent").pack(anchor="w", pady=(6, 0))
        e.focus()

    # ---- สมาชิก ----
    def page_members(self):
        actions = self._header("สมาชิก", "ดับเบิลคลิกที่แถวเพื่อดูรายละเอียด ปรับแต้ม แบน หรือลบบัญชีสมาชิก")
        ad_button(actions, "รีเฟรช", lambda: self.go("members"), "ghost").pack()
        if self._members_flash:
            text, ok = self._members_flash
            self._members_flash = None
            tk.Label(self.content, text=text, bg=AD_BG, fg=AD_OK if ok else AD_BAD,
                     font=(FONT, 11, "bold")).pack(anchor="w", pady=(0, 8))
        bar = tk.Frame(self.content, bg=AD_BG)
        bar.pack(fill="x", pady=(0, 10))

        def pick(key):
            self.member_filter = key
            self.go("members")

        self._chip_row(bar, [("all", "ทั้งหมด"), ("active", "ใช้งานได้"), ("banned", "ถูกแบน")],
                       self.member_filter, pick).pack(side="right")
        tk.Label(bar, text="ค้นหา (ชื่อ / เบอร์ / อีเมล):", bg=AD_BG, fg=AD_MUTED,
                 font=(FONT, 11)).pack(side="left", padx=(0, 6))
        search_box = ad_entry(bar, width=280)
        search_box.pack(side="left")
        search = search_box.entry
        tier_bar(self.content).pack(fill="x", pady=(0, 10))      # เกณฑ์การเลื่อนระดับ
        holder = tk.Frame(self.content, bg=AD_BG)
        holder.pack(fill="both", expand=True)
        members = admin_list_members()
        state = {"tree": None}

        def render(*_):
            for w in holder.winfo_children():
                w.destroy()
            q = search.get().strip().lower()
            want = {"all": None, "active": False, "banned": True}[self.member_filter]
            shown = [m for m in members
                     if (want is None or bool(m["banned"]) == want)
                     and (not q or q in f"{m['name']} {m['phone']} {m['email'] or ''}".lower())]
            rows = [(m["member_id"], (m["name"], m["phone"], m["email"] or "-", tier_for(m["lifetime"]),
                                      f"{m['lifetime']:,}", f"{m['points']:,}", m["orders"], fmt_price(m["spent"]),
                                      "ถูกแบน" if m["banned"] else "ใช้งานได้"))
                    for m in shown]
            frame, tree = ad_make_table(
                holder, [("ชื่อ", 160, "w"), ("เบอร์โทร", 100, "w"), ("อีเมล", 180, "w"),
                         ("ระดับ", 75, "center"), ("แต้มสะสมรวม", 100, "e"), ("แต้มคงเหลือ", 90, "e"),
                         ("ออเดอร์", 65, "e"), ("ยอดซื้อรวม", 95, "e"), ("สถานะ", 80, "center")], rows,
                on_double=open_selected, height=14)
            tree.tag_configure("banned", foreground=AD_BAD)
            for m in shown:
                if m["banned"]:
                    tree.item(str(m["member_id"]), tags=("banned",))     # แถวสมาชิกที่ถูกแบนเป็นสีแดง
            frame.pack(fill="both", expand=True)
            state["tree"] = tree
            n_banned = sum(1 for m in members if m["banned"])
            tk.Label(holder, text=f"แสดง {len(rows)} คน  •  สมาชิกทั้งหมด {len(members)} คน  •  ถูกแบน {n_banned} คน",
                     bg=AD_BG, fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w", pady=(6, 0))

        def open_selected():
            sel = state["tree"].selection() if state["tree"] else ()
            if sel:
                m = next((x for x in members if x["member_id"] == int(sel[0])), None)
                if m:
                    open_member_dialog(self, m, lambda: self.go("members"))

        search.bind("<KeyRelease>", render)
        render()

    # ---- บัญชีแอดมิน ----
    # ---- ปุ่มเลือกแบบชิป (ใช้ในหน้ารายงาน) ----
    def _chip_row(self, parent, items, current, on_pick):
        row = tk.Frame(parent, bg=bg_of(parent))
        for key, label in items:
            colors = (AD_SIDE, "white", AD_SIDE, "") if key == current else AD_BUTTONS["ghost"]
            PillButton(row, label, lambda k=key: on_pick(k), height=34, size=10, padx=14,
                       radius=10, colors=colors).pack(side="left", padx=(0, 6))
        return row

    # ---- รายงานยอดขาย ----
    @staticmethod
    def _preset_range(key):
        """ช่วงวันที่ของปุ่มลัด คืนค่า (วันเริ่ม, วันสิ้นสุด)"""
        t = thai_today()
        if key == "today":
            return t, t
        if key == "7d":
            return t - timedelta(days=6), t
        if key == "month":
            return t.replace(day=1), t
        if key == "last_month":
            end = t.replace(day=1) - timedelta(days=1)
            return end.replace(day=1), end
        if key == "year":
            return t.replace(month=1, day=1), t
        return min(date.fromisoformat(first_sale_date()), t), t

    def page_report(self):
        st = self.report_state
        if st["preset"] != "custom":
            st["from"], st["to"] = self._preset_range(st["preset"])
        r = admin_sales_report(st["from"].isoformat(), st["to"].isoformat(), st["group"])
        self._report = r
        s = r["summary"]
        actions = self._header("รายงานยอดขาย", f"{fmt_period(r['from'])} - {fmt_period(r['to'])}"
                                                "  •  นับเฉพาะออเดอร์ที่ชำระเงินแล้ว"
                                                f"  •  ข้อมูล ณ {thai_now():%H:%M:%S}")
        ad_button(actions, "ส่งออก Excel", self._export_report, "accent").pack(side="left", padx=(0, 6))
        # รีเฟรช: ดึงยอดขายล่าสุด (ช่วงวันที่ / รายวัน-รายเดือน / แท็บที่เลือกอยู่ยังเหมือนเดิม)
        ad_button(actions, "รีเฟรช", lambda: self.go("report"), "ghost").pack(side="left")

        def pick_preset(k):
            st["preset"] = k
            self.go("report")

        def pick_group(k):
            st["group"] = k
            self.go("report")

        bar = tk.Frame(self.content, bg=AD_BG)
        bar.pack(fill="x", pady=(0, 8))
        self._chip_row(bar, self.REPORT_PRESETS, st["preset"], pick_preset).pack(side="left")
        self._chip_row(bar, [("day", "รายวัน"), ("month", "รายเดือน")], st["group"],
                       pick_group).pack(side="right")

        bar2 = tk.Frame(self.content, bg=AD_BG)
        bar2.pack(fill="x", pady=(0, 10))
        tk.Label(bar2, text="กำหนดช่วงเอง  ตั้งแต่", bg=AD_BG, fg=AD_TEXT,
                 font=(FONT, 11)).pack(side="left")
        box = ad_entry(bar2, width=130)
        box.pack(side="left", padx=6)
        self.report_from = box.entry
        tk.Label(bar2, text="ถึง", bg=AD_BG, fg=AD_TEXT, font=(FONT, 11)).pack(side="left")
        box = ad_entry(bar2, width=130)
        box.pack(side="left", padx=6)
        self.report_to = box.entry
        self.report_from.insert(0, st["from"].strftime("%d/%m/%Y"))
        self.report_to.insert(0, st["to"].strftime("%d/%m/%Y"))
        for e in (self.report_from, self.report_to):
            e.bind("<Return>", lambda ev: self._apply_custom_range())
        ad_button(bar2, "แสดง", self._apply_custom_range, "primary", height=36).pack(
            side="left", padx=(4, 10))
        self.report_msg = tk.Label(bar2, text="วัน/เดือน/ปี เช่น 01/10/2026 (ใช้ปี พ.ศ. ได้)",
                                   bg=AD_BG, fg=AD_MUTED, font=(FONT, 10))
        self.report_msg.pack(side="left")

        # การ์ดสรุป
        cards = [("ยอดขายสุทธิ", baht(s["net"]), AD_OK), ("จำนวนออเดอร์", f"{s['orders']:,}", AD_TEXT),
                 ("แก้วที่ขายได้", f"{s['cups']:,} แก้ว", AD_TEXT),
                 ("ส่วนลดรวม", baht(s["discount"]), AD_WARN if s["discount"] else AD_TEXT),
                 (f"VAT {VAT_RATE:g}%", baht(s["vat"]), AD_TEXT),
                 ("เฉลี่ยต่อออเดอร์", baht(s["avg"]), AD_TEXT)]
        grid = tk.Frame(self.content, bg=AD_BG)
        grid.pack(fill="x")
        for i, (label, value, color) in enumerate(cards):
            card = RoundFrame(grid, fill=AD_CARD, border=AD_LINE, radius=14, padx=16, pady=12)
            flow_add(grid, card, 170)
            tk.Label(card.inner, text=label, bg=AD_CARD, fg=AD_MUTED, font=(FONT, 11)).pack(anchor="w")
            tk.Label(card.inner, text=value, bg=AD_CARD, fg=color,
                     font=(FONT, 15, "bold")).pack(anchor="w", pady=(4, 0))

        lower = tk.Frame(self.content, bg=AD_BG)
        lower.pack(fill="both", expand=True, pady=(12, 0))
        left = tk.Frame(lower, bg=AD_BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        unit = "วันที่" if st["group"] == "day" else "เดือน"
        tk.Label(left, text="ยอดขายรายวัน (ล่าสุดอยู่บน)" if st["group"] == "day"
                 else "ยอดขายรายเดือน (ล่าสุดอยู่บน)", bg=AD_BG, fg=AD_TEXT,
                 font=(FONT, 12, "bold")).pack(anchor="w", pady=(0, 6))
        rows = [(i, (fmt_period(k), f"{o:,}", f"{c:,}", fmt_price(g), fmt_price(d), fmt_price(nv),
                     fmt_price(round(v, 2))))
                for i, (k, o, c, g, d, nv, v, _) in enumerate(reversed(r["periods"]))]
        frame, _ = ad_make_table(left, [(unit, 100, "w"), ("ออเดอร์", 64, "e"), ("แก้ว", 54, "e"),
                                        ("ก่อนส่วนลด", 90, "e"), ("ส่วนลด", 70, "e"),
                                        ("ยอดสุทธิ", 90, "e"), (f"VAT {VAT_RATE:g}%", 80, "e")],
                                 rows, height=9)
        frame.pack(fill="both", expand=True)
        self.report_side = tk.Frame(lower, bg=AD_BG)
        self.report_side.pack(side="left", fill="both")
        self._render_report_side()

    def _set_report_tab(self, key):
        self.report_state["tab"] = key
        self._render_report_side()

    def _render_report_side(self):
        """ตารางด้านขวาของหน้ารายงาน: เมนูขายดี / วิธีชำระเงิน / ช่วงเวลาขายดี"""
        side = self.report_side
        for w in side.winfo_children():
            w.destroy()
        r, tab = self._report, self.report_state["tab"]
        self._chip_row(side, self.REPORT_TABS, tab, self._set_report_tab).pack(anchor="w", pady=(0, 6))
        if tab == "products":
            cols = [("#", 40, "center"), ("เมนู", 170, "w"), ("แก้ว", 60, "e"), ("ยอดขาย", 90, "e")]
            rows = [(i, (i, name, f"{q:,}", fmt_price(m))) for i, (name, q, m) in enumerate(r["products"], 1)]
        elif tab == "payments":
            total = r["summary"]["net"] or 1
            cols = [("วิธีชำระ", 140, "w"), ("ออเดอร์", 70, "e"), ("ยอดสุทธิ", 90, "e"), ("สัดส่วน", 72, "e")]
            rows = [(i, (m, f"{o:,}", fmt_price(v), f"{v * 100 / total:.0f}%"))
                    for i, (m, o, v) in enumerate(r["payments"])]
        else:
            cols = [("ช่วงเวลา", 140, "w"), ("ออเดอร์", 80, "e"), ("ยอดสุทธิ", 100, "e")]
            rows = [(i, (f"{h}:00 - {h}:59", f"{o:,}", fmt_price(v))) for i, (h, o, v) in enumerate(r["hours"])]
        frame, _ = ad_make_table(side, cols, rows, height=9)
        frame.pack(fill="both", expand=True)
        if not rows:
            tk.Label(side, text="ยังไม่มียอดขายในช่วงนี้", bg=AD_BG, fg=AD_MUTED,
                     font=(FONT, 11)).pack(anchor="w", pady=(6, 0))

    def _apply_custom_range(self):
        d0, d1 = parse_date(self.report_from.get()), parse_date(self.report_to.get())
        if d0 is None or d1 is None:
            self.report_msg.config(text="วันที่ไม่ถูกต้อง กรุณากรอกแบบ วัน/เดือน/ปี เช่น 01/10/2026",
                                   fg=AD_BAD)
            return
        if d0 > d1:
            self.report_msg.config(text="วันเริ่มต้นต้องไม่อยู่หลังวันสิ้นสุด", fg=AD_BAD)
            return
        self.report_state.update(preset="custom", **{"from": d0, "to": d1})
        self.go("report")

    def _export_report(self):
        """บันทึกรายงานที่แสดงอยู่เป็นไฟล์ Excel (.xlsx)"""
        r = self._report
        os.makedirs(REPORT_DIR, exist_ok=True)
        path = filedialog.asksaveasfilename(
            parent=self, title="บันทึกรายงานยอดขาย", initialdir=REPORT_DIR,
            initialfile=f"sales_{r['from']}_to_{r['to']}.xlsx", defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")])
        if not path:
            return
        try:
            export_report_xlsx(r, path)
        except PermissionError:
            messagebox.showerror("บันทึกไม่ได้", "ไฟล์นี้เปิดอยู่ในโปรแกรมอื่น (เช่น Excel)\n"
                                                 "กรุณาปิดไฟล์ก่อน แล้วลองอีกครั้ง", parent=self)
            return
        except OSError as e:
            messagebox.showerror("บันทึกไม่ได้", f"บันทึกไฟล์ไม่สำเร็จ: {e}", parent=self)
            return
        if hasattr(os, "startfile"):
            if messagebox.askyesno("ส่งออกเรียบร้อย", f"บันทึกรายงานที่\n{path}\n\nเปิดไฟล์เลยไหม?",
                                   parent=self):
                try:
                    os.startfile(path)
                except OSError:
                    pass
        else:
            messagebox.showinfo("ส่งออกเรียบร้อย", f"บันทึกรายงานที่\n{path}", parent=self)

    def page_account(self):
        self._header("บัญชีแอดมิน", f"คุณเข้าสู่ระบบเป็น {self.admin['name']}  (ชื่อผู้ใช้: {self.admin['username']})")
        if self._account_flash:
            text, ok = self._account_flash
            self._account_flash = None
            tk.Label(self.content, text=text, bg=AD_BG, fg=AD_OK if ok else AD_BAD,
                     font=(FONT, 11, "bold")).pack(anchor="w", pady=(0, 8))
        self._admin_list()
        row = tk.Frame(self.content, bg=AD_BG)
        row.pack(fill="x", anchor="n", pady=(14, 0))

        def card(title_text):
            rf = RoundFrame(row, fill=AD_CARD, border=AD_LINE, radius=14, padx=22, pady=18)
            rf.pack(side="left", fill="y", padx=(0, 14), anchor="n")
            c = rf.inner
            tk.Label(c, text=title_text, bg=AD_CARD, fg=AD_TEXT,
                     font=(FONT, 12, "bold")).pack(anchor="w")
            tk.Frame(c, bg=AD_CARD, width=320, height=1).pack()
            return c

        c1 = card("เปลี่ยนรหัสผ่าน")
        old = ad_field(c1, "รหัสผ่านปัจจุบัน", show="•", bg=AD_CARD)
        new = ad_field(c1, f"รหัสผ่านใหม่ ({PASSWORD_HINT})", show="•", bg=AD_CARD)
        new2 = ad_field(c1, "ยืนยันรหัสผ่านใหม่", show="•", bg=AD_CARD)
        m1 = tk.Label(c1, text="", bg=AD_CARD, fg=AD_BAD, font=(FONT, 11), wraplength=320, justify="left")
        m1.pack(anchor="w", pady=(6, 0))

        def change():
            if new.get() != new2.get():
                m1.config(text="รหัสผ่านใหม่ทั้งสองช่องไม่ตรงกัน", fg=AD_BAD)
                return
            ok, text = change_admin_password(self.admin["admin_id"], old.get(), new.get())
            m1.config(text=text, fg=AD_OK if ok else AD_BAD)
            if ok:
                for e in (old, new, new2):
                    e.delete(0, "end")

        ad_button(c1, "บันทึก", change, "accent").pack(anchor="w", pady=(8, 0))

        c2 = card("เพิ่มแอดมินคนอื่น")
        n_name = ad_field(c2, "ชื่อแอดมิน", bg=AD_CARD)
        n_user = ad_field(c2, "ชื่อผู้ใช้", bg=AD_CARD)
        n_pass = ad_field(c2, f"รหัสผ่าน ({PASSWORD_HINT})", show="•", bg=AD_CARD)
        m2 = tk.Label(c2, text="", bg=AD_CARD, fg=AD_BAD, font=(FONT, 11), wraplength=320, justify="left")
        m2.pack(anchor="w", pady=(6, 0))

        def add_admin():
            ok, text = create_admin(n_user.get(), n_pass.get(), n_name.get())
            m2.config(text=text, fg=AD_OK if ok else AD_BAD)
            if ok:
                self._account_flash = (f"เพิ่มแอดมิน {n_name.get().strip()} (@{n_user.get().strip().lower()}) แล้ว", True)
                self.go("account")                   # รายชื่อแอดมินด้านบนอัปเดตทันที

        ad_button(c2, "เพิ่มแอดมิน", add_admin, "primary").pack(anchor="w", pady=(8, 0))

    def _admin_list(self):
        """การ์ดรายชื่อแอดมินทั้งหมด: ชื่อ ชื่อผู้ใช้ วันที่สร้าง + ปุ่มลบ (ลบบัญชีตัวเองไม่ได้)"""
        admins = admin_list_admins()
        rf = RoundFrame(self.content, fill=AD_CARD, border=AD_LINE, radius=14, padx=20, pady=14)
        rf.pack(fill="x", padx=(0, 14))
        box = rf.inner
        tk.Label(box, text=f"รายชื่อแอดมิน ({len(admins)} คน)", bg=AD_CARD, fg=AD_TEXT,
                 font=(FONT, 12, "bold")).pack(anchor="w")
        tk.Label(box, text="แอดมินทุกคนเข้าหน้าหลังร้านได้เหมือนกัน  ลบบัญชีตัวเองไม่ได้ และต้องเหลืออย่างน้อย 1 คน",
                 bg=AD_CARD, fg=AD_MUTED, font=(FONT, 10)).pack(anchor="w", pady=(0, 6))
        for n, a in enumerate(admins):
            if n:
                tk.Frame(box, bg=AD_LINE, height=1).pack(fill="x")
            r = tk.Frame(box, bg=AD_CARD)
            r.pack(fill="x", pady=6)
            me = a["admin_id"] == self.admin["admin_id"]
            av = tk.Canvas(r, width=34, height=34, bg=AD_CARD, highlightthickness=0)
            av.pack(side="left")
            aa_oval(av, 1, 1, 33, 33, fill=AD_ACCENT if me else "#EEF1F5", outline="")
            av.create_text(17, 17, text=member_initial(a["name"]), fill=AD_SIDE, font=(FONT, 11, "bold"))
            t = tk.Frame(r, bg=AD_CARD)
            t.pack(side="left", padx=(10, 0))
            top = tk.Frame(t, bg=AD_CARD)
            top.pack(anchor="w")
            tk.Label(top, text=a["name"], bg=AD_CARD, fg=AD_TEXT, font=(FONT, 11, "bold")).pack(side="left")
            if me:
                ad_chip(top, "คุณ", AD_OK).pack(side="left", padx=8)
            tk.Label(t, text=f"@{a['username']}  •  สร้างเมื่อ {fmt_datetime(a['created_at'])}", bg=AD_CARD,
                     fg=AD_MUTED, font=(FONT, 10)).pack(anchor="w")
            if not me:
                ad_button(r, "ลบแอดมิน", lambda a=a: self._delete_admin(a), "danger", height=32).pack(side="right")

    def _delete_admin(self, a):
        if not messagebox.askyesno("ลบแอดมิน", f"ลบบัญชีแอดมิน {a['name']} (@{a['username']})?\n"
                                               "บัญชีนี้จะเข้าสู่ระบบแอดมินไม่ได้อีก", parent=self):
            return
        ok, text = delete_admin(a["admin_id"], self.admin["admin_id"])
        self._account_flash = (text, ok)
        self.go("account")

if __name__ == "__main__":
    print("ไฟล์นี้เป็นส่วนหนึ่งของโปรแกรม Meme Beans  ให้เปิดโปรแกรมด้วยไฟล์ project.py")
