"""
up.py  -  อัปเดตเลขบรรทัดในสารบัญและป้ายหัวข้อของโปรแกรม Meme Beans (4 ไฟล์)

วิธีใช้ (หลังแก้โค้ดแล้วเลขบรรทัดเลื่อน):
    python up.py

สคริปต์จะ
  1) หา "ป้ายหัวข้อ" (บรรทัด  # ส่วนที่ N: ชื่อส่วน) ในทั้ง 4 ไฟล์: project.py, database.py, receipt.py, admin.py
  2) คำนวณบรรทัดเริ่ม-จบของแต่ละส่วน แล้วเขียนลงบรรทัด "# บรรทัด a - b" ในป้ายหัวข้อ
  3) สร้างสารบัญที่หัวไฟล์ project.py ใหม่ (บอกว่าแต่ละส่วนอยู่ไฟล์ไหน บรรทัดเท่าไร)

เลขส่วนไม่ถูกเปลี่ยน (ส่วนที่ 1-22 กระจายอยู่หลายไฟล์)
เพิ่มส่วนใหม่: คัดลอกป้ายหัวข้อเดิมไปวางก่อนโค้ดส่วนนั้น ตั้งเลขส่วนใหม่ (เช่น 23) แล้วรันสคริปต์นี้
ไม่แตะโค้ดส่วนอื่น
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ["project.py", "database.py", "receipt.py", "admin.py"]
RUN_HINT = 'if __name__ == "__main__":'


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read().split("\n")


def save(name, lines):
    with open(os.path.join(BASE, name), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def banners(lines):
    """ดัชนีบรรทัดแรก (เส้น # =====) ของทุกป้ายหัวข้อ"""
    return [i for i in range(len(lines) - 1)
            if lines[i].startswith("# =====") and lines[i + 1].startswith("# ส่วนที่")]


def section_ranges(lines, is_main):
    """[(เลขส่วน, ชื่อส่วน, ดัชนีบรรทัดแรก, เลขบรรทัดสุดท้าย)]"""
    found = banners(lines)
    out = []
    for k, start in enumerate(found):
        stop = found[k + 1] if k + 1 < len(found) else len(lines)
        while stop > start + 1 and lines[stop - 1].strip() == "":
            stop -= 1
        # ไฟล์ย่อยจบด้วย 2 บรรทัดบอกให้เปิดโปรแกรมด้วย project.py -> ไม่นับรวมในส่วนสุดท้าย
        if not is_main and k + 1 == len(found) and lines[stop - 2].startswith(RUN_HINT):
            stop -= 2
            while lines[stop - 1].strip() == "":
                stop -= 1
        m = re.match(r"# ส่วนที่\s*(\d+):\s*(.*)", lines[start + 1])
        out.append((int(m.group(1)), m.group(2).strip(), start, stop))
    return out


def update():
    info = {}
    for name in FILES:
        lines = load(name)
        for n, title, start, stop in section_ranges(lines, name == "project.py"):
            info[n] = (name, title, start + 1, stop)
            for j in range(start, min(start + 10, len(lines))):
                if lines[j].startswith("# บรรทัด"):
                    lines[j] = f"# บรรทัด {start + 1} - {stop}"
                    break
        save(name, lines)

    lines = load("project.py")
    head = next(k for k in range(min(len(lines), 80)) if lines[k].startswith("สารบัญโค้ด"))
    a = b = head + 1
    while b < len(lines) and lines[b].startswith("  ส่วนที่"):
        b += 1
    lines[a:b] = [f"  ส่วนที่ {n:>2}  {title} ".ljust(50, ".") + f" {name:<12} บรรทัด {s} - {e}"
                  for n, (name, title, s, e) in sorted(info.items())]
    save("project.py", lines)
    return info


update()            # รอบแรก: สารบัญยาวขึ้น/สั้นลงอาจทำให้บรรทัดใน project.py เลื่อน
info = update()     # รอบสอง: เลขบรรทัดนิ่งแล้ว
print(f"อัปเดตแล้ว {len(info)} ส่วน ใน {len(FILES)} ไฟล์")
for n, (name, title, s, e) in sorted(info.items()):
    print(f"  ส่วนที่ {n:>2}: {name:<12} บรรทัด {s} - {e}  {title}")
