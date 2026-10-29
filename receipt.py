"""
receipt.py  -  ไฟล์ใบเสร็จ (ไฟล์ 3 จาก 4) ของ Meme Beans Coffee

หน้าที่: รูปแบบตัวเลขเงิน, สร้างใบเสร็จ PDF (ส่งทางอีเมลเป็นไฟล์แนบ ลูกค้ากดเปิด/ดาวน์โหลดได้),
         ส่งใบเสร็จและรหัสยืนยันทางอีเมล  (ฟอนต์ไทยสำหรับ PDF อยู่ในโฟลเดอร์ fonts/)
ประกอบด้วย: ส่วนที่ 5
เชื่อมกับไฟล์อื่น: ดึงข้อมูลออเดอร์จาก database.py
                  project.py (หน้าชำระเงิน) และ admin.py เรียกใช้ฟังก์ชันในไฟล์นี้
เปิดโปรแกรมด้วยไฟล์ project.py
"""

from datetime import datetime
import json
import os
import smtplib
import ssl
import struct
import zlib
import xml.etree.ElementTree as ET
from email.message import EmailMessage
from email.utils import formataddr

# จากไฟล์ฐานข้อมูล: ข้อมูลออเดอร์สำหรับทำใบเสร็จ + ค่าตั้งต้นของร้าน
from database import (
    BASE_DIR, EMAIL_CONFIG_PATH, RESET_CODE_MINUTES, SHOP_NAME, VAT_LABEL, get_order_receipt,
    order_amounts, round_money, set_receipt_sent, thai_now,
)


# =====================================================================
# ส่วนที่ 5: ใบเสร็จและการส่งอีเมล
#   ประกอบด้วย: รูปแบบตัวเลขเงิน (fmt_price, money_rows), load_email_config,
#              order_code, fmt_datetime, ตัวช่วยสร้างหน้าอีเมล (css, html_tag, email_layout, email_html),
#              build_receipt (ใบเสร็จในเนื้ออีเมล ใช้เมื่อทำ PDF ไม่ได้), ใบเสร็จ PDF (PdfFont, thai_shape,
#              write_pdf, receipt_page เลย์เอาต์ใบเสร็จ (ใช้ทั้งทำ PDF และแสดงบนจอ), build_receipt_pdf),
#              build_receipt_notice (ข้อความสั้นคู่กับ PDF),
#              send_receipt_email (ส่งใบเสร็จเป็นไฟล์ PDF แนบ),
#              send_reset_code_email (รหัสยืนยันลืมรหัสผ่าน), send_email, explain_email_error
#   แก้ที่นี่เมื่อ: แก้หน้าตา/ข้อความใบเสร็จ หรือวิธีส่งอีเมล (ตั้งค่าบัญชีอีเมลที่ไฟล์ email_config.json)
# บรรทัด 30 - 744
# =====================================================================
class EmailConfigError(Exception):
    """ตั้งค่าอีเมลของร้านยังไม่ครบ หรือไม่พบไฟล์ตั้งค่า"""


def load_email_config():
    """อ่าน email_config.json (ดูตัวอย่างที่ email_config.example.json) และตรวจความครบถ้วน"""
    try:
        with open(EMAIL_CONFIG_PATH, encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        raise EmailConfigError(
            "ยังไม่ได้ตั้งค่าอีเมลของร้าน (ไม่พบไฟล์ email_config.json)") from None
    except json.JSONDecodeError:
        raise EmailConfigError("ไฟล์ email_config.json เขียนผิดรูปแบบ") from None

    cfg.setdefault("smtp_port", 587)
    cfg.setdefault("security", "starttls")        # starttls / ssl / none (none ใช้ทดสอบในเครื่อง)
    cfg["from_address"] = cfg.get("from_address") or cfg.get("username", "")
    if not cfg.get("smtp_host") or not cfg["from_address"]:
        raise EmailConfigError("email_config.json ต้องมี smtp_host และ username")
    if cfg["security"] != "none":
        if not cfg.get("username") or not cfg.get("password"):
            raise EmailConfigError("email_config.json ต้องมี username และ password")
        if "ใส่" in cfg["username"] or "ใส่" in cfg["password"]:
            raise EmailConfigError("ยังไม่ได้ใส่อีเมลและรหัสผ่านของร้านใน email_config.json")
    return cfg


def order_code(order_id):
    return f"MB{order_id:05d}"


def fmt_datetime(s):
    try:
        return datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return s or "-"


# ---------- รูปแบบตัวเลขเงิน (ใช้ทั้งใบเสร็จ หน้าชำระเงิน และหน้าแอดมิน) ----------
def fmt_price(v):
    """ตัวเลขเงินสำหรับแสดงผล: 65 -> 65, 1250 -> 1,250, 69.55 -> 69.55"""
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}"


def money_rows(a, disc_label="ส่วนลด"):
    """แถวแจกแจงยอดเงินก่อนบรรทัด "ยอดรวม" [(ชื่อ, จำนวนเงิน)] ใช้กับใบเสร็จ/หน้าชำระเงิน/หน้าแอดมิน
    a = ผลจาก order_amounts()   ไม่มีส่วนลดและไม่มีภาษี -> ไม่มีแถว (แสดงแค่ยอดรวม)"""
    rows = []
    if a["discount"] or a["vat"]:
        rows.append(("ราคาสินค้า", f"฿{fmt_price(a['subtotal'])}"))
    if a["discount"]:
        rows.append((disc_label, f"-฿{fmt_price(a['discount'])}"))
    if a["vat"]:
        if a["discount"] or a["included"]:
            rows.append(("ยอดก่อน VAT", f"฿{fmt_price(float(round_money(a['paid'] - a['vat'])))}"))
        rows.append((VAT_LABEL, f"฿{fmt_price(a['vat'])}"))
    return rows


# ---------- ตัวช่วยสร้างหน้าอีเมล (โปรแกรมอีเมลแสดงสี/ตารางได้จากเอกสาร HTML เท่านั้น
#            ส่วนนี้จึงสร้างเอกสารนั้นด้วยฟังก์ชัน Python ผ่าน ElementTree แทนการพิมพ์แท็กเอง) ----------
def css(**props):
    """รวมการตกแต่งเป็นค่า style: css(font_size="13px", color="#7A6B58") -> "font-size:13px;color:#7A6B58"
    (ขีดล่างในชื่อจะกลายเป็นขีดกลาง)"""
    return ";".join(f"{name.replace('_', '-')}:{value}" for name, value in props.items())


def html_tag(parent, tag, text=None, style=None, tail=None, **attrs):
    """เพิ่มแท็กใต้ parent (parent=None = สร้างแท็กบนสุด) คืนแท็กที่สร้าง
    text = ข้อความข้างใน, tail = ข้อความที่ต่อท้ายหลังปิดแท็ก, style = ค่าจาก css()
    ข้อความถูกแปลงอักขระพิเศษ (เช่น < >) ให้อัตโนมัติ"""
    attrs = {name: str(value) for name, value in attrs.items()}
    if style:
        attrs["style"] = style
    node = ET.Element(tag, attrs) if parent is None else ET.SubElement(parent, tag, attrs)
    node.text, node.tail = text, tail
    return node


def email_layout():
    """โครงอีเมลของร้าน: พื้นครีม การ์ดกว้าง 480 หัวการ์ดสีดำมีชื่อร้าน
    คืนค่า (หน้าอีเมลทั้งหน้า, ช่องเนื้อหาในการ์ดสำหรับใส่ข้อความต่อ)"""
    page = html_tag(None, "html")
    body = html_tag(page, "body", style=css(margin=0, background="#EFE8DC",
                                            font_family="Tahoma,Arial,sans-serif", color="#1A1A1A"))
    outer = html_tag(body, "table", width="100%", cellpadding=0, cellspacing=0)
    center = html_tag(html_tag(outer, "tr"), "td", align="center", style=css(padding="24px 12px"))
    card = html_tag(center, "table", width=480, cellpadding=0, cellspacing=0,
                    style=css(background="#FBF8F2", border_radius="12px", overflow="hidden"))
    head = html_tag(html_tag(card, "tr"), "td", style=css(background="#1A1A1A", padding="22px 28px"))
    html_tag(head, "div", SHOP_NAME, style=css(font_size="24px", font_weight="bold", color="#EFE8DC"))
    html_tag(head, "div", "Coffee + Meme = Happiness", style=css(color="#B89A7A", font_size="13px"))
    content = html_tag(html_tag(card, "tr"), "td", style=css(padding="24px 28px"))
    return page, content


def email_html(page):
    """แปลงหน้าอีเมลที่สร้างไว้เป็นข้อความสำหรับแนบไปกับอีเมล"""
    return ET.tostring(page, encoding="unicode", method="html")


def build_receipt(order_id, extra=None):
    """สร้างใบเสร็จในเนื้ออีเมล คืนค่า (หัวเรื่อง, ข้อความธรรมดา, หน้าอีเมลแบบมีสี)
    ปกติส่งใบเสร็จเป็นไฟล์ PDF แทน  ใช้อันนี้เมื่อทำ PDF ไม่ได้ (เช่น ไม่มีโฟลเดอร์ fonts)
    extra = {"received": เงินที่รับ, "change": เงินทอน} (ใช้กับเงินสด ไม่บังคับ)"""
    r = get_order_receipt(order_id)
    if r is None:
        raise ValueError("ไม่พบออเดอร์นี้")
    extra = extra or {}
    code = order_code(order_id)
    when = fmt_datetime(r.get("paid_at") or r["order_date"])
    amounts = order_amounts(r)
    payable = amounts["paid"]                       # ยอดที่ลูกค้าจ่ายจริง (หลังลด รวมภาษีแล้ว)
    method = r.get("payment_method") or "-"
    customer = r.get("member_name") or "ลูกค้าทั่วไป"
    money = lambda v: f"฿{fmt_price(v)}"
    disc_label = f"ส่วนลด {r['coupon']['percent']}%" if r.get("coupon") else "ส่วนลด"
    breakdown = money_rows(amounts, disc_label)     # ราคาสินค้า / ส่วนลด / ยอดก่อนภาษี / ภาษี 7%
    vat_note = f"(ราคารวม {VAT_LABEL} แล้ว)" if amounts["included"] else ""

    # ---- ข้อความธรรมดา ----
    t = [f"{SHOP_NAME.upper()}", "ใบเสร็จรับเงิน", "",
         f"เลขที่ออเดอร์: {code}", f"วันที่: {when}", f"ลูกค้า: {customer}",
         "-" * 34]
    for it in r["items"]:
        t.append(f"{it['quantity']} x {it['name']}   {money(it['quantity'] * it['unit_price'])}")
        if it["options"]:
            t.append(f"    {it['options']}")
    t.append("-" * 34)
    for label, value in breakdown:
        t.append(f"{label}: {value}")
    t.append(f"ยอดรวม: {money(payable)}" + (f" {vat_note}" if vat_note else ""))
    t.append(f"ชำระโดย: {method}")
    if "received" in extra:
        t.append(f"รับเงิน: {money(extra['received'])}   เงินทอน: {money(extra['change'])}")
    if r["points_earned"]:
        t.append(f"แต้มที่ได้รับ: +{r['points_earned']} แต้ม (แต้มสะสม {r['member_points']} แต้ม)")
    t += ["", "ขอบคุณที่ใช้บริการ", "Coffee + Meme = Happiness"]
    text = "\n".join(t)

    # ---- หน้าอีเมล (สีและตารางเหมือนใบเสร็จจริง) ----
    muted, line = "#7A6B58", "1px solid #E0D5C1"
    page, box = email_layout()
    html_tag(box, "h2", "ใบเสร็จรับเงิน", style=css(margin="0 0 4px 0"))
    info = html_tag(box, "div", "เลขที่ออเดอร์ ", style=css(color=muted, font_size="13px"))
    html_tag(info, "b", code, tail=f" · {when}")
    html_tag(info, "br", tail=f"ลูกค้า: {customer}")

    items = html_tag(box, "table", width="100%", cellpadding=0, cellspacing=0,
                     style=css(margin_top="14px", font_size="14px"))
    for it in r["items"]:
        tr = html_tag(items, "tr")
        cell = html_tag(tr, "td", style=css(padding="10px 0", border_bottom=line))
        html_tag(cell, "b", f"{it['quantity']} × {it['name']}")
        if it["options"]:
            html_tag(cell, "div", it["options"], style=css(font_size="12px", color=muted))
        html_tag(tr, "td", money(it["quantity"] * it["unit_price"]),
                 style=css(padding="10px 0", border_bottom=line, text_align="right", white_space="nowrap"))

    summary = html_tag(box, "table", width="100%", cellpadding=4, cellspacing=0,
                       style=css(margin_top="10px", font_size="14px"))

    def pair(label, value, left=None, right=css(text_align="right")):
        """แถวสรุป 2 ช่อง: ชื่อชิดซ้าย / จำนวนเงินชิดขวา"""
        tr = html_tag(summary, "tr")
        html_tag(tr, "td", label, style=left)
        html_tag(tr, "td", value, style=right)

    for label, value in breakdown:                  # ราคาสินค้า / ส่วนลด / ยอดก่อนภาษี / ภาษี 7%
        pair(label, value)
    pair("ยอดรวม", money(payable), css(font_size="18px", font_weight="bold", padding_top="8px"),
         css(font_size="18px", font_weight="bold", text_align="right", color="#4F7A3B", padding_top="8px"))
    if vat_note:
        html_tag(html_tag(summary, "tr"), "td", vat_note, colspan=2,
                 style=css(text_align="right", font_size="12px", color=muted))
    divider = html_tag(html_tag(summary, "tr"), "td", colspan=2, style=css(padding=0))
    html_tag(divider, "div", style=css(border_top=line, margin="6px 0"))
    pair("ชำระโดย", method)
    if "received" in extra:
        pair("รับเงิน", money(extra["received"]))
        pair("เงินทอน", money(extra["change"]))

    if r["points_earned"]:
        badge = html_tag(box, "p", "ได้รับ ", style=css(background="#4F7A3B", color="#EFE8DC",
                                                         padding="10px 14px", border_radius="8px"))
        html_tag(badge, "b", f"+{r['points_earned']} แต้ม",
                 tail=f" (แต้มสะสมตอนนี้ {r['member_points']} แต้ม)")
    html_tag(box, "p", "ขอบคุณที่ใช้บริการ ☕", style=css(color=muted, font_size="13px", margin_bottom=0))

    return f"ใบเสร็จรับเงิน {SHOP_NAME} #{code}", text, email_html(page)


# ---------- ใบเสร็จ PDF (ส่งทางอีเมลเป็นไฟล์แนบ ลูกค้ากดเปิดดู/ดาวน์โหลดเก็บไว้ได้) ----------
# เขียนไฟล์ PDF ด้วย Python ล้วน (ไม่ต้องติดตั้งอะไรเพิ่ม) ฝังฟอนต์ไทย Loma ไว้ในไฟล์
# จึงเปิดได้ทุกเครื่อง/มือถือ แม้ไม่มีฟอนต์ไทย
# ฟอนต์ Loma: TLWG / NECTEC สัญญาอนุญาต GPL-2+ with font exception (ฝังในเอกสารได้) อยู่ที่โฟลเดอร์ fonts/
PDF_FONT_DIR = os.path.join(BASE_DIR, "fonts")
PDF_FONTS = {"regular": "Loma.ttf", "bold": "Loma-Bold.ttf"}
_pdf_font_cache = {}
# ข้อผิดพลาดตอนทำใบเสร็จ PDF (ไม่มีไฟล์ฟอนต์ / ไฟล์ฟอนต์เสีย / ไม่พบออเดอร์)
RECEIPT_PDF_ERRORS = (OSError, ValueError, KeyError, struct.error)


class PdfFont:
    """อ่านไฟล์ฟอนต์ TrueType (.ttf) เท่าที่ต้องใช้ทำ PDF:
    ตัวอักษร -> หมายเลข glyph (cmap), ความกว้างแต่ละ glyph, ความสูงฟอนต์ และชื่อฟอนต์"""

    def __init__(self, path):
        with open(path, "rb") as f:
            self.data = data = f.read()
        tables = {}
        for i in range(struct.unpack(">H", data[4:6])[0]):
            tag, _, offset, length = struct.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
            tables[tag.decode("latin-1")] = data[offset:offset + length]
        head, hhea, os2 = tables["head"], tables["hhea"], tables["OS/2"]
        self.upm = struct.unpack(">H", head[18:20])[0]                 # หน่วยต่อ 1 em
        self.bbox = struct.unpack(">hhhh", head[36:44])
        self.ascent, self.descent = struct.unpack(">hh", hhea[4:8])
        self.cap_height = struct.unpack(">h", os2[88:90])[0] if len(os2) >= 90 else self.ascent
        n_glyphs = struct.unpack(">H", tables["maxp"][4:6])[0]
        n_metrics = struct.unpack(">H", hhea[34:36])[0]
        hmtx = tables["hmtx"]
        self.widths = [struct.unpack(">H", hmtx[4 * i:4 * i + 2])[0] for i in range(n_metrics)]
        self.widths += [self.widths[-1]] * (n_glyphs - n_metrics)
        self.cmap = self._read_cmap(tables["cmap"])
        self.name = os.path.splitext(os.path.basename(path))[0].replace(" ", "")

    @staticmethod
    def _read_cmap(cmap):
        """อ่านตาราง cmap แบบ format 4 (Windows Unicode BMP) คืนค่า {รหัสตัวอักษร: glyph}"""
        u16 = lambda pos: struct.unpack(">H", cmap[pos:pos + 2])[0]
        for i in range(u16(2)):
            platform, encoding, offset = struct.unpack(">HHI", cmap[4 + 8 * i:12 + 8 * i])
            if (platform, encoding) == (3, 1) and u16(offset) == 4:
                break
        else:
            raise ValueError("ฟอนต์นี้ไม่มีตาราง cmap แบบ Unicode")
        seg2 = u16(offset + 6)
        ends, starts = offset + 14, offset + 16 + seg2
        deltas, ranges = starts + seg2, starts + 2 * seg2
        out = {}
        for s in range(0, seg2, 2):
            start, end = u16(starts + s), u16(ends + s)
            delta, rng = u16(deltas + s), u16(ranges + s)
            for code in range(start, min(end, 0xFFFE) + 1):
                if rng == 0:
                    gid = (code + delta) & 0xFFFF
                else:
                    gid = u16(ranges + s + rng + 2 * (code - start))
                    gid = (gid + delta) & 0xFFFF if gid else 0
                if gid:
                    out[code] = gid
        return out

    def glyphs(self, text):
        """ข้อความ -> [(glyph, ตัวอักษรต้นฉบับ)] (จัดตำแหน่งสระ/วรรณยุกต์ไทยแล้ว ตัวที่ไม่มีในฟอนต์ใช้ ?)"""
        out = []
        for shaped, original in thai_shape(text):
            gid = self.cmap.get(ord(shaped)) or self.cmap.get(ord(original)) or self.cmap.get(ord("?"), 0)
            out.append((gid, original))
        return out

    def width(self, text, size):
        """ความกว้างของข้อความ (หน่วย point)"""
        return sum(self.widths[g] for g, _ in self.glyphs(text)) * size / self.upm


def pdf_font(style="regular"):
    """ฟอนต์สำหรับ PDF (อ่านไฟล์ครั้งเดียวแล้วจำไว้)"""
    if style not in _pdf_font_cache:
        _pdf_font_cache[style] = PdfFont(os.path.join(PDF_FONT_DIR, PDF_FONTS[style]))
    return _pdf_font_cache[style]


# ---- จัดตำแหน่งสระบน/ล่างและวรรณยุกต์ไทย ----
# โปรแกรมอ่าน PDF ไม่จัดตำแหน่งตัวอักษรให้ จึงต้องเลือก glyph ที่ "ขยับไว้แล้ว" เอง
# (ฟอนต์ไทยมาตรฐานมี glyph พวกนี้ที่รหัส U+F700-F71A เช่น วรรณยุกต์ตัวต่ำเมื่อไม่มีสระบน)
_TH_UPPER = "ัิีึื็ํ"        # ั ิ ี ึ ื ็ ํ
_TH_TONES = "่้๊๋์"                    # ่ ้ ๊ ๋ ์
_TH_LOWER = "ฺุู"                                # ุ ู ฺ
_TH_TALL = "ปฝฟฬ"                           # ป ฝ ฟ ฬ (หางสูง)
_TH_DESC = "ฎฏ"                                       # ฎ ฏ (หางลงล่าง)
_TH_CUT = {"ญ": "", "ฐ": ""}              # ญ ฐ แบบตัดเชิง (เมื่อมีสระล่าง)
_TH_UPPER_LEFT = dict(zip(_TH_UPPER, ""))
_TH_TONE_LOW = dict(zip(_TH_TONES, ""))
_TH_TONE_LOW_LEFT = dict(zip(_TH_TONES, ""))
_TH_TONE_LEFT = dict(zip(_TH_TONES, ""))
_TH_LOWER_LOW = dict(zip(_TH_LOWER, ""))


def thai_shape(text):
    """คืนค่า [(ตัวที่จะวาด, ตัวอักษรต้นฉบับ)]
    - สระอำ แยกเป็น นิคหิต + สระอา (วรรณยุกต์ย้ายไปอยู่บนนิคหิต เช่น น้ำ)
    - วรรณยุกต์ไม่มีสระบน -> ตัวต่ำ / มีสระบน -> ตัวสูง
    - ตัวหางสูง (ป ฝ ฟ ฬ) -> สระบนและวรรณยุกต์ขยับซ้าย
    - ฎ ฏ + สระล่าง -> สระล่างต่ำลง / ญ ฐ + สระล่าง -> ใช้ตัวตัดเชิง"""
    chars = []
    for ch in text:
        if ch == "ำ":                                      # ำ
            if chars and chars[-1] in _TH_TONES:
                tone = chars.pop()
                chars += ["ํ", tone, "า"]
            else:
                chars += ["ํ", "า"]
        else:
            chars.append(ch)
    out, base, base_at, upper = [], "", -1, False
    for ch in chars:
        tall = base in _TH_TALL
        if ch in _TH_UPPER:
            upper = True
            out.append((_TH_UPPER_LEFT[ch] if tall else ch, ch))
        elif ch in _TH_TONES:
            if upper:
                out.append((_TH_TONE_LEFT[ch] if tall else ch, ch))
            else:
                out.append(((_TH_TONE_LOW_LEFT if tall else _TH_TONE_LOW)[ch], ch))
        elif ch in _TH_LOWER:
            if base in _TH_DESC:
                out.append((_TH_LOWER_LOW[ch], ch))
            else:
                if base in _TH_CUT and base_at >= 0:
                    out[base_at] = (_TH_CUT[base], base)
                out.append((ch, ch))
        else:
            base, base_at, upper = ch, len(out), False
            out.append((ch, ch))
    return out


def _pdf_wrap(text, font, size, width):
    """ตัดบรรทัดตามความกว้าง (ตัดที่ช่องว่างก่อน คำยาวมากค่อยตัดทีละตัวอักษรโดยไม่แยกสระ/วรรณยุกต์)"""
    lines = []
    for paragraph in str(text).split("\n"):
        line = ""
        for word in paragraph.split(" "):
            trial = f"{line} {word}" if line else word
            if font.width(trial, size) <= width:
                line = trial
                continue
            if line:
                lines.append(line)
            line = ""
            for ch in word:                                     # คำเดียวยาวเกินบรรทัด
                if line and ch not in _TH_UPPER + _TH_TONES + _TH_LOWER + "ำ" and \
                        font.width(line + ch, size) > width:
                    lines.append(line)
                    line = ""
                line += ch
        lines.append(line)
    return lines


class _PdfPage:
    """คำสั่งวาดในหน้า PDF (พิกัดวัดจากมุมซ้ายบนลงมา หน่วย point) แปลงเป็นพิกัด PDF ตอนสร้างไฟล์"""

    def __init__(self, width):
        self.width, self.ops, self.used = width, [], {}

    @staticmethod
    def _rgb(color):
        return " ".join(f"{int(color[i:i + 2], 16) / 255:.3f}" for i in (1, 3, 5))

    def rect(self, x, y, w, h, color, radius=0):
        r = min(radius, w / 2, h / 2)
        self.ops.append(("rect", x, y, w, h, color, r))

    def line(self, x1, y1, x2, y2, color, width=0.6):
        self.ops.append(("line", x1, y1, x2, y2, color, width))

    def text(self, x, y, text, size, color="#1A1A1A", style="regular", align="left"):
        """วาดข้อความ (y = เส้นฐานของตัวอักษร) คืนค่าความกว้าง
        เก็บข้อความเดิม จุดอ้างอิง และการจัดชิดไว้ด้วย ให้หน้าจอวาดใบเสร็จแบบเดียวกันได้ (draw_receipt_page)"""
        font = pdf_font(style)
        glyphs = font.glyphs(text)
        w = sum(font.widths[g] for g, _ in glyphs) * size / font.upm
        anchor_x = x
        if align == "right":
            x -= w
        elif align == "center":
            x -= w / 2
        used = self.used.setdefault(style, {})
        for g, ch in glyphs:
            used.setdefault(g, ch)
        self.ops.append(("text", x, y, glyphs, size, color, style, text, anchor_x, align, w))
        return w

    def content(self, height):
        """คำสั่งวาดทั้งหมดเป็นข้อความ PDF (แกน y ของ PDF นับจากล่างขึ้นบน)"""
        out = []
        for op in self.ops:
            if op[0] == "rect":
                _, x, y, w, h, color, r = op
                y0 = height - y - h
                out.append(f"{self._rgb(color)} rg")
                if r <= 0:
                    out.append(f"{x:.2f} {y0:.2f} {w:.2f} {h:.2f} re f")
                else:
                    k = r * 0.5523                               # เส้นโค้งมุมมน (Bezier)
                    x1, y1 = x + w, y0 + h
                    out.append(
                        f"{x + r:.2f} {y0:.2f} m {x1 - r:.2f} {y0:.2f} l "
                        f"{x1 - r + k:.2f} {y0:.2f} {x1:.2f} {y0 + r - k:.2f} {x1:.2f} {y0 + r:.2f} c "
                        f"{x1:.2f} {y1 - r:.2f} l "
                        f"{x1:.2f} {y1 - r + k:.2f} {x1 - r + k:.2f} {y1:.2f} {x1 - r:.2f} {y1:.2f} c "
                        f"{x + r:.2f} {y1:.2f} l "
                        f"{x + r - k:.2f} {y1:.2f} {x:.2f} {y1 - r + k:.2f} {x:.2f} {y1 - r:.2f} c "
                        f"{x:.2f} {y0 + r:.2f} l "
                        f"{x:.2f} {y0 + r - k:.2f} {x + r - k:.2f} {y0:.2f} {x + r:.2f} {y0:.2f} c f")
            elif op[0] == "line":
                _, x1, y1, x2, y2, color, width = op
                out.append(f"{self._rgb(color)} RG {width:.2f} w {x1:.2f} {height - y1:.2f} m "
                           f"{x2:.2f} {height - y2:.2f} l S")
            else:
                _, x, y, glyphs, size, color, style = op[:7]
                hexgids = "".join(f"{g:04X}" for g, _ in glyphs)
                out.append(f"BT /F{'B' if style == 'bold' else 'R'} {size:.2f} Tf {self._rgb(color)} rg "
                           f"{x:.2f} {height - y:.2f} Td <{hexgids}> Tj ET")
        return "\n".join(out).encode("ascii")


def _pdf_string(text):
    """ข้อความในข้อมูลเอกสาร PDF (รองรับภาษาไทย: UTF-16BE ฐานสิบหก)"""
    return "<FEFF" + text.encode("utf-16-be").hex().upper() + ">"


def write_pdf(page, height, title):
    """ประกอบไฟล์ PDF 1 หน้า (ฝังฟอนต์ที่ใช้) คืนค่า bytes"""
    objs = []

    def add(body):
        objs.append(body if isinstance(body, bytes) else body.encode("latin-1"))
        return len(objs)

    def stream(data, extra=""):
        packed = zlib.compress(data, 9)
        return add(f"<< /Length {len(packed)} /Filter /FlateDecode {extra}>>\nstream\n".encode("latin-1")
                   + packed + b"\nendstream")

    fonts = {}
    for style, used in page.used.items():
        font = pdf_font(style)
        scale = 1000 / font.upm
        file_ref = stream(font.data, f"/Length1 {len(font.data)} ")
        gids = sorted(used)
        widths = " ".join(f"{g} [{round(font.widths[g] * scale)}]" for g in gids)
        bbox = " ".join(str(round(v * scale)) for v in font.bbox)
        desc = add(f"<< /Type /FontDescriptor /FontName /{font.name} /Flags 4 /FontBBox [{bbox}] "
                   f"/ItalicAngle 0 /Ascent {round(font.ascent * scale)} /Descent {round(font.descent * scale)} "
                   f"/CapHeight {round(font.cap_height * scale)} /StemV 80 /FontFile2 {file_ref} 0 R >>")
        cid = add(f"<< /Type /Font /Subtype /CIDFontType2 /BaseFont /{font.name} "
                  "/CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> "
                  f"/FontDescriptor {desc} 0 R /DW 1000 /W [{widths}] /CIDToGIDMap /Identity >>")
        # ToUnicode: ให้คัดลอก/ค้นหาข้อความในใบเสร็จได้
        pairs = [f"<{g:04X}> <{ord(used[g]):04X}>" for g in gids if ord(used[g]) <= 0xFFFF]
        blocks = "".join(f"{len(pairs[i:i + 100])} beginbfchar\n" + "\n".join(pairs[i:i + 100]) + "\nendbfchar\n"
                         for i in range(0, len(pairs), 100))
        cmap = ("/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
                "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
                "/CMapName /Adobe-Identity-UCS def\n/CMapType 2 def\n"
                "1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n" + blocks +
                "endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend")
        to_unicode = stream(cmap.encode("ascii"))
        fonts["F" + ("B" if style == "bold" else "R")] = add(
            f"<< /Type /Font /Subtype /Type0 /BaseFont /{font.name} /Encoding /Identity-H "
            f"/DescendantFonts [{cid} 0 R] /ToUnicode {to_unicode} 0 R >>")

    contents = stream(page.content(height))
    font_res = " ".join(f"/{k} {v} 0 R" for k, v in fonts.items())
    pages_id = len(objs) + 2                                   # หมายเลขของ /Pages (สร้างถัดจาก /Page)
    page_id = add(f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {page.width:.2f} {height:.2f}] "
                  f"/Resources << /Font << {font_res} >> >> /Contents {contents} 0 R >>")
    add(f"<< /Type /Pages /Kids [{page_id} 0 R] /Count 1 >>")
    catalog = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")
    info = add(f"<< /Title {_pdf_string(title)} /Producer {_pdf_string(SHOP_NAME + ' (Python)')} "
               f"/CreationDate (D:{thai_now().strftime('%Y%m%d%H%M%S')}) >>")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for n, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{n} 0 obj\n".encode("ascii") + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode("ascii")
    out += "".join(f"{o:010d} 00000 n \n" for o in offsets).encode("ascii")
    out += (f"trailer\n<< /Size {len(objs) + 1} /Root {catalog} 0 R /Info {info} 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode("ascii")
    return bytes(out)


def receipt_filename(order_id, ext=".pdf"):
    """ชื่อไฟล์ใบเสร็จ เช่น MemeBeans_receipt_MB00099.pdf"""
    return f"MemeBeans_receipt_{order_code(order_id)}{ext}"


def build_receipt_pdf(order_id, extra=None):
    """ใบเสร็จเป็นไฟล์ PDF (หน้าตาเดียวกับใบเสร็จในอีเมล) คืนค่า (ชื่อไฟล์, bytes)
    ไม่พบไฟล์ฟอนต์ในโฟลเดอร์ fonts/ จะ raise FileNotFoundError"""
    page, height = receipt_page(order_id, extra)
    return receipt_filename(order_id), write_pdf(page, height, f"ใบเสร็จรับเงิน {SHOP_NAME} #{order_code(order_id)}")


def receipt_page(order_id, extra=None):
    """วางเลย์เอาต์ใบเสร็จ 1 หน้า คืนค่า (หน้า _PdfPage, ความสูงหน้า หน่วย point)
    ใช้ทั้งทำไฟล์ PDF (build_receipt_pdf) และวาดบนจอ (หน้าดูใบเสร็จย้อนหลัง) หน้าตาจึงตรงกัน
    ไม่พบไฟล์ฟอนต์ในโฟลเดอร์ fonts/ จะ raise FileNotFoundError"""
    r = get_order_receipt(order_id)
    if r is None:
        raise ValueError("ไม่พบออเดอร์นี้")
    extra = extra or {}
    code = order_code(order_id)
    amounts = order_amounts(r)
    money = lambda v: f"฿{fmt_price(v)}"
    disc_label = f"ส่วนลด {r['coupon']['percent']}%" if r.get("coupon") else "ส่วนลด"
    muted, line_color, green = "#7A6B58", "#E0D5C1", "#4F7A3B"

    W, M = 320, 24                       # กว้างหน้า (ประมาณ 11 ซม.) และระยะขอบซ้ายขวา
    right = W - M
    p = _PdfPage(W)
    regular, bold = pdf_font("regular"), pdf_font("bold")

    # หัวกระดาษสีดำ + ชื่อร้าน
    p.rect(0, 0, W, 66, "#1A1A1A")
    p.text(M, 34, SHOP_NAME, 19, "#EFE8DC", "bold")
    p.text(M, 51, "Coffee + Meme = Happiness", 9, "#B89A7A")
    y = 66 + 34
    p.text(M, y, "ใบเสร็จรับเงิน", 17, style="bold")
    y += 18
    x = M + p.text(M, y, "เลขที่ออเดอร์ ", 9, muted)
    x += p.text(x, y, code, 9, muted, "bold")
    p.text(x, y, f" · {fmt_datetime(r.get('paid_at') or r['order_date'])}", 9, muted)
    for text in _pdf_wrap(f"ลูกค้า: {r.get('member_name') or 'ลูกค้าทั่วไป'}", regular, 9, right - M):
        y += 13
        p.text(M, y, text, 9, muted)
    y += 10

    # รายการสินค้า
    for it in r["items"]:
        price = money(it["quantity"] * it["unit_price"])
        name_w = right - M - bold.width(price, 10.5) - 12
        for n, text in enumerate(_pdf_wrap(f"{it['quantity']} × {it['name']}", bold, 10.5, name_w)):
            y += 15
            p.text(M, y, text, 10.5, style="bold")
            if n == 0:
                p.text(right, y, price, 10.5, align="right")
        for text in _pdf_wrap(it["options"] or "", regular, 8.5, name_w) if it["options"] else []:
            y += 11.5
            p.text(M, y, text, 8.5, muted)
        y += 9
        p.line(M, y, right, y, line_color)
        y += 2

    def pair(label, value, size=10, style="regular", color="#1A1A1A", gap=17):
        nonlocal y
        y += gap
        p.text(M + 2, y, label, size, "#1A1A1A", style)
        p.text(right - 2, y, value, size, color, style, align="right")

    y += 4
    for label, value in money_rows(amounts, disc_label):
        pair(label, value)
    pair("ยอดรวม", money(amounts["paid"]), 14, "bold", green, gap=24)
    if amounts["included"]:
        y += 13
        p.text(right - 2, y, f"(ราคารวม {VAT_LABEL} แล้ว)", 8.5, muted, align="right")
    y += 10
    p.line(M, y, right, y, line_color)
    pair("ชำระโดย", r.get("payment_method") or "-")
    if "received" in extra:
        pair("รับเงิน", money(extra["received"]))
        pair("เงินทอน", money(extra["change"]))

    if r["points_earned"]:                                     # กล่องแต้มสีเขียว
        y += 14
        p.rect(M, y, right - M, 28, green, radius=6)
        x = M + 12
        x += p.text(x, y + 18.5, "ได้รับ ", 10, "#EFE8DC")
        x += p.text(x, y + 18.5, f"+{r['points_earned']} แต้ม", 10, "#EFE8DC", "bold")
        p.text(x, y + 18.5, f" (แต้มสะสมตอนนี้ {r['member_points']} แต้ม)", 10, "#EFE8DC")
        y += 28
    y += 26
    p.text(M, y, "ขอบคุณที่ใช้บริการ", 9.5, muted)
    y += 13
    p.text(M, y, "เอกสารนี้ออกโดยระบบร้าน " + SHOP_NAME, 7.5, "#A89A88")
    return p, y + 26


def build_receipt_notice(order_id, filename):
    """เนื้ออีเมลสั้น ๆ ที่ส่งคู่กับใบเสร็จ PDF (รายการทั้งหมดอยู่ในไฟล์ PDF ไม่ซ้ำในเนื้ออีเมล)
    คืนค่า (หัวเรื่อง, ข้อความธรรมดา, หน้าอีเมล)"""
    r = get_order_receipt(order_id)
    if r is None:
        raise ValueError("ไม่พบออเดอร์นี้")
    code = order_code(order_id)
    total = f"฿{fmt_price(order_amounts(r)['paid'])}"
    name = (r.get("member_name") or "").strip()
    for title in ("นางสาว", "นาย", "นาง", "น.ส.", "ด.ช.", "ด.ญ."):    # ตัดคำนำหน้า: "คุณนายสมชาย" -> "คุณสมชาย"
        rest = name[len(title):]
        if name.startswith(title) and rest and (rest[0] == " " or "ก" <= rest[0] <= "ฮ"):
            name = rest.strip()
            break
    hello = f"สวัสดีคุณ{name}" if name else "สวัสดี"
    how = "กดที่ไฟล์ใบเสร็จด้านล่างเพื่อเปิดดูแบบเต็มหน้า หรือกดดาวน์โหลดเพื่อบันทึกเป็นไฟล์ PDF เก็บไว้"
    text = "\n".join([hello, "",
                      f"ขอบคุณที่ใช้บริการ {SHOP_NAME}",
                      f"ใบเสร็จรับเงินเลขที่ {code} ยอดรวม {total} แนบมาเป็นไฟล์ PDF ({filename})",
                      how, "", SHOP_NAME, "Coffee + Meme = Happiness"])

    muted = "#7A6B58"
    page = html_tag(None, "html")
    body = html_tag(page, "body", style=css(font_family="Tahoma,Arial,sans-serif", color="#1A1A1A",
                                            font_size="14px", line_height="1.6"))
    html_tag(body, "p", hello)
    p = html_tag(body, "p", f"ขอบคุณที่ใช้บริการ {SHOP_NAME} ☕ ใบเสร็จรับเงินเลขที่ ")
    html_tag(p, "b", code, tail=" ยอดรวม ")
    html_tag(p, "b", total, tail=" แนบมาเป็นไฟล์ PDF")
    html_tag(body, "p", how, style=css(color=muted))
    sign = html_tag(body, "p", style=css(color=muted, font_size="13px", margin_top="20px"))
    html_tag(sign, "b", SHOP_NAME, tail=" · Coffee + Meme = Happiness")
    return f"ใบเสร็จรับเงิน {SHOP_NAME} #{code}", text, email_html(page)


def send_receipt_email(order_id, to_address, extra=None):
    """ส่งใบเสร็จไปที่อีเมลผู้รับเป็นไฟล์ PDF แนบ (เนื้ออีเมลเป็นข้อความสั้น ๆ ไม่มีใบเสร็จซ้ำ)
    ลูกค้ากดที่ไฟล์เพื่อเปิดดูหรือดาวน์โหลดเป็น PDF ได้  เกิดข้อผิดพลาดในการส่งจะ raise
    ถ้าทำ PDF ไม่ได้ (เช่น ไม่มีโฟลเดอร์ fonts) จะส่งใบเสร็จแบบหน้าอีเมลมีสีแทน
    สำเร็จแล้วบันทึก receipt_sent = 1"""
    load_email_config()                   # ตั้งค่าอีเมลไม่ครบจะแจ้งก่อนสร้างใบเสร็จ
    try:
        filename, pdf = build_receipt_pdf(order_id, extra)
    except RECEIPT_PDF_ERRORS as e:
        print("สร้างใบเสร็จ PDF ไม่ได้ (ส่งใบเสร็จในเนื้ออีเมลแทน):", e)
        subject, text, html_body = build_receipt(order_id, extra)
        send_email(to_address, subject, text, html_body)
    else:
        subject, text, html_body = build_receipt_notice(order_id, filename)
        send_email(to_address, subject, text, html_body, [(filename, pdf, "application/pdf")])
    set_receipt_sent(order_id, True)


def send_reset_code_email(to_address, name, code):
    """ส่งรหัสยืนยันสำหรับตั้งรหัสผ่านใหม่ไปที่อีเมลสมาชิก (เกิดข้อผิดพลาดจะ raise)"""
    subject = f"รหัสยืนยันสำหรับตั้งรหัสผ่านใหม่ - {SHOP_NAME}"
    text = (f"สวัสดีคุณ {name}\n\n"
            f"รหัสยืนยันสำหรับตั้งรหัสผ่านใหม่ของคุณคือ  {code}\n"
            f"รหัสนี้ใช้ได้ {RESET_CODE_MINUTES} นาที\n\n"
            "ถ้าคุณไม่ได้ขอเปลี่ยนรหัสผ่าน ไม่ต้องทำอะไร รหัสผ่านเดิมยังใช้ได้ตามปกติ\n"
            f"{SHOP_NAME}")
    page, box = email_layout()
    html_tag(box, "h2", "ตั้งรหัสผ่านใหม่", style=css(margin="0 0 8px 0"))
    html_tag(box, "p", f"สวัสดีคุณ {name} รหัสยืนยันของคุณคือ", style=css(margin="0 0 16px 0"))
    html_tag(box, "div", code, style=css(font_size="34px", font_weight="bold", letter_spacing="8px",
                                         background="#1A1A1A", color="#FFD43B", text_align="center",
                                         padding="14px 0", border_radius="10px"))
    html_tag(box, "p", f"รหัสนี้ใช้ได้ {RESET_CODE_MINUTES} นาที "
                       "ถ้าคุณไม่ได้ขอเปลี่ยนรหัสผ่าน ไม่ต้องทำอะไร รหัสผ่านเดิมยังใช้ได้ตามปกติ",
             style=css(color="#7A6B58", font_size="13px", margin="1em 0"))
    send_email(to_address, subject, text, email_html(page))


def send_email(to_address, subject, text, html_body=None, attachments=None):
    """ส่งอีเมล 1 ฉบับผ่าน SMTP ตาม email_config.json (ข้อความธรรมดา + HTML ถ้ามี + ไฟล์แนบ)
    attachments = [(ชื่อไฟล์, bytes, ชนิดไฟล์ เช่น "application/pdf")]
    เกิดข้อผิดพลาดจะ raise ให้ผู้เรียกจัดการ (ใช้ explain_email_error แปลเป็นข้อความไทย)"""
    cfg = load_email_config()
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((cfg.get("sender_name", SHOP_NAME), cfg["from_address"]))
    msg["To"] = to_address
    msg.set_content(text)
    if html_body:
        msg.add_alternative(html_body, subtype="html")
    for filename, data, mime in attachments or []:
        maintype, subtype = mime.split("/")
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    security = cfg["security"].lower()
    host, port = cfg["smtp_host"], int(cfg["smtp_port"])
    context = ssl.create_default_context()
    if security == "ssl":
        server = smtplib.SMTP_SSL(host, port, timeout=20, context=context)
    else:
        server = smtplib.SMTP(host, port, timeout=20)
    with server:
        if security == "starttls":
            server.starttls(context=context)
        if security != "none":
            server.login(cfg["username"], cfg["password"])
        server.send_message(msg)


def explain_email_error(e):
    """แปลงข้อผิดพลาดการส่งอีเมลเป็นข้อความภาษาไทยที่อ่านง่าย"""
    if isinstance(e, EmailConfigError):
        return str(e)
    if isinstance(e, smtplib.SMTPAuthenticationError):
        return "อีเมลหรือรหัสผ่านของร้านไม่ถูกต้อง (ถ้าใช้ Gmail ต้องใช้ 'รหัสผ่านแอป')"
    if isinstance(e, smtplib.SMTPRecipientsRefused):
        return "เซิร์ฟเวอร์ปฏิเสธอีเมลผู้รับ กรุณาตรวจสอบที่อยู่อีเมล"
    if isinstance(e, (smtplib.SMTPException, OSError)):
        return "เชื่อมต่อเซิร์ฟเวอร์อีเมลไม่ได้ ตรวจสอบอินเทอร์เน็ตหรือการตั้งค่า"
    return f"ส่งไม่สำเร็จ: {e}"

if __name__ == "__main__":
    print("ไฟล์นี้เป็นส่วนหนึ่งของโปรแกรม Meme Beans  ให้เปิดโปรแกรมด้วยไฟล์ project.py")
