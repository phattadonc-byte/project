"""
Meme Beans Coffee - ระบบสั่งเครื่องดื่มร้านกาแฟ (Python + tkinter + SQLite)
project.py  -  ไฟล์โค้ดหลัก (ไฟล์ 1 จาก 4)  เปิดโปรแกรมด้วยไฟล์นี้:  python project.py

โปรแกรมแบ่งเป็น 4 ไฟล์ (ต้องอยู่โฟลเดอร์เดียวกัน)
  1. project.py   ไฟล์หลัก: หน้าจอฝั่งลูกค้า (ล็อกอิน เมนู ตะกร้า ชำระเงิน ติดตามออเดอร์ แต้ม โปรไฟล์ ผู้จัดทำ)
                  และตัวเปิดโปรแกรม
  2. database.py  ไฟล์ฐานข้อมูล: ค่าตั้งต้นของร้าน ตาราง และข้อมูลสมาชิก/เมนู/ออเดอร์/แต้ม/ภาษี
  3. receipt.py   ไฟล์ใบเสร็จ: รูปแบบเงิน ใบเสร็จ และการส่งอีเมล
  4. admin.py     ไฟล์แอดมิน: ข้อมูลและหน้าจอระบบหลังร้าน

ไฟล์เชื่อมกันอย่างไร (ลูกศร = ดึงของจากไฟล์นั้นมาใช้ ด้วยคำสั่ง from ... import ...)
  project.py  -> database.py, receipt.py, admin.py (เปิดหน้าแอดมิน)
  receipt.py  -> database.py
  admin.py    -> database.py, receipt.py, project.py (ปุ่ม การ์ด ฟอนต์)
  database.py -> ไม่ใช้ไฟล์อื่น

สารบัญโค้ด (ค้นหาคำว่า  "# ส่วนที่ N:"  ในไฟล์ที่ระบุ ด้วย Ctrl+F  /  อัปเดตเลขบรรทัดด้วย:  python up.py)
  ส่วนที่  1  ตั้งค่าและข้อมูลตั้งต้น ............ database.py  บรรทัด 21 - 158
  ส่วนที่  2  ฐานข้อมูล: เชื่อมต่อและสร้างตาราง .. database.py  บรรทัด 161 - 482
  ส่วนที่  3  ระบบสมาชิก (ฐานข้อมูล) ............. database.py  บรรทัด 485 - 757
  ส่วนที่  4  เมนูและออเดอร์ (ฐานข้อมูล) ......... database.py  บรรทัด 760 - 1347
  ส่วนที่  5  ใบเสร็จและการส่งอีเมล .............. receipt.py   บรรทัด 30 - 744
  ส่วนที่  6  ระบบแอดมิน (ฐานข้อมูล) ............. admin.py     บรรทัด 49 - 1133
  ส่วนที่  7  ธีมสีและฟอนต์ ...................... project.py   บรรทัด 94 - 154
  ส่วนที่  8  ตัวช่วยพื้นฐานของหน้าจอ ............ project.py   บรรทัด 157 - 918
  ส่วนที่  9  ตะกร้าสินค้า (ตรรกะ) ............... project.py   บรรทัด 921 - 965
  ส่วนที่ 10  วิดเจ็ตทั่วไป ...................... project.py   บรรทัด 968 - 1336
  ส่วนที่ 11  หน้าปรับแต่งเครื่องดื่ม ............ project.py   บรรทัด 1339 - 1808
  ส่วนที่ 12  รูปทรงและไอคอนหมวดหมู่ ............. project.py   บรรทัด 1811 - 1875
  ส่วนที่ 13  รูปเมนูและแบนเนอร์ ................. project.py   บรรทัด 1878 - 2561
  ส่วนที่ 14  วิดเจ็ตย่อยของหน้าเมนู ............. project.py   บรรทัด 2564 - 2735
  ส่วนที่ 15  หน้าต่างตะกร้า ..................... project.py   บรรทัด 2738 - 2873
  ส่วนที่ 16  หน้าชำระเงิน ....................... project.py   บรรทัด 2876 - 3753
  ส่วนที่ 17  หน้าแต้มสะสมและส่วนลด .............. project.py   บรรทัด 3756 - 4173
  ส่วนที่ 18  หน้าข้อมูลสมาชิก + ประวัติการสั่งซื้อ  project.py   บรรทัด 4176 - 4979
  ส่วนที่ 19  หน้าเลือกเมนู ...................... project.py   บรรทัด 4982 - 5779
  ส่วนที่ 20  ระบบแอดมิน (หน้าจอ) ................ admin.py     บรรทัด 1136 - 3680
  ส่วนที่ 21  แอปหลัก + หน้าล็อกอิน / สมัครสมาชิก  project.py   บรรทัด 5782 - 6222
  ส่วนที่ 22  จุดเริ่มโปรแกรม .................... project.py   บรรทัด 6824 - 6837
  ส่วนที่ 23  หน้าผู้จัดทำ ....................... project.py   บรรทัด 6226 - 6440
  ส่วนที่ 24  ติดตามสถานะออเดอร์ (ฝั่งลูกค้า) .... project.py   บรรทัด 6443 - 6821
"""

import sys                                  # ข้อมูลของตัว Python: sys.modules ให้ admin.py ใช้ไฟล์นี้ชุดเดียวกัน, sys.platform เช็กว่าเป็น Windows ไหม
import base64                               # แปลงไฟล์รูป PNG (bytes) เป็นข้อความ base64 เพื่อส่งให้ tk.PhotoImage แสดงรูป
import io                                   # io.BytesIO เก็บไฟล์รูปไว้ในหน่วยความจำแทนไฟล์จริง ตอนย่อ/แปลงรูปด้วย Pillow
import itertools                            # itertools.count สร้างเลขลำดับไม่ซ้ำ ใช้ตั้งชื่อ tag ของรูปที่วาดแบบขอบเนียน
import math                                 # คำนวณรูปทรงที่วาดเอง เช่น วงกลม มุมโค้ง ดาว (sin cos hypot) และปัดขนาดรูป (ceil floor)
from datetime import datetime               # แปลงวันที่จากฐานข้อมูล (ปี-เดือน-วัน) เป็น วัน/เดือน/ปี ตอนแสดงผล (fmt_date)
import os                                   # จัดการไฟล์และโฟลเดอร์ เช่น ต่อชื่อไฟล์รูปเมนู เช็กว่ามีไฟล์ไหม ดูนามสกุลไฟล์
import struct                               # แปลงตัวเลขเป็นไบต์ ใช้ประกอบไฟล์รูป PNG เอง (หัวไฟล์และความยาวแต่ละช่วง)
import tempfile                             # สร้างไฟล์ชั่วคราว .ppm ตอนดึงข้อมูลรูปออกจาก tkinter บางรุ่น
import threading                            # ส่งอีเมล (ใบเสร็จ, รหัสยืนยันลืมรหัสผ่าน) ในเธรดแยก หน้าจอจะได้ไม่ค้าง
import traceback                            # พิมพ์รายละเอียดข้อผิดพลาดลงคอนโซล ตอนเปิดหน้าชำระเงินไม่สำเร็จ (ไว้หาสาเหตุ)
import unicodedata                          # เช็กสระ/วรรณยุกต์ไทยที่ลอยอยู่ (ประเภท Mn) ตอนตัดข้อความ/แบ่งบรรทัด จะได้ไม่ค้างครึ่งตัว
import zlib                                 # บีบอัดข้อมูลรูปและคำนวณ CRC ตอนประกอบไฟล์ PNG เอง (ใช้คู่กับ struct)
import tkinter as tk                        # สร้างหน้าต่างและวิดเจ็ตทั้งหมดของโปรแกรม เช่น ปุ่ม ช่องกรอก Canvas รูปภาพ
from tkinter import filedialog, messagebox  # filedialog เลือกรูปสลิป/รูปโปรไฟล์ และบันทึกใบเสร็จ, messagebox กล่องแจ้งเตือน/ถามยืนยัน
import tkinter.font as tkfont               # ดูรายชื่อฟอนต์ในเครื่อง และวัดความกว้างข้อความ เพื่อเลือกฟอนต์และจัดขนาดตัวหนังสือ

# จากไฟล์ฐานข้อมูล: ค่าตั้งต้นของร้าน + ฟังก์ชันอ่าน/เขียนข้อมูลสมาชิก เมนู ออเดอร์ แต้ม
from database import (
    BAHT_PER_POINT, IMAGE_DIR, MAX_CUPS_PER_MENU, MINUTES_PER_CUP, PAYMENT_METHODS, PREP_ACTIVE,
    PREP_LABEL, PREP_STEPS, RESET_CODE_MINUTES, REWARD_BY_CODE, REWARDS, SHOP_NAME, SIZE_EXTRA,
    SIZE_OPTIONS, SLIP_MAX_BYTES, TIERS, VAT_INCLUDED_IN_PRICE, VAT_RATE, cancel_order,
    cancel_reset_code, change_password, create_order, create_reset_code, cup_limit,
    discount_amount, find_member_by_phone, get_categories, get_coupons, get_member,
    get_member_active_orders, get_member_avatar, get_member_favorites, get_member_open_slips,
    get_member_orders, get_member_tier, get_order_prep, get_order_receipt, get_payment_state,
    get_point_history, get_popular_products, get_product, get_products, get_slip_image,
    get_unused_coupons, is_valid_email, login_member, mark_order_paid, mask_email,
    member_order_stats, order_amounts, redeem_coupon, register_member, reset_password_with_code,
    set_member_avatar, set_member_email, setup_database, size_from_options, stock_status,
    submit_payment_slip, tier_progress, update_member, vat_split,
    password_char_problem, password_checks, password_problem,
)

# จากไฟล์ใบเสร็จ: รูปแบบเงิน เลขออเดอร์ และการส่งใบเสร็จ/อีเมล
from receipt import (
    RECEIPT_PDF_ERRORS, build_receipt, build_receipt_pdf, explain_email_error, fmt_datetime,
    fmt_price, money_rows, order_code, receipt_filename, receipt_page, send_receipt_email,
    send_reset_code_email,
)

# เปิดด้วย "python project.py" Python จะเรียกไฟล์นี้ว่า __main__
# บรรทัดนี้ให้ชื่อ project ชี้มาที่ไฟล์ที่กำลังทำงานอยู่ด้วย เพื่อให้ admin.py ที่เขียนว่า
# "from project import ..." ใช้ปุ่ม/ฟอนต์ชุดเดียวกัน (ไม่โหลดไฟล์นี้ซ้ำเป็นอีกชุด)
sys.modules.setdefault("project", sys.modules[__name__])

# หน้าจอแอดมินอยู่ในไฟล์ admin.py  (โหลดตอนกดเข้าหน้าแอดมิน ดูส่วนที่ 21: show_admin)


# =====================================================================
# ส่วนที่ 7: ธีมสีและฟอนต์
#   ประกอบด้วย: สีธีม (PANEL, BG, SURFACE, TEXT, ACCENT, ...), สีภาพวาด และ FONT, FONT_MEME, FONT_SCRIPT, setup_fonts
#              ขนาดหน้าต่างเล็กสุด (MIN_WINDOW)
#   แก้ที่นี่เมื่อ: เปลี่ยนสีหรือฟอนต์ของทั้งโปรแกรม
# บรรทัด 94 - 154
# =====================================================================
# ธีม "คาเฟ่ปูนเปลือยโทนมืด + มีม": พื้นดำ/เทาแบบผนังปูน ตัวอักษรขาวนวล เน้นด้วยเหลืองมีม
PANEL = "#0F0F0F"          # ดำสนิท (แถบหัว แผงซ้าย)
BG = "#171717"             # พื้นหลังหน้า (เทาถ่าน)
SURFACE = "#212121"        # การ์ด
SURFACE_2 = "#2B2B2B"      # ช่องกรอก / ปุ่มรอง / พื้นรูป
SURFACE_3 = "#383838"      # ตอนเอาเมาส์ชี้
LINE = "#3A3A3A"           # เส้นขอบ / เส้นแบ่ง
TEXT = "#F2EFEA"           # ตัวอักษรหลัก (ขาวนวล)
TEXT_MUTED = "#B4ADA2"     # ตัวอักษรรอง (สว่างพอให้อ่านง่ายบนพื้นมืด)
LATTE = "#C9A47E"          # น้ำตาลลาเต้ (คำอธิบาย)
ACCENT = "#FFD43B"         # เหลืองมีม (ปุ่มหลัก ราคา จุดเด่น)
ACCENT_DARK = "#E9BD1E"
ACCENT_INK = "#141414"     # ตัวอักษรบนพื้นเหลือง
PINK = "#FF5C8A"           # สติกเกอร์ HOT / ตัวเลขบนตะกร้า
SUCCESS = "#6CC487"
DRINK_CARD = "#1D1915"     # พื้นการ์ดเมนู (น้ำตาลดำ แบบป้ายเมนูร้านกาแฟ)
DRINK_LINE = "#3A3129"     # ขอบการ์ดเมนู
GOLD = "#E9C98F"           # ชื่อเมนูสีทอง
MENU_DESC = "#DCCFBD"      # คำอธิบายบนการ์ดเมนู (ครีมอุ่น อ่านง่ายบนพื้นน้ำตาลดำ)
ERROR = "#FF6B5E"

# สีสำหรับภาพวาด (ตัวการ์ตูน แก้ว ไอคอน ลายแก้ว)
BLACK = "#141414"
CREAM = "#F2EFEA"
TAN = "#C9A47E"
TAN_DARK = "#9C7A55"
GREEN = "#4E7A3A"
# สีเหรียญระดับสมาชิก (ชื่อระดับกำหนดที่ TIERS ในส่วนที่ 1  ระดับที่ไม่มีในนี้ใช้สี LATTE)
TIER_COLORS = {"Silver": "#C9CED6", "Gold": "#F2C94C", "Platinum": "#9ED9E8"}
TIER_TAGLINES = {"Silver": "สมาชิกใหม่ทุกคนเริ่มที่ระดับนี้", "Gold": "ลูกค้าประจำ สายจิบทุกวัน",
                 "Platinum": "ระดับสูงสุด สายคาเฟอีนตัวจริง"}

# ฟอนต์: เลือกตัวแรกที่มีในเครื่อง (Windows มีครบทุกตัว)
FONT_CHOICES = ["Leelawadee UI", "Tahoma"]            # ภาษาไทยทั้งโปรแกรม
FONT_MEME_CHOICES = ["Impact", "Arial Black"]          # ตัวหนังสือมีม (อังกฤษตัวพิมพ์ใหญ่)
FONT_SCRIPT_CHOICES = ["Segoe UI Black", "Arial Black"]  # ตัวหนาแบบโลโก้ (อ่านง่ายกว่าตัวลายมือ)
FONT = "Tahoma"
MIN_WINDOW = (640, 480)          # หน้าต่างย่อได้เล็กสุดเท่านี้ (จัดวาง 2 หน้าต่างครึ่งจอได้)
FONT_MEME = "Impact"
FONT_SCRIPT = "Segoe UI Black"
FONT_HAND = "Segoe Print"        # ลายมือแบบป้ายชอล์ก
FONT_LOGO = "Segoe UI Black"    # ตัวหนาหนาแบบโลโก้ (ถ้าไม่มีจะใช้ฟอนต์ระบบแทน)


def setup_fonts(root):
    """เลือกฟอนต์ที่มีในเครื่อง (เรียกครั้งเดียวหลังสร้างหน้าต่างหลัก)"""
    global FONT, FONT_MEME, FONT_SCRIPT
    try:
        families = set(tkfont.families(root))
    except tk.TclError:
        return
    FONT = next((f for f in FONT_CHOICES if f in families), FONT)
    FONT_MEME = next((f for f in FONT_MEME_CHOICES if f in families), FONT)
    FONT_SCRIPT = next((f for f in FONT_SCRIPT_CHOICES if f in families), FONT)


# =====================================================================
# ส่วนที่ 8: ตัวช่วยพื้นฐานของหน้าจอ
#   ประกอบด้วย: rounded_rect, meme_text (ตัวหนังสือมีม), PillButton/make_button (ปุ่มมุมมน), LinkButton,
#              RoundEntry/make_field (ช่องกรอกมุมมน), RoundFrame (การ์ดมุมมน), Pill (ป้าย),
#              text_width / font_linespace / fit_text (ตัดข้อความ 1 บรรทัด),
#              wrap_text (แบ่งบรรทัดภาษาไทยตรงรอยต่อคำ)
#   แก้ที่นี่เมื่อ: แก้หน้าตาปุ่ม/ช่องกรอก/การ์ด หรือวิธีตัดบรรทัดข้อความ
# บรรทัด 157 - 918
# =====================================================================
# ---------- วาดขอบเนียน (anti-alias) ----------
# ที่คำนวณความทึบของแต่ละพิกเซลเอง ส่วนเส้นตรงใช้สี่เหลี่ยมธรรมดา (คมอยู่แล้ว)
try:                                    
    from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

_AA_CACHE = {}
_AA_SEQ = itertools.count(1)


def _rgb(color):
    if not color:
        return None
    if color.startswith("#") and len(color) == 7:
        return int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    r, g, b = tk._default_root.winfo_rgb(color)
    return r >> 8, g >> 8, b >> 8


def _photo_from_rows(w, h, rows):
    """สร้าง PhotoImage (PNG มีความโปร่งใส) จากข้อมูลพิกเซล RGBA ทีละแถว"""
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 3)) + chunk(b"IEND", b""))
    return tk.PhotoImage(data=base64.b64encode(png).decode("ascii"), format="png")


def _aa_pixel(d, bw, F, O):
    """สีพิกเซลจากระยะถึงขอบ d (ค่าลบ = อยู่ด้านในรูป), bw = ความหนาเส้นขอบ"""
    co = min(0.5 - d, 1.0)
    if co <= 0:
        return (0, 0, 0, 0)
    ci = min(max(0.5 - (d + bw), 0.0), 1.0) if (O and bw) else co
    if not F:
        a = co - ci
        return (O[0], O[1], O[2], int(a * 255 + .5)) if a > 0 else (0, 0, 0, 0)
    if not (O and bw):
        return (F[0], F[1], F[2], int(co * 255 + .5))
    fo = co - ci
    return (int((F[0] * ci + O[0] * fo) / co + .5), int((F[1] * ci + O[1] * fo) / co + .5),
            int((F[2] * ci + O[2] * fo) / co + .5), int(co * 255 + .5))


def _corner_image(R, fill, outline, bw, corner):
    key = ("corner", R, fill, outline, bw, corner)
    if key not in _AA_CACHE:
        F, O = _rgb(fill), _rgb(outline)
        rows = []
        for j in range(R):
            row = []
            for i in range(R):
                d = math.hypot(R - (i + .5), R - (j + .5)) - R
                row.extend(_aa_pixel(d, bw, F, O))
            rows.append(row)
        if corner in ("tr", "br"):
            rows = [sum([r[k:k + 4] for k in range(len(r) - 4, -1, -4)], []) for r in rows]
        if corner in ("bl", "br"):
            rows = rows[::-1]
        _AA_CACHE[key] = _photo_from_rows(R, R, rows)
    return _AA_CACHE[key]


def _oval_image(w, h, fill, outline, bw):
    key = ("oval", w, h, fill, outline, bw)
    if key not in _AA_CACHE:
        F, O = _rgb(fill), _rgb(outline)
        a, b = w / 2, h / 2
        m = min(a, b)
        rows = []
        for j in range(h):
            dy = j + .5 - b
            row = []
            for i in range(w):
                dx = i + .5 - a
                d = (math.hypot(dx, dy) - a) if a == b else (math.hypot(dx / a, dy / b) - 1) * m
                row.extend(_aa_pixel(d, bw, F, O))
            rows.append(row)
        _AA_CACHE[key] = _photo_from_rows(w, h, rows)
    return _AA_CACHE[key]


def _polygon_rect(c, x1, y1, x2, y2, r, **kw):
    """แบบเดิม (ใช้กรณีพิเศษ เช่น เส้นประ)"""
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
           x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
    return c.create_polygon(pts, smooth=True, **kw)


def _shapes(c):
    try:
        return c.aa_shapes
    except AttributeError:
        c.aa_shapes = {}
        return c.aa_shapes


def rounded_rect(c, x1, y1, x2, y2, r, fill="", outline="", width=1, tags=None, **kw):
    """สี่เหลี่ยมมุมมนขอบเนียน: ส่วนตรงเป็นสี่เหลี่ยม ส่วนโค้ง 4 มุมเป็นรูปที่ลบรอยหยักแล้ว
    คืนค่าชื่อแท็ก (ใช้กับ tag_lower / delete / restyle ได้)"""
    if isinstance(c, _PilCanvas):
        return _polygon_rect(c, x1, y1, x2, y2, r, fill=fill, outline=outline, width=width)
    X1, Y1, X2, Y2 = (int(round(v)) for v in (x1, y1, x2, y2))
    w, h = X2 - X1, Y2 - Y1
    if kw or w < 3 or h < 3 or not fill:
        return _polygon_rect(c, x1, y1, x2, y2, r, fill=fill, outline=outline, width=width,
                             tags=tags, **kw)
    R = int(round(max(0, min(r, w / 2, h / 2))))
    O = outline if (outline and outline != fill and width) else ""
    bw = int(round(width)) if O else 0
    tag = f"aa{next(_AA_SEQ)}"
    extra = (tags,) if isinstance(tags, str) else tuple(tags or ())
    t = (tag,) + extra

    def rect(a, b, cc, d, col):
        if cc > a and d > b:
            c.create_rectangle(a, b, cc, d, fill=col, outline="", width=0, tags=t)

    rect(X1 + R, Y1, X2 - R, Y2, fill)
    rect(X1, Y1 + R, X1 + R, Y2 - R, fill)
    rect(X2 - R, Y1 + R, X2, Y2 - R, fill)
    if O:
        rect(X1 + R, Y1, X2 - R, Y1 + bw, O)
        rect(X1 + R, Y2 - bw, X2 - R, Y2, O)
        rect(X1, Y1 + R, X1 + bw, Y2 - R, O)
        rect(X2 - bw, Y1 + R, X2, Y2 - R, O)
    if R > 0:
        for corner, (cx, cy) in (("tl", (X1, Y1)), ("tr", (X2 - R, Y1)),
                                 ("bl", (X1, Y2 - R)), ("br", (X2 - R, Y2 - R))):
            c.create_image(cx, cy, image=_corner_image(R, fill, O, bw, corner), anchor="nw", tags=t)
    _shapes(c)[tag] = ("rr", (x1, y1, x2, y2, r), {"fill": fill, "outline": outline,
                                                   "width": width, "tags": tags})
    return tag


def aa_oval(c, x1, y1, x2, y2, fill="", outline="", width=1, tags=None, state="normal"):
    """วงกลม/วงรีขอบเนียน (ใช้แทน create_oval) คืนค่า id ของรูป"""
    X1, Y1, X2, Y2 = (int(round(v)) for v in (x1, y1, x2, y2))
    w, h = X2 - X1, Y2 - Y1
    if isinstance(c, _PilCanvas) or w < 4 or h < 4:
        return c.create_oval(x1, y1, x2, y2, fill=fill, outline=outline, width=width,
                             tags=tags, state=state)
    O = outline if (outline and outline != fill and width) else ""
    bw = int(round(width)) if O else 0
    item = c.create_image(X1, Y1, image=_oval_image(w, h, fill, O, bw), anchor="nw",
                          tags=tags, state=state)
    _shapes(c)[item] = ("oval", (x1, y1, x2, y2), {"fill": fill, "outline": outline,
                                                   "width": width})
    return item


def restyle(c, ref, **changes):
    """เปลี่ยนสีพื้น/ขอบของรูปที่วาดด้วย rounded_rect หรือ aa_oval (เช่น ตอนเอาเมาส์ชี้)"""
    info = _shapes(c).get(ref)
    if info is None:
        try:
            c.itemconfig(ref, **changes)
        except tk.TclError:
            pass
        return
    kind, coords, params = info
    params = dict(params, **changes)
    if kind == "oval":
        X1, Y1, X2, Y2 = (int(round(v)) for v in coords)
        O = params["outline"] if (params["outline"] and params["outline"] != params["fill"]
                                  and params["width"]) else ""
        img = _oval_image(X2 - X1, Y2 - Y1, params["fill"], O, int(round(params["width"])) if O else 0)
        c.itemconfig(ref, image=img)
        _shapes(c)[ref] = (kind, coords, params)
        return
    new = rounded_rect(c, *coords, **params)
    c.tag_raise(new, ref)
    c.delete(ref)
    c.addtag_withtag(ref, new)
    c.dtag(new, new)
    _shapes(c)[ref] = (kind, coords, params)
    _shapes(c).pop(new, None)


class _PilCanvas:
    """ตัวกลางให้ฟังก์ชันวาดเดิม (ที่ใช้คำสั่งของ Canvas) วาดลงรูปของ Pillow แบบความละเอียดสูงแทน"""

    def __init__(self, draw, scale, ox, oy, zoom=1.0):
        self.d, self.s, self.ox, self.oy, self.z = draw, scale, ox, oy, zoom
        self.texts = []

    def _pts(self, coords):
        flat = []
        for v in coords:
            flat.extend(v if isinstance(v, (list, tuple)) else [v])
        z = self.z
        return [((flat[i] * z - self.ox) * self.s, (flat[i + 1] * z - self.oy) * self.s)
                for i in range(0, len(flat) - 1, 2)]

    @staticmethod
    def _spline(pts, n=10):
        """เส้นโค้งแบบ smooth=True ของ Tk (ประมาณด้วยเส้นโค้งกำลังสอง)"""
        if len(pts) < 3:
            return pts
        out = [pts[0]]
        mids = [((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
                for i in range(len(pts) - 1)]
        mids[0], mids[-1] = pts[0], pts[-1]
        for i in range(1, len(pts) - 1):
            a, ctl, b = mids[i - 1], pts[i], mids[i]
            for k in range(1, n + 1):
                t = k / n
                out.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * ctl[0] + t * t * b[0],
                            (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * ctl[1] + t * t * b[1]))
        return out

    def _w(self, width):
        return max(1, int(round(float(width) * self.s * self.z)))

    def create_oval(self, *coords, fill="", outline="black", width=1, **kw):
        (x1, y1), (x2, y2) = self._pts(coords)
        self.d.ellipse([x1, y1, x2, y2], fill=fill or None, outline=outline or None,
                       width=self._w(width) if outline else 0)

    def create_rectangle(self, *coords, fill="", outline="black", width=1, **kw):
        (x1, y1), (x2, y2) = self._pts(coords)
        self.d.rectangle([x1, y1, x2, y2], fill=fill or None, outline=outline or None,
                         width=self._w(width) if outline else 0)

    def create_polygon(self, *coords, fill="black", outline="", width=1, smooth=False, **kw):
        pts = self._pts(coords)
        if smooth:
            pts = self._spline(pts + [pts[0], pts[1]])[1:]
        self.d.polygon(pts, fill=fill or None, outline=outline or None,
                       width=self._w(width) if outline else 0)

    def create_line(self, *coords, fill="black", width=1, smooth=False, capstyle="butt", **kw):
        pts = self._pts(coords)
        if smooth:
            pts = self._spline(pts)
        w = self._w(width)
        self.d.line(pts, fill=fill, width=w, joint="curve")
        if capstyle == "round" or smooth:
            for (x, y) in (pts[0], pts[-1]):
                self.d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)

    def create_arc(self, *coords, start=0, extent=90, style="pieslice", fill="",
                   outline="black", width=1, **kw):
        (x1, y1), (x2, y2) = self._pts(coords)
        a0, a1 = -(start + extent), -start
        if a0 > a1:
            a0, a1 = a1, a0
        box = [x1, y1, x2, y2]
        if style == "arc":
            self.d.arc(box, a0, a1, fill=outline or fill, width=self._w(width))
        elif style == "chord":
            self.d.chord(box, a0, a1, fill=fill or None, outline=outline or None,
                         width=self._w(width) if outline else 0)
        else:
            self.d.pieslice(box, a0, a1, fill=fill or None, outline=outline or None,
                            width=self._w(width) if outline else 0)

    def create_text(self, *coords, **kw):
        self.texts.append((coords, kw))

    def delete(self, *args):
        pass


def crisp(c, x0, y0, x1, y1, draw_fn, key, zoom=1.0):
    """วาดลายการ์ตูน/ไอคอนแบบเนียน: ถ้ามี Pillow จะวาดใหญ่ 4 เท่าแล้วย่อลง
    (ไม่มี Pillow ก็วาดลง Canvas ตามปกติ)  zoom = ย่อ/ขยายลายทั้งชุด (พิกัดที่ส่งให้ draw_fn คูณ zoom)"""
    if not HAS_PIL:
        before = set(c.find_all())
        draw_fn(c)
        if zoom != 1.0:
            for item in set(c.find_all()) - before:
                c.scale(item, 0, 0, zoom, zoom)
        return
    x0, y0, x1, y1 = (int(math.floor(x0)), int(math.floor(y0)), int(math.ceil(x1)), int(math.ceil(y1)))
    w, h = max(x1 - x0, 1), max(y1 - y0, 1)
    full = ("crisp", key, w, h)
    if full not in _AA_CACHE:
        S = 4
        img = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        pc = _PilCanvas(ImageDraw.Draw(img), S, x0, y0, zoom)
        draw_fn(pc)
        img = img.resize((w, h), Image.LANCZOS)
        _AA_CACHE[full] = (ImageTk.PhotoImage(img), pc.texts)
    photo, texts = _AA_CACHE[full]
    c.create_image(x0, y0, image=photo, anchor="nw")
    for coords, kw in texts:
        c.create_text(*coords, **kw)


def soft_glow(c, cx, cy, w, h, color, strength=90):
    """แสงไฟนุ่มๆ (วงรีฟุ้ง) เหมือนไฟในร้าน (ต้องมี Pillow)"""
    if not HAS_PIL:
        return
    key = ("glow", w, h, color, strength)
    if key not in _AA_CACHE:
        pad = int(min(w, h) * .35)
        img = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), _rgb(color) + (0,))
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).ellipse([pad, pad, pad + w, pad + h], fill=strength)
        img.putalpha(mask.filter(ImageFilter.GaussianBlur(pad / 2)))
        _AA_CACHE[key] = ImageTk.PhotoImage(img)
    c.create_image(cx, cy, image=_AA_CACHE[key])


def bg_of(widget):
    """สีพื้นหลังของวิดเจ็ต (ใช้ให้มุมมนกลืนกับพื้นด้านหลัง)"""
    try:
        return widget.cget("bg")
    except tk.TclError:
        return BG


# สไตล์ปุ่ม: (สีพื้น, สีตัวอักษร, สีตอนชี้, สีขอบ)
BUTTON_STYLES = {
    "primary": (ACCENT, ACCENT_INK, ACCENT_DARK, ""),          # ปุ่มหลักสีเหลืองมีม
    "secondary": (SURFACE_2, TEXT, SURFACE_3, LINE),
    "dark": (PANEL, TEXT, SURFACE_2, ""),
    "dark_ghost": (PANEL, TEXT, SURFACE_2, LINE),
    "light": (TEXT, ACCENT_INK, "#FFFFFF", ""),
}


def meme_text(c, x, y, text, size=20, fill="white", stroke="black", font=None,
              anchor="center", width=None, thick=2, angle=0):
    """ตัวหนังสือสไตล์มีม: ตัวขาวขอบดำ (วาดเงาดำรอบตัวอักษร 8 ทิศ แล้ววางตัวขาวทับ)
    font=None ใช้ FONT_MEME (Impact) สำหรับภาษาอังกฤษ ถ้าเป็นภาษาไทยส่ง font=(FONT, size, "bold")"""
    f = font or (FONT_MEME, size)
    kw = {"anchor": anchor, "font": f, "angle": angle}
    if width:
        kw["width"] = width
        kw["justify"] = "center"
    for dx in (-thick, 0, thick):
        for dy in (-thick, 0, thick):
            if dx or dy:
                c.create_text(x + dx, y + dy, text=text, fill=stroke, **kw)
    return c.create_text(x, y, text=text, fill=fill, **kw)


class PillButton(tk.Canvas):
    """ปุ่มมุมมน (วาดด้วย Canvas) ใช้แทน tk.Button
    รองรับ .config(text=..., state="disabled"/"normal", command=...) เหมือนปุ่มปกติ"""

    def __init__(self, parent, text, command, kind="primary", height=44, size=11,
                 radius=None, padx=22, colors=None, bold=True):
        super().__init__(parent, height=height, bg=bg_of(parent), highlightthickness=0,
                         bd=0, cursor="hand2")
        self.btn_text = text
        self.btn_cmd = command
        self.btn_state = "normal"
        self.btn_hover = False
        self.btn_colors = colors or BUTTON_STYLES[kind]
        self.btn_font = (FONT, size, "bold" if bold else "normal")
        self.btn_radius = height / 2 if radius is None else radius
        self.btn_padx = padx
        self._fit_width()
        self.bind("<Configure>", lambda e: self._paint())
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
        self.bind("<ButtonRelease-1>", self._click)

    def _fit_width(self):
        w = text_width(self.btn_text, self.btn_font) + 2 * self.btn_padx
        tk.Canvas.configure(self, width=max(w, int(self.cget("height"))))

    def _set_hover(self, on):
        self.btn_hover = on
        self._paint()

    def _click(self, e):
        inside = 0 <= e.x <= self.winfo_width() and 0 <= e.y <= self.winfo_height()
        if inside and self.btn_state == "normal" and self.btn_cmd:
            self.btn_cmd()

    def _paint(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4 or h < 4:
            w, h = int(self.cget("width")), int(self.cget("height"))
        bg, fg, hover, border = self.btn_colors
        if self.btn_state != "normal":
            bg, fg, border = SURFACE_2, TEXT_MUTED, ""
        elif self.btn_hover:
            bg = hover
        rounded_rect(self, 1, 1, w - 1, h - 1, self.btn_radius, fill=bg,
                     outline=border or bg, width=1)
        self.create_text(w / 2, h / 2, text=self.btn_text, fill=fg, font=self.btn_font)

    def configure(self, cnf=None, **kw):
        if cnf:
            kw.update(cnf)
        changed = False
        if "text" in kw:
            self.btn_text = kw.pop("text")
            self._fit_width()
            changed = True
        if "state" in kw:
            self.btn_state = kw.pop("state")
            self.config_cursor()
            changed = True
        if "command" in kw:
            self.btn_cmd = kw.pop("command")
        if kw:
            tk.Canvas.configure(self, **kw)
        if changed:
            self._paint()

    config = configure

    def config_cursor(self):
        tk.Canvas.configure(self, cursor="hand2" if self.btn_state == "normal" else "arrow")

    def cget(self, key):
        if key == "text":
            return self.btn_text
        if key == "state":
            return self.btn_state
        return tk.Canvas.cget(self, key)


def make_button(parent, text, command, primary=True, kind=None, height=44, size=11):
    """ปุ่มหลัก (ดำ) / ปุ่มรอง (ขาวมีขอบ) แบบมุมมน"""
    return PillButton(parent, text, command, kind or ("primary" if primary else "secondary"),
                      height=height, size=size)


class LinkButton(tk.Label):
    """ปุ่มแบบข้อความ (ไม่มีกรอบ) เปลี่ยนสีเมื่อชี้"""

    def __init__(self, parent, text, command, fg=TEXT_MUTED, hover=TEXT, size=10, bold=False):
        super().__init__(parent, text=text, bg=bg_of(parent), fg=fg, cursor="hand2",
                         font=(FONT, size, "bold" if bold else "normal"))
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", lambda e: self.config(fg=hover, font=(FONT, size, "bold" if bold else "normal", "underline")))
        self.bind("<Leave>", lambda e: self.config(fg=fg, font=(FONT, size, "bold" if bold else "normal")))


class RoundEntry(tk.Canvas):
    """ช่องกรอกมุมมน: วาดกรอบด้วย Canvas แล้ววาง tk.Entry ไว้ข้างใน (ใช้งานผ่าน .entry)"""

    def __init__(self, parent, show=None, height=44, size=12, fill=SURFACE_2,
                 border=LINE, focus=ACCENT, fg=TEXT, width=None, radius=12, **entry_kw):
        super().__init__(parent, height=height, bg=bg_of(parent), highlightthickness=0, bd=0)
        if width:
            tk.Canvas.configure(self, width=width)
        self.re_fill, self.re_border, self.re_focus = fill, border, focus
        self.re_radius = radius
        self.re_active = False
        self.entry = tk.Entry(self, font=entry_kw.pop("font", (FONT, size)), bg=fill, fg=fg,
                              insertbackground=fg, relief="flat", bd=0, highlightthickness=0,
                              selectbackground=ACCENT, selectforeground=ACCENT_INK,
                              disabledbackground=fill, show=show, **entry_kw)
        self.re_win = self.create_window(14, height / 2, window=self.entry, anchor="w")
        self.bind("<Configure>", lambda e: self._paint())
        self.bind("<Button-1>", lambda e: self.entry.focus_set())
        self.entry.bind("<FocusIn>", lambda e: self._set_active(True), add="+")
        self.entry.bind("<FocusOut>", lambda e: self._set_active(False), add="+")

    def _set_active(self, on):
        self.re_active = on
        self._paint()

    def _paint(self):
        self.delete("frame")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4:
            w, h = int(self.cget("width")), int(self.cget("height"))
        col = self.re_focus if self.re_active else self.re_border
        rounded_rect(self, 1, 1, w - 1, h - 1, self.re_radius, fill=self.re_fill,
                     outline=col, width=2 if self.re_active else 1, tags="frame")
        self.tag_lower("frame")
        self.itemconfig(self.re_win, width=max(w - 28, 10))
        self.coords(self.re_win, 14, h / 2)


def make_field(parent, label, show=None, compact=False):
    """หัวข้อ + ช่องกรอกมุมมน  คืนค่า tk.Entry (ใช้ .get() / .insert() ได้ตามปกติ)"""
    bg = bg_of(parent)
    tk.Label(parent, text=label, bg=bg, fg=TEXT, font=(FONT, 11, "bold"),
             anchor="w").pack(fill="x", pady=(8, 3) if compact else (12, 4))
    box = RoundEntry(parent, show=show, height=40 if compact else 44)
    box.pack(fill="x")
    return box.entry


def make_password_field(parent, label, compact=False):
    """ช่องตั้งรหัสผ่านใหม่: เหมือน make_field แต่ข้างชื่อช่องมีกติกา 8 ตัวขึ้นไป / A-Z / a-z / 0-9
    แต่ละข้อขึ้น ✓ สีเขียวทันทีที่พิมพ์ได้ตามนั้น  ถ้าพิมพ์ภาษาไทย อักขระพิเศษ หรือเว้นวรรค จะขึ้นคำเตือนสีแดงแทน
    (ตัวกติกาอยู่ใน database.py: password_checks)  คืนค่า tk.Entry เหมือน make_field"""
    bg = bg_of(parent)
    head = tk.Frame(parent, bg=bg)
    head.pack(fill="x", pady=(8, 3) if compact else (12, 4))
    tk.Label(head, text=label, bg=bg, fg=TEXT, font=(FONT, 11, "bold")).pack(side="left")
    rules = tk.Frame(head, bg=bg)                # กติกาอยู่ชิดขวาบรรทัดเดียวกับชื่อช่อง (ฟอร์มไม่สูงขึ้น)
    rules.pack(side="right")
    items = [tk.Label(rules, bg=bg, font=(FONT, 10)) for _ in password_checks("")]
    warn = tk.Label(rules, text="× ใช้ได้เฉพาะ A-Z a-z 0-9", bg=bg, fg=ERROR, font=(FONT, 10))
    box = RoundEntry(parent, show="•", height=40 if compact else 44)
    box.pack(fill="x")
    entry = box.entry

    def update(*_):
        pw = entry.get()
        for w in items + [warn]:
            w.pack_forget()
        if password_char_problem(pw):
            warn.pack(side="left")
            return
        for lb, (short, ok) in zip(items, password_checks(pw)):
            lb.config(text=("✓ " if ok else "• ") + short, fg=SUCCESS if ok else TEXT_MUTED)
            lb.pack(side="left", padx=(10, 0))

    entry.pw_var = tk.StringVar(entry)          # เก็บไว้กับช่องกรอก (ไม่งั้นตัวแปรหาย)
    entry.config(textvariable=entry.pw_var)
    entry.pw_var.trace_add("write", update)     # อัปเดตทุกครั้งที่ข้อความเปลี่ยน (พิมพ์ ลบ วาง)
    update()
    return entry


class RoundFrame(tk.Canvas):
    """กรอบการ์ดมุมมน: ใส่วิดเจ็ตลงใน .inner ได้เหมือน Frame ปกติ (ความสูงปรับตามเนื้อหา)"""

    def __init__(self, parent, fill=SURFACE, border="", radius=16, pad=16, padx=None,
                 pady=None, border_width=1):
        super().__init__(parent, bg=bg_of(parent), highlightthickness=0, bd=0)
        self.rf_fill, self.rf_border, self.rf_radius = fill, border, radius
        self.rf_bw = border_width
        self.rf_padx = pad if padx is None else padx
        self.rf_pady = pad if pady is None else pady
        self.inner = tk.Frame(self, bg=fill)
        self.rf_win = self.create_window(self.rf_padx, self.rf_pady, window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._fit, add="+")
        self.bind("<Configure>", self._paint)

    def _fit(self, e=None):
        w = self.inner.winfo_reqwidth() + 2 * self.rf_padx
        h = self.inner.winfo_reqheight() + 2 * self.rf_pady
        if int(self.cget("width")) != w or int(self.cget("height")) != h:
            tk.Canvas.configure(self, width=w, height=h)

    def _paint(self, e=None):
        w, h = self.winfo_width(), self.winfo_height()
        self.delete("bg")
        rounded_rect(self, 1, 1, w - 1, h - 1, self.rf_radius, fill=self.rf_fill,
                     outline=self.rf_border or self.rf_fill, width=self.rf_bw, tags="bg")
        self.tag_lower("bg")
        self.itemconfig(self.rf_win, width=max(w - 2 * self.rf_padx, 1),
                        height=max(h - 2 * self.rf_pady, 1))

    def set_fill(self, fill, border=None):
        self.rf_fill = fill
        if border is not None:
            self.rf_border = border
        self.inner.config(bg=fill)
        self._paint()


class Pill(tk.Canvas):
    """ป้ายมุมมนขนาดเล็ก (เช่น แต้ม / ระดับสมาชิก / สถานะ)  เปลี่ยนข้อความด้วย set_text"""

    def __init__(self, parent, text, fill, fg, size=10, height=24, padx=10, bold=True):
        super().__init__(parent, height=height, bg=bg_of(parent), highlightthickness=0, bd=0)
        self.p_text, self.p_fill, self.p_fg = text, fill, fg
        self.p_font = (FONT, size, "bold" if bold else "normal")
        self.p_padx = padx
        self._paint()

    def _paint(self):
        self.delete("all")
        h = int(self.cget("height"))
        w = text_width(self.p_text, self.p_font) + 2 * self.p_padx
        tk.Canvas.configure(self, width=w)
        rounded_rect(self, 0, 0, w, h, h / 2, fill=self.p_fill, outline=self.p_fill)
        self.create_text(w / 2, h / 2, text=self.p_text, fill=self.p_fg, font=self.p_font)

    def set_text(self, text):
        self.p_text = text
        self._paint()

    def set_fill(self, fill, fg=None):
        self.p_fill = fill
        if fg:
            self.p_fg = fg
        self._paint()


def make_divider(parent, color=LINE, pady=0):
    tk.Frame(parent, bg=color, height=1).pack(fill="x", pady=pady)


_FONT_OBJ = {}
_TEXT_W = {}


def text_width(text, font):
    """ความกว้างข้อความเป็นพิกเซล  จำฟอนต์และผลที่วัดแล้วไว้ใช้ซ้ำ
    (สร้าง tkfont.Font ใหม่ทุกครั้งที่วัดช้ามาก ปุ่มเยอะ ๆ แล้วหน้าจอจะเปิดช้า/กระตุก)"""
    key = (text, font)
    w = _TEXT_W.get(key)
    if w is None:
        f = _FONT_OBJ.get(font)
        if f is None:
            f = _FONT_OBJ[font] = tkfont.Font(font=font)
        if len(_TEXT_W) > 5000:                     # กันไม่ให้จำไว้เยอะเกินไป
            _TEXT_W.clear()
        w = _TEXT_W[key] = f.measure(text)
    return w


def font_linespace(font):
    """ความสูงหนึ่งบรรทัดของฟอนต์ (พิกเซล) รวมที่ว่างของสระ/วรรณยุกต์บนล่าง"""
    f = _FONT_OBJ.get(font)
    if f is None:
        f = _FONT_OBJ[font] = tkfont.Font(font=font)
    return f.metrics("linespace")


def fit_text(text, font, max_w):
    """ตัดข้อความให้พอดีความกว้าง แล้วเติม … (ใช้กับชื่อ/คำอธิบายบนการ์ด)"""
    text = (text or "").replace("\n", " ")
    if text_width(text, font) <= max_w:
        return text
    while text and text_width(text + "…", font) > max_w:
        text = text[:-1]
        while text and unicodedata.category(text[-1]) == "Mn":    # อย่าให้เหลือสระ/วรรณยุกต์ลอย
            text = text[:-1]
    return text.rstrip() + "…"


# ---- แบ่งข้อความเป็นหลายบรรทัด (ภาษาไทยไม่เว้นวรรคระหว่างคำ จึงต้องหาจุดตัดบรรทัดเอง) ----
_TH_LEAD = "เแโใไ"                # สระหน้า: ห้ามค้างอยู่ท้ายบรรทัด
_TH_FOLLOW = "ะาำๆ"               # สระหลัง/ไม้ยมก: ห้ามขึ้นต้นบรรทัด
# คำที่พบบ่อยในคำอธิบายเมนู ใช้หารอยต่อคำ (ตัดบรรทัดก่อน/หลังคำเหล่านี้ได้สวย) เพิ่มคำใหม่ได้
_TH_WORDS = """
และ ที่ ของ ด้วย ใน กับ เป็น ให้ ได้ ไม่ มี ผสม หอม รสชาติ กลิ่น เหมาะ สำหรับ แบบ ความ นมสด นมข้นหวาน นมข้นจืด
นมข้น กาแฟ ชา โซดา หวาน เปรี้ยว เข้มข้น สดชื่น นุ่ม ละมุน เนียน ดื่ม ซ่า เย็น ร้อน กลุ่ม คน ผู้ ชื่นชอบ
เรียบง่าย พิเศษ เมล็ด เฉพาะ ออกมา พร้อม ฟอง ลงตัว โดดเด่น ยอดนิยม คาเฟ่ ยุค ช็อต ช็อกโกแลต คาราเมล น้ำ
เมนู สุด เสิร์ฟ อากาศ เมือง ดั้งเดิม เอกลักษณ์ ลูกเล่น ทุก กรอง ชง วิธี ดึง สาย ญี่ปุ่น ไต้หวัน กำลังดี ชุ่มคอ
ทันใจ ชื่นใจ กลมกล่อม อร่อย ง่าย มัน ขม จัด อ่อน เขียว ไทย ผลไม้ เขตร้อน อมเปรี้ยว อมหวาน ใบชา คั่ว ส้ม
มะนาว มะม่วง ลิ้นจี่ เสาวรส พีช เผือก น้ำผึ้ง มัทฉะ โฮจิฉะ แอปเปิ้ล สตรอว์เบอร์รี บลูเบอร์รี่ คลาสสิก นิยม
สุขภาพ กลาย ใหม่ เบาๆ ชัด สดใส สไตล์ แท้ ถั่ว ครีม วิปครีม ไซรัป
""".split()
_TH_WORD_INDEX = {}                # ตัวอักษรตัวแรก -> คำที่ขึ้นต้นด้วยตัวนั้น (คำยาวก่อน)
for _w in sorted(set(_TH_WORDS), key=len, reverse=True):
    _TH_WORD_INDEX.setdefault(_w[0], []).append(_w)
_WRAP_CACHE = {}


def _break_ok(t, i):
    """ขึ้นบรรทัดใหม่ก่อนตัวที่ i ได้ไหม (ไม่ให้สระ/วรรณยุกต์หลุดจากพยัญชนะ)"""
    return 0 < i < len(t) and not (unicodedata.category(t[i]) == "Mn" or t[i] in _TH_FOLLOW
                                   or t[i - 1] in _TH_LEAD)


def _break_ranks(t):
    """คะแนนจุดตัดบรรทัดของทุกตำแหน่ง i (ตัดก่อนตัวที่ i)  น้อย = ตัดแล้วสวย
    0 ช่องว่าง  1 รอยต่อคำที่รู้จัก  2 ก่อนสระหน้า/หลัง ะ ำ ๆ  3 กลางคำ (ไม่ให้เหลือเศษสั้นกว่า 3 ตัว)  9 ห้ามตัด"""
    words, i = set(), 0
    while i < len(t):                                   # แบ่งคำจากซ้ายไปขวา เลือกคำที่ยาวที่สุดก่อน
        end = next((i + len(w) for w in _TH_WORD_INDEX.get(t[i], ())
                    if t.startswith(w, i) and (i + len(w) == len(t) or t[i + len(w)] == " "
                                               or _break_ok(t, i + len(w)))), 0)
        if end:
            words.update((i, end))
            i = end
        else:
            i += 1
    ranks = [9] * (len(t) + 1)
    for i in range(1, len(t)):
        if t[i - 1] == " " or t[i] == " ":
            ranks[i] = 0
        elif not _break_ok(t, i):
            continue
        elif i in words:
            ranks[i] = 1
        elif t[i] in _TH_LEAD or t[i - 1] in "ะำๆ":
            ranks[i] = 2
        else:
            word_start = t.rfind(" ", 0, i) + 1
            word_end = t.find(" ", i) if " " in t[i:] else len(t)
            if i - word_start >= 3 and word_end - i >= 3:
                ranks[i] = 3
    return ranks


def _wrap_spans(t, font, max_w, max_lines, ranks, space_first):
    """แบ่ง t เป็นช่วง (ต้น, ท้าย) ทีละบรรทัด  space_first = อยากตัดตรงช่องว่างก่อน (ถ้าบรรทัดเต็มพอ)"""
    tiers = ((0, .65), (1, .35), (2, .5), (3, 0)) if space_first else ((1, .35), (2, .5), (3, 0))
    spans, start, n = [], 0, len(t)
    while start < n and (max_lines is None or len(spans) < max_lines):
        if text_width(t[start:], font) <= max_w:
            spans.append((start, n))
            return spans, n
        lo, hi = start + 1, n                           # ตัวอักษรมากที่สุดที่ยังพอดีบรรทัด
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if text_width(t[start:mid], font) <= max_w:
                lo = mid
            else:
                hi = mid - 1
        cut = 0
        for rank, fill in tiers:                        # จุดตัดที่สวยที่สุด โดยบรรทัดไม่สั้นเกินไป
            cut = next((i for i in range(lo, start, -1) if ranks[i] <= rank
                        and text_width(t[start:i], font) >= max_w * fill), 0)
            if cut:
                break
        if not cut:
            cut = next((i for i in range(lo, start, -1) if _break_ok(t, i)), lo)
        spans.append((start, cut))
        start = cut
        while start < n and t[start] == " ":
            start += 1
    return spans, start


def wrap_text(text, font, max_w, max_lines=None):
    """แบ่งข้อความเป็นบรรทัด แต่ละบรรทัดกว้างไม่เกิน max_w พิกเซล (ใช้กับคำอธิบายบนการ์ดเมนู)
    ตัดตรงช่องว่างหรือรอยต่อคำก่อน ไม่ให้คำขาดกลาง/สระลอย  ถ้าเกิน max_lines บรรทัด
    บรรทัดสุดท้ายลงท้ายด้วย …  คืนค่าเป็นลิสต์ของบรรทัด"""
    t = " ".join((text or "").split())
    key = (t, font, max_w, max_lines)
    if key in _WRAP_CACHE:
        return list(_WRAP_CACHE[key])
    ranks = _break_ranks(t)
    for space_first in (True, False):                   # ลองตัดตรงช่องว่างก่อน ถ้าไม่พอที่ค่อยตัดตรงรอยต่อคำ
        spans, end = _wrap_spans(t, font, max_w, max_lines, ranks, space_first)
        if end >= len(t):
            break
    lines = [t[a:b].rstrip() for a, b in spans]
    if end < len(t) and spans:                          # ยังเหลือข้อความ -> บรรทัดสุดท้ายลงท้าย …
        a = spans[-1][0]
        lo, hi = a, len(t)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if text_width(t[a:mid].rstrip() + "…", font) <= max_w:
                lo = mid
            else:
                hi = mid - 1
        cut = next((i for i in range(lo, a, -1) if ranks[i] <= 1
                    and text_width(t[a:i], font) >= max_w * .5), 0) or \
            next((i for i in range(lo, a, -1) if _break_ok(t, i)), lo)
        lines[-1] = t[a:cut].rstrip() + "…"
    if len(_WRAP_CACHE) > 2000:
        _WRAP_CACHE.clear()
    _WRAP_CACHE[key] = lines
    return list(lines)


# =====================================================================
# ส่วนที่ 9: ตะกร้าสินค้า (ตรรกะ)
#   ประกอบด้วย: class Cart: add / change / remove / total / cups_of (จำนวนแก้วของเมนูหนึ่งในตะกร้า)
#   แก้ที่นี่เมื่อ: แก้วิธีรวมรายการหรือคำนวณยอดรวมในตะกร้า
# บรรทัด 921 - 965
# =====================================================================
class Cart:
    """ตะกร้าสินค้า (ไม่เกี่ยวกับหน้าจอ)"""

    def __init__(self):
        self.items = [] 

    def add(self, product, options, qty, unit_price=None, size=None):
        price = product["price"] if unit_price is None else unit_price
        for it in self.items:
            if it["product_id"] == product["product_id"] and it["options"] == options:
                it["qty"] += qty
                return
        self.items.append({"product_id": product["product_id"],
                           "name": product["name"], "price": price,
                           "options": options, "qty": qty, "size": size})

    def change(self, index, delta):
        self.items[index]["qty"] += delta
        if self.items[index]["qty"] <= 0:
            del self.items[index]

    def remove(self, index):
        del self.items[index]

    def clear(self):
        self.items.clear()

    def total(self):
        return sum(i["price"] * i["qty"] for i in self.items)

    def count(self):
        return sum(i["qty"] for i in self.items)

    def cups_of(self, product_id):
        """จำนวนแก้วของเมนูนี้ในตะกร้า (รวมทุกตัวเลือก/ขนาด)"""
        return sum(i["qty"] for i in self.items if i["product_id"] == product_id)

    def is_empty(self):
        return not self.items


# =====================================================================
# ส่วนที่ 10: วิดเจ็ตทั่วไป
#   ประกอบด้วย: make_choice (ปุ่มเลือก), make_qty_button (ปุ่ม +/-), ThinScrollbar, ScrollFrame (กรอบเลื่อน),
#              fill_screen (เปิดหน้าต่างย่อยเต็มจอ), work_area / fit_work_area (พอดีพื้นที่จอเหนือแถบงาน),
#              maximize_window (เต็มพื้นที่จอแบบมีแถบชื่อ), placed_owner / cover_window
#              (หน้าต่างย่อยของหน้าลูกค้าเปิดเท่าหน้าต่างหน้าลูกค้าที่จัดวางเอง),
#              pack_bottom (ปุ่มล่างไม่โดนตัด), keep_centered (จัดเนื้อหาให้อยู่กลางเมื่อหน้าต่างกว้าง),
#              HoverTip (กล่องข้อความเล็ก ๆ ที่โผล่เมื่อชี้เมาส์ค้าง)
#   แก้ที่นี่เมื่อ: แก้หน้าตาปุ่มเลือก การเลื่อนหน้า หรือการเปิดหน้าต่างเต็มจอ
# บรรทัด 968 - 1336
# =====================================================================
def make_choice(parent, options, var, on_change=None):
    """แถวปุ่มเลือก 1 ตัวเลือกแบบปุ่มมน (ปุ่มที่เลือกจะเป็นสีดำ)"""
    frame = tk.Frame(parent, bg=bg_of(parent))
    buttons = {}

    def refresh():
        for o, b in buttons.items():
            sel = var.get() == o
            b.btn_colors = ((ACCENT, ACCENT_INK, ACCENT, "") if sel
                            else (SURFACE_2, TEXT, SURFACE_3, LINE))
            b._paint()

    def pick(o):
        var.set(o)
        refresh()
        if on_change:
            on_change()

    for o in options:
        b = PillButton(frame, o, lambda o=o: pick(o), "secondary", height=36, size=10, padx=16)
        b.pack(side="left", padx=(0, 8))
        buttons[o] = b
    refresh()
    return frame


class QtyButton(PillButton):
    """ปุ่มวงกลม + / − (วาดเครื่องหมายเป็นเส้น ให้คมชัดทุกฟอนต์)"""

    def _paint(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4:
            w, h = int(self.cget("width")), int(self.cget("height"))
        bg, fg, hover, border = self.btn_colors
        if self.btn_hover:
            bg = hover
        aa_oval(self, 1, 1, w - 1, h - 1, fill=bg, outline=border or bg)
        cx, cy, r = w / 2, h / 2, min(w, h) * 0.22
        self.create_line(cx - r, cy, cx + r, cy, fill=fg, width=2, capstyle="round")
        if self.btn_text == "+":
            self.create_line(cx, cy - r, cx, cy + r, fill=fg, width=2, capstyle="round")


def make_qty_button(parent, text, command, size=34):
    """ปุ่มวงกลม + / - (ส่ง "+" หรือ "-")"""
    return QtyButton(parent, "+" if text == "+" else "-", command, "secondary",
                     height=size, padx=0)


class ThinScrollbar(tk.Canvas):
    """แถบเลื่อนแบบบางสีเข้ม (แทน Scrollbar สีเทาของ Windows ให้เข้ากับธีมมืด)"""

    def __init__(self, parent, command, bg, width=10):
        super().__init__(parent, width=width, bg=bg, highlightthickness=0, bd=0)
        self.sb_cmd = command
        self.sb_first, self.sb_last = 0.0, 1.0
        self.sb_hover = False
        self.sb_drag = None
        self.bind("<Configure>", lambda e: self._paint())
        self.bind("<Enter>", lambda e: self._hover(True))
        self.bind("<Leave>", lambda e: self._hover(False))
        self.bind("<ButtonPress-1>", self._press)
        self.bind("<B1-Motion>", self._move)
        self.bind("<ButtonRelease-1>", lambda e: setattr(self, "sb_drag", None))

    def set(self, first, last):
        self.sb_first, self.sb_last = float(first), float(last)
        self._paint()

    def _hover(self, on):
        self.sb_hover = on
        self._paint()

    def _paint(self):
        self.delete("all")
        if self.sb_last - self.sb_first >= 0.999:
            return
        w, h = self.winfo_width(), self.winfo_height()
        y0, y1 = self.sb_first * h, max(self.sb_last * h, self.sb_first * h + 24)
        rounded_rect(self, 2, y0 + 2, w - 2, y1 - 2, (w - 4) / 2,
                     fill=TEXT_MUTED if self.sb_hover else SURFACE_3, outline="")

    def _press(self, e):
        h = max(self.winfo_height(), 1)
        y0, y1 = self.sb_first * h, self.sb_last * h
        if y0 <= e.y <= y1:
            self.sb_drag = e.y - y0
        else:
            self.sb_cmd("scroll", -1 if e.y < y0 else 1, "pages")

    def _move(self, e):
        if self.sb_drag is not None:
            self.sb_cmd("moveto", (e.y - self.sb_drag) / max(self.winfo_height(), 1))


class ScrollFrame(tk.Frame):
    """กรอบที่เลื่อนขึ้นลงได้ (ใช้กับรายการเมนูและตะกร้า)"""

    def __init__(self, parent, bg):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, yscrollincrement=1)
        self.scrollbar = ThinScrollbar(self, self.canvas.yview, bg)
        self.sf_pending = 0.0               # ระยะที่ยังต้องเลื่อน (พิกเซล) สำหรับเลื่อนแบบนุ่มนวล
        self.sf_anim = None
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self._win, width=e.width))
        self.bind_all("<MouseWheel>", self._on_wheel, add="+")

    def _on_wheel(self, e):
        try:
            if not self.winfo_exists():
                return
            if self.inner.winfo_height() <= self.canvas.winfo_height():
                return
            w = self.winfo_containing(e.x_root, e.y_root)
        except (KeyError, tk.TclError):
            return
        while w is not None:
            if w is self:
                self.sf_pending += -e.delta / 120 * 120
                if self.sf_anim is None:
                    self._glide()
                return
            w = w.master

    def _glide(self):
        """เลื่อนทีละนิดหลายเฟรม (ค่อยๆ ช้าลง) ให้รู้สึกลื่นเหมือนแอปมือถือ"""
        self.sf_anim = None
        if not self.winfo_exists() or abs(self.sf_pending) < 1:
            self.sf_pending = 0.0
            return
        step = int(self.sf_pending * 0.3) or (1 if self.sf_pending > 0 else -1)
        self.canvas.yview_scroll(step, "units")
        self.sf_pending -= step
        self.sf_anim = self.after(12, self._glide)



# ---------- หน้าต่างย่อยแบบเต็มจอ ----------
def fill_screen(win):
    """เปิดหน้าต่างย่อยให้เต็มจอ (ใช้กับหน้าปรับแต่งเครื่องดื่ม ชำระเงิน แต้ม โปรไฟล์ ประวัติ)
    ถ้าหน้าหลักเปิดโหมดเต็มจอ (F11) อยู่ จะเต็มจอแบบเดียวกัน
    ไม่งั้นขยายเต็มพื้นที่จอ "เหนือแถบงาน (taskbar)" แบบมีแถบชื่อและปุ่มปิด ปุ่มด้านล่างจึงไม่โดนแถบงานบัง"""
    win.resizable(True, True)
    if owner_fullscreen(win):
        win.attributes("-fullscreen", True)
        return
    owner = placed_owner(win)
    if owner is not None:                       # หน้าลูกค้าที่จัดวางเอง (เช่น แบ่งจอกับหน้าแอดมิน)
        cover_window(win, owner)                # -> หน้าต่างย่อยเต็มเท่าหน้าต่างหน้าลูกค้า ไม่ทับหน้าแอดมิน
        return
    maximize_window(win)


def maximize_window(win):
    """ขยายหน้าต่างเต็มพื้นที่จอเหนือแถบงาน แบบมีแถบชื่อและปุ่มย่อ/ขยาย/ปิด (ยังลากหรือจัดวางเองได้)"""
    if fit_work_area(win):                      # Windows
        return
    try:
        win.state("zoomed")                     # macOS
    except tk.TclError:
        try:
            win.attributes("-zoomed", True)     # Linux
        except tk.TclError:
            pass


def owner_fullscreen(win):
    """หน้าต่างเจ้าของ (หน้าต่างหลัก หรือหน้าต่างลูกค้าที่เปิดจากหน้าแอดมิน) เปิดโหมดเต็มจอ (F11) อยู่ไหม"""
    w = win.master
    while w is not None:
        if hasattr(w, "is_fullscreen"):
            return w.is_fullscreen
        w = w.master
    return False


def placed_owner(win):
    """หน้าต่าง "หน้าลูกค้า" (เปิดจากปุ่ม Main Menu) ที่เป็นเจ้าของหน้าต่างย่อยนี้ ไม่ใช่คืนค่า None"""
    w = win.master
    while w is not None:
        if getattr(w, "keep_place", False) and not getattr(w, "is_fullscreen", False):
            return w
        w = w.master
    return None


def cover_window(win, owner):
    """วางหน้าต่างย่อยทับพอดีหน้าต่างเจ้าของ (ขนาดและตำแหน่งเดียวกัน ขอบหน้าต่างแบบเดียวกัน)"""
    owner.update_idletasks()
    win.geometry(f"{owner.winfo_width()}x{owner.winfo_height()}+{owner.winfo_x()}+{owner.winfo_y()}")


def grab_modal(win):
    """ล็อกให้กดได้เฉพาะหน้าต่างย่อยนี้จนกว่าจะปิด (หน้าต่างด้านหลังกดไม่ได้)
    ยกเว้นหน้าต่างของ "หน้าลูกค้า" ที่เปิดจากหน้าแอดมิน: ไม่ล็อก ไม่งั้นหน้าแอดมินจะกดอะไรไม่ได้ไปด้วย"""
    w = win
    while w is not None:
        if isinstance(w, CustomerWindow):
            return
        w = w.master
    try:
        win.grab_set()
    except tk.TclError:           # บางเครื่อง grab ตอนหน้าต่างยังไม่แสดงจะ error -> ข้ามได้
        pass


def work_area(win):
    """พื้นที่จอที่หน้าต่างอยู่ ไม่รวมแถบงานของ Windows: (ซ้าย, บน, ขวา, ล่าง)  ระบบอื่นคืนค่า None
    (หน้าต่างย่อยของ tkinter บน Windows ถ้าสั่ง zoomed จะขยายทับแถบงาน ปุ่มล่างเลยโดนบัง จึงต้องคำนวณเอง)"""
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class MONITORINFO(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                        ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]

        user32 = ctypes.windll.user32
        user32.MonitorFromWindow.restype = ctypes.c_void_p
        user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
        user32.GetMonitorInfoW.argtypes = [ctypes.c_void_p, ctypes.POINTER(MONITORINFO)]
        info = MONITORINFO()
        info.cbSize = ctypes.sizeof(MONITORINFO)
        monitor = user32.MonitorFromWindow(int(win.wm_frame(), 16), 2)    # 2 = จอที่ใกล้หน้าต่างที่สุด
        if monitor and user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            r = info.rcWork
        else:                                                         # สำรอง: จอหลัก
            r = wintypes.RECT()
            if not user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(r), 0):   # SPI_GETWORKAREA
                return None
        if r.right - r.left < 200 or r.bottom - r.top < 200:
            return None
        return r.left, r.top, r.right, r.bottom
    except (AttributeError, OSError, ValueError, tk.TclError):
        return None


def fit_work_area(win):
    """ขยายหน้าต่างให้พอดีพื้นที่จอเหนือแถบงาน (Windows) สำเร็จคืนค่า True"""
    win.update_idletasks()                      # ให้หน้าต่างขึ้นจอก่อน จะได้วัดแถบชื่อ/ขอบหน้าต่างได้
    area = work_area(win)
    if area is None:
        return False
    left, top, right, bottom = area
    side = win.winfo_rootx() - win.winfo_x()    # ความหนาขอบซ้าย/ขวา/ล่าง
    head = win.winfo_rooty() - win.winfo_y()    # แถบชื่อ + ขอบบน
    if not (0 <= side <= 40 and 10 <= head <= 120):
        side, head = 8, 31                      # วัดไม่ได้: ใช้ขนาดทั่วไปของ Windows 10/11
    # Windows 10/11 มีขอบใส (ไว้จับย่อขยาย) ที่มองไม่เห็นกว้างประมาณ side-1 พิกเซล
    # เลื่อนออกนอกพื้นที่ให้ขอบที่มองเห็นชนขอบจอพอดี เหมือนหน้าต่างที่กดขยายเต็มจอ
    clear = max(0, side - 1)
    w = right - left - 2 * (side - clear)
    h = bottom - top - head - (side - clear)
    win.geometry(f"{w}x{h}+{left - clear}+{top}")
    return True


def pack_bottom(widget, **kw):
    """วางวิดเจ็ต (เช่น แถวปุ่ม) ไว้ล่างสุด และให้ได้พื้นที่ก่อนเนื้อหาอื่น
    จอเตี้ยแล้วปุ่มจะไม่โดนตัด (เนื้อหาด้านบนถูกบีบแทน)"""
    others = [w for w in widget.master.pack_slaves() if w is not widget]
    if others:
        kw["before"] = others[0]
    widget.pack(side="bottom", **kw)


def keep_centered(space, child, max_width, min_pad=0, reserved=0):
    """ให้ child (ที่ pack อยู่) กว้างไม่เกิน max_width และอยู่กลางพื้นที่ space เสมอ (ปรับ padx ให้)
    หน้าต่างเต็มจอจะได้ไม่ยืดเนื้อหาจนกว้างเกินไป  reserved = ความกว้างที่ส่วนอื่นข้าง ๆ ใช้ไปแล้ว
    space ต้องเป็นกรอบที่ความกว้างไม่ขึ้นกับ child (เช่น หน้าต่าง หรือ canvas ของ ScrollFrame)
    (เรียกซ้ำกับ space เดิมได้ เช่น ตอนวาดหน้าใหม่ จะจัดกลางให้ child ตัวล่าสุด)"""
    space.center_target = (child, max_width, min_pad, reserved)
    if not getattr(space, "center_bound", False):
        space.center_bound = True
        space.bind("<Configure>", lambda e: e.widget is space and _fit_center(space), add="+")
    _fit_center(space)


def _fit_center(space):
    child, max_width, min_pad, reserved = space.center_target
    if not child.winfo_exists():
        return
    pad = max(min_pad, (space.winfo_width() - reserved - max_width) // 2)
    if getattr(child, "center_pad", None) != pad:
        child.center_pad = pad
        child.pack_configure(padx=pad)


class HoverTip:
    """กล่องข้อความเล็ก ๆ ที่โผล่ข้างวิดเจ็ตเมื่อชี้เมาส์ค้างไว้ครู่หนึ่ง เอาเมาส์ออก/คลิกแล้วหายไป
    (ใช้แสดงคำอธิบายเมนูแบบเต็มเมื่อบนการ์ดยาวเกินจนต้องตัด …)"""
    DELAY = 450                     # มิลลิวินาทีที่ต้องชี้ค้างก่อนกล่องจะโผล่
    WIDTH = 300                     # ความกว้างข้อความในกล่อง (พิกเซล)
    SIZE = 12                       # ขนาดตัวอักษร

    def __init__(self, widget, text, title=None):
        self.widget, self.text, self.title = widget, text, title
        self.tip = self.job = None
        widget.bind("<Enter>", self._schedule, add="+")
        for seq in ("<Leave>", "<ButtonPress>", "<Destroy>"):
            widget.bind(seq, self.hide, add="+")

    def _schedule(self, e=None):
        self.hide()
        self.job = self.widget.after(self.DELAY, self.show)

    def show(self):
        self.job = None
        w = self.widget
        if not w.winfo_exists() or not w.winfo_viewable():
            return
        tip = self.tip = tk.Toplevel(w)
        tip.overrideredirect(True)                       # ไม่มีแถบชื่อ/ปุ่มปิด
        try:
            tip.attributes("-topmost", True)            # ให้อยู่เหนือหน้าต่างหลักแม้เปิดเต็มจอ
        except tk.TclError:
            pass
        box = tk.Frame(tip, bg=DRINK_CARD, highlightthickness=1, highlightbackground=GOLD)
        box.pack()
        if self.title:
            tk.Label(box, text=self.title, bg=DRINK_CARD, fg=GOLD, font=(FONT, self.SIZE, "bold"),
                     anchor="w", justify="left").pack(fill="x", padx=12, pady=(8, 0))
        tk.Label(box, text="\n".join(wrap_text(self.text, (FONT, self.SIZE), self.WIDTH)), bg=DRINK_CARD,
                 fg=TEXT, font=(FONT, self.SIZE), anchor="w",
                 justify="left").pack(fill="x", padx=12, pady=(2 if self.title else 8, 9))
        tip.update_idletasks()
        tw, th = tip.winfo_reqwidth(), tip.winfo_reqheight()
        x = w.winfo_rootx() + w.winfo_width() + 6           # ขวาของวิดเจ็ต ถ้าล้นจอย้ายไปซ้าย
        if x + tw > w.winfo_screenwidth() - 4:
            x = max(4, w.winfo_rootx() - tw - 6)
        y = min(w.winfo_rooty() + 8, w.winfo_screenheight() - th - 4)
        tip.geometry(f"+{x}+{max(4, y)}")

    def hide(self, e=None):
        if self.job:
            try:
                self.widget.after_cancel(self.job)
            except tk.TclError:
                pass
            self.job = None
        if self.tip is not None:
            try:
                self.tip.destroy()
            except tk.TclError:
                pass
            self.tip = None


# =====================================================================
# ส่วนที่ 11: หน้าปรับแต่งเครื่องดื่ม
#   ประกอบด้วย: SWEET_OPTIONS, DESIGN_OPTIONS (ลายแก้ว 5 แบบ), NOTE_CHIPS (หมายเหตุถึงบาริสต้า), temps_for,
#              draw_doodle, draw_cup_preview, draw_design_tile, TilePicker, OptionDialog
#   แก้ที่นี่เมื่อ: เพิ่มระดับความหวาน/ลายแก้ว (ใส่รูป cup_<รหัส>.png ในโฟลเดอร์ images) หรือปรับพรีวิวแก้ว
# บรรทัด 1339 - 1810
# =====================================================================
# ระดับความหวาน (ข้อความนี้แสดงบนปุ่ม และบันทึกในออเดอร์/ใบเสร็จ/คิวหลังร้าน)
SWEET_OPTIONS = ["ไม่หวาน 0%", "หวานน้อย 50%", "หวานปกติ 100%", "หวานมาก 125%"]
SWEET_DEFAULT = SWEET_OPTIONS[2]                  # ค่าเริ่มต้น: หวานปกติ

# ลายแก้ว 5 แบบของร้าน  รูปแก้วแบบไดคัท (พื้นหลังโปร่งใส) อยู่ในโฟลเดอร์ images:
#   cup_<รหัส>_S.png / _M.png / _L.png = รูปแก้วในพรีวิวด้านซ้าย ตามขนาดแก้วที่เลือก
#   cup_<รหัส>_thumb.png               = รูปส่วนบนของแก้ว บนการ์ดให้กดเลือก
#   cup_<รหัส>.png                     = รูปแก้วต้นฉบับ (ใช้ย่อเองถ้าไม่มีไฟล์ตามขนาด)
# (รหัสลาย, ชื่อบนการ์ด, ข้อความที่บันทึกในออเดอร์, สีแก้ว - ใช้วาดแทนถ้าไม่มีรูป)
DESIGN_OPTIONS = [
    ("yellow", "Good Coffee", "ลาย Good Coffee Bad Decisions", "#FFD43B"),
    ("intern", "Intern Joke", "ลาย Intern Joke", "#EFE8DA"),
    ("noway", "No Way!", "ลาย No Way!", "#262626"),
    ("hehe", "Hehe...", "ลาย Hehe...", "#1B1924"),
    ("confused", "???", "ลาย ???", "#EDE4D3"),
]
CUP_PREVIEW_H = {"S": 300, "M": 338, "L": 376}     # ความสูงรูปแก้วในพรีวิว (พิกเซล) ตามขนาดที่เลือก

# หมายเหตุถึงบาริสต้า: ปุ่มลัดตามรูปแบบเครื่องดื่ม และความยาวสูงสุดของข้อความ
NOTE_CHIPS = {"ร้อน": ["ร้อนจัด", "ขอฝาปิด", "ไม่รับหลอด"],
              "default": ["น้ำแข็งน้อย", "แยกน้ำแข็ง", "ไม่รับหลอด"]}
NOTE_MAX = 60
TEMP_BADGE = {"ร้อน": "#FF7A45", "เย็น": "#5FB8E8", "ปั่น": "#C9A47E"}   # สีป้ายรูปแบบบนพรีวิว


def temps_for(product, category_name=""):
    """คืนค่า (รูปแบบที่เลือกได้, ค่าเริ่มต้น) เช่น โซดาไม่มีแบบร้อน"""
    name = product["name"].lower()
    if "soda" in name or "โซดา" in category_name:
        return ["เย็น", "ปั่น"], "เย็น"
    default = "เย็น" if ("iced" in name or "orange" in name) else "ร้อน"
    return ["ร้อน", "เย็น", "ปั่น"], default


def drink_color(name):
    """สีเครื่องดื่มในพรีวิวแก้ว ตามชื่อเมนู"""
    n = name.lower()
    if "green apple" in n:
        return "#9CCB4A"
    if "matcha" in n or "green" in n:
        return "#8DB36B"
    if "blueberry" in n or "taro" in n:
        return "#8A68B8"
    if "blue" in n:
        return "#5FA8D3"
    if "red lime" in n:
        return "#E0384C"
    if "lychee" in n:
        return "#F0A2A2"
    if "mango" in n or "honey" in n:
        return "#F4B230"
    if "hojicha" in n:
        return "#8E5A3A"
    if "strawberry" in n:
        return "#E07A8B"
    if "passion" in n:
        return "#F0B93A"
    if "lemon" in n:
        return "#E6D65C"
    if "thai tea" in n or "peach" in n:
        return "#D98A3D"
    if "mocha" in n:
        return "#5A3620"
    if any(k in n for k in ("americano", "espresso", "drip")):
        return "#3A2216"
    return "#A9784F"


def draw_doodle(c, cx, cy, r, kind, ink=BLACK, paper=CREAM):
    """ลายหน้าการ์ตูนบนแก้ว (วาดขึ้นใหม่แบบเรียบง่าย)"""
    w = max(2, int(r / 12))

    def dot(x, y, d):
        aa_oval(c, x - d, y - d, x + d, y + d, fill=ink, outline="")

    if kind == "cat":
        for s in (-1, 1):
            c.create_polygon(cx + s * .85 * r, cy - .1 * r, cx + s * .78 * r,
                             cy - 1.05 * r, cx + s * .22 * r, cy - .68 * r,
                             fill=paper, outline=ink, width=w)
        aa_oval(c, cx - r, cy - .78 * r, cx + r, cy + .85 * r, fill=paper,
                      outline=ink, width=w)
        for s in (-1, 1):
            dot(cx + s * .38 * r, cy - .12 * r, .09 * r)
            c.create_line(cx + s * .55 * r, cy + .22 * r, cx + s * 1.15 * r,
                          cy + .1 * r, fill=ink, width=1)
            c.create_line(cx + s * .55 * r, cy + .38 * r, cx + s * 1.15 * r,
                          cy + .5 * r, fill=ink, width=1)
        c.create_polygon(cx - .1 * r, cy + .12 * r, cx + .1 * r, cy + .12 * r,
                         cx, cy + .26 * r, fill=ink, outline="")
    elif kind == "dog":
        for s in (-1, 1):
            aa_oval(c, cx + s * .9 * r - .27 * r, cy - .7 * r,
                          cx + s * .9 * r + .27 * r, cy + .35 * r,
                          fill=TAN, outline=ink, width=w)
        aa_oval(c, cx - .95 * r, cy - .9 * r, cx + .95 * r, cy + .9 * r,
                      fill=paper, outline=ink, width=w)
        aa_oval(c, cx - .5 * r, cy, cx + .5 * r, cy + .7 * r, fill="#EBD8B9",
                      outline="")
        for s in (-1, 1):
            dot(cx + s * .38 * r, cy - .25 * r, .09 * r)
        aa_oval(c, cx - .16 * r, cy + .08 * r, cx + .16 * r, cy + .28 * r,
                      fill=ink, outline="")
        c.create_line(cx, cy + .28 * r, cx, cy + .4 * r, fill=ink, width=1)
        for x0 in (cx - .3 * r, cx):
            c.create_arc(x0, cy + .3 * r, x0 + .3 * r, cy + .55 * r, start=180,
                         extent=180, style="arc", outline=ink, width=1)
    elif kind == "frog":
        aa_oval(c, cx - 1.05 * r, cy - .4 * r, cx + 1.05 * r, cy + .8 * r,
                      fill=GREEN, outline=ink, width=w)
        for s in (-1, 1):
            ex, ey = cx + s * .5 * r, cy - .5 * r
            aa_oval(c, ex - .36 * r, ey - .36 * r, ex + .36 * r, ey + .36 * r,
                          fill=paper, outline=ink, width=w)
            dot(ex, ey + .05 * r, .13 * r)
        c.create_arc(cx - .8 * r, cy - .25 * r, cx + .8 * r, cy + .6 * r,
                     start=200, extent=140, style="arc", outline=ink, width=w)
    else:  # logo / smirk
        aa_oval(c, cx - r, cy - r, cx + r, cy + r, fill=paper, outline=ink,
                      width=w)
        if kind == "logo":
            for s in (-1, 1):
                dot(cx + s * .36 * r, cy - .1 * r, .09 * r)
            c.create_line(cx - .62 * r, cy - .34 * r, cx - .12 * r, cy - .42 * r,
                          fill=ink, width=w, capstyle="round")
            c.create_line(cx + .12 * r, cy - .52 * r, cx + .62 * r, cy - .3 * r,
                          fill=ink, width=w, capstyle="round")
            c.create_arc(cx - .5 * r, cy - .05 * r, cx + .5 * r, cy + .6 * r,
                         start=200, extent=140, style="arc", outline=ink, width=w)
        else:
            for s in (-1, 1):
                c.create_line(cx + s * .6 * r, cy - .18 * r, cx + s * .14 * r,
                              cy - .18 * r, fill=ink, width=w, capstyle="round")
                dot(cx + s * .36 * r, cy - .04 * r, .08 * r)
            c.create_arc(cx - .62 * r, cy - .12 * r, cx + .62 * r, cy + .7 * r,
                         start=200, extent=140, style="arc", outline=ink, width=w)


def draw_cup_preview(c, W, H, size, temp, design, color):
    """พรีวิวแก้วแบบวาดเอง (ใช้เมื่อไม่มีรูป cup_<รหัส>.png): ขนาดตามที่เลือก
    ร้อน=แก้วกระดาษสีตามลาย เย็น/ปั่น=แก้วใสพร้อมหลอด"""
    c.delete("all")
    k = {"S": 0.82, "M": 0.94, "L": 1.08}.get(size, 0.94)
    cx, bottom = W / 2, H - 24
    ht, top_w, bot_w = 150 * k, 112 * k, 80 * k
    top = bottom - ht
    lt, rt = cx - top_w / 2, cx + top_w / 2
    lb, rb = cx - bot_w / 2, cx + bot_w / 2
    body = [lt, top, rt, top, rb, bottom, lb, bottom]
    aa_oval(c, lb - 12, bottom - 6, rb + 12, bottom + 10, fill="#262626",
                  outline="")
    if temp == "ร้อน":
        cup = next((d[3] for d in DESIGN_OPTIONS if d[0] == design), CREAM)
        c.create_polygon(body, fill=cup, outline=CREAM, width=2)
        c.create_rectangle(lt - 5 * k, top - 12 * k, rt + 5 * k, top + 3,
                           fill="#5A5A5A", outline="")
        c.create_rectangle(cx - top_w * .36, top - 20 * k, cx + top_w * .36,
                           top - 12 * k, fill="#5A5A5A", outline="")
        for x in (cx - 14 * k, cx, cx + 14 * k):
            c.create_line(x, top - 28 * k, x - 6 * k, top - 40 * k,
                          x + 6 * k, top - 54 * k, x, top - 68 * k,
                          smooth=True, fill=CREAM, width=2)
    else:
        c.create_polygon(body, fill=color, outline="")
        if temp == "ปั่น":
            c.create_arc(lt + 4, top - 36 * k, rt - 4, top + 20 * k, start=0,
                         extent=180, fill="#F3E9D9", outline="")
        c.create_polygon(body, fill="", outline=CREAM, width=3)
        c.create_arc(lt, top - 44 * k, rt, top + 14 * k, start=0, extent=180,
                     style="arc", outline=CREAM, width=3)
        c.create_rectangle(lt - 4 * k, top - 3, rt + 4 * k, top + 4, fill=CREAM,
                           outline="")
        c.create_line(cx + 10 * k, top - 58 * k, cx + 26 * k, bottom - 34 * k,
                      fill=ACCENT, width=6, capstyle="round")
    draw_doodle(c, cx, top + ht * 0.55, top_w * 0.28, "logo")


def tile_fg(sel):
    """สีตัวอักษร/ไอคอนบนการ์ดเลือก (การ์ดที่เลือกเป็นสีเหลือง)"""
    return ACCENT_INK if sel else TEXT


def tile_sub(sel):
    return "#6B5600" if sel else TEXT_MUTED


def draw_size_tile(c, key, sel):
    code, thai, oz, extra = next(s for s in SIZE_OPTIONS if s[0] == key)
    fg = tile_fg(sel)
    h = {"S": 24, "M": 32, "L": 42}[key]
    cx, base = 52, 50
    c.create_polygon(cx - h * .43, base - h, cx + h * .43, base - h,
                     cx + h * .3, base, cx - h * .3, base, fill=fg, outline="")
    c.create_text(cx, 62, text=f"{code} · {thai}", fill=fg, font=(FONT, 11, "bold"))
    sub = f"{oz} oz" + (f" · +฿{extra}" if extra else "")
    c.create_text(cx, 80, text=sub, fill=tile_sub(sel), font=(FONT, 9))


def draw_design_tile(c, key, sel):
    """การ์ดลายแก้ว: รูปลายบนแก้วจริง (images/cup_<รหัส>_thumb.png) + ชื่อลาย"""
    _, label, _, cup = next(d for d in DESIGN_OPTIONS if d[0] == key)
    w = int(c.cget("width"))
    iw = w - 12
    ih = iw * 4 // 3
    photo = load_meme_image(f"cup_{key}_thumb", iw, ih)       # รูปไดคัท ไม่ต้องตัดมุม
    if photo is not None:
        c.create_image(w / 2, 6 + ih / 2, image=photo)
    else:                                  # ไม่มีรูป: วาดแผ่นสีแก้ว + หน้ามาสคอต
        rounded_rect(c, 6, 6, w - 6, 6 + ih, 10, fill=cup, outline=LINE)
        cx, cy = w / 2, 6 + ih / 2
        crisp(c, cx - 26, cy - 26, cx + 26, cy + 26,
              lambda d: draw_doodle(d, cx, cy, 20, "logo"), ("doodle", "logo", w))
    h = int(c.cget("height"))
    c.create_text(w / 2, (6 + ih + h) / 2, text=label, fill=tile_fg(sel), width=w - 8,
                  justify="center", font=(FONT, 10, "bold"))     # ชื่อยาวขึ้นบรรทัดใหม่ได้


class TilePicker(tk.Frame):
    """แถวการ์ดเลือก 1 ตัวเลือกแบบมีภาพ มุมมน (ใช้เลือกขนาดแก้ว ลายแก้ว วิธีชำระเงิน ส่วนลด)"""

    def __init__(self, parent, keys, var, tile_w, tile_h, draw, on_change=None):
        super().__init__(parent, bg=bg_of(parent))
        self.var, self.draw, self.on_change = var, draw, on_change
        self.tiles = {}
        self.hover_key = None
        for key in keys:
            c = tk.Canvas(self, width=tile_w, height=tile_h, bg=bg_of(parent),
                          highlightthickness=0, cursor="hand2")
            c.pack(side="left", padx=(0, 10))
            c.bind("<Button-1>", lambda e, k=key: self.pick(k))
            c.bind("<Enter>", lambda e, k=key: self._hover(k))
            c.bind("<Leave>", lambda e: self._hover(None))
            self.tiles[key] = c
        self.refresh()

    def _hover(self, key):
        self.hover_key = key
        self.refresh()

    def pick(self, key):
        self.var.set(key)
        self.refresh()
        if self.on_change:
            self.on_change()

    def refresh(self):
        for key, c in self.tiles.items():
            sel = self.var.get() == key
            c.delete("all")
            w, h = int(c.cget("width")), int(c.cget("height"))
            edge = ACCENT if sel else (TEXT_MUTED if key == self.hover_key else LINE)
            rounded_rect(c, 1, 1, w - 1, h - 1, 14, fill=ACCENT if sel else SURFACE,
                         outline=edge, width=1)
            self.draw(c, key, sel)


class OptionDialog(tk.Toplevel):
    """หน้าปรับแต่งเครื่องดื่ม: รูปแบบ ความหวาน ขนาดแก้ว ลายแก้ว จำนวน (มีพรีวิวแก้ว)"""
    PREVIEW_W, PREVIEW_H = 262, 400

    def __init__(self, parent, product, on_add, temps=None, default_temp="ร้อน",
                 max_qty=MAX_CUPS_PER_MENU, qty_hint=""):
        super().__init__(parent)
        self.product = product
        self.on_add = on_add
        self.max_qty = max(1, max_qty)        # สั่งได้มากสุดกี่แก้ว (ไม่เกิน 10/เมนู และไม่เกินสต็อก)
        self._hint_job = None
        self.title(f"ปรับแต่ง {product['name']}")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        temps = temps or ["ร้อน", "เย็น", "ปั่น"]
        self.temp = tk.StringVar(value=default_temp if default_temp in temps else temps[0])
        self.sweet = tk.StringVar(value=SWEET_DEFAULT)
        self.size = tk.StringVar(value="M")
        self.design = tk.StringVar(value=DESIGN_OPTIONS[0][0])
        self.qty = 1
        self.color = drink_color(product["name"])

        # ---- ซ้าย: พรีวิวแก้ว ----
        left = tk.Frame(self, bg=PANEL, width=310)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        brand_row(left, "CUSTOMIZE ME").pack(anchor="w", padx=26, pady=(22, 8))
        tk.Label(left, text=product["name"], bg=PANEL, fg=TEXT,
                 font=(FONT, 18, "bold"), wraplength=258,
                 justify="left").pack(anchor="w", padx=26)
        tk.Label(left, text=product.get("description") or "", bg=PANEL, fg=LATTE,
                 font=(FONT, 11), wraplength=258,
                 justify="left").pack(anchor="w", padx=26, pady=(4, 0))
        self.preview = tk.Canvas(left, width=self.PREVIEW_W, height=self.PREVIEW_H, bg=PANEL,
                                 highlightthickness=0)
        self.preview.pack(pady=(6, 0))
        self.sum_card = RoundFrame(left, fill=SURFACE_2, radius=14, pad=12)
        self.sum_card.pack(fill="x", padx=22, pady=(4, 0))
        self.summary = tk.Label(self.sum_card.inner, text="", bg=SURFACE_2, fg=TEXT,
                                font=(FONT, 11), wraplength=236, justify="center")
        self.summary.pack(fill="x")

        # ---- ขวา: ตัวเลือก ----
        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=28, pady=(18, 22))
        keep_centered(self, right, 560, min_pad=28, reserved=310)   # เต็มจอ: ตัวเลือกอยู่กลางพื้นที่ขวา

        self._section(right, "รูปแบบ")
        make_choice(right, temps, self.temp, self._update).pack(anchor="w")
        self._section(right, "ความหวาน")
        make_choice(right, SWEET_OPTIONS, self.sweet, self._update).pack(anchor="w")
        self._section(right, "ขนาดแก้ว")
        TilePicker(right, [s[0] for s in SIZE_OPTIONS], self.size, 104, 92,
                   draw_size_tile, self._update).pack(anchor="w")
        self._section(right, "ลายแก้ว")
        TilePicker(right, [d[0] for d in DESIGN_OPTIONS], self.design, 96, 156,
                   draw_design_tile, self._update).pack(anchor="w")
        # แถวล่าง: จำนวน (ซ้าย) + หมายเหตุถึงบาริสต้า (ขวา)
        last = tk.Frame(right, bg=BG)
        last.pack(fill="x")
        qty_col = tk.Frame(last, bg=BG)
        qty_col.pack(side="left", anchor="n")
        self._section(qty_col, "จำนวน")
        row = tk.Frame(qty_col, bg=BG)
        row.pack(anchor="w")
        make_qty_button(row, "-", lambda: self._change(-1)).pack(side="left")
        self.qty_label = tk.Label(row, text="1", width=3, bg=BG, fg=TEXT,
                                  font=(FONT, 14, "bold"))
        self.qty_label.pack(side="left")
        make_qty_button(row, "+", lambda: self._change(1)).pack(side="left")
        self.qty_hint_text = qty_hint or f"สูงสุด {MAX_CUPS_PER_MENU} แก้วต่อเมนู"
        self.qty_hint = tk.Label(qty_col, text=self.qty_hint_text, bg=BG, fg=TEXT_MUTED,
                                 font=(FONT, 9), wraplength=150, justify="left")
        self.qty_hint.pack(anchor="w", pady=(4, 0))

        note_col = tk.Frame(last, bg=BG)
        note_col.pack(side="left", fill="x", expand=True, padx=(30, 0), anchor="n")
        self._section(note_col, "หมายเหตุถึงบาริสต้า (ไม่บังคับ)")
        self.note_var = tk.StringVar()
        RoundEntry(note_col, height=40, size=11, textvariable=self.note_var).pack(fill="x")
        self.note_chips = tk.Frame(note_col, bg=BG)
        self.note_chips.pack(anchor="w", pady=(6, 0))
        self._chips_for = None
        self.note_var.trace_add("write", lambda *a: self._on_note())

        btns = tk.Frame(right, bg=BG)
        pack_bottom(btns, fill="x")                  # ปุ่มล่างได้พื้นที่ก่อน ไม่โดนตัดแม้จอเตี้ย
        make_button(btns, "ยกเลิก", self.destroy, primary=False).pack(
            side="left", padx=(0, 10))
        self.add_btn = make_button(btns, "", self._submit, height=48)
        self.add_btn.pack(side="left", expand=True, fill="x")

        self._update()
        w, h = 900, 730                          # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)
        grab_modal(self)

    def _section(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(14, 6))

    def _design_text(self):
        return next(d[2] for d in DESIGN_OPTIONS if d[0] == self.design.get())

    def _note(self):
        """หมายเหตุที่พิมพ์ (ตัดช่องว่างซ้ำออก)"""
        return " ".join(self.note_var.get().split())

    def _options_text(self):
        text = (f"{self.temp.get()}, {self.sweet.get()}, "
                f"ขนาด {self.size.get()}, {self._design_text()}")
        return text + (f", หมายเหตุ: {self._note()}" if self._note() else "")

    def _on_note(self):
        if len(self.note_var.get()) > NOTE_MAX:           # จำกัดความยาว
            self.note_var.set(self.note_var.get()[:NOTE_MAX])
            return
        self._update()

    def _add_note(self, text):
        """กดปุ่มลัด: เพิ่มข้อความต่อท้ายหมายเหตุ (ถ้ายังไม่มี)"""
        note = self._note()
        if text not in note:
            self.note_var.set(f"{note} / {text}" if note else text)

    def _render_note_chips(self):
        """ปุ่มลัดหมายเหตุ เปลี่ยนตามรูปแบบ (ร้อน/เย็น/ปั่น)"""
        key = "ร้อน" if self.temp.get() == "ร้อน" else "default"
        if key == self._chips_for:
            return
        self._chips_for = key
        for w in self.note_chips.winfo_children():
            w.destroy()
        for text in NOTE_CHIPS[key]:
            PillButton(self.note_chips, f"+ {text}", lambda t=text: self._add_note(t), "secondary",
                       height=30, size=9, padx=12).pack(side="left", padx=(0, 6))

    def unit_price(self):
        return self.product["price"] + SIZE_EXTRA[self.size.get()]

    def _draw_preview(self):
        """พรีวิวด้านซ้าย: รูปแก้วลายที่เลือก (ใหญ่/เล็กตามขนาดแก้ว) + ป้ายรูปแบบและขนาด"""
        c, W, H = self.preview, self.PREVIEW_W, self.PREVIEW_H
        size, temp, design = self.size.get(), self.temp.get(), self.design.get()
        c.delete("all")
        bottom = H - 12
        photo = load_cup_image(design, size)
        if photo is None:                  # ไม่มีรูปแก้ว: วาดแก้วการ์ตูนแทน
            args = (size, temp, design, self.color)
            crisp(c, 0, 0, W, H, lambda d: draw_cup_preview(d, W, H, *args), ("cup",) + args)
        else:
            pw, ph = photo.width(), photo.height()
            soft_glow(c, W / 2, bottom - ph * .45, 150, int(ph * .6), ACCENT, 34)
            aa_oval(c, W / 2 - pw * .62, bottom - 9, W / 2 + pw * .62, bottom + 7,
                    fill="#050505", outline="")                 # เงาใต้แก้ว
            c.create_image(W / 2, bottom, image=photo, anchor="s")
        # ป้ายบอกรูปแบบ (ซ้ายบน) และขนาดแก้ว (ขวาบน)
        oz = next(s[2] for s in SIZE_OPTIONS if s[0] == size)
        font = (FONT, 10, "bold")
        for text, fill, fg, side in ((temp, TEMP_BADGE.get(temp, LATTE), ACCENT_INK, "w"),
                                     (f"{size} · {oz} oz", SURFACE_2, TEXT, "e")):
            tw = text_width(text, font) + 22
            x0 = 2 if side == "w" else W - 2 - tw
            rounded_rect(c, x0, 4, x0 + tw, 30, 13, fill=fill, outline=fill)
            c.create_text(x0 + tw / 2, 17, text=text, fill=fg, font=font)

    def _update(self):
        self._draw_preview()
        self._render_note_chips()
        text = (f"{self.temp.get()}, {self.sweet.get()}, "
                f"ขนาด {self.size.get()}, {self._design_text()}")
        if self._note():
            text += f"\nหมายเหตุ: {self._note()}"
        self.summary.config(text=text)
        self.summary.update_idletasks()
        self.sum_card._fit()                   # ข้อความยาวขึ้น/สั้นลง ให้กรอบสรุปสูงตามเนื้อหา
        self.add_btn.config(
            text=f"เพิ่มลงตะกร้า  •  ฿{fmt_price(self.unit_price() * self.qty)}")

    def _change(self, delta):
        if delta > 0 and self.qty >= self.max_qty:          # ครบจำนวนที่สั่งได้แล้ว: เตือนสั้น ๆ
            self.qty_hint.config(text=f"สั่งได้สูงสุด {self.max_qty} แก้ว", fg=ERROR)
            if self._hint_job:
                self.after_cancel(self._hint_job)
            self._hint_job = self.after(1600, self._reset_hint)
            return
        self.qty = max(1, min(self.max_qty, self.qty + delta))
        self.qty_label.config(text=str(self.qty))
        self._update()

    def _reset_hint(self):
        self._hint_job = None
        self.qty_hint.config(text=self.qty_hint_text, fg=TEXT_MUTED)

    def destroy(self):
        if self._hint_job:                       # ยกเลิกตัวจับเวลาที่ค้างก่อนปิดหน้าต่าง
            self.after_cancel(self._hint_job)
            self._hint_job = None
        super().destroy()

    def _submit(self):
        self.on_add(self.product, self._options_text(), self.qty,
                    self.unit_price(), self.size.get())
        self.destroy()


# =====================================================================
# ส่วนที่ 12: รูปทรงและไอคอนหมวดหมู่
#   ประกอบด้วย: icon_all/cup/leaf/cake/star/soda, icon_for
#   แก้ที่นี่เมื่อ: เพิ่มไอคอนของหมวดหมู่ใหม่
# บรรทัด 1813 - 1877
# =====================================================================
def icon_all(c, cx, cy, col):
    for dx in (-12, 3):
        for dy in (-12, 3):
            c.create_rectangle(cx + dx, cy + dy, cx + dx + 10, cy + dy + 10,
                               fill=col, outline="")


def icon_cup(c, cx, cy, col):
    c.create_polygon(cx - 15, cy - 6, cx + 11, cy - 6, cx + 8, cy + 15,
                     cx - 12, cy + 15, fill=col, outline="")
    c.create_arc(cx + 5, cy - 3, cx + 19, cy + 10, start=270, extent=180,
                 style="arc", outline=col, width=3)
    for x in (cx - 8, cx + 1):
        c.create_line(x, cy - 11, x - 3, cy - 16, x + 3, cy - 21,
                      smooth=True, fill=col, width=2)


def icon_leaf(c, cx, cy, col):
    c.create_polygon(cx - 15, cy + 11, cx - 10, cy - 6, cx + 4, cy - 15,
                     cx + 15, cy - 13, cx + 13, cy + 2, cx, cy + 11,
                     smooth=True, fill=col, outline="")
    c.create_line(cx - 17, cy + 17, cx - 8, cy + 6, fill=col, width=3,
                  capstyle="round")


def icon_cake(c, cx, cy, col):
    c.create_rectangle(cx - 15, cy - 2, cx + 15, cy + 15, fill=col, outline="")
    c.create_line(cx, cy - 3, cx, cy - 12, fill=col, width=3)
    aa_oval(c, cx - 3, cy - 20, cx + 3, cy - 12, fill=col, outline="")


def icon_star(c, cx, cy, col):
    pts = []
    for i in range(10):
        r = 16 if i % 2 == 0 else 7
        a = -math.pi / 2 + i * math.pi / 5
        pts += [cx + r * math.cos(a), cy + r * math.sin(a)]
    c.create_polygon(pts, fill=col, outline="")


def icon_soda(c, cx, cy, col):
    c.create_polygon(cx - 13, cy - 8, cx + 13, cy - 8, cx + 9, cy + 17,
                     cx - 9, cy + 17, fill=col, outline="")
    c.create_line(cx + 3, cy - 21, cx + 8, cy - 5, fill=col, width=3,
                  capstyle="round")
    aa_oval(c, cx + 8, cy - 15, cx + 19, cy - 4, outline=col, width=2)


def icon_for(name):
    n = name.lower()
    if any(k in n for k in ("โซดา", "soda")):
        return icon_soda
    if any(k in n for k in ("ชา", "tea", "non")):
        return icon_leaf
    if any(k in n for k in ("เบเกอรี่", "bakery", "ขนม", "cake")):
        return icon_cake
    if any(k in n for k in ("special", "พิเศษ")):
        return icon_star
    return icon_cup


# =====================================================================
# ส่วนที่ 13: รูปเมนูและแบนเนอร์
#   ประกอบด้วย: load_product_image, รูปเมนูที่แอดมินอัปโหลด (make_menu_png, png_photo_fit),
#              load_meme_image (รูปมีมในโฟลเดอร์ images), load_art (รูปตกแต่งขนาดพอดี),
#              load_cup_image (รูปแก้วไดคัท), load_logo / draw_logo / logo_canvas / brand_row (โลโก้ร้าน),
#              draw_polaroid, draw_vine, draw_meme_face (หน้ามีมของร้าน), draw_meme_tile,
#              draw_meme_collage (หน้าล็อกอินแบบสติกเกอร์), draw_meme_collage_basic, draw_hero,
#              รูปโปรไฟล์ (make_avatar_png, avatar_photo, draw_avatar)
#   แก้ที่นี่เมื่อ: แก้รูปเมนู/รูปมีม/โลโก้ คำมีม (LOGIN_MEMES, HERO_MEMES) หรือหน้าตาแบนเนอร์
# บรรทัด 1880 - 2563
# =====================================================================
def load_product_image(product, w, h):
    """รูปเมนูในโฟลเดอร์ images: ตั้งชื่อไฟล์เป็นชื่อเมนู (เช่น Latte.png) หรือเลข product_id
    ย่อให้พอดีกรอบ w x h โดยไม่ตัดรูป (รูปพื้นใสจะกลืนกับการ์ด)  ไม่มีไฟล์คืนค่า None"""
    for stem in (product["name"], str(product["product_id"])):
        for ext in (".png", ".gif"):
            path = os.path.join(IMAGE_DIR, stem + ext)
            if not os.path.exists(path):
                continue
            key = ("product", path, os.path.getmtime(path), w, h)
            if key in _AA_CACHE:
                return _AA_CACHE[key]
            try:
                if HAS_PIL:
                    img = ImageOps.contain(Image.open(path).convert("RGBA"), (w, h), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                else:
                    photo = tk.PhotoImage(file=path)
                    factor = max(1, math.ceil(max(photo.width() / w, photo.height() / h) - .01))
                    if factor > 1:
                        photo = photo.subsample(factor)
            except (tk.TclError, OSError, ValueError):
                return None
            _AA_CACHE[key] = photo
            return photo
    return None


MENU_IMAGE_MAX = (600, 600)                 # รูปเมนูที่อัปโหลดย่อให้ไม่เกินนี้ (รูปเดิมของร้าน 372 x 392)
MENU_IMAGE_MAX_BYTES = 5 * 1024 * 1024


def make_menu_png(path):
    """อ่านรูปเมนูที่แอดมินเลือก -> ข้อมูลไฟล์ PNG (คงพื้นใสไว้ ย่อให้ไม่เกิน 600 x 600)
    มี Pillow เปิดได้ทั้ง jpg/png/gif/bmp/webp  ไม่มี Pillow ใช้ได้เฉพาะ png และ gif
    เปิดไม่ได้จะ raise ValueError พร้อมข้อความภาษาไทย"""
    max_w, max_h = MENU_IMAGE_MAX
    if HAS_PIL:
        try:
            img = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
            if img.width > max_w or img.height > max_h:
                img = ImageOps.contain(img, MENU_IMAGE_MAX, Image.LANCZOS)
        except (OSError, ValueError, Image.DecompressionBombError):
            raise ValueError("เปิดไฟล์รูปนี้ไม่ได้ ลองเลือกรูปอื่น") from None
        buf = io.BytesIO()
        img.save(buf, "PNG", optimize=True)
        png = buf.getvalue()
    else:
        ext = os.path.splitext(path)[1].lower()
        if ext not in (".png", ".gif"):
            raise ValueError("เครื่องนี้ใช้ได้เฉพาะรูป .png และ .gif\n(ติดตั้ง Pillow เพื่อใช้รูป .jpg)")
        try:
            photo = tk.PhotoImage(file=path)
            with open(path, "rb") as f:
                raw = f.read()
        except (tk.TclError, OSError):
            raise ValueError("เปิดไฟล์รูปนี้ไม่ได้ ลองเลือกรูปอื่น") from None
        if ext == ".png" and raw.startswith(b"\x89PNG") and photo.width() <= max_w and photo.height() <= max_h:
            png = raw                                       # ใช้ไฟล์เดิมเลย พื้นใสยังอยู่ครบ
        else:                                               # ต้องย่อ/แปลง: พื้นใสกลายเป็นสีการ์ดเมนู
            w, h, data = _photo_rgb(photo, DRINK_CARD)
            f = max(1, math.ceil(max(w / max_w, h / max_h)))
            if f > 1:
                w, h, data = _box_shrink(w, h, data, f)
            png = _encode_png(w, h, data)
    if len(png) > MENU_IMAGE_MAX_BYTES:
        raise ValueError("รูปใหญ่เกินไป (ไม่เกิน 5 MB)")
    return png


def png_photo_fit(png, w, h):
    """รูป PNG (ข้อมูลไฟล์) ย่อให้พอดีกรอบ w x h โดยไม่ตัด และคงพื้นใส  เปิดไม่ได้คืนค่า None
    (ใช้แสดงรูปเมนูที่เพิ่งเลือก ก่อนกดบันทึก)"""
    try:
        if HAS_PIL:
            img = ImageOps.contain(Image.open(io.BytesIO(png)).convert("RGBA"), (w, h), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        photo = _png_photo(png)
        f = max(1, math.ceil(max(photo.width() / w, photo.height() / h) - .01))
        return photo.subsample(f) if f > 1 else photo
    except (tk.TclError, OSError, ValueError):
        return None


def load_meme_image(name, w, h, radius=0):
    """รูปมีมของร้าน: images/<name>.png (หรือ .gif) ย่อแล้วตัดให้เต็มกรอบพอดี
    (มี Pillow จะคมกว่าและมุมมนตาม radius)  ถ้าไม่มีไฟล์คืนค่า None แล้วจะวาดหน้ามีมแทน
    ถ้ามีไฟล์ images/<name>_<w>x<h>.png (ย่อและตัดมุมไว้แล้ว) จะใช้ไฟล์นั้นทันที คมชัดแม้ไม่มี Pillow"""
    w, h = int(w), int(h)
    if w < 4 or h < 4:
        return None
    key = ("meme", name, w, h, radius)
    if key in _AA_CACHE:
        return _AA_CACHE[key]
    exact = load_art(f"{name}_{w}x{h}")          # มีไฟล์ย่อขนาดพอดีไว้แล้ว (เช่น meme_cart_250x250.png) ใช้เลย
    if exact is not None:
        _AA_CACHE[key] = exact
        return exact
    path = next((p for p in (os.path.join(IMAGE_DIR, name + ext) for ext in (".png", ".gif"))
                 if os.path.exists(p)), None)
    if path is None:
        return None
    try:
        if HAS_PIL:
            img = ImageOps.fit(Image.open(path).convert("RGBA"), (w, h), Image.LANCZOS)
            if radius:
                img = _round_corners(img, radius)
            photo = ImageTk.PhotoImage(img)
        else:
            src = tk.PhotoImage(file=path)
            src = _scale_photo(src, max(w / src.width(), h / src.height()), cover=True)
            cw, ch = min(w, src.width()), min(h, src.height())
            x0, y0 = (src.width() - cw) // 2, (src.height() - ch) // 2
            photo = tk.PhotoImage(width=cw, height=ch)
            photo.tk.call(photo, "copy", src, "-from", x0, y0, x0 + cw, y0 + ch, "-to", 0, 0)
    except (tk.TclError, OSError, ValueError):
        return None
    _AA_CACHE[key] = photo
    return photo


def _round_corners(img, radius):
    """ตัดมุมรูป (Pillow) ให้มนแบบเนียน"""
    w, h = img.size
    mask = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], radius * 4, fill=255)
    img.putalpha(mask.resize((w, h), Image.LANCZOS))
    return img


def load_art(name):
    """รูปตกแต่งที่ทำขนาดพอดีไว้แล้ว images/<name>.png (แสดงตามขนาดจริง ไม่ย่อ ไม่ตัด)
    ไม่ต้องมี Pillow ก็คมชัด  ไม่มีไฟล์คืนค่า None"""
    path = os.path.join(IMAGE_DIR, name + ".png")
    if not os.path.exists(path):
        return None
    key = ("art", path, os.path.getmtime(path))
    if key in _AA_CACHE:
        return _AA_CACHE[key]
    try:
        photo = ImageTk.PhotoImage(Image.open(path)) if HAS_PIL else tk.PhotoImage(file=path)
    except (tk.TclError, OSError, ValueError):
        return None
    _AA_CACHE[key] = photo
    return photo


def load_cup_image(key, size):
    """รูปแก้วไดคัทสำหรับพรีวิว: images/cup_<key>_<S/M/L>.png
    (ไม่มีไฟล์ตามขนาด จะย่อจาก cup_<key>.png ให้สูงตาม CUP_PREVIEW_H)  ไม่มีไฟล์เลยคืนค่า None"""
    photo = load_art(f"cup_{key}_{size}")
    if photo is not None:
        return photo
    h = CUP_PREVIEW_H.get(size, 340)
    path = os.path.join(IMAGE_DIR, f"cup_{key}.png")
    if not os.path.exists(path):
        return None
    ck = ("cup", key, h, os.path.getmtime(path))
    if ck in _AA_CACHE:
        return _AA_CACHE[ck]
    try:
        if HAS_PIL:
            img = Image.open(path).convert("RGBA")
            img = img.resize((max(1, round(img.width * h / img.height)), h), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        else:
            src = tk.PhotoImage(file=path)
            photo = _scale_photo(src, h / max(1, src.height()))
    except (tk.TclError, OSError, ValueError):
        return None
    _AA_CACHE[ck] = photo
    return photo


def _scale_photo(src, scale, cover=False):
    """ย่อ/ขยายรูปแบบไม่ใช้ Pillow (ประมาณสัดส่วนเป็นเศษส่วน zoom/subsample ไม่เกิน 6)
    cover=True เลือกสัดส่วนที่ไม่เล็กกว่าที่ขอ (ไว้ตัดให้เต็มกรอบ)"""
    options = [(z / sub, z, sub) for z in range(1, 7) for sub in range(1, 7)]
    if cover:
        options = [o for o in options if o[0] >= scale - 1e-6] or [max(options)]
    _, z, sub = min(options, key=lambda o: (abs(o[0] - scale), o[1]))
    if z == sub:
        return src
    dst = tk.PhotoImage()
    dst.tk.call(dst, "copy", src, "-zoom", z, z, "-subsample", sub, sub)
    return dst


# ---------- รูปโปรไฟล์สมาชิก ----------
AVATAR_SIZE = 576              # เก็บรูปโปรไฟล์เป็น PNG 576x576 (แสดงที่ 192 / 72 / 48 พิกเซล = ย่อ 3, 8, 12 เท่าพอดี)
AVATAR_SHOW = 192              # รูปใหญ่ในหน้าข้อมูลสมาชิก (ข้างการ์ดข้อมูล)
AVATAR_TYPES_PIL = ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.webp")
AVATAR_TYPES_TK = ("*.png", "*.gif")   # ไม่มี Pillow: tkinter เปิดได้เฉพาะ PNG กับ GIF


def _photo_rgb(photo, bg="#FFFFFF"):
    """พิกเซลของรูป tkinter เป็น bytes แบบ RGB เรียงทีละแถว (ส่วนโปร่งใสแทนด้วยสี bg)
    คืนค่า (กว้าง, สูง, พิกเซล)"""
    w, h = photo.width(), photo.height()
    try:
        raw = photo.tk.call(photo, "data", "-format", "ppm", "-background", bg)
    except tk.TclError:
        raw = None
    if not isinstance(raw, bytes):            # tkinter บางรุ่นส่งออกแบบนี้ไม่ได้: เขียนลงไฟล์ชั่วคราวแทน
        fd, path = tempfile.mkstemp(suffix=".ppm")
        os.close(fd)
        try:
            photo.tk.call(photo, "write", path, "-format", "ppm", "-background", bg)
            with open(path, "rb") as f:
                raw = f.read()
        finally:
            os.remove(path)
    return w, h, raw[len(raw) - w * h * 3:]   # ไฟล์ PPM = หัวไฟล์สั้น ๆ + พิกเซล RGB


def _box_shrink(w, h, data, n):
    """ย่อพิกเซล RGB ลง n เท่า โดยเฉลี่ยสีทีละบล็อก n x n
    (ภาพเนียนกว่า subsample ของ tkinter ที่แค่หยิบพิกเซลเว้นช่วง) คืนค่า (กว้าง, สูง, พิกเซล)"""
    ow, oh = w // n, h // n
    stride, area = w * 3, n * n
    out = bytearray()
    for oy in range(oh):
        acc = [0] * (ow * 3)
        for y in range(oy * n, oy * n + n):
            row = data[y * stride:y * stride + ow * n * 3]
            for dx in range(n):
                for ch in range(3):
                    acc[ch::3] = map(int.__add__, acc[ch::3], row[dx * 3 + ch::n * 3])
        out += bytes([(v + area // 2) // area for v in acc])
    return ow, oh, bytes(out)


def _encode_png(w, h, data, alpha=False, level=6, up_filter=False):
    """เขียนไฟล์ PNG จากพิกเซลดิบ (RGB หรือ RGBA เรียงทีละแถว) ด้วย Python ล้วน คืนค่า bytes
    up_filter=True: เก็บผลต่างจากแถวบน ไฟล์รูปถ่ายเล็กลงราวครึ่งหนึ่ง (ช้ากว่าเล็กน้อย ใช้ตอนบันทึก)"""
    n = w * (4 if alpha else 3)
    rows, prev = [], bytes(n)
    for y in range(h):
        row = data[y * n:(y + 1) * n]
        if up_filter:
            rows.append(b"\x02" + bytes([(a - b) & 255 for a, b in zip(row, prev)]))
            prev = row
        else:
            rows.append(b"\x00" + row)

    def chunk(tag, body):
        return (struct.pack(">I", len(body)) + tag + body
                + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))

    head = struct.pack(">IIBBBBB", w, h, 8, 6 if alpha else 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head)
            + chunk(b"IDAT", zlib.compress(b"".join(rows), level)) + chunk(b"IEND", b""))


def _png_photo(png):
    return tk.PhotoImage(data=base64.b64encode(png).decode("ascii"), format="png")


def _nearest_rgb(w, h, data, size):
    """ปรับพิกเซล RGB เป็น size x size แบบหยิบพิกเซลที่ใกล้ที่สุด (ใช้ปรับเศษที่เหลือหลังย่อแบบเฉลี่ยสีแล้ว)"""
    xs = [min(w - 1, int((j + .5) * w / size)) * 3 for j in range(size)]
    out = bytearray()
    for i in range(size):
        y = min(h - 1, int((i + .5) * h / size))
        row = data[y * w * 3:(y + 1) * w * 3]
        out += b"".join([row[x:x + 3] for x in xs])
    return bytes(out)


def _square_rgb(photo, size):
    """รูปสี่เหลี่ยมจัตุรัส -> พิกเซล RGB ขนาด size x size (ไม่ใช้ Pillow)
    ย่อด้วยการเฉลี่ยสีทีละบล็อก (ภาพเนียนไม่แตก) แล้วปรับเศษที่เหลือให้พอดีขนาด"""
    w = photo.width()
    if w < size:                                              # รูปเล็ก: ขยายก่อน
        photo = photo.zoom(math.ceil(size / w))
    elif w > 2400:                                            # รูปใหญ่มาก: ข้ามพิกเซลก่อน (เร็ว) แล้วค่อยเฉลี่ยสี
        photo = photo.subsample(math.ceil(w / 2400))
    w = photo.width()
    f = w // size
    if f == 1 and w != size:                                  # ใหญ่กว่าไม่ถึง 2 เท่า: ขยาย 2 เท่าก่อน จะได้เฉลี่ยสีได้
        photo = photo.zoom(2)
        f = 2 * w // size
    w, h, data = _photo_rgb(photo)
    if f > 1:
        w, h, data = _box_shrink(w, h, data, f)
    if w != size or h != size:
        data = _nearest_rgb(w, h, data, size)
    return data


def make_avatar_png(path):
    """อ่านไฟล์รูปที่เลือก -> ตัดเป็นสี่เหลี่ยมจัตุรัสตรงกลาง -> ย่อเป็น 576x576 -> คืนค่าข้อมูลไฟล์ PNG
    มี Pillow เปิดได้ทั้ง jpg/png/gif/bmp/webp  ไม่มี Pillow เปิดได้เฉพาะ png และ gif
    (ส่วนโปร่งใสในรูปจะเป็นพื้นขาว)  เปิดไม่ได้จะ raise ValueError พร้อมข้อความภาษาไทย"""
    if HAS_PIL:
        try:
            img = Image.open(path)
            img = ImageOps.exif_transpose(img)               # รูปจากมือถือ: หมุนให้ถูกทิศ
            img = img.convert("RGBA")
            flat = Image.new("RGB", img.size, "white")
            flat.paste(img, mask=img.getchannel("A"))
            img = ImageOps.fit(flat, (AVATAR_SIZE, AVATAR_SIZE), Image.LANCZOS)
        except (OSError, ValueError, Image.DecompressionBombError):
            raise ValueError("เปิดไฟล์รูปนี้ไม่ได้ ลองเลือกรูปอื่น") from None
        buf = io.BytesIO()
        img.save(buf, "PNG")
        return buf.getvalue()

    if os.path.splitext(path)[1].lower() not in (".png", ".gif"):
        raise ValueError("เครื่องนี้ใช้ได้เฉพาะรูป .png และ .gif\n"
                         "(ถ้าติดตั้ง Pillow จะใช้รูป .jpg ได้ด้วย: pip install pillow)")
    try:
        src = tk.PhotoImage(file=path)
    except tk.TclError:
        raise ValueError("เปิดไฟล์รูปนี้ไม่ได้ ลองเลือกรูปอื่น") from None
    w, h = src.width(), src.height()
    side = min(w, h)
    square = tk.PhotoImage()                                  # ตัดตรงกลางให้เป็นสี่เหลี่ยมจัตุรัส
    x0, y0 = (w - side) // 2, (h - side) // 2
    square.tk.call(square, "copy", src, "-from", x0, y0, x0 + side, y0 + side)
    data = _square_rgb(square, AVATAR_SIZE)
    return _encode_png(AVATAR_SIZE, AVATAR_SIZE, data, up_filter=True)


def _round_alpha(size, data, radius, inset=0.0):
    """พิกเซล RGB -> RGBA ตัดเป็นสี่เหลี่ยมมุมมนรัศมี radius (ห่างขอบรูป inset พิกเซล)
    รัศมีเท่าครึ่งหนึ่งของกรอบ = วงกลม  พิกเซลตรงขอบโปร่งแสงตามส่วนที่อยู่ในรูป ขอบจึงเนียนแม้ไม่มี Pillow"""
    out = bytearray(size * size * 4)
    for ch in range(3):
        out[ch::4] = data[ch::3]
    out[3::4] = b"\xff" * (size * size)
    lo, hi = inset + radius, size - inset - radius           # ช่วงที่จุดศูนย์กลางมุมโค้งเลื่อนได้
    for y in range(size):
        py = y + .5
        cy = min(max(py, lo), hi)
        for x in range(size):
            px = x + .5
            cx = min(max(px, lo), hi)
            if cx == px and cy == py:                         # อยู่ด้านในแน่นอน
                continue
            d = math.hypot(px - cx, py - cy) - radius         # ระยะออกนอกขอบ (ติดลบ = อยู่ในรูป)
            if d > -.5:
                out[(y * size + x) * 4 + 3] = int(max(0.0, min(1.0, .5 - d)) * 255 + .5)
    return bytes(out)


def avatar_photo(png, size, radius=None):
    """รูปโปรไฟล์ขนาด size x size จากข้อมูล PNG (นอกขอบโปร่งใส) เปิดไม่ได้คืนค่า None
    radius=None -> วงกลม (เล็กกว่ากรอบ 1 พิกเซล ให้เส้นขอบที่วาดทับปิดขอบรูปพอดี)
    radius=ตัวเลข -> สี่เหลี่ยมมุมมน (ใช้กับรูปใหญ่ในหน้าข้อมูลสมาชิก)"""
    key = ("avatar", hash(png), size, radius)
    if key in _AA_CACHE:
        return _AA_CACHE[key]
    try:
        if HAS_PIL:
            img = ImageOps.fit(Image.open(io.BytesIO(png)).convert("RGB"), (size, size), Image.LANCZOS)
            img = img.convert("RGBA")
            if radius is None:
                mask = Image.new("L", (size * 4, size * 4), 0)    # วาดวงกลมใหญ่แล้วย่อ ขอบจะเนียน
                ImageDraw.Draw(mask).ellipse((4, 4, size * 4 - 5, size * 4 - 5), fill=255)
                img.putalpha(mask.resize((size, size), Image.LANCZOS))
            else:
                img = _round_corners(img, radius)
            photo = ImageTk.PhotoImage(img)
        else:
            data = _square_rgb(_png_photo(png), size)
            rgba = (_round_alpha(size, data, size / 2 - 1, inset=1) if radius is None
                    else _round_alpha(size, data, radius))
            photo = _png_photo(_encode_png(size, size, rgba, alpha=True, level=1))
    except (tk.TclError, OSError, ValueError):
        return None
    _AA_CACHE[key] = photo
    return photo


def draw_avatar(c, size, member, ring=SURFACE_3, ring_width=2, photo_size=None, font_size=18):
    """วาดรูปโปรไฟล์วงกลมบน canvas ขนาด size x size
    มีรูป -> แสดงรูป / ยังไม่มี -> ตัวอักษรแรกของชื่อบนวงกลมสีน้ำตาล
    คืนค่า id ของวงขอบ (ใช้เปลี่ยนสีขอบตอนเอาเมาส์ชี้)"""
    c.delete("avatar")
    png = get_member_avatar(member["member_id"])
    photo = avatar_photo(png, photo_size or size - 4) if png else None
    if photo is None:
        aa_oval(c, 2, 2, size - 2, size - 2, fill=TAN, outline="", tags="avatar")
        c.create_text(size / 2, size / 2, text=member_initial(member["name"]),
                      font=(FONT, font_size, "bold"), fill=BLACK, tags="avatar")
    else:
        c.create_image(size / 2, size / 2, image=photo, tags="avatar")
        c.avatar_photo = photo                                # กันรูปถูกเก็บทิ้ง
    return aa_oval(c, 2, 2, size - 2, size - 2, fill="", outline=ring, width=ring_width, tags="avatar")


def load_logo(size):
    """โลโก้ร้าน images/logo.png ขนาด size x size
    (ไม่มี Pillow จะใช้ไฟล์ที่ย่อไว้แล้ว เช่น logo_56.png)  ไม่มีไฟล์คืนค่า None"""
    size = int(size)
    key = ("logo", size)
    if key in _AA_CACHE:
        return _AA_CACHE[key]
    big = os.path.join(IMAGE_DIR, "logo.png")
    exact = os.path.join(IMAGE_DIR, f"logo_{size}.png")
    photo = None
    try:
        if HAS_PIL and os.path.exists(big):
            img = Image.open(big).convert("RGBA").resize((size, size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        elif os.path.exists(exact):
            photo = tk.PhotoImage(file=exact)
        elif os.path.exists(big):
            photo = tk.PhotoImage(file=big)
            f = max(1, math.ceil(photo.width() / size))
            if f > 1:
                photo = photo.subsample(f)
    except (tk.TclError, OSError, ValueError):
        photo = None
    if photo is not None:
        _AA_CACHE[key] = photo
    return photo


def draw_logo(c, cx, cy, size):
    """วาดโลโก้ร้านบน canvas ที่จุดกึ่งกลาง (cx, cy)  ถ้าไม่มีไฟล์โลโก้จะวาดป้ายเหลืองรูปแก้วแทน"""
    photo = load_logo(size)
    if photo is not None:
        c.create_image(cx, cy, image=photo)
        return
    h = size / 2
    rounded_rect(c, cx - h, cy - h, cx + h, cy + h, max(6, int(size * .26)), fill=ACCENT,
                 outline=ACCENT)
    z = size / 50 * .85
    crisp(c, cx - h + 2, cy - h + 2, cx + h - 2, cy + h - 2,
          lambda d: icon_cup(d, cx / z, (cy + size * .04) / z, ACCENT_INK),
          ("logo_fb", size, cx % 1, cy % 1), zoom=z)


def logo_canvas(parent, size):
    """วิดเจ็ตโลโก้ร้านขนาด size x size (ใช้วางในแถบหัวของหน้าต่างต่างๆ)"""
    c = tk.Canvas(parent, width=size, height=size, bg=bg_of(parent), highlightthickness=0, bd=0)
    draw_logo(c, size / 2, size / 2, size)
    return c


def brand_row(parent, pill_text, fill=ACCENT, fg=ACCENT_INK, size=40):
    """แถวหัวของหน้าต่าง: โลโก้ร้าน + ป้ายชื่อหน้า"""
    row = tk.Frame(parent, bg=bg_of(parent))
    logo_canvas(row, size).pack(side="left")
    Pill(row, pill_text, fill, fg, size=9, height=22).pack(side="left", padx=(10, 0))
    return row


def draw_polaroid(c, x0, y0, w, name, caption, kind="smirk", tape=True):
    """รูปโพลารอยด์แปะผนัง (รูปมีม + คำบรรยายลายมือด้านล่าง) สูง = w + 32"""
    h = w + 32
    rounded_rect(c, x0 + 4, y0 + 6, x0 + w + 4, y0 + h + 6, 4, fill="#0B0B0B", outline="")
    rounded_rect(c, x0, y0, x0 + w, y0 + h, 3, fill="#F5F2EC", outline="")
    if tape:
        c.create_rectangle(x0 + w / 2 - 16, y0 - 7, x0 + w / 2 + 16, y0 + 7, fill="#D8CDB8",
                           outline="")
    photo = load_meme_image(name, w - 16, w - 16, radius=2)
    draw_meme_tile(c, x0 + 8, y0 + 8, x0 + w - 8, y0 + w - 8, kind, photo=photo, radius=2)
    c.create_text(x0 + w / 2, y0 + w + 8, text=caption, fill=BLACK, width=w - 8,
                  font=(FONT, 11, "bold"))


def draw_vine(c, x, length):
    """เถาไม้ห้อยจากขอบบน (ต้นไม้แขวนแบบคาเฟ่ปูนเปลือย)"""
    c.create_line(x, 2, x, length, fill="#3F5E32", width=2)
    for i, y in enumerate(range(16, length, 20)):
        col = "#4E7A3A" if i % 2 == 0 else "#62914A"
        if i % 2 == 0:
            aa_oval(c, x, y, x + 15, y + 9, fill=col, outline="")
        else:
            aa_oval(c, x - 15, y, x, y + 9, fill=col, outline="")


def draw_meme_face(c, cx, cy, r, kind, paper=CREAM, ink=BLACK):
    """หน้ามีมแบบของร้าน (วาดขึ้นเอง ไม่ได้ลอกจากรูปมีมของใคร)
    kind: tired (ง่วง) / hype (ตาเป็นดาว) / side_eye (มองค้อน) / cry_laugh (ขำจนน้ำตาไหล) / shock (ช็อก) / smirk (มาสคอตร้าน)"""
    w = max(2, int(r / 11))
    if kind == "smirk":
        draw_doodle(c, cx, cy, r, "logo", ink=ink, paper=paper)
        return
    aa_oval(c, cx - r, cy - r, cx + r, cy + r, fill=paper, outline=ink, width=w)

    def dot(x, y, d):
        aa_oval(c, x - d, y - d, x + d, y + d, fill=ink, outline="")

    if kind == "tired":
        for s in (-1, 1):
            ex, ey = cx + s * .38 * r, cy - .12 * r
            c.create_arc(ex - .2 * r, ey - .14 * r, ex + .2 * r, ey + .18 * r, start=180,
                         extent=180, fill=ink, outline=ink)
            c.create_line(ex - .24 * r, ey, ex + .24 * r, ey, fill=ink, width=w)
            c.create_arc(ex - .18 * r, ey + .14 * r, ex + .18 * r, ey + .32 * r, start=200,
                         extent=140, style="arc", outline="#8C8C8C", width=1)
        c.create_line(cx - .3 * r, cy + .48 * r, cx - .1 * r, cy + .42 * r, cx + .1 * r,
                      cy + .5 * r, cx + .3 * r, cy + .44 * r, smooth=True, fill=ink, width=w)
        c.create_text(cx + .95 * r, cy - .95 * r, text="z", fill=ink, font=(FONT, max(8, int(r * .32)), "bold"))
    elif kind == "hype":
        for s in (-1, 1):
            ex, ey, rr = cx + s * .38 * r, cy - .18 * r, .22 * r
            pts = []
            for i in range(10):
                rad = rr if i % 2 == 0 else rr * .45
                a = -math.pi / 2 + i * math.pi / 5
                pts += [ex + rad * math.cos(a), ey + rad * math.sin(a)]
            c.create_polygon(pts, fill=ACCENT, outline=ink, width=1)
        c.create_arc(cx - .52 * r, cy - .05 * r, cx + .52 * r, cy + .72 * r, start=180,
                     extent=180, fill=ink, outline=ink)
        c.create_arc(cx - .25 * r, cy + .3 * r, cx + .25 * r, cy + .66 * r, start=180,
                     extent=180, fill=PINK, outline="")
        for a in (-150, -30, -100, -80):
            rad = math.radians(a)
            c.create_line(cx + 1.12 * r * math.cos(rad), cy + 1.12 * r * math.sin(rad),
                          cx + 1.32 * r * math.cos(rad), cy + 1.32 * r * math.sin(rad),
                          fill=ACCENT, width=w)
    elif kind == "side_eye":
        for s in (-1, 1):
            ex, ey = cx + s * .36 * r, cy - .1 * r
            aa_oval(c, ex - .2 * r, ey - .12 * r, ex + .2 * r, ey + .12 * r, fill="white",
                          outline=ink, width=1)
            dot(ex + .1 * r, ey, .08 * r)
        c.create_line(cx - .58 * r, cy - .42 * r, cx - .16 * r, cy - .3 * r, fill=ink, width=w,
                      capstyle="round")
        c.create_line(cx + .16 * r, cy - .38 * r, cx + .58 * r, cy - .48 * r, fill=ink, width=w,
                      capstyle="round")
        c.create_line(cx - .25 * r, cy + .45 * r, cx + .3 * r, cy + .38 * r, fill=ink, width=w,
                      capstyle="round")
    elif kind == "cry_laugh":
        for s in (-1, 1):
            ex, ey = cx + s * .36 * r, cy - .16 * r
            c.create_arc(ex - .18 * r, ey - .1 * r, ex + .18 * r, ey + .22 * r, start=20,
                         extent=140, style="arc", outline=ink, width=w)
            tx = cx + s * .72 * r
            c.create_polygon(tx, cy - .02 * r, tx - .1 * r, cy + .22 * r, tx + .1 * r,
                             cy + .22 * r, fill="#7EC8F0", outline="")
            aa_oval(c, tx - .1 * r, cy + .14 * r, tx + .1 * r, cy + .34 * r, fill="#7EC8F0",
                          outline="")
        c.create_arc(cx - .5 * r, cy - .1 * r, cx + .5 * r, cy + .7 * r, start=180, extent=180,
                     fill=ink, outline=ink)
        c.create_rectangle(cx - .3 * r, cy + .3 * r, cx + .3 * r, cy + .38 * r, fill="white",
                           outline="")
    elif kind == "shock":
        for s in (-1, 1):
            ex, ey = cx + s * .36 * r, cy - .14 * r
            aa_oval(c, ex - .17 * r, ey - .19 * r, ex + .17 * r, ey + .19 * r, fill="white",
                          outline=ink, width=1)
            dot(ex, ey, .06 * r)
            c.create_arc(ex - .2 * r, ey - .52 * r, ex + .2 * r, ey - .22 * r, start=20,
                         extent=140, style="arc", outline=ink, width=w)
        aa_oval(c, cx - .14 * r, cy + .3 * r, cx + .14 * r, cy + .62 * r, fill=ink, outline="")
        c.create_polygon(cx + .78 * r, cy - .7 * r, cx + .7 * r, cy - .48 * r, cx + .86 * r,
                         cy - .48 * r, fill="#7EC8F0", outline="")


def is_thai(text):
    return any("฀" <= ch <= "๿" for ch in text)


def draw_meme_tile(c, x0, y0, x1, y1, kind, top="", bottom="", photo=None, radius=14,
                   place="split"):
    """การ์ดมีม 1 ช่อง: รูปมีม (หรือหน้ามีมที่วาดเอง ถ้าไม่มีรูป) + คำบรรยายแบบมีม
    place: "split" = คำบน/ล่าง, "top" = สองบรรทัดด้านบน, "bottom" = สองบรรทัดด้านล่าง"""
    rounded_rect(c, x0, y0, x1, y1, radius, fill="#1C1C1C", outline="")
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    if photo is not None:
        c.create_image(cx, (y0 + y1) / 2, image=photo)
    else:
        face_y = {"split": (y0 + y1) / 2, "top": y0 + h * .58, "bottom": y0 + h * .42}[place]
        r = int(min(w, h) * .24)
        soft_glow(c, cx, face_y, int(r * 2.6), int(r * 2.6), ACCENT, 34)
        crisp(c, cx - 1.5 * r, face_y - 1.5 * r, cx + 1.5 * r, face_y + 1.5 * r,
              lambda d: draw_meme_face(d, cx, face_y, r, kind),
              ("face", kind, r, cx % 1, face_y % 1))
    if place == "split":
        lines = ((top, y0 + 24), (bottom, y1 - 24))
    elif place == "top":
        lines = ((top, y0 + 24), (bottom, y0 + 52))
    else:
        lines = ((top, y1 - 52), (bottom, y1 - 24))
    for text, y in lines:
        if text:
            size = 16 if is_thai(text) else 20
            font = (FONT, size - 2, "bold") if is_thai(text) else (FONT_MEME, size)
            meme_text(c, cx, y, text.upper(), font=font, width=w - 14)


# มีมบนหน้าล็อกอิน: รูป images/meme1.png - meme4.png ตามลำดับ
# (หน้ามีมที่จะวาดแทนถ้าไม่มีรูป, คำบน, คำล่าง)
LOGIN_MEMES = [("tired", "ME BEFORE", "COFFEE"),
               ("hype", "ME AFTER", "COFFEE"),
               ("side_eye", "ขอกาแฟก่อน", "แล้วค่อยคุย"),
               ("smirk", "TRUST ME", "I'M A BARISTA")]
# มีมบนแบนเนอร์หน้าเมนู: รูป images/meme_hero1.png - meme_hero3.png (หน้าที่วาดแทน, คำใต้รูป)
HERO_MEMES = [("side_eye", "ไม่กินกาแฟ?"), ("hype", "coffee hits"), ("shock", "รอกาแฟอยู่")]


# ตำแหน่งสติกเกอร์มีมรอบโลโก้ (ซ้ายบน, ขวาบน, ซ้ายล่าง, ขวาล่าง)
LOGIN_STICKER_POS = [(-1, -1), (1, -1), (-1, 1), (1, 1)]


def draw_meme_collage(c, W, H):
    """แผงซ้ายหน้าล็อกอิน: พื้นลายเส้นมีม + โลโก้ร้านแบบสติกเกอร์ตรงกลาง + สติกเกอร์มีม 4 ใบรอบๆ
    รูปในโฟลเดอร์ images: login_pattern, login_glow_s/l, login_logo_s/l, login_sticker1-4_s/l
    (s = หน้าต่างปกติ, l = หน้าต่างใหญ่/เต็มจอ)  ถ้าไม่มีรูปพวกนี้จะใช้คอลลาจมีมแบบเดิม"""
    size = "l" if W >= 760 and H >= 760 else "s"
    stickers = [load_art(f"login_sticker{i}_{size}") for i in range(1, 5)]
    logo = load_art(f"login_logo_{size}")
    if logo is None or None in stickers:
        draw_meme_collage_basic(c, W, H)
        return
    pattern = load_art("login_pattern")          # ลายเส้นจางๆ ปูเต็มพื้น
    if pattern is not None:
        for y in range(0, int(H), pattern.height()):
            for x in range(0, int(W), pattern.width()):
                c.create_image(x, y, image=pattern, anchor="nw")
    cx, cy = W / 2, H / 2
    glow = load_art(f"login_glow_{size}")
    if glow is not None:
        c.create_image(cx, cy, image=glow)
    sw = max(p.width() for p in stickers)
    sh = max(p.height() for p in stickers)
    dx = min(W * .25, logo.width() / 2 + sw * .32)
    dy = min(H / 2 - sh / 2 - 8, logo.height() / 2 + sh * .32)
    for photo, (sx, sy) in zip(stickers, LOGIN_STICKER_POS):
        c.create_image(cx + sx * dx, cy + sy * dy, image=photo)
    c.create_image(cx, cy, image=logo)


def draw_meme_collage_basic(c, W, H):
    """คอลลาจมีม 2x2 + โลโก้ร้านตรงกลาง (ใช้เมื่อไม่มีรูปสติกเกอร์ของหน้าล็อกอิน)"""
    gap, m = 6, 8
    tw, th = (W - 2 * m - gap) / 2, (H - 2 * m - gap) / 2
    for i, (kind, top, bottom) in enumerate(LOGIN_MEMES):
        x0 = m + (i % 2) * (tw + gap)
        y0 = m + (i // 2) * (th + gap)
        photo = load_meme_image(f"meme{i + 1}", int(tw), int(th), radius=14)
        draw_meme_tile(c, x0, y0, x0 + tw, y0 + th, kind, top, bottom, photo,
                       place="top" if i < 2 else "bottom")
    cx, cy = W / 2, H / 2
    size = 240 if min(W, H) > 760 else 184        # จอใหญ่ โลโก้ใหญ่ขึ้น
    soft_glow(c, cx, cy, size + 160, size + 160, ACCENT, 44)
    edge = size / 2 + 7                            # ขอบดำรอบโลโก้ ให้แยกจากรูปมีม
    rounded_rect(c, cx - edge, cy - edge, cx + edge, cy + edge, int(size * .25), fill=PANEL,
                 outline=PANEL)
    draw_logo(c, cx, cy, size)


def draw_hero(c, W, H):
    """แบนเนอร์หน้าเมนู: ผนังมืด + แสงไฟนุ่ม + ต้นไม้แขวน + คำมีม + รูปโพลารอยด์มีม 3 ใบ
    (กว้างตามหน้าต่าง: รูปโพลารอยด์ชิดขวาเสมอ)"""
    c.delete("all")
    rounded_rect(c, 0, 0, W, H, 22, fill=SURFACE, outline=LINE)
    # หน้าต่างแคบ (เช่น แบ่งจอกับหน้าแอดมิน): ลดจำนวนโพลารอยด์ ไม่ให้บังข้อความด้านซ้าย
    text_end = 36 + max(text_width("WHEN THE COFFEE HITS DIFFERENT", (FONT_MEME, 22)),
                        text_width("สั่งล่วงหน้า รับหน้าร้าน", (FONT, 26, "bold")))
    count = max(0, min(len(HERO_MEMES), (W - 24 - text_end - 70) // 132))
    right = W - 24 - 132 * count                # จุดเริ่มกลุ่มโพลารอยด์ (3 ใบ = W - 420 เหมือนเดิม)
    soft_glow(c, right + 200, 70, 420, 170, LATTE, 46)
    soft_glow(c, 170, H - 40, 360, 120, ACCENT, 18)
    if count:
        for x, ln in ((right - 64, 96), (right - 42, 58), (right - 20, 80)):
            draw_vine(c, x, ln)
    # ซ้าย: ข้อความ (จัดกึ่งกลางแนวตั้งของแบนเนอร์)
    c.create_text(36, 64, anchor="w", text="สั่งล่วงหน้า รับหน้าร้าน", fill=TEXT,
                  font=(FONT, 26, "bold"))
    meme_text(c, 36, 110, "WHEN THE COFFEE HITS DIFFERENT", font=(FONT_MEME, 22),
              fill=ACCENT, anchor="w")
    c.create_text(36, 150, anchor="w", text="ไม่ต้องรอคิว  •  Coffee + Meme = Happiness",
                  fill=TEXT_MUTED, font=(FONT, 11))
    # ขวา: โพลารอยด์ 3 ใบ (ระดับสูงต่ำต่างกันนิดหน่อยให้ดูเหมือนแปะผนัง)
    for i, (kind, caption) in enumerate(HERO_MEMES[:count]):
        draw_polaroid(c, right + i * 132, (22, 34, 16)[i], 118, f"meme_hero{i + 1}", caption, kind)


# =====================================================================
# ส่วนที่ 14: วิดเจ็ตย่อยของหน้าเมนู
#   ประกอบด้วย: section_header, section_title, category_label (หัวข้อ), SearchBox + search_text (ค้นหาเมนู),
#              HScrollRow (แถวเลื่อนซ้าย-ขวา), CartButton (ไอคอนตะกร้า)
#   แก้ที่นี่เมื่อ: แก้หัวข้อ ช่องค้นหา (คำไทยที่ค้นได้: SEARCH_ALIASES) แถวเมนูแนะนำ หรือไอคอนตะกร้า
# บรรทัด 2566 - 2737
# =====================================================================
def section_header(parent, text):
    bg = bg_of(parent)
    f = tk.Frame(parent, bg=bg)
    bar = tk.Canvas(f, width=6, height=24, bg=bg, highlightthickness=0)
    rounded_rect(bar, 0, 0, 6, 24, 3, fill=ACCENT, outline=ACCENT)
    bar.pack(side="left", padx=(0, 10))
    lbl = tk.Label(f, text=text, bg=bg, fg=TEXT, font=(FONT, 15, "bold"))
    lbl.pack(side="left")
    return f, lbl


CATEGORY_EN = {"กาแฟ": "Coffee", "ชา": "Tea", "โซดา": "Soda"}


def category_label(name):
    """ชื่อหมวดแบบ "กาแฟ (Coffee)" """
    en = CATEGORY_EN.get(name)
    return f"{name} ({en})" if en else name


def section_title(parent, text, icon, note=""):
    """หัวข้อส่วน: ไอคอนสีเหลือง + ชื่อ + ข้อความเล็ก (วางเส้นคั่นต่อท้ายเองได้)"""
    bg = bg_of(parent)
    f = tk.Frame(parent, bg=bg)
    ic = tk.Canvas(f, width=28, height=28, bg=bg, highlightthickness=0)
    ic.pack(side="left")
    crisp(ic, 0, 0, 28, 28, lambda d: icon(d, 14 / .6, 15 / .6, ACCENT),
          ("section", icon.__name__), zoom=.6)
    tk.Label(f, text=text, bg=bg, fg=TEXT, font=(FONT, 15, "bold")).pack(side="left", padx=(8, 0))
    if note:
        tk.Label(f, text=note, bg=bg, fg=TEXT_MUTED, font=(FONT, 11)).pack(side="left",
                                                                          padx=(8, 0), pady=(4, 0))
    return f


# คำค้นภาษาไทย -> ชื่อเมนูภาษาอังกฤษ (พิมพ์ "ลาเต้" ก็เจอ Latte)
SEARCH_ALIASES = {
    "อเมริกาโน่": "americano", "ลาเต้": "latte", "เอสเปรสโซ่": "espresso", "กาแฟเย็น": "thai iced coffee",
    "มอคค่า": "mocha", "คาปูชิโน่": "cappuccino", "คาราเมล": "caramel", "มัคคิอาโต้": "macchiato",
    "กาแฟส้ม": "orange coffee", "ดริป": "drip", "ชาไทย": "thai tea", "ชาเย็น": "thai tea",
    "ชาเขียว": "green tea", "ชามะนาว": "lemon tea", "เลมอน": "lemon", "มะนาว": "lemon",
    "พีช": "peach", "มัทฉะ": "matcha", "บลู": "blue", "สตรอเบอร์รี่": "strawberry",
    "เสาวรส": "passion", "แพชชั่น": "passion", "ส้ม": "orange",
    "ชานม": "milk tea", "น้ำผึ้ง": "honey", "โฮจิฉะ": "hojicha", "ลิ้นจี่": "lychee", "เผือก": "taro",
    "แอปเปิ้ล": "apple", "แอปเปิล": "apple", "มะม่วง": "mango", "บลูเบอร์รี่": "blueberry",
    "แดงมะนาว": "red lime", "น้ำแดง": "red lime",
}


def search_text(product, category=""):
    """ข้อความทั้งหมดที่ใช้ค้นหาเมนู (ชื่อ คำอธิบาย หมวด และคำไทยที่ตรงกับชื่อ)"""
    name = product["name"].lower()
    thai = [th for th, en in SEARCH_ALIASES.items() if en in name]
    return " ".join([name, (product.get("description") or "").lower(), category.lower()] + thai)


class SearchBox(RoundEntry):
    """ช่องค้นหามุมมน: ไอคอนแว่นขยาย + ข้อความจางๆ บอกว่าค้นอะไรได้ + ปุ่ม × ล้างคำค้น
    on_change(คำค้น) ถูกเรียกทุกครั้งที่พิมพ์"""

    def __init__(self, parent, placeholder, on_change, width=300, height=42):
        self.sb_var = tk.StringVar()
        super().__init__(parent, height=height, width=width, radius=height // 2, size=11,
                         textvariable=self.sb_var)
        self.sb_change = on_change
        self.sb_ph = tk.Label(self, text=placeholder, bg=self.re_fill, fg=TEXT_MUTED,
                              font=(FONT, 11), cursor="xterm")
        self.sb_ph.bind("<Button-1>", lambda e: self.entry.focus_set())
        cy = height / 2
        crisp(self, 12, cy - 11, 34, cy + 11, lambda d: self._icon(d, 22, cy), ("search_icon", height))
        self.tag_bind("clear", "<Button-1>", lambda e: self.clear())
        self.tag_bind("clear", "<Enter>", lambda e: self.config(cursor="hand2"))
        self.tag_bind("clear", "<Leave>", lambda e: self.config(cursor=""))
        self.entry.bind("<Escape>", lambda e: (self.clear(), "break")[1])
        self.sb_var.trace_add("write", lambda *a: self._changed())

    @staticmethod
    def _icon(c, cx, cy):
        aa_oval(c, cx - 7, cy - 7, cx + 4, cy + 4, outline=TEXT_MUTED, width=2)
        c.create_line(cx + 3, cy + 3, cx + 8, cy + 8, fill=TEXT_MUTED, width=2, capstyle="round")

    def get(self):
        return self.sb_var.get().strip()

    def clear(self):
        self.sb_var.set("")
        self.entry.focus_set()

    def _changed(self):
        self._paint()
        self.sb_change(self.get())

    def _paint(self):
        super()._paint()
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4:
            w, h = int(self.cget("width")), int(self.cget("height"))
        has_text = bool(self.sb_var.get())
        self.itemconfig(self.re_win, width=max(w - 40 - (34 if has_text else 14), 10))
        self.coords(self.re_win, 40, h / 2)
        self.delete("clear")
        if has_text or self.re_active:          # กำลังพิมพ์: ซ่อนข้อความจาง ให้เห็นเคอร์เซอร์
            self.sb_ph.place_forget()
        if has_text:
            self.create_text(w - 20, h / 2, text="×", fill=TEXT_MUTED, font=(FONT, 15, "bold"),
                             tags="clear")
        if not has_text and not self.re_active:
            self.sb_ph.place(x=40, rely=0.5, anchor="w")


class HScrollRow(tk.Frame):
    """แถวเลื่อนซ้าย-ขวา (ใช้กับ 'เมนูแนะนำ')"""

    def __init__(self, parent, bg, height):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, height=height,
                                highlightthickness=0, xscrollincrement=1)
        self.hs_pending = 0
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.pack(fill="x")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

    def scroll(self, direction):
        """เลื่อนไป 1 การ์ด แบบค่อยๆ เลื่อน"""
        start = self.hs_pending == 0
        self.hs_pending += direction * 204
        if start:
            self._glide()

    def _glide(self):
        if not self.winfo_exists() or self.hs_pending == 0:
            self.hs_pending = 0
            return
        step = int(self.hs_pending * 0.25) or (1 if self.hs_pending > 0 else -1)
        self.canvas.xview_scroll(step, "units")
        self.hs_pending -= step
        self.after(12, self._glide)


class CartButton(tk.Canvas):
    """ไอคอนตะกร้ามุมขวาบน พร้อมตัวเลขจำนวนสินค้า"""

    def __init__(self, parent, command):
        super().__init__(parent, width=62, height=56, bg=PANEL,
                         highlightthickness=0, cursor="hand2")
        self.bind("<Button-1>", lambda e: command())
        self.bg_item = rounded_rect(self, 4, 8, 50, 54, 14, fill=SURFACE_2, outline=SURFACE_2)
        self.bind("<Enter>", lambda e: restyle(self, self.bg_item, fill=SURFACE_3, outline=SURFACE_3))
        self.bind("<Leave>", lambda e: restyle(self, self.bg_item, fill=SURFACE_2, outline=SURFACE_2))
        self.create_line(13, 20, 18, 20, 22, 36, 40, 36, fill=CREAM, width=2,
                         joinstyle="round", capstyle="round")
        self.create_polygon(20, 24, 42, 24, 39, 33, 22, 33, fill=CREAM, outline="")
        aa_oval(self, 22, 40, 27, 45, fill=CREAM, outline="")
        aa_oval(self, 35, 40, 40, 45, fill=CREAM, outline="")
        self.badge = aa_oval(self, 38, 1, 60, 23, fill=PINK, outline=PANEL,
                                      width=2, state="hidden")
        self.badge_text = self.create_text(49, 12, text="0", fill="white",
                                           font=(FONT, 11, "bold"), state="hidden")

    def set_count(self, n):
        state = "normal" if n else "hidden"
        self.itemconfig(self.badge, state=state)
        self.itemconfig(self.badge_text, state=state, text=str(min(n, 99)))


# =====================================================================
# ส่วนที่ 15: หน้าต่างตะกร้า
#   ประกอบด้วย: class CartDialog: รายการในตะกร้า ปรับจำนวน ยืนยันสั่งซื้อ
#   แก้ที่นี่เมื่อ: แก้หน้าตาหรือปุ่มในหน้าต่างตะกร้า
# บรรทัด 2740 - 2875
# =====================================================================
class CartDialog(tk.Toplevel):
    """หน้าต่างตะกร้า: ปรับจำนวน ลบรายการ และยืนยันสั่งซื้อ"""

    def __init__(self, parent, page):
        super().__init__(parent)
        self.page = page
        self.title("ตะกร้าของคุณ")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        head = tk.Frame(self, bg=BG)
        head.pack(fill="x", padx=22, pady=(18, 8))
        logo_canvas(head, 40).pack(side="left", padx=(0, 12))
        tk.Label(head, text="ตะกร้าของคุณ", bg=BG, fg=TEXT,
                 font=(FONT, 17, "bold")).pack(side="left")
        self.count_pill = Pill(head, "", ACCENT, ACCENT_INK)
        self.count_pill.pack(side="left", padx=10)

        bottom = tk.Frame(self, bg=BG)
        bottom.pack(side="bottom", fill="x", padx=22, pady=(10, 20))
        self._notice_job = None
        self.notice = tk.Label(bottom, text="", bg=BG, fg=ERROR, font=(FONT, 10, "bold"),
                               wraplength=410, justify="left")
        self.notice.pack(anchor="w")
        total_row = tk.Frame(bottom, bg=BG)
        total_row.pack(fill="x", pady=(0, 12))
        tk.Label(total_row, text="ยอดรวม", bg=BG, fg=TEXT_MUTED,
                 font=(FONT, 11)).pack(side="left")
        self.total_label = tk.Label(total_row, text="", bg=BG, fg=TEXT,
                                    font=(FONT, 18, "bold"))
        self.total_label.pack(side="right")
        make_button(bottom, "ยืนยันการสั่งซื้อ",
                    lambda: page.checkout(self), height=48).pack(fill="x")
        make_button(bottom, "ล้างตะกร้า", page.clear_cart,
                    primary=False).pack(fill="x", pady=(8, 0))
        make_divider(self, LINE)

        self.area = ScrollFrame(self, BG)
        self.area.pack(fill="both", expand=True, padx=(16, 4))
        self.render()

        self.win_w = 460
        self.win_h = self._fit_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.win_w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.win_h) // 2
        self.win_x, self.win_y = max(x, 0), max(y, 0)
        self.geometry(f"{self.win_w}x{self.win_h}+{self.win_x}+{self.win_y}")
        grab_modal(self)

    def _fit_height(self):
        """ความสูงหน้าต่างตามจำนวนรายการ (สูงสุด 580)"""
        n = len(self.page.cart.items)
        if n == 0:
            return 640                     # มีรูปมีมตอนตะกร้าว่าง
        return 640 if n > 3 else max(440, 318 + 124 * n)

    def show_notice(self, text):
        """ข้อความเตือนใต้รายการ (เช่น สั่งเกิน 10 แก้ว) หายไปเองหลัง 4 วินาที"""
        self.notice.config(text=text)
        if self._notice_job:
            self.after_cancel(self._notice_job)
        self._notice_job = self.after(4000, self._clear_notice)

    def _clear_notice(self):
        self._notice_job = None
        self.notice.config(text="")

    def destroy(self):
        if self._notice_job:                     # ยกเลิกตัวจับเวลาที่ค้างก่อนปิดหน้าต่าง
            self.after_cancel(self._notice_job)
            self._notice_job = None
        super().destroy()

    def render(self):
        page = self.page
        inner = self.area.inner
        for w in inner.winfo_children():
            w.destroy()
        full = page.full_menus()                 # เมนูที่ในตะกร้าครบจำนวนที่สั่งได้แล้ว

        if page.cart.is_empty():
            empty = tk.Canvas(inner, width=250, height=250, bg=BG, highlightthickness=0)
            empty.pack(pady=(24, 8))
            photo = load_meme_image("meme_cart", 250, 250, radius=18)
            if photo is not None:                       # images/meme_cart.png
                empty.create_image(125, 125, image=photo)
            else:
                draw_meme_tile(empty, 0, 0, 250, 250, "tired", "ME WHEN", "ตะกร้าว่าง")
            tk.Label(inner, text="ตะกร้ายังว่างอยู่เลย", bg=BG, fg=TEXT,
                     font=(FONT, 13, "bold")).pack()
            tk.Label(inner, text="ชีวิตก็ต้องมีกาแฟบ้าง เลือกเมนูได้เลย", bg=BG, fg=TEXT_MUTED,
                     font=(FONT, 11)).pack(pady=(2, 10))

        for idx, it in enumerate(page.cart.items):
            card = RoundFrame(inner, fill=SURFACE, border=LINE, radius=16, pad=14)
            card.pack(fill="x", padx=(6, 10), pady=(10, 0))
            row = card.inner

            top = tk.Frame(row, bg=SURFACE)
            top.pack(fill="x")
            tk.Label(top, text=it["name"], bg=SURFACE, fg=TEXT,
                     font=(FONT, 12, "bold"), wraplength=280, justify="left",
                     anchor="w").pack(side="left", fill="x", expand=True)
            LinkButton(top, "ลบ", lambda i=idx: page.remove_item(i), fg=TEXT_MUTED,
                       hover=ERROR, size=9, bold=True).pack(side="right")

            tk.Label(row, text=it["options"], bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 11),
                     wraplength=330, justify="left").pack(anchor="w", pady=(2, 0))

            line = tk.Frame(row, bg=SURFACE)
            line.pack(fill="x", pady=(8, 0))
            make_qty_button(line, "-", lambda i=idx: page.change_qty(i, -1), 30
                            ).pack(side="left")
            tk.Label(line, text=str(it["qty"]), width=3, bg=SURFACE, fg=TEXT,
                     font=(FONT, 11, "bold")).pack(side="left")
            make_qty_button(line, "+", lambda i=idx: page.change_qty(i, 1), 30
                            ).pack(side="left")
            if it["product_id"] in full:
                tk.Label(line, text=full[it["product_id"]], bg=SURFACE, fg=ACCENT,
                         font=(FONT, 9, "bold")).pack(side="left", padx=(8, 0))
            tk.Label(line, text=f"฿{fmt_price(it['price'] * it['qty'])}",
                     bg=SURFACE, fg=TEXT,
                     font=(FONT, 13, "bold")).pack(side="right")

        self.count_pill.set_text(f"{page.cart.count()} รายการ")
        self.total_label.config(text=f"฿{fmt_price(page.cart.total())}")
        if hasattr(self, "win_h"):                       # ปรับความสูงเมื่อเพิ่ม/ลดรายการ
            self.win_h = self._fit_height()
            self.geometry(f"{self.win_w}x{self.win_h}+{self.win_x}+{self.win_y}")


# =====================================================================
# ส่วนที่ 16: หน้าชำระเงิน
#   ประกอบด้วย: draw_pay_tile, load_qr_image, สลิปโอนเงิน (make_slip_png, slip_photo), draw_status_icon,
#              class PaymentDialog (เลือกวิธีชำระ: เงินสด / QR + แนบสลิป -> ยืนยัน -> รอร้านตรวจสลิป
#              -> แจ้งผล + ส่งใบเสร็จ)
#   แก้ที่นี่เมื่อ: เพิ่มวิธีชำระเงิน แก้หน้าตาหน้าชำระเงิน ขั้นตอนแนบสลิป หรือหน้าแจ้งผลหลังชำระเสร็จ
# บรรทัด 2878 - 3755
# =====================================================================
def draw_pay_tile(c, key, sel):
    """การ์ดเลือกวิธีชำระเงิน (ไอคอนวาดด้วยโค้ด)"""
    fg = tile_fg(sel)
    if key == "cash":
        c.create_rectangle(28, 18, 84, 50, outline=fg, width=3)
        aa_oval(c, 46, 25, 66, 43, outline=fg, width=2)
        aa_oval(c, 33, 30, 38, 35, fill=fg, outline="")
        aa_oval(c, 74, 33, 79, 38, fill=fg, outline="")
        label = "เงินสด"
    else:                                             # qr
        for x, y in ((32, 16), (58, 16), (32, 42)):
            c.create_rectangle(x, y, x + 22, y + 22, outline=fg, width=3)
            c.create_rectangle(x + 7, y + 7, x + 15, y + 15, fill=fg, outline="")
        for x, y in ((60, 44), (72, 44), (66, 52), (74, 56), (58, 58)):
            c.create_rectangle(x, y, x + 6, y + 6, fill=fg, outline="")
        label = "QR พร้อมเพย์"
    c.create_text(56, 72, text=label, fill=fg, font=(FONT, 11, "bold"))


QR_SIZE = 198                 # ขนาดรูป QR บนหน้าชำระเงิน (images/qr.png ทำไว้ขนาดนี้พอดี คมชัดสแกนง่าย)


def load_qr_image(size=QR_SIZE):
    """โหลดรูป QR พร้อมเพย์ของร้านจาก images/qr.png (หรือ .gif)
    ถ้ารูปใหญ่กว่า size จะย่อให้พอดีโดยไม่ตัดขอบ  ไม่มีไฟล์คืนค่า None"""
    for ext in (".png", ".gif"):
        path = os.path.join(IMAGE_DIR, "qr" + ext)
        if not os.path.exists(path):
            continue
        key = ("qr", path, os.path.getmtime(path), size)
        if key in _AA_CACHE:
            return _AA_CACHE[key]
        try:
            if HAS_PIL:
                img = Image.open(path).convert("RGB")
                if max(img.size) > size:
                    img = ImageOps.contain(img, (size, size), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
            else:
                photo = tk.PhotoImage(file=path)
                big = max(photo.width(), photo.height())
                if big > size:
                    photo = _scale_photo(photo, size / big)
        except (tk.TclError, OSError, ValueError):
            return None
        _AA_CACHE[key] = photo
        return photo
    return None


# ---------- สลิปโอนเงิน (จ่ายด้วย QR ต้องแนบสลิป แล้วรอแอดมินยืนยัน) ----------
SLIP_MAX_SIDE = (1000, 1600)    # ย่อรูปสลิปให้กว้าง/สูงไม่เกินนี้ก่อนเก็บ (ยังอ่านตัวเลขได้ชัด ไฟล์ไม่ใหญ่)


def make_slip_png(path):
    """อ่านรูปสลิปที่เลือก -> ย่อให้ไม่เกิน 1000x1600 -> คืนค่าข้อมูลไฟล์ PNG
    มี Pillow เปิดได้ทั้ง jpg/png/gif/bmp/webp  ไม่มี Pillow เปิดได้เฉพาะ png และ gif
    เปิดไม่ได้จะ raise ValueError พร้อมข้อความภาษาไทย"""
    max_w, max_h = SLIP_MAX_SIDE
    if HAS_PIL:
        try:
            img = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
            flat = Image.new("RGB", img.size, "white")     # ส่วนโปร่งใส -> พื้นขาว
            flat.paste(img, mask=img.getchannel("A"))
            flat.thumbnail((max_w, max_h), Image.LANCZOS)
        except (OSError, ValueError, Image.DecompressionBombError):
            raise ValueError("เปิดไฟล์รูปนี้ไม่ได้ ลองเลือกรูปอื่น") from None
        buf = io.BytesIO()
        flat.save(buf, "PNG")
        png = buf.getvalue()
    else:
        if os.path.splitext(path)[1].lower() not in (".png", ".gif"):
            raise ValueError("เครื่องนี้ใช้ได้เฉพาะรูป .png และ .gif\n"
                             "(แคปหน้าจอสลิปจากมือถือเป็น .png ได้เลย  หรือติดตั้ง Pillow เพื่อใช้ .jpg)")
        try:
            photo = tk.PhotoImage(file=path)
        except tk.TclError:
            raise ValueError("เปิดไฟล์รูปนี้ไม่ได้ ลองเลือกรูปอื่น") from None
        w, h, data = _photo_rgb(photo)
        f = max(1, math.ceil(max(w / max_w, h / max_h)))
        if f > 1:                                        # ย่อแบบเฉลี่ยสี ตัวหนังสือบนสลิปไม่แตก
            w, h, data = _box_shrink(w, h, data, f)
        png = _encode_png(w, h, data)
    if len(png) > SLIP_MAX_BYTES:
        raise ValueError("รูปสลิปใหญ่เกินไป ลองแคปหน้าจอสลิปใหม่")
    return png


def slip_photo(png, max_w, max_h):
    """รูปสลิปย่อให้พอดีกรอบ max_w x max_h (ไม่ตัดขอบ) เปิดไม่ได้คืนค่า None"""
    if not png:
        return None
    key = ("slip", hash(png), max_w, max_h)
    if key in _AA_CACHE:
        return _AA_CACHE[key]
    try:
        if HAS_PIL:
            img = ImageOps.contain(Image.open(io.BytesIO(png)).convert("RGB"), (max_w, max_h),
                                   Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        else:
            photo = _png_photo(png)
            f = max(1, math.ceil(max(photo.width() / max_w, photo.height() / max_h)))
            if f > 1:
                w, h, data = _box_shrink(*_photo_rgb(photo), f)
                photo = _png_photo(_encode_png(w, h, data, level=1))
    except (tk.TclError, OSError, ValueError):
        return None
    _AA_CACHE[key] = photo
    return photo


def draw_status_icon(c, kind):
    """วงกลมสถานะขนาด 84x84: "ok" ติ๊กถูก / "wait" นาฬิกาทราย / "bad" เครื่องหมายตกใจ"""
    ring, fill = {"ok": ("#3A3415", ACCENT), "wait": ("#3A3415", ACCENT),
                  "bad": ("#3E1C19", ERROR)}[kind]
    aa_oval(c, 1, 1, 83, 83, fill=ring, outline="")
    aa_oval(c, 11, 11, 73, 73, fill=fill, outline="")
    if kind == "ok":
        crisp(c, 0, 0, 84, 84, lambda d: d.create_line(28, 43, 38, 53, 57, 32, fill=ACCENT_INK,
                                                        width=6, capstyle="round",
                                                        joinstyle="round"), ("check",))
    elif kind == "wait":
        c.create_line(32, 27, 52, 27, fill=ACCENT_INK, width=4, capstyle="round")
        c.create_line(32, 57, 52, 57, fill=ACCENT_INK, width=4, capstyle="round")
        c.create_polygon(34, 29, 50, 29, 42, 42, fill=ACCENT_INK, outline="")
        c.create_polygon(42, 42, 34, 55, 50, 55, fill="", outline=ACCENT_INK, width=2)
        c.create_polygon(42, 47, 37, 55, 47, 55, fill=ACCENT_INK, outline="")
    else:
        c.create_text(42, 42, text="!", fill="white", font=(FONT, 30, "bold"))


class PaymentDialog(tk.Toplevel):
    """ขั้นตอนชำระเงิน: เลือกวิธีชำระ -> ยืนยัน -> แจ้งผล + ส่งใบเสร็จทางอีเมล
    เงินสด: ยืนยันแล้วชำระสำเร็จทันที
    QR พร้อมเพย์: ต้องแนบสลิปก่อนจึงกดยืนยันได้ -> รอแอดมินตรวจสลิป (หน้านี้เช็กผลให้อัตโนมัติ)
        แอดมินยืนยัน -> ชำระสำเร็จ (ร้านส่งใบเสร็จให้)  /  สลิปไม่ผ่าน -> แนบสลิปใหม่ หรือยกเลิกออเดอร์
    ออเดอร์ถูกสร้างเป็น pending ก่อนเปิดหน้านี้ ถ้าปิดหน้าต่าง/กดยกเลิกก่อนส่งสลิปจะเปลี่ยนเป็น cancelled
    resume=True: เปิดดูสถานะออเดอร์ที่ส่งสลิปไปแล้ว (จากแถบแจ้งเตือนบนหน้าเมนู)"""
    POLL_MS = 1500                # เช็กผลการตรวจสลิปทุก 1.5 วินาที

    def __init__(self, parent, page, order_id, cart_dialog=None, resume=False):
        super().__init__(parent)
        self.page = page
        self.order_id = order_id
        self.cart_dialog = cart_dialog
        self.paid = False
        self.submitted = False        # ส่งสลิปแล้ว (ปิดหน้านี้ก็ไม่ยกเลิกออเดอร์)
        self._closed = False
        self._poll_job = None
        try:
            self._build_dialog(parent, page, order_id, resume)
        except Exception:
            # สร้างหน้าไม่สำเร็จ: ห้ามทิ้งหน้าต่างเปล่าค้างไว้ และยกเลิกออเดอร์ที่ยังไม่จ่าย
            self._closed = True
            cancel_order(order_id)
            tk.Toplevel.destroy(self)
            raise

    def _build_dialog(self, parent, page, order_id, resume=False):
        self.receipt = get_order_receipt(order_id)
        self.subtotal = self.receipt["total_price"]       # ราคาสินค้าก่อนลด
        self.discount = 0                                  # ส่วนลดที่เลือกใช้ (บาท)
        self.percent = 0
        self.total = self.subtotal                         # ราคาหลังหักส่วนลด (ก่อนบวกภาษี)
        self.vat, self.grand = vat_split(self.total)       # ภาษีมูลค่าเพิ่ม, ยอดที่ต้องชำระจริง
        self.coupon_id = None
        self.coupons = get_unused_coupons(page.member["member_id"])
        self.coupon_var = tk.StringVar(value="")           # "" = ไม่ใช้ส่วนลด / ไม่งั้นเป็นรหัส เช่น D25
        self.slip_png = None                               # รูปสลิปที่แนบ (PNG) ใช้กับ QR พร้อมเพย์
        self.slip_email = None                             # อีเมลที่ให้ร้านส่งใบเสร็จหลังยืนยันสลิป
        self._send_result = None
        self.extra = {}
        self.title(f"ชำระเงิน - ออเดอร์ {order_code(order_id)}")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        w, h = 900, 724                          # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)

        self.method = tk.StringVar(value="cash")
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True)
        if resume:
            self._resume()
        else:
            self.show_choose()
        self.update_idletasks()
        try:
            grab_modal(self)
        except tk.TclError:           # บางเครื่อง grab ตอนหน้าต่างยังไม่แสดงจะ error -> ข้ามได้
            pass

    def destroy(self):
        """ปิดหน้าต่าง: ถ้ายังไม่ชำระเงิน (และยังไม่ส่งสลิป) จะยกเลิกออเดอร์ แล้วคืนโฟกัสให้หน้าต่างตะกร้า"""
        if self._closed:
            return
        self._closed = True
        if self._poll_job:
            self.after_cancel(self._poll_job)
            self._poll_job = None
        if not self.paid and not self.submitted:
            cancel_order(self.order_id)
        super().destroy()
        try:
            cd = self.cart_dialog
            if cd is not None and cd.winfo_exists():
                grab_modal(cd)
        except tk.TclError:           # ปิดโปรแกรมทั้งหมดอยู่ (หน้าต่างถูกทำลายไปแล้ว)
            pass

    # ---------- ขั้นที่ 1: เลือกวิธีชำระเงิน ----------
    def show_choose(self):
        for w in self.body.winfo_children():
            w.destroy()

        # ซ้าย: สรุปรายการ
        left = tk.Frame(self.body, bg=PANEL, width=330)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        brand_row(left, "สรุปคำสั่งซื้อ", SURFACE_2, ACCENT).pack(anchor="w", padx=26, pady=(22, 8))
        tk.Label(left, text=f"ออเดอร์ {order_code(self.order_id)}", bg=PANEL, fg=TEXT,
                 font=(FONT, 18, "bold")).pack(anchor="w", padx=26)

        bottom = tk.Frame(left, bg=PANEL)
        bottom.pack(side="bottom", fill="x", padx=26, pady=24)
        tk.Frame(bottom, bg=LINE, height=1).pack(fill="x", pady=(0, 12))
        self.sum_rows = tk.Frame(bottom, bg=PANEL)          # ราคาสินค้า / ส่วนลด / ภาษี 7%
        self.sum_rows.pack(fill="x")
        tk.Label(bottom, text="ยอดที่ต้องชำระ", bg=PANEL, fg=LATTE,
                 font=(FONT, 11)).pack(anchor="w", pady=(6, 0))
        self.lbl_total = tk.Label(bottom, text="", bg=PANEL, fg=TEXT,
                                  font=(FONT, 32, "bold"))
        self.lbl_total.pack(anchor="w")
        self.lbl_points = tk.Label(bottom, text="", bg=PANEL, fg=SUCCESS,
                                   font=(FONT, 11, "bold"))
        self.lbl_points.pack(anchor="w")

        items = ScrollFrame(left, PANEL)
        items.pack(fill="both", expand=True, padx=(20, 4), pady=(14, 0))
        for n, it in enumerate(self.receipt["items"]):
            if n:
                tk.Frame(items.inner, bg=LINE, height=1).pack(fill="x", padx=6, pady=(10, 0))
            row = tk.Frame(items.inner, bg=PANEL)
            row.pack(fill="x", padx=6, pady=(10, 0))
            top = tk.Frame(row, bg=PANEL)
            top.pack(fill="x")
            Pill(top, f"{it['quantity']}×", SURFACE_2, TEXT, size=9, height=20,
                 padx=7).pack(side="left", padx=(0, 8))
            tk.Label(top, text=it["name"], bg=PANEL, fg=TEXT,
                     font=(FONT, 11, "bold"), wraplength=160, justify="left",
                     anchor="w").pack(side="left")
            tk.Label(top, text=f"฿{fmt_price(it['quantity'] * it['unit_price'])}",
                     bg=PANEL, fg=TEXT, font=(FONT, 11, "bold")).pack(side="right")
            tk.Label(row, text=it["options"] or "", bg=PANEL, fg=LATTE, font=(FONT, 9),
                     wraplength=260, justify="left").pack(anchor="w", pady=(3, 0))

        # ขวา: เลือกวิธีชำระเงิน
        right = tk.Frame(self.body, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=28, pady=(20, 22))
        keep_centered(self.body, right, 600, min_pad=28, reserved=330)   # เต็มจอ: อยู่กลางพื้นที่ขวา
        tk.Label(right, text="เลือกวิธีชำระเงิน", bg=BG, fg=TEXT,
                 font=(FONT, 17, "bold")).pack(anchor="w")
        TilePicker(right, [k for k, _ in PAYMENT_METHODS], self.method, 112, 90,
                   draw_pay_tile, self._render_method).pack(anchor="w", pady=(10, 0))
        self.method_box = tk.Frame(right, bg=BG)
        self.method_box.pack(fill="x", pady=(14, 0))

        # ส่วนลด: เลือกใช้ส่วนลดที่แลกแต้มไว้ (1 ใบต่อ 1 ออเดอร์)
        tk.Label(right, text="ส่วนลด", bg=BG, fg=TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(14, 6))
        self.coupon_box = tk.Frame(right, bg=BG)
        self.coupon_box.pack(fill="x")
        self._render_coupons()

        # ส่วนใบเสร็จอีเมล
        member = self.page.member
        tk.Label(right, text="ใบเสร็จทางอีเมล", bg=BG, fg=TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(14, 4))
        self.send_var = tk.BooleanVar(value=True)
        tk.Checkbutton(right, text="ส่งใบเสร็จไปที่อีเมลนี้หลังชำระเงิน",
                       variable=self.send_var, bg=BG, activebackground=BG,
                       fg=TEXT, selectcolor=SURFACE_2, font=(FONT, 11), bd=0,
                       highlightthickness=0, cursor="hand2").pack(anchor="w")
        email_box = RoundEntry(right, height=42)
        email_box.pack(fill="x", pady=(6, 0))
        self.email_entry = email_box.entry
        self.email_entry.insert(0, member.get("email") or "")
        self.save_email_var = tk.BooleanVar(value=True)
        if not member.get("email"):
            tk.Checkbutton(right, text="บันทึกอีเมลนี้ไว้ในข้อมูลสมาชิก",
                           variable=self.save_email_var, bg=BG,
                           activebackground=BG, fg=TEXT_MUTED,
                           selectcolor=SURFACE_2, font=(FONT, 11), bd=0,
                           highlightthickness=0, cursor="hand2").pack(anchor="w")

        btns = tk.Frame(right, bg=BG)
        pack_bottom(btns, fill="x")                  # ปุ่มล่างได้พื้นที่ก่อน ไม่โดนตัดแม้จอเตี้ย
        self.msg = tk.Label(right, text="", bg=BG, fg=ERROR, font=(FONT, 11))
        self.msg.pack(side="bottom", anchor="w", pady=(0, 6), after=btns)
        make_button(btns, "ยกเลิก", self.destroy, primary=False).pack(
            side="left", padx=(0, 10))
        self.confirm_btn = make_button(btns, "", self.confirm, height=48)
        self.confirm_btn.pack(side="left", expand=True, fill="x")

        self._render_method()
        self._refresh_totals()

    def _draw_coupon_tile(self, c, key, sel):
        """การ์ดเลือกส่วนลด: '' = ไม่ใช้ส่วนลด, ไม่งั้นเป็นรหัสส่วนลด (กลุ่มคูปองประเภทเดียวกัน)"""
        fg = tile_fg(sel)
        if key == "":
            c.create_text(78, 29, text="ไม่ใช้ส่วนลด", fill=fg, font=(FONT, 11, "bold"))
            return
        group = [x for x in self.coupons if x["reward_code"] == key]
        pct = group[0]["percent"]
        amount = discount_amount(self.subtotal, pct)
        c.create_text(78, 19, text=f"ลด {pct}%" + (f"  ×{len(group)}" if len(group) > 1 else ""),
                      fill=fg, font=(FONT, 12, "bold"))
        c.create_text(78, 40, text=f"-฿{fmt_price(amount)}  →  ฿{fmt_price(self.subtotal - amount)}",
                      fill=tile_sub(sel), font=(FONT, 11))

    def _apply_coupon(self):
        """คำนวณส่วนลด/ยอดสุทธิจากส่วนลดที่เลือก (ไม่แตะหน้าจอ)"""
        code = self.coupon_var.get()
        self.coupon_id, self.percent = None, 0
        group = [x for x in self.coupons if x["reward_code"] == code]
        if code and group:
            self.coupon_id, self.percent = group[0]["coupon_id"], group[0]["percent"]
        else:
            self.coupon_var.set("")
        self.discount = discount_amount(self.subtotal, self.percent)
        self.total = self.subtotal - self.discount
        self.vat, self.grand = vat_split(self.total)

    def _on_coupon_change(self):
        """เลือก/ยกเลิกส่วนลด: คำนวณยอดใหม่ แล้วรีเฟรชหน้าจอ"""
        self._apply_coupon()
        self._refresh_totals()
        self._render_method()

    def _render_coupons(self):
        """วาดส่วน 'ส่วนลด': ส่วนลดที่แลกไว้ให้เลือกใช้ + ปุ่มแลกส่วนลดด้วยแต้ม"""
        box = self.coupon_box
        for w in box.winfo_children():
            w.destroy()
        member = self.page.member
        self.coupons = get_unused_coupons(member["member_id"])
        codes = sorted({c["reward_code"] for c in self.coupons},
                       key=lambda k: REWARD_BY_CODE[k][1])
        self._apply_coupon()
        if codes:
            TilePicker(box, [""] + codes, self.coupon_var, 156, 58,
                       self._draw_coupon_tile, self._on_coupon_change).pack(anchor="w")
        else:
            tk.Label(box, text="ยังไม่มีส่วนลดที่แลกไว้", bg=BG, fg=TEXT_MUTED,
                     font=(FONT, 11)).pack(anchor="w")
        fresh = get_member(member["member_id"])
        if fresh:
            member.update(fresh)
        LinkButton(box, f"+ แลกส่วนลดด้วยแต้ม   (แต้มคงเหลือ {member['points']:,})",
                   self._open_points, fg=ACCENT, hover=TEXT, size=10,
                   bold=True).pack(anchor="w", pady=(8, 0))

    def _open_points(self):
        """เปิดหน้าแต้มเพื่อแลกส่วนลด พอปิดแล้วกลับมาเลือกใช้ส่วนลดที่เพิ่งแลกได้ทันที"""
        dlg = PointsDialog(self, self.page.member, self.page.refresh_header)
        self.wait_window(dlg)
        if self._closed:
            return
        try:
            grab_modal(self)
        except tk.TclError:
            pass
        self._render_coupons()
        self._refresh_totals()
        self._render_method()

    def _money_rows(self):
        """แถวแจกแจงยอด (ราคาสินค้า / ส่วนลด / ยอดก่อนภาษี / ภาษี 7%) ใช้ชุดเดียวกับใบเสร็จ"""
        a = {"subtotal": self.subtotal, "discount": self.discount, "net": self.total,
             "vat": self.vat, "paid": self.grand, "included": VAT_INCLUDED_IN_PRICE}
        return money_rows(a, f"ส่วนลด {self.percent}%")

    def _refresh_totals(self):
        for w in self.sum_rows.winfo_children():
            w.destroy()
        for label, value in self._money_rows():
            color = SUCCESS if label.startswith("ส่วนลด") else LATTE
            row = tk.Frame(self.sum_rows, bg=PANEL)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=label, bg=PANEL, fg=color, font=(FONT, 11)).pack(side="left")
            tk.Label(row, text=value, bg=PANEL, fg=color, font=(FONT, 11, "bold")).pack(side="right")
        self.lbl_total.config(text=f"฿{fmt_price(self.grand)}")
        self.lbl_points.config(text=f"จะได้รับ {int(self.total // BAHT_PER_POINT)} แต้มสะสม")
        self._update_confirm()

    def _update_confirm(self):
        """ปุ่มยืนยัน: จ่ายด้วย QR ต้องแนบสลิปก่อนจึงจะกดได้"""
        if self.method.get() == "qr" and not self.slip_png:
            self.confirm_btn.config(text="แนบสลิปก่อน จึงจะยืนยันการชำระเงินได้", state="disabled")
            return
        label = "ส่งสลิปและยืนยันการชำระเงิน" if self.method.get() == "qr" else "ยืนยันการชำระเงิน"
        self.confirm_btn.config(text=f"{label}  •  ฿{fmt_price(self.grand)}", state="normal")

    def _render_method(self):
        """แสดงรายละเอียดตามวิธีชำระเงินที่เลือก"""
        box = self.method_box
        for w in box.winfo_children():
            w.destroy()
        m = self.method.get()

        if m == "cash":
            tk.Label(box, text="รับเงินจากลูกค้า (บาท)", bg=BG, fg=TEXT,
                     font=(FONT, 11, "bold")).pack(anchor="w")
            row = tk.Frame(box, bg=BG)
            row.pack(fill="x", pady=(4, 0))
            self.cash_var = tk.StringVar(value=fmt_price(self.grand))
            cash_box = RoundEntry(row, height=42, width=140, textvariable=self.cash_var,
                                  font=(FONT, 14, "bold"))
            cash_box.pack(side="left")
            self.cash_entry = cash_box.entry
            for text, val in (("พอดี", self.grand), ("100", 100), ("500", 500),
                              ("1,000", 1000)):
                PillButton(row, text, lambda v=val: self.cash_var.set(fmt_price(v)),
                           "secondary", height=36, size=10, padx=14).pack(side="left", padx=(8, 0))
            self.change_label = tk.Label(box, text="", bg=BG, font=(FONT, 12, "bold"))
            self.change_label.pack(anchor="w", pady=(8, 0))
            self.cash_var.trace_add("write", lambda *a: self._update_change())
            self._update_change()
        elif m == "qr":
            photo = load_qr_image()
            side = (max(photo.width(), photo.height()) if photo is not None else 150) + 16
            c = tk.Canvas(box, width=side, height=side, bg=BG, highlightthickness=0)
            c.pack(side="left")
            if photo is not None:            # การ์ดพื้นขาว ให้แอปธนาคารสแกนได้ง่าย
                rounded_rect(c, 1, 1, side - 1, side - 1, 16, fill="white", outline="white")
                c.create_image(side / 2, side / 2, image=photo)
                c.photo = photo
            else:
                rounded_rect(c, 1, 1, side - 1, side - 1, 16, fill=SURFACE, outline=LINE)
                rounded_rect(c, 12, 12, side - 12, side - 12, 12, fill="", outline=TEXT_MUTED,
                             dash=(5, 4), width=2)
                c.create_text(side / 2, side / 2, text="วางรูป QR ของร้านที่\nimages/qr.png",
                              fill=TEXT_MUTED, font=(FONT, 11), justify="center")
            info = tk.Frame(box, bg=BG)
            info.pack(side="left", padx=(18, 0), anchor="n")
            badge = load_art("promptpay")            # images/promptpay.png
            if badge is not None:
                tk.Label(info, image=badge, bg=BG, bd=0).pack(anchor="w", pady=(2, 6))
            tk.Label(info, text="สแกนจ่ายผ่านพร้อมเพย์", bg=BG, fg=TEXT,
                     font=(FONT, 12, "bold")).pack(anchor="w")
            tk.Label(info, text=f"ยอดที่ต้องโอน  ฿{fmt_price(self.grand)}", bg=BG, fg=ACCENT,
                     font=(FONT, 18, "bold")).pack(anchor="w")
            tk.Label(info, text="โอนแล้วแนบสลิป ร้านตรวจสลิปแล้วจึงชำระสำเร็จ",
                     bg=BG, fg=TEXT_MUTED, font=(FONT, 10), justify="left").pack(anchor="w")
            self.slip_box = tk.Frame(info, bg=BG)
            self.slip_box.pack(anchor="w", pady=(8, 0))
            self._render_slip()
        self._update_confirm()

    # ---------- แนบสลิป (QR พร้อมเพย์) ----------
    def _render_slip(self):
        """รูปย่อสลิป + ปุ่มแนบ/เปลี่ยนสลิป"""
        box = self.slip_box
        for w in box.winfo_children():
            w.destroy()
        th = tk.Canvas(box, width=58, height=80, bg=BG, highlightthickness=0, cursor="hand2")
        th.pack(side="left")
        th.bind("<Button-1>", lambda e: self.choose_slip())
        photo = slip_photo(self.slip_png, 58, 80) if self.slip_png else None
        if photo is not None:
            th.create_image(29, 40, image=photo)
            th.photo = photo
        else:
            rounded_rect(th, 1, 1, 57, 79, 8, fill="", outline=TEXT_MUTED, dash=(4, 3), width=2)
            th.create_text(29, 40, text="สลิป", fill=TEXT_MUTED, font=(FONT, 10, "bold"))
        col = tk.Frame(box, bg=BG)
        col.pack(side="left", padx=(10, 0))
        if self.slip_png:
            tk.Label(col, text="แนบสลิปแล้ว", bg=BG, fg=SUCCESS,
                     font=(FONT, 11, "bold")).pack(anchor="w")
        else:
            tk.Label(col, text="ยังไม่ได้แนบสลิป *", bg=BG, fg=ERROR,
                     font=(FONT, 11, "bold")).pack(anchor="w")
        PillButton(col, "เปลี่ยนรูปสลิป" if self.slip_png else "แนบสลิปการโอน", self.choose_slip,
                   "secondary" if self.slip_png else "primary", height=34, size=10,
                   padx=14).pack(anchor="w", pady=(6, 0))

    def _pick_slip_file(self):
        """เลือกไฟล์สลิป แล้วแปลงเป็น PNG  ยกเลิก/เปิดไม่ได้คืนค่า None"""
        patterns = AVATAR_TYPES_PIL if HAS_PIL else AVATAR_TYPES_TK
        path = filedialog.askopenfilename(parent=self, title="เลือกรูปสลิปการโอนเงิน",
                                          filetypes=[("รูปภาพ", " ".join(patterns)), ("ทุกไฟล์", "*.*")])
        if not path:
            return None
        self.config(cursor="watch")
        self.update_idletasks()
        try:
            return make_slip_png(path)
        except ValueError as e:
            messagebox.showerror("ใช้รูปนี้ไม่ได้", str(e), parent=self)
            return None
        finally:
            self.config(cursor="")

    def choose_slip(self):
        png = self._pick_slip_file()
        if png is None or self._closed:
            return
        self.slip_png = png
        self.msg.config(text="")
        self._render_slip()
        self._update_confirm()

    def _parse_cash(self):
        try:
            return float(self.cash_var.get().replace(",", "").strip())
        except ValueError:
            return None

    def _update_change(self):
        v = self._parse_cash()
        if v is None:
            self.change_label.config(text="กรอกจำนวนเงินเป็นตัวเลข", fg=ERROR)
        elif v + 1e-9 < self.grand:
            self.change_label.config(
                text=f"ยังไม่ครบ ขาดอีก ฿{fmt_price(round(self.grand - v, 2))}", fg=ERROR)
        else:
            self.change_label.config(text=f"เงินทอน ฿{fmt_price(round(v - self.grand, 2))}",
                                     fg=SUCCESS)

    def confirm(self):
        method = self.method.get()
        label = dict(PAYMENT_METHODS)[method]
        extra = {}
        if method == "cash":
            v = self._parse_cash()
            if v is None or v + 1e-9 < self.grand:
                self.msg.config(text="จำนวนเงินที่รับยังไม่ครบตามยอดที่ต้องชำระ")
                return
            extra = {"received": v, "change": round(v - self.grand, 2)}
        elif not self.slip_png:
            self.msg.config(text="กรุณาแนบสลิปการโอนเงินก่อนกดยืนยัน")
            return
        email = self.email_entry.get().strip()
        want_email = self.send_var.get()
        if want_email and not is_valid_email(email):
            self.msg.config(text="รูปแบบอีเมลไม่ถูกต้อง (หรือเอาเครื่องหมายส่งใบเสร็จออก)")
            return
        if method == "qr":
            self._submit_slip(email, want_email)
            return

        try:
            result = mark_order_paid(self.order_id, label, self.coupon_id)
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"บันทึกการชำระเงินไม่สำเร็จ\n{e}", parent=self)
            return
        self.paid = True
        self.method_label = label
        self.result = result
        self.extra = extra

        member = self.page.member
        if email and is_valid_email(email) and not member.get("email") and self.save_email_var.get():
            set_member_email(member["member_id"], email)
        self.page.on_paid()                       # ล้างตะกร้า + รีเฟรชแต้มและระดับสมาชิก
        cd = self.cart_dialog
        if cd is not None and cd.winfo_exists():
            cd.destroy()
        self.show_done(email, want_email)

    def _submit_slip(self, email, want_email):
        """ส่งสลิปให้ร้านตรวจ: ออเดอร์ยังรอชำระ แต่ล้างตะกร้าได้แล้ว แล้วไปหน้ารอผล"""
        try:
            submit_payment_slip(self.order_id, self.slip_png, self.grand, self.coupon_id,
                                email if want_email else None)
        except ValueError as e:
            self.msg.config(text=str(e))
            return
        self.submitted = True
        self.slip_email = email if want_email else None
        member = self.page.member
        if email and is_valid_email(email) and not member.get("email") and self.save_email_var.get():
            set_member_email(member["member_id"], email)
        self.page.on_paid()                       # ล้างตะกร้า + แสดงแถบ "รอร้านตรวจสลิป" บนหน้าเมนู
        cd = self.cart_dialog
        if cd is not None and cd.winfo_exists():
            cd.destroy()
        self.show_waiting()

    def _resume(self):
        """เปิดดูออเดอร์ที่ส่งสลิปไปแล้ว: รอตรวจ / ไม่ผ่าน / ร้านยืนยันแล้ว"""
        st = get_payment_state(self.order_id)
        slip = st["slip"] if st else None
        if slip is None:
            self.show_choose()
            return
        self.submitted = True
        self.grand = slip["amount"]
        self.coupon_id = slip["coupon_id"]
        self.slip_email = slip["email"]
        self.slip_png = get_slip_image(slip["slip_id"])
        if st["status"] == "paid":
            self._slip_approved(st)
        elif st["status"] == "cancelled":
            self.show_cancelled()
        elif slip["status"] == "rejected":
            self.show_rejected(slip["note"])
        else:
            self.show_waiting()

    def _center_box(self, width=470):
        for w in self.body.winfo_children():
            w.destroy()
        box = tk.Frame(self.body, bg=BG)
        box.place(relx=0.5, rely=0.5, anchor="center", width=width)
        return box

    # ---------- ส่งสลิปแล้ว: รอร้านตรวจ ----------
    def show_waiting(self):
        """รอแอดมินตรวจสลิป (เช็กผลจากฐานข้อมูลเองทุก 1.5 วินาที)"""
        box = self._center_box()
        icon = tk.Canvas(box, width=84, height=84, bg=BG, highlightthickness=0)
        icon.pack()
        draw_status_icon(icon, "wait")
        tk.Label(box, text="ส่งสลิปแล้ว รอร้านตรวจสอบ", bg=BG, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(pady=(6, 0))
        tk.Label(box, text=f"ออเดอร์ {order_code(self.order_id)}  •  ยอดโอน ฿{fmt_price(self.grand)}",
                 bg=BG, fg=TEXT_MUTED, font=(FONT, 11)).pack()
        tk.Label(box, text="HOLD ON...  THE BARISTA IS CHECKING", bg=BG, fg=ACCENT,
                 font=(FONT_MEME, 14)).pack(pady=(6, 0))
        photo = slip_photo(self.slip_png, 170, 250) if self.slip_png else None
        if photo is not None:
            pic = tk.Label(box, image=photo, bg=BG, bd=0)
            pic.image = photo
            pic.pack(pady=(14, 0))
        self.wait_status = tk.Label(box, text="กำลังรอร้านยืนยันการชำระเงิน", bg=BG, fg=ACCENT,
                                    font=(FONT, 12, "bold"))
        self.wait_status.pack(pady=(12, 0))
        note = "ปิดหน้านี้ได้ ร้านยืนยันแล้วจะแจ้งที่หน้าเมนู"
        if self.slip_email:
            note += f"\nและส่งใบเสร็จไปที่ {self.slip_email}"
        tk.Label(box, text=note, bg=BG, fg=TEXT_MUTED, font=(FONT, 10),
                 justify="center").pack(pady=(4, 0))
        make_button(box, "กลับไปหน้าเมนู", self.destroy, primary=False).pack(fill="x", pady=(18, 0))
        self._dots = 0
        self._poll_payment()

    def _poll_payment(self):
        self._poll_job = None
        if self._closed or not self.winfo_exists():
            return
        st = get_payment_state(self.order_id)
        if st is None or st["status"] == "cancelled":
            self.show_cancelled()
            return
        if st["status"] == "paid":
            self._slip_approved(st)
            return
        slip = st["slip"]
        if slip and slip["status"] == "rejected":
            self.show_rejected(slip["note"])
            return
        self._dots = (self._dots + 1) % 4
        self.wait_status.config(text="กำลังรอร้านยืนยันการชำระเงิน" + " ." * self._dots)
        self._poll_job = self.after(self.POLL_MS, self._poll_payment)

    def _slip_approved(self, st):
        """ร้านยืนยันสลิปแล้ว: แสดงผลชำระสำเร็จจากยอดที่บันทึกจริง (ร้านเป็นคนส่งใบเสร็จ)"""
        self.paid = True
        r = get_order_receipt(self.order_id)
        a = order_amounts(r)
        self.subtotal, self.discount, self.total = a["subtotal"], a["discount"], a["net"]
        self.vat, self.grand = a["vat"], a["paid"]
        self.percent = r["coupon"]["percent"] if r.get("coupon") else 0
        member = get_member(self.page.member["member_id"]) or {}
        self.result = {"points_earned": r["points_earned"], "points": member.get("points"),
                       "tier": member.get("tier"), "paid_total": a["paid"]}
        self.method_label = r.get("payment_method") or dict(PAYMENT_METHODS)["qr"]
        self.extra = {}
        self.page.refresh_after_payment()         # แต้ม/ระดับ/สต็อกบนหน้าเมนู (ไม่แตะตะกร้า)
        note = None
        if self.slip_email:
            note = (f"ร้านส่งใบเสร็จไปที่ {self.slip_email} แล้ว" if st.get("receipt_sent")
                    else f"ร้านกำลังส่งใบเสร็จไปที่ {self.slip_email}")
        self.show_done(self.slip_email or "", False, note)

    # ---------- สลิปไม่ผ่าน ----------
    def show_rejected(self, reason):
        box = self._center_box()
        icon = tk.Canvas(box, width=84, height=84, bg=BG, highlightthickness=0)
        icon.pack()
        draw_status_icon(icon, "bad")
        tk.Label(box, text="สลิปไม่ผ่านการตรวจสอบ", bg=BG, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(pady=(6, 0))
        tk.Label(box, text=f"ออเดอร์ {order_code(self.order_id)}  •  ยอดที่ต้องโอน ฿{fmt_price(self.grand)}",
                 bg=BG, fg=TEXT_MUTED, font=(FONT, 11)).pack()
        card = RoundFrame(box, fill="#3E1C19", radius=14, padx=16, pady=12)
        card.pack(fill="x", pady=(16, 0))
        tk.Label(card.inner, text="เหตุผลจากร้าน", bg="#3E1C19", fg=TEXT_MUTED,
                 font=(FONT, 10)).pack(anchor="w")
        tk.Label(card.inner, text=reason or "-", bg="#3E1C19", fg=TEXT, font=(FONT, 12, "bold"),
                 wraplength=410, justify="left").pack(anchor="w")
        tk.Label(box, text="ตรวจยอดโอนแล้วแนบสลิปใหม่ หรือยกเลิกออเดอร์นี้", bg=BG,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack(pady=(12, 0))
        self.reject_msg = tk.Label(box, text="", bg=BG, fg=ERROR, font=(FONT, 11))
        self.reject_msg.pack()
        make_button(box, "แนบสลิปใหม่", self._resubmit_slip, height=48).pack(fill="x", pady=(8, 0))
        make_button(box, "ยกเลิกออเดอร์", self._cancel_submitted, primary=False).pack(fill="x", pady=(8, 0))
        LinkButton(box, "กลับไปหน้าเมนู", self.destroy).pack(pady=(12, 0))

    def _resubmit_slip(self):
        png = self._pick_slip_file()
        if png is None or self._closed:
            return
        try:
            submit_payment_slip(self.order_id, png, self.grand, self.coupon_id, self.slip_email)
        except ValueError as e:
            self.reject_msg.config(text=str(e))
            return
        self.slip_png = png
        self.page.refresh_slip_banner()
        self.show_waiting()

    def _cancel_submitted(self):
        if messagebox.askyesno("ยกเลิกออเดอร์", f"ยกเลิกออเดอร์ {order_code(self.order_id)}?",
                               parent=self):
            cancel_order(self.order_id)
            self.page.refresh_slip_banner()
            self.destroy()

    def show_cancelled(self):
        box = self._center_box()
        icon = tk.Canvas(box, width=84, height=84, bg=BG, highlightthickness=0)
        icon.pack()
        draw_status_icon(icon, "bad")
        tk.Label(box, text="ออเดอร์นี้ถูกยกเลิกแล้ว", bg=BG, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(pady=(6, 0))
        tk.Label(box, text=f"ออเดอร์ {order_code(self.order_id)}  •  สอบถามเพิ่มเติมได้ที่เคาน์เตอร์",
                 bg=BG, fg=TEXT_MUTED, font=(FONT, 11)).pack()
        make_button(box, "ปิด", self.destroy, primary=False).pack(fill="x", pady=(20, 0))
        self.page.refresh_slip_banner()

    # ---------- ขั้นที่ 2: แจ้งผล + ส่งใบเสร็จ ----------
    def show_done(self, email, auto_send, note=None):
        for w in self.body.winfo_children():
            w.destroy()
        # รูปมีมแปะผนังสองข้าง (images/meme_done1.png, meme_done2.png) วางเทียบกับกลางจอ
        # หน้าต่างจะเล็กหรือเต็มจอ รูปก็อยู่ข้างการ์ดสรุปเสมอ
        for dx, dy, name, caption, kind in ((-432, -292, "meme_done1", "สำเร็จไหม? ยัง!?", "shock"),
                                            (252, -32, "meme_done2", "แก้วนี้แหละ!", "hype")):
            deco = tk.Canvas(self.body, width=186, height=230, bg=BG, highlightthickness=0)
            deco.place(relx=0.5, rely=0.5, x=dx, y=dy)
            draw_polaroid(deco, 10, 12, 160, name, caption, kind)
        box = tk.Frame(self.body, bg=BG)
        box.place(relx=0.5, rely=0.5, anchor="center", width=470)

        ck = tk.Canvas(box, width=84, height=84, bg=BG, highlightthickness=0)
        ck.pack()
        aa_oval(ck, 1, 1, 83, 83, fill="#3A3415", outline="")
        aa_oval(ck, 11, 11, 73, 73, fill=ACCENT, outline="")
        crisp(ck, 0, 0, 84, 84, lambda d: d.create_line(28, 43, 38, 53, 57, 32, fill=ACCENT_INK,
                                                        width=6, capstyle="round",
                                                        joinstyle="round"), ("check",))
        tk.Label(box, text="ชำระเงินสำเร็จ", bg=BG, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(pady=(6, 0))
        tk.Label(box, text=f"ออเดอร์ {order_code(self.order_id)}", bg=BG, fg=TEXT_MUTED,
                 font=(FONT, 11)).pack()
        tk.Label(box, text="BIG W!  COFFEE IS LOADING...", bg=BG, fg=ACCENT,
                 font=(FONT_MEME, 14)).pack(pady=(6, 0))

        lines = self._money_rows()
        lines += [("ยอดชำระ", f"฿{fmt_price(self.result['paid_total'])}"),
                  ("วิธีชำระเงิน", self.method_label)]
        if "change" in self.extra:
            lines.append(("เงินทอน", f"฿{fmt_price(self.extra['change'])}"))
        r = self.result
        if r["points_earned"]:
            lines.append(("แต้มที่ได้รับ", f"+{r['points_earned']} แต้ม"))
        if r["points"] is not None:
            lines.append(("แต้มสะสม / ระดับ", f"{r['points']} แต้ม  •  {r['tier']}"))
        card = RoundFrame(box, fill=SURFACE, border=LINE, radius=16, padx=18, pady=10)
        card.pack(fill="x", pady=(16, 0))
        table = card.inner
        for n, (k, v) in enumerate(lines):
            if n:
                tk.Frame(table, bg=LINE, height=1).pack(fill="x")
            row = tk.Frame(table, bg=SURFACE)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=k, bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 11)).pack(side="left")
            tk.Label(row, text=v, bg=SURFACE, fg=TEXT,
                     font=(FONT, 11, "bold")).pack(side="right")

        tk.Label(box, text="ส่งใบเสร็จทางอีเมล", bg=BG, fg=TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(18, 6))
        row = tk.Frame(box, bg=BG)
        row.pack(fill="x")
        done_box = RoundEntry(row, height=42)
        done_box.pack(side="left", fill="x", expand=True)
        self.done_email = done_box.entry
        self.done_email.insert(0, email or self.page.member.get("email") or "")
        self.send_btn = PillButton(row, "ส่งใบเสร็จ", self._send, "primary", height=42,
                                   size=10, padx=18)
        self.send_btn.pack(side="left", padx=(8, 0))
        self.status = tk.Label(box, text="", bg=BG, fg=TEXT_MUTED, font=(FONT, 11),
                               wraplength=460, justify="left")
        self.status.pack(anchor="w", pady=(6, 0))

        foot = tk.Frame(box, bg=BG)
        foot.pack(fill="x", pady=(20, 0))
        make_button(foot, "เสร็จสิ้น", self.destroy, height=48).pack(side="right", fill="x", expand=True,
                                                                     padx=(8, 0))
        PillButton(foot, "ติดตามออเดอร์", self._track_order, "secondary", height=48,
                   size=11).pack(side="left", fill="x", expand=True)
        if auto_send and email:
            self._send()
        elif note:                                # จ่ายด้วยสลิป: ร้านเป็นคนส่งใบเสร็จ
            self._set_status(note, SUCCESS)
            self.send_btn.config(text="ส่งอีกครั้ง")
        elif not auto_send:
            self.status.config(text="ยังไม่ได้ส่งใบเสร็จ กรอกอีเมลแล้วกด \"ส่งใบเสร็จ\" ได้")

    def _set_status(self, text, color):
        self.status.config(text=text, fg=color)

    def _track_order(self):
        """ปิดหน้าชำระเงิน แล้วเปิดหน้าติดตามออเดอร์ (ดูคิว / สถานะหลังร้าน)"""
        page, order_id = self.page, self.order_id
        self.destroy()
        page.open_order_status(order_id)

    def _send(self):
        email = self.done_email.get().strip()
        if not is_valid_email(email):
            self._set_status("รูปแบบอีเมลไม่ถูกต้อง", ERROR)
            return
        self.send_btn.config(state="disabled")
        self._set_status(f"กำลังส่งใบเสร็จไปที่ {email} ...", TEXT_MUTED)
        self._send_result = None
        order_id, extra = self.order_id, dict(self.extra)

        def work():                       # ทำงานในเธรดแยก ไม่แตะหน้าจอ (กันโปรแกรมค้าง)
            try:
                send_receipt_email(order_id, email, extra)
                self._send_result = (True, "")
            except Exception as e:
                self._send_result = (False, explain_email_error(e))

        threading.Thread(target=work, daemon=True).start()
        self.after(300, self._poll_send, email)

    def _poll_send(self, email):
        if self._closed or not self.winfo_exists():
            return
        if self._send_result is None:
            self.after(300, self._poll_send, email)
            return
        ok, err = self._send_result
        self.send_btn.config(state="normal", text="ส่งอีกครั้ง")
        if ok:
            self._set_status(f"ส่งใบเสร็จไปที่ {email} เรียบร้อยแล้ว ✓", SUCCESS)
        else:
            self._set_status(f"ส่งใบเสร็จไม่สำเร็จ: {err}\n(การชำระเงินบันทึกเรียบร้อยแล้ว)", ERROR)


# =====================================================================
# ส่วนที่ 17: หน้าแต้มสะสมและส่วนลด
#   ประกอบด้วย: class PointsDialog (ดูแต้ม, แลกส่วนลดด้วยแต้ม, ส่วนลดของฉัน, ประวัติแต้ม),
#              ระดับสมาชิก (draw_tier_medal, TierDialog เกณฑ์การเลื่อนระดับ + อีกกี่แต้มถึงระดับถัดไป,
#              open_tier_dialog กดที่ระดับของผู้ใช้เพื่อเปิด)
#   แก้ที่นี่เมื่อ: แก้หน้าตาหน้าแต้ม/หน้าระดับสมาชิก (ส่วนลดที่แลกได้กำหนดที่ REWARDS เกณฑ์ระดับที่ TIERS ในส่วนที่ 1)
# บรรทัด 3758 - 4175
# =====================================================================
def draw_tier_medal(c, cx, cy, d, color, dim=False):
    """เหรียญระดับสมาชิก (เหรียญมีดาว + ริบบิ้นด้านล่าง) ในกรอบขนาด d  dim = ยังไม่ถึงระดับนี้ (สีจาง)"""
    mix = lambda a, b, t: "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(_rgb(a), _rgb(b)))
    if dim:
        color = SURFACE_3
    ribbon = (SURFACE_2, LINE) if dim else ("#C0503F", "#93372B")
    for side, col in ((-1, ribbon[0]), (1, ribbon[1])):             # ริบบิ้น 2 หาง
        pts = [(0.04, 0.05), (0.29, 0.47), (0.20, 0.40), (0.11, 0.47), (-0.08, 0.12)]
        c.create_polygon(*[v for x, y in pts for v in (cx + side * x * d, cy + y * d)], fill=col, outline="")
    my, R = cy - 0.08 * d, 0.34 * d
    aa_oval(c, cx - R, my - R, cx + R, my + R, fill=color, outline="")
    r = R * 0.78
    aa_oval(c, cx - r, my - r, cx + r, my + r, fill=mix(color, "#000000", 0.14), outline="")
    star = []
    for k in range(10):                                            # ดาว 5 แฉก
        ang = math.pi / 2 + k * math.pi / 5
        rad = r * (0.66 if k % 2 == 0 else 0.28)
        star += [cx + rad * math.cos(ang), my - rad * math.sin(ang)]
    c.create_polygon(*star, fill=mix(color, "#FFFFFF", 0.55) if not dim else LINE, outline="")


def open_tier_dialog(parent, member, on_change=None):
    """เปิดหน้าระดับสมาชิก ถ้าเปิดจากหน้าต่างย่อย (เช่น หน้าแต้ม / โปรไฟล์) ปิดแล้วกลับไปหน้าต่างเดิม"""
    dlg = TierDialog(parent, member, on_change)
    if isinstance(parent, tk.Toplevel) and not isinstance(parent, CustomerWindow):
        parent.wait_window(dlg)
        if parent.winfo_exists():
            grab_modal(parent)
    return dlg


class TierDialog(tk.Toplevel):
    """ระดับสมาชิก: ระดับตอนนี้ อีกกี่แต้มถึงระดับถัดไป เกณฑ์ทุกระดับ และวิธีนับแต้มที่ใช้วัดระดับ
    เปิดโดยกดที่ระดับของผู้ใช้ (หัวหน้าเมนู / หน้าแต้ม / โปรไฟล์)  เกณฑ์มาจาก TIERS ในส่วนที่ 1"""

    PAGE_W = 760

    def __init__(self, parent, member, on_change=None):
        super().__init__(parent)
        self.title("ระดับสมาชิก")
        self.configure(bg=BG)
        self.transient(parent)
        w, h = 760, 720                           # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)
        info = get_member_tier(member["member_id"]) or {
            "points": member["points"], "redeemed": 0, "lifetime": member["points"],
            **tier_progress(member["points"])}
        self.info = info
        if member.get("tier") != info["tier"] or member.get("points") != info["points"]:
            member.update(tier=info["tier"], points=info["points"])        # ให้หัวหน้าเมนูตรงกัน
            if on_change:
                on_change()
        tier = info["tier"]
        color = TIER_COLORS.get(tier, LATTE)

        bar = tk.Frame(self, bg=PANEL, height=124)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar_full, bar = bar, tk.Frame(bar, bg=PANEL)
        bar.pack(fill="both", expand=True)
        keep_centered(bar_full, bar, self.PAGE_W)
        medal = tk.Canvas(bar, width=80, height=84, bg=PANEL, highlightthickness=0)
        medal.pack(side="left", padx=(24, 0))
        draw_tier_medal(medal, 40, 44, 78, color)
        head = tk.Frame(bar, bg=PANEL)
        head.pack(side="left", padx=14)
        tk.Label(head, text="ระดับสมาชิกของฉัน", bg=PANEL, fg=LATTE, font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Label(head, text=tier, bg=PANEL, fg=color, font=(FONT, 28, "bold")).pack(anchor="w")
        tk.Label(head, text=f"แต้มสะสมทั้งหมด {info['lifetime']:,} แต้ม", bg=PANEL, fg=TEXT_MUTED,
                 font=(FONT, 11)).pack(anchor="w")
        PillButton(bar, "ปิด", self.destroy, "dark_ghost", height=38, size=10,
                   padx=22).pack(side="right", padx=28)

        area = ScrollFrame(self, BG)
        area.pack(fill="both", expand=True)
        col = tk.Frame(area.inner, bg=BG)
        col.pack(fill="x")
        keep_centered(area.canvas, col, self.PAGE_W)
        self._progress_card(col, info, color)
        self._ladder_card(col, info)
        self._points_card(col, info)
        self._rules_card(col)
        tk.Frame(col, bg=BG, height=24).pack()
        try:
            grab_modal(self)
        except tk.TclError:
            pass

    @staticmethod
    def _card(parent, title):
        card = RoundFrame(parent, fill=SURFACE, border=LINE, radius=18, padx=22, pady=18)
        card.pack(fill="x", padx=24, pady=(16, 0))
        if title:
            tk.Label(card.inner, text=title, bg=SURFACE, fg=TEXT, font=(FONT, 14, "bold")).pack(anchor="w")
        return card.inner

    def _progress_card(self, parent, info, color):
        """อีกกี่แต้ม (ประมาณยอดซื้อเท่าไร) ถึงระดับถัดไป + แถบความคืบหน้า"""
        card = RoundFrame(parent, fill=SURFACE, border=color, radius=20, padx=24, pady=20, border_width=2)
        card.pack(fill="x", padx=24, pady=(22, 0))
        c = card.inner
        if info["next_tier"] is None:
            tk.Label(c, text="คุณอยู่ระดับสูงสุดแล้ว!", bg=SURFACE, fg=TEXT,
                     font=(FONT, 20, "bold")).pack(anchor="w")
            tk.Label(c, text=f"ขอบคุณที่เป็นลูกค้าประจำของ {SHOP_NAME}  ระดับนี้ไม่ลดลงแม้จะแลกแต้มเป็นส่วนลด",
                     bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 12), wraplength=640, justify="left").pack(anchor="w")
            return
        nxt = info["next_tier"]
        tk.Label(c, text=f"อีก {info['to_next']:,} แต้ม จะได้เลื่อนเป็น {nxt}", bg=SURFACE, fg=TEXT,
                 font=(FONT, 20, "bold")).pack(anchor="w")
        tk.Label(c, text=f"ประมาณยอดซื้ออีก ฿{info['to_next'] * BAHT_PER_POINT:,}  "
                         f"(ทุก {BAHT_PER_POINT} บาท ได้ 1 แต้ม)",
                 bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 12)).pack(anchor="w", pady=(2, 0))
        bar = tk.Canvas(c, height=14, bg=SURFACE, highlightthickness=0)
        bar.pack(fill="x", pady=(14, 4))

        def paint(e):
            bar.delete("all")
            w, h = e.width, 14
            rounded_rect(bar, 0, 0, w, h, h / 2, fill=SURFACE_2)
            if info["progress"] > 0:
                rounded_rect(bar, 0, 0, max(h, w * info["progress"]), h, h / 2, fill=color)
        bar.bind("<Configure>", paint)
        ends = tk.Frame(c, bg=SURFACE)
        ends.pack(fill="x")
        tk.Label(ends, text=f"{info['tier']}  {info['floor']:,}", bg=SURFACE, fg=TEXT_MUTED,
                 font=(FONT, 10)).pack(side="left")
        tk.Label(ends, text=f"{nxt}  {info['next_need']:,} แต้ม", bg=SURFACE,
                 fg=TIER_COLORS.get(nxt, LATTE), font=(FONT, 10, "bold")).pack(side="right")
        tk.Label(ends, text=f"คุณ {info['lifetime']:,} แต้ม", bg=SURFACE, fg=TEXT,
                 font=(FONT, 10, "bold")).pack()

    def _ladder_card(self, parent, info):
        """เกณฑ์ทุกระดับ (ต่ำ -> สูง): เหรียญ ชื่อ แต้มขั้นต่ำ ยอดซื้อโดยประมาณ และสถานะของผู้ใช้"""
        box = self._card(parent, "เกณฑ์การเลื่อนระดับ")
        ladder = sorted(TIERS, key=lambda t: t[1])
        mine = [n for n, _ in ladder].index(info["tier"])
        for i, (name, need) in enumerate(ladder):
            tk.Frame(box, bg=LINE, height=1).pack(fill="x", pady=(12, 0))
            row = tk.Frame(box, bg=SURFACE)
            row.pack(fill="x", pady=(12, 0))
            reached = i <= mine
            medal = tk.Canvas(row, width=50, height=54, bg=SURFACE, highlightthickness=0)
            medal.pack(side="left")
            draw_tier_medal(medal, 25, 28, 50, TIER_COLORS.get(name, LATTE), dim=not reached)
            if i == mine:
                st = ("ระดับของคุณ", ACCENT, ACCENT_INK)
            elif reached:
                st = ("ผ่านแล้ว", SUCCESS, ACCENT_INK)
            else:
                st = (f"อีก {need - info['lifetime']:,} แต้ม", SURFACE_2, TEXT)
            Pill(row, st[0], st[1], st[2], size=10, height=28, padx=12).pack(side="right")
            right = tk.Frame(row, bg=SURFACE)
            right.pack(side="right", padx=(0, 16))
            tk.Label(right, text="เริ่มต้นทุกคน" if need == 0 else f"ตั้งแต่ {need:,} แต้ม", bg=SURFACE,
                     fg=TEXT, font=(FONT, 12, "bold"), anchor="e").pack(anchor="e")
            tk.Label(right, text="สมัครสมาชิกแล้วได้ทันที" if need == 0 else
                     f"ประมาณยอดซื้อรวม ฿{need * BAHT_PER_POINT:,}", bg=SURFACE, fg=TEXT_MUTED,
                     font=(FONT, 10), anchor="e").pack(anchor="e")
            texts = tk.Frame(row, bg=SURFACE)
            texts.pack(side="left", padx=(12, 0))
            tk.Label(texts, text=name, bg=SURFACE, fg=TIER_COLORS.get(name, LATTE) if reached else TEXT_MUTED,
                     font=(FONT, 15, "bold")).pack(anchor="w")
            tk.Label(texts, text=TIER_TAGLINES.get(name, ""), bg=SURFACE, fg=TEXT_MUTED,
                     font=(FONT, 10)).pack(anchor="w")

    def _points_card(self, parent, info):
        """แต้มสะสมทั้งหมด = แต้มคงเหลือ + แต้มที่แลกส่วนลดไปแล้ว"""
        box = self._card(parent, "แต้มที่ใช้วัดระดับของคุณ")
        row = tk.Frame(box, bg=SURFACE)
        row.pack(fill="x", pady=(12, 0))
        parts = [("แต้มคงเหลือ", info["points"], TEXT), ("+", None, None),
                 ("แต้มที่แลกส่วนลดไปแล้ว", info["redeemed"], TEXT), ("=", None, None),
                 ("แต้มสะสมทั้งหมด", info["lifetime"], ACCENT)]
        for i, (label, value, fg) in enumerate(parts):
            if value is None:
                tk.Label(row, text=label, bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 18, "bold")).grid(
                    row=0, column=i, padx=6)
                continue
            row.grid_columnconfigure(i, weight=1, uniform="pts")
            cell = RoundFrame(row, fill=SURFACE_2, border=ACCENT if fg == ACCENT else "", radius=14,
                              padx=12, pady=10)
            cell.grid(row=0, column=i, sticky="nsew")
            tk.Label(cell.inner, text=f"{value:,}", bg=SURFACE_2, fg=fg, font=(FONT, 18, "bold")).pack()
            tk.Label(cell.inner, text=label, bg=SURFACE_2, fg=TEXT_MUTED, font=(FONT, 10)).pack()

    def _rules_card(self, parent):
        box = self._card(parent, "วิธีนับแต้มและเลื่อนระดับ")
        vat = "" if VAT_INCLUDED_IN_PRICE else " ไม่นับ VAT ที่บวกเพิ่ม"
        rules = [f"ทุกยอดซื้อ {BAHT_PER_POINT} บาท ได้ 1 แต้ม (คิดจากราคาเมนูหลังหักส่วนลด{vat})",
                 "ระดับวัดจาก \"แต้มสะสมทั้งหมด\" ตั้งแต่สมัคร รวมแต้มที่แลกส่วนลดไปแล้ว "
                 "จึงแลกแต้มได้เต็มที่ ระดับไม่ลดลง",
                 "เลื่อนระดับให้อัตโนมัติทันทีที่ชำระเงินออเดอร์ที่ทำให้แต้มถึงเกณฑ์",
                 "แต้มที่ร้านเพิ่มหรือหักให้ (เช่น ชดเชยออเดอร์) นับรวมในแต้มสะสมด้วย"]
        for text in rules:
            r = tk.Frame(box, bg=SURFACE)
            r.pack(fill="x", pady=(10, 0))
            dot = tk.Canvas(r, width=10, height=10, bg=SURFACE, highlightthickness=0)
            dot.pack(side="left", anchor="n", pady=(7, 0))
            aa_oval(dot, 1, 1, 9, 9, fill=ACCENT, outline="")
            tk.Label(r, text=text, bg=SURFACE, fg=TEXT, font=(FONT, 11), anchor="w", justify="left",
                     wraplength=640).pack(side="left", fill="x", expand=True, padx=(10, 0))


class PointsDialog(tk.Toplevel):
    """หน้าแต้มสะสม: ดูแต้ม แลกส่วนลดด้วยแต้ม ดูส่วนลดที่แลกไว้ และประวัติแต้ม"""
    PAGE_W = 760                  # ความกว้างเนื้อหา (เต็มจอแล้วเนื้อหาอยู่กลาง ไม่ยืดเกินนี้)

    def _tier_changed(self):
        """หน้าระดับสมาชิกแก้ระดับให้ตรงเกณฑ์แล้ว -> อัปเดตหัวหน้าเมนูด้วย"""
        self.on_change()

    def __init__(self, parent, member, on_change):
        super().__init__(parent)
        self.member = member          # dict เดียวกับที่หน้าเมนูใช้ (อัปเดตให้เมื่อแต้มเปลี่ยน)
        self.on_change = on_change
        self.title("แต้มสะสมและส่วนลด")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        w, h = 760, 680                          # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)

        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True)
        self.render()
        grab_modal(self)

    def render(self):
        fresh = get_member(self.member["member_id"])
        if fresh:
            self.member.update(fresh)
        m = self.member
        for w in self.body.winfo_children():
            w.destroy()

        # ---- แถบบน: แต้มคงเหลือ ----
        bar = tk.Frame(self.body, bg=PANEL, height=140)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar_full, bar = bar, tk.Frame(bar, bg=PANEL)        # แถบเต็มความกว้าง เนื้อหาอยู่กลาง
        bar.pack(fill="both", expand=True)
        keep_centered(bar_full, bar, self.PAGE_W)
        logo_canvas(bar, 56).pack(side="left", padx=(28, 0))
        info = tk.Frame(bar, bg=PANEL)
        info.pack(side="left", padx=(16, 28))
        tk.Label(info, text="แต้มสะสมของฉัน", bg=PANEL, fg=LATTE,
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(20, 0))
        tk.Label(info, text=f"{m['points']:,} แต้ม", bg=PANEL, fg=TEXT,
                 font=(FONT, 34, "bold")).pack(anchor="w")
        sub = tk.Frame(info, bg=PANEL)
        sub.pack(anchor="w")
        tier_pill = Pill(sub, f"{m['tier']}  ›", ACCENT, ACCENT_INK)      # กดดูเกณฑ์ระดับสมาชิก
        tier_pill.pack(side="left")
        tier_pill.config(cursor="hand2")
        tier_pill.bind("<Button-1>", lambda e: open_tier_dialog(self, self.member, self._tier_changed))
        tier_pill.bind("<Enter>", lambda e: tier_pill.set_fill(ACCENT_DARK))
        tier_pill.bind("<Leave>", lambda e: tier_pill.set_fill(ACCENT))
        tk.Label(sub, text=f"จ่ายทุก {BAHT_PER_POINT} บาท ได้ 1 แต้ม", bg=PANEL, fg=LATTE,
                 font=(FONT, 11)).pack(side="left", padx=8)
        PillButton(bar, "ปิด", self.destroy, "dark_ghost", height=38, size=10,
                   padx=22).pack(side="right", padx=(10, 28))
        sticker = tk.Canvas(bar, width=150, height=124, bg=PANEL, highlightthickness=0)
        sticker.pack(side="right")
        photo = load_meme_image("meme_points", 112, 112, radius=16)     # images/meme_points.png
        if photo is not None:
            rounded_rect(sticker, 17, 4, 133, 120, 18, fill=ACCENT, outline=ACCENT)
            sticker.create_image(75, 62, image=photo)
        else:
            draw_meme_tile(sticker, 19, 6, 131, 118, "hype", radius=16)
        rounded_rect(sticker, 8, 92, 104, 116, 12, fill=PINK, outline=PINK)
        sticker.create_text(56, 104, text="สะสมต่อไป!", fill="white", font=(FONT, 11, "bold"))

        area = ScrollFrame(self.body, BG)
        area.pack(fill="both", expand=True)
        root = tk.Frame(area.inner, bg=BG)                  # คอลัมน์เนื้อหา (อยู่กลางเมื่อเต็มจอ)
        root.pack(fill="x")
        keep_centered(area.canvas, root, self.PAGE_W)

        # ---- แลกส่วนลดด้วยแต้ม ----
        section_header(root, "แลกส่วนลดด้วยแต้ม")[0].pack(anchor="w", padx=28, pady=(20, 8))
        cards = tk.Frame(root, bg=BG)
        cards.pack(fill="x", padx=22)
        cards.columnconfigure(0, weight=1, uniform="reward")
        cards.columnconfigure(1, weight=1, uniform="reward")
        for i, (code, cost, pct) in enumerate(REWARDS):
            self._reward_card(cards, i, code, cost, pct)

        # ---- ส่วนลดของฉัน ----
        section_header(root, "ส่วนลดของฉัน")[0].pack(anchor="w", padx=28, pady=(20, 2))
        tk.Label(root, text="เลือกใช้ได้ตอนชำระเงิน (ใช้ได้ 1 ใบต่อ 1 ออเดอร์)", bg=BG,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w", padx=28, pady=(0, 6))
        coupons = get_coupons(m["member_id"])
        unused = [c for c in coupons if c["status"] == "unused"]
        used = [c for c in coupons if c["status"] == "used"][-5:]
        if not coupons:
            tk.Label(root, text="ยังไม่มีส่วนลด แลกจากด้านบนได้เลย", bg=BG,
                     fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w", padx=28, pady=8)
        for c in unused + used[::-1]:
            self._coupon_row(root, c)

        # ---- ประวัติแต้ม ----
        section_header(root, "ประวัติแต้มล่าสุด")[0].pack(anchor="w", padx=28, pady=(22, 8))
        history = get_point_history(m["member_id"])
        if not history:
            tk.Label(root, text="ยังไม่มีประวัติแต้ม", bg=BG, fg=TEXT_MUTED,
                     font=(FONT, 11)).pack(anchor="w", padx=28, pady=4)
        else:
            card = RoundFrame(root, fill=SURFACE, border=LINE, radius=16, padx=18, pady=8)
            card.pack(fill="x", padx=28)
            for n, h in enumerate(history):
                if n:
                    tk.Frame(card.inner, bg=LINE, height=1).pack(fill="x")
                self._history_row(card.inner, h)
        tk.Frame(root, bg=BG, height=24).pack()

    def _reward_card(self, parent, col, code, cost, pct):
        points = self.member["points"]
        card = RoundFrame(parent, fill=SURFACE, border=LINE, radius=20, padx=22, pady=20)
        card.grid(row=0, column=col, sticky="nsew", padx=6, pady=6)
        pad = card.inner
        top = tk.Frame(pad, bg=SURFACE)
        top.pack(fill="x")
        tk.Label(top, text=f"{pct}%", bg=SURFACE, fg=TEXT,
                 font=(FONT_LOGO, 34)).pack(side="left")
        Pill(top, f"{cost} แต้ม", SURFACE_2, ACCENT).pack(side="right", anchor="n", pady=(8, 0))
        tk.Label(pad, text=f"ส่วนลด {pct}% สำหรับทั้งออเดอร์", bg=SURFACE, fg=LATTE,
                 font=(FONT, 11)).pack(anchor="w")
        have = min(points, cost)
        tk.Label(pad, text=f"สะสมแล้ว {have:,} / {cost:,} แต้ม", bg=SURFACE, fg=TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w", pady=(12, 6))
        prog = tk.Canvas(pad, width=290, height=10, bg=SURFACE, highlightthickness=0)
        prog.pack(anchor="w")
        rounded_rect(prog, 0, 0, 290, 10, 5, fill=LINE, outline=LINE)
        done_w = int(290 * min(points / cost, 1))
        if done_w > 0:
            rounded_rect(prog, 0, 0, max(done_w, 10), 10, 5, fill=ACCENT, outline=ACCENT)
        if points >= cost:
            PillButton(pad, "แลกส่วนลด", lambda: self.redeem(code), "primary",
                       height=42).pack(fill="x", pady=(14, 0))
        else:
            tk.Label(pad, text=f"แต้มไม่พอ ขาดอีก {cost - points} แต้ม", bg=SURFACE,
                     fg=LATTE, font=(FONT, 11)).pack(anchor="w", pady=(14, 0))

    def _coupon_row(self, parent, c):
        is_unused = c["status"] == "unused"
        card = RoundFrame(parent, fill=SURFACE, border=LINE, radius=16, padx=18, pady=12)
        card.pack(fill="x", padx=28, pady=4)
        inner = card.inner
        icon = tk.Canvas(inner, width=44, height=44, bg=SURFACE, highlightthickness=0)
        icon.pack(side="left", padx=(0, 12))
        aa_oval(icon, 2, 2, 42, 42, fill=ACCENT if is_unused else SURFACE_2, outline="")
        icon.create_text(22, 22, text="%", fill=ACCENT_INK if is_unused else TEXT_MUTED,
                         font=(FONT, 15, "bold"))
        left = tk.Frame(inner, bg=SURFACE)
        left.pack(side="left")
        tk.Label(left, text=f"ส่วนลด {c['percent']}%", bg=SURFACE,
                 fg=TEXT if is_unused else TEXT_MUTED,
                 font=(FONT, 12, "bold")).pack(anchor="w")
        tk.Label(left, text=f"แลกเมื่อ {fmt_datetime(c['redeemed_at'])}", bg=SURFACE,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w")
        Pill(inner, "พร้อมใช้" if is_unused else "ใช้แล้ว",
             SUCCESS if is_unused else SURFACE_2,
             CREAM if is_unused else TEXT_MUTED).pack(side="right")

    def _history_row(self, parent, h):
        if h["type"] == "earn":
            text = (f"ได้รับแต้มจากออเดอร์ {order_code(h['order_id'])}"
                    if h["order_id"] else "ได้รับแต้ม")
        elif h["type"] == "redeem":
            text = "แลกส่วนลด"
        else:
            text = "ปรับแต้ม"
        plus = h["points"] >= 0
        bg = bg_of(parent)
        row = tk.Frame(parent, bg=bg)
        row.pack(fill="x", pady=7)
        col = tk.Frame(row, bg=bg)
        col.pack(side="left")
        tk.Label(col, text=text, bg=bg, fg=TEXT, font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Label(col, text=fmt_datetime(h["created_at"]), bg=bg, fg=TEXT_MUTED,
                 font=(FONT, 9)).pack(anchor="w")
        tk.Label(row, text=f"{'+' if plus else ''}{h['points']} แต้ม", bg=bg,
                 fg=SUCCESS if plus else ERROR,
                 font=(FONT, 11, "bold")).pack(side="right")

    def redeem(self, code):
        cost, pct = REWARD_BY_CODE[code]
        if not messagebox.askyesno(
                "แลกส่วนลด",
                f"ใช้ {cost} แต้ม แลกส่วนลด {pct}% ใช่หรือไม่?\n\n"
                "ส่วนลดจะอยู่ใน \"ส่วนลดของฉัน\" และเลือกใช้ได้ตอนชำระเงิน", parent=self):
            return
        try:
            redeem_coupon(self.member["member_id"], code)
        except ValueError as e:
            messagebox.showerror("แลกไม่สำเร็จ", str(e), parent=self)
            self.render()
            return
        self.render()
        self.on_change()
        messagebox.showinfo("แลกส่วนลดสำเร็จ",
                            f"ได้รับส่วนลด {pct}% แล้ว\nเลือกใช้ได้ตอนกดชำระเงิน", parent=self)


# =====================================================================
# ส่วนที่ 18: หน้าข้อมูลสมาชิก + ประวัติการสั่งซื้อ
#   ประกอบด้วย: ProfileDialog (ดูข้อมูล + รูปโปรไฟล์และปุ่มอัปโหลดรูป / แก้ไขข้อมูล / เปลี่ยนรหัสผ่าน),
#              OrderHistoryDialog (เมนูที่สั่งบ่อยที่สุด + ประวัติการสั่งซื้อทั้งหมดแบบแบ่งหน้า + ปุ่มสั่งซ้ำ),
#              ReceiptDialog + draw_receipt_page (ดูใบเสร็จย้อนหลัง + บันทึกเป็น PDF)
#   แก้ที่นี่เมื่อ: แก้หน้าข้อมูลสมาชิก หรือหน้าประวัติการสั่งซื้อ
# บรรทัด 4178 - 4981
# =====================================================================
def member_initial(name):
    """ตัวอักษรแรกของชื่อ (ข้ามสระหน้า เ แ โ ใ ไ)"""
    for ch in name.strip():
        if ch not in "เแโใไ":
            return ch.upper()
    return "?"


def fmt_date(s):
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return "-"


class ProfileDialog(tk.Toplevel):
    """หน้าข้อมูลสมาชิก: ดูข้อมูล (รูปโปรไฟล์ข้างการ์ดข้อมูล + ปุ่มอัปโหลดรูป) / แก้ไขข้อมูล /
    เปลี่ยนรหัสผ่าน (+ ปุ่มไปหน้าประวัติการสั่งซื้อ)"""
    PAGE_W = 520                  # ความกว้างเนื้อหาหน้าแก้ไข/เปลี่ยนรหัส (เต็มจอแล้วเนื้อหาอยู่กลาง ไม่ยืดเกินนี้)
    VIEW_W = 800                  # ความกว้างหน้าดูข้อมูล (รูปโปรไฟล์ + การ์ดข้อมูลวางข้างกัน)
    STACK_BELOW = 640             # พื้นที่แคบกว่านี้ (ย่อหน้าต่าง): วางรูปไว้เหนือการ์ดข้อมูลแทน

    def __init__(self, parent, member, on_change, on_history=None):
        super().__init__(parent)
        self.member = member          # dict เดียวกับที่หน้าเมนูใช้ (อัปเดตให้เมื่อแก้ไข)
        self.on_change = on_change
        self.on_history = on_history  # เปิดหน้าประวัติการสั่งซื้อ (ไม่บังคับ)
        self.title("ข้อมูลสมาชิก")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        w = min(860, self.winfo_screenwidth() - 40)        # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        h = min(740, self.winfo_screenheight() - 80)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)

        self.photo_card = None        # กรอบรูปโปรไฟล์ในหน้าดูข้อมูล
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True)
        self.show_view()
        grab_modal(self)

    # ---------- ส่วนประกอบร่วม ----------
    def _tier_changed(self):
        """หน้าระดับสมาชิกแก้ระดับให้ตรงเกณฑ์แล้ว -> อัปเดตหัวหน้าเมนู และแถว "ระดับสมาชิก" ในหน้านี้"""
        self.on_change()
        self.after_idle(lambda: self.winfo_exists() and self.show_view())

    def _reload(self):
        fresh = get_member(self.member["member_id"])
        if fresh:
            self.member.update(fresh)

    def _page(self, subtitle, width=None):
        """ล้างหน้าเดิม วาดแถบโปรไฟล์ด้านบน แล้วคืนกรอบเนื้อหา (width = ความกว้างเนื้อหาของหน้านี้)"""
        width = width or self.PAGE_W
        for w in self.body.winfo_children():
            w.destroy()
        bar = tk.Frame(self.body, bg=PANEL, height=124)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar_full, bar = bar, tk.Frame(bar, bg=PANEL)        # แถบเต็มความกว้าง เนื้อหาอยู่กลาง
        bar.pack(fill="both", expand=True)
        keep_centered(bar_full, bar, width)
        av = tk.Canvas(bar, width=76, height=76, bg=PANEL, highlightthickness=0)
        av.pack(side="left", padx=(28, 16))
        self.header_avatar = av                             # รูปโปรไฟล์วงกลม (ใช้รูปเดียวกับกรอบรูปด้านล่าง)
        col = tk.Frame(bar, bg=PANEL)
        col.pack(side="left")
        tk.Label(col, text=self.member["name"], bg=PANEL, fg=TEXT,
                 font=(FONT, 16, "bold"), wraplength=280,
                 justify="left").pack(anchor="w")
        Pill(col, subtitle, SURFACE_2, ACCENT, size=9, height=22).pack(anchor="w", pady=(4, 0))
        self._draw_header_avatar()
        logo_canvas(bar, 48).pack(side="right", padx=(0, 24))
        content = tk.Frame(self.body, bg=BG)
        content.pack(fill="both", expand=True)
        keep_centered(self.body, content, width)            # เต็มจอ: เนื้อหาอยู่กลาง กว้างเท่าเดิม
        self.content = content
        return content

    # ---------- รูปโปรไฟล์ ----------
    def _draw_header_avatar(self):
        """รูปโปรไฟล์วงกลมบนแถบหัว"""
        draw_avatar(self.header_avatar, 72, self.member, ACCENT, 3, photo_size=72, font_size=24)

    def _build_photo_panel(self):
        """กรอบรูปโปรไฟล์ข้างการ์ดข้อมูล: รูปใหญ่ + ปุ่มอัปโหลดรูปด้านล่าง (+ ลิงก์ลบรูป)"""
        box = self.photo_card.inner
        for w in box.winfo_children():
            w.destroy()
        has_photo = get_member_avatar(self.member["member_id"]) is not None
        S = AVATAR_SHOW
        pic = tk.Canvas(box, width=S, height=S, bg=SURFACE, highlightthickness=0, bd=0, cursor="hand2")
        pic.pack()
        pic.bind("<Button-1>", lambda e: self.change_avatar())     # กดที่รูปก็อัปโหลดได้
        self.photo_canvas = pic
        self._draw_big_photo()
        self.upload_btn = PillButton(box, "เปลี่ยนรูป" if has_photo else "อัปโหลดรูป", self.change_avatar,
                                     "secondary", height=38, size=10)
        self.upload_btn.pack(fill="x", pady=(14, 0))
        foot = tk.Frame(box, bg=SURFACE)
        foot.pack(pady=(8, 0))
        if has_photo:
            LinkButton(foot, "ลบรูป", self.remove_avatar, fg=TEXT_MUTED, hover=ERROR,
                       size=9, bold=True).pack()
        else:
            tk.Label(foot, text="ไฟล์ .jpg .png หรือ .gif" if HAS_PIL else "ไฟล์ .png หรือ .gif",
                     bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 9)).pack()

    def _draw_big_photo(self):
        """รูปโปรไฟล์ขนาดใหญ่ (มุมมน) / ยังไม่มีรูป -> ตัวอักษรแรกของชื่อบนพื้นสีน้ำตาล"""
        c, S = self.photo_canvas, AVATAR_SHOW
        c.delete("all")
        png = get_member_avatar(self.member["member_id"])
        photo = avatar_photo(png, S, radius=16) if png else None
        if photo is None:
            rounded_rect(c, 0, 0, S, S, 16, fill=TAN)
            c.create_text(S / 2, S / 2 - 12, text=member_initial(self.member["name"]),
                          font=(FONT, 60, "bold"), fill=BLACK)
            c.create_text(S / 2, S - 28, text="ยังไม่มีรูปโปรไฟล์", font=(FONT, 10), fill=BLACK)
        else:
            c.create_image(S / 2, S / 2, image=photo)
            c.big_photo = photo                               # กันรูปถูกเก็บทิ้ง

    def change_avatar(self):
        """เลือกไฟล์รูป -> ตัด/ย่อ -> บันทึกเป็นรูปโปรไฟล์"""
        patterns = AVATAR_TYPES_PIL if HAS_PIL else AVATAR_TYPES_TK
        path = filedialog.askopenfilename(parent=self, title="เลือกรูปโปรไฟล์",
                                          filetypes=[("รูปภาพ", " ".join(patterns)), ("ทุกไฟล์", "*.*")])
        if not path:
            return
        self.config(cursor="watch")                # รูปใหญ่ใช้เวลาย่อสักครู่
        self.update_idletasks()
        try:
            png = make_avatar_png(path)
        except ValueError as e:
            messagebox.showerror("ใช้รูปนี้ไม่ได้", str(e), parent=self)
            return
        finally:
            self.config(cursor="")
        ok, text = set_member_avatar(self.member["member_id"], png)
        if not ok:
            messagebox.showerror("บันทึกรูปไม่สำเร็จ", text, parent=self)
            return
        self._avatar_changed()

    def remove_avatar(self):
        if messagebox.askyesno("ลบรูปโปรไฟล์", "ลบรูปโปรไฟล์และกลับไปใช้ตัวอักษรแรกของชื่อ?", parent=self):
            set_member_avatar(self.member["member_id"], None)
            self._avatar_changed()

    def _avatar_changed(self):
        if self.winfo_exists():
            self._draw_header_avatar()
            if self.photo_card is not None and self.photo_card.winfo_exists():
                self._build_photo_panel()
        self.on_change()                       # อัปเดตรูปบนหัวหน้าเมนูด้วย

    def _row(self, label, value, muted=False, on_click=None):
        """แถวข้อมูล ชื่อหัวข้อ (ซ้าย) / ค่า (ขวา)  on_click = กดที่แถวแล้วทำอะไร (ค่าจะเป็นสีเหลืองมี ›)"""
        parent = self.rows_card.inner
        if parent.winfo_children():
            tk.Frame(parent, bg=LINE, height=1).pack(fill="x")
        f = tk.Frame(parent, bg=SURFACE)
        f.pack(fill="x", pady=7, expand=True)       # การ์ดสูงกว่าเนื้อหา (ข้างรูปโปรไฟล์) -> แถวกระจายเท่า ๆ กัน
        head = tk.Label(f, text=label, bg=SURFACE, fg=TEXT_MUTED, font=(FONT, 11))
        head.pack(side="left")
        val = tk.Label(f, text=f"{value}  ›" if on_click else value, bg=SURFACE,
                       fg=ACCENT if on_click else TEXT_MUTED if muted else TEXT,
                       font=(FONT, 11, "bold"), wraplength=250, justify="right")
        val.pack(side="right")
        if on_click:
            for w in (f, head, val):
                w.config(cursor="hand2")
                w.bind("<Button-1>", lambda e: on_click())

    def _buttons(self):
        f = tk.Frame(self.content, bg=BG)
        pack_bottom(f, fill="x", padx=28, pady=22)   # ปุ่มล่างได้พื้นที่ก่อน ไม่โดนตัดแม้จอเตี้ย
        return f

    def _form(self):
        box = tk.Frame(self.content, bg=BG)
        box.pack(fill="x", padx=30, pady=(6, 0))
        return box

    def _message(self, box):
        self.msg = tk.Label(box, text="", bg=BG, fg=ERROR, font=(FONT, 11),
                            wraplength=self.PAGE_W - 60, justify="left")
        self.msg.pack(anchor="w", pady=(8, 0))

    # ---------- ดูข้อมูล ----------
    def show_view(self):
        self._reload()
        self._page("ข้อมูลสมาชิก", self.VIEW_W)
        m = self.member
        row = tk.Frame(self.content, bg=BG)                 # รูปโปรไฟล์ (ซ้าย) + การ์ดข้อมูล (ขวา)
        row.pack(fill="x", padx=28, pady=(22, 0))
        self.info_row = row
        self.photo_card = RoundFrame(row, fill=SURFACE, border=LINE, radius=18, padx=18, pady=18)
        self._build_photo_panel()
        self.rows_card = RoundFrame(row, fill=SURFACE, border=LINE, radius=18,
                                    padx=20, pady=8)
        row.bind("<Configure>", lambda e: self._layout_info_row())
        self._layout_info_row()
        self._row("ชื่อ-นามสกุล", m["name"])
        self._row("เบอร์โทรศัพท์", m["phone"])
        self._row("อีเมล", m["email"] or "ยังไม่ได้ระบุ", muted=not m["email"])
        self._row("ระดับสมาชิก", m["tier"], on_click=lambda: open_tier_dialog(self, self.member, self._tier_changed))
        self._row("แต้มสะสม", f"{m['points']} แต้ม")
        self._row("สมัครสมาชิกเมื่อ", fmt_date(m["joined_date"]))

        btns = self._buttons()
        make_button(btns, "แก้ไขข้อมูล", self.show_edit).pack(fill="x")
        if self.on_history:
            make_button(btns, "ประวัติการสั่งซื้อ", self._open_history,
                        primary=False).pack(fill="x", pady=(8, 0))
        make_button(btns, "เปลี่ยนรหัสผ่าน", self.show_password,
                    primary=False).pack(fill="x", pady=(8, 0))
        make_button(btns, "ปิด", self.destroy, primary=False).pack(fill="x", pady=(8, 0))

    def _layout_info_row(self):
        """กว้างพอ: รูปโปรไฟล์อยู่ข้างการ์ดข้อมูล  แคบ (ย่อหน้าต่าง): รูปอยู่เหนือการ์ด"""
        row = self.info_row
        if not row.winfo_exists():
            return
        stacked = 1 < row.winfo_width() < self.STACK_BELOW - 56
        if getattr(row, "stacked", None) == stacked:
            return
        row.stacked = stacked
        if stacked:
            self.photo_card.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 14))
            self.rows_card.grid(row=1, column=0, sticky="ew")
            row.grid_columnconfigure(0, weight=1)
            row.grid_columnconfigure(1, weight=0)
        else:
            self.photo_card.grid(row=0, column=0, sticky="ns", padx=(0, 18), pady=0)
            self.rows_card.grid(row=0, column=1, sticky="nsew")
            row.grid_columnconfigure(0, weight=0)
            row.grid_columnconfigure(1, weight=1)

    def _open_history(self):
        self.destroy()
        self.on_history()

    # ---------- แก้ไขข้อมูล ----------
    def show_edit(self):
        self._page("แก้ไขข้อมูลสมาชิก")
        m = self.member
        box = self._form()
        self.f_name = make_field(box, "ชื่อ-นามสกุล")
        self.f_phone = make_field(box, "เบอร์โทรศัพท์ (ใช้เข้าสู่ระบบ)")
        self.f_email = make_field(box, "อีเมล")
        self.f_name.insert(0, m["name"])
        self.f_phone.insert(0, m["phone"])
        self.f_email.insert(0, m["email"] or "")
        self._message(box)

        btns = self._buttons()
        make_button(btns, "บันทึก", self.save_edit).pack(fill="x")
        make_button(btns, "ยกเลิก", self.show_view,
                    primary=False).pack(fill="x", pady=(8, 0))
        self.f_name.focus()

    def save_edit(self):
        name = self.f_name.get().strip()
        phone = self.f_phone.get().strip()
        email = self.f_email.get().strip()
        if not name or not phone or not email:
            self.msg.config(text="กรุณากรอกข้อมูลให้ครบ")
        elif not phone.isdigit() or not (9 <= len(phone) <= 10):
            self.msg.config(text="เบอร์โทรต้องเป็นตัวเลข 9-10 หลัก")
        elif not is_valid_email(email):
            self.msg.config(text="รูปแบบอีเมลไม่ถูกต้อง เช่น name@example.com")
        else:
            ok, text = update_member(self.member["member_id"], name, phone, email)
            if not ok:
                self.msg.config(text=text)
                return
            self._reload()
            self.on_change()
            messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อย", parent=self)
            self.show_view()

    # ---------- เปลี่ยนรหัสผ่าน ----------
    def show_password(self):
        self._page("เปลี่ยนรหัสผ่าน")
        box = self._form()
        self.f_old = make_field(box, "รหัสผ่านปัจจุบัน", show="•")
        self.f_new = make_password_field(box, "รหัสผ่านใหม่")
        self.f_new2 = make_field(box, "ยืนยันรหัสผ่านใหม่", show="•")
        self._message(box)

        btns = self._buttons()
        make_button(btns, "บันทึกรหัสผ่านใหม่", self.save_password).pack(fill="x")
        make_button(btns, "ยกเลิก", self.show_view,
                    primary=False).pack(fill="x", pady=(8, 0))
        self.f_old.focus()

    def save_password(self):
        old, new, new2 = self.f_old.get(), self.f_new.get(), self.f_new2.get()
        problem = password_problem(new)
        if not old or not new:
            self.msg.config(text="กรุณากรอกข้อมูลให้ครบ")
        elif problem:
            self.msg.config(text=problem)
        elif new != new2:
            self.msg.config(text="รหัสผ่านใหม่ทั้งสองช่องไม่ตรงกัน")
        elif new == old:
            self.msg.config(text="รหัสผ่านใหม่ต้องต่างจากรหัสผ่านเดิม")
        else:
            ok, text = change_password(self.member["member_id"], old, new)
            if not ok:
                self.msg.config(text=text)
                return
            messagebox.showinfo("สำเร็จ", "เปลี่ยนรหัสผ่านเรียบร้อย", parent=self)
            self.show_view()


class OrderHistoryDialog(tk.Toplevel):
    """ประวัติการสั่งซื้อ: เมนูที่สั่งบ่อยที่สุด (กด "สั่งอีก" ได้) + ออเดอร์ที่ชำระเงินแล้วทั้งหมด
    แบ่งหน้าละ 10 ออเดอร์ (ล่าสุดอยู่บน) กดปุ่มเลขหน้า / ก่อนหน้า / ถัดไป เพื่อดูออเดอร์เก่าได้ครบทุกออเดอร์
    แต่ละออเดอร์กด "สั่งซ้ำ" = ใส่ทุกแก้วพร้อมตัวเลือกเดิมลงตะกร้า ใช้ราคาปัจจุบัน (เมนูที่ปิดขายจะถูกข้าม)
    กด "ดูใบเสร็จ" = เปิดใบเสร็จของออเดอร์นั้น (ดู + บันทึกเป็นไฟล์ PDF ได้)"""

    PAGE_SIZE = 10                # ออเดอร์ต่อหน้า
    FAV_LIMIT = 5                 # เมนูที่สั่งบ่อยที่สุดกี่อันดับ
    PAGE_W = 760                  # ความกว้างเนื้อหา (เต็มจอแล้วเนื้อหาอยู่กลาง ไม่ยืดเกินนี้)

    def __init__(self, parent, page):
        super().__init__(parent)
        self.page = page
        self.title("ประวัติการสั่งซื้อ")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)
        w, h = 760, 680                          # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)

        member_id = page.member["member_id"]
        self.member_id = member_id
        count, spent = member_order_stats(member_id)
        self.count = count
        self.pages = max(1, math.ceil(count / self.PAGE_SIZE))
        self.page_no = 1

        bar = tk.Frame(self, bg=PANEL, height=124)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar_full, bar = bar, tk.Frame(bar, bg=PANEL)        # แถบเต็มความกว้าง เนื้อหาอยู่กลาง
        bar.pack(fill="both", expand=True)
        keep_centered(bar_full, bar, self.PAGE_W)
        logo_canvas(bar, 56).pack(side="left", padx=(28, 0))
        info = tk.Frame(bar, bg=PANEL)
        info.pack(side="left", padx=16)
        tk.Label(info, text="ประวัติการสั่งซื้อ", bg=PANEL, fg=LATTE,
                 font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Label(info, text=f"{count:,} ออเดอร์", bg=PANEL, fg=TEXT,
                 font=(FONT, 26, "bold")).pack(anchor="w")
        tk.Label(info, text=f"ใช้จ่ายรวม ฿{fmt_price(spent)}", bg=PANEL, fg=TEXT_MUTED,
                 font=(FONT, 11)).pack(anchor="w")
        PillButton(bar, "ปิด", self.destroy, "dark_ghost", height=38, size=10,
                   padx=22).pack(side="right", padx=28)

        area = ScrollFrame(self, BG)
        area.pack(fill="both", expand=True)
        self.area = area
        column = tk.Frame(area.inner, bg=BG)                # คอลัมน์ออเดอร์ (อยู่กลางเมื่อเต็มจอ)
        column.pack(fill="x")
        keep_centered(area.canvas, column, self.PAGE_W)
        if not count:
            self._empty(column)
        else:
            self._favorites(column)
            tk.Label(column, text="ออเดอร์ทั้งหมด", bg=BG, fg=TEXT,
                     font=(FONT, 14, "bold")).pack(anchor="w", padx=24, pady=(22, 0))
            self.list_box = tk.Frame(column, bg=BG)         # ออเดอร์ของหน้าที่เลือก (วาดใหม่ตอนเปลี่ยนหน้า)
            self.list_box.pack(fill="x")
            self.show_page(1)
        tk.Frame(column, bg=BG, height=20).pack()
        try:
            grab_modal(self)
        except tk.TclError:
            pass

    def _empty(self, parent):
        box = tk.Frame(parent, bg=BG)
        box.pack(pady=(50, 0))
        photo = load_meme_image("meme_cart", 180, 180, radius=18)
        c = tk.Canvas(box, width=180, height=180, bg=BG, highlightthickness=0)
        c.pack()
        if photo is not None:
            c.create_image(90, 90, image=photo)
        else:
            draw_meme_tile(c, 0, 0, 180, 180, "side_eye", radius=18)
        tk.Label(box, text="ยังไม่มีประวัติการสั่งซื้อ", bg=BG, fg=TEXT,
                 font=(FONT, 16, "bold")).pack(pady=(14, 2))
        tk.Label(box, text="สั่งแก้วแรกเลย แล้วครั้งหน้ากด \"สั่งซ้ำ\" ได้ในคลิกเดียว", bg=BG,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack()
        make_button(box, "ไปเลือกเมนู", self.destroy, height=42).pack(pady=(14, 0))

    # ---------- เมนูที่สั่งบ่อยที่สุด ----------
    def _favorites(self, parent):
        """การ์ดเมนูที่สั่งบ่อยที่สุด 5 อันดับ (รูป + จำนวนแก้ว/ครั้ง + ปุ่ม "สั่งอีก")"""
        favs = get_member_favorites(self.member_id, self.FAV_LIMIT)
        if not favs:
            return
        head = tk.Frame(parent, bg=BG)
        head.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(head, text="เมนูที่คุณสั่งบ่อยที่สุด", bg=BG, fg=TEXT,
                 font=(FONT, 14, "bold")).pack(side="left")
        tk.Label(head, text=f"นับจากทั้งหมด {self.count:,} ออเดอร์", bg=BG, fg=TEXT_MUTED,
                 font=(FONT, 10)).pack(side="right")
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", padx=24, pady=(10, 0))
        for i in range(self.FAV_LIMIT):                     # ช่องเท่ากันเสมอ (มีน้อยกว่า 5 เมนูก็ไม่ยืด)
            row.grid_columnconfigure(i, weight=1, uniform="fav")
        for i, f in enumerate(favs):
            tile = RoundFrame(row, fill=SURFACE, border=ACCENT if i == 0 else LINE, radius=16,
                              padx=10, pady=10)
            tile.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 8, 0))
            t = tile.inner
            Pill(t, f"#{i + 1}", ACCENT if i == 0 else SURFACE_2, ACCENT_INK if i == 0 else TEXT,
                 size=9, height=22, padx=8).pack(anchor="w")
            pic = tk.Canvas(t, width=96, height=96, bg=SURFACE, highlightthickness=0)
            pic.pack(pady=(4, 0))
            photo = load_product_image(f, 96, 96)
            if photo is not None:
                pic.create_image(48, 48, image=photo)
                pic.photo = photo
            else:
                icon_cup(pic, 48, 52, drink_color(f["name"]))
            tk.Label(t, text=f["name"], bg=SURFACE, fg=TEXT, font=(FONT, 10, "bold"),   # สูง 2 บรรทัดเสมอ
                     wraplength=112, justify="center", height=2, anchor="n").pack(pady=(4, 0))  # ปุ่มจะได้ตรงกัน
            tk.Label(t, text=f"{f['cups']:,} แก้ว  •  {f['times']:,} ครั้ง", bg=SURFACE, fg=ACCENT,
                     font=(FONT, 9, "bold")).pack()
            ok = f["is_available"] and f["stock"] > 0
            btn = PillButton(t, "สั่งอีก" if ok else ("หมดแล้ว" if f["is_available"] else "ปิดขาย"),
                             lambda pid=f["product_id"]: self._order_again(pid), "secondary",
                             height=30, size=9, padx=12)
            btn.pack(pady=(6, 0))
            if not ok:
                btn.config(state="disabled")

    def _order_again(self, product_id):
        """ปิดหน้าประวัติ แล้วเปิดหน้าปรับแต่งเครื่องดื่มของเมนูนั้น"""
        page = self.page
        self.destroy()
        product = get_product(product_id)
        if product:
            page.open_options(product)

    # ---------- แบ่งหน้า ----------
    def show_page(self, n):
        """แสดงออเดอร์หน้าที่ n (หน้าละ PAGE_SIZE ออเดอร์) แล้วเลื่อนกลับขึ้นบนสุด"""
        self.page_no = max(1, min(n, self.pages))
        box = self.list_box
        for w in box.winfo_children():
            w.destroy()
        orders = get_member_orders(self.member_id, self.PAGE_SIZE, (self.page_no - 1) * self.PAGE_SIZE)
        self._pager(box)
        for o in orders:
            self._order_card(box, o)
        if self.pages > 1:
            self._pager(box)
        self.update_idletasks()
        self.area.canvas.yview_moveto(0)

    def _page_numbers(self):
        """เลขหน้าที่จะแสดง (หน้าแรก หน้าสุดท้าย และหน้ารอบ ๆ หน้าปัจจุบัน ที่เหลือเป็น ...)"""
        p, last = self.page_no, self.pages
        keep = {1, last, p - 1, p, p + 1}
        out = []
        for n in range(1, last + 1):
            if n in keep:
                out.append(n)
            elif out and out[-1] != "…":
                out.append("…")
        return out

    def _pager(self, parent):
        """แถวบอกช่วงออเดอร์ + ปุ่ม ก่อนหน้า / เลขหน้า / ถัดไป"""
        p, size = self.page_no, self.PAGE_SIZE
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill="x", padx=24, pady=(14, 0))
        first, last = (p - 1) * size + 1, min(p * size, self.count)
        tk.Label(bar, text=f"ออเดอร์ที่ {first}–{last} จาก {self.count:,}  •  หน้า {p}/{self.pages}",
                 bg=BG, fg=TEXT_MUTED, font=(FONT, 10)).pack(side="left")
        if self.pages == 1:
            return
        nav = tk.Frame(bar, bg=BG)
        nav.pack(side="right")
        prev = PillButton(nav, "‹ ก่อนหน้า", lambda: self.show_page(p - 1), "secondary",
                          height=32, size=10, padx=12)
        prev.pack(side="left")
        for n in self._page_numbers():
            if n == "…":
                tk.Label(nav, text="…", bg=BG, fg=TEXT_MUTED, font=(FONT, 10)).pack(side="left", padx=2)
                continue
            PillButton(nav, str(n), lambda n=n: self.show_page(n), "primary" if n == p else "secondary",
                       height=32, size=10, padx=11).pack(side="left", padx=(4, 0))
        nxt = PillButton(nav, "ถัดไป ›", lambda: self.show_page(p + 1), "secondary",
                         height=32, size=10, padx=12)
        nxt.pack(side="left", padx=(4, 0))
        if p == 1:
            prev.config(state="disabled")
        if p == self.pages:
            nxt.config(state="disabled")

    def _order_card(self, parent, o):
        amounts = order_amounts(o)                      # ยอดที่จ่ายจริง (หลังลด รวมภาษีแล้ว)
        card = RoundFrame(parent, fill=SURFACE, border=LINE, radius=16, padx=18, pady=14)
        card.pack(fill="x", padx=24, pady=(14, 0))
        c = card.inner
        top = tk.Frame(c, bg=SURFACE)
        top.pack(fill="x")
        tk.Label(top, text=order_code(o["order_id"]), bg=SURFACE, fg=TEXT,
                 font=(FONT, 13, "bold")).pack(side="left")
        tk.Label(top, text=fmt_datetime(o["paid_at"]), bg=SURFACE, fg=TEXT_MUTED,
                 font=(FONT, 10)).pack(side="left", padx=10)
        tk.Label(top, text=f"฿{fmt_price(amounts['paid'])}", bg=SURFACE, fg=TEXT,
                 font=(FONT, 15, "bold")).pack(side="right")

        for it in o["items"]:
            row = tk.Frame(c, bg=SURFACE)
            row.pack(fill="x", pady=(8, 0))
            tk.Label(row, text=f"{it['quantity']}×", bg=SURFACE, fg=ACCENT, width=3, anchor="w",
                     font=(FONT, 11, "bold")).pack(side="left", anchor="n")
            tk.Label(row, text=f"฿{fmt_price(it['quantity'] * it['unit_price'])}", bg=SURFACE,
                     fg=TEXT_MUTED, font=(FONT, 11)).pack(side="right", anchor="n")
            col = tk.Frame(row, bg=SURFACE)
            col.pack(side="left", fill="x", expand=True)
            off = not it["is_available"] or it["stock"] <= 0
            tag = "   (ปิดขายอยู่)" if not it["is_available"] else "   (หมดแล้ว)" if off else ""
            tk.Label(col, text=it["name"] + tag, bg=SURFACE,
                     fg=TEXT_MUTED if off else TEXT, font=(FONT, 11, "bold")).pack(anchor="w")
            if it["options"]:
                tk.Label(col, text=it["options"], bg=SURFACE, fg=LATTE, font=(FONT, 10),
                         wraplength=520, justify="left").pack(anchor="w")

        tk.Frame(c, bg=LINE, height=1).pack(fill="x", pady=(12, 10))
        bottom = tk.Frame(c, bg=SURFACE)
        bottom.pack(fill="x")
        Pill(bottom, o["payment_method"] or "-", SURFACE_2, TEXT, size=9, height=24).pack(side="left")
        if o["points_earned"]:
            Pill(bottom, f"+{o['points_earned']} แต้ม", SURFACE_2, ACCENT, size=9,
                 height=24).pack(side="left", padx=(6, 0))
        if o["discount"]:
            Pill(bottom, f"ส่วนลด -฿{fmt_price(o['discount'])}", SURFACE_2, SUCCESS, size=9,
                 height=24).pack(side="left", padx=(6, 0))
        if amounts["vat"]:
            Pill(bottom, f"VAT {VAT_RATE:g}% ฿{fmt_price(amounts['vat'])}", SURFACE_2, LATTE, size=9,
                 height=24).pack(side="left", padx=(6, 0))
        if o.get("prep_status") in PREP_ACTIVE:           # ยังไม่ได้รับ: กดป้ายเพื่อติดตามออเดอร์
            tag = Pill(bottom, PREP_LABEL[o["prep_status"]], PREP_COLORS[o["prep_status"]], ACCENT_INK,
                       size=9, height=24)
            tag.pack(side="left", padx=(6, 0))
            tag.config(cursor="hand2")
            tag.bind("<Button-1>", lambda e: self._track(o["order_id"]))
        can = any(it["is_available"] and it["stock"] > 0 for it in o["items"])
        btn = PillButton(bottom, "สั่งซ้ำ" if can else "หมด/ปิดขายทั้งหมด", lambda: self._reorder(o),
                         "primary", height=38, size=10, padx=22)
        btn.pack(side="right")
        if not can:
            btn.config(state="disabled")
        PillButton(bottom, "ดูใบเสร็จ", lambda: self.show_receipt(o["order_id"]), "secondary",
                   height=38, size=10, padx=18).pack(side="right", padx=(0, 8))

    def _reorder(self, o):
        page = self.page
        self.destroy()
        page.reorder(o)

    def _track(self, order_id):
        page = self.page
        self.destroy()
        page.open_order_status(order_id)

    def show_receipt(self, order_id):
        """เปิดหน้าดูใบเสร็จ (ดู + บันทึกเป็น PDF) ปิดแล้วกลับมาที่หน้าประวัติหน้าเดิม"""
        dlg = ReceiptDialog(self, order_id)
        self.wait_window(dlg)
        if self.winfo_exists():
            grab_modal(self)


def draw_receipt_page(c, page, height, scale, ox=0, oy=0):
    """วาดใบเสร็จลง Canvas จากเลย์เอาต์เดียวกับไฟล์ PDF (receipt_page) หน้าตาบนจอจึงตรงกับไฟล์ที่บันทึก
    scale = พิกเซลต่อ 1 point, (ox, oy) = มุมซ้ายบนของกระดาษ
    ฟอนต์บนจอ (FONT) กว้างไม่เท่าฟอนต์ใน PDF: ข้อความที่ยาวเกินที่ PDF เผื่อไว้จะย่อลงให้พอดี
    และข้อความที่วางต่อกันในบรรทัดเดียว (เช่น "เลขที่ออเดอร์ " + เลขตัวหนา) จะต่อจากความกว้างจริงบนจอ"""
    X = lambda v: ox + v * scale
    Y = lambda v: oy + v * scale
    c.create_rectangle(X(0), Y(0), X(page.width), Y(height), fill="#FFFFFF", outline="")
    fonts, run_end = {}, {}

    def font(px, bold):
        if (px, bold) not in fonts:
            key = (FONT, -px, "bold" if bold else "normal")
            fonts[px, bold] = _FONT_OBJ.get(key) or _FONT_OBJ.setdefault(key, tkfont.Font(font=key))
        return fonts[px, bold]

    for op in page.ops:
        if op[0] == "rect":
            _, x, y, w, h, color, r = op
            if r > 0:
                rounded_rect(c, X(x), Y(y), X(x + w), Y(y + h), r * scale, fill=color)
            else:
                c.create_rectangle(X(x), Y(y), X(x + w), Y(y + h), fill=color, outline="")
        elif op[0] == "line":
            _, x1, y1, x2, y2, color, width = op
            c.create_line(X(x1), Y(y1), X(x2), Y(y2), fill=color, width=max(1, round(width * scale)))
        else:
            _, x, y, _glyphs, size, color, style, text, anchor_x, align, w = op
            bold = style == "bold"
            px = max(6, round(size * scale))
            f = font(px, bold)
            room = w * scale + 1
            if f.measure(text) > room:                       # กว้างกว่าใน PDF -> ย่อลง
                px = max(6, int(px * room / f.measure(text)))
                f = font(px, bold)
            base = Y(y) + f.metrics("descent")               # y ของ PDF คือเส้นฐานตัวอักษร
            if align == "left":
                sx = run_end.get((round(y, 2), round(x, 2)), X(x))
                c.create_text(sx, base, text=text, fill=color, font=f, anchor="sw")
                run_end[round(y, 2), round(x + w, 2)] = sx + f.measure(text)
            else:
                c.create_text(X(anchor_x), base, text=text, fill=color, font=f,
                              anchor="se" if align == "right" else "s")


class ReceiptDialog(tk.Toplevel):
    """ดูใบเสร็จย้อนหลังของออเดอร์ที่ชำระแล้ว + บันทึกเป็นไฟล์ PDF (ไฟล์เดียวกับที่ส่งทางอีเมล)
    ใบเสร็จบนจอวาดจากเลย์เอาต์เดียวกับไฟล์ PDF  ถ้าไม่มีฟอนต์ในโฟลเดอร์ fonts จะแสดงแบบข้อความ
    และบันทึกเป็นไฟล์ .html แทน (เปิดด้วยเว็บเบราว์เซอร์ แล้วสั่งพิมพ์เป็น PDF ได้)"""

    SCALE = 1.6                   # ขนาดใบเสร็จบนจอ (1 point ในไฟล์ PDF = 1.6 พิกเซล)
    PAGE_W = 760

    def __init__(self, parent, order_id):
        super().__init__(parent)
        self.order_id = order_id
        self.code = order_code(order_id)
        self.saved_path = None
        self.title(f"ใบเสร็จ {self.code}")
        self.configure(bg=BG)
        self.transient(parent)
        w, h = 700, 760                           # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)
        r = get_order_receipt(order_id)
        try:
            self.layout = receipt_page(order_id)        # (หน้า, ความสูง)
        except RECEIPT_PDF_ERRORS:
            self.layout = None                          # ไม่มีฟอนต์ทำ PDF -> แสดงแบบข้อความ

        bar = tk.Frame(self, bg=PANEL, height=110)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar_full, bar = bar, tk.Frame(bar, bg=PANEL)
        bar.pack(fill="both", expand=True)
        keep_centered(bar_full, bar, self.PAGE_W)
        logo_canvas(bar, 52).pack(side="left", padx=(28, 0))
        info = tk.Frame(bar, bg=PANEL)
        info.pack(side="left", padx=16)
        tk.Label(info, text="ใบเสร็จรับเงิน", bg=PANEL, fg=LATTE, font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Label(info, text=self.code, bg=PANEL, fg=TEXT, font=(FONT, 24, "bold")).pack(anchor="w")
        if r:
            tk.Label(info, text=f"{fmt_datetime(r.get('paid_at') or r['order_date'])}  •  "
                                f"฿{fmt_price(order_amounts(r)['paid'])}",
                     bg=PANEL, fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w")
        PillButton(bar, "ปิด", self.destroy, "dark_ghost", height=38, size=10,
                   padx=22).pack(side="right", padx=28)

        foot_full = tk.Frame(self, bg=PANEL)            # แถวปุ่มล่างสุด (จอเตี้ยก็ไม่โดนตัด)
        pack_bottom(foot_full, fill="x")
        tk.Frame(foot_full, bg=LINE, height=1).pack(fill="x")
        foot = tk.Frame(foot_full, bg=PANEL)
        foot.pack(fill="x", pady=14)
        keep_centered(foot_full, foot, self.PAGE_W)
        self.save_btn = PillButton(foot, "บันทึกใบเสร็จ (PDF)" if self.layout else "บันทึกใบเสร็จ (HTML)",
                                   self.save, "primary", height=44, size=11, padx=24)
        self.save_btn.pack(side="right", padx=(0, 28))
        self.status = tk.Frame(foot, bg=PANEL)
        self.status.pack(side="left", fill="x", expand=True, padx=(28, 16))
        self._show_hint()

        area = ScrollFrame(self, BG)
        area.pack(fill="both", expand=True)
        self.area = area
        if self.layout:
            self._draw_paper(area.inner)
        else:
            self._draw_text(area.inner)
        try:
            grab_modal(self)
        except tk.TclError:
            pass

    def _draw_paper(self, parent):
        """กระดาษใบเสร็จ (มีเงา) วาดจากเลย์เอาต์เดียวกับไฟล์ PDF"""
        page, height = self.layout
        s, pad = self.SCALE, 14
        w, h = page.width * s, height * s
        c = tk.Canvas(parent, width=int(w + 2 * pad), height=int(h + 2 * pad), bg=BG, highlightthickness=0)
        c.pack(pady=(18, 18))
        rounded_rect(c, pad + 4, pad + 6, pad + w + 4, pad + h + 6, 6, fill="#0B0B0B")
        draw_receipt_page(c, page, height, s, pad, pad)
        self.paper = c

    def _draw_text(self, parent):
        """สำรองเมื่อไม่มีฟอนต์ทำ PDF: ใบเสร็จแบบข้อความบนกระดาษขาว"""
        tk.Label(parent, text="ไม่พบไฟล์ฟอนต์ในโฟลเดอร์ fonts จึงแสดงใบเสร็จแบบย่อ และบันทึกเป็นไฟล์ .html แทน PDF",
                 bg=BG, fg=TEXT_MUTED, font=(FONT, 10)).pack(pady=(18, 0))
        try:
            text = build_receipt(self.order_id)[1]
        except ValueError as e:
            text = str(e)
        paper = tk.Frame(parent, bg="#FFFFFF")
        paper.pack(pady=(10, 18))
        tk.Label(paper, text=text, bg="#FFFFFF", fg="#1A1A1A", font=(FONT, 11), justify="left",
                 anchor="w", wraplength=520).pack(padx=30, pady=24)

    def _clear_status(self):
        for w in self.status.winfo_children():
            w.destroy()

    def _show_hint(self):
        self._clear_status()
        kind = "PDF" if self.layout else "HTML"
        tk.Label(self.status, text=f"บันทึกเป็นไฟล์ {kind} เก็บไว้ เปิดดูหรือสั่งพิมพ์ได้ทุกเครื่อง",
                 bg=PANEL, fg=TEXT_MUTED, font=(FONT, 10), anchor="w").pack(fill="x")

    def _default_folder(self):
        """โฟลเดอร์เริ่มต้นตอนบันทึก: Downloads ถ้ามี ไม่งั้นโฟลเดอร์ผู้ใช้"""
        home = os.path.expanduser("~")
        downloads = os.path.join(home, "Downloads")
        return downloads if os.path.isdir(downloads) else home

    def save(self):
        """เลือกที่บันทึก แล้วเขียนไฟล์ใบเสร็จ (PDF หรือ HTML ถ้าไม่มีฟอนต์)"""
        pdf = self.layout is not None
        ext = ".pdf" if pdf else ".html"
        path = filedialog.asksaveasfilename(
            parent=self, title="บันทึกใบเสร็จ", initialdir=self._default_folder(),
            initialfile=receipt_filename(self.order_id, ext), defaultextension=ext,
            filetypes=[("ไฟล์ PDF", "*.pdf")] if pdf else [("หน้าเว็บ (HTML)", "*.html")])
        if not path:
            return
        try:
            if pdf:
                data = build_receipt_pdf(self.order_id)[1]
            else:
                data = build_receipt(self.order_id)[2].encode("utf-8")
            with open(path, "wb") as f:
                f.write(data)
        except PermissionError:
            messagebox.showerror("บันทึกไม่ได้", "ไฟล์นี้เปิดอยู่ในโปรแกรมอื่น (เช่น โปรแกรมอ่าน PDF)\n"
                                                 "กรุณาปิดไฟล์ก่อน หรือบันทึกเป็นชื่ออื่น", parent=self)
            return
        except RECEIPT_PDF_ERRORS as e:
            messagebox.showerror("บันทึกไม่ได้", f"บันทึกใบเสร็จไม่สำเร็จ: {e}", parent=self)
            return
        self.saved_path = path
        self._show_saved()

    def _show_saved(self):
        """แจ้งว่าบันทึกแล้ว + ปุ่มเปิดไฟล์ / เปิดโฟลเดอร์ (Windows)"""
        self._clear_status()
        path = self.saved_path
        row = tk.Frame(self.status, bg=PANEL)
        row.pack(fill="x")
        tk.Label(row, text="บันทึกใบเสร็จแล้ว", bg=PANEL, fg=SUCCESS,
                 font=(FONT, 11, "bold")).pack(side="left")
        if hasattr(os, "startfile"):
            LinkButton(row, "เปิดไฟล์", lambda: self._open(path), fg=ACCENT, hover=TEXT,
                       size=10, bold=True).pack(side="left", padx=(14, 0))
            LinkButton(row, "เปิดโฟลเดอร์", lambda: self._open(os.path.dirname(path)), fg=ACCENT,
                       hover=TEXT, size=10, bold=True).pack(side="left", padx=(12, 0))
        tk.Label(self.status, text=path, bg=PANEL, fg=TEXT_MUTED, font=(FONT, 9),
                 anchor="w", justify="left", wraplength=440).pack(fill="x")

    def _open(self, path):
        try:
            os.startfile(path)
        except OSError as e:
            messagebox.showerror("เปิดไม่ได้", f"เปิดไม่สำเร็จ: {e}", parent=self)


# =====================================================================
# ส่วนที่ 19: หน้าเลือกเมนู
#   ประกอบด้วย: class MenuPage: แถบโปรไฟล์, แถบแจ้งสถานะสลิป (รอตรวจ/ไม่ผ่าน/ร้านยืนยันแล้ว),
#              แถบสถานะออเดอร์หลังร้าน (รอคิว/กำลังทำ/พร้อมรับ + แจ้งเตือนเด้ง), แบนเนอร์,
#              หมวดหมู่วงกลม, ค้นหาเมนู, สั่งซ้ำออเดอร์ล่าสุด, การ์ดเมนู, แถบตะกร้า, ยืนยันสั่งซื้อ
#   แก้ที่นี่เมื่อ: แก้เลย์เอาต์หน้าเมนู การ์ดเมนู หรือขั้นตอนสั่งซื้อ
# บรรทัด 4984 - 5781
# =====================================================================
class MenuPage(tk.Frame):
    """หน้าเมนูสไตล์แอป: โปรไฟล์ + แบนเนอร์ + หมวดหมู่วงกลม + เมนูแนะนำ + ทุกเมนู"""

    CARD_W = 194                    # ความกว้างการ์ดขั้นต่ำ (การ์ดยืดเท่า ๆ กันให้เต็มแถวตามความกว้างหน้าต่าง)
    CARD_H = 370                    # ความสูงการ์ด (คำนวณใหม่ตอนเปิดหน้า ตามความสูงบรรทัดของฟอนต์ในเครื่อง)
    TITLE_SIZE = 14                 # ขนาดตัวอักษรชื่อเมนูบนการ์ด
    DESC_SIZE = 12                  # ขนาดตัวอักษรคำอธิบายเมนูบนการ์ด
    DESC_LINES = 3                  # คำอธิบายแสดงได้สูงสุดกี่บรรทัด (ยาวกว่านี้ลงท้าย … ชี้เมาส์ค้างอ่านเต็ม)
    IMG_H = 196                     # ความสูงพื้นที่รูปเครื่องดื่ม (รูปของร้าน 372 x 392 ย่อครึ่งพอดี)
    COLS = 5                      # จำนวนคอลัมน์เริ่มต้น (จะคำนวณใหม่ตามความกว้างหน้าต่าง)

    def __init__(self, app, member, on_logout):
        super().__init__(app, bg=BG)
        self.app = app
        self.member = member
        self.on_logout = on_logout
        self.cart = Cart()
        self.cart_dialog = None
        self.categories = get_categories()
        self.selected_cat = None          # None = ทั้งหมด
        self.cols = self.COLS
        self.card_w = self.CARD_W                 # ความกว้างการ์ดตอนนี้ (คำนวณใหม่ตามความกว้างหน้าต่าง)
        # ขนาดการ์ดเมนู = ชื่อ + คำอธิบาย 3 บรรทัด + รูป + แถวราคา (ความสูงบรรทัดขึ้นกับฟอนต์ในเครื่อง)
        self.title_font = (FONT, self.TITLE_SIZE, "bold")
        self.desc_font = (FONT, self.DESC_SIZE)
        self.desc_top = 13 + font_linespace(self.title_font) + 1      # คำอธิบายเริ่มใต้ชื่อเมนู
        self.desc_line_h = font_linespace(self.desc_font)
        self.img_top = self.desc_top + self.DESC_LINES * self.desc_line_h + 6
        self.CARD_H = self.img_top + self.IMG_H + 58
        self.grid_sections = []
        self.resize_job = None

        self._build_header()
        self.slip_bar = tk.Frame(self, bg=BG)       # แถบแจ้งสถานะสลิปโอนเงิน (แสดงเมื่อมี)
        self._open_slip_ids = []
        self._slip_sig = None
        self._slip_job = None
        self._slip_flash = None
        self.order_bar = tk.Frame(self, bg=BG)      # แถบสถานะออเดอร์หลังร้าน (แสดงเมื่อมีออเดอร์ที่ยังไม่ได้รับ)
        self._prep_seen = None                      # {order_id: prep_seq ที่เห็นแล้ว} ไว้ดูว่าแอดมินกดแจ้งใหม่ไหม
        self._prep_sig = None
        self._prep_job = None
        self._toasts = []
        self.bottom_bar = self._build_bottom_bar()
        self.main = ScrollFrame(self, BG)
        self.main.pack(fill="both", expand=True)
        self._build_content(self.main.inner)
        self.main.canvas.bind("<Configure>", self._on_resize, add="+")

        self.render_shortcuts()
        self.render_reorder_strip()
        self.render_recommended()
        self.render_grid()
        self.refresh_cart_ui()
        self.refresh_slip_banner()
        self.refresh_order_status()

    def destroy(self):
        if self._slip_job:
            self.after_cancel(self._slip_job)
            self._slip_job = None
        if self._prep_job:
            self.after_cancel(self._prep_job)
            self._prep_job = None
        for t in self._toasts:                      # ออกจากระบบแล้วไม่ทิ้งแจ้งเตือนค้างไว้
            if t.winfo_exists():
                t.close()
        super().destroy()

    # ---------- โครงหน้า ----------
    def _build_header(self):
        """แถบบน: ซ้าย = โลโก้ร้าน / ขวา = สมาชิก (กดดูโปรไฟล์) แต้ม ตะกร้า ติดต่อ (หน้าผู้จัดทำ) ออกจากระบบ"""
        m = self.member
        bar = tk.Frame(self, bg=PANEL, height=84)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        logo_canvas(bar, 56).pack(side="left", padx=(24, 12))
        brand = tk.Frame(bar, bg=PANEL)
        brand.pack(side="left")
        tk.Label(brand, text="Meme Beans", bg=PANEL, fg=TEXT,
                 font=(FONT_SCRIPT, 17, "bold")).pack(anchor="w")
        tk.Label(brand, text="สั่งเครื่องดื่มล่วงหน้า  •  Coffee + Meme", bg=PANEL,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w")

        PillButton(bar, "ออกจากระบบ", self.on_logout, "dark_ghost", height=38,
                   size=10, padx=18).pack(side="right", padx=(10, 24))
        PillButton(bar, "ติดต่อ", lambda: CreditsDialog(self.app), "dark_ghost", height=38,
                   size=10, padx=16).pack(side="right", padx=(10, 0))
        self.cart_btn = CartButton(bar, self.open_cart)
        self.cart_btn.pack(side="right", padx=(14, 4))

        user = tk.Frame(bar, bg=PANEL)
        user.pack(side="right")
        av = tk.Canvas(user, width=52, height=52, bg=PANEL, highlightthickness=0)
        av.pack(side="right", padx=(10, 0))
        self.avatar = av
        self.avatar_ring = draw_avatar(av, 52, m, SURFACE_3, 2, photo_size=48)   # รูปโปรไฟล์ / ตัวอักษรแรก
        info = tk.Frame(user, bg=PANEL)
        info.pack(side="right")
        self.h_name = tk.Label(info, text=f"สวัสดี, {m['name']}", bg=PANEL, fg=TEXT,
                               font=(FONT, 11, "bold"))
        self.h_name.pack(anchor="e")
        pills = tk.Frame(info, bg=PANEL)
        pills.pack(anchor="e", pady=(4, 0))
        self.h_tier = Pill(pills, f"{m['tier']}  ›", SURFACE_2, TEXT)     # กดดูเกณฑ์ระดับสมาชิก
        self.h_tier.pack(side="right", padx=(6, 0))
        self.h_points = Pill(pills, f"★ {m['points']:,} แต้ม  ›", ACCENT, ACCENT_INK)
        self.h_points.pack(side="right")

        # กดที่รูป/ชื่อ เพื่อเปิดหน้าข้อมูลสมาชิก
        for w in (av, info, self.h_name, pills):
            w.bind("<Button-1>", lambda e: self.open_profile())
            w.bind("<Enter>", lambda e: restyle(av, self.avatar_ring, outline=ACCENT))
            w.bind("<Leave>", lambda e: restyle(av, self.avatar_ring, outline=SURFACE_3))
            w.config(cursor="hand2")

        # กดที่แต้ม เพื่อเปิดหน้าแต้มสะสม / แลกส่วนลด
        self.h_points.bind("<Button-1>", lambda e: self.open_points())
        self.h_points.bind("<Enter>", lambda e: self.h_points.set_fill(ACCENT_DARK))
        self.h_points.bind("<Leave>", lambda e: self.h_points.set_fill(ACCENT))
        self.h_points.config(cursor="hand2")

        # กดที่ระดับสมาชิก (Silver / Gold / Platinum) เพื่อดูเกณฑ์การเลื่อนระดับ
        self.h_tier.bind("<Button-1>", lambda e: self.open_tiers())
        self.h_tier.bind("<Enter>", lambda e: self.h_tier.set_fill(SURFACE_3))
        self.h_tier.bind("<Leave>", lambda e: self.h_tier.set_fill(SURFACE_2))
        self.h_tier.config(cursor="hand2")

    def refresh_header(self):
        m = self.member
        self.avatar_ring = draw_avatar(self.avatar, 52, m, SURFACE_3, 2, photo_size=48)
        self.h_name.config(text=f"สวัสดี, {m['name']}")
        self.h_points.set_text(f"★ {m['points']:,} แต้ม  ›")
        self.h_tier.set_text(f"{m['tier']}  ›")

    def open_tiers(self):
        """หน้าระดับสมาชิก: เกณฑ์การเลื่อนระดับ + อีกกี่แต้มถึงระดับถัดไป"""
        d = getattr(self, "tier_dialog", None)
        if d is not None and d.winfo_exists():
            d.lift()
            return
        self.tier_dialog = open_tier_dialog(self.app, self.member, self.refresh_header)

    def open_profile(self):
        d = getattr(self, "profile_dialog", None)
        if d is not None and d.winfo_exists():
            d.lift()
            return
        self.profile_dialog = ProfileDialog(self.app, self.member, self.refresh_header,
                                            on_history=self.open_history)

    def open_history(self):
        d = getattr(self, "history_dialog", None)
        if d is not None and d.winfo_exists():
            d.lift()
            return
        self.history_dialog = OrderHistoryDialog(self.app, self)

    # ---------- สั่งซ้ำ ----------
    def render_reorder_strip(self):
        """แถบ "สั่งซ้ำออเดอร์ล่าสุด" ใต้หมวดหมู่ (แสดงเมื่อเคยสั่งแล้ว)"""
        for w in self.reorder_box.winfo_children():
            w.destroy()
        orders = get_member_orders(self.member["member_id"], 1)
        if not orders:
            return
        o = orders[0]
        card = RoundFrame(self.reorder_box, fill=SURFACE, border=LINE, radius=18, padx=16, pady=12)
        card.pack(fill="x", padx=28, pady=(18, 0))
        c = card.inner
        icon = tk.Canvas(c, width=46, height=46, bg=SURFACE, highlightthickness=0)
        icon.pack(side="left", padx=(0, 14))
        aa_oval(icon, 1, 1, 45, 45, fill=ACCENT, outline="")
        crisp(icon, 8, 8, 38, 38, lambda d: icon_cup(d, 23 / .62, 25 / .62, ACCENT_INK),
              ("reorder_icon",), zoom=.62)
        PillButton(c, "สั่งซ้ำ", lambda: self.reorder(o), "primary", height=40, size=11,
                   padx=26).pack(side="right")
        PillButton(c, "ประวัติทั้งหมด", self.open_history, "secondary", height=40, size=10,
                   padx=18).pack(side="right", padx=(0, 8))
        col = tk.Frame(c, bg=SURFACE)
        col.pack(side="left", fill="x", expand=True)
        tk.Label(col, text="สั่งซ้ำออเดอร์ล่าสุด", bg=SURFACE, fg=TEXT,
                 font=(FONT, 12, "bold")).pack(anchor="w")
        cups = sum(it["quantity"] for it in o["items"])
        items = ", ".join(f"{it['quantity']}× {it['name']}" for it in o["items"])
        detail = f"{order_code(o['order_id'])}  •  {fmt_datetime(o['paid_at'])}  •  {cups} แก้ว: {items}"
        tk.Label(col, text=fit_text(detail, (FONT, 10), 560), bg=SURFACE, fg=TEXT_MUTED,
                 font=(FONT, 10)).pack(anchor="w")

    def reorder(self, order):
        """ใส่ทุกแก้วในออเดอร์เดิมลงตะกร้า (ตัวเลือกเดิม ราคาปัจจุบัน) แล้วเปิดตะกร้า
        เมนูที่ปิดขาย/หมดจะถูกข้าม และแต่ละเมนูใส่ได้ไม่เกินจำนวนที่สั่งได้ (10 แก้ว/สต็อกที่เหลือ)
        คืนค่าจำนวนแก้วที่เพิ่ม"""
        added, skipped, cut, changed = 0, [], [], False
        for it in order["items"]:
            p = get_product(it["product_id"])
            if p is None or not p["is_available"] or p["stock"] <= 0:
                skipped.append(it["name"])
                continue
            qty = min(it["quantity"], self.cups_left(p))
            if qty < it["quantity"]:
                cut.append(it["name"])
            if qty <= 0:
                continue
            size = size_from_options(it["options"])
            unit = p["price"] + SIZE_EXTRA.get(size, 0)
            changed = changed or abs(unit - it["unit_price"]) > 1e-9
            self.cart.add(p, it["options"] or "", qty, unit, size)
            added += qty
        self.refresh_cart_ui()
        notes = []
        if skipped:
            notes.append("เมนูที่หมดหรือปิดขายอยู่จึงไม่ได้เพิ่ม: " + ", ".join(dict.fromkeys(skipped)))
        if cut:
            notes.append(f"เพิ่มได้ไม่ครบ (สั่งได้ไม่เกิน {MAX_CUPS_PER_MENU} แก้วต่อเมนู หรือสต็อกเหลือน้อย): "
                         + ", ".join(dict.fromkeys(cut)))
        if changed:
            notes.append("ราคาบางเมนูเปลี่ยนจากครั้งก่อน ตะกร้าใช้ราคาปัจจุบัน")
        if not added:
            messagebox.showinfo("สั่งซ้ำไม่ได้", "\n".join(notes) or "เมนูในออเดอร์นี้หมดหรือปิดขายอยู่ทั้งหมด",
                                parent=self.app)
            return 0
        if notes:
            messagebox.showinfo("เพิ่มลงตะกร้าแล้ว", f"เพิ่ม {added} แก้วลงตะกร้าแล้ว\n\n" + "\n".join(notes),
                                parent=self.app)
        self.open_cart()
        return added

    def open_points(self):
        d = getattr(self, "points_dialog", None)
        if d is not None and d.winfo_exists():
            d.lift()
            return
        self.points_dialog = PointsDialog(self.app, self.member, self.refresh_header)

    def _build_bottom_bar(self):
        bar = tk.Frame(self, bg=ACCENT, height=66)
        bar.pack_propagate(False)
        self.bar_label = tk.Label(bar, text="", bg=ACCENT, fg=ACCENT_INK,
                                  font=(FONT, 12, "bold"))
        self.bar_label.pack(side="left", padx=28)
        PillButton(bar, "ดูตะกร้า  ›", self.open_cart, "dark", height=42,
                   padx=26).pack(side="right", padx=26)
        self.bar_total = tk.Label(bar, text="", bg=ACCENT, fg=ACCENT_INK,
                                  font=(FONT, 15, "bold"))
        self.bar_total.pack(side="right", padx=(0, 6))
        return bar

    def _build_content(self, root):
        self.hero = tk.Canvas(root, width=1020, height=206, bg=BG, highlightthickness=0)
        self.hero.pack(anchor="w", padx=28, pady=(22, 0))
        draw_hero(self.hero, 1020, 206)

        bar = tk.Frame(root, bg=BG)                       # หมวดหมู่ (ซ้าย) + ช่องค้นหาเมนู (ขวา)
        bar.pack(fill="x", padx=28, pady=(20, 0))
        self.shortcut_row = tk.Frame(bar, bg=BG)
        self.shortcut_row.pack(side="left")
        self.query = ""
        self.search_job = None
        self.search_box = SearchBox(bar, "ค้นหาเมนู เช่น ลาเต้, ชาไทย", self._on_search, width=290)
        self.search_box.pack(side="right")

        self.rec_box = tk.Frame(root, bg=BG)              # เมนูแนะนำ (ซ่อนตอนกำลังค้นหา)
        self.rec_box.pack(fill="x")
        self.reorder_box = tk.Frame(self.rec_box, bg=BG)  # แถบ "สั่งซ้ำออเดอร์ล่าสุด"
        self.reorder_box.pack(fill="x")
        head = tk.Frame(self.rec_box, bg=BG)
        head.pack(fill="x", padx=28, pady=(22, 8))
        section_title(head, "เมนูแนะนำ", icon_star).pack(side="left")
        Pill(head, "TRENDING", PINK, "white", size=9, height=22).pack(side="left", padx=10)
        for txt, d in (("›", 1), ("‹", -1)):
            PillButton(head, txt, lambda d=d: self.rec_row.scroll(d), "secondary",
                       height=36, size=13, padx=0).pack(side="right", padx=(8, 0))
        tk.Frame(head, bg=LINE, height=1).pack(side="left", fill="x", expand=True, padx=(4, 8))
        self.rec_row = HScrollRow(self.rec_box, BG, self.CARD_H + 12)
        self.rec_row.pack(fill="x", padx=22)

        self.grid_frame = tk.Frame(root, bg=BG)          # เมนูทั้งหมด แยกเป็นหมวด
        self.grid_frame.pack(fill="x", pady=(4, 30))

    # ---------- หมวดหมู่ (ชิปมีไอคอน แบบแอปสั่งอาหาร) ----------
    def render_shortcuts(self):
        for w in self.shortcut_row.winfo_children():
            w.destroy()
        items = [(None, "ทั้งหมด", icon_all)] + [
            (cid, category_label(name), icon_for(name)) for cid, name in self.categories]
        font = (FONT, 11, "bold")
        for cid, name, icon in items:
            active = (cid == self.selected_cat)
            W, H = text_width(name, font) + 60, 42
            c = tk.Canvas(self.shortcut_row, width=W, height=H, bg=BG, highlightthickness=0,
                          cursor="hand2")
            c.pack(side="left", padx=(0, 10))
            pill = rounded_rect(c, 1, 1, W - 1, H - 1, 20, fill=ACCENT if active else SURFACE_2,
                                outline=ACCENT if active else LINE)
            col = ACCENT_INK if active else TEXT
            crisp(c, 12, 9, 36, 33, lambda d, icon=icon, col=col: icon(d, 24 / .5, 21 / .5, col),
                  ("chip", icon.__name__, col), zoom=.5)
            c.create_text(42, H / 2, anchor="w", text=name, fill=col, font=font)
            c.bind("<Button-1>", lambda e, cid=cid: self.select_category(cid))
            if not active:
                c.bind("<Enter>", lambda e, c=c, r=pill: restyle(c, r, outline=TEXT_MUTED))
                c.bind("<Leave>", lambda e, c=c, r=pill: restyle(c, r, outline=LINE))

    def select_category(self, cid):
        self.selected_cat = cid
        self.render_shortcuts()
        self.render_grid()

    # ---------- ค้นหาเมนู ----------
    def _on_search(self, text):
        """พิมพ์ในช่องค้นหา: รอให้หยุดพิมพ์แป๊บหนึ่งแล้วค่อยกรองเมนู (ไม่กระตุกตอนพิมพ์เร็ว)"""
        if self.search_job:
            self.after_cancel(self.search_job)
        self.search_job = self.after(180, self._apply_search, text)

    def _apply_search(self, text):
        self.search_job = None
        query = text.strip().lower()
        if query == self.query:
            return
        was_searching = bool(self.query)
        self.query = query
        if query and not was_searching:
            self.rec_box.pack_forget()
        elif not query and was_searching:
            self.rec_box.pack(fill="x", before=self.grid_frame)
        self.render_grid()
        self.main.canvas.yview_moveto(0)

    # ---------- การ์ดเมนู ----------
    TEMP_EN = {"ร้อน": "HOT", "เย็น": "COLD", "ปั่น": "FRAPPE"}

    def product_card(self, parent, p, hot=0):
        """การ์ดเมนูแบบป้ายเมนูร้านกาแฟ: ชื่อตัวใหญ่สีทอง / คำอธิบาย / รูปแก้วเครื่องดื่ม (มีม) /
        HOT-COLD-FRAPPE / ราคา / ปุ่ม +   (hot = อันดับขายดี 1-3 มีสติกเกอร์ HOT)"""
        W, H = self.card_w, self.CARD_H
        c = tk.Canvas(parent, width=W, height=H, bg=bg_of(parent), highlightthickness=0)
        frame = rounded_rect(c, 1, 1, W - 1, H - 1, 16, fill=DRINK_CARD, outline=DRINK_LINE,
                             width=1)
        title = p["name"].upper()
        if text_width(title, self.title_font) > W - 28:
            title = p["name"]                 # ชื่อยาว: ใช้ตัวพิมพ์ปกติ (แคบกว่า) ก่อน
        size = self.TITLE_SIZE
        while size > self.TITLE_SIZE - 2 and text_width(title, (FONT, size, "bold")) > W - 28:
            size -= 1                         # ยังยาวอยู่: ลดขนาดลงได้อีก 2 ขั้น (ยาวกว่านั้นตัด …)
        title_font = (FONT, size, "bold")
        c.create_text(14, 13, anchor="nw", fill=GOLD, font=title_font,
                      text=fit_text(title, title_font, W - 28))
        # คำอธิบาย: สูงสุด 3 บรรทัด ตัดบรรทัดตรงรอยต่อคำ  ยาวเกินลงท้าย … แล้วชี้เมาส์ค้างอ่านเต็มได้
        desc = " ".join((p.get("description") or "").split())
        lines = wrap_text(desc, self.desc_font, W - 28, self.DESC_LINES)
        for i, line in enumerate(lines):
            c.create_text(14, self.desc_top + i * self.desc_line_h, anchor="nw", fill=MENU_DESC,
                          font=self.desc_font, text=line)
        img_top = self.img_top                    # เว้นที่ 3 บรรทัดทุกการ์ด รูปจะได้ตรงกัน
        img_h = self.IMG_H
        photo = load_product_image(p, self.CARD_W - 2, img_h)    # รูปขนาดเท่าเดิมแม้การ์ดยืด
        if photo is not None:                     # images/<ชื่อเมนู>.png
            c.create_image(W // 2, img_top + img_h // 2, image=photo)
            c.photo = photo                       # กันรูปถูกเก็บทิ้ง
        else:
            c.create_text(W // 2, img_top + img_h // 2, text="NO PIC, JUST VIBES",
                          fill="#4A4038", font=(FONT_MEME, 12))
        if hot:
            sx, sy = 30, img_top + 24
            aa_oval(c, sx - 20, sy - 20, sx + 20, sy + 20, fill=PINK, outline=DRINK_CARD, width=2)
            c.create_text(sx, sy - 4, text="HOT", fill="white", font=(FONT_MEME, 11), angle=12)
            c.create_text(sx, sy + 9, text=f"#{hot}", fill="white", font=(FONT, 9, "bold"))
        # แถวล่าง: แบบที่สั่งได้ + ราคา + ปุ่ม +
        c.create_line(14, H - 64, W - 14, H - 64, fill=DRINK_LINE)
        cat_name = dict(self.categories).get(p.get("category_id"), "")
        temps, _ = temps_for(p, cat_name)
        c.create_text(14, H - 49, anchor="w", fill=TEXT_MUTED, font=(FONT, 10, "bold"),
                      text=" · ".join(self.TEMP_EN.get(t, t) for t in temps))
        c.create_text(14, H - 21, anchor="w", text=f"฿{fmt_price(p['price'])}",
                      fill=TEXT, font=(FONT, 16, "bold"))
        status = stock_status(p["stock"])
        if p["is_available"] and status == "low":          # ป้ายเตือนของใกล้หมด (มุมขวาบนของรูป)
            text = f"เหลือ {p['stock']} แก้ว"
            font = (FONT, 9, "bold")
            tw = text_width(text, font) + 18
            rounded_rect(c, W - 10 - tw, img_top + 6, W - 10, img_top + 30, 12, fill=PINK, outline=PINK)
            c.create_text(W - 10 - tw / 2, img_top + 18, text=text, fill="white", font=font)
        if p["is_available"] and status != "out":
            plus = aa_oval(c, W - 50, H - 40, W - 14, H - 4, fill=ACCENT, outline="")
            cx, cy = W - 32, H - 22
            c.create_line(cx - 7, cy, cx + 7, cy, fill=ACCENT_INK, width=3, capstyle="round")
            c.create_line(cx, cy - 7, cx, cy + 7, fill=ACCENT_INK, width=3, capstyle="round")

            def hover(on):
                restyle(c, frame, outline=GOLD if on else DRINK_LINE)
                restyle(c, plus, fill=ACCENT_DARK if on else ACCENT)

            c.bind("<Enter>", lambda e: hover(True))
            c.bind("<Leave>", lambda e: hover(False))
            c.bind("<Button-1>", lambda e, p=p: self.open_options(p))
            c.config(cursor="hand2")
        else:
            rounded_rect(c, W - 90, H - 36, W - 14, H - 8, 14, fill=SURFACE_2, outline=LINE)
            c.create_text(W - 52, H - 22, text="SOLD OUT", fill=TEXT_MUTED, font=(FONT, 9, "bold"))
        if lines and lines[-1].endswith("…") and not desc.endswith("…"):
            HoverTip(c, desc, title=p["name"])           # ผูกหลัง c.bind ด้านบน (ใช้ add="+" ต่อท้าย)
        return c

    def render_recommended(self):
        inner = self.rec_row.inner
        for w in inner.winfo_children():
            w.destroy()
        for rank, p in enumerate(get_popular_products(8), 1):
            self.product_card(inner, p, hot=rank if rank <= 3 else 0).pack(
                side="left", padx=6, pady=4)

    def _calc_layout(self):
        """จำนวนคอลัมน์ + ความกว้างการ์ด: ใส่ได้กี่ใบต่อแถว แล้วยืดการ์ดเท่า ๆ กันให้เต็มแถวพอดี"""
        w = self.main.canvas.winfo_width()
        if w < 100:
            return self.cols, self.card_w
        avail = w - 40
        cols = max(3, avail // (self.CARD_W + 16))
        return cols, max(self.CARD_W, avail // cols - 16)

    def _on_resize(self, e=None):
        """ขนาดหน้าต่างเปลี่ยน (เช่น กดขยายเต็มจอ): วาดแบนเนอร์ใหม่ และจัดคอลัมน์การ์ดใหม่"""
        if self.resize_job:
            self.after_cancel(self.resize_job)
        self.resize_job = self.after(60, self._apply_resize)

    def _apply_resize(self):
        self.resize_job = None
        w = self.main.canvas.winfo_width() - 56
        if w > 200 and w != getattr(self, "hero_w", None):
            self.hero_w = w
            self.hero.config(width=w)
            draw_hero(self.hero, w, 206)
        cols, card_w = self._calc_layout()
        if card_w != self.card_w:                 # การ์ดกว้างขึ้น/แคบลง: วาดการ์ดใหม่ทั้งหมด
            self.render_grid()
            self.render_recommended()
        elif cols != self.cols:
            self.cols = cols
            for cards in self.grid_sections:
                for i, card in enumerate(cards):
                    card.grid_configure(row=i // cols, column=i % cols)

    def render_grid(self):
        """เมนูทั้งหมด แยกเป็นหมวด (หัวข้อมีไอคอน + เส้นคั่น) ถ้าเลือกหมวดไว้จะแสดงหมวดเดียว"""
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.grid_sections = []
        self.cols, self.card_w = self._calc_layout()
        for cid, name in self.categories:
            if self.selected_cat not in (None, cid):
                continue
            products = get_products(cid)
            if self.query:                                  # กำลังค้นหา: เหลือเฉพาะเมนูที่ตรง
                products = [p for p in products
                            if self.query in search_text(p, category_label(name))]
            if not products:
                continue
            head = tk.Frame(self.grid_frame, bg=BG)
            head.pack(fill="x", padx=28, pady=(24, 8))
            note = f"พบ {len(products)} เมนู" if self.query else f"{len(products)} เมนู"
            section_title(head, category_label(name), icon_for(name), note).pack(side="left")
            tk.Frame(head, bg=LINE, height=1).pack(side="left", fill="x", expand=True, padx=(14, 0))
            grid = tk.Frame(self.grid_frame, bg=BG)
            grid.pack(anchor="w", padx=20)
            cards = []
            for i, p in enumerate(products):
                card = self.product_card(grid, p)
                card.grid(row=i // self.cols, column=i % self.cols, padx=8, pady=9)
                cards.append(card)
            self.grid_sections.append(cards)
        if not self.grid_sections and self.query:
            box = tk.Frame(self.grid_frame, bg=BG)
            box.pack(anchor="w", padx=28, pady=(30, 20))
            tk.Label(box, text=f"ไม่พบเมนู \"{self.search_box.get()}\"", bg=BG, fg=TEXT,
                     font=(FONT, 16, "bold")).pack(anchor="w")
            where = "ในหมวดนี้ " if self.selected_cat is not None else ""
            tk.Label(box, text=f"ลองพิมพ์คำอื่น {where}เช่น ชื่อเมนู (Latte) หรือรสชาติ (นม, ผลไม้, ช็อกโกแลต)",
                     bg=BG, fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w", pady=(4, 12))
            buttons = tk.Frame(box, bg=BG)
            buttons.pack(anchor="w")
            PillButton(buttons, "ล้างคำค้นหา", self.search_box.clear, "secondary", height=38,
                       size=10, padx=18).pack(side="left")
            if self.selected_cat is not None:
                PillButton(buttons, "ค้นหาทุกหมวด", lambda: self.select_category(None), "secondary",
                           height=38, size=10, padx=18).pack(side="left", padx=(8, 0))
        elif not self.grid_sections:
            tk.Label(self.grid_frame, text="ยังไม่มีเมนูในหมวดนี้", bg=BG, fg=TEXT_MUTED,
                     font=(FONT, 11)).pack(anchor="w", padx=28, pady=20)

    def open_options(self, product):
        fresh = get_product(product["product_id"]) or product      # อ่านสต็อกล่าสุด
        left = self.cups_left(fresh)
        if left <= 0:
            messagebox.showinfo("สั่งเพิ่มไม่ได้", self.limit_text(fresh), parent=self.app)
            self.render_grid()
            return
        if fresh["stock"] < MAX_CUPS_PER_MENU:
            hint = f"เหลือในสต็อก {fresh['stock']} แก้ว"
        elif left < MAX_CUPS_PER_MENU:
            hint = f"สั่งเพิ่มได้อีก {left} แก้ว (สูงสุด {MAX_CUPS_PER_MENU} แก้วต่อเมนู)"
        else:
            hint = ""
        cat_name = dict(self.categories).get(product["category_id"], "")
        temps, default = temps_for(product, cat_name)
        OptionDialog(self.app, fresh, self.add_to_cart, temps, default, max_qty=left, qty_hint=hint)

    # ---------- จำกัดจำนวนแก้วต่อเมนู ----------
    def cups_left(self, product):
        """เมนูนี้ใส่ตะกร้าเพิ่มได้อีกกี่แก้ว (ไม่เกิน 10 แก้วต่อเมนู และไม่เกินสต็อกที่เหลือ)"""
        return cup_limit(product["stock"]) - self.cart.cups_of(product["product_id"])

    def limit_text(self, product):
        """ข้อความอธิบายว่าทำไมสั่งเพิ่มไม่ได้"""
        name, stock = product["name"], product["stock"]
        in_cart = self.cart.cups_of(product["product_id"])
        if stock <= 0:
            return f"{name} หมดแล้ว"
        if stock < MAX_CUPS_PER_MENU:
            return f"{name} เหลือในสต็อก {stock} แก้ว (ในตะกร้ามี {in_cart} แก้วแล้ว)"
        return f"{name} สั่งได้สูงสุด {MAX_CUPS_PER_MENU} แก้วต่อออเดอร์ (ในตะกร้ามี {in_cart} แก้วแล้ว)"

    def full_menus(self):
        """เมนูในตะกร้าที่ครบจำนวนที่สั่งได้แล้ว {product_id: ข้อความสั้น}"""
        out = {}
        for pid in {it["product_id"] for it in self.cart.items}:
            p = get_product(pid)
            if p is not None and self.cups_left(p) <= 0:
                out[pid] = (f"สต็อกมีแค่ {p['stock']} แก้ว" if p["stock"] < MAX_CUPS_PER_MENU
                            else f"ครบ {MAX_CUPS_PER_MENU} แก้วแล้ว")
        return out

    def _cart_notice(self, text):
        d = self.cart_dialog
        if d is not None and d.winfo_exists():
            d.show_notice(text)
        else:
            messagebox.showinfo("สั่งเพิ่มไม่ได้", text, parent=self.app)

    # ---------- ตะกร้า ----------
    def add_to_cart(self, product, options, qty, unit_price=None, size=None):
        fresh = get_product(product["product_id"]) or product
        qty = min(qty, self.cups_left(fresh))                    # กันใส่เกินจำนวนที่สั่งได้
        if qty <= 0:
            self._cart_notice(self.limit_text(fresh))
            return
        self.cart.add(product, options, qty, unit_price, size)
        self.refresh_cart_ui()

    def change_qty(self, index, delta):
        if delta > 0:
            p = get_product(self.cart.items[index]["product_id"])
            if p is not None and self.cups_left(p) < delta:
                self._cart_notice(self.limit_text(p))
                return
        self.cart.change(index, delta)
        self.refresh_cart_ui()

    def remove_item(self, index):
        self.cart.remove(index)
        self.refresh_cart_ui()

    def clear_cart(self):
        self.cart.clear()
        self.refresh_cart_ui()

    def refresh_cart_ui(self):
        n = self.cart.count()
        self.cart_btn.set_count(n)
        if n:
            self.bar_label.config(text=f"ตะกร้า  •  {n} รายการ")
            self.bar_total.config(text=f"฿{fmt_price(self.cart.total())}")
            self.bottom_bar.pack(side="bottom", fill="x", before=self.main)
        else:
            self.bottom_bar.pack_forget()
        d = self.cart_dialog
        if d is not None and d.winfo_exists():
            d.render()

    def open_cart(self):
        d = self.cart_dialog
        if d is not None and d.winfo_exists():
            d.lift()
            return
        self.cart_dialog = CartDialog(self.app, self)

    def checkout(self, dialog=None):
        """กด 'ยืนยันการสั่งซื้อ': สร้างออเดอร์สถานะ pending แล้วเปิดหน้าชำระเงิน"""
        if self.cart.is_empty():
            messagebox.showwarning("ตะกร้าว่าง", "กรุณาเลือกเมนูก่อนสั่งซื้อ")
            return
        fresh = get_member(self.member["member_id"])
        if fresh and fresh.get("banned"):         # ถูกแบนระหว่างใช้งาน: แจ้งแล้วออกจากระบบ
            reason = f"\nเหตุผล: {fresh['ban_reason']}" if fresh.get("ban_reason") else ""
            if dialog is not None and dialog.winfo_exists():
                dialog.destroy()
            messagebox.showerror("บัญชีถูกระงับ", f"บัญชีนี้ถูกระงับการใช้งาน กรุณาติดต่อพนักงานที่ร้าน{reason}",
                                 parent=self.app)
            self.on_logout()
            return
        try:
            order_id, _ = create_order(self.member["member_id"], self.cart.items)
        except Exception as e:
            messagebox.showerror("ผิดพลาด", f"บันทึกออเดอร์ไม่สำเร็จ\n{e}")
            return
        try:
            PaymentDialog(self.app, self, order_id, dialog)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("เปิดหน้าชำระเงินไม่สำเร็จ",
                                 f"{type(e).__name__}: {e}\n\n(ออเดอร์ถูกยกเลิกแล้ว ตะกร้ายังอยู่)")

    def on_paid(self):
        """เรียกหลังชำระเงินสำเร็จ (หรือส่งสลิปแล้ว): ล้างตะกร้า และรีเฟรชหน้าเมนู"""
        self.cart.clear()
        self.refresh_after_payment()

    def refresh_after_payment(self, banner=True):
        """รีเฟรชแต้ม/ระดับสมาชิกบนหัวหน้าเมนู สต็อกบนการ์ดเมนู และแถบสลิป (ไม่แตะตะกร้า)"""
        fresh = get_member(self.member["member_id"])
        if fresh:
            self.member.update(fresh)
        self.refresh_header()
        self.refresh_cart_ui()
        self.render_reorder_strip()
        self.render_recommended()
        self.render_grid()                     # สต็อกลดแล้ว: อัปเดตป้าย "เหลือ N แก้ว" / SOLD OUT
        if banner:
            self.refresh_slip_banner()
        self.refresh_order_status()            # ออเดอร์ที่เพิ่งจ่ายขึ้นแถบสถานะทันที

    # ---------- แจ้งสถานะสลิปโอนเงิน (จ่ายด้วย QR พร้อมเพย์) ----------
    def refresh_slip_banner(self):
        """แถบใต้หัวหน้าเมนู: ออเดอร์ที่ส่งสลิปแล้ว "รอร้านตรวจ" / "สลิปไม่ผ่าน" / "ร้านยืนยันแล้ว"
        ระหว่างมีสลิปรอตรวจจะเช็กซ้ำทุก 3 วินาที (แอดมินยืนยันจากอีกหน้าต่าง/อีกเครื่องก็เห็นทันที)"""
        if self._slip_job:
            self.after_cancel(self._slip_job)
            self._slip_job = None
        if not self.winfo_exists():
            return
        slips = get_member_open_slips(self.member["member_id"])
        now_ids = {x["order_id"] for x in slips}
        for oid in [o for o in self._open_slip_ids if o not in now_ids]:   # หายจากรายการ = จบแล้ว
            st = get_payment_state(oid)
            if st and st["status"] == "paid":
                self._slip_flash = [f"ร้านยืนยันการชำระเงินออเดอร์ {order_code(oid)} แล้ว", 3]
                self.refresh_after_payment(banner=False)        # แต้มเพิ่ม + สต็อกลด
        self._open_slip_ids = [x["order_id"] for x in slips]
        flash = self._slip_flash[0] if self._slip_flash else None
        sig = (tuple((x["order_id"], x["status"], x["note"]) for x in slips), flash)
        if sig != self._slip_sig:
            self._slip_sig = sig
            self._draw_slip_bar(slips, flash)
        if self._slip_flash:                                    # ข้อความ "ยืนยันแล้ว" แสดงราว 9 วินาที
            self._slip_flash[1] -= 1
            if self._slip_flash[1] < 0:
                self._slip_flash = None
        if slips or flash:
            self._slip_job = self.after(3000, self.refresh_slip_banner)

    def _draw_slip_bar(self, slips, flash):
        bar = self.slip_bar
        for w in bar.winfo_children():
            w.destroy()
        if not slips and not flash:
            bar.pack_forget()
            return
        bar.pack(fill="x", before=self.main)
        rows = [("ok", flash, None)] if flash else []
        for x in slips:
            if x["status"] == "rejected":
                rows.append(("bad", f"สลิปออเดอร์ {order_code(x['order_id'])} ไม่ผ่านการตรวจสอบ: "
                                    f"{x['note'] or '-'}", x["order_id"]))
            else:
                rows.append(("wait", f"ออเดอร์ {order_code(x['order_id'])} ส่งสลิปแล้ว  •  "
                                     f"รอร้านตรวจสอบ (฿{fmt_price(x['amount'])})", x["order_id"]))
        colors = {"ok": ("#16301F", SUCCESS), "wait": ("#2E2812", ACCENT), "bad": ("#3E1C19", ERROR)}
        for kind, text, oid in rows:
            bg, dot = colors[kind]
            row = tk.Frame(bar, bg=bg)
            row.pack(fill="x")
            inner = tk.Frame(row, bg=bg)
            inner.pack(fill="x", padx=24, pady=7)
            d = tk.Canvas(inner, width=12, height=12, bg=bg, highlightthickness=0)
            d.pack(side="left")
            aa_oval(d, 1, 1, 11, 11, fill=dot, outline="")
            tk.Label(inner, text=text, bg=bg, fg=TEXT, font=(FONT, 11, "bold")).pack(side="left", padx=(10, 0))
            if oid is not None:
                PillButton(inner, "แนบสลิปใหม่" if kind == "bad" else "ดูสถานะ",
                           lambda o=oid: self.open_slip(o), "primary" if kind == "bad" else "secondary",
                           height=32, size=10, padx=16).pack(side="right")

    # ---------- สถานะออเดอร์หลังร้าน (รอคิว / กำลังทำ / พร้อมรับ) ----------
    def refresh_order_status(self):
        """แถบ "ออเดอร์ของคุณ" ใต้หัวหน้าเมนู + แจ้งเตือนเด้งเมื่อแอดมินเปลี่ยนสถานะ (เช็กทุก 3 วินาที)
        เข้าระบบมาตอนออเดอร์พร้อมรับอยู่แล้ว ก็เด้งแจ้งให้ทันที"""
        if self._prep_job:
            self.after_cancel(self._prep_job)
            self._prep_job = None
        if not self.winfo_exists():
            return
        orders = get_member_active_orders(self.member["member_id"])
        first, seen = self._prep_seen is None, self._prep_seen or {}
        now_ids = {o["order_id"] for o in orders}
        for oid in [i for i in seen if i not in now_ids]:          # หายจากรายการ = ลูกค้ารับแล้ว
            o = get_order_prep(oid)
            if o and o["prep_status"] == "picked_up" and o["prep_seq"] > seen[oid]:
                self._notify_prep(o)
        for o in orders:
            old = seen.get(o["order_id"])
            if first:
                if o["prep_status"] == "ready":
                    self._notify_prep(o)
            elif (o["prep_seq"] > old) if old is not None else o["prep_seq"] > 0:
                self._notify_prep(o)
        self._prep_seen = {o["order_id"]: o["prep_seq"] for o in orders}
        sig = tuple((o["order_id"], o["prep_status"], o["cups_done"], o["ahead_orders"], o["ahead_cups"],
                     o["wait_minutes"]) for o in orders)
        if sig != self._prep_sig:
            self._prep_sig = sig
            self._draw_order_bar(orders)
        self._prep_job = self.after(3000, self.refresh_order_status)

    def _notify_prep(self, o):
        """เด้งแจ้งเตือนบนหน้าต่างที่ลูกค้าเห็นอยู่ (ถ้าเปิดหน้าต่างย่อยอยู่ก็ขึ้นบนหน้าต่างนั้น)"""
        self._toasts = [t for t in self._toasts if t.winfo_exists()]
        for t in self._toasts:                      # ออเดอร์เดิมมีแจ้งเตือนค้างอยู่ -> แทนที่ด้วยอันใหม่
            if t.order_id == o["order_id"]:
                t.close()
        self._toasts.append(OrderToast(top_window(self.app), o, self.open_order_status))

    def _draw_order_bar(self, orders):
        bar = self.order_bar
        for w in bar.winfo_children():
            w.destroy()
        if not orders:
            bar.pack_forget()
            return
        bar.pack(fill="x", before=self.main)
        for o in orders:
            st = o["prep_status"]
            bg = PREP_TINT[st]
            row = tk.Frame(bar, bg=bg)
            row.pack(fill="x")
            inner = tk.Frame(row, bg=bg)
            inner.pack(fill="x", padx=24, pady=6)
            icon = tk.Canvas(inner, width=30, height=30, bg=bg, highlightthickness=0)
            icon.pack(side="left")
            draw_prep_icon(icon, 15, 15, 30, st)
            tk.Label(inner, text=f"ออเดอร์ {order_code(o['order_id'])}", bg=bg, fg=TEXT,
                     font=(FONT, 11, "bold")).pack(side="left", padx=(10, 0))
            Pill(inner, "พร้อมรับแล้ว!" if st == "ready" else PREP_LABEL[st], PREP_COLORS[st], ACCENT_INK,
                 size=9, height=24, padx=10).pack(side="left", padx=(8, 0))
            tk.Label(inner, text=prep_detail(o), bg=bg, fg=TEXT if st == "ready" else TEXT_MUTED,
                     font=(FONT, 10, "bold" if st == "ready" else "normal")).pack(side="left", padx=(10, 0))
            PillButton(inner, "ติดตามออเดอร์", lambda oid=o["order_id"]: self.open_order_status(oid),
                       "primary" if st == "ready" else "secondary", height=32, size=10,
                       padx=16).pack(side="right")
            steps = tk.Canvas(inner, width=118, height=30, bg=bg, highlightthickness=0)
            steps.pack(side="right", padx=(0, 14))
            draw_mini_steps(steps, st, bg)

    def open_order_status(self, order_id):
        """เปิดหน้าติดตามออเดอร์ (กดจากแถบสถานะ แจ้งเตือน หรือหน้าชำระเงินสำเร็จ)
        ถ้ามีหน้าต่างย่อยเปิดอยู่ (เช่น หน้าปรับแต่งเครื่องดื่ม) จะเปิดซ้อน ปิดแล้วกลับไปหน้าต่างเดิม"""
        d = getattr(self, "status_dialog", None)
        if d is not None and d.winfo_exists():
            if d.order_id == order_id:
                d.lift()
                return
            d.destroy()
        top = top_window(self.app)
        self.status_dialog = dlg = OrderStatusDialog(top, order_id)
        if top is not self.app:
            top.wait_window(dlg)
            if top.winfo_exists():
                grab_modal(top)

    def open_slip(self, order_id):
        """เปิดหน้าสถานะการชำระเงินของออเดอร์ที่ส่งสลิปแล้ว"""
        d = getattr(self, "slip_dialog", None)
        if d is not None and d.winfo_exists():
            if d.order_id == order_id:
                d.lift()
                return
            d.destroy()
        self.slip_dialog = PaymentDialog(self.app, self, order_id, resume=True)


# =====================================================================
# ส่วนที่ 21: แอปหลัก + หน้าล็อกอิน / สมัครสมาชิก
#   ประกอบด้วย: ForgotPasswordDialog (ลืมรหัสผ่าน: ส่งรหัสยืนยันทางอีเมล),
#              class CoffeeApp: หน้าต่างหลัก, show_login, show_register, show_menu, logout,
#              class CustomerWindow: หน้าต่าง "หน้าลูกค้า" ที่เปิดจากหน้าแอดมิน (ใช้พร้อมกับหน้าแอดมินได้)
# บรรทัด 5784 - 6224
# =====================================================================
class ForgotPasswordDialog(tk.Toplevel):
    """ลืมรหัสผ่าน: กรอกเบอร์โทร -> ส่งรหัสยืนยัน 6 หลักไปที่อีเมลสมาชิก -> ตั้งรหัสผ่านใหม่"""

    def __init__(self, app, phone="", on_done=None):
        super().__init__(app)
        self.app, self.on_done = app, on_done
        self.member, self.phone, self.step = None, "", "phone"
        self._send_result = None
        self.title("ลืมรหัสผ่าน")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(app)
        w, h = 440, 530
        x = app.winfo_rootx() + (app.winfo_width() - w) // 2
        y = app.winfo_rooty() + (app.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=30, pady=24)
        self.bind("<Return>", lambda e: self.request_code() if self.step == "phone" else self.save())
        self.show_phone(phone)
        try:
            grab_modal(self)
        except tk.TclError:
            pass

    def _page(self, title_text, sub):
        for w in self.body.winfo_children():
            w.destroy()
        head = tk.Frame(self.body, bg=BG)
        head.pack(anchor="w", pady=(0, 8))
        logo_canvas(head, 44).pack(side="left", padx=(0, 12))
        tk.Label(head, text=title_text, bg=BG, fg=TEXT, font=(FONT, 18, "bold")).pack(side="left")
        tk.Label(self.body, text=sub, bg=BG, fg=TEXT_MUTED, font=(FONT, 11), wraplength=380,
                 justify="left").pack(anchor="w")

    def _message(self):
        self.msg = tk.Label(self.body, text="", bg=BG, fg=ERROR, font=(FONT, 11), wraplength=380,
                            justify="left")
        self.msg.pack(anchor="w", pady=(8, 0))

    # ---- ขั้นที่ 1: กรอกเบอร์โทร ----
    def show_phone(self, phone=""):
        self.step = "phone"
        self._page("ลืมรหัสผ่าน", "กรอกเบอร์โทรที่ใช้สมัครสมาชิก ระบบจะส่งรหัสยืนยัน 6 หลัก"
                                  "ไปที่อีเมลที่คุณบันทึกไว้")
        self.f_phone = make_field(self.body, "เบอร์โทรศัพท์")
        self.f_phone.insert(0, phone)
        self._message()
        self.send_btn = make_button(self.body, "ส่งรหัสยืนยัน", self.request_code, height=46)
        self.send_btn.pack(fill="x", pady=(10, 8))
        make_button(self.body, "กลับไปหน้าเข้าสู่ระบบ", self.destroy, primary=False).pack(fill="x")
        self.f_phone.focus_set()

    def request_code(self):
        """ขอรหัสยืนยัน (ใช้ทั้งปุ่ม "ส่งรหัสยืนยัน" และลิงก์ "ส่งรหัสอีกครั้ง")"""
        if self._send_result is False:          # กำลังส่งอยู่
            return
        phone = self.f_phone.get().strip() if self.step == "phone" else self.phone
        m = find_member_by_phone(phone) if phone else None
        if m is None:
            self.msg.config(text="ไม่พบเบอร์นี้ในระบบ กรุณาตรวจสอบอีกครั้ง", fg=ERROR)
            return
        if not m["email"]:
            self.msg.config(text="บัญชีนี้ยังไม่ได้บันทึกอีเมล จึงส่งรหัสยืนยันไม่ได้\n"
                                 "กรุณาติดต่อพนักงานที่ร้านเพื่อตั้งรหัสผ่านใหม่", fg=ERROR)
            return
        code, err = create_reset_code(m["member_id"])
        if code is None:
            self.msg.config(text=err, fg=ERROR)
            return
        self.member, self.phone = m, phone
        self.msg.config(text="กำลังส่งรหัสยืนยัน...", fg=TEXT_MUTED)
        if self.step == "phone":
            self.send_btn.config(state="disabled", text="กำลังส่ง...")
        self._send_result = False

        def work():
            try:
                send_reset_code_email(m["email"], m["name"], code)
                self._send_result = (True, "")
            except Exception as e:              # ส่งอีเมลไม่ได้ (ยังไม่ตั้งค่า/เน็ตหลุด/รหัสผิด)
                self._send_result = (False, explain_email_error(e))

        threading.Thread(target=work, daemon=True).start()
        self.after(150, self._poll_send)

    def _poll_send(self):
        try:
            if not self.winfo_exists():
                return
        except tk.TclError:
            return
        if self._send_result is False:
            self.after(150, self._poll_send)
            return
        ok, err = self._send_result
        self._send_result = None
        if ok:
            self.show_code()
            return
        cancel_reset_code(self.member["member_id"])
        if self.step == "phone":
            self.send_btn.config(state="normal", text="ส่งรหัสยืนยัน")
        self.msg.config(text=f"ส่งรหัสยืนยันไม่สำเร็จ: {err}", fg=ERROR)

    # ---- ขั้นที่ 2: กรอกรหัสยืนยัน + รหัสผ่านใหม่ ----
    def show_code(self):
        self.step = "code"
        self._page("ตั้งรหัสผ่านใหม่", f"ส่งรหัสยืนยันไปที่ {mask_email(self.member['email'])} แล้ว "
                                       f"รหัสใช้ได้ {RESET_CODE_MINUTES} นาที "
                                       "(ถ้าไม่เห็นอีเมล ลองดูในโฟลเดอร์สแปม)")
        self.f_code = make_field(self.body, "รหัสยืนยัน 6 หลัก", compact=True)
        self.f_new = make_password_field(self.body, "รหัสผ่านใหม่", compact=True)
        self.f_new2 = make_field(self.body, "ยืนยันรหัสผ่านใหม่", show="•", compact=True)
        self._message()
        make_button(self.body, "ตั้งรหัสผ่านใหม่", self.save, height=46).pack(fill="x", pady=(8, 6))
        links = tk.Frame(self.body, bg=BG)
        links.pack(fill="x")
        LinkButton(links, "ไม่ได้รับรหัส? ส่งอีกครั้ง", self.request_code).pack(side="left")
        LinkButton(links, "เปลี่ยนเบอร์", lambda: self.show_phone(self.phone)).pack(side="right")
        self.f_code.focus_set()

    def save(self):
        problem = password_problem(self.f_new.get())
        if problem:
            self.msg.config(text=problem, fg=ERROR)
            return
        if self.f_new.get() != self.f_new2.get():
            self.msg.config(text="รหัสผ่านใหม่ทั้งสองช่องไม่ตรงกัน", fg=ERROR)
            return
        ok, text = reset_password_with_code(self.member["member_id"], self.f_code.get(),
                                            self.f_new.get())
        if not ok:
            self.msg.config(text=text, fg=ERROR)
            return
        messagebox.showinfo("สำเร็จ", "ตั้งรหัสผ่านใหม่เรียบร้อย\nกรุณาเข้าสู่ระบบด้วยรหัสผ่านใหม่",
                            parent=self)
        phone = self.phone
        self.destroy()
        if self.on_done:
            self.on_done(phone)


class CoffeeApp(tk.Tk):
    admin_link = True             # หน้าล็อกอินมีลิงก์ "สำหรับผู้ดูแลระบบ"

    def __init__(self):
        super().__init__()
        setup_fonts(self)
        self.title("Meme Beans")
        self.resizable(True, True)          # ขยายหน้าต่าง/กดปุ่มขยายเต็มจอได้
        self.configure(bg=PANEL)
        self.current_member = None
        self.current_admin = None
        self.is_fullscreen = False
        self.bind("<F11>", lambda e: self.toggle_fullscreen(True))
        self.bind("<Escape>", lambda e: self.toggle_fullscreen(False) if self.is_fullscreen else None)
        self._set_icon()
        self._build_auth_layout()

    def _set_icon(self):
        """ไอคอนหน้าต่าง/แถบงาน = โลโก้ร้าน (images/logo_64.png)  ไม่มีไฟล์ก็ข้ามไป"""
        path = os.path.join(IMAGE_DIR, "logo_64.png")
        if not os.path.exists(path):
            return
        try:
            self._icon = tk.PhotoImage(file=path)
            self.iconphoto(True, self._icon)
        except tk.TclError:
            pass

    def toggle_fullscreen(self, on=None):
        """เปิด/ปิดโหมดเต็มจอ: โปรแกรมเปิดมาเต็มจอ  กด Esc = ย่อเป็นหน้าต่าง  กด F11 = กลับมาเต็มจอ
        (ไม่มีปุ่มหรือข้อความบอกบนหน้าจอ)  ย่อแล้วหน้าต่างกลับเป็นขนาดของหน้าที่เปิดอยู่ตรงกลางจอ"""
        self.is_fullscreen = (not self.is_fullscreen) if on is None else on
        self.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen and getattr(self, "page_size", None):
            self._center(*self.page_size)

    def _center(self, w, h):
        """ตั้งขนาดหน้าต่างตามหน้าที่เปิด (ถ้าขยายเต็มจออยู่ จะคงเต็มจอไว้ แล้วใช้ขนาดนี้ตอนย่อ)"""
        self.page_size = (w, h)
        self.minsize(min(w, MIN_WINDOW[0]), min(h, MIN_WINDOW[1]))   # ย่อ/จัดวางเองได้ถึงครึ่งจอ
        if getattr(self, "keep_place", False):      # หน้าลูกค้าที่ผู้ใช้จัดวางเองแล้ว: เปลี่ยนหน้าไม่ย้ายหน้าต่าง
            return
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if self.is_fullscreen or self.state() == "zoomed":
            return
        x = (sw - w) // 2
        y = max((sh - h) // 2 - 20, 0)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _clear_all(self):
        for w in self.winfo_children():
            w.destroy()

    def _build_auth_layout(self):
        """หน้าล็อกอิน/สมัครสมาชิก (แผงซ้ายโลโก้ + แผงขวาฟอร์ม)"""
        self._clear_all()
        self._center(960, 680)
        self.right = tk.Frame(self, bg=BG, width=520)
        self.right.pack(side="right", fill="y")
        self.right.pack_propagate(False)
        self._build_left_panel()
        self.show_login()

    # ---- แผงซ้าย: คอลลาจมีม + ป้ายชื่อร้าน ----
    def _build_left_panel(self):
        """คอลลาจขยายตามหน้าต่าง (วาดใหม่เมื่อขนาดเปลี่ยน)"""
        canvas = tk.Canvas(self, width=440, height=680, bg=PANEL, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        state = {"job": None, "size": None}

        def redraw():
            state["job"] = None
            size = (canvas.winfo_width(), canvas.winfo_height())
            if size != state["size"] and size[0] > 50:
                state["size"] = size
                canvas.delete("all")
                draw_meme_collage(canvas, *size)

        def on_resize(e):
            if state["job"]:
                canvas.after_cancel(state["job"])
            if state["size"] is None:         # ครั้งแรกวาดทันที ครั้งต่อไปรอให้หยุดลากก่อน
                redraw()
            else:
                state["job"] = canvas.after(80, redraw)

        canvas.bind("<Configure>", on_resize)

    def _clear_right(self):
        """ล้างฝั่งขวา แล้ววางการ์ดฟอร์มสีขาวมุมมนไว้ตรงกลาง (คืนกรอบด้านในการ์ด)"""
        for w in self.right.winfo_children():
            w.destroy()
        card = RoundFrame(self.right, fill=SURFACE, border=LINE, radius=24, padx=32, pady=28)
        card.place(relx=0.5, rely=0.5, anchor="center", width=410)
        return card.inner

    # ---------------- หน้า Login ----------------
    def show_login(self):
        box = self._clear_right()

        tk.Label(box, text="NO COFFEE, NO TALK.", bg=SURFACE, fg=ACCENT,
                 font=(FONT_MEME, 13)).pack(anchor="w")
        tk.Label(box, text="ยินดีต้อนรับ", bg=SURFACE, fg=TEXT,
                 font=(FONT, 24, "bold")).pack(anchor="w")
        tk.Label(box, text="เข้าสู่ระบบสมาชิกเพื่อสั่งเครื่องดื่ม", bg=SURFACE,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w", pady=(0, 8))

        self.login_phone = make_field(box, "เบอร์โทรศัพท์")
        self.login_pass = make_field(box, "รหัสผ่าน", show="•")

        self.show_pw = tk.BooleanVar(value=False)
        pw_row = tk.Frame(box, bg=SURFACE)
        pw_row.pack(fill="x", pady=(6, 0))
        tk.Checkbutton(pw_row, text="แสดงรหัสผ่าน", variable=self.show_pw,
                       command=lambda: self.login_pass.config(
                           show="" if self.show_pw.get() else "•"),
                       bg=SURFACE, activebackground=SURFACE, fg=TEXT_MUTED,
                       selectcolor=SURFACE_2, font=(FONT, 11), bd=0,
                       highlightthickness=0, cursor="hand2"
                       ).pack(side="left")
        LinkButton(pw_row, "ลืมรหัสผ่าน?", self.open_forgot, fg=ACCENT, hover=TEXT,
                   size=11).pack(side="right")

        self.login_msg = tk.Label(box, text="", bg=SURFACE, fg=ERROR,
                                  font=(FONT, 11), wraplength=340, justify="left")
        self.login_msg.pack(anchor="w", pady=(6, 0))

        make_button(box, "เข้าสู่ระบบ", self.do_login, height=48).pack(fill="x", pady=(8, 8))
        make_button(box, "สมัครสมาชิกใหม่", self.show_register,
                    primary=False).pack(fill="x")
        links = tk.Frame(box, bg=SURFACE)
        links.pack(fill="x", pady=(14, 0))
        LinkButton(links, "ผู้จัดทำ", lambda: CreditsDialog(self)).pack(side="left")
        if self.admin_link:                       # หน้าต่างลูกค้าที่เปิดจากหน้าแอดมินไม่มีลิงก์นี้
            LinkButton(links, "สำหรับผู้ดูแลระบบ  ›", self.show_admin).pack(side="right")

        self.login_phone.focus()
        self.bind("<Return>", lambda e: self.do_login())

    def open_forgot(self):
        """เปิดหน้าลืมรหัสผ่าน (ใส่เบอร์ที่พิมพ์ไว้ให้เลย) ตั้งรหัสใหม่เสร็จแล้วกลับมาที่ช่องรหัสผ่าน"""
        def done(phone):
            self.login_phone.delete(0, "end")
            self.login_phone.insert(0, phone)
            self.login_pass.delete(0, "end")
            self.login_msg.config(text="")
            self.login_pass.focus_set()
        ForgotPasswordDialog(self, self.login_phone.get().strip(), done)

    def do_login(self):
        phone = self.login_phone.get().strip()
        password = self.login_pass.get()
        if not phone or not password:
            self.login_msg.config(text="กรุณากรอกเบอร์โทรและรหัสผ่าน")
            return
        member = login_member(phone, password)
        if member is None:
            self.login_msg.config(text="เบอร์โทรหรือรหัสผ่านไม่ถูกต้อง")
            return
        if member.get("banned"):                  # แอดมินแบนบัญชีนี้ไว้
            reason = f"\nเหตุผล: {member['ban_reason']}" if member.get("ban_reason") else ""
            self.login_msg.config(text=f"บัญชีนี้ถูกระงับการใช้งาน กรุณาติดต่อพนักงานที่ร้าน{reason}")
            return
        self.current_member = member
        self.show_menu()

    # ---------------- หน้าสมัครสมาชิก ----------------
    def show_register(self):
        box = self._clear_right()

        tk.Label(box, text="JOIN THE MEME CLUB", bg=SURFACE, fg=ACCENT,
                 font=(FONT_MEME, 13)).pack(anchor="w")
        tk.Label(box, text="สมัครสมาชิก", bg=SURFACE, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(anchor="w")
        tk.Label(box, text="สะสมแต้มทุกแก้ว ยิ้มได้ทุกวัน", bg=SURFACE,
                 fg=TEXT_MUTED, font=(FONT, 11)).pack(anchor="w")

        self.reg_name = make_field(box, "ชื่อ-นามสกุล", compact=True)
        self.reg_phone = make_field(box, "เบอร์โทรศัพท์", compact=True)
        self.reg_email = make_field(box, "อีเมล", compact=True)
        self.reg_pass = make_password_field(box, "รหัสผ่าน", compact=True)
        self.reg_pass2 = make_field(box, "ยืนยันรหัสผ่าน", show="•", compact=True)

        self.reg_msg = tk.Label(box, text="", bg=SURFACE, fg=ERROR,
                                font=(FONT, 11), wraplength=340, justify="left")
        self.reg_msg.pack(anchor="w", pady=(6, 0))

        make_button(box, "สมัครสมาชิก", self.do_register, height=46).pack(fill="x", pady=(6, 8))
        make_button(box, "กลับไปหน้าเข้าสู่ระบบ", self.show_login,
                    primary=False).pack(fill="x")

        self.reg_name.focus()
        self.bind("<Return>", lambda e: self.do_register())

    def do_register(self):
        name = self.reg_name.get().strip()
        phone = self.reg_phone.get().strip()
        email = self.reg_email.get().strip()
        pw = self.reg_pass.get()
        pw2 = self.reg_pass2.get()
        problem = password_problem(pw)      # กติกา: 8 ตัวขึ้นไป มี A-Z a-z 0-9 ห้ามอักขระพิเศษ (database.py)

        if not name or not phone or not email or not pw:
            self.reg_msg.config(text="กรุณากรอกข้อมูลให้ครบ")
        elif not phone.isdigit() or not (9 <= len(phone) <= 10):
            self.reg_msg.config(text="เบอร์โทรต้องเป็นตัวเลข 9-10 หลัก")
        elif not is_valid_email(email):
            self.reg_msg.config(text="รูปแบบอีเมลไม่ถูกต้อง เช่น name@example.com")
        elif problem:
            self.reg_msg.config(text=problem)
        elif pw != pw2:
            self.reg_msg.config(text="รหัสผ่านทั้งสองช่องไม่ตรงกัน")
        else:
            ok, msg = register_member(name, phone, pw, email)
            if ok:
                messagebox.showinfo("สำเร็จ", "สมัครสมาชิกเรียบร้อย\nกรุณาเข้าสู่ระบบ", parent=self)
                self.show_login()
                self.login_phone.insert(0, phone)
                self.login_pass.focus()
            else:
                self.reg_msg.config(text=msg)

    # ---------------- หน้าเมนู ----------------
    def show_menu(self):
        self._clear_all()
        self.unbind("<Return>")
        self._center(1100, 700)
        MenuPage(self, self.current_member, self.logout).pack(fill="both", expand=True)

    def logout(self):
        self.current_member = None
        self._build_auth_layout()

    # ---------------- ระบบแอดมิน ----------------
    def show_admin(self):
        """หน้าล็อกอินแอดมิน (หน้าต่างแยกสไตล์จากฝั่งลูกค้า)"""
        from admin import AdminLoginPage      # หน้าจอแอดมินอยู่ในไฟล์ admin.py (โหลดตอนกดเข้าหน้าแอดมิน)
        self._clear_all()
        self.unbind("<Return>")
        self._center(1000, 660)
        AdminLoginPage(self, self.show_admin_home, self._build_auth_layout).pack(fill="both", expand=True)

    def show_admin_home(self, admin):
        from admin import AdminPage           # หน้าจอแอดมินอยู่ในไฟล์ admin.py
        self.current_admin = admin
        self._clear_all()
        self.unbind("<Return>")
        self._center(1280, 760)
        AdminPage(self, admin, self.admin_logout).pack(fill="both", expand=True)

    def admin_logout(self):
        self.current_admin = None
        self._build_auth_layout()


class CustomerWindow(tk.Toplevel):
    """หน้าต่าง "หน้าลูกค้า" ที่แอดมินเปิดจากหน้าแอดมิน (ปุ่ม "Main Menu")
    แอดมินกับลูกค้าใช้พร้อมกันได้ในโปรแกรมเดียว: ลูกค้าสั่ง/ส่งสลิปในหน้าต่างนี้
    แล้วแอดมินตรวจสลิปที่หน้าการชำระเงินได้ทันที (ข้อมูลอยู่ในฐานข้อมูลเดียวกัน)
    ใช้หน้าจอฝั่งลูกค้าชุดเดียวกับหน้าต่างหลัก (ยืมเมธอดจาก CoffeeApp) แต่ไม่มีลิงก์เข้าหน้าแอดมิน"""
    admin_link = False

    def __init__(self, master):
        super().__init__(master)
        self.title(f"{SHOP_NAME} - หน้าลูกค้า")
        self.configure(bg=PANEL)
        self.resizable(True, True)
        self.current_member = None
        self.is_fullscreen = False
        self.keep_place = True                      # เปลี่ยนหน้า (ล็อกอิน/เมนู) แล้วหน้าต่างอยู่ที่เดิม ไม่เด้งกลับกลางจอ
        self.bind("<F11>", lambda e: self.toggle_fullscreen(True))
        self.bind("<Escape>", lambda e: self.toggle_fullscreen(False) if self.is_fullscreen else None)
        self._build_auth_layout()
        maximize_window(self)                       # เปิดมาเต็มจอแบบมีแถบชื่อ (ลาก/จัดวางคู่กับหน้าแอดมินเองได้)
        self.lift()
        self.focus_force()

    # หน้าล็อกอิน / สมัครสมาชิก / หน้าเมนู: โค้ดชุดเดียวกับหน้าต่างหลัก
    toggle_fullscreen = CoffeeApp.toggle_fullscreen
    _center = CoffeeApp._center
    _clear_all = CoffeeApp._clear_all
    _build_auth_layout = CoffeeApp._build_auth_layout
    _build_left_panel = CoffeeApp._build_left_panel
    _clear_right = CoffeeApp._clear_right
    show_login = CoffeeApp.show_login
    open_forgot = CoffeeApp.open_forgot
    do_login = CoffeeApp.do_login
    show_register = CoffeeApp.show_register
    do_register = CoffeeApp.do_register
    show_menu = CoffeeApp.show_menu
    logout = CoffeeApp.logout



# =====================================================================
# ส่วนที่ 23: หน้าผู้จัดทำ
#   ประกอบด้วย: CREATOR (ชื่อ + ช่องทางติดต่อผู้จัดทำ), CREDIT_STICKERS (สติกเกอร์ตกแต่งรอบหน้า),
#              CreditsDialog (หน้าผู้จัดทำ กดช่องทางติดต่อเพื่อคัดลอก)
#   แก้ที่นี่เมื่อ: เปลี่ยนชื่อ/ช่องทางติดต่อ (แก้ CREATOR) หรือหน้าตาหน้าผู้จัดทำ
#   รูปที่ใช้ (โฟลเดอร์ images): creator_photo.png, icon_fb/ig/mail/tel.png, credit_*.png
#   (รูปและสติกเกอร์ตัดมาจากไฟล์ออกแบบหน้าผู้จัดทำ contact.pdf หน้า 1 ทำขนาดพอดีไว้แล้ว ไม่ต้องมี Pillow)
#   หมายเหตุ: ส่วนนี้อยู่ก่อนส่วนที่ 22 ในไฟล์ เพราะส่วนที่ 22 (จุดเริ่มโปรแกรม) ต้องอยู่ท้ายไฟล์เสมอ
# บรรทัด 6228 - 6442
# =====================================================================
CREATOR = {
    "name": "นายพัทธดนย์ ชมภูพงศ์",
    "role": "ผู้จัดทำและพัฒนาโปรแกรม Meme Beans Coffee",
    "contacts": [                               # (รูปไอคอน, ชื่อช่องทาง, ข้อมูลที่แสดง/คัดลอก)
        ("icon_fb", "Facebook", "Phattadon Chomphupong"),
        ("icon_ig", "Instagram", "phatc0n_d"),
        ("icon_mail", "Gmail", "phattadon.c@kkumail.com"),
        ("icon_tel", "โทรศัพท์", "090-242-6531"),
    ],
}

# สติกเกอร์รอบหน้า (วางตามสัดส่วนของหน้าต่าง เหมือนในไฟล์ออกแบบ)
# (ชื่อรูป, ตำแหน่ง x เป็นสัดส่วนความกว้าง, ตำแหน่ง y เป็นสัดส่วนความสูง, เลื่อน x, เลื่อน y (พิกเซล), จุดยึดของรูป)
CREDIT_STICKERS = [
    ("credit_splash_tl", 0, 0, 0, 0, "nw"),
    ("credit_splash_l", 0, .42, 0, 0, "w"),
    ("credit_sparkle", 0, .40, 34, 0, "w"),
    ("credit_bean2", 0, .60, 52, 0, "w"),
    ("credit_crown", .5, 0, 0, 26, "n"),
    ("credit_polaroid", 1, 0, -34, 86, "ne"),
    ("credit_bean", 1, .27, -86, 0, "e"),
    ("credit_splash_r", 1, .65, 0, 0, "e"),
    ("credit_doge", 0, 1, 0, 0, "sw"),
    ("credit_cat", 1, 1, 0, 0, "se"),
]


class CreditsDialog(tk.Toplevel):
    """หน้าผู้จัดทำ: รูป + ชื่อ + ช่องทางติดต่อ (กดเพื่อคัดลอก)
    ตกแต่งด้วยสติกเกอร์มีมแบบไฟล์ออกแบบ พื้นดำ ปุ่มเหลือง เหมือนหน้าอื่นของร้าน"""
    PHOTO_W, PHOTO_H = 300, 400

    def __init__(self, parent):
        super().__init__(parent)
        self.title("ผู้จัดทำ")
        self.configure(bg=PANEL)
        self.resizable(False, False)
        self.transient(parent)
        self._copy_jobs = {}

        self.canvas = tk.Canvas(self, bg=PANEL, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.body = tk.Frame(self.canvas, bg=PANEL)
        self.body_win = self.canvas.create_window(0, 0, window=self.body, anchor="n")
        close = PillButton(self.canvas, "ปิด", self.destroy, "dark_ghost", height=38, size=10, padx=22)
        self.close_win = self.canvas.create_window(0, 0, window=close, anchor="ne")   # มุมขวาบน
        self._build_body()
        self.canvas.bind("<Configure>", lambda e: self._layout())
        self.bind("<Escape>", lambda e: self.destroy())

        w = min(1080, self.winfo_screenwidth() - 40)      # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        h = min(760, self.winfo_screenheight() - 80)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)
        grab_modal(self)

    # ---------- เนื้อหากลางหน้า ----------
    def _build_body(self):
        b = self.body
        tk.Label(b, text="MEET THE MAKER", bg=PANEL, fg=ACCENT, font=(FONT_MEME, 14)).pack()
        tk.Label(b, text="ผู้จัดทำ", bg=PANEL, fg=TEXT, font=(FONT, 26, "bold")).pack()

        card = RoundFrame(b, fill=SURFACE, border=LINE, radius=24, padx=24, pady=24)
        card.pack(pady=(14, 0))
        inner = card.inner
        photo = load_art("creator_photo")
        pic = tk.Canvas(inner, width=self.PHOTO_W, height=self.PHOTO_H, bg=SURFACE,
                        highlightthickness=0, bd=0)
        pic.pack(side="left", anchor="n")
        if photo is not None:
            pic.create_image(self.PHOTO_W / 2, self.PHOTO_H / 2, image=photo)
            pic.photo = photo
        else:                                       # ไม่มีไฟล์รูป: ตัวอักษรแรกของชื่อ
            rounded_rect(pic, 0, 0, self.PHOTO_W, self.PHOTO_H, 18, fill=TAN)
            pic.create_text(self.PHOTO_W / 2, self.PHOTO_H / 2, text=member_initial(CREATOR["name"]),
                            font=(FONT, 90, "bold"), fill=BLACK)

        info = tk.Frame(inner, bg=SURFACE, width=460)
        info.pack(side="left", fill="y", padx=(28, 0))
        Pill(info, "ผู้จัดทำโปรแกรม", ACCENT, ACCENT_INK, size=10, height=26, padx=12).pack(anchor="w")
        tk.Label(info, text=CREATOR["name"], bg=SURFACE, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(anchor="w", pady=(10, 0))
        tk.Label(info, text=CREATOR["role"], bg=SURFACE, fg=LATTE,
                 font=(FONT, 11)).pack(anchor="w")
        tk.Frame(info, bg=LINE, height=1).pack(fill="x", pady=(16, 12))
        head = tk.Frame(info, bg=SURFACE)
        head.pack(fill="x")
        tk.Label(head, text="ช่องทางการติดต่อ", bg=SURFACE, fg=TEXT,
                 font=(FONT, 12, "bold")).pack(side="left")
        tk.Label(head, text="กดเพื่อคัดลอก", bg=SURFACE, fg=TEXT_MUTED,
                 font=(FONT, 9)).pack(side="right")
        self.contact_rows = []
        for icon, label, value in CREATOR["contacts"]:
            self._contact_row(info, icon, label, value)


        # การ์ดซ้อนการ์ด: ปรับขนาดการ์ดในก่อน แล้วค่อยการ์ดนอก (ไม่งั้นการ์ดนอกค้างขนาดตอนกำลังสร้าง)
        for rf in self.contact_rows + [card]:
            self.update_idletasks()
            rf._fit()

    def _contact_row(self, parent, icon, label, value):
        """แถวช่องทางติดต่อ 1 แถว: ไอคอน + ชื่อช่องทาง + ข้อมูล  กดแล้วคัดลอกข้อมูลไปวางที่อื่นได้"""
        row = RoundFrame(parent, fill=SURFACE_2, radius=14, padx=12, pady=8)
        row.pack(fill="x", pady=(8, 0))
        box = row.inner
        img = load_art(icon)
        ic = tk.Label(box, bg=SURFACE_2, image=img, width=40, height=40) if img is not None else \
            tk.Label(box, bg=SURFACE_2, text="•", fg=ACCENT, font=(FONT, 16, "bold"), width=2)
        ic.image = img
        ic.pack(side="left")
        text = tk.Frame(box, bg=SURFACE_2)
        text.pack(side="left", padx=(12, 0))
        tk.Label(text, text=label, bg=SURFACE_2, fg=TEXT_MUTED, font=(FONT, 9)).pack(anchor="w")
        tk.Label(text, text=value, bg=SURFACE_2, fg=TEXT, font=(FONT, 12, "bold")).pack(anchor="w")
        hint = tk.Label(box, text="คัดลอก", bg=SURFACE_2, fg=SURFACE_2, font=(FONT, 9, "bold"),
                        width=10, anchor="e")           # กว้างคงที่ ข้อความเปลี่ยนแล้วแถวไม่ขยับ
        hint.pack(side="right", padx=(8, 4))
        row.hint, row.value = hint, value
        widgets = [row, box, ic, text, hint] + text.winfo_children()
        for w in widgets:
            w.bind("<Enter>", lambda e, r=row: self._hover(r, True))
            w.bind("<Leave>", lambda e, r=row: self._hover(r, False))
            w.bind("<Button-1>", lambda e, r=row: self.copy(r))
            w.config(cursor="hand2")
        self.contact_rows.append(row)

    def _paint_row(self, row, fill):
        row.set_fill(fill)
        stack = list(row.inner.winfo_children())
        while stack:
            w = stack.pop()
            w.config(bg=fill)
            stack.extend(w.winfo_children())
        if not row.hint.cget("text").startswith("คัดลอกแล้ว"):
            row.hint.config(fg=ACCENT if fill == SURFACE_3 else fill)

    @staticmethod
    def _pointer_in(row):
        """เมาส์ยังชี้อยู่ในแถวนี้ไหม (รวมตัวหนังสือ/ไอคอนในแถว)"""
        try:
            w = row.winfo_containing(*row.winfo_pointerxy())
        except (KeyError, tk.TclError):
            return False
        while w is not None and w is not row:
            w = w.master
        return w is row

    def _hover(self, row, on):
        if not on and self._pointer_in(row):        # เลื่อนเมาส์ไปบนตัวหนังสือในแถวเดียวกัน = ยังชี้แถวนี้อยู่
            return
        self._paint_row(row, SURFACE_3 if on else SURFACE_2)

    def copy(self, row):
        """คัดลอกข้อมูลช่องทางติดต่อ แล้วขึ้นคำว่า "คัดลอกแล้ว" สักครู่"""
        self.clipboard_clear()
        self.clipboard_append(row.value)
        row.hint.config(text="คัดลอกแล้ว", fg=SUCCESS)
        job = self._copy_jobs.pop(row, None)
        if job:
            self.after_cancel(job)
        self._copy_jobs[row] = self.after(1600, lambda: self._reset_hint(row))

    def _reset_hint(self, row):
        self._copy_jobs.pop(row, None)
        if row.winfo_exists():
            row.hint.config(text="คัดลอก")
            self._paint_row(row, SURFACE_3 if self._pointer_in(row) else SURFACE_2)

    def destroy(self):
        for job in self._copy_jobs.values():
            self.after_cancel(job)
        self._copy_jobs.clear()
        super().destroy()

    # ---------- จัดวางตามขนาดหน้าต่าง ----------
    def _layout(self):
        c = self.canvas
        w, h = c.winfo_width(), c.winfo_height()
        bw, bh = self.body.winfo_reqwidth(), self.body.winfo_reqheight()
        top = max(24, (h - bh) // 2)                # เนื้อหาอยู่กลางหน้า (จอเตี้ยชิดบนแทน)
        c.coords(self.body_win, w / 2, top)
        c.coords(self.close_win, w - 28, 30)
        body = (w / 2 - bw / 2 - 12, top - 12, w / 2 + bw / 2 + 12, top + bh + 12)
        c.delete("deco")
        before = set(c.find_all())
        for name, fx, fy, dx, dy, anchor in CREDIT_STICKERS:
            img = load_art(name)
            if img is None:
                continue
            item = c.create_image(w * fx + dx, h * fy + dy, image=img, anchor=anchor)
            x0, y0, x1, y1 = c.bbox(item)
            if x0 < body[2] and x1 > body[0] and y0 < body[3] and y1 > body[1]:
                c.delete(item)                      # หน้าต่างเล็กจนสติกเกอร์ทับเนื้อหา: ไม่วางชิ้นนั้น
        draw_logo(c, 36 + 32, 30 + 32, 64)          # โลโก้ร้านมุมซ้ายบน (วาดทับสีเหลืองที่มุม)
        c.create_text(36 + 64 + 12, 30 + 21, text="Meme Beans", anchor="w", fill=TEXT,
                      font=(FONT_SCRIPT, 15, "bold"))
        c.create_text(36 + 64 + 12, 30 + 44, text="Coffee + Meme", anchor="w", fill=TEXT_MUTED,
                      font=(FONT, 10))
        for item in set(c.find_all()) - before:     # ติดป้าย "deco" ให้ลบแล้ววาดใหม่ได้ตอนย่อขยาย
            if item not in (self.body_win, self.close_win):
                c.addtag_withtag("deco", item)
        c.tag_lower("deco")


# =====================================================================
# ส่วนที่ 24: ติดตามสถานะออเดอร์ (ฝั่งลูกค้า)
#   ประกอบด้วย: สีและข้อความสถานะหลังร้าน (PREP_COLORS, prep_detail, prep_toast_text), draw_prep_icon,
#              draw_mini_steps, draw_prep_steps, top_window, OrderToast (แจ้งเตือนเด้งมุมขวาบน),
#              OrderStatusDialog (หน้าติดตามออเดอร์: สถานะ คิวก่อนหน้า แก้วที่เสร็จแล้ว อัปเดตอัตโนมัติ)
#   แก้ที่นี่เมื่อ: แก้หน้าตา/ข้อความสถานะออเดอร์ที่ลูกค้าเห็น (แอดมินเปลี่ยนสถานะที่หน้า "คิวหลังร้าน")
# บรรทัด 6445 - 6823
# =====================================================================
PREP_COLORS = {"queued": LATTE, "making": ACCENT, "ready": SUCCESS, "picked_up": TEXT_MUTED}
PREP_RING = {"queued": "#3A2F22", "making": "#3A3415", "ready": "#1E3A27", "picked_up": "#2E2E2E"}
PREP_TINT = {"queued": "#2A241C", "making": "#2E2812", "ready": "#16301F", "picked_up": SURFACE}
TRACK_STEPS = [("paid", "ชำระเงินแล้ว"), ("queued", "รอคิว"), ("making", "กำลังทำ"),
               ("ready", "พร้อมรับ"), ("picked_up", "รับแล้ว")]


def prep_queue_text(o):
    """ข้อความคิวก่อนหน้า เช่น "อีก 4 แก้ว (2 ออเดอร์) จะถึงคิวของคุณ" """
    n, cups = o["ahead_orders"], o["ahead_cups"]
    if not n:
        return "ออเดอร์ของคุณเป็นคิวถัดไป"
    if not cups:                           # ออเดอร์ก่อนหน้าทำครบทุกแก้วแล้ว รอแค่ส่งมอบ
        return f"อีก {n} ออเดอร์จะถึงคิวของคุณ"
    return f"อีก {cups} แก้ว ({n} ออเดอร์) จะถึงคิวของคุณ"


def prep_detail(o):
    """ข้อความสั้นบอกความคืบหน้า (แถบบนหน้าเมนู)"""
    st = o["prep_status"]
    if st == "queued":
        return f"{prep_queue_text(o)}  •  ประมาณ {o['wait_minutes']} นาที"
    if st == "making":
        more = f"  •  อีกประมาณ {o['wait_minutes']} นาที" if o["wait_minutes"] else "  •  ใกล้เสร็จแล้ว"
        return f"เสร็จแล้ว {o['cups_done']}/{o['cups']} แก้ว{more}"
    if st == "ready":
        return "มารับเครื่องดื่มที่เคาน์เตอร์ได้เลย"
    return f"ขอบคุณที่อุดหนุน {SHOP_NAME}"


def prep_toast_text(o):
    """(หัวข้อ, รายละเอียด) ของแจ้งเตือนเด้งเมื่อหลังร้านเปลี่ยนสถานะ"""
    code, st = order_code(o["order_id"]), o["prep_status"]
    if st == "queued":
        return f"ออเดอร์ {code} กลับไปรอคิว", prep_queue_text(o)
    if st == "making":
        return f"กำลังทำออเดอร์ {code} ของคุณ", prep_detail(o)
    if st == "ready":
        again = f"  (ร้านเรียกครั้งที่ {o['prep_calls'] + 1})" if o.get("prep_calls") else ""
        return f"ออเดอร์ {code} พร้อมรับแล้ว!", "มารับเครื่องดื่มที่เคาน์เตอร์ได้เลย" + again
    return f"รับออเดอร์ {code} เรียบร้อย", f"ขอบคุณที่อุดหนุน {SHOP_NAME} แล้วมาใหม่นะ"


def draw_prep_icon(c, cx, cy, d, status):
    """ไอคอนสถานะในวงกลมเส้นผ่านศูนย์กลาง d (จุดกลาง cx, cy เป็นเลขจำนวนเต็ม)
    รอคิว = นาฬิกาทราย / กำลังทำ = แก้วมีไอร้อน / พร้อมรับ และ รับแล้ว = ติ๊กถูก"""
    r, s = d / 2, d / 84
    X = lambda v: cx + (v - 42) * s
    Y = lambda v: cy + (v - 42) * s
    aa_oval(c, cx - r, cy - r, cx + r, cy + r, fill=PREP_RING[status], outline="")
    r2 = r * 31 / 42
    aa_oval(c, cx - r2, cy - r2, cx + r2, cy + r2, fill=PREP_COLORS[status], outline="")
    ink, lw = ACCENT_INK, lambda v: max(1, round(v * s))
    if status in ("ready", "picked_up"):
        crisp(c, cx - r, cy - r, cx + r, cy + r,
              lambda g: g.create_line(X(28), Y(43), X(38), Y(53), X(57), Y(32), fill=ink, width=max(2, 6 * s),
                                      capstyle="round", joinstyle="round"), ("prep_tick", d))
    elif status == "queued":
        c.create_line(X(32), Y(27), X(52), Y(27), fill=ink, width=lw(4), capstyle="round")
        c.create_line(X(32), Y(57), X(52), Y(57), fill=ink, width=lw(4), capstyle="round")
        c.create_polygon(X(34), Y(29), X(50), Y(29), X(42), Y(42), fill=ink, outline="")
        c.create_polygon(X(42), Y(42), X(34), Y(55), X(50), Y(55), fill="", outline=ink, width=lw(2))
        c.create_polygon(X(42), Y(47), X(37), Y(55), X(47), Y(55), fill=ink, outline="")
    else:
        c.create_polygon(X(29), Y(38), X(53), Y(38), X(50), Y(60), X(32), Y(60), fill=ink, outline="")
        c.create_arc(X(48), Y(41), X(60), Y(53), start=270, extent=180, style="arc", outline=ink, width=lw(3))
        for x in (36, 45):
            c.create_line(X(x), Y(33), X(x - 3), Y(28), X(x + 1), Y(22), smooth=True, fill=ink,
                          width=lw(3), capstyle="round")


def draw_mini_steps(c, status, bg):
    """จุด 4 ขั้นเล็ก ๆ (รอคิว / กำลังทำ / พร้อมรับ / รับแล้ว) ขั้นที่ผ่านแล้วเป็นสีของสถานะ"""
    keys = [k for k, _ in PREP_STEPS]
    cur, col = keys.index(status), PREP_COLORS[status]
    y, gap = int(c.cget("height")) // 2, 34
    for i in range(len(keys) - 1):
        c.create_line(8 + i * gap, y, 8 + (i + 1) * gap, y, fill=col if i < cur else LINE, width=3)
    for i in range(len(keys)):
        x = 8 + i * gap
        r = 6 if i == cur else 4
        aa_oval(c, x - r, y - r, x + r, y + r, fill=col if i <= cur else bg,
                outline=col if i <= cur else LINE, width=2)


def draw_prep_steps(c, o, w):
    """เส้นขั้นตอน 5 ขั้น: ชำระเงินแล้ว -> รอคิว -> กำลังทำ -> พร้อมรับ -> รับแล้ว (ใต้แต่ละขั้นบอกเวลา)"""
    c.delete("all")
    keys = [k for k, _ in TRACK_STEPS]
    cur = keys.index(o["prep_status"])
    pad, y = 56, 24
    gap = (w - 2 * pad) / (len(keys) - 1)
    hhmm = lambda t: t[11:16] if t else ""
    times = {"paid": o["paid_at"], "ready": o.get("ready_at"), "picked_up": o.get("picked_up_at")}
    times.setdefault(o["prep_status"], o.get("prep_at"))
    if not times.get(o["prep_status"]):
        times[o["prep_status"]] = o.get("prep_at")
    for i in range(len(keys) - 1):
        c.create_line(pad + i * gap, y, pad + (i + 1) * gap, y, fill=ACCENT if i < cur else LINE, width=4)
    for i, (key, label) in enumerate(TRACK_STEPS):
        x = pad + i * gap
        if i == cur:
            aa_oval(c, x - 17, y - 17, x + 17, y + 17, fill="#3A3415", outline="")
        if i <= cur:
            aa_oval(c, x - 11, y - 11, x + 11, y + 11, fill=ACCENT, outline="")
            c.create_line(x - 5, y, x - 1.5, y + 4, x + 5.5, y - 4, fill=ACCENT_INK, width=2.5,
                          capstyle="round", joinstyle="round")
        else:
            aa_oval(c, x - 11, y - 11, x + 11, y + 11, fill=SURFACE_2, outline=LINE, width=2)
        c.create_text(x, y + 32, text=label, fill=TEXT if i <= cur else TEXT_MUTED,
                      font=(FONT, 10, "bold" if i == cur else "normal"))
        t = hhmm(times.get(key)) if i <= cur else ""
        if t:
            c.create_text(x, y + 52, text=f"{t} น.", fill=TEXT_MUTED, font=(FONT, 9))


def top_window(app):
    """หน้าต่างบนสุดของแอปที่ลูกค้าเห็นอยู่ (หน้าต่างย่อยที่เปิดซ้อนล่าสุด) ใช้วางแจ้งเตือน
    ไม่นับหน้าต่าง "หน้าลูกค้า" ที่เปิดจากหน้าแอดมิน (เป็นอีกหน้าจอหนึ่ง)"""
    win = app
    while True:
        kids = [w for w in win.winfo_children() if isinstance(w, tk.Toplevel)
                and not isinstance(w, CustomerWindow) and w.winfo_viewable()]
        if not kids:
            return win
        win = kids[-1]


class OrderToast(RoundFrame):
    """แจ้งเตือนเด้งมุมขวาบนของหน้าต่าง เมื่อหลังร้านเปลี่ยนสถานะออเดอร์
    พร้อมรับ = การ์ดสีเขียว มีเสียงเตือน และค้างไว้จนกว่าจะกดปิด / สถานะอื่นหายเองใน 8 วินาที
    มีหลายอันจะเรียงต่อกันลงมา"""

    WIDTH = 410

    def __init__(self, win, o, on_open):
        st = o["prep_status"]
        ready = st == "ready"
        fill = "#173322" if ready else SURFACE_2
        super().__init__(win, fill=fill, border=PREP_COLORS[st], radius=18, padx=16, pady=14,
                         border_width=2)
        self.win = win
        self.order_id = o["order_id"]
        self.status = st
        self._job = None
        row = tk.Frame(self.inner, bg=fill)
        row.pack(fill="x")
        icon = tk.Canvas(row, width=50, height=50, bg=fill, highlightthickness=0)
        icon.pack(side="left", anchor="n")
        draw_prep_icon(icon, 25, 25, 50, st)
        LinkButton(row, "×", self.close, fg=TEXT_MUTED, hover=TEXT, size=14, bold=True).pack(side="right",
                                                                                                anchor="n")
        texts = tk.Frame(row, bg=fill)
        texts.pack(side="left", fill="x", expand=True, padx=(12, 6))
        title, detail = prep_toast_text(o)
        tk.Label(texts, text=title, bg=fill, fg=TEXT, font=(FONT, 13 if ready else 12, "bold"), anchor="w",
                 justify="left", wraplength=290).pack(fill="x")
        tk.Label(texts, text=detail, bg=fill, fg=TEXT if ready else TEXT_MUTED, font=(FONT, 10), anchor="w",
                 justify="left", wraplength=290).pack(fill="x", pady=(2, 0))
        PillButton(texts, "ดูสถานะออเดอร์", lambda: self._open(on_open), "primary" if ready else "secondary",
                   height=32, size=10, padx=14).pack(anchor="w", pady=(8, 0))
        win._toasts = [t for t in getattr(win, "_toasts", []) if t.winfo_exists()] + [self]
        layout_toasts(win)
        if ready:
            win.bell()
            self._job = self.after(700, win.bell)
        else:
            self._job = self.after(8000, self.close)

    def _open(self, on_open):
        oid = self.order_id
        self.close()
        on_open(oid)

    def destroy(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        super().destroy()

    def close(self):
        if not self.winfo_exists():
            return
        win = self.win
        self.destroy()
        if win.winfo_exists():
            layout_toasts(win)


def layout_toasts(win):
    """เรียงแจ้งเตือนจากมุมขวาบนลงมา (อันใหม่อยู่ล่าง)"""
    win._toasts = [t for t in getattr(win, "_toasts", []) if t.winfo_exists()]
    y = 18
    for t in win._toasts:
        t.place(relx=1.0, x=-22, y=y, anchor="ne", width=OrderToast.WIDTH)
        tk.Misc.tkraise(t)                          # ขึ้นบนสุด (Canvas ใช้ชื่อ lift กับรูปวาดข้างใน)
        t.update_idletasks()
        y += t.winfo_reqheight() + 10


class OrderStatusDialog(tk.Toplevel):
    """หน้าติดตามออเดอร์: สถานะตอนนี้ (รอคิว อีกกี่แก้วถึงคิว / กำลังทำ เสร็จแล้วกี่แก้ว / พร้อมรับ / รับแล้ว)
    เส้นขั้นตอนพร้อมเวลา และรายการเครื่องดื่มที่ทำเสร็จแล้ว  เช็กจากฐานข้อมูลทุก 2.5 วินาที (แอดมินกดแล้วเห็นทันที)"""

    PAGE_W = 760
    POLL_MS = 2500

    def __init__(self, parent, order_id):
        super().__init__(parent)
        self.order_id = order_id
        self.code = order_code(order_id)
        self._sig = self._job = None
        self.title(f"ติดตามออเดอร์ {self.code}")
        self.configure(bg=BG)
        self.transient(parent)
        w, h = 760, 720                           # ขนาดตอนย่อหน้าต่าง (ปกติเปิดเต็มจอ)
        x = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{max(x, 0)}+{max(y, 0)}")
        fill_screen(self)

        bar = tk.Frame(self, bg=PANEL, height=110)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        bar_full, bar = bar, tk.Frame(bar, bg=PANEL)
        bar.pack(fill="both", expand=True)
        keep_centered(bar_full, bar, self.PAGE_W)
        logo_canvas(bar, 52).pack(side="left", padx=(28, 0))
        info = tk.Frame(bar, bg=PANEL)
        info.pack(side="left", padx=16)
        tk.Label(info, text="ติดตามออเดอร์", bg=PANEL, fg=LATTE, font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Label(info, text=self.code, bg=PANEL, fg=TEXT, font=(FONT, 24, "bold")).pack(anchor="w")
        self.sub = tk.Label(info, text="", bg=PANEL, fg=TEXT_MUTED, font=(FONT, 11))
        self.sub.pack(anchor="w")
        PillButton(bar, "ปิด", self.destroy, "dark_ghost", height=38, size=10,
                   padx=22).pack(side="right", padx=28)

        self.area = ScrollFrame(self, BG)
        self.area.pack(fill="both", expand=True)
        self.column = tk.Frame(self.area.inner, bg=BG)
        self.column.pack(fill="x")
        keep_centered(self.area.canvas, self.column, self.PAGE_W)
        self.refresh()
        try:
            grab_modal(self)
        except tk.TclError:
            pass

    def destroy(self):
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        super().destroy()

    def refresh(self):
        """อ่านสถานะล่าสุด วาดใหม่เฉพาะตอนมีอะไรเปลี่ยน (เลื่อนอยู่ตำแหน่งเดิม)"""
        self._job = None
        if not self.winfo_exists():
            return
        o = get_order_prep(self.order_id)
        sig = o and (o["prep_status"], o["prep_seq"], o["cups_done"], o["ahead_orders"], o["ahead_cups"],
                     o["wait_minutes"], o["prep_calls"])
        if sig != self._sig or self._sig is None:
            self._sig = sig
            pos = self.area.canvas.yview()[0]
            for w in self.column.winfo_children():
                w.destroy()
            self._build(o)
            self.update_idletasks()
            self.area.canvas.yview_moveto(pos)
        if o is not None and o["prep_status"] != "picked_up":
            self._job = self.after(self.POLL_MS, self.refresh)

    def _build(self, o):
        col = self.column
        if o is None:
            tk.Label(col, text="ไม่พบสถานะของออเดอร์นี้", bg=BG, fg=TEXT_MUTED,
                     font=(FONT, 13)).pack(pady=60)
            return
        st = o["prep_status"]
        self.sub.config(text=f"ชำระเมื่อ {fmt_datetime(o['paid_at'])}  •  ฿{fmt_price(o['paid'])}")

        # การ์ดสถานะตอนนี้
        hero = RoundFrame(col, fill=PREP_TINT[st] if st != "picked_up" else SURFACE,
                          border=PREP_COLORS[st], radius=20, padx=24, pady=20, border_width=2)
        hero.pack(fill="x", padx=24, pady=(22, 0))
        h = hero.inner
        bg = bg_of(h)
        icon = tk.Canvas(h, width=96, height=96, bg=bg, highlightthickness=0)
        icon.pack(side="left", anchor="n")
        draw_prep_icon(icon, 48, 48, 96, st)
        texts = tk.Frame(h, bg=bg)
        texts.pack(side="left", fill="x", expand=True, padx=(20, 0))
        kicker = {"queued": "รอคิว", "making": "กำลังทำ", "ready": "พร้อมรับ", "picked_up": "รับแล้ว"}[st]
        Pill(texts, kicker, PREP_COLORS[st], ACCENT_INK, size=10, height=26, padx=12).pack(anchor="w")
        title, detail = {
            "queued": (prep_queue_text(o),
                       f"ก่อนหน้าคุณมี {o['ahead_orders']} ออเดอร์  •  คาดว่าจะได้รับในอีกประมาณ "
                       f"{o['wait_minutes']} นาที"),
            "making": ("บาริสต้ากำลังทำเครื่องดื่มของคุณ",
                       f"เสร็จแล้ว {o['cups_done']} จาก {o['cups']} แก้ว"
                       + (f"  •  อีกประมาณ {o['wait_minutes']} นาที" if o["wait_minutes"] else "  •  ใกล้เสร็จแล้ว")),
            "ready": ("เครื่องดื่มของคุณพร้อมแล้ว!",
                      f"มารับที่เคาน์เตอร์ได้เลย แจ้งเลขออเดอร์ {self.code} กับพนักงาน"),
            "picked_up": ("รับเครื่องดื่มเรียบร้อย", f"ขอบคุณที่อุดหนุน {SHOP_NAME} แล้วมาใหม่นะ"),
        }[st]
        tk.Label(texts, text=title, bg=bg, fg=TEXT, font=(FONT, 20, "bold"), anchor="w", justify="left",
                 wraplength=520).pack(fill="x", pady=(8, 0))
        tk.Label(texts, text=detail, bg=bg, fg=TEXT if st == "ready" else TEXT_MUTED, font=(FONT, 12),
                 anchor="w", justify="left", wraplength=520).pack(fill="x", pady=(2, 0))
        if st == "making":                               # แถบความคืบหน้า (แก้วที่เสร็จ / ทั้งหมด)
            frac = o["cups_done"] / o["cups"] if o["cups"] else 0
            bar = tk.Canvas(texts, height=10, bg=bg, highlightthickness=0)
            bar.pack(fill="x", pady=(12, 0))
            bar.bind("<Configure>", lambda e: self._draw_bar(e.widget, frac, PREP_COLORS[st]))

        # ขั้นตอน
        steps = RoundFrame(col, fill=SURFACE, border=LINE, radius=18, padx=10, pady=14)
        steps.pack(fill="x", padx=24, pady=(14, 0))
        sc = tk.Canvas(steps.inner, height=86, bg=SURFACE, highlightthickness=0)
        sc.pack(fill="x")
        sc.bind("<Configure>", lambda e: draw_prep_steps(e.widget, o, e.width))

        # รายการเครื่องดื่ม
        items = RoundFrame(col, fill=SURFACE, border=LINE, radius=18, padx=20, pady=16)
        items.pack(fill="x", padx=24, pady=(14, 0))
        box = items.inner
        tk.Label(box, text=f"เครื่องดื่มในออเดอร์ ({o['cups']} แก้ว)", bg=SURFACE, fg=TEXT,
                 font=(FONT, 13, "bold")).pack(anchor="w")
        for n, it in enumerate(o["items"]):
            if n:
                tk.Frame(box, bg=LINE, height=1).pack(fill="x", pady=(10, 0))
            row = tk.Frame(box, bg=SURFACE)
            row.pack(fill="x", pady=(10, 0))
            done = it["done"] or st in ("ready", "picked_up")
            state = ("done", "เสร็จแล้ว", SUCCESS) if done else \
                    ("making", "กำลังทำ", ACCENT) if st == "making" else ("queued", "รอคิว", TEXT_MUTED)
            dot = tk.Canvas(row, width=26, height=26, bg=SURFACE, highlightthickness=0)
            dot.pack(side="left", anchor="n")
            if done:
                aa_oval(dot, 1, 1, 25, 25, fill=SUCCESS, outline="")
                dot.create_line(7.5, 13.5, 11.5, 17.5, 18.5, 9, fill=ACCENT_INK, width=3, capstyle="round",
                                joinstyle="round")
            else:
                aa_oval(dot, 2, 2, 24, 24, fill=SURFACE, outline=state[2], width=3)
            tk.Label(row, text=state[1], bg=SURFACE, fg=state[2], font=(FONT, 10, "bold")).pack(side="right",
                                                                                              anchor="n")
            t = tk.Frame(row, bg=SURFACE)
            t.pack(side="left", fill="x", expand=True, padx=(12, 0))
            tk.Label(t, text=f"{it['quantity']} × {it['name']}", bg=SURFACE, fg=TEXT,
                     font=(FONT, 12, "bold"), anchor="w").pack(fill="x")
            if it["options"]:
                tk.Label(t, text=it["options"], bg=SURFACE, fg=LATTE, font=(FONT, 10), anchor="w",
                         justify="left", wraplength=520).pack(fill="x")

        note = ("หน้านี้อัปเดตอัตโนมัติ  ร้านจะเด้งแจ้งเตือนเมื่อเครื่องดื่มพร้อมรับ"
                f"\nเวลาเป็นค่าประมาณ (ประมาณ {MINUTES_PER_CUP} นาทีต่อแก้ว)" if st != "picked_up" else
                f"รับเมื่อ {fmt_datetime(o['picked_up_at'])}" if o.get("picked_up_at") else "")
        if note:
            tk.Label(col, text=note, bg=BG, fg=TEXT_MUTED, font=(FONT, 10),
                     justify="center").pack(pady=(14, 20))

    @staticmethod
    def _draw_bar(c, frac, color):
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 10:
            return
        rounded_rect(c, 0, 0, w, h, h / 2, fill=LINE)
        if frac > 0:
            rounded_rect(c, 0, 0, max(h, w * frac), h, h / 2, fill=color)


# =====================================================================
# ส่วนที่ 22: จุดเริ่มโปรแกรม
#   ประกอบด้วย: สร้างโฟลเดอร์ images, เตรียมฐานข้อมูล, เปิดหน้าต่างโปรแกรมแบบเต็มจอ
# บรรทัด 6826 - 6839
# =====================================================================
if __name__ == "__main__":
    if not HAS_PIL:
        print("แนะนำ: ติดตั้ง Pillow เพื่อให้ลายการ์ตูน/ไอคอนเนียนขึ้น  ->  pip install pillow")
    os.makedirs(IMAGE_DIR, exist_ok=True)
    setup_database()
    app = CoffeeApp()
    app.toggle_fullscreen(True)               # เปิดมาเต็มจอเลย (Esc = ย่อ, F11 = กลับมาเต็มจอ)
    app.after(100, lambda: app.toggle_fullscreen(True))   # บางเครื่องต้องสั่งซ้ำหลังหน้าต่างขึ้นจอแล้ว
    app.mainloop()
