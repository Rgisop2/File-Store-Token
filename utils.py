# Credit: @Hanimes_Hindi

import logging, asyncio, os, re, random, pytz, aiohttp, requests, string, json, http.client
from datetime import date, datetime, timedelta
from config import (
    SHORTLINK_API_1, SHORTLINK_URL_1, SHORTLINK_API_2, SHORTLINK_URL_2, 
    PASTIME, VERIFY_TIME_1, VERIFY_TIME_2
)
from shortzy import Shortzy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TOKENS_1 = {}  # Verification system 1 tokens
TOKENS_2 = {}  # Verification system 2 tokens
VERIFIED_1 = {}  # Tracks first verification with PASTIME expiry
VERIFIED_2 = {}  # Tracks second verification after PASTIME expires
USER_VERIFICATION_STATE = {}  # Tracks which verification stage user is in (1 or 2)

async def get_verify_shorted_link(link, system=1):
    """Generate shortened verification link for system 1 or 2"""
    shortlink_url = SHORTLINK_URL_1 if system == 1 else SHORTLINK_URL_2
    shortlink_api = SHORTLINK_API_1 if system == 1 else SHORTLINK_API_2
    
    if shortlink_url == "api.shareus.io":
        url = f'https://{shortlink_url}/easy_api'
        params = {
            "key": shortlink_api,
            "link": link,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.text()
                    return data
        except Exception as e:
            logger.error(e)
            return link
    else:
        shortzy = Shortzy(api_key=shortlink_api, base_site=shortlink_url)
        link = await shortzy.convert(link)
        return link

async def check_token(bot, userid, token, system=1):
    """Check if token is valid for verification system 1 or 2"""
    user = await bot.get_users(userid)
    tokens_dict = TOKENS_1 if system == 1 else TOKENS_2
    
    if user.id in tokens_dict.keys():
        TKN = tokens_dict[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False

async def get_token(bot, userid, link, system=1):
    """Generate verification token and shortened link for system 1 or 2"""
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    tokens_dict = TOKENS_1 if system == 1 else TOKENS_2
    tokens_dict[user.id] = {token: False}
    link = f"{link}verify-{user.id}-{token}-{system}"
    shortened_verify_url = await get_verify_shorted_link(link, system=system)
    return str(shortened_verify_url)

async def verify_user_system_1(bot, userid, token):
    """Mark user as verified in system 1 (sets PASTIME expiry)"""
    user = await bot.get_users(userid)
    TOKENS_1[user.id] = {token: True}
    
    # Set expiry time as current time + PASTIME
    expiry_time = datetime.now() + timedelta(seconds=PASTIME)
    VERIFIED_1[user.id] = expiry_time.isoformat()
    USER_VERIFICATION_STATE[user.id] = 1  # Stage 1 verified

async def verify_user_system_2(bot, userid, token):
    """Mark user as verified in system 2 (full access)"""
    user = await bot.get_users(userid)
    TOKENS_2[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    VERIFIED_2[user.id] = str(today)
    USER_VERIFICATION_STATE[user.id] = 2  # Stage 2 verified (full access)

async def check_verification(bot, userid):
    """
    Check user verification status:
    - If no verification: False
    - If in stage 1 but PASTIME expired: False (needs stage 2)
    - If in stage 1 and PASTIME active: True
    - If in stage 2: True
    """
    user = await bot.get_users(userid)
    
    # Check if user is in stage 2 (second verification completed)
    if user.id in VERIFIED_2.keys():
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        EXP = VERIFIED_2[user.id]
        try:
            years, month, day = EXP.split('-')
            comp = date(int(years), int(month), int(day))
            if comp >= today:
                return True
        except:
            pass
    
    # Check if user is in stage 1 (first verification with PASTIME)
    if user.id in VERIFIED_1.keys():
        try:
            expiry_time = datetime.fromisoformat(VERIFIED_1[user.id])
            if datetime.now() < expiry_time:
                return True  # Still has access
            else:
                # PASTIME expired, need stage 2 verification
                return False
        except:
            pass
    
    return False

async def need_second_verification(bot, userid):
    """Check if user needs to do second verification (PASTIME expired)"""
    user = await bot.get_users(userid)
    
    if user.id in VERIFIED_1.keys():
        try:
            expiry_time = datetime.fromisoformat(VERIFIED_1[user.id])
            if datetime.now() >= expiry_time:
                return True  # PASTIME expired, need stage 2
        except:
            pass
    
    return False

async def reset_user_verification(userid):
    """Reset user verification when they need to re-verify from stage 1"""
    if userid in VERIFIED_1:
        del VERIFIED_1[userid]
    if userid in VERIFIED_2:
        del VERIFIED_2[userid]
    if userid in TOKENS_1:
        del TOKENS_1[userid]
    if userid in TOKENS_2:
        del TOKENS_2[userid]
    if userid in USER_VERIFICATION_STATE:
        del USER_VERIFICATION_STATE[userid]
