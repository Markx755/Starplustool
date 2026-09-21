#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# STAR Plus v4.3 — Multi-Account Roblox Auto-Rejoin + Live Dashboard (Termux)
#
# ใหม่ใน v4.3:
#   [โลโก้ STAR Plus] banner ตัวใหญ่เปลี่ยนเป็น "STAR Plus" (STAR + Plus) ทั้งหน้าเมนูและดาชบอร์ด
#                     พร้อมแอนิเมชันเปิดตัวทีละเส้น + shimmer + loading bar แสดง %
#   [คีย์มีผลทันที]   key_guard เฝ้า keystore จากดิสก์ทุก 30 วิ — แอดมิน revoke/ลบ/หมดอายุ
#                     มีผลทันทีทุกเครื่อง ผู้ใช้ไม่ต้องรีสตาร์ท (โดนระงับ = โปรแกรมหยุดเอง)
#   [คีย์ 1 บรรทัด]   รองรับ star_keys.txt — เพิ่มคีย์โดยพิมพ์ "1 บรรทัดต่อคีย์"
#                     รูปแบบ: KEY | KEY|ชื่อ | KEY|ชื่อ|2026-12-31 | KEY|ชื่อ|epoch
#                     คอนโซลแอดมินเพิ่ม [7] export→txt · [8] import←txt
#   [เมนู 1 ไม่ตรวจ 2FA] เพิ่มบัญชีด้วย Uss/Pss โดยไม่ล็อกอินผ่าน API อีกต่อไป
#                     อาศัยการล็อกอินที่ผู้ใช้ทำไว้ในแอป Roblox บนเครื่อง (ไม่โดน captcha)
#                     ใช้คู่กับเมนู [q] ได้เต็มที่ — โหมด passive เฝ้า process แอป (pidof)
#                     แอปตาย/หลุด → สั่งเปิดเกมกลับอัตโนมัติ · ผูก cookie ที่ [4] ภายหลัง
#                     ระบบสลับเป็นโหมดเฝ้าแบบ presence ให้เอง
#
# ใหม่ใน v4.2:
#   [Autoexec Delta] เมนู [x] จัดการสคริปต์ autoexecute สำหรับ Delta Executor
#                    - เพิ่ม/นำเข้า/ลบสคริปต์ · ผูกสคริปต์แยกต่อบัญชี
#                    - ตอนกด START ระบบ push สคริปต์ลงโฟลเดอร์ autoexec ของ Delta อัตโนมัติ
#                      (เคลียร์ไฟล์ที่ push ไว้ครั้งก่อนทุกรอบ กันไอดี A รันสคริปต์ของไอดี B)
#                    - หาโฟลเดอร์ autoexec อัตโนมัติ (ลองหลายพาธยอดนิยม)
#
# ใหม่ใน v4.1:
#   [คีย์จากแอดมิน] เปลี่ยนจาก key แบบผู้ใช้ตั้งเอง → คีย์ที่ "แอดมินสร้าง" จาก Admin Console
#                  เปิดคอนโซลแอดมินด้วย:  python star_plus.py admin
#                  รองรับ: วันหมดอายุ · ระงับทันทีทุกเครื่อง · ต่ออายุ · ลบถาวร · นับจำนวนการใช้
#   [อัตโนมัติ]     คีย์ที่เคยใส่ถูกจำไว้ในเครื่อง เปิดใหม่ปลดล็อกเองทันที
#                  แต่ตรวจสถานะ (หมดอายุ/ถูกระงับ) กับ keystore ทุกครั้ง — แอดมิน revoke ได้เรียลไทม์
#   [แจ้งเตือน]     เตือนเมื่อคีย์จะหมดอายุภายใน 72 ชม. · เมนู [k] ดูข้อมูลคีย์ / ล็อกเอาต์ได้
#
# ใหม่ใน v4.0 (STAR Plus):
#   [ชื่อใหม่] STAR Plus ทั้ง banner, ดาชบอร์ด, webhook
#   [โทนสี]  ตารางดาชบอร์ด + หน้าโหลด โทนน้ำเงิน truecolor ทั้งหมด
#   [หน้าโหลด] แอนิเมชัน loading bar + spinner ตอนเปิดโปรแกรมและก่อนเริ่มเฝ้าดู
#   [คีย์ล็อก] ระบบคีย์จากแอดมิน — ผู้ใช้ใส่คีย์ที่แอดมินสร้าง (ไม่ตั้งเอง) รองรับวันหมดอายุ/ระงับ
#             แอดมินจัดการคีย์ได้ที่คอนโซล: python star_plus.py admin
#   [Start Rejoin] เมนู [q] สำหรับผู้ใช้ที่ล็อกอินในเกมแล้ว ไม่ต้องล็อกอินผ่าน UI อีก
#   [Live Discord] webhook สร้าง "ข้อความแดชบอร์ดสด" บน Discord แล้วแก้ไขอัตโนมัติ
#                  ทุก 30 วิ (มีแถบนิ่ง% สีน้ำเงิน ครบทุกบัญชีแบบเรียลไทม์)
#   [ECO โหมด] ประหยัดแบต+RAM — poll ช้าลง หน้าจออัปเดตน้อยลง (เมนู [e])
#   [แก้บั๊ก] session แยกต่อบัญชี (ไม่รั่ว CSRF) · supervisor restart thread อัตโนมัติ
#             รองรับ 429 rate-limit · เปลี่ยนชื่อแล้ว state ไม่ค้าง · log หมุนเวียนลงไฟล์
#             กัน cookie ซ้ำ · validate place id · ลบโค้ดตาย
#
# ปิดสี: NO_COLOR=1 python star_plus.py

import json, os, re, sys, time, random, subprocess, threading, hashlib, logging
from logging.handlers import RotatingFileHandler
from collections import deque

try:
    import requests
except ImportError:
    sys.exit("[!] pip install requests ก่อนนะ")

VERSION = "4.3"
HERE    = os.path.dirname(os.path.abspath(__file__))
CONFIG  = os.path.join(HERE, "star_config.json")
STATS_F = os.path.join(HERE, "star_stats.json")
STOPF   = os.path.join(HERE, "STOP")
KEY_F   = os.path.join(HERE, "star_plus.key")
KEYS_F  = os.path.join(HERE, "star_keys.json")     # keystore ที่แอดมินจัดการ (v4.1)
KEYS_TXT = os.path.join(HERE, "star_keys.txt")     # เพิ่มคีย์ 1 บรรทัดต่อคีย์ — แก้ไขได้ทันที (v4.3)
ADMIN_F = os.path.join(HERE, "star_admin.json")    # master key แอดมิน (เก็บ hash)
HOOK_F  = os.path.join(HERE, "star_plus.hook.json")
LOG_F   = os.path.join(HERE, "star_plus.log")
SCRIPTS_D    = os.path.join(HERE, "star_scripts")            # คลังสคริปต์ของ STAR Plus (v4.2)
DELTA_MANIFEST = os.path.join(HERE, "star_delta.manifest.json")  # ไฟล์ push ลง autoexec ครั้งล่าสุด

# พาธยอดนิยมของโฟลเดอร์ autoexec ของ Delta (เช็กจากบนลงล่าง เอาอันที่เจอ)
DELTA_AUTOEXEC_CANDIDATES = [
    "/sdcard/Delta/autoexec",
    "/sdcard/Delta/autoexecute",
    "/sdcard/DeltaX/autoexec",
    "/sdcard/Android/data/com.delta.executor/files/autoexec",
    "/sdcard/Android/data/com.delta/files/autoexec",
]

POLL, ECO_POLL = 20, 45
GRACE, RETRY, RETRY_DELAY, BACKOFF = 50, 3, 15, 300
IN_GAME = 2
COLORS_ON = not os.environ.get("NO_COLOR") and sys.stdout.isatty()

stop   = threading.Event()
slock  = threading.Lock()
LOGQ   = deque(maxlen=64)
STATES = {}
THREADS = {}
TOTALS = {"rejoins": 0, "hops": 0, "alerts": 0}
_session_start = time.time()
_last_notify = {"t": 0, "key": ""}
_last_save   = {"t": 0}
_last_report = {"t": 0}
DASH         = {"on": False}
ECO          = {"on": False}
HOOK_STATE   = {"id": None}

logger = logging.getLogger("starplus")
logger.setLevel(logging.INFO)
try:
    _fh = RotatingFileHandler(LOG_F, maxBytes=200_000, backupCount=3, encoding="utf-8")
    _fh.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(_fh)
except Exception:
    pass

# ---------- ANSI (โทนน้ำเงิน) ----------
def ac(t, code): return f"\033[{code}m{t}\033[0m" if COLORS_ON else t
def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m" if COLORS_ON else ""
def grad_txt(line, w=None):
    if not COLORS_ON: return line
    w = w or max(1, len(line))
    c1, c2 = (0, 80, 235), (0, 195, 255)   # น้ำเงินเข้ม → ฟ้าอมน้ำเงิน
    out = []
    for i, ch in enumerate(line):
        t = i / max(1, w - 1)
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        out.append(rgb(r, g, b) + ch)
    return "".join(out) + ("\033[0m" if COLORS_ON else "")
GREEN, YELLOW, RED, GRAY = "92", "93", "91", "90"
CYAN, MAGENTA, BLUE = "96", "95", "94"
BORDER = "38;2;45;110;255"   # เส้นขอบตารางสีน้ำเงิน
PALETTE = [CYAN, MAGENTA, GREEN, YELLOW, BLUE, RED]

SYM = {"ok": ("✔", GREEN), "err": ("✘", RED), "warn": ("!!", YELLOW),
       "info": ("▶", CYAN), "dim": ("··", GRAY)}
ST_EMOJI = {"WATCH": "🟢", "REJOIN": "🟡", "HOP": "🟣",
            "COOLDOWN": "🔴", "DEAD": "⛔", "INIT": "⚪"}
ST_COLOR = {"WATCH": GREEN, "REJOIN": YELLOW, "HOP": MAGENTA,
            "COOLDOWN": RED, "DEAD": RED, "INIT": GRAY}

# ---------- หน้าโหลด ----------
def loading_screen(title="STAR PLUS", sub="กำลังเริ่มระบบ", secs=1.1):
    if not COLORS_ON:
        print(f"[*] {title} — {sub}"); time.sleep(0.3); return
    spin = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    c1, c2 = (0, 70, 220), (0, 190, 255)
    W = 44
    msgs = ["initializing", "loading config", "checking key", "preparing api", "ready"]
    steps = max(1, int(secs / 0.045))
    for step in range(steps + 1):
        fill = int(step / steps * W)
        bar = ""
        for i in range(W):
            if i < fill:
                t = i / (W - 1)
                bar += rgb(int(c1[0]+(c2[0]-c1[0])*t),
                           int(c1[1]+(c2[1]-c1[1])*t),
                           int(c1[2]+(c2[2]-c1[2])*t)) + "█"
            else:
                bar += "\033[90m░"
        bar += "\033[0m"
        msg = msgs[min(4, step * 5 // (steps + 1))]
        pct = int(step / steps * 100)
        sys.stdout.write(f"\r  {ac(spin[step % len(spin)], CYAN)} "
                         f"{grad_txt(title, len(title))} {bar} {ac(f'{pct:3d}%', BLUE)} {ac(msg, GRAY)}   ")
        sys.stdout.flush()
        time.sleep(0.045)
    sys.stdout.write("\r" + " " * 110 + "\r")
    print(f"  {ac('✔', GREEN)} {grad_txt(title, len(title))} {ac('พร้อมใช้งาน', GREEN)}")

# ---------- ระบบคีย์จากแอดมิน (v4.1) ----------
# ผู้ใช้ "ไม่ตั้งคีย์เอง" อีกต่อไป — แอดมินสร้างคีย์จากคอนโซล: python star_plus.py admin
# ผู้ใช้ได้คีย์ไปใส่ในโปรแกรม ระบบตรวจสถานะกับ star_keys.json ทุกครั้งที่เปิด
def _norm_key(k):
    """ทำให้คีย์เป็นรูปแบบมาตรฐาน: ตัดอักขระพิเศษ/ช่องว่าง พิมพ์ใหญ่ (รับทั้ง XXXX-XXXX หรือยาวติดกัน)"""
    return re.sub(r"[^A-Z0-9]", "", (k or "").upper())

def _khash(salt, k):
    return hashlib.sha256((salt + k).encode()).hexdigest()

def pretty_key(nk):
    """แสดงคีย์แบบมีขีด: STAR-XXXX-XXXX-XXXX-XXXX"""
    nk = _norm_key(nk)
    if len(nk) == 20:
        return "-".join([nk[:4]] + [nk[i:i+4] for i in range(4, 20, 4)])
    return nk

def mask_key(nk):
    """ปิดคีย์บางส่วนเพื่อแสดงผล: STAR-XXXX-****-****-****"""
    nk = _norm_key(nk)
    return nk[:8] + "-****-****-****" if len(nk) >= 8 else "****"

def gen_key():
    """สุ่มคีย์ 128-bit (STAR + 16 ตัวอักษร hex) ผ่าน os.urandom — cryptographically secure PRNG"""
    return "STAR" + os.urandom(8).hex().upper()

# ---------- keystore (star_keys.json + star_keys.txt) ----------
def load_keys_txt():
    """star_keys.txt — เพิ่มคีย์แบบ 1 บรรทัดต่อคีย์ แก้ไขได้ทันที (มีผลภายใน 30 วิ)
    รูปแบบบรรทัด:
        STAR-XXXX-XXXX-XXXX-XXXX                          ไม่หมดอายุ ไม่มีชื่อ
        STAR-XXXX-XXXX-XXXX-XXXX|ชื่อผู้ใช้
        STAR-XXXX-XXXX-XXXX-XXXX|ชื่อผู้ใช้|2026-12-31       หมดอายุวันที่ (สิ้นวัน)
        STAR-XXXX-XXXX-XXXX-XXXX|ชื่อผู้ใช้|1735689600      หมดอายุแบบ epoch
    บรรทัดว่าง หรือขึ้นต้นด้วย # = คอมเมนต์ (ข้าม)"""
    out = {}
    if not os.path.exists(KEYS_TXT):
        return out
    now = time.time()
    try:
        with open(KEYS_TXT, encoding="utf-8", errors="ignore") as f:
            for raw in f:
                ln = raw.strip()
                if not ln or ln.startswith("#"):
                    continue
                parts = [p.strip() for p in ln.split("|")]
                nk = _norm_key(parts[0])
                if len(nk) < 8:
                    continue
                label, exp = None, None
                for extra in parts[1:]:
                    if not extra:
                        continue
                    if re.fullmatch(r"\d{9,12}", extra):
                        exp = int(extra)
                    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", extra):
                        try:
                            exp = int(time.mktime(time.strptime(extra, "%Y-%m-%d"))) + 86399
                        except Exception:
                            pass
                    else:
                        label = extra
                out[nk] = {"label": label, "created": now, "expires": exp,
                           "revoked": False, "uses": 0, "last_used": None}
    except Exception:
        pass
    return out

def load_keystore():
    """รวมคีย์จาก star_keys.json (ฐานข้อมูลหลัก แอดมินคอนโซล) + star_keys.txt (overlay 1 บรรทัด/คีย์)
    โหลดจากดิสก์ใหม่ทุกครั้งที่เรียก — แอดมินแก้ไขมีผลทันที ไม่ต้องรีสตาร์ทโปรแกรม"""
    store = {"keys": {}}
    if os.path.exists(KEYS_F):
        try:
            with open(KEYS_F) as f:
                d = json.load(f)
            if isinstance(d, dict):
                for kk, k in d.get("keys", {}).items():
                    if isinstance(k, dict):
                        k["_src"] = "json"
                        store["keys"][kk] = k
        except Exception:
            pass
    for kk, k in load_keys_txt().items():
        k["_src"] = "txt"          # txt ทับฟิลด์ของ json เสมอ (overlay)
        store["keys"][kk] = k
    return store

def save_keystore(store):
    try:
        data = {"keys": {kk: {a: b for a, b in kv.items() if a != "_src"}
                         for kk, kv in store.get("keys", {}).items()
                         if kv.get("_src") != "txt"}}   # คีย์จาก txt ไม่เขียนลง json
        with open(KEYS_F, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(KEYS_F, 0o600)
    except Exception:
        pass

def key_status(store, nk):
    """คืนสถานะคีย์: OK / MISSING / REVOKED / EXPIRED"""
    k = store.get("keys", {}).get(nk)
    if not k:
        return "MISSING"
    if k.get("revoked"):
        return "REVOKED"
    exp = k.get("expires")
    if exp and time.time() > exp:
        return "EXPIRED"
    return "OK"

def check_key(store, key):
    """ตรวจคีย์ + บันทึก last_used/uses (audit) — คืน (info_dict, 'OK') หรือ (None, สถานะผิดพลาด)"""
    nk = _norm_key(key)
    st = key_status(store, nk)
    if st != "OK":
        return None, st
    k = store["keys"][nk]
    k["last_used"] = int(time.time())
    k["uses"] = int(k.get("uses", 0)) + 1
    save_keystore(store)
    return k, "OK"

def key_expiry_text(k):
    exp = k.get("expires")
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(exp)) if exp else "ไม่มีวันหมดอายุ"

def warn_expiry(k):
    """แจ้งเตือนถ้าคีย์จะหมดอายุภายใน 72 ชม."""
    exp = k.get("expires")
    if not exp:
        return
    left = exp - time.time()
    if 0 < left < 72 * 3600:
        print(ac(f"[!] คีย์นี้จะหมดอายุในอีก {int(left // 3600)} ชม. — ติดต่อแอดมินเพื่อต่ออายุ", YELLOW))

# ---------- cache คีย์ในเครื่องผู้ใช้ ----------
def save_keycache(nk):
    try:
        with open(KEY_F, "w") as f:
            json.dump({"key": nk}, f)
        os.chmod(KEY_F, 0o600)
    except Exception:
        pass

def load_keycache():
    try:
        with open(KEY_F) as f:
            return json.load(f).get("key", "")
    except Exception:
        return ""

def clear_keycache():
    try:
        if os.path.exists(KEY_F):
            os.remove(KEY_F)
    except Exception:
        pass

# ---------- key guard: เฝ้าคีย์แบบเรียลไทม์ (v4.3) ----------
def key_guard():
    """เฝ้าสถานะคีย์ทุก 30 วิ — โหลด keystore จากดิสก์ใหม่ทุกรอบ
    แอดมิน revoke / ลบ / ให้หมดอายุที่ star_keys.json หรือ star_keys.txt
    มีผลทันทีทุกเครื่อง โดยผู้ใช้ไม่ต้องรีสตาร์ทโปรแกรม"""
    nk = load_keycache()
    if not nk:
        return
    while not stop.is_set():
        time.sleep(30)
        try:
            store = load_keystore()
        except Exception:
            continue
        st = key_status(store, nk)
        if st == "OK":
            continue
        msg = {"REVOKED": "คีย์ถูกระงับโดยแอดมิน",
               "EXPIRED": "คีย์หมดอายุแล้ว",
               "MISSING": "คีย์ถูกลบออกจากระบบ"}.get(st, "คีย์ใช้ไม่ได้อีกต่อไป")
        try:
            print(ac(f"\n[✘] {msg} — ระบบหยุดทำงานทันที (STAR Plus)", RED))
            with open(STOPF, "w") as f:
                f.write("key revoked")
        except Exception:
            pass
        os._exit(3)

# ---------- ประตูคีย์ฝั่งผู้ใช้ (แทน key_gate เดิม) ----------
def key_gate():
    store = load_keystore()
    if not store.get("keys"):
        print(ac("\n  [!] ยังไม่มีคีย์ในระบบ — ติดต่อแอดมินเพื่อขอคีย์", RED))
        print(ac("      แอดมินเปิดคอนโซลด้วยคำสั่ง: python star_plus.py admin", GRAY))
        return False
    # 1) ลองปลดล็อกอัตโนมัติด้วยคีย์ที่จำไว้ (แต่ยังเช็กกับ keystore ทุกครั้ง)
    cached = load_keycache()
    if cached and key_status(store, cached) == "OK":
        k = store["keys"][_norm_key(cached)]
        k["last_used"] = int(time.time())
        save_keystore(store)
        print(ac(f"[OK] ปลดล็อกด้วยคีย์เดิมอัตโนมัติ ({mask_key(cached)})", GREEN))
        warn_expiry(k)
        return True
    if cached:
        print(ac("[!] คีย์ที่จำไว้ใช้ไม่ได้แล้ว (หมดอายุ/ถูกระงับ) — ใส่คีย์ใหม่จากแอดมิน", YELLOW))
        clear_keycache()
    # 2) ให้ผู้ใช้ใส่คีย์จากแอดมิน (3 ครั้ง)
    for att in range(3, 0, -1):
        store = load_keystore()   # โหลดใหม่ทุกครั้ง — แอดมินเพิ่มคีย์มีผลทันที
        try:
            k = input(f"[🔑] ใส่คีย์จากแอดมิน (เหลือ {att} ครั้ง): ").strip()
        except (EOFError, KeyboardInterrupt):
            return False
        info, st = check_key(store, k)
        if info:
            save_keycache(_norm_key(k))
            print(ac("[OK] ปลดล็อกแล้ว", GREEN))
            warn_expiry(info)
            return True
        msg = {"MISSING": "ไม่มีคีย์นี้ในระบบ — เช็กการพิมพ์อีกที",
               "REVOKED": "คีย์นี้ถูกระงับโดยแอดมิน",
               "EXPIRED": "คีย์นี้หมดอายุแล้ว — ติดต่อแอดมินเพื่อต่ออายุ"}.get(st, "คีย์ผิด")
        print(ac(f"[!] {msg}", RED))
    print(ac("[✘] ล็อกเกินกำหนด — ปิดโปรแกรม", RED))
    return False

def key_info_menu():
    """เมนู [k] ฝั่งผู้ใช้: ดูข้อมูลคีย์ตัวเอง + ล็อกเอาต์"""
    store = load_keystore()
    nk = load_keycache()
    if not nk:
        print("[!] เครื่องนี้ยังไม่ได้จำคีย์ไว้")
        return
    k = store.get("keys", {}).get(nk)
    if not k:
        print("[!] ไม่พบคีย์ในระบบ (อาจถูกลบโดยแอดมิน) — ล้างคีย์ที่จำไว้แล้ว")
        clear_keycache()
        return
    print(f"  คีย์ปัจจุบัน : {mask_key(nk)}")
    print(f"  ชื่อ/หมายเหตุ: {k.get('label') or '-'}")
    print(f"  หมดอายุ    : {key_expiry_text(k)}")
    lu = k.get("last_used")
    print(f"  ใช้ล่าสุด   : {time.strftime('%Y-%m-%d %H:%M', time.localtime(lu)) if lu else '-'}")
    print(f"  จำนวนการใช้: {k.get('uses', 0)} ครั้ง")
    if input("\n[?] ล็อกเอาต์ (ลบคีย์ที่จำไว้ในเครื่อง)? (y/n): ").strip().lower() == "y":
        clear_keycache()
        print(ac("[OK] ล็อกเอาต์แล้ว — เปิดใหม่จะต้องใส่คีย์จากแอดมินอีกครั้ง", GREEN))

# ---------- Admin Console: สร้าง/จัดการคีย์ (python star_plus.py admin) ----------
def _find_key_interactive(store, prompt="[?] คีย์ (STAR-...): "):
    raw = input(prompt).strip()
    nk = _norm_key(raw)
    if nk not in store.get("keys", {}):
        print(ac("[!] ไม่มีคีย์นี้ในระบบ", RED))
        return None
    return nk

def admin_console():
    print()
    print(grad_txt("  ★ STAR PLUS — ADMIN KEY CONSOLE ★", w=40))
    # ตั้ง Master Key ครั้งแรก (เก็บ hash เท่านั้น — กู้คืนไม่ได้ ถ้าลืมให้ลบ star_admin.json)
    if not os.path.exists(ADMIN_F):
        print(ac("  ครั้งแรก — ตั้ง Master Key สำหรับแอดมิน (เก็บแค่ hash ในเครื่อง)", YELLOW))
        while True:
            m1 = input("[🔐] ตั้ง Master Key (อย่างน้อย 6 ตัวอักษร): ").strip()
            if len(m1) < 6:
                print(ac("[!] สั้นไป — อย่างน้อย 6 ตัวอักษร", RED)); continue
            if input("[🔐] พิมพ์ซ้ำยืนยัน: ").strip() != m1:
                print(ac("[!] ไม่ตรงกัน", RED)); continue
            salt = os.urandom(8).hex()
            with open(ADMIN_F, "w") as f:
                json.dump({"salt": salt, "hash": _khash(salt, m1)}, f)
            os.chmod(ADMIN_F, 0o600)
            print(ac("[OK] ตั้ง Master Key แล้ว — เก็บให้ดี ลืมแล้วต้องลบ star_admin.json", GREEN))
            break
    try:
        data = json.load(open(ADMIN_F))
    except Exception:
        print(ac("[!] ไฟล์แอดมินเสีย — ลบ star_admin.json แล้วเริ่มตั้งใหม่", RED))
        return
    ok = False
    for att in range(3, 0, -1):
        try:
            m = input(f"[🔐] Master Key (เหลือ {att} ครั้ง): ").strip()
        except (EOFError, KeyboardInterrupt):
            return
        if _khash(data["salt"], m) == data["hash"]:
            ok = True; break
        print(ac("[!] Master Key ผิด", RED))
    if not ok:
        print(ac("[✘] ปิดคอนโซลแอดมิน", RED))
        return
    print(ac("[OK] เข้าสู่คอนโซลแอดมินแล้ว", GREEN))
    store = load_keystore()
    while True:
        total = len(store["keys"])
        active = sum(1 for kk in store["keys"] if key_status(store, kk) == "OK")
        print()
        print(ac(f"  ┌─ Admin Console ── คีย์ทั้งหมด {total} · ใช้งานได้ {active} ─┐", BORDER))
        print("  [1] สร้างคีย์ใหม่")
        print("  [2] รายชื่อคีย์ทั้งหมด")
        print("  [3] ระงับ / ปลดระงับคีย์ (มีผลทันทีทุกเครื่อง)")
        print("  [4] ต่ออายุคีย์")
        print("  [5] ลบคีย์ถาวร")
        print("  [6] เปลี่ยน Master Key")
        print("  [7] export คีย์ทั้งหมด → star_keys.txt (1 บรรทัด/คีย์)")
        print("  [8] import คีย์จาก star_keys.txt เข้าฐานข้อมูล")
        print("  [0] ออก")
        c = input("[?] เลือก: ").strip()
        if c == "0":
            return
        elif c == "1":
            label = input("[?] ชื่อ/หมายเหตุผู้ใช้ (Enter ข้าม): ").strip() or None
            d = input("[?] อายุคีย์ (วัน, Enter = ไม่หมดอายุ): ").strip()
            expires = None
            if d.isdigit() and int(d) > 0:
                expires = int(time.time()) + int(d) * 86400
            nk = gen_key()
            store["keys"][nk] = {"label": label, "created": int(time.time()),
                                 "expires": expires, "revoked": False,
                                 "uses": 0, "last_used": None}
            save_keystore(store)
            print(ac("[OK] สร้างคีย์แล้ว — ส่งให้ผู้ใช้ได้เลย (แสดงครั้งเดียว):", GREEN))
            print(ac(f"     {pretty_key(nk)}", CYAN))
            if expires:
                print(ac(f"     หมดอายุ: {key_expiry_text(store['keys'][nk])}", GRAY))
        elif c == "2":
            if not store["keys"]:
                print("  (ยังไม่มีคีย์)")
                continue
            for kk, k in store["keys"].items():
                st = key_status(store, kk)
                mark = {"OK": ac("✔ ใช้ได้", GREEN), "EXPIRED": ac("⏰ หมดอายุ", GRAY),
                        "REVOKED": ac("✘ ระงับ", RED)}.get(st, st)
                lu = k.get("last_used")
                lu_txt = time.strftime("%m-%d %H:%M", time.localtime(lu)) if lu else "-"
                print(f"  {pretty_key(kk)}  {mark}  {k.get('label') or '-'}  "
                      f"หมดอายุ {key_expiry_text(k)}  ใช้ {k.get('uses',0)} ครั้ง  ล่าสุด {lu_txt}")
        elif c == "3":
            kk = _find_key_interactive(store)
            if not kk:
                continue
            k = store["keys"][kk]
            k["revoked"] = not k.get("revoked", False)
            save_keystore(store)
            print(ac(f"[OK] {'ระงับ' if k['revoked'] else 'ปลดระงับ'}แล้ว — มีผลทันทีทุกเครื่อง", GREEN))
        elif c == "4":
            kk = _find_key_interactive(store, "[?] คีย์ที่จะต่ออายุ: ")
            if not kk:
                continue
            d = input("[?] ต่ออายุอีกกี่วัน (Enter = ไม่หมดอายุ): ").strip()
            if d.isdigit() and int(d) > 0:
                base = max(store["keys"][kk].get("expires") or 0, time.time())
                store["keys"][kk]["expires"] = int(base) + int(d) * 86400
            else:
                store["keys"][kk]["expires"] = None
            save_keystore(store)
            print(ac(f"[OK] ต่ออายุแล้ว → {key_expiry_text(store['keys'][kk])}", GREEN))
        elif c == "5":
            kk = _find_key_interactive(store, "[?] คีย์ที่จะลบถาวร: ")
            if not kk:
                continue
            if input(f"[?] ยืนยันลบ {pretty_key(kk)}? (y/n): ").strip().lower() == "y":
                del store["keys"][kk]
                save_keystore(store)
                print("[OK] ลบแล้ว")
        elif c == "6":
            cur = input("[🔐] Master Key ปัจจุบัน: ").strip()
            if _khash(data["salt"], cur) != data["hash"]:
                print(ac("[!] ผิด", RED)); continue
            m1 = input("[🔐] Master Key ใหม่ (อย่างน้อย 6 ตัวอักษร): ").strip()
            if len(m1) < 6:
                print(ac("[!] สั้นไป", RED)); continue
            if input("[🔐] พิมพ์ซ้ำยืนยัน: ").strip() != m1:
                print(ac("[!] ไม่ตรงกัน", RED)); continue
            salt = os.urandom(8).hex()
            with open(ADMIN_F, "w") as f:
                json.dump({"salt": salt, "hash": _khash(salt, m1)}, f)
            os.chmod(ADMIN_F, 0o600)
            print(ac("[OK] เปลี่ยน Master Key แล้ว", GREEN))
        elif c == "7":
            try:
                n = 0
                with open(KEYS_TXT, "w", encoding="utf-8") as f:
                    f.write("# STAR Plus — 1 คีย์ต่อบรรทัด: KEY|ชื่อ|วันหมดอายุ(YYYY-MM-DD หรือ epoch)\n")
                    for kk, k in store["keys"].items():
                        exp = k.get("expires")
                        exp_txt = time.strftime("%Y-%m-%d", time.localtime(exp)) if exp else ""
                        line = pretty_key(kk)
                        if k.get("label") or exp_txt:
                            line += "|" + (k.get("label") or "")
                        if exp_txt:
                            line += "|" + exp_txt
                        f.write(line + "\n")
                        n += 1
                print(ac(f"[OK] export {n} คีย์แล้ว → {KEYS_TXT}", GREEN))
                print(ac("     แก้ไขไฟล์นี้ได้เลย — มีผลทันทีภายใน 30 วิทุกเครื่อง", GRAY))
            except Exception as e:
                print(ac(f"[!] export ไม่สำเร็จ: {e}", RED))
        elif c == "8":
            found = load_keys_txt()
            n = 0
            for kk, k in found.items():
                if kk not in store["keys"]:
                    k.pop("_src", None)
                    store["keys"][kk] = k
                    n += 1
            save_keystore(store)
            print(ac(f"[OK] import แล้ว — เพิ่มใหม่ {n} คีย์จาก {KEYS_TXT}", GREEN))

# ---------- log ----------
def dlog(tag, msg, level="info", tcolor=None):
    ts = time.strftime("%H:%M:%S")
    sym, sc = SYM.get(level, SYM["info"])
    line = f"{ac(ts, GRAY)} {ac(sym, sc)} {ac(tag, tcolor or CYAN)} {msg}"
    rec = (ts, sym, sc, tag, tcolor or CYAN, msg)
    LOGQ.append(rec)
    try: logger.info("%s %s %s", tag, msg)
    except Exception: pass
    if not DASH["on"]:
        with slock:
            print(line, flush=True)

def notify(cfg, key, title, desc, color=0xf1c40f):
    TOTALS["alerts"] += 1
    now = time.time()
    if key and (now - _last_notify["t"] < 30) and _last_notify["key"] == key:
        return
    _last_notify.update(t=now, key=key)
    url = cfg.get("webhook", "").strip()
    def _post():
        try:
            if url:
                requests.post(url, json={"embeds": [{"title": title, "description": desc,
                                                     "color": color, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}]},
                              timeout=10)
        except Exception: pass
        try:
            subprocess.run(["termux-notification", "-t", "STAR Plus", "-c", f"{title}: {desc}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        except Exception: pass
    threading.Thread(target=_post, daemon=True).start()

# ---------- รายงานสถานะเข้า webhook ----------
def acc_snapshot(acc):
    st = STATES.get(acc.get("label", ""), {})
    state = st.get("state", "INIT")
    app = st.get("app") or {}
    up = time.time() - st.get("start", time.time())
    stable = (st.get("in_ts", 0) / up * 100) if up > 5 and state != "DEAD" else 0
    apptxt = f"แอป #{app.get('num')}" if app else "ไม่ได้ผูกแอป"
    return (f"{state} · {apptxt} · place {st.get('place','-')} · "
            f"rejoin {st.get('rejoins',0)} · hop {st.get('hops',0)} · "
            f"นิ่ง {stable:.0f}% · up {fmt_up(up)}"), state

def stab_bar(pct, n=10):
    f = max(0, min(n, int(pct / 100 * n)))
    return "🟦" * f + "⬜" * (n - f)

def send_report(cfg, reason="รายงานประจำ"):
    url = cfg.get("webhook", "").strip()
    if not url or not cfg["accounts"]:
        return
    fields, states = [], []
    for acc in cfg["accounts"]:
        txt, state = acc_snapshot(acc)
        fields.append({"name": acc.get("label", "?"), "value": txt, "inline": False})
        states.append(state)
    color = (0xe74c3c if ("DEAD" in states or "COOLDOWN" in states)
             else 0xf1c40f if any(s in ("REJOIN", "HOP", "INIT") for s in states)
             else 0x0099ff)
    embed = {"embeds": [{
        "title": f"STAR Plus · {reason}",
        "description": f"rejoin รวม {TOTALS['rejoins']} · hop {TOTALS['hops']} · alert {TOTALS['alerts']}",
        "fields": fields,
        "color": color,
        "footer": {"text": f"STAR Plus v{VERSION} · https://discord.gg/kYDu7qth"},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }]}
    def _post():
        try:
            requests.post(url, json=embed, timeout=10)
        except Exception:
            pass
    threading.Thread(target=_post, daemon=True).start()

def report_loop(cfg):
    while not stop.is_set():
        time.sleep(20)
        mins = cfg.get("report_min", 60)
        if time.time() - _last_report["t"] >= max(1, mins) * 60:
            _last_report["t"] = time.time()
            send_report(cfg)

# ---------- Live Discord Dashboard (แก้ข้อความเดิมอัตโนมัติ) ----------
def load_hookstate():
    if os.path.exists(HOOK_F):
        try:
            with open(HOOK_F) as f:
                HOOK_STATE.update({k: v for k, v in json.load(f).items() if k in HOOK_STATE})
        except Exception:
            pass

def save_hookstate():
    try:
        with open(HOOK_F, "w") as f:
            json.dump(HOOK_STATE, f)
    except Exception:
        pass

def live_embed(cfg):
    fields, states = [], []
    for acc in cfg["accounts"]:
        txt, state = acc_snapshot(acc)
        states.append(state)
        st = STATES.get(acc.get("label", ""), {})
        up = time.time() - st.get("start", time.time())
        stable = (st.get("in_ts", 0) / up * 100) if up > 5 and state != "DEAD" else 0
        fields.append({
            "name": f"{ST_EMOJI.get(state, '⚪')} {acc.get('label', '?')}",
            "value": f"{stab_bar(stable)} **{stable:.0f}%**\n{txt}",
            "inline": False,
        })
    color = (0xe74c3c if ("DEAD" in states or "COOLDOWN" in states)
             else 0xf1c40f if any(s in ("REJOIN", "HOP", "INIT") for s in states)
             else 0x0099ff)
    return {
        "title": "📡 STAR Plus · Live Dashboard",
        "description": (f"🕒 อัปเดต {time.strftime('%H:%M:%S')} · rejoin {TOTALS['rejoins']} · "
                        f"hop {TOTALS['hops']} · {'🍃 ECO' if ECO['on'] else '⚡ ปกติ'}"),
        "fields": fields,
        "color": color,
        "footer": {"text": f"STAR Plus v{VERSION} · ข้อความนี้จะอัปเดตเองแบบเรียลไทม์"},
    }

def live_update(cfg):
    url = cfg.get("webhook", "").strip()
    if not url or not cfg["accounts"]:
        return
    mid = HOOK_STATE.get("id")
    target = f"{url}/messages/{mid}" if mid else url
    method = "PATCH" if mid else "POST"
    try:
        r = requests.request(method, target, json={"embeds": [live_embed(cfg)]}, timeout=10)
        if method == "POST" and r.status_code in (200, 204):
            HOOK_STATE["id"] = (r.json() or {}).get("id")
            save_hookstate()
        elif method == "PATCH" and r.status_code in (400, 401, 404):
            HOOK_STATE["id"] = None
            save_hookstate()
    except Exception:
        pass

def live_loop(cfg):
    time.sleep(8)
    while not stop.is_set():
        live_update(cfg)
        time.sleep(60 if ECO["on"] else 30)

# ---------- config / stats ----------
def load_cfg():
    if os.path.exists(CONFIG):
        try:
            with open(CONFIG) as f:
                c = json.load(f)
                if "eco" in c:
                    ECO["on"] = bool(c["eco"])
                return c
        except Exception:
            pass
    return {"accounts": [], "apps": [], "webhook": "", "version": 4}

def save_cfg(c):
    c["version"] = 4
    c["eco"] = ECO["on"]
    with open(CONFIG, "w") as f: json.dump(c, f, indent=2)
    os.chmod(CONFIG, 0o600)

def throttled_save(cfg):
    if time.time() - _last_save["t"] > 60:
        _last_save["t"] = time.time()
        save_cfg(cfg)

def load_totals():
    global TOTALS
    if os.path.exists(STATS_F):
        try:
            with open(STATS_F) as f: TOTALS.update({k: v for k, v in json.load(f).items()
                                                    if k in TOTALS})
        except Exception: pass

def save_totals():
    TOTALS["uptime_sec"] = int(time.time() - _session_start)
    try:
        with open(STATS_F, "w") as f: json.dump(TOTALS, f, indent=2)
    except Exception: pass

# ---------- Roblox API (session แยกต่อบัญชี + รองรับ 429) ----------
def new_session():
    s = requests.Session()
    s.headers.update({"User-Agent": f"Mozilla/5.0 (Linux; Android 13) STARPlus/{VERSION}",
                      "Accept": "application/json"})
    return s

S = new_session()

def req(sess, method, url, rl_retries=2, **kw):
    """ยิง API พร้อมรองรับ 429 — คืน response ตัวสุดท้าย (หรือ None ถ้า network พัง)"""
    s = sess or S
    r = None
    for _ in range(rl_retries + 1):
        try:
            r = s.request(method, url, timeout=15, **kw)
        except Exception:
            return None
        if r.status_code == 429:
            try:
                wait = float(r.headers.get("Retry-After", 5))
            except Exception:
                wait = 5
            time.sleep(min(max(wait, 1), 30))
            continue
        return r
    return r

def whoami(cookie, sess=None):
    r = req(sess, "GET", "https://users.roblox.com/v1/users/authenticated",
            cookies={".ROBLOSECURITY": cookie})
    return r.json() if r is not None and r.status_code == 200 else None

def presence(uid, cookie=None, sess=None):
    r = req(sess, "POST", "https://presence.roblox.com/v1/presence/users",
            cookies={".ROBLOSECURITY": cookie} if cookie else None,
            json={"userIds": [uid]})
    if r is None or r.status_code != 200:
        return None
    lst = r.json().get("userPresences", [])
    return lst[0] if lst else None

def uid_by_username(name):
    r = req(S, "POST", "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [name], "excludeBannedUsers": False})
    d = r.json().get("data", []) if r is not None else []
    return d[0]["id"] if d else None

def place_info(pid):
    r = req(S, "GET", f"https://apis.roblox.com/universes/v1/places/{pid}/universe")
    return r.json().get("universeId") if r is not None and r.status_code == 200 else None

def pick_server(universe_id):
    if not universe_id: return None
    r = req(S, "GET", f"https://games.roblox.com/v1/games/{universe_id}/servers/Public",
            params={"limit": 25, "sortOrder": "Asc"})
    if r is None:
        return None
    try:
        data = r.json().get("data", [])
        room = [d for d in data if d.get("playing", 999) < d.get("maxPlayers", 0)]
        return random.choice(room[:5])["id"] if room else None
    except Exception:
        return None

# ---------- เพิ่มบัญชี ----------
def extract_cookie(text):
    m = re.search(r"_\|WARNING:-DO-NOT-SHARE-THIS[^\"'\s;]+", text)
    return m.group(0) if m else None

def parse_cookie_text(text):
    out = []
    for ln in text.splitlines():
        ln = ln.strip().strip(",")
        if not ln or ln == ".":
            continue
        ck = extract_cookie(ln)
        if not ck:
            continue
        rest = ln.replace(ck, "").strip().strip("|:").strip()
        out.append((rest or None, ck))
    return out

def parse_cookie_file(path):
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except Exception:
        return []
    pairs = []
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    ck = extract_cookie(v) or v.strip()
                    if ck:
                        pairs.append((k, ck))
        elif isinstance(data, list):
            for it in data:
                if isinstance(it, str):
                    ck = extract_cookie(it)
                    if ck:
                        pairs.append((None, ck))
                elif isinstance(it, dict):
                    ck = extract_cookie(str(it.get("cookie", "")))
                    if ck:
                        pairs.append((it.get("label"), ck))
        if pairs:
            return pairs
    except Exception:
        pass
    return parse_cookie_text(text)

def login_userpass(username, password):
    """ล็อกอินด้วย user/pass → .ROBLOSECURITY
    ใช้ session ชั่วคราว (CSRF ไม่หลุดไปปนกับ session ของบัญชีอื่น)"""
    s = new_session()
    for _ in range(2):
        try:
            r = s.post("https://auth.roblox.com/v2/login",
                       json={"ctype": "Username", "cvalue": username, "password": password},
                       timeout=15)
            if r.status_code == 403 and r.headers.get("x-csrf-token"):
                s.headers.update({"X-CSRF-TOKEN": r.headers["x-csrf-token"]})
                continue
            if r.status_code in (200, 201):
                return r.cookies.get(".ROBLOSECURITY")
            return None
        except Exception:
            return None
    return None

def add_account(cfg, label, cookie, app_num=None):
    """ตรวจ cookie + กันซ้ำ + เพิ่มบัญชี — คืน me ถ้าสำเร็จ, None ถ้าไม่"""
    if any(a.get("cookie") == cookie for a in cfg["accounts"]):
        return None
    me = whoami(cookie)
    if not me:
        return None
    label = (label or "").strip() or me["name"]
    if any(a.get("label") == label for a in cfg["accounts"]):
        label = f"{label}#{len(cfg['accounts']) + 1}"
    cfg["accounts"].append({"label": label, "cookie": cookie,
                            "place_id": None, "app_num": app_num, "hop": False})
    return me

def choose_app_map(cfg, count):
    if not cfg["apps"]:
        print(ac("  (ยังไม่มีแอป — ไปสแกนที่เมนู [3] ก่อน แล้วค่อยผูกทีหลังได้)", GRAY))
        return [None] * count
    show_apps(cfg)
    print(ac("  พิมพ์ตัวเลขแอป เช่น 1,2,1  |  a = หมุนเวียนอัตโนมัติ  |  Enter = ไม่ผูก", GRAY))
    s = input(f"[?] ผูกแอปให้ {count} ไอดี: ").strip().lower()
    if not s:
        return [None] * count
    if s == "a":
        return [cfg["apps"][i % len(cfg["apps"])]["num"] for i in range(count)]
    nums = [int(x) for x in re.split(r"[,\s]+", s) if x.isdigit()]
    if not nums:
        return [None] * count
    return [nums[i] if i < len(nums) else nums[-1] for i in range(count)]

def pick_app(cfg, prompt="[?] เลือกแอป #(เลข, Enter ไม่ผูก): "):
    if not cfg["apps"]:
        print(ac("  (ยังไม่มีแอป — ไปสแกนที่เมนู [3] ก่อน)", GRAY))
        return None
    show_apps(cfg)
    s = input(prompt).strip()
    if s.isdigit() and any(a.get("num") == int(s) for a in cfg["apps"]):
        return int(s)
    return None

def bulk_add(cfg, pairs):
    if not pairs:
        print("[!] ไม่พบ cookie ที่ใช้ได้")
        return 0
    print(f"[*] พบ cookie {len(pairs)} ตัว — กำลังตรวจสอบกับ Roblox...")
    appmap = choose_app_map(cfg, len(pairs))
    added = 0
    for i, (lb, ck) in enumerate(pairs):
        me = add_account(cfg, lb, ck, appmap[i])
        if me:
            added += 1
            apptxt = ""
            if appmap[i]:
                app = next((a for a in cfg["apps"] if a.get("num") == appmap[i]), None)
                apptxt = ac(f" → #{appmap[i]} {app.get('name','') if app else ''}", MAGENTA)
            print(f"[OK] {ac(me['name'], GREEN)}{apptxt}")
        else:
            dup = any(a.get("cookie") == ck for a in cfg["accounts"])
            why = "ซ้ำกับบัญชีที่มีอยู่" if dup else "cookie ใช้ไม่ได้ — ข้าม"
            print(f"[{ac('!!', YELLOW)}] {lb or ck[:24] + '..'} {why}")
    if added:
        save_cfg(cfg)
    print(ac(f"[OK] เพิ่มสำเร็จ {added}/{len(pairs)} บัญชี", CYAN))
    if added and not all(a.get("place_id") for a in cfg["accounts"]):
        if input("[?] ตั้ง place id ให้ไอดีที่ยังไม่มีแมพเลยไหม (y/n): ").strip().lower() == "y":
            pid = input("[?] place id: ").strip()
            if pid.isdigit():
                uni = place_info(int(pid))
                for a in cfg["accounts"]:
                    if not a.get("place_id"):
                        a["place_id"] = int(pid)
                save_cfg(cfg)
                print(ac(f"[OK] ตั้งแมพให้ทุกไอดีแล้ว"
                         + (f" (universe {uni})" if uni else " (⚠ ตรวจแมพไม่เจอ — เช็กเลขอีกที)"), GREEN))
                print(ac("     กด [7] หรือ [q] เพื่อเริ่มเฝ้าดูได้เลย", GRAY))
    return added

# ---------- บทเรียนในตัว ----------
def tut_up():
    bar = ac("─" * 64, GRAY)
    print(bar)
    print(ac("  บทเรียน: เพิ่มบัญชีด้วย Uss/Pss (ไม่ต้องล็อกอินผ่านสคริปต์)", CYAN))
    print(bar)
    print("  1) พิมพ์ Username ของ Roblox ลงที่นี่ — ไม่ต้องใส่พาสเวิร์ด ไม่ต้องกรอก 2FA")
    print("  2) ระบบเพิ่มบัญชีทันที โดยอาศัยการล็อกอินที่คุณทำไว้ในแอป Roblox บนเครื่องนี้")
    print("  3) กด [q] (Start Rejoin) เพื่อเริ่มเฝ้าดู — เหมาะกับคนที่ล็อกอินในเกมแล้ว")
    print()
    print(ac("  ทำไมไม่ต้องตรวจ 2FA:", YELLOW))
    print("  • การล็อกอินผ่าน API มักโดน captcha/2FA จนเพิ่มบัญชีไม่สำเร็จ")
    print("  • โหมดนี้เฝ้าดู process แอปด้วย pidof — แอปตาย/หลุด จะสั่งเปิดเกมกลับเอง")
    print("  • อยากเฝ้าแบบละเอียด (presence API) ให้ผูก cookie ทีหลังที่เมนู [4]")
    print("    พอผูก cookie ระบบจะสลับเป็นโหมดเฝ้าเต็มรูปแบบให้อัตโนมัติ")
    print(bar)

def tut_ck():
    bar = ac("─" * 64, GRAY)
    print(bar)
    print(ac("  บทเรียน: หา cookie (.ROBLOSECURITY)", CYAN))
    print(bar)
    print(ac("  วิธีที่ 1 — มือถือ (Kiwi Browser):", GREEN))
    print("   1. ติดตั้ง Kiwi Browser → เพิ่มส่วนขยาย 'Cookie-Editor'")
    print("   2. เข้า roblox.com ล็อกอิน → แตะส่วนขยาย → ค้น .ROBLOSECURITY → Copy")
    print(ac("  วิธีที่ 2 — PC:", GREEN))
    print("   1. เปิด roblox.com ล็อกอิน → F12 → Application → Cookies")
    print("   2. คัดลอกค่า .ROBLOSECURITY (ขึ้นต้นด้วย _|WARNING:...)")
    print(ac("  วิธีที่ 3 — ไฟล์หลายไอดี (ดีที่สุดสำหรับมัลติบ็อกซ์):", GREEN))
    print("   1. วาง cookie ลงไฟล์ บรรทัดละตัว เช่น /sdcard/Download/cookies.txt")
    print("      เติมชื่อนำหน้าได้:  Farm1|_|WARNING:...")
    print("   2. ใช้เมนู [b] ดึงทั้งไฟล์เข้าสคริปต์ แล้วเลือกผูกแอปแบบหมุนเวียน")
    print(bar)

# ---------- เฮดเดอร์เมนู + จัดการบัญชี ----------
def menu_header(cfg):
    n_acc = len(cfg["accounts"])
    n_app = len(cfg["apps"])
    n_scr = len(list_scripts()) if os.path.isdir(SCRIPTS_D) else 0
    placed = sum(1 for a in cfg["accounts"] if a.get("place_id"))
    hops = sum(1 for a in cfg["accounts"] if a.get("hop"))
    wh = ac("✔ live", GREEN) if cfg.get("webhook") else ac("✘ ยังไม่ตั้ง", RED)
    eco = ac("🍃 ECO", GREEN) if ECO["on"] else ac("⚡ ปกติ", GRAY)
    bar = ac("─" * 62, GRAY)
    print(bar)
    print(f"  บัญชี {ac(str(n_acc), CYAN)} · แอป {ac(str(n_app), CYAN)} · script {ac(str(n_scr), CYAN)} · "
          f"ตั้งแมพ {ac(f'{placed}/{n_acc}', GREEN)} · hop {ac(f'{hops}/{n_acc}', MAGENTA)} · "
          f"webhook {wh} · {eco}")
    print(bar)

def manage_one(cfg, acc):
    while True:
        app = next((a for a in cfg["apps"] if a.get("num") == acc.get("app_num")), None)
        apptxt = f"#{app['num']} {app['name']}" if app else ac("ยังไม่ผูก", GRAY)
        hop = ac("ON", MAGENTA) if acc.get("hop") else ac("off", GRAY)
        print(f"\n  ▸ {ac(acc.get('label','?'), CYAN)} | แอป {apptxt} | hop {hop} | place {acc.get('place_id') or '-'}")
        print("  [1] แก้ชื่อ   [2] ผูก/เปลี่ยนแอป   [3] สลับ server hop")
        print("  [4] เปลี่ยน cookie   [5] ลบบัญชีนี้   [0] กลับ")
        s = input("[?] เลือก: ").strip()
        if s == "0":
            return
        elif s == "1":
            nm = input(f"[?] ชื่อใหม่ ({acc['label']}): ").strip()
            if not nm:
                continue
            if any(a is not acc and a.get("label") == nm for a in cfg["accounts"]):
                print("[!] ชื่อนี้ซ้ำกับบัญชีอื่น")
                continue
            old = acc["label"]
            acc["label"] = nm
            if old in STATES: STATES[nm] = STATES.pop(old)   # state ไม่ค้าง
            if old in THREADS: THREADS[nm] = THREADS.pop(old)
            save_cfg(cfg)
            print("[OK]")
        elif s == "2":
            an = pick_app(cfg, "[?] เลือกแอป #(เลข, Enter เพื่อถอดการผูก): ")
            acc["app_num"] = an
            save_cfg(cfg)
            print("[OK]")
        elif s == "3":
            acc["hop"] = not acc.get("hop", False)
            save_cfg(cfg)
            print(f"[OK] hop = {'ON' if acc['hop'] else 'off'}")
        elif s == "4":
            raw = input("[?] วาง cookie ใหม่: ").strip().strip('"').strip("'")
            ck = extract_cookie(raw) or raw
            me = whoami(ck)
            if not me:
                print("[!] cookie ใช้ไม่ได้")
                continue
            acc["cookie"] = ck
            save_cfg(cfg)
            print(f"[OK] เปลี่ยน cookie แล้ว ({me['name']})")
        elif s == "5":
            if input(f"[?] ยืนยันลบ {acc['label']}? (y/n): ").strip().lower() == "y":
                tag = acc.get("label", "")
                cfg["accounts"].remove(acc)
                STATES.pop(tag, None)
                THREADS.pop(tag, None)
                save_cfg(cfg)
                print("[OK] ลบแล้ว")
                return

def manage_accounts(cfg):
    while True:
        print()
        show_accounts(cfg)
        if not cfg["accounts"]:
            return
        print("\n  [n] พิมพ์เลขเพื่อจัดการบัญชีนั้น · [d] ลบทั้งหมด · [0] กลับ")
        s = input("[?] เลือก: ").strip().lower()
        if s == "0":
            return
        if s == "d":
            if input("[?] ยืนยันลบบัญชีทั้งหมด? (y/n): ").strip().lower() == "y":
                cfg["accounts"].clear()
                STATES.clear()
                THREADS.clear()
                save_cfg(cfg)
                print("[OK] ลบหมดแล้ว")
            continue
        if s.isdigit() and 1 <= int(s) <= len(cfg["accounts"]):
            manage_one(cfg, cfg["accounts"][int(s) - 1])

# ---------- android ----------
def pm_candidates():
    try:
        r = subprocess.run(["pm", "list", "packages"], capture_output=True, text=True)
        return sorted(p.replace("package:", "").strip()
                      for p in r.stdout.splitlines() if "roblox" in p.lower())
    except Exception: return []

def launch(app, place_id, job_id=None):
    u1 = f"roblox://placeID={place_id}" + (f"&gameInstanceId={job_id}" if job_id else "")
    u2 = f"https://www.roblox.com/games/start?placeId={place_id}" + (f"&gameInstanceId={job_id}" if job_id else "")
    tries = []
    if app and app.get("package"):
        tries.append(["am", "start", "-p", app["package"], "-a", "android.intent.action.VIEW", "-d", u1])
    tries.append(["am", "start", "-a", "android.intent.action.VIEW", "-d", u1])
    tries.append(["am", "start", "-a", "android.intent.action.VIEW", "-d", u2])
    for t in tries:
        r = subprocess.run(t, capture_output=True, text=True)
        if "error" not in (r.stdout + r.stderr).lower():
            return True, t[-1]
    return False, u1

def launch_app(pkg):
    """เปิดแอปอย่างเดียว (ยังไม่ทราบแมพ) — ใช้ในโหมดบัญชีไม่มี cookie"""
    for t in (["am", "start", "-p", pkg, "-a", "android.intent.action.MAIN"],
              ["monkey", "-p", pkg, "1"]):
        try:
            r = subprocess.run(t, capture_output=True, text=True, timeout=10)
            if r.returncode == 0 and "error" not in (r.stdout + r.stderr).lower():
                return True
        except Exception:
            pass
    return False

def app_is_running(pkg):
    """เช็กว่าแอปยังมี process รันอยู่ไหม (pidof)"""
    if not pkg:
        return True
    try:
        r = subprocess.run(["pidof", pkg], capture_output=True, text=True, timeout=5)
        return bool(r.stdout.strip())
    except Exception:
        return True

def watch_passive(acc, cfg, tcolor, quick=False):
    """โหมดบัญชีไม่มี cookie — ผู้ใช้ล็อกอินไว้ในแอปแล้ว (ใช้คู่กับเมนู [q])
    เฝ้าดู process แอปด้วย pidof · แอปตาย/หลุด → สั่งเปิดเกมกลับอัตโนมัติ
    ถ้าภายหลังผูก cookie ที่เมนู [4] ระบบจะสลับเป็นโหมดเฝ้าแบบ presence ทันที"""
    tag = acc.get("label", "acct")
    app = next((a for a in cfg.get("apps", []) if a.get("num") == acc.get("app_num")), None)
    pkg = (app or {}).get("package") or "com.roblox.client"
    place = acc.get("place_id")
    apptxt = f"แอป #{app['num']} ({app.get('name','')})" if app else pkg
    set_state(tag, state="WATCH", app=app or {"num": "-", "name": pkg},
              place=place or "-", job="app-mode", rejoins=0, hops=0,
              in_ts=0.0, start=time.time(), universe=None, color=tcolor)
    dlog(tag, f"โหมดแอป (ไม่มี cookie) → {apptxt} — เฝ้าดู process แอป", "info")
    if not place:
        dlog(tag, "ยังไม่มีแมพ — ตั้งที่เมนู [5] หรือเข้าเกมเองก่อน", "dim")
    last_t = time.time()
    while not stop.is_set():
        info = THREADS.get(tag)
        if info:
            info["hb"] = time.time()
        if os.path.exists(STOPF):
            dlog(tag, "เจอไฟล์ STOP — หยุด", "warn")
            stop.set(); break
        if acc.get("cookie"):
            dlog(tag, "พบ cookie ใหม่ — สลับเป็นโหมดเฝ้าแบบ presence", "ok")
            t = threading.Thread(target=watch, args=(acc, cfg, tcolor, quick), daemon=True)
            t.start()
            return
        now = time.time(); dt = now - last_t; last_t = now
        with slock:
            st = STATES[tag]
            if st.get("state") == "WATCH":
                st["in_ts"] = st.get("in_ts", 0) + dt
        if not app_is_running(pkg):
            set_state(tag, state="REJOIN")
            dlog(tag, f"แอปไม่รัน — สั่งเปิดกลับ ({pkg})", "warn")
            ok = launch(app, place, None)[0] if place else launch_app(pkg)
            time.sleep(GRACE)
            if ok and app_is_running(pkg):
                TOTALS["rejoins"] += 1
                set_state(tag, state="WATCH")
                dlog(tag, "เปิดแอปกลับสำเร็จ", "ok")
            else:
                set_state(tag, state="COOLDOWN")
                dlog(tag, f"สั่งเปิดไม่ติด — พัก {BACKOFF//60} นาที", "err")
                notify(cfg, tag, f"{tag}: เปิดแอปไม่สำเร็จ", pkg, 0xe74c3c)
                time.sleep(BACKOFF)
                continue
        time.sleep(poll_interval() + random.uniform(0, 2 if ECO["on"] else 5))

# ---------- core ----------
def poll_interval():
    return ECO_POLL if ECO["on"] else POLL

def set_state(tag, **kw):
    with slock:
        STATES.setdefault(tag, {}).update(kw)

def rejoin(acc, app, place, job, tag):
    st = STATES[tag]
    for a in range(1, RETRY + 1):
        j = job if a == 1 else None
        ok, uri = launch(app, place, j)
        apptxt = f"แอป #{app['num']} ({app.get('name','')})" if app else "Roblox"
        dlog(tag, f"เปิดเกมด้วย{apptxt}: {uri}", "info")
        if not ok:
            dlog(tag, "am start ไม่ติด — ลองลิงก์สำรอง", "warn")
        time.sleep(GRACE)
        p = presence(acc["_uid"], acc["cookie"], acc["_s"])
        if p and p.get("userPresenceType") == IN_GAME:
            TOTALS["rejoins"] += 1
            set_state(tag, state="WATCH")
            dlog(tag, "กลับเข้าเกมแล้ว", "ok")
            return True, p.get("placeId") or place, p.get("gameId"), p.get("universeId")
        dlog(tag, f"ยังไม่เข้า (ลอง {a}/{RETRY})", "warn")
        time.sleep(RETRY_DELAY)

    if acc.get("hop") and st.get("universe"):
        srv = pick_server(st["universe"])
        if srv:
            TOTALS["hops"] += 1
            set_state(tag, state="HOP")
            dlog(tag, f"rejoin ไม่สำเร็จ → hop ไปเซิร์ฟใหม่ job {srv[:8]}..", "warn")
            notify(acc["_cfg"], tag, f"{tag}: hop เซิร์ฟใหม่", f"place {place}", 0x3498db)
            ok, uri = launch(app, place, srv)
            time.sleep(GRACE)
            p = presence(acc["_uid"], acc["cookie"], acc["_s"])
            if p and p.get("userPresenceType") == IN_GAME:
                TOTALS["rejoins"] += 1
                set_state(tag, state="WATCH")
                dlog(tag, "hop สำเร็จ กลับเข้าเกมแล้ว", "ok")
                return True, place, srv, st["universe"]

    set_state(tag, state="COOLDOWN")
    dlog(tag, f"rejoin ไม่สำเร็จ — พัก {BACKOFF//60} นาที", "err")
    notify(acc["_cfg"], tag, f"{tag}: rejoin ไม่สำเร็จ", f"place {place} —  cooldown 5 นาที", 0xe74c3c)
    time.sleep(BACKOFF)
    return False, place, job, st.get("universe")

def watch(acc, cfg, tcolor, quick=False):
    tag = acc.get("label", "acct")
    acc["_cfg"] = cfg
    if not acc.get("cookie"):
        watch_passive(acc, cfg, tcolor, quick)   # ผู้ใช้ล็อกอินในแอปแล้ว — ไม่ต้องใช้ cookie
        return
    acc["_s"] = new_session()          # session แยกของบัญชีนี้โดยเฉพาะ
    app = next((a for a in cfg.get("apps", []) if a.get("num") == acc.get("app_num")), None)
    me = whoami(acc["cookie"], acc["_s"])
    if not me:
        set_state(tag, state="DEAD")
        dlog(tag, "cookie ใช้ไม่ได้/หมดอายุ — ข้าม", "err")
        notify(cfg, tag, f"{tag}: cookie หมดอายุ", "ต้อง login ใหม่", 0xe74c3c)
        return
    acc["_uid"] = me["id"]
    set_state(tag, state="WATCH", app=app, place=acc.get("place_id") or "-",
              job="-", rejoins=0, hops=0, in_ts=0.0, start=time.time(),
              universe=None, color=tcolor)
    place = acc.get("place_id")
    job = None
    app_txt = f"→ แอป #{app['num']} ({app.get('name','')})" if app else ""
    dlog(tag, f"เฝ้าดู {me['name']} (uid {me['id']}) {app_txt}", "info")

    p = presence(acc["_uid"], acc["cookie"], acc["_s"])
    if place and (not p or p.get("userPresenceType") != IN_GAME):
        dlog(tag, "มีแมพเป้าหมายแต่ยังไม่ในเกม — สั่งเข้าเกมเลย", "info")
        ok, place, job, uni = rejoin(acc, app, place, None, tag)
        set_state(tag, universe=uni)

    last_t = time.time()
    while not stop.is_set():
        info = THREADS.get(tag)
        if info: info["hb"] = time.time()
        if os.path.exists(STOPF):
            dlog(tag, "เจอไฟล์ STOP — หยุด", "warn")
            stop.set(); break
        now = time.time(); dt = now - last_t; last_t = now
        with slock:
            st = STATES[tag]
            if st.get("state") == "WATCH": st["in_ts"] = st.get("in_ts", 0) + dt
        p = presence(acc["_uid"], acc["cookie"], acc["_s"])
        if p is None:
            dlog(tag, "อ่าน presence ไม่ได้ (network/rate-limit)", "warn")
            time.sleep(poll_interval()); continue

        if p.get("userPresenceType") == IN_GAME:
            new_place = p.get("placeId") or p.get("rootPlaceId") or place
            job = p.get("gameId")
            if new_place and new_place != acc.get("place_id"):
                acc["place_id"] = new_place
                throttled_save(cfg)
            place = new_place
            set_state(tag, state="WATCH", place=place, job=str(job)[:8] if job else "-",
                      universe=p.get("universeId"))
        else:
            if not place:
                dlog(tag, "ยังไม่มีแมพเป้าหมาย — เข้าเกมเองครั้งแรกแล้วจะเรียนรู้แมพอัตโนมัติ"
                     if quick else "ยังไม่มีแมพเป้าหมาย — ตั้งที่เมนู [5]", "dim")
            else:
                dlog(tag, "หลุดจากเกม! rejoin", "warn")
                ok, place, job, uni = rejoin(acc, app, place, job, tag)
                set_state(tag, universe=uni)
        time.sleep(poll_interval() + random.uniform(0, 2 if ECO["on"] else 5))

# ---------- supervisor: เฝ้า thread แล้ว restart ให้อัตโนมัติ ----------
def supervisor(cfg):
    while not stop.is_set():
        time.sleep(15)
        for i, acc in enumerate(cfg["accounts"]):
            tag = acc.get("label", f"acct{i}")
            info = THREADS.get(tag)
            if not info:
                continue
            alive = info["t"].is_alive()
            stale = (time.time() - info["hb"]) > poll_interval() * 5
            if alive and not stale:
                continue
            if alive and stale:
                dlog(tag, f"heartbeat ขาดหายเกิน {poll_interval()*5:.0f} วิ — ระวัง network ค้าง", "warn")
                continue
            if info["restarts"] + 1 > 5:
                set_state(tag, state="DEAD")
                notify(cfg, tag, f"{tag}: restart ไม่สำเร็จ", "thread ล้มเหลว 5 ครั้ง — เช็กด้วยตา", 0xe74c3c)
                continue
            info["restarts"] += 1
            dlog(tag, f"thread หยุดทำงาน — restart อัตโนมัติ (#{info['restarts']})", "warn")
            t = threading.Thread(target=watch, args=(acc, cfg, info["color"]), daemon=True)
            info["t"] = t
            info["hb"] = time.time()
            t.start()

# ---------- dashboard (โทนน้ำเงิน) ----------
def vlen(s): return len(re.sub(r"\033\[[0-9;]*m", "", s))
def pad(s, w): return s + " " * max(0, w - vlen(s))
def row(cols, widths): return ac("│ " + " │ ".join(pad(c, w) for c, w in zip(cols, widths)) + " │", BORDER)
def sep(widths, l, m, r): return ac(l + m.join("─" * (w + 2) for w in widths) + r, BORDER)

W = [12, 10, 18, 11, 6, 5, 7]

def fmt_up(sec):
    sec = int(sec)
    if sec < 3600: return f"{sec//60}m{sec%60:02d}s"
    return f"{sec//3600}h{(sec%3600)//60:02d}m"

def dashboard(cfg):
    while not stop.is_set():
        time.sleep(4 if ECO["on"] else 1)
        L = []
        L.append(grad_txt("  ★ STAR PLUS ★", w=18)
                  + ac(f"   v{VERSION}", BORDER)
                  + f"   {time.strftime('%H:%M:%S')}   uptime {fmt_up(time.time()-_session_start)}"
                  + (f"   {ac('🍃ECO', GREEN)}" if ECO["on"] else ""))
        head = [ac("Account", "38;2;120;180;255"), ac("Status", "38;2;120;180;255"),
                ac("App", "38;2;120;180;255"), ac("Place", "38;2;120;180;255"),
                ac("Rejoin", "38;2;120;180;255"), ac("Hop", "38;2;120;180;255"),
                ac("Stable%", "38;2;120;180;255")]
        L.append(sep(W, "┌", "┬", "┐"))
        L.append(row(head, W))
        L.append(sep(W, "├", "┼", "┤"))
        for acc in cfg["accounts"]:
            st = STATES.get(acc.get("label", ""), {})
            col = st.get("color", CYAN)
            state = st.get("state", "INIT")
            app = st.get("app") or {}
            apptxt = f"#{app.get('num','-')} {app.get('name','')[:11]}" if app else "-"
            up = time.time() - st.get("start", time.time())
            stable = (st.get("in_ts", 0) / up * 100) if up > 5 and state != "DEAD" else 0
            L.append(row([
                ac(acc.get("label", "?")[:12], col),
                ac(state, ST_COLOR.get(state, GRAY)),
                apptxt[:18],
                str(st.get("place", "-"))[:11],
                str(st.get("rejoins", 0)),
                str(st.get("hops", 0)),
                f"{stable:4.0f}%"], W))
        L.append(sep(W, "└", "┴", "┘"))
        L.append(f"  rejoin รวม {ac(str(TOTALS['rejoins']), GREEN)} · hop {ac(str(TOTALS['hops']), MAGENTA)} · แจ้งเตือน {ac(str(TOTALS['alerts']), YELLOW)}   (หยุด: Ctrl+C / ไฟล์ STOP)")
        L.append(ac("  📡 ข้อความ Live Dashboard บน Discord อัปเดตเองทุก 30 วิ", BORDER))
        L.append("")
        for ts, sym, sc, tag, tc, msg in list(LOGQ)[-7:]:
            L.append(f"{ac(ts, GRAY)} {ac(sym, sc)} {ac(tag, tc)} {msg}")
        with slock:
            sys.stdout.write("\033[H\033[2J" + "\n".join(L) + "\n")
            sys.stdout.flush()

# ---------- เริ่มเฝ้าดู (ใช้ร่วมกันระหว่าง [7] กับ [q]) ----------
def spawn_watch(cfg, acc, i, quick=False):
    tag = acc.get("label", f"acct{i}")
    color = PALETTE[i % len(PALETTE)]
    t = threading.Thread(target=watch, args=(acc, cfg, color, quick), daemon=True)
    THREADS[tag] = {"t": t, "hb": time.time(), "restarts": 0, "color": color}
    t.start()

def start_watching(cfg, quick=False):
    global _session_start
    if os.path.exists(STOPF):
        os.remove(STOPF)
    _session_start = time.time()
    _last_report["t"] = time.time()
    if cfg.get("delta_autosync", True):
        sync_delta_autoexec(cfg, quiet=True)   # push สคริปต์ลง autoexec ของ Delta ก่อนเริ่มเฝ้าดู
    for i, a in enumerate(cfg["accounts"]):
        set_state(a.get("label", f"acct{i}"), state="INIT", color=PALETTE[i % len(PALETTE)])
    if quick:
        print(ac("[*] โหมด Start Rejoin — สำหรับผู้ใช้ที่ล็อกอินในเกมแล้ว", CYAN))
        print(ac("    ไม่ต้องล็อกอินผ่าน UI อีก · ระบบเฝ้าดูแล rejoin ให้อัตโนมัติ", GRAY))
        print(ac("    บัญชีที่ยังไม่มีแมพจะรอจนกว่าจะเข้าเกมเอง แล้วเรียนรู้แมพให้อัตโนมัติ", GRAY))
    print(ac("[*] แนะนำหมุนจอแนวนอน — กด Ctrl+C หรือแตะไฟล์ STOP เพื่อหยุด", GRAY))
    loading_screen("STARTING", "กำลังสตาร์ท watcher", secs=min(2.0, 0.6 + 0.4 * len(cfg["accounts"])))
    DASH["on"] = True
    time.sleep(1)
    ts = []
    for i, a in enumerate(cfg["accounts"]):
        spawn_watch(cfg, a, i, quick)
        ts.append(THREADS[a.get("label", f"acct{i}")]["t"])
        time.sleep(5 if ECO["on"] else 3)
    for fn, args in ((dashboard, (cfg,)), (report_loop, (cfg,)),
                     (live_loop, (cfg,)), (supervisor, (cfg,))):
        d = threading.Thread(target=fn, args=args, daemon=True)
        d.start()
        ts.append(d)
    try:
        while any(t.is_alive() for t in ts) and not stop.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop.set()
    DASH["on"] = False
    save_totals()
    print("\n" + ac(f"[*] จบเซสชัน — rejoin {TOTALS['rejoins']} · hop {TOTALS['hops']} · alert {TOTALS['alerts']}", CYAN))
    print(ac("    STAR Plus · discord.gg/kYDu7qth", MAGENTA))
    stop.clear()
    THREADS.clear()
    for st in STATES.values():
        st["start"] = time.time()
        st["in_ts"] = 0

# ---------- Autoexec Script สำหรับ Delta Executor (v4.2) ----------
def ensure_scripts_dir():
    os.makedirs(SCRIPTS_D, exist_ok=True)
    return SCRIPTS_D

def find_delta_autoexec():
    """หาโฟลเดอร์ autoexec ของ Delta — คืนพาธแรกที่เจอ หรือ None"""
    for p in DELTA_AUTOEXEC_CANDIDATES:
        if os.path.isdir(p):
            return p
    return None

def list_scripts():
    ensure_scripts_dir()
    return sorted(f for f in os.listdir(SCRIPTS_D) if f.endswith((".lua", ".txt")))

def _script_stats(name):
    fp = os.path.join(SCRIPTS_D, name)
    sz = os.path.getsize(fp)
    mt = time.strftime("%m-%d %H:%M", time.localtime(os.path.getmtime(fp)))
    return sz, mt

def add_script_from_paste():
    """วางโค้ด Lua ทีละบรรทัด (พิมพ์ . บนบรรทัดเดียวเพื่อจบ) แล้วเซฟเป็นชื่อที่ตั้ง"""
    name = input("[?] ชื่อสคริปต์ (ภาษาอังกฤษ/ตัวเลข/ _ - เท่านั้น): ").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", name or ""):
        print(ac("[!] ชื่อไม่ถูกต้อง — ใช้ a-z 0-9 _ - ความยาว ≤40", RED))
        return
    fn = name + ".lua"
    if os.path.exists(os.path.join(SCRIPTS_D, fn)):
        print(ac("[!] มีสคริปต์ชื่อนี้อยู่แล้ว — ลบก่อนหรือตั้งชื่อใหม่", YELLOW))
        return
    print(ac("  วางโค้ดได้เลย (ทีละบรรทัด) — พิมพ์ . บนบรรทัดเดียวเพื่อจบ", GRAY))
    lines = []
    while True:
        try:
            ln = input()
        except EOFError:
            break
        if ln.strip() == ".":
            break
        lines.append(ln)
    if not lines:
        print("[!] ยังไม่ได้วางโค้ด — ยกเลิก")
        return
    ensure_scripts_dir()
    with open(os.path.join(SCRIPTS_D, fn), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(ac(f"[OK] เซฟ {fn} แล้ว ({len(lines)} บรรทัด)", GREEN))

def import_script():
    p = input("[?] พาธไฟล์สคริปต์ (เช่น /sdcard/Download/farm.lua): ").strip().strip('"').strip("'")
    if not os.path.isfile(p):
        print("[!] ไม่เจอไฟล์ — เช็กพาธ (อย่าลืม termux-setup-storage)")
        return
    base = os.path.basename(p)
    if not base.endswith((".lua", ".txt")):
        base += ".lua"
    dst = os.path.join(ensure_scripts_dir(), base)
    if os.path.exists(dst):
        stem, ext = os.path.splitext(base)
        n = 2
        while os.path.exists(os.path.join(SCRIPTS_D, f"{stem}_{n}{ext}")):
            n += 1
        dst = os.path.join(SCRIPTS_D, f"{stem}_{n}{ext}")
    try:
        with open(p, encoding="utf-8", errors="ignore") as f1, open(dst, "w", encoding="utf-8") as f2:
            f2.write(f1.read())
        print(ac(f"[OK] นำเข้าแล้ว → {os.path.basename(dst)}", GREEN))
    except Exception as e:
        print(ac(f"[!] อ่าน/เขียนไฟล์ไม่สำเร็จ: {e}", RED))

def view_or_delete_script(cfg, name):
    print(f"\n  ▸ {ac(name, CYAN)}  ({_script_stats(name)[0]} bytes · แก้ไข {_script_stats(name)[1]})")
    s = input("[?] v=ดูเนื้อหา (25 บรรทัดแรก) · d=ลบ · Enter=กลับ: ").strip().lower()
    fp = os.path.join(SCRIPTS_D, name)
    if s == "v":
        try:
            with open(fp, encoding="utf-8", errors="ignore") as f:
                for i, ln in enumerate(f):
                    if i >= 25:
                        print(ac("  ... (แสดงแค่ 25 บรรทัดแรก)", GRAY))
                        break
                    print("  " + ln.rstrip())
        except Exception:
            pass
        input("[Enter เพื่อกลับ]")
    elif s == "d":
        if input(f"[?] ยืนยันลบ {name}? (y/n): ").strip().lower() == "y":
            try:
                os.remove(fp)
            except Exception:
                pass
            for ac_ in cfg["accounts"]:
                if ac_.get("delta_script") == name:
                    ac_["delta_script"] = None
            save_cfg(cfg)
            print("[OK] ลบแล้ว (บัญชีที่ผูกไว้ถูกถอดให้อัตโนมัติ)")

# ---------- manifest ไฟล์ที่เคย push ลง autoexec (เพื่อเคลียร์ของเก่าให้ถูก) ----------
def load_manifest():
    if os.path.exists(DELTA_MANIFEST):
        try:
            with open(DELTA_MANIFEST) as f:
                d = json.load(f)
            if isinstance(d, dict):
                return d
        except Exception:
            pass
    return {"pushed": []}

def save_manifest(m):
    try:
        with open(DELTA_MANIFEST, "w") as f:
            json.dump(m, f)
    except Exception:
        pass

def sync_delta_autoexec(cfg, quiet=False):
    """push สคริปต์ที่ผูกกับบัญชีลงโฟลเดอร์ autoexec ของ Delta
    1) ลบไฟล์ที่ push ไว้ครั้งก่อน (อ่านจาก manifest)  2) copy สคริปต์ปัจจุบันลงไปใหม่
    → รับประกันว่า autoexec มีเฉพาะสคริปต์ของบัญชีที่กำลังเฝ้าดูจริง ๆ"""
    target = find_delta_autoexec()
    if not target:
        if not quiet:
            print(ac("[!] หาโฟลเดอร์ autoexec ของ Delta ไม่เจอ", RED))
            print(ac("    เปิด Delta สักครั้งเพื่อให้มันสร้างโฟลเดอร์ แล้วลอง [a] อีกที", GRAY))
        return 0
    manifest = load_manifest()
    removed = 0
    for f in manifest.get("pushed", []):
        fp = os.path.join(target, f)
        try:
            if os.path.exists(fp):
                os.remove(fp)
                removed += 1
        except Exception:
            pass
    pushed, n = [], 0
    for acc in cfg["accounts"]:
        s = acc.get("delta_script")
        if not s:
            continue
        srcf = os.path.join(SCRIPTS_D, s)
        if not os.path.exists(srcf):
            continue
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", acc.get("label", "acct"))[:24]
        dst_name = f"starplus_{safe}.lua"
        try:
            with open(srcf, encoding="utf-8", errors="ignore") as f1, \
                 open(os.path.join(target, dst_name), "w", encoding="utf-8") as f2:
                f2.write(f1.read())
            pushed.append(dst_name)
            n += 1
        except Exception:
            pass
    manifest["pushed"] = pushed
    save_manifest(manifest)
    if not quiet:
        print(ac(f"[OK] sync แล้ว — เคลียร์ของเก่า {removed} · push ใหม่ {n} สคริปต์ → {target}", GREEN))
    return n

def delta_script_menu(cfg):
    while True:
        target = find_delta_autoexec()
        ttxt = ac(target, GREEN) if target else ac("ไม่เจอ (เปิด Delta สักครั้งก่อน)", RED)
        auto = ac("ON", GREEN) if cfg.get("delta_autosync", True) else ac("off", GRAY)
        print(f"\n  ▸ autoexec ของ Delta: {ttxt}")
        print(f"    คลังสคริปต์: {SCRIPTS_D}  ·  auto-sync ตอน START: {auto}")
        print("  [a] ตรวจหาโฟลเดอร์ autoexec อีกครั้ง")
        print("  [b] เพิ่มสคริปต์ใหม่ (วางโค้ด)")
        print("  [c] นำเข้าสคริปต์จากไฟล์")
        print("  [d] รายชื่อสคริปต์ / ดู / ลบ")
        print("  [e] ผูกสคริปต์กับบัญชี")
        print("  [f] sync ลง autoexec ตอนนี้")
        print("  [g] สลับ auto-sync ตอน START")
        print("  [0] กลับ")
        c = input("[?] เลือก: ").strip().lower()
        if c == "0":
            return
        elif c == "a":
            t = find_delta_autoexec()
            if t:
                print(ac(f"[OK] เจอ: {t}", GREEN))
            else:
                print(ac("[!] ยังไม่เจอ — เปิด Delta รอสักพักให้สร้างโฟลเดอร์ก่อน", RED))
        elif c == "b":
            add_script_from_paste()
        elif c == "c":
            import_script()
        elif c == "d":
            scs = list_scripts()
            if not scs:
                print("  (ยังไม่มีสคริปต์)")
                continue
            for i, s in enumerate(scs, 1):
                sz, mt = _script_stats(s)
                bound = [a.get("label") for a in cfg["accounts"] if a.get("delta_script") == s]
                btxt = ac(f" ← ผูกกับ: {', '.join(bound)}", MAGENTA) if bound else ""
                print(f"  [{i}] {s} ({sz}B · {mt}){btxt}")
            s = input("[?] พิมพ์เลขเพื่อจัดการ (Enter กลับ): ").strip()
            if s.isdigit() and 1 <= int(s) <= len(scs):
                view_or_delete_script(cfg, scs[int(s) - 1])
        elif c == "e":
            if not cfg["accounts"]:
                print("  (ยังไม่มีบัญชี — เพิ่มที่เมนู [1]/[2] ก่อน)")
                continue
            show_accounts(cfg)
            i = input("[?] เลือกบัญชี (เลข): ").strip()
            if not (i.isdigit() and 1 <= int(i) <= len(cfg["accounts"])):
                continue
            acc = cfg["accounts"][int(i) - 1]
            scs = list_scripts()
            if not scs:
                print("  (ยังไม่มีสคริปต์ — สร้างที่ [b]/[c] ก่อน)")
                continue
            for j, s in enumerate(scs, 1):
                mark = ac(" ✔", GREEN) if acc.get("delta_script") == s else ""
                print(f"  [{j}] {s}{mark}")
            j = input(f"[?] เลือกสคริปต์ให้ {acc.get('label')} (เลข, Enter=ถอดการผูก): ").strip()
            if not j:
                acc["delta_script"] = None
                save_cfg(cfg)
                print("[OK] ถอดการผูกแล้ว")
            elif j.isdigit() and 1 <= int(j) <= len(scs):
                acc["delta_script"] = scs[int(j) - 1]
                save_cfg(cfg)
                print(ac(f"[OK] {acc.get('label')} → {scs[int(j)-1]}", GREEN))
        elif c == "f":
            sync_delta_autoexec(cfg)
            input("[Enter เพื่อกลับ]")
        elif c == "g":
            cfg["delta_autosync"] = not cfg.get("delta_autosync", True)
            save_cfg(cfg)
            print(ac(f"[OK] auto-sync ตอน START = {'ON' if cfg['delta_autosync'] else 'off'}",
                     GREEN if cfg["delta_autosync"] else CYAN))

# ---------- UI ----------
_BANNER_ANIMATED = {"done": False}

STAR_PLUS_ART = [
    "  ███████╗████████╗ █████╗ ██████╗",
    "  ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗",
    "  ███████╗   ██║   ███████║██████╔╝",
    "  ╚════██║   ██║   ██╔══██║██╔══██╗",
    "  ███████║   ██║   ██║  ██║██║  ██║",
    "  ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝",
    "  ██████╗ ██╗     ██╗   ██╗███████╗",
    "  ██╔══██╗██║     ██║   ██║██╔════╝",
    "  ██████╔╝██║     ██║   ██║███████╗",
    "  ██╔═══╝ ██║     ██║   ██║╚════██║",
    "  ██║     ███████╗╚██████╔╝███████║",
    "  ╚═╝     ╚══════╝ ╚═════╝ ╚══════╝",
]

def banner():
    """banner STAR Plus — แอนิเมชันเปิดตัวครั้งแรก (ไล่เส้นทีละเส้น + shimmer)"""
    if COLORS_ON and not _BANNER_ANIMATED["done"]:
        for ln in STAR_PLUS_ART:                 # ไล่ความสว่างทีละบรรทัด
            print(grad_txt(ln, w=len(ln)))
            time.sleep(0.05)
        shimmer = "  ── ✦ ──  S T A R   P L U S  ── ✦ ──"
        for i in range(1, len(shimmer) + 1):     # เอฟเฟกต์ shimmer วิ่งผ่าน
            sys.stdout.write("\r" + grad_txt(shimmer[:i], len(shimmer)))
            sys.stdout.flush()
            time.sleep(0.008)
        sys.stdout.write("\r" + grad_txt(shimmer, len(shimmer)) + "\n")
        _BANNER_ANIMATED["done"] = True
    else:
        for ln in STAR_PLUS_ART:
            print(grad_txt(ln, w=len(ln)))
    print(ac(f"   ★ STAR PLUS ★ multi-account auto rejoin · termux · v{VERSION}", GRAY))
    print(ac("   discord: https://discord.gg/kYDu7qth\n", MAGENTA))

def show_apps(cfg):
    if not cfg["apps"]: print("  (ยังไม่มีแอป)")
    for a in cfg["apps"]:
        print(f"  [#{a['num']}] {a.get('name','')} — {a.get('package','(ไม่มี package)')}")

def show_accounts(cfg):
    if not cfg["accounts"]: print("  (ยังไม่มีบัญชี)")
    for i, ac_ in enumerate(cfg["accounts"], 1):
        app = next((a for a in cfg["apps"] if a.get("num") == ac_.get("app_num")), None)
        at = f"→ แอป #{app['num']} {app.get('name','')}" if app else "→ ยังไม่ผูกแอป"
        hop = "hop:ON" if ac_.get("hop") else "hop:off"
        dsc = f" | δ:{ac_.get('delta_script')}" if ac_.get("delta_script") else ""
        print(f"  [{i}] {ac_.get('label','?')} | place {ac_.get('place_id') or '-'} | {at} | {hop}{dsc}")

def pick_account(cfg):
    show_accounts(cfg)
    if not cfg["accounts"]: return None
    i = input("[?] เลือกบัญชี (เลข): ").strip()
    return cfg["accounts"][int(i)-1] if i.isdigit() and 1 <= int(i) <= len(cfg["accounts"]) else None

def main():
    global _session_start
    if len(sys.argv) > 1 and sys.argv[1].lower() == "admin":
        admin_console()
        return
    load_totals()
    load_hookstate()
    cfg = load_cfg()
    loading_screen("STAR PLUS", "กำลังเปิดระบบ", secs=1.2)
    if not key_gate():
        sys.exit(0)
    threading.Thread(target=key_guard, daemon=True).start()   # คีย์มีผลแบบเรียลไทม์
    while True:
        banner()
        menu_header(cfg)
        items = [
            ("1", "เพิ่มบัญชีด้วย Uss/Pss",            "มีบทเรียนในตัว"),
            ("2", "เพิ่มบัญชีด้วย Cookie",             "วางทีละตัว · ไฟล์ · หลายไอดีพร้อมกัน"),
            ("3", "จัดการแอป",                        "สแกน → กด Enter ใช้ชื่ออัตโนมัติ"),
            ("4", "จัดการบัญชี",                      "แก้ชื่อ · ผูกแอป · เปลี่ยน cookie · ลบ"),
            ("5", "ตั้งแมพ · จอยเพื่อน · server hop", ""),
            ("6", "Webhook + แจ้งเตือน",              "ต่อ Live Dashboard บน Discord"),
            ("x", "Autoexec Script (Delta)",              "ผูกสคริปต์กับไอดี · sync อัตโนมัติ"),
            ("7", ac("START (live dashboard)", GREEN), ""),
            ("q", ac("Start Rejoin (เล่นอยู่แล้ว)", BLUE), "ล็อกอินในเกมแล้ว ไม่ต้องล็อกอินผ่าน UI"),
            ("e", "🍃 สลับโหมดประหยัดแบต+RAM",          ""),
            ("8", "เช็กสถานะบัญชี",                   ""),
            ("9", "ทดสอบเปิดเกม",                     ""),
            ("k", "ข้อมูลคีย์ / ล็อกเอาต์",              ""),
            ("s", "สถิติ / backup config",            ""),
            ("0", "ออก / ลบ config",                  ""),
        ]
        print()
        for k, t, d in items:
            dt = ac(f"   ← {d}", GRAY) if d else ""
            print(f"  [{ac(k, CYAN)}] {t}{dt}")
        c = input("\n[?] เลือก: ").strip().lower()

        # ---------- [1] Uss/Pss (เพิ่มไว้ล็อกอินเอง — ไม่ต้องผ่าน API) ----------
        if c == "1":
            tut_up()
            if input("[?] เพิ่มบัญชีเลยไหม (y/n): ").strip().lower() != "y":
                continue
            while True:
                u = input("[?] Username (Enter เพื่อกลับเมนู): ").strip()
                if not u:
                    break
                if any(a.get("label") == u for a in cfg["accounts"]):
                    print(ac(f"[!] {u}: มีบัญชีชื่อนี้อยู่แล้ว", YELLOW))
                    continue
                pid = input("[?] place id (Enter = ยังไม่ใส่ ตั้งทีหลังที่เมนู [5]): ").strip()
                place = int(pid) if pid.isdigit() else None
                an = pick_app(cfg, "[?] ผูกแอป #(เลข, Enter = ใช้แอปหลัก): ")
                cfg["accounts"].append({"label": u, "cookie": None,
                                        "place_id": place, "app_num": an, "hop": False})
                save_cfg(cfg)
                print(ac(f"[OK] เพิ่ม {u} แล้ว — ไม่ต้องล็อกอินผ่านสคริปต์ (ไม่มี 2FA/captcha)", GREEN))
                print(ac("     ล็อกอินไว้ในแอป Roblox บนเครื่องนี้ แล้วกด [q] เพื่อเริ่มเฝ้าดู", GRAY))

        # ---------- [2] Cookie ----------
        elif c == "2":
            print("  [t] บทเรียน: หา cookie จากเบราว์เซอร์")
            print("  [a] วาง cookie ทีละไอดี")
            print("  [b] ดึงจากไฟล์ในเครื่อง (.txt/.json)")
            print("  [c] วางหลายไอดีพร้อมกัน (ทีละบรรทัด)")
            sub = input("[?] เลือก: ").strip().lower()
            if sub == "t":
                tut_ck()
                input("[Enter เพื่อกลับ]")
            elif sub == "a":
                raw = input("[?] วาง .ROBLOSECURITY cookie: ").strip().strip('"').strip("'")
                ck = extract_cookie(raw) or raw
                if not extract_cookie(ck):
                    print("[!] ดูไม่เหมือน cookie — ลองใหม่ หรือกด [t] ดูบทเรียน")
                    continue
                if any(a.get("cookie") == ck for a in cfg["accounts"]):
                    print("[!] cookie นี้ซ้ำกับบัญชีที่มีอยู่แล้ว")
                    continue
                me = add_account(cfg, None, ck)
                if not me:
                    print("[!] cookie ใช้ไม่ได้ (หมดอายุ/ถูก reset) — ต้องเอาใหม่")
                    continue
                an = pick_app(cfg)
                cfg["accounts"][-1]["app_num"] = an
                save_cfg(cfg)
                print(f"[OK] เพิ่ม {me['name']} แล้ว")
            elif sub == "b":
                path = input("[?] พาธไฟล์ (เช่น /sdcard/Download/cookies.txt): ").strip().strip('"').strip("'")
                if not os.path.isfile(path):
                    print("[!] ไม่เจอไฟล์ — เช็กพาธอีกที (อย่าลืม termux-setup-storage)")
                    continue
                bulk_add(cfg, parse_cookie_file(path))
                input("[Enter เพื่อกลับ]")
            elif sub == "c":
                print("  วางทีละบรรทัด รูปแบบ: label|cookie หรือ cookie ล้วน (ไม่ใส่ label ก็ได้)")
                print("  พิมพ์ . บนบรรทัดเดียวเพื่อจบ")
                lines = []
                while True:
                    try:
                        ln = input()
                    except EOFError:
                        break
                    if ln.strip() == ".":
                        break
                    if ln.strip():
                        lines.append(ln)
                bulk_add(cfg, parse_cookie_text("\n".join(lines)))
                input("[Enter เพื่อกลับ]")

        # ---------- [3] จัดการแอป ----------
        elif c == "3":
            show_apps(cfg)
            print("\n  [a] สแกนหาแอป Roblox (กด Enter ใช้ชื่ออัตโนมัติ)")
            print("  [b] เพิ่มเอง (package name)")
            print("  [r] แก้ชื่อแอป")
            print("  [d] ลบแอป")
            sub = input("[?] เลือก: ").strip().lower()
            if sub == "a":
                found = pm_candidates()
                if not found:
                    print("[!] ไม่เจอแอปที่มีคำว่า roblox — ลองเพิ่มเอง [b]")
                    continue
                for p in found:
                    print("   -", p)
                for p in found:
                    nums = [a["num"] for a in cfg["apps"]] or [0]
                    default = f"Roblox #{max(nums) + 1}"
                    nm = input(f"[?] ตั้งชื่อให้ {p} [{default}]: ").strip() or default
                    cfg["apps"].append({"num": max(nums) + 1, "name": nm, "package": p})
                save_cfg(cfg)
                print("[OK] บันทึกแล้ว")
            elif sub == "b":
                pkg = input("[?] package name (เช่น com.roblox.client): ").strip()
                if not pkg:
                    continue
                nums = [a["num"] for a in cfg["apps"]] or [0]
                default = f"Roblox #{max(nums) + 1}"
                nm = input(f"[?] ชื่อที่แสดง [{default}]: ").strip() or default
                cfg["apps"].append({"num": max(nums) + 1, "name": nm, "package": pkg})
                save_cfg(cfg)
                print("[OK] บันทึกแล้ว")
            elif sub == "r":
                if not cfg["apps"]:
                    print("  (ยังไม่มีแอป)")
                    continue
                s = input("[?] แก้ชื่อแอป #(เลข): ").strip()
                app = next((a for a in cfg["apps"] if str(a["num"]) == s), None)
                if app:
                    nm = input(f"[?] ชื่อใหม่ ({app['name']}): ").strip()
                    if nm:
                        app["name"] = nm
                        save_cfg(cfg)
                        print("[OK]")
            elif sub == "d":
                if not cfg["apps"]:
                    print("  (ยังไม่มีแอป)")
                    continue
                s = input("[?] ลบแอป #(เลข): ").strip()
                app = next((a for a in cfg["apps"] if str(a["num"]) == s), None)
                if app:
                    for ac_ in cfg["accounts"]:
                        if ac_.get("app_num") == app["num"]:
                            ac_["app_num"] = None
                    cfg["apps"].remove(app)
                    save_cfg(cfg)
                    print("[OK] ลบแล้ว (บัญชีที่ผูกไว้ถูกถอดให้อัตโนมัติ)")

        # ---------- [4] จัดการบัญชี ----------
        elif c == "4":
            manage_accounts(cfg)

        # ---------- [5] แมพ / เพื่อน / hop ----------
        elif c == "5":
            acc = pick_account(cfg)
            if not acc:
                continue
            print(f"  ▸ {ac(acc.get('label','?'), CYAN)}")
            print("  [a] ตั้ง place id (แมพที่จะเล่น)")
            print("  [b] จอยเซิฟเพื่อน (พิมพ์ชื่อ user)")
            hop_cur = "ON" if acc.get("hop") else "off"
            print(f"  [c] สลับ server hop (ตอนนี้: {hop_cur})")
            sub = input("[?] เลือก: ").strip().lower()
            if sub == "a":
                pid = input(f"[?] place id (ปัจจุบัน {acc.get('place_id') or '-'}): ").strip()
                if pid.isdigit():
                    uni = place_info(int(pid))
                    acc["place_id"] = int(pid)
                    save_cfg(cfg)
                    print(ac(("[OK]" + (f" (universe {uni})" if uni else " (⚠ ตรวจแมพไม่เจอ — เช็กเลขอีกที)")),
                             GREEN if uni else YELLOW))
                else:
                    print("[!] ตัวเลขเท่านั้น")
            elif sub == "b":
                un = input("[?] ชื่อเพื่อนใน Roblox: ").strip()
                fuid = uid_by_username(un)
                if not fuid:
                    print("[!] หา user ไม่เจอ")
                    continue
                p = presence(fuid)
                if not p or p.get("userPresenceType") != IN_GAME:
                    print(f"[!] {un} ไม่ได้อยู่ในเกม")
                    continue
                place = p.get("placeId") or p.get("rootPlaceId")
                job = p.get("gameId")
                acc["place_id"] = place
                save_cfg(cfg)
                app = next((a for a in cfg["apps"] if a.get("num") == acc.get("app_num")), None)
                ok, uri = launch(app, place, job)
                print(f"[OK] เข้าเซิฟ {un}: place {place} job {str(job)[:8]}..")
                print(f"     {uri} ({'สั่งสำเร็จ' if ok else 'สั่งไม่ติด'})")
            elif sub == "c":
                acc["hop"] = not acc.get("hop", False)
                save_cfg(cfg)
                print(f"[OK] hop = {'ON' if acc['hop'] else 'off'}")

        # ---------- [6] Webhook ----------
        elif c == "6":
            print(f"  webhook ปัจจุบัน: {cfg.get('webhook') or ac('(ยังไม่ตั้ง)', GRAY)}")
            print("  [a] ใส่/แก้ webhook URL")
            print("  [b] ส่งข้อความทดสอบ")
            print("  [c] ตั้งช่วงส่งรายงานสถานะ (นาที)")
            print("  [d] ส่งรายงานตอนนี้ทันที")
            print(ac("  [i] ตอน START ระบบจะสร้าง 'ข้อความ Live Dashboard' แล้วแก้ไขมัน\n"
                     "      ทุก 30 วิ (60 วิในโหมด ECO) เป็นแดชบอร์ดสดบน Discord", GRAY))
            sub = input("[?] เลือก: ").strip().lower()
            if sub == "a":
                cfg["webhook"] = input("[?] Discord webhook URL: ").strip()
                HOOK_STATE["id"] = None
                save_hookstate()
                save_cfg(cfg)
                print("[OK] (เริ่มเฝ้าดูครั้งหน้าจะสร้างข้อความ Live ใหม่)")
            elif sub == "b":
                notify(cfg, "", "STAR Plus test", "แจ้งเตือนทำงานปกติ", 0x2ecc71)
                print("[OK] ส่งแล้ว — เช็ก Discord / แถบแจ้งเตือนเครื่อง")
            elif sub == "c":
                cur = cfg.get("report_min", 60)
                t = input(f"[?] ส่งรายงานทุกกี่นาที (ปัจจุบัน {cur}): ").strip()
                if t.isdigit():
                    cfg["report_min"] = int(t)
                    save_cfg(cfg)
                    print(f"[OK] ส่งรายงานทุก {cfg['report_min']} นาที")
            elif sub == "d":
                send_report(cfg, "ทดสอบรายงาน")
                print("[OK] ส่งรายงานแล้ว — เช็ก Discord")

        # ---------- [7] START ----------
        elif c == "7":
            if not cfg["accounts"]:
                print("[!] เพิ่มบัญชีก่อน (เมนู [1] หรือ [2])")
                continue
            start_watching(cfg, quick=False)

        # ---------- [q] Start Rejoin (เล่นอยู่แล้ว) ----------
        elif c == "q":
            if not cfg["accounts"]:
                print("[!] ยังไม่มีบัญชี — ล็อกอินผ่าน UI ครั้งแรกที่เมนู [1]/[2] ก่อน")
                continue
            start_watching(cfg, quick=True)

        # ---------- [x] Autoexec Script (Delta) ----------
        elif c == "x":
            delta_script_menu(cfg)

        # ---------- [e] ECO ----------
        elif c == "e":
            ECO["on"] = not ECO["on"]
            cfg["eco"] = ECO["on"]
            save_cfg(cfg)
            if ECO["on"]:
                print(ac("[OK] 🍃 ECO ON — poll 45 วิ · จออัปเดตทุก 4 วิ · เหมาะกับปล่อยค้างคืน", GREEN))
            else:
                print(ac("[OK] ⚡ กลับโหมดปกติ", CYAN))

        # ---------- [8] เช็กสถานะ ----------
        elif c == "8":
            if not cfg["accounts"]:
                print("  (ยังไม่มีบัญชี)")
                continue
            for ac_ in cfg["accounts"]:
                if not ac_.get("cookie"):
                    app8 = next((a for a in cfg["apps"] if a.get("num") == ac_.get("app_num")), None)
                    pkg8 = (app8 or {}).get("package") or "com.roblox.client"
                    run8 = ac("รันอยู่ ✔", GREEN) if app_is_running(pkg8) else ac("ไม่รัน ✘", RED)
                    hop8 = ac("hop:ON", MAGENTA) if ac_.get("hop") else ""
                    print(f"  {ac('◆', CYAN)} {ac_.get('label','?'):<14} โหมดแอป (ล็อกอินในเกมแล้ว) · {run8} · place {ac_.get('place_id') or '-'} {hop8}")
                    continue
                me = whoami(ac_["cookie"])
                if not me:
                    print(f"  {ac('✘', RED)} {ac_.get('label','?'):<14} cookie หมดอายุ — ต้อง login ใหม่")
                    continue
                p = presence(me["id"], ac_["cookie"])
                pst = {0: "offline", 1: "online", 2: ac("in-game", GREEN), 3: "studio"}.get(
                    p.get("userPresenceType"), "?") if p else "อ่านไม่ได้"
                extra = ""
                if p and p.get("userPresenceType") == IN_GAME:
                    extra = f" | place {p.get('placeId')} | {p.get('lastLocation','')[:22]}"
                st = STATES.get(ac_.get("label", ""), {})
                if st:
                    extra += f" | rejoin {st.get('rejoins',0)} hop {st.get('hops',0)}"
                hop = ac("hop:ON", MAGENTA) if ac_.get("hop") else ""
                print(f"  {ac('✔', GREEN)} {ac_.get('label','?'):<14} {pst}{extra} {hop}")

        # ---------- [9] ทดสอบเปิดเกม ----------
        elif c == "9":
            acc = pick_account(cfg)
            if not acc:
                continue
            pid = acc.get("place_id")
            if not pid:
                t = input("[?] ยังไม่มี place id — พิมพ์เอง: ").strip()
                pid = int(t) if t.isdigit() else None
            if not pid:
                print("[!] ไม่มี place id")
                continue
            app = next((a for a in cfg["apps"] if a.get("num") == acc.get("app_num")), None)
            ok, uri = launch(app, pid)
            print(f"[{'OK' if ok else '!!'}] {uri}")

        # ---------- [k] เปลี่ยน key ----------
        elif c == "k":
            key_info_menu()

        # ---------- [s] สถิติ ----------
        elif c == "s":
            print(f"  สะสมทั้งหมด: rejoin {TOTALS['rejoins']} · hop {TOTALS['hops']} · alert {TOTALS['alerts']}")
            print(f"  log ไฟล์: {LOG_F} (หมุนเวียน 3 ไฟล์ สูงสุด ~600KB)")
            b = os.path.join(HERE, "star_config.backup.json")
            if input("[?] backup config ตอนนี้? (y/n): ").strip().lower() == "y":
                save_cfg(cfg)
                with open(CONFIG) as f1, open(b, "w") as f2:
                    f2.write(f1.read())
                print(f"[OK] → {b}")

        # ---------- [0] ออก ----------
        elif c == "0":
            save_totals()
            if os.path.exists(CONFIG):
                os.remove(CONFIG)
                print("[*] ลบ config แล้ว")
            sys.exit("[*] บาย!")

if __name__ == "__main__":
    try:
        main()
    finally:
        save_totals()
