"""
database.py  -  ไฟล์ฐานข้อมูล (ไฟล์ 2 จาก 4) ของ Meme Beans Coffee

หน้าที่: ค่าตั้งต้นของร้าน (เมนู ราคา ขนาดแก้ว แต้ม ภาษี) + สร้างตารางในฐานข้อมูล SQLite (coffee2_shop.db)
         + ฟังก์ชันอ่าน/เขียนข้อมูลสมาชิก เมนู ออเดอร์ แต้มสะสม และคิดภาษี
ประกอบด้วย: ส่วนที่ 1 - 4
เชื่อมกับไฟล์อื่น: ไฟล์นี้ไม่ได้ใช้ไฟล์อื่น (เป็นฐานของทุกไฟล์)
                  project.py, receipt.py และ admin.py ดึงข้อมูลและฟังก์ชันจากไฟล์นี้ไปใช้
เปิดโปรแกรมด้วยไฟล์ project.py
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
import os
import time


# =====================================================================
# ส่วนที่ 1: ตั้งค่าและข้อมูลตั้งต้น
#   ประกอบด้วย: ที่อยู่ไฟล์ DB/รูป, เมนูตั้งต้น (กาแฟ/ชา/โซดา), ขนาดแก้ว, วิธีชำระเงิน (เงินสด / QR + สลิป),
#              ภาษีมูลค่าเพิ่ม (VAT_RATE),
#              สต็อกสินค้า (DEFAULT_STOCK, LOW_STOCK_LEVEL, MAX_CUPS_PER_MENU),
#              เวลาทำเครื่องดื่มโดยประมาณ (MINUTES_PER_CUP ใช้บอกลูกค้าว่าอีกประมาณกี่นาที),
#              ระบบแต้ม (BAHT_PER_POINT, TIERS), ส่วนลดที่แลกได้ (REWARDS)
#   แก้ที่นี่เมื่อ: เพิ่ม/แก้ชื่อเมนู ราคา คำอธิบาย เปลี่ยนราคาส่วนต่างของขนาดแก้ว อัตราภาษี หรือกติกาสต็อก
# บรรทัด 21 - 158
# =====================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")             # โฟลเดอร์ใส่รูปเมนู
DB_PATH = os.path.join(BASE_DIR, "coffee2_shop.db")   # ไฟล์อยู่ข้างๆ project.py เสมอ

MENU = [
    ("Americano", 55,
     "กาแฟดำรสชาติกลมกล่อม ไม่มีน้ำตาลและนม ได้รับความนิยมในกลุ่มคนรักสุขภาพและผู้ชื่นชอบกาแฟเรียบง่าย"),
    ("Latte", 65,
     "กาแฟนุ่มละมุน ผสมนมสดและช็อตกาแฟ หอมอร่อย ดื่มง่าย เหมาะสำหรับทุกเพศทุกวัย"),
    ("Espresso (iced)", 60,
     "เมนูสุดเข้มข้นที่เสิร์ฟแบบเย็น สดชื่น เหมาะกับอากาศร้อนของเมืองไทย"),
    ("Thai Iced Coffee", 55,
     "กาแฟดั้งเดิม ผสมนมข้นหวานและนมข้นจืด รสชาติหวานมันที่เป็นเอกลักษณ์"),
    ("Mocha", 70,
     "กาแฟที่ผสมช็อกโกแลต ได้รสชาติหอมหวานและเข้มข้น เหมาะสำหรับคนที่ชอบกาแฟแบบมีลูกเล่น"),
    ("Cappuccino", 65,
     "กาแฟที่มาพร้อมฟองนมเนียนนุ่ม รสชาติกลมกล่อม หอมมันลงตัว"),
    ("Caramel Macchiato", 75,
     "เมนูที่เติมความหวานด้วยคาราเมล ผสมนมและกาแฟ กลิ่นหอมโดดเด่น"),
    ("Espresso", 50,
     "กาแฟแบบช็อตที่เน้นรสชาติเข้มข้น เป็นที่ชื่นชอบของคอกาแฟที่รักความดั้งเดิม"),
    ("Orange Coffee", 75,
     "กาแฟที่ผสมน้ำส้มสด ให้รสชาติเปรี้ยวหวานและสดชื่น กลายเป็นเมนูยอดนิยมในคาเฟ่ยุคใหม่"),
    ("Drip Coffee", 80,
     "กาแฟที่ชงด้วยวิธีกรองแบบพิเศษ ดึงรสชาติและกลิ่นหอมเฉพาะตัวของเมล็ดกาแฟออกมา เหมาะสำหรับสาย Specialty"),
]

TEA_MENU = [
    ("Thai Tea", 50,
     "ชาไทยเข้มข้น หอมใบชา หวานมันกำลังดี ดื่มแล้วชื่นใจ"),
    ("Green Tea", 50,
     "ชาเขียวหอมละมุน รสชาติสดชื่น ไม่ขมจัด"),
    ("Lemon Tea", 50,
     "ชาดำผสมน้ำมะนาว เปรี้ยวหวานสดชื่น ดื่มง่าย"),
    ("Peach Tea", 55,
     "ชาพีชหอมหวาน กลิ่นผลไม้ชัด ดื่มแล้วสดชื่น"),
    ("Matcha Latte", 60,
     "มัทฉะเข้มข้นผสมนมสด หอมชาเขียวญี่ปุ่น นุ่มละมุน"),
    ("Milk Tea", 55,
     "ชานมสไตล์ไต้หวัน ชาดำเข้มข้นผสมนมสด หอมกลมกล่อม หวานกำลังดี"),
    ("Honey Lemon Tea", 55,
     "ชาดำผสมน้ำผึ้งแท้และมะนาวสด เปรี้ยวหวานชุ่มคอ"),
    ("Hojicha Latte", 65,
     "โฮจิฉะ ชาเขียวคั่วญี่ปุ่นผสมนมสด หอมกลิ่นคั่ว นุ่มละมุน"),
    ("Lychee Tea", 55,
     "ชาหอมกลิ่นลิ้นจี่ หวานอ่อนๆ สดชื่น ดื่มง่าย"),
    ("Taro Milk Tea", 60,
     "ชานมเผือกสีม่วงอ่อน หอมมัน หวานละมุน"),
]

SODA_MENU = [
    ("Lemon Soda", 50,
     "โซดามะนาวซ่าสดชื่น เปรี้ยวหวานกำลังดี ดับกระหายทันใจ"),
    ("Blue Lemon Soda", 55,
     "โซดามะนาวสีฟ้าสดใส ซ่าเย็นชื่นใจ"),
    ("Strawberry Soda", 55,
     "โซดาสตรอว์เบอร์รีหวานอมเปรี้ยว หอมผลไม้"),
    ("Passion Fruit Soda", 55,
     "โซดาเสาวรสเปรี้ยวหวานซ่า กลิ่นหอมเขตร้อน"),
    ("Peach Soda", 55,
     "โซดาพีชหอมหวาน ซ่าเบาๆ ดื่มง่าย"),
    ("Lychee Soda", 55,
     "โซดาลิ้นจี่ซ่าเย็น หอมหวานสดชื่น"),
    ("Green Apple Soda", 55,
     "โซดาแอปเปิ้ลเขียว เปรี้ยวอมหวาน ซ่าชื่นใจ"),
    ("Mango Soda", 55,
     "โซดามะม่วงหอมหวาน กลิ่นผลไม้เขตร้อน"),
    ("Blueberry Soda", 55,
     "โซดาบลูเบอร์รี่สีม่วงสวย หวานอมเปรี้ยว"),
    ("Red Lime Soda", 50,
     "น้ำแดงมะนาวโซดา เมนูคลาสสิกแบบไทย หวานซ่าสดชื่น"),
]

# เมนูที่เพิ่มทีหลัง: โปรแกรมจะเพิ่มให้ฐานข้อมูลเดิมที่มีอยู่แล้วโดยอัตโนมัติ (ครั้งเดียว)
MENU_ADDED_V3 = {"Milk Tea", "Honey Lemon Tea", "Hojicha Latte", "Lychee Tea", "Taro Milk Tea",
                 "Lychee Soda", "Green Apple Soda", "Mango Soda", "Blueberry Soda", "Red Lime Soda"}

# หมวดหมู่ -> รายการเมนู (เพิ่มหมวดหรือเมนูใหม่ที่นี่ได้เลย)
MENU_BY_CATEGORY = [
    ("กาแฟ", MENU),
    ("ชา", TEA_MENU),
    ("โซดา", SODA_MENU),
]

# ขนาดแก้ว: (รหัส, ชื่อ, ออนซ์, ราคาที่บวกเพิ่ม)
SIZE_OPTIONS = [
    ("S", "เล็ก", 12, 0),
    ("M", "กลาง", 16, 10),
    ("L", "ใหญ่", 22, 20),
]
SIZE_EXTRA = {code: extra for code, _, _, extra in SIZE_OPTIONS}

SHOP_NAME = "Meme Beans"
EMAIL_CONFIG_PATH = os.path.join(BASE_DIR, "email_config.json")   # ตั้งค่าอีเมลร้านสำหรับส่งใบเสร็จ

# วิธีชำระเงิน: (รหัส, ชื่อที่บันทึกในฐานข้อมูลและใบเสร็จ)
PAYMENT_METHODS = [
    ("cash", "เงินสด"),
    ("qr", "QR พร้อมเพย์"),          # ลูกค้าต้องแนบสลิป แล้วรอแอดมินยืนยันรับเงิน
]
SLIP_MAX_BYTES = 5 * 1024 * 1024    # รูปสลิปโอนเงิน (PNG ที่ย่อแล้ว) ต้องไม่เกิน 5 MB

# ภาษีมูลค่าเพิ่ม (VAT) คิดจากยอดหลังหักส่วนลด
#   VAT_INCLUDED_IN_PRICE = False -> ราคาเมนูยังไม่รวมภาษี บวกเพิ่มตอนชำระเงิน (ลาเต้ 65 -> จ่าย 69.55)
#   VAT_INCLUDED_IN_PRICE = True  -> ราคาเมนูรวมภาษีแล้ว จ่ายเท่าราคาเดิม ใบเสร็จแยกให้เห็นว่าเป็นภาษีเท่าไร
VAT_RATE = 7                      # เปอร์เซ็นต์
VAT_INCLUDED_IN_PRICE = False
VAT_LABEL = f"VAT {VAT_RATE:g}%"                # ชื่อที่แสดงบนหน้าจอและใบเสร็จ

# สต็อกสินค้า (นับเป็นแก้ว): ลดอัตโนมัติเมื่อลูกค้าชำระเงิน แอดมินเติมได้ที่หน้า "เมนูและสต็อก"
DEFAULT_STOCK = 50          # สต็อกตั้งต้นของเมนูใหม่ (และเมนูเดิมตอนเริ่มใช้ระบบสต็อก)
LOW_STOCK_LEVEL = 10        # เหลือไม่เกินนี้ = "ใกล้หมด" (แจ้งเตือนแอดมิน + ป้ายบอกลูกค้า)
MAX_CUPS_PER_MENU = 10      # แต่ละเมนูสั่งได้ไม่เกินกี่แก้วในหนึ่งออเดอร์
MINUTES_PER_CUP = 2         # หลังร้านทำ 1 แก้วใช้เวลาประมาณกี่นาที (บอกลูกค้าว่า "อีกประมาณ N นาที")

# ระบบแต้ม: จ่ายทุก 10 บาทได้ 1 แต้ม (คิดจากราคาเมนูหลังหักส่วนลด ไม่นับ VAT ที่บวกเพิ่ม)
# ระดับสมาชิก (เรียงจากสูงไปต่ำ): (ชื่อระดับ, แต้มสะสมทั้งหมดขั้นต่ำ)
#   "แต้มสะสมทั้งหมด" = แต้มที่ได้จากทุกออเดอร์ตั้งแต่สมัคร + แต้มที่ร้านปรับให้ (รวมแต้มที่แลกส่วนลดไปแล้ว)
#   แลกแต้มแล้วระดับจึงไม่ลด  เลื่อนระดับอัตโนมัติตอนชำระเงิน  แก้เกณฑ์ที่นี่ได้ (เปิดโปรแกรมครั้งถัดไปปรับให้ทุกคน)
BAHT_PER_POINT = 10
TIERS = [("Platinum", 1500), ("Gold", 500), ("Silver", 0)]

# ส่วนลดที่แลกด้วยแต้มได้: (รหัส, ใช้กี่แต้ม, ลดกี่ %)  เพิ่มส่วนลดใหม่ที่นี่ได้
REWARDS = [
    ("D25", 100, 25),
    ("D50", 200, 50),
]
REWARD_BY_CODE = {code: (cost, pct) for code, cost, pct in REWARDS}


# =====================================================================
# ส่วนที่ 2: ฐานข้อมูล: เชื่อมต่อและสร้างตาราง
#   ประกอบด้วย: get_conn, เวลาประเทศไทย (thai_now, thai_today, now_text),
#              setup_database (สร้างตาราง + ใส่เมนูที่ยังไม่มี)
#   แก้ที่นี่เมื่อ: เพิ่มตารางหรือคอลัมน์ใหม่ในฐานข้อมูล
# บรรทัด 161 - 482
# =====================================================================
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------- เวลาประเทศไทย ----------
# ทุกเวลาที่บันทึก (สั่งซื้อ ชำระเงิน สมัครสมาชิก ฯลฯ) เป็นเวลาไทย UTC+7 เสมอ แม้เครื่องตั้งเขตเวลาไว้ผิด
# (ห้ามใช้ CURRENT_TIMESTAMP ของ SQLite เพราะเป็นเวลา UTC ช้ากว่าเวลาไทย 7 ชั่วโมง)
THAI_TZ = timezone(timedelta(hours=7), "Asia/Bangkok")


def thai_now():
    """เวลาปัจจุบันของไทย (ไม่มีข้อมูลเขตเวลาติดมา จึงเทียบกับเวลาที่เก็บในฐานข้อมูลได้ตรง ๆ)"""
    return datetime.now(THAI_TZ).replace(tzinfo=None)


def thai_today():
    """วันที่ปัจจุบันของไทย"""
    return thai_now().date()


def now_text():
    """เวลาไทยตอนนี้ในรูปแบบที่เก็บในฐานข้อมูล เช่น '2026-10-13 03:58:00'"""
    return thai_now().strftime("%Y-%m-%d %H:%M:%S")


def setup_database():
    """สร้างตารางที่ยังไม่มี และใส่เมนูตั้งต้นเฉพาะตอนที่ยังไม่มีข้อมูล
    ไม่ลบข้อมูลเดิม จึงรันกี่ครั้งก็ได้ ข้อมูลสมาชิกไม่หาย"""
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript(f"""
    CREATE TABLE IF NOT EXISTS members (
        member_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT NOT NULL,
        phone         TEXT NOT NULL UNIQUE,
        email         TEXT,
        points        INTEGER NOT NULL DEFAULT 0,
        tier          TEXT NOT NULL DEFAULT 'Silver',
        joined_date   TEXT NOT NULL DEFAULT (datetime('now', '+7 hours')),     -- เวลาไทย
        password_hash TEXT
    );

    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id  INTEGER NOT NULL,
        name         TEXT NOT NULL,
        description  TEXT,
        price        REAL NOT NULL CHECK (price >= 0),
        is_available INTEGER NOT NULL DEFAULT 1,
        stock        INTEGER NOT NULL DEFAULT {DEFAULT_STOCK},
        is_deleted   INTEGER NOT NULL DEFAULT 0,      -- 1 = แอดมินลบเมนูแล้ว (เคยขาย จึงเก็บแถวไว้ให้ประวัติ/รายงาน)
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id      INTEGER,
        order_date     TEXT NOT NULL DEFAULT (datetime('now', '+7 hours')),    -- เวลาไทย
        total_price    REAL NOT NULL DEFAULT 0,
        discount       REAL NOT NULL DEFAULT 0,
        points_earned  INTEGER NOT NULL DEFAULT 0,
        points_used    INTEGER NOT NULL DEFAULT 0,
        status         TEXT NOT NULL DEFAULT 'pending'
                       CHECK (status IN ('pending','paid','cancelled')),
        payment_method TEXT,
        FOREIGN KEY (member_id) REFERENCES members(member_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id   INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity   INTEGER NOT NULL CHECK (quantity > 0),
        unit_price REAL NOT NULL,
        options    TEXT,
        FOREIGN KEY (order_id)   REFERENCES orders(order_id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    CREATE TABLE IF NOT EXISTS point_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id  INTEGER NOT NULL,
        order_id   INTEGER,
        points     INTEGER NOT NULL,
        type       TEXT NOT NULL CHECK (type IN ('earn','redeem','adjust')),
        created_at TEXT NOT NULL DEFAULT (datetime('now', '+7 hours')),
        FOREIGN KEY (member_id) REFERENCES members(member_id),
        FOREIGN KEY (order_id)  REFERENCES orders(order_id)
    );

    CREATE TABLE IF NOT EXISTS coupons (
        coupon_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id   INTEGER NOT NULL,
        reward_code TEXT NOT NULL,
        percent     INTEGER NOT NULL,
        points_cost INTEGER NOT NULL,
        status      TEXT NOT NULL DEFAULT 'unused' CHECK (status IN ('unused','used')),
        redeemed_at TEXT NOT NULL,
        used_at     TEXT,
        order_id    INTEGER,
        FOREIGN KEY (member_id) REFERENCES members(member_id),
        FOREIGN KEY (order_id)  REFERENCES orders(order_id)
    );

    CREATE TABLE IF NOT EXISTS admins (
        admin_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        name          TEXT NOT NULL,
        created_at    TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS payment_slips (
        slip_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id     INTEGER NOT NULL,
        image        BLOB NOT NULL,              -- รูปสลิป (PNG)
        amount       REAL NOT NULL,              -- ยอดที่ต้องโอน ณ ตอนส่งสลิป
        coupon_id    INTEGER,                    -- ส่วนลดที่ลูกค้าเลือก (ใช้จริงตอนแอดมินยืนยัน)
        email        TEXT,                       -- ส่งใบเสร็จไปที่อีเมลนี้หลังยืนยัน (ว่าง = ไม่ส่ง)
        status       TEXT NOT NULL DEFAULT 'waiting'
                     CHECK (status IN ('waiting','approved','rejected')),
        note         TEXT,                       -- เหตุผลที่สลิปไม่ผ่าน
        submitted_at TEXT NOT NULL,
        checked_at   TEXT,
        checked_by   TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );

    CREATE TABLE IF NOT EXISTS app_settings (
        key   TEXT PRIMARY KEY,
        value TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_orders_member     ON orders(member_id);
    CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
    CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
    CREATE INDEX IF NOT EXISTS idx_slips_order       ON payment_slips(order_id);
    """)

    # ไฟล์เก่าที่สร้างไว้ก่อนหน้าไม่มีคอลัมน์ password_hash -> เพิ่มให้
    columns = [r[1] for r in cur.execute("PRAGMA table_info(members)")]
    if "password_hash" not in columns:
        cur.execute("ALTER TABLE members ADD COLUMN password_hash TEXT")
    if "avatar" not in columns:                 # รูปโปรไฟล์ (ไฟล์ PNG เก็บในฐานข้อมูล สำรองข้อมูลแล้วรูปไปด้วย)
        cur.execute("ALTER TABLE members ADD COLUMN avatar BLOB")
    for col, ddl in (("banned", "INTEGER NOT NULL DEFAULT 0"),   # แอดมินแบนแล้ว = 1 (เข้าสู่ระบบ/สั่งซื้อไม่ได้)
                     ("ban_reason", "TEXT"), ("banned_at", "TEXT"), ("banned_by", "TEXT")):
        if col not in columns:
            cur.execute(f"ALTER TABLE members ADD COLUMN {col} {ddl}")

    # ตาราง coupons ที่มีอยู่แล้วแต่โครงสร้างเก่า/ไม่ครบ -> เพิ่มคอลัมน์ที่ขาดให้ (ข้อมูลเดิมไม่หาย)
    coupon_cols = {r[1] for r in cur.execute("PRAGMA table_info(coupons)")}
    if not {"coupon_id", "member_id"} <= coupon_cols:
        # โครงสร้างต่างจากที่โปรแกรมใช้มาก -> เก็บตารางเก่าไว้เป็นชื่อสำรอง แล้วสร้างใหม่
        cur.execute("ALTER TABLE coupons RENAME TO coupons_old_" + thai_now().strftime("%Y%m%d%H%M%S"))
        cur.execute("""CREATE TABLE coupons (
            coupon_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id   INTEGER NOT NULL,
            reward_code TEXT NOT NULL,
            percent     INTEGER NOT NULL,
            points_cost INTEGER NOT NULL,
            status      TEXT NOT NULL DEFAULT 'unused' CHECK (status IN ('unused','used')),
            redeemed_at TEXT NOT NULL,
            used_at     TEXT,
            order_id    INTEGER,
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (order_id)  REFERENCES orders(order_id))""")
    else:
        for col, ddl in (("reward_code", "TEXT NOT NULL DEFAULT ''"),
                         ("percent", "INTEGER NOT NULL DEFAULT 0"),
                         ("points_cost", "INTEGER NOT NULL DEFAULT 0"),
                         ("status", "TEXT NOT NULL DEFAULT 'unused'"),
                         ("redeemed_at", "TEXT NOT NULL DEFAULT ''"),
                         ("used_at", "TEXT"),
                         ("order_id", "INTEGER")):
            if col not in coupon_cols:
                cur.execute(f"ALTER TABLE coupons ADD COLUMN {col} {ddl}")

    # ถ้า coupons เก่ากำหนดค่า status ไว้ต่างจากโปรแกรมนี้ (เช่น 'active') คูปองที่แลกแล้วจะไม่ขึ้นให้เลือก
    # -> สร้างตารางใหม่ตามโครงสร้างที่ถูกต้อง ย้ายข้อมูลเดิมมา แล้วเก็บตารางเก่าไว้เป็นชื่อสำรอง
    row = cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='coupons'").fetchone()
    if row and "DEFAULT 'unused'" not in row[0]:
        cols = {r[1] for r in cur.execute("PRAGMA table_info(coupons)")}
        pick = lambda name, default: name if name in cols else default
        used_cond = " OR ".join(c for c in ("order_id IS NOT NULL" if "order_id" in cols else "",
                                            "used_at IS NOT NULL" if "used_at" in cols else "",
                                            "lower(status) = 'used'" if "status" in cols else "") if c) or "0"
        cur.execute("ALTER TABLE coupons RENAME TO coupons_old_" + thai_now().strftime("%Y%m%d%H%M%S"))
        old_name = cur.execute("SELECT name FROM sqlite_master WHERE name LIKE 'coupons_old_%' "
                               "ORDER BY name DESC LIMIT 1").fetchone()[0]
        cur.execute("""CREATE TABLE coupons (
            coupon_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id   INTEGER NOT NULL,
            reward_code TEXT NOT NULL,
            percent     INTEGER NOT NULL,
            points_cost INTEGER NOT NULL,
            status      TEXT NOT NULL DEFAULT 'unused' CHECK (status IN ('unused','used')),
            redeemed_at TEXT NOT NULL,
            used_at     TEXT,
            order_id    INTEGER,
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (order_id)  REFERENCES orders(order_id))""")
        pct = pick("percent", "0")
        code = (f"CASE WHEN reward_code IS NULL OR reward_code = '' THEN "
                f"CASE {pct} WHEN 25 THEN 'D25' WHEN 50 THEN 'D50' ELSE '' END ELSE reward_code END"
                if "reward_code" in cols else f"CASE {pct} WHEN 25 THEN 'D25' WHEN 50 THEN 'D50' ELSE '' END")
        cur.execute(f"""INSERT INTO coupons (member_id, reward_code, percent, points_cost, status,
                                             redeemed_at, used_at, order_id)
            SELECT member_id, {code}, {pct},
                   {pick("points_cost", "0")},
                   CASE WHEN {used_cond} THEN 'used' ELSE 'unused' END,
                   COALESCE({pick("redeemed_at", "NULL")}, ''),
                   {pick("used_at", "NULL")},
                   CASE WHEN {pick("order_id", "NULL")} IN (SELECT order_id FROM orders)
                        THEN {pick("order_id", "NULL")} END
            FROM {old_name}
            WHERE member_id IN (SELECT member_id FROM members)""")

    # ไฟล์เก่าไม่มีคอลัมน์เวลาชำระเงิน/สถานะส่งใบเสร็จ -> เพิ่มให้
    order_cols = [r[1] for r in cur.execute("PRAGMA table_info(orders)")]
    if "paid_at" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN paid_at TEXT")
    if "receipt_sent" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN receipt_sent INTEGER NOT NULL DEFAULT 0")
    # ระบบภาษี: vat = ภาษีมูลค่าเพิ่มของออเดอร์, paid_total = ยอดที่ลูกค้าจ่ายจริง (รวมภาษีแล้ว)
    if "vat" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN vat REAL NOT NULL DEFAULT 0")
    if "paid_total" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN paid_total REAL")
        # ออเดอร์ที่ชำระก่อนมีระบบภาษี: ยอดที่จ่ายจริง = ราคาหลังหักส่วนลด (ไม่มีภาษี)
        cur.execute("UPDATE orders SET paid_total = total_price - discount WHERE status = 'paid'")

    # สถานะหลังร้าน (คิวทำเครื่องดื่ม): prep_status = queued รอคิว / making กำลังทำ / ready พร้อมรับ /
    # picked_up รับแล้ว  prep_seq เพิ่มทุกครั้งที่แอดมินกดแจ้งลูกค้า (ฝั่งลูกค้าดูเลขนี้เพื่อเด้งแจ้งเตือน)
    # ออเดอร์ที่ชำระก่อนมีระบบนี้ถือว่าลูกค้ารับไปแล้ว (จะได้ไม่ค้างในคิว)
    if "prep_status" not in order_cols:
        cur.execute("ALTER TABLE orders ADD COLUMN prep_status TEXT")
        cur.execute("UPDATE orders SET prep_status = 'picked_up' WHERE status = 'paid'")
    for col, ddl in (("prep_seq", "INTEGER NOT NULL DEFAULT 0"), ("prep_at", "TEXT"), ("prep_by", "TEXT"),
                     ("ready_at", "TEXT"), ("picked_up_at", "TEXT"), ("prep_calls", "INTEGER NOT NULL DEFAULT 0")):
        if col not in order_cols:
            cur.execute(f"ALTER TABLE orders ADD COLUMN {col} {ddl}")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_prep ON orders(prep_status)")
    # done = แก้วรายการนี้ทำเสร็จแล้ว (แอดมินติ๊กทีละรายการ ลูกค้าเห็นว่าเสร็จแล้วกี่แก้ว)
    if "done" not in [r[1] for r in cur.execute("PRAGMA table_info(order_items)")]:
        cur.execute("ALTER TABLE order_items ADD COLUMN done INTEGER NOT NULL DEFAULT 0")

    # ระบบสต็อก: ไฟล์เก่ายังไม่มีคอลัมน์ stock -> เพิ่มให้ ทุกเมนูเริ่มที่ DEFAULT_STOCK แก้ว
    product_cols = [r[1] for r in cur.execute("PRAGMA table_info(products)")]
    if "stock" not in product_cols:
        cur.execute(f"ALTER TABLE products ADD COLUMN stock INTEGER NOT NULL DEFAULT {int(DEFAULT_STOCK)}")
    # ลบเมนู: เมนูที่เคยถูกสั่งแล้วจะถูกซ่อนถาวร (is_deleted = 1) ไม่ลบแถวทิ้ง ประวัติออเดอร์และรายงานจึงยังครบ
    if "is_deleted" not in product_cols:
        cur.execute("ALTER TABLE products ADD COLUMN is_deleted INTEGER NOT NULL DEFAULT 0")

    # ใส่หมวดหมู่/เมนูตั้งต้นเพียงครั้งเดียว (หลังจากนั้นแอดมินแก้ชื่อ/ลบ/ปิดขายได้โดยไม่ถูกใส่กลับ)
    if not cur.execute("SELECT 1 FROM app_settings WHERE key = 'menu_seed_v2'").fetchone():
        for cat_name, items in MENU_BY_CATEGORY:
            cur.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat_name,))
            cat_id = cur.execute(
                "SELECT category_id FROM categories WHERE name = ?", (cat_name,)
            ).fetchone()[0]
            for n, p, d in items:
                if not cur.execute("SELECT 1 FROM products WHERE name = ?", (n,)).fetchone():
                    cur.execute(
                        "INSERT INTO products (category_id, name, price, description) "
                        "VALUES (?, ?, ?, ?)", (cat_id, n, p, d))
        cur.execute("INSERT INTO app_settings (key, value) VALUES ('menu_seed_v2', '1')")

    # เมนูชา/โซดาที่เพิ่มภายหลัง (MENU_ADDED_V3): ใส่ให้ฐานข้อมูลเดิมครั้งเดียว ไม่แตะเมนูเดิม
    if not cur.execute("SELECT 1 FROM app_settings WHERE key = 'menu_seed_v3'").fetchone():
        for cat_name, items in MENU_BY_CATEGORY:
            added = [it for it in items if it[0] in MENU_ADDED_V3]
            if not added:
                continue
            row = cur.execute("SELECT category_id FROM categories WHERE name = ?", (cat_name,)).fetchone()
            if row is None:            # แอดมินเปลี่ยนชื่อหมวดไปแล้ว -> ใช้หมวดของเมนูเดิมในกลุ่มเดียวกัน
                names = [n for n, _, _ in items if n not in MENU_ADDED_V3]
                row = cur.execute(
                    f"SELECT category_id FROM products WHERE name IN ({','.join('?' * len(names))}) "
                    "LIMIT 1", names).fetchone() if names else None
            if row is None:
                cur.execute("INSERT INTO categories (name) VALUES (?)", (cat_name,))
                row = (cur.lastrowid,)
            for n, p, d in added:
                if not cur.execute("SELECT 1 FROM products WHERE name = ?", (n,)).fetchone():
                    cur.execute("INSERT INTO products (category_id, name, price, description) "
                                "VALUES (?, ?, ?, ?)", (row[0], n, p, d))
        cur.execute("INSERT INTO app_settings (key, value) VALUES ('menu_seed_v3', '1')")

    # วันที่สั่ง/วันที่สมัครที่บันทึกก่อนแก้ เป็นเวลา UTC (ค่าเริ่มต้นของ SQLite) ช้ากว่าเวลาไทย 7 ชั่วโมง
    # -> บวก 7 ชั่วโมงให้ครั้งเดียว (จดไว้ใน app_settings ว่าแปลงแล้ว จะได้ไม่บวกซ้ำ)
    if not cur.execute("SELECT 1 FROM app_settings WHERE key = 'thai_time_v1'").fetchone():
        cur.execute("UPDATE orders SET order_date = datetime(order_date, '+7 hours') "
                    "WHERE datetime(order_date) IS NOT NULL")
        cur.execute("UPDATE members SET joined_date = datetime(joined_date, '+7 hours') "
                    "WHERE datetime(joined_date) IS NOT NULL")
        cur.execute("INSERT INTO app_settings (key, value) VALUES ('thai_time_v1', '1')")

    # ระดับสมาชิกให้ตรงเกณฑ์ TIERS เสมอ (เช่น ร้านเพิ่งแก้แต้มขั้นต่ำของแต่ละระดับ)
    for member_id, points, tier in cur.execute("SELECT member_id, points, tier FROM members").fetchall():
        want = tier_for(points + redeemed_total(conn, member_id))
        if want != tier:
            cur.execute("UPDATE members SET tier = ? WHERE member_id = ?", (want, member_id))

    conn.commit()
    conn.close()


# =====================================================================
# ส่วนที่ 3: ระบบสมาชิก (ฐานข้อมูล)
#   ประกอบด้วย: hash_password, verify_password, กติการหัสผ่าน (password_checks, password_problem),
#              is_valid_email, register_member, login_member, get_member, update_member,
#              change_password, ลืมรหัสผ่าน (find_member_by_phone, create_reset_code, reset_password_with_code),
#              รูปโปรไฟล์ (get_member_avatar, set_member_avatar), สมาชิกที่ถูกแบนเข้าสู่ระบบ/สั่งซื้อไม่ได้
#   แก้ที่นี่เมื่อ: แก้กติกาการสมัคร ล็อกอิน แก้ไขข้อมูล หรือรหัสผ่าน (ความยาวรหัส: PASSWORD_MIN_LENGTH,
#              อายุรหัสยืนยัน: RESET_CODE_MINUTES)
# บรรทัด 485 - 757
# =====================================================================
def hash_password(password):
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt.hex() + "$" + h.hex()


def verify_password(password, stored):
    try:
        salt_hex, h_hex = stored.split("$")
    except ValueError:
        return False
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                            bytes.fromhex(salt_hex), 100_000)
    return h.hex() == h_hex


# ---- กติการหัสผ่าน: ยาว 8 ตัวขึ้นไป มีตัวพิมพ์ใหญ่ ตัวพิมพ์เล็ก และตัวเลข ใช้ได้เฉพาะ A-Z a-z 0-9 ----
# ตรวจเฉพาะตอนตั้งรหัสใหม่ (สมัคร / เปลี่ยนรหัส / ลืมรหัส / บัญชีแอดมิน)
# ตอนล็อกอินไม่ตรวจกติกานี้ รหัสเดิมของสมาชิกที่สมัครไว้ก่อนแล้วจึงยังใช้เข้าสู่ระบบได้เหมือนเดิม
PASSWORD_MIN_LENGTH = 8
PASSWORD_HINT = f"{PASSWORD_MIN_LENGTH} ตัวขึ้นไป มี A-Z a-z 0-9"      # ข้อความสั้นต่อท้ายชื่อช่องรหัสผ่าน


def password_checks(password):
    """กติกาแต่ละข้อ และรหัสนี้ผ่านข้อนั้นหรือยัง  คืนค่า [(ชื่อสั้น, ผ่านไหม), ...]
    (หน้าจอใช้ทำเครื่องหมาย ✓ ข้างชื่อช่องรหัสผ่านตอนพิมพ์)"""
    return [
        (f"{PASSWORD_MIN_LENGTH} ตัวขึ้นไป", len(password) >= PASSWORD_MIN_LENGTH),
        ("A-Z", any("A" <= ch <= "Z" for ch in password)),
        ("a-z", any("a" <= ch <= "z" for ch in password)),
        ("0-9", any("0" <= ch <= "9" for ch in password)),
    ]


def password_char_problem(password):
    """มีตัวอักษรที่ห้ามใช้ไหม (ภาษาไทย อักขระพิเศษ เว้นวรรค) คืนค่าข้อความเตือน หรือ "" ถ้าไม่มี"""
    if any("\u0e00" <= ch <= "\u0e7f" for ch in password):
        return "รหัสผ่านมีภาษาไทย ใช้ได้เฉพาะ A-Z a-z 0-9"
    if any(not ("A" <= ch <= "Z" or "a" <= ch <= "z" or "0" <= ch <= "9") for ch in password):
        return "รหัสผ่านห้ามมีอักขระพิเศษหรือเว้นวรรค"
    return ""


def password_problem(password):
    """ตรวจรหัสผ่านใหม่ตามกติกา คืนค่าข้อความบอกสิ่งที่ยังไม่ผ่าน หรือ "" ถ้าผ่านครบทุกข้อ
    เช่น "Abc12345" ผ่าน, "abc12345" -> "รหัสผ่านต้องมี A-Z", "Abc@1234" -> ห้ามมีอักขระพิเศษ"""
    bad = password_char_problem(password)
    if bad:
        return bad
    parts = []
    if len(password) < PASSWORD_MIN_LENGTH:
        parts.append(f"ต้องยาว {PASSWORD_MIN_LENGTH} ตัวขึ้นไป")
    need = [name for name, ok in password_checks(password)[1:] if not ok]   # [1:] = ข้ามข้อความยาว
    if need:
        parts.append(("และมี " if parts else "ต้องมี ") + ", ".join(need))
    return "รหัสผ่าน" + " ".join(parts) if parts else ""


def is_valid_email(email):
    """รูปแบบอีเมล ชื่อ@โดเมน.นามสกุล: มี @ ตัวเดียว ไม่มีช่องว่าง มีชื่อหน้า @
    และโดเมนมีจุดที่ไม่ได้อยู่ตัวแรกหรือตัวสุดท้าย เช่น a@b.com ผ่าน, a@b. หรือ a@.com ไม่ผ่าน"""
    email = email.strip()
    if email.count("@") != 1 or any(ch.isspace() for ch in email):
        return False
    name, domain = email.split("@")
    return name != "" and "." in domain[1:-1]


def register_member(name, phone, password, email=None):
    email = email.strip().lower() if email else None
    if email and not is_valid_email(email):
        return False, "รูปแบบอีเมลไม่ถูกต้อง"
    problem = password_problem(password)
    if problem:
        return False, problem
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO members (name, phone, email, password_hash, joined_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, phone, email or None, hash_password(password), now_text()),
        )
        conn.commit()
        return True, "สมัครสมาชิกสำเร็จ"
    except sqlite3.IntegrityError:
        return False, "เบอร์โทรนี้ถูกใช้สมัครแล้ว"
    finally:
        conn.close()


def login_member(phone, password):
    """ตรวจเบอร์ + รหัสผ่าน คืนค่าข้อมูลสมาชิก หรือ None ถ้าไม่ถูกต้อง
    สมาชิกที่ถูกแบนจะได้ "banned": True และ "ban_reason" (หน้าล็อกอินจะไม่ให้เข้า)"""
    conn = get_conn()
    row = conn.execute(
        "SELECT member_id, name, points, tier, password_hash, email, banned, ban_reason "
        "FROM members WHERE phone = ?",
        (phone,),
    ).fetchone()
    conn.close()
    if row and row[4] and verify_password(password, row[4]):
        return {"member_id": row[0], "name": row[1],
                "points": row[2], "tier": row[3], "email": row[5],
                "banned": bool(row[6]), "ban_reason": row[7]}
    return None


AVATAR_MAX_BYTES = 2 * 1024 * 1024          # รูปโปรไฟล์ (PNG ที่ย่อแล้ว) ต้องไม่เกิน 2 MB


def get_member_avatar(member_id):
    """รูปโปรไฟล์ของสมาชิก (ข้อมูลไฟล์ PNG) ยังไม่มีรูปคืนค่า None"""
    conn = get_conn()
    row = conn.execute("SELECT avatar FROM members WHERE member_id = ?", (member_id,)).fetchone()
    conn.close()
    return bytes(row[0]) if row and row[0] else None


def set_member_avatar(member_id, png):
    """บันทึกรูปโปรไฟล์ (png = ข้อมูลไฟล์ PNG) หรือลบรูป (png = None) คืนค่า (สำเร็จไหม, ข้อความ)"""
    if png is not None:
        if not png.startswith(b"\x89PNG\r\n\x1a\n"):
            return False, "ข้อมูลรูปไม่ถูกต้อง"
        if len(png) > AVATAR_MAX_BYTES:
            return False, "รูปมีขนาดใหญ่เกินไป"
    conn = get_conn()
    cur = conn.execute("UPDATE members SET avatar = ? WHERE member_id = ?",
                       (sqlite3.Binary(png) if png is not None else None, member_id))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return False, "ไม่พบสมาชิก"
    return True, "บันทึกรูปโปรไฟล์แล้ว" if png is not None else "ลบรูปโปรไฟล์แล้ว"


def set_member_email(member_id, email):
    """บันทึกอีเมลให้สมาชิก (ใช้ตอนสมาชิกเก่าที่ยังไม่มีอีเมลกรอกตอนชำระเงิน)"""
    email = email.strip().lower()
    if not is_valid_email(email):
        return False
    conn = get_conn()
    conn.execute("UPDATE members SET email = ? WHERE member_id = ?", (email, member_id))
    conn.commit()
    conn.close()
    return True


def get_member(member_id):
    """ข้อมูลสมาชิกทั้งหมด (ไม่รวมรหัสผ่าน) หรือ None ถ้าไม่พบ"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT member_id, name, phone, email, points, tier, joined_date, banned, ban_reason "
        "FROM members WHERE member_id = ?", (member_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_member(member_id, name, phone, email):
    """แก้ไขชื่อ เบอร์โทร อีเมล คืนค่า (สำเร็จไหม, ข้อความ)"""
    email = email.strip().lower()
    if not is_valid_email(email):
        return False, "รูปแบบอีเมลไม่ถูกต้อง"
    conn = get_conn()
    try:
        conn.execute(
            "UPDATE members SET name = ?, phone = ?, email = ? WHERE member_id = ?",
            (name.strip(), phone.strip(), email, member_id))
        conn.commit()
        return True, "บันทึกข้อมูลเรียบร้อย"
    except sqlite3.IntegrityError:
        return False, "เบอร์โทรนี้มีสมาชิกคนอื่นใช้อยู่แล้ว"
    finally:
        conn.close()


def change_password(member_id, old_password, new_password):
    """เปลี่ยนรหัสผ่าน (ต้องยืนยันรหัสผ่านเดิมก่อน)  รหัสใหม่ต้องผ่านกติกา password_problem"""
    problem = password_problem(new_password)
    if problem:
        return False, problem
    conn = get_conn()
    try:
        row = conn.execute("SELECT password_hash FROM members WHERE member_id = ?",
                           (member_id,)).fetchone()
        if not row or not row[0] or not verify_password(old_password, row[0]):
            return False, "รหัสผ่านปัจจุบันไม่ถูกต้อง"
        conn.execute("UPDATE members SET password_hash = ? WHERE member_id = ?",
                     (hash_password(new_password), member_id))
        conn.commit()
        return True, "เปลี่ยนรหัสผ่านเรียบร้อย"
    finally:
        conn.close()


# ---- ลืมรหัสผ่าน: ส่งรหัสยืนยัน 6 หลักไปที่อีเมลสมาชิก ----
# รหัสเก็บไว้ในหน่วยความจำของโปรแกรม (เก็บแบบแฮช ไม่เก็บตัวเลขจริง) ปิดโปรแกรมแล้วรหัสหายไป
RESET_CODE_MINUTES = 10        # รหัสใช้ได้กี่นาที
RESET_MAX_TRIES = 5            # กรอกรหัสผิดได้กี่ครั้งก่อนต้องขอรหัสใหม่
RESET_RESEND_SECONDS = 60      # ขอรหัสใหม่ได้ทุกกี่วินาที
_reset_codes = {}              # member_id -> {"hash", "expires", "tries", "sent"}


def find_member_by_phone(phone):
    """ข้อมูลสมาชิกจากเบอร์โทร (ใช้ตอนลืมรหัสผ่าน) คืนค่า {member_id, name, email} หรือ None"""
    conn = get_conn()
    row = conn.execute("SELECT member_id, name, email FROM members WHERE phone = ?",
                       (phone.strip(),)).fetchone()
    conn.close()
    return {"member_id": row[0], "name": row[1], "email": row[2]} if row else None


def mask_email(email):
    """ซ่อนอีเมลบางส่วน เช่น somchai@gmail.com -> so*****@gmail.com"""
    name, _, domain = (email or "").partition("@")
    return (name[:2] + "*" * max(len(name) - 2, 3)) + ("@" + domain if domain else "")


def create_reset_code(member_id):
    """สร้างรหัสยืนยัน 6 หลักใหม่ (รหัสเดิมใช้ไม่ได้ทันที)  คืนค่า (รหัส, ข้อความผิดพลาด)"""
    now = time.time()
    old = _reset_codes.get(member_id)
    if old and now - old["sent"] < RESET_RESEND_SECONDS:
        wait = int(RESET_RESEND_SECONDS - (now - old["sent"])) + 1
        return None, f"กรุณารอ {wait} วินาทีก่อนขอรหัสใหม่"
    code = f"{secrets.randbelow(1_000_000):06d}"
    _reset_codes[member_id] = {"hash": hashlib.sha256(code.encode()).hexdigest(),
                               "expires": now + RESET_CODE_MINUTES * 60, "tries": 0, "sent": now}
    return code, ""


def cancel_reset_code(member_id):
    """ลบรหัสยืนยันทิ้ง (เช่น ส่งอีเมลไม่สำเร็จ จะได้ขอใหม่ได้ทันที)"""
    _reset_codes.pop(member_id, None)


def reset_password_with_code(member_id, code, new_password):
    """ตั้งรหัสผ่านใหม่ด้วยรหัสยืนยันจากอีเมล  คืนค่า (สำเร็จไหม, ข้อความ)"""
    problem = password_problem(new_password)
    if problem:
        return False, problem
    rec = _reset_codes.get(member_id)
    if rec is None:
        return False, "กรุณากดขอรหัสยืนยันก่อน"
    if time.time() > rec["expires"]:
        cancel_reset_code(member_id)
        return False, "รหัสยืนยันหมดอายุแล้ว กรุณาขอรหัสใหม่"
    if not secrets.compare_digest(hashlib.sha256(code.strip().encode()).hexdigest(), rec["hash"]):
        rec["tries"] += 1
        left = RESET_MAX_TRIES - rec["tries"]
        if left <= 0:
            cancel_reset_code(member_id)
            return False, "กรอกรหัสผิดหลายครั้งเกินไป กรุณาขอรหัสใหม่"
        return False, f"รหัสยืนยันไม่ถูกต้อง (กรอกได้อีก {left} ครั้ง)"
    conn = get_conn()
    try:
        conn.execute("UPDATE members SET password_hash = ? WHERE member_id = ?",
                     (hash_password(new_password), member_id))
        conn.commit()
    finally:
        conn.close()
    cancel_reset_code(member_id)
    return True, "ตั้งรหัสผ่านใหม่เรียบร้อย"


# =====================================================================
# ส่วนที่ 4: เมนูและออเดอร์ (ฐานข้อมูล)
#   ประกอบด้วย: get_categories, get_products (ไม่รวมเมนูที่ลบแล้ว), get_popular_products,
#              สต็อก (stock_status, cup_limit),
#              create_order (ตรวจสต็อก + ไม่เกิน 10 แก้วต่อเมนู), mark_order_paid (ตัดสต็อก), cancel_order,
#              get_order_receipt, discount_amount, ภาษี 7% (round_money, vat_split, order_amounts),
#              redeem_coupon (แลกส่วนลดด้วยแต้ม), get_coupons, get_point_history,
#              ประวัติการสั่งซื้อ (get_member_orders แบ่งหน้าได้, get_member_favorites เมนูที่สั่งบ่อย,
#              member_order_stats, get_product, size_from_options),
#              สลิปโอนเงิน QR (submit_payment_slip, get_payment_state, get_slip_image, get_member_open_slips),
#              ระดับสมาชิก (tier_for, tier_progress, get_member_tier เกณฑ์ + ความคืบหน้าถึงระดับถัดไป),
#              สถานะหลังร้าน (PREP_STEPS, fill_prep_details คิวก่อนหน้า/แก้วที่เสร็จ, get_member_active_orders,
#              get_order_prep)
#   แก้ที่นี่เมื่อ: แก้การดึงเมนูหรือการบันทึกออเดอร์ (ต่อไปจะเพิ่มแต้ม/ชำระเงินที่นี่)
# บรรทัด 760 - 1347
# =====================================================================
def get_categories():
    """คืนค่า [(category_id, name), ...]"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT category_id, name FROM categories ORDER BY category_id"
    ).fetchall()
    conn.close()
    return rows


def get_products(category_id=None):
    """คืนค่าลิสต์ของ dict เมนู (ทุกหมวด ถ้าไม่ระบุ category_id) ไม่รวมเมนูที่แอดมินลบแล้ว"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    sql = ("SELECT product_id, category_id, name, description, price, is_available, stock "
           "FROM products WHERE is_deleted = 0")
    params = ()
    if category_id is not None:
        sql += " AND category_id = ?"
        params = (category_id,)
    sql += " ORDER BY product_id"
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def get_product(product_id):
    """เมนู 1 รายการ (รวมเมนูที่ปิดขาย) ไม่พบคืนค่า None
    เมนูที่แอดมินลบแล้วแต่เคยขาย ยังคืนค่าได้ (ปิดขาย สต็อก 0 จึงสั่งเพิ่มไม่ได้)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT product_id, category_id, name, description, price, is_available, stock "
                       "FROM products WHERE product_id = ?", (product_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_popular_products(limit=8):
    """เมนูแนะนำ: เรียงตามยอดขายรวม (ถ้ายังไม่มีออเดอร์ เรียงตามลำดับเมนู)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT p.product_id, p.category_id, p.name, p.description, p.price, "
        "p.is_available, p.stock, COALESCE(SUM(oi.quantity), 0) AS sold "
        "FROM products p LEFT JOIN order_items oi ON oi.product_id = p.product_id "
        "WHERE p.is_available = 1 AND p.is_deleted = 0 "
        "GROUP BY p.product_id ORDER BY sold DESC, p.product_id LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def stock_status(stock):
    """สถานะสต็อก: "out" หมดแล้ว / "low" ใกล้หมด (เหลือไม่เกิน LOW_STOCK_LEVEL) / "ok" ปกติ"""
    if stock <= 0:
        return "out"
    return "low" if stock <= LOW_STOCK_LEVEL else "ok"


def cup_limit(stock):
    """เมนูนี้สั่งได้มากสุดกี่แก้วในหนึ่งออเดอร์: ไม่เกิน MAX_CUPS_PER_MENU และไม่เกินสต็อกที่เหลือ"""
    return max(0, min(MAX_CUPS_PER_MENU, stock))


def create_order(member_id, cart_items):
    """บันทึกออเดอร์ (สถานะ pending) และรายการสินค้า คืนค่า (order_id, ยอดรวม)
    ราคาอ่านจากตาราง products ณ ตอนสั่ง แล้วเก็บลง unit_price
    ตรวจก่อนบันทึก: เมนูเปิดขาย, แต่ละเมนูไม่เกิน MAX_CUPS_PER_MENU แก้ว และสต็อกพอ"""
    conn = get_conn()
    try:
        if member_id is not None and conn.execute(
                "SELECT banned FROM members WHERE member_id = ?", (member_id,)).fetchone() == (1,):
            raise ValueError("บัญชีนี้ถูกระงับการใช้งาน กรุณาติดต่อพนักงานที่ร้าน")
        lines = []
        cups = {}                                   # product_id -> จำนวนแก้วรวมทุกตัวเลือก
        for it in cart_items:
            row = conn.execute(
                "SELECT price, is_available, stock FROM products WHERE product_id = ?",
                (it["product_id"],),
            ).fetchone()
            if row is None or not row[1]:
                raise ValueError(f"เมนู {it['name']} ไม่พร้อมขาย")
            unit = row[0] + SIZE_EXTRA.get(it.get("size"), 0)
            lines.append((it["product_id"], it["qty"], unit, it["options"]))
            cups[it["product_id"]] = cups.get(it["product_id"], 0) + it["qty"]
            total_cups, stock = cups[it["product_id"]], row[2]
            if total_cups > MAX_CUPS_PER_MENU:
                raise ValueError(f"เมนู {it['name']} สั่งได้ไม่เกิน {MAX_CUPS_PER_MENU} แก้วต่อออเดอร์ "
                                 f"(ในตะกร้ามี {total_cups} แก้ว)")
            if total_cups > stock:
                raise ValueError(f"เมนู {it['name']} หมดแล้ว" if stock <= 0 else
                                 f"เมนู {it['name']} เหลือในสต็อก {stock} แก้ว (ในตะกร้ามี {total_cups} แก้ว)")

        total = sum(qty * price for _, qty, price, _ in lines)
        cur = conn.execute(
            "INSERT INTO orders (member_id, total_price, status, order_date) VALUES (?, ?, 'pending', ?)",
            (member_id, total, now_text()),            # วันที่สั่งเป็นเวลาไทย
        )
        order_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price, options) "
            "VALUES (?, ?, ?, ?, ?)",
            [(order_id, pid, qty, price, opt) for pid, qty, price, opt in lines],
        )
        conn.commit()
        return order_id, total
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_member_orders(member_id, limit=30, offset=0):
    """ประวัติการสั่งซื้อของสมาชิก (เฉพาะออเดอร์ที่ชำระเงินแล้ว ล่าสุดอยู่ก่อน)
    limit/offset ใช้แบ่งหน้า เช่น หน้า 2 ทีละ 10 ออเดอร์ = limit 10, offset 10
    แต่ละออเดอร์มี items = [{product_id, name, quantity, unit_price, options, is_available, stock}]"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    orders = [dict(r) for r in conn.execute(
        "SELECT order_id, COALESCE(paid_at, order_date) AS paid_at, total_price, discount, "
        "vat, paid_total, points_earned, payment_method, prep_status FROM orders "
        "WHERE member_id = ? AND status = 'paid' "
        "ORDER BY COALESCE(paid_at, order_date) DESC, order_id DESC LIMIT ? OFFSET ?",
        (member_id, limit, offset)).fetchall()]
    for o in orders:
        o["items"] = [dict(r) for r in conn.execute(
            "SELECT oi.product_id, p.name, oi.quantity, oi.unit_price, oi.options, p.is_available, p.stock "
            "FROM order_items oi JOIN products p ON p.product_id = oi.product_id "
            "WHERE oi.order_id = ? ORDER BY oi.item_id", (o["order_id"],)).fetchall()]
    conn.close()
    return orders


def get_member_favorites(member_id, limit=5):
    """เมนูที่สมาชิกสั่งบ่อยที่สุด (นับจากออเดอร์ที่ชำระแล้วทั้งหมด เรียงตามจำนวนแก้ว)
    คืนค่า [{product_id, name, price, cups แก้วรวม, times กี่ออเดอร์, spent ยอดรวม, is_available, stock}]"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(
        "SELECT oi.product_id, p.name, p.price, p.is_available, p.stock, "
        "SUM(oi.quantity) AS cups, COUNT(DISTINCT oi.order_id) AS times, "
        "SUM(oi.quantity * oi.unit_price) AS spent, MAX(COALESCE(o.paid_at, o.order_date)) AS last_at "
        "FROM order_items oi JOIN orders o ON o.order_id = oi.order_id "
        "JOIN products p ON p.product_id = oi.product_id "
        "WHERE o.member_id = ? AND o.status = 'paid' AND p.is_deleted = 0 GROUP BY oi.product_id "
        "ORDER BY cups DESC, times DESC, last_at DESC LIMIT ?", (member_id, limit)).fetchall()]
    conn.close()
    return rows


def member_order_stats(member_id):
    """(จำนวนออเดอร์ที่ชำระแล้ว, ยอดใช้จ่ายรวมที่จ่ายจริง หลังหักส่วนลดและรวมภาษีแล้ว) ของสมาชิก"""
    conn = get_conn()
    n, total = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(COALESCE(paid_total, total_price - discount)), 0) FROM orders "
        "WHERE member_id = ? AND status = 'paid'", (member_id,)).fetchone()
    conn.close()
    return n, total


def size_from_options(options):
    """อ่านขนาดแก้วจากข้อความตัวเลือก เช่น "เย็น, หวานปกติ, ขนาด L, ..." -> "L" (ไม่พบคืนค่า None)"""
    for part in (options or "").split(","):
        words = part.split()
        if len(words) >= 2 and words[0] == "ขนาด":
            return words[1] if words[1] in SIZE_EXTRA else None
    return None


def tier_for(points):
    """ระดับสมาชิกตามแต้มสะสมทั้งหมด"""
    for name, need in TIERS:
        if points >= need:
            return name
    return TIERS[-1][0]


def tier_progress(lifetime):
    """ระดับตอนนี้ + ระยะถึงระดับถัดไป จากแต้มสะสมทั้งหมด (lifetime)
    คืนค่า {tier, floor แต้มขั้นต่ำของระดับนี้, next_tier (None = ระดับสูงสุดแล้ว), next_need แต้มขั้นต่ำของระดับถัดไป,
           to_next อีกกี่แต้ม, progress 0-1 (ความคืบหน้าจากระดับนี้ไประดับถัดไป)}"""
    ladder = sorted(TIERS, key=lambda t: t[1])            # ต่ำ -> สูง
    tier = tier_for(lifetime)
    i = [name for name, _ in ladder].index(tier)
    floor = ladder[i][1]
    if i + 1 == len(ladder):
        return {"tier": tier, "floor": floor, "next_tier": None, "next_need": None, "to_next": 0, "progress": 1.0}
    nxt, need = ladder[i + 1]
    return {"tier": tier, "floor": floor, "next_tier": nxt, "next_need": need, "to_next": need - lifetime,
            "progress": max(0.0, min(1.0, (lifetime - floor) / (need - floor)))}


def get_member_tier(member_id):
    """ข้อมูลหน้า "ระดับสมาชิก": {points แต้มคงเหลือ, redeemed แต้มที่แลกไปแล้ว, lifetime แต้มสะสมทั้งหมด}
    + ข้อมูลจาก tier_progress  (ระดับที่บันทึกไว้ไม่ตรงเกณฑ์จะแก้ให้ตรง)  ไม่พบสมาชิกคืนค่า None"""
    conn = get_conn()
    try:
        row = conn.execute("SELECT points, tier FROM members WHERE member_id = ?", (member_id,)).fetchone()
        if row is None:
            return None
        redeemed = redeemed_total(conn, member_id)
        info = {"points": row[0], "redeemed": redeemed, "lifetime": row[0] + redeemed}
        info.update(tier_progress(info["lifetime"]))
        if row[1] != info["tier"]:
            conn.execute("UPDATE members SET tier = ? WHERE member_id = ?", (info["tier"], member_id))
            conn.commit()
        return info
    finally:
        conn.close()


def mark_order_paid(order_id, payment_method, coupon_id=None):
    """บันทึกว่าชำระเงินแล้ว: ตัดสต็อก + สถานะ paid + (ใช้ส่วนลด) + คิดภาษี + ให้แต้ม + เลื่อนระดับสมาชิก
    ทำได้เฉพาะออเดอร์ที่ยังเป็น pending  (สต็อกไม่พอ -> raise และไม่บันทึกอะไรเลย)
    คืนค่า {points_earned, points, tier, discount, vat, paid_total}
    coupon_id = คูปองที่เลือกใช้ (ต้องเป็นของสมาชิกคนนี้และยังไม่ถูกใช้)"""
    conn = get_conn()
    try:
        row = conn.execute("SELECT member_id, total_price, status FROM orders WHERE order_id = ?",
                           (order_id,)).fetchone()
        if row is None:
            raise ValueError("ไม่พบออเดอร์นี้")
        member_id, total, status = row
        if status != "pending":
            raise ValueError("ออเดอร์นี้ไม่ได้อยู่ในสถานะรอชำระเงิน")
        now = thai_now().strftime("%Y-%m-%d %H:%M:%S")

        # ตัดสต็อกตามจำนวนแก้วของแต่ละเมนู (ลดได้เฉพาะเมื่อสต็อกพอ)
        for product_id, name, cups in conn.execute(
                "SELECT oi.product_id, p.name, SUM(oi.quantity) FROM order_items oi "
                "JOIN products p ON p.product_id = oi.product_id WHERE oi.order_id = ? "
                "GROUP BY oi.product_id", (order_id,)).fetchall():
            cur = conn.execute("UPDATE products SET stock = stock - ? WHERE product_id = ? AND stock >= ?",
                               (cups, product_id, cups))
            if cur.rowcount == 0:
                left = conn.execute("SELECT stock FROM products WHERE product_id = ?",
                                    (product_id,)).fetchone()[0]
                raise ValueError(f"สต็อก {name} ไม่พอ (เหลือ {left} แก้ว แต่สั่ง {cups} แก้ว) "
                                 "กรุณาแก้จำนวนในตะกร้า")

        discount = 0
        if coupon_id is not None:
            c = conn.execute("SELECT percent FROM coupons WHERE coupon_id = ? "
                             "AND member_id = ? AND status = 'unused'",
                             (coupon_id, member_id)).fetchone()
            if c is None:
                raise ValueError("ส่วนลดนี้ใช้ไม่ได้ (อาจถูกใช้ไปแล้ว)")
            discount = discount_amount(total, c[0])
            conn.execute("UPDATE coupons SET status = 'used', used_at = ?, order_id = ? "
                         "WHERE coupon_id = ?", (now, order_id, coupon_id))

        vat, paid_total = vat_split(total - discount)       # ภาษีมูลค่าเพิ่ม + ยอดที่ลูกค้าจ่ายจริง
        earned = int((total - discount) // BAHT_PER_POINT)  # แต้มคิดจากราคาสินค้าหลังลด (ไม่นับภาษี)
        conn.execute(                                  # จ่ายแล้ว = เข้าคิวหลังร้าน (รอคิว)
            "UPDATE orders SET status = 'paid', payment_method = ?, paid_at = ?, "
            "discount = ?, vat = ?, paid_total = ?, points_earned = ?, "
            "prep_status = 'queued', prep_at = ?, prep_seq = 0 WHERE order_id = ?",
            (payment_method, now, discount, vat, paid_total, earned, now, order_id))

        points = tier = None
        if member_id is not None:
            current = conn.execute("SELECT points FROM members WHERE member_id = ?",
                                   (member_id,)).fetchone()[0]
            points = current + earned
            # ระดับสมาชิกดูจากแต้มที่เคยได้ทั้งหมด (ไม่ลดลงเมื่อเอาแต้มไปแลกส่วนลด)
            tier = tier_for(points + redeemed_total(conn, member_id))
            conn.execute("UPDATE members SET points = ?, tier = ? WHERE member_id = ?",
                         (points, tier, member_id))
            if earned:
                conn.execute(
                    "INSERT INTO point_history (member_id, order_id, points, type, created_at) "
                    "VALUES (?, ?, ?, 'earn', ?)", (member_id, order_id, earned, now))
        conn.commit()
        return {"points_earned": earned, "points": points, "tier": tier, "discount": discount,
                "vat": vat, "paid_total": paid_total}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def cancel_order(order_id):
    """ยกเลิกออเดอร์ที่ยังไม่ชำระเงิน (ออเดอร์ที่ชำระแล้วจะไม่ถูกแตะ)"""
    conn = get_conn()
    conn.execute("UPDATE orders SET status = 'cancelled' "
                 "WHERE order_id = ? AND status = 'pending'", (order_id,))
    conn.commit()
    conn.close()


# ---------- สลิปโอนเงิน (จ่ายด้วย QR พร้อมเพย์) ----------
# ลูกค้าแนบสลิป -> ออเดอร์ยังเป็น pending แต่มีสลิปสถานะ waiting (รอตรวจ)
# แอดมินกด "ยืนยันรับเงิน" -> mark_order_paid (ตัดสต็อก ให้แต้ม) + สลิป approved
# แอดมินกด "สลิปไม่ผ่าน" -> สลิป rejected + เหตุผล  ลูกค้าแนบสลิปใหม่ได้ (เก็บประวัติทุกใบ)
def submit_payment_slip(order_id, image, amount, coupon_id=None, email=None):
    """ส่งสลิปโอนเงินของออเดอร์ที่ยังรอชำระ คืนค่า slip_id  (ผิดเงื่อนไขจะ raise ValueError)"""
    if not image or not image.startswith(b"\x89PNG"):
        raise ValueError("ไฟล์สลิปไม่ถูกต้อง")
    if len(image) > SLIP_MAX_BYTES:
        raise ValueError("รูปสลิปใหญ่เกินไป (ไม่เกิน 5 MB)")
    conn = get_conn()
    try:
        row = conn.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,)).fetchone()
        if row is None:
            raise ValueError("ไม่พบออเดอร์นี้")
        if row[0] != "pending":
            raise ValueError("ออเดอร์นี้ไม่ได้อยู่ในสถานะรอชำระเงิน")
        if conn.execute("SELECT 1 FROM payment_slips WHERE order_id = ? AND status = 'waiting'",
                        (order_id,)).fetchone():
            raise ValueError("ส่งสลิปของออเดอร์นี้ไปแล้ว กำลังรอร้านตรวจสอบ")
        cur = conn.execute(
            "INSERT INTO payment_slips (order_id, image, amount, coupon_id, email, submitted_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, image, amount, coupon_id, email or None,
             thai_now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def _slip_info(row):
    keys = ("slip_id", "order_id", "amount", "coupon_id", "email", "status", "note",
            "submitted_at", "checked_at", "checked_by")
    return dict(zip(keys, row)) if row else None


_SLIP_COLS = ("slip_id, order_id, amount, coupon_id, email, status, note, submitted_at, "
              "checked_at, checked_by")


def get_payment_state(order_id):
    """สถานะการชำระเงินของออเดอร์ (ใช้ทั้งฝั่งลูกค้าที่รอผล และฝั่งแอดมิน)
    คืนค่า {"status": pending/paid/cancelled, "receipt_sent": 0/1, "slip": สลิปใบล่าสุด (ไม่มีรูป) หรือ None}"""
    conn = get_conn()
    o = conn.execute("SELECT status, receipt_sent FROM orders WHERE order_id = ?", (order_id,)).fetchone()
    slip = conn.execute(f"SELECT {_SLIP_COLS} FROM payment_slips WHERE order_id = ? "
                        "ORDER BY slip_id DESC LIMIT 1", (order_id,)).fetchone()
    conn.close()
    if o is None:
        return None
    return {"status": o[0], "receipt_sent": o[1], "slip": _slip_info(slip)}


def get_slip_image(slip_id):
    conn = get_conn()
    row = conn.execute("SELECT image FROM payment_slips WHERE slip_id = ?", (slip_id,)).fetchone()
    conn.close()
    return bytes(row[0]) if row else None


def get_member_open_slips(member_id):
    """ออเดอร์ของสมาชิกที่ส่งสลิปแล้วแต่ยังไม่จบ: สลิปล่าสุดรอตรวจ (waiting) หรือไม่ผ่าน (rejected)"""
    conn = get_conn()
    rows = conn.execute(
        f"SELECT {', '.join('s.' + c.strip() for c in _SLIP_COLS.split(','))} "
        "FROM payment_slips s JOIN orders o ON o.order_id = s.order_id "
        "WHERE o.member_id = ? AND o.status = 'pending' AND s.status IN ('waiting', 'rejected') "
        "AND s.slip_id = (SELECT MAX(slip_id) FROM payment_slips WHERE order_id = s.order_id) "
        "ORDER BY s.slip_id", (member_id,)).fetchall()
    conn.close()
    return [_slip_info(r) for r in rows]


# ---------- สถานะหลังร้าน: ลูกค้าติดตามได้ว่าออเดอร์ถึงไหนแล้ว ----------
# ชำระเงินแล้ว -> รอคิว -> กำลังทำ (แอดมินติ๊กแก้วที่เสร็จทีละรายการ) -> พร้อมรับ -> รับแล้ว
# แอดมินเปลี่ยนสถานะที่หน้า "คิวหลังร้าน" (admin.py) ฝั่งลูกค้าเช็กทุก 3 วินาทีแล้วเด้งแจ้งเตือน
PREP_STEPS = [("queued", "รอคิว"), ("making", "กำลังทำ"), ("ready", "พร้อมรับ"), ("picked_up", "รับแล้ว")]
PREP_LABEL = dict(PREP_STEPS)
PREP_ACTIVE = ("queued", "making", "ready")            # ยังไม่จบ (ลูกค้ายังต้องติดตาม)
_PREP_COLS = ("o.order_id, o.member_id, COALESCE(o.paid_at, o.order_date) AS paid_at, o.prep_status, "
              "o.prep_seq, o.prep_at, o.ready_at, o.picked_up_at, o.prep_calls, o.payment_method, "
              "COALESCE(o.paid_total, o.total_price - o.discount) AS paid")


def prep_queue(conn):
    """คิวทำเครื่องดื่มทั้งร้าน (ออเดอร์ที่ยังไม่พร้อมรับ) ตามลำดับที่หลังร้านจะทำ:
    ออเดอร์ที่กำลังทำอยู่มาก่อน แล้วตามด้วยออเดอร์ที่รอคิวตามเวลาที่ชำระเงิน
    คืนค่า [(order_id, prep_status, จำนวนแก้วที่ยังไม่เสร็จ)]"""
    return [tuple(r) for r in conn.execute(
        "SELECT o.order_id, o.prep_status, "
        "COALESCE(SUM(CASE WHEN oi.done = 0 THEN oi.quantity ELSE 0 END), 0) "
        "FROM orders o JOIN order_items oi ON oi.order_id = o.order_id "
        "WHERE o.status = 'paid' AND o.prep_status IN ('queued', 'making') GROUP BY o.order_id "
        "ORDER BY CASE o.prep_status WHEN 'making' THEN 0 ELSE 1 END, "
        "COALESCE(o.paid_at, o.order_date), o.order_id").fetchall()]


def fill_prep_details(conn, orders):
    """เติมข้อมูลที่ลูกค้า/หลังร้านต้องใช้ให้ทุกออเดอร์ (แก้ list ที่ส่งมา และคืนค่า list เดิม)
    items [{item_id, name, quantity, options, done}], cups แก้วทั้งหมด, cups_done แก้วที่เสร็จแล้ว,
    ahead_orders / ahead_cups = ออเดอร์/แก้วที่ต้องทำก่อนถึงคิว (เฉพาะออเดอร์ที่รอคิว),
    wait_minutes = อีกประมาณกี่นาทีจะเสร็จ (คิวก่อนหน้า + แก้วของตัวเองที่ยังไม่เสร็จ)"""
    queue = prep_queue(conn)
    for o in orders:
        o["items"] = [{"item_id": r[0], "name": r[1], "quantity": r[2], "options": r[3], "done": r[4]}
                      for r in conn.execute(
                          "SELECT oi.item_id, p.name, oi.quantity, oi.options, oi.done FROM order_items oi "
                          "JOIN products p ON p.product_id = oi.product_id WHERE oi.order_id = ? "
                          "ORDER BY oi.item_id", (o["order_id"],))]
        o["cups"] = sum(i["quantity"] for i in o["items"])
        o["cups_done"] = sum(i["quantity"] for i in o["items"] if i["done"])
        ahead_orders = ahead_cups = 0
        if o["prep_status"] == "queued":
            for oid, _status, left in queue:
                if oid == o["order_id"]:
                    break
                ahead_orders += 1
                ahead_cups += left
        o["ahead_orders"], o["ahead_cups"] = ahead_orders, ahead_cups
        left = o["cups"] - o["cups_done"]
        o["wait_minutes"] = ((ahead_cups + left) * MINUTES_PER_CUP
                             if o["prep_status"] in ("queued", "making") else 0)
    return orders


def get_member_active_orders(member_id):
    """ออเดอร์ของสมาชิกที่ชำระแล้วแต่ยังไม่ได้รับ (รอคิว / กำลังทำ / พร้อมรับ) เก่าสุดก่อน
    พร้อมคิวก่อนหน้าและจำนวนแก้วที่เสร็จแล้ว (ดู fill_prep_details)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(
        f"SELECT {_PREP_COLS} FROM orders o WHERE o.member_id = ? AND o.status = 'paid' "
        "AND o.prep_status IN ('queued', 'making', 'ready') "
        "ORDER BY COALESCE(o.paid_at, o.order_date), o.order_id", (member_id,)).fetchall()]
    fill_prep_details(conn, rows)
    conn.close()
    return rows


def get_order_prep(order_id):
    """สถานะหลังร้านของออเดอร์เดียว (หน้าติดตามออเดอร์ของลูกค้า) ไม่พบหรือยังไม่ชำระคืนค่า None"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute(f"SELECT {_PREP_COLS} FROM orders o WHERE o.order_id = ? AND o.status = 'paid' "
                       "AND o.prep_status IS NOT NULL", (order_id,)).fetchone()
    out = fill_prep_details(conn, [dict(row)])[0] if row else None
    conn.close()
    return out


def get_order_receipt(order_id):
    """ข้อมูลออเดอร์ทั้งหมดสำหรับทำใบเสร็จ (รายการสินค้า ยอด แต้ม ชื่อสมาชิก)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    o = conn.execute(
        "SELECT o.*, m.name AS member_name, m.points AS member_points "
        "FROM orders o LEFT JOIN members m ON m.member_id = o.member_id "
        "WHERE o.order_id = ?", (order_id,)).fetchone()
    if o is None:
        conn.close()
        return None
    items = conn.execute(
        "SELECT p.name AS name, oi.options AS options, oi.quantity AS quantity, "
        "oi.unit_price AS unit_price FROM order_items oi "
        "JOIN products p ON p.product_id = oi.product_id "
        "WHERE oi.order_id = ? ORDER BY oi.item_id", (order_id,)).fetchall()
    coupon = conn.execute("SELECT percent, points_cost FROM coupons WHERE order_id = ?",
                          (order_id,)).fetchone()
    conn.close()
    receipt = dict(o)
    receipt["items"] = [dict(i) for i in items]
    receipt["coupon"] = {"percent": coupon[0], "points_cost": coupon[1]} if coupon else None
    return receipt


def set_receipt_sent(order_id, sent=True):
    conn = get_conn()
    conn.execute("UPDATE orders SET receipt_sent = ? WHERE order_id = ?",
                 (1 if sent else 0, order_id))
    conn.commit()
    conn.close()


def discount_amount(total, percent):
    """ส่วนลดเป็นบาท (ปัดเป็นบาทเต็ม) เช่น 205 บาท ลด 25% = 51 บาท"""
    return int(total * percent / 100 + 0.5)


def round_money(v):
    """ปัดเงินเป็นทศนิยม 2 ตำแหน่ง แบบปัดครึ่งขึ้น (ใช้ Decimal กันเลขทศนิยมของคอมพิวเตอร์เพี้ยน)"""
    return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def vat_split(amount):
    """คิดภาษีมูลค่าเพิ่มจากยอดหลังหักส่วนลด คืนค่า (ภาษี, ยอดที่ลูกค้าต้องจ่าย)
    ราคายังไม่รวมภาษี: 65 -> (4.55, 69.55)    ราคารวมภาษีแล้ว: 65 -> (4.25, 65.0)"""
    amount = round_money(amount)
    rate = Decimal(str(VAT_RATE)) / 100
    if VAT_INCLUDED_IN_PRICE:
        return float(round_money(amount * rate / (1 + rate))), float(amount)
    vat = round_money(amount * rate)
    return float(vat), float(amount + vat)


def order_amounts(o):
    """แยกยอดเงินของออเดอร์ (o ต้องมี total_price, discount, vat, paid_total)
    คืนค่า {subtotal ราคาสินค้า, discount ส่วนลด, net หลังลด, vat ภาษี,
            paid ยอดที่จ่ายจริง, included ภาษีรวมอยู่ในราคาแล้วหรือไม่}
    ออเดอร์ที่ชำระก่อนมีระบบภาษี: vat = 0 และ paid = net"""
    o = dict(o)
    net = float(round_money(o["total_price"] - o["discount"]))
    vat = o.get("vat") or 0
    paid = net if o.get("paid_total") is None else o["paid_total"]
    return {"subtotal": o["total_price"], "discount": o["discount"], "net": net, "vat": vat,
            "paid": paid, "included": bool(vat) and abs(paid - net) < 0.005}


def redeemed_total(conn, member_id):
    """แต้มที่สมาชิกเคยใช้แลกส่วนลดไปทั้งหมด"""
    return conn.execute("SELECT COALESCE(-SUM(points), 0) FROM point_history "
                        "WHERE member_id = ? AND type = 'redeem'", (member_id,)).fetchone()[0]


def redeem_coupon(member_id, reward_code):
    """แลกส่วนลดด้วยแต้ม: หักแต้ม + สร้างคูปองสถานะ unused  คืนค่า {coupon_id, points}
    (ระดับสมาชิกไม่ลดลงเมื่อแลกแต้ม เพราะดูจากแต้มที่เคยได้ทั้งหมด)"""
    if reward_code not in REWARD_BY_CODE:
        raise ValueError("ไม่พบส่วนลดนี้")
    cost, percent = REWARD_BY_CODE[reward_code]
    now = thai_now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn()
    try:
        cur = conn.execute("UPDATE members SET points = points - ? "
                           "WHERE member_id = ? AND points >= ?", (cost, member_id, cost))
        if cur.rowcount == 0:
            raise ValueError(f"แต้มไม่พอ (ต้องใช้ {cost} แต้ม)")
        cur = conn.execute(
            "INSERT INTO coupons (member_id, reward_code, percent, points_cost, status, redeemed_at) "
            "VALUES (?, ?, ?, ?, 'unused', ?)", (member_id, reward_code, percent, cost, now))
        coupon_id = cur.lastrowid
        conn.execute("INSERT INTO point_history (member_id, order_id, points, type, created_at) "
                     "VALUES (?, NULL, ?, 'redeem', ?)", (member_id, -cost, now))
        points = conn.execute("SELECT points FROM members WHERE member_id = ?",
                              (member_id,)).fetchone()[0]
        conn.commit()
        return {"coupon_id": coupon_id, "points": points}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_coupons(member_id):
    """คูปองทั้งหมดของสมาชิก (เก่า -> ใหม่)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT coupon_id, reward_code, percent, points_cost, status, redeemed_at, used_at, order_id "
        "FROM coupons WHERE member_id = ? ORDER BY coupon_id", (member_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_unused_coupons(member_id):
    return [c for c in get_coupons(member_id)
            if c["status"] == "unused" and c["reward_code"] in REWARD_BY_CODE]


def get_point_history(member_id, limit=8):
    """ประวัติแต้มล่าสุด (ใหม่ -> เก่า)"""
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT points, type, order_id, created_at FROM point_history "
        "WHERE member_id = ? ORDER BY history_id DESC LIMIT ?", (member_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

if __name__ == "__main__":
    print("ไฟล์นี้เป็นส่วนหนึ่งของโปรแกรม Meme Beans  ให้เปิดโปรแกรมด้วยไฟล์ project.py")
