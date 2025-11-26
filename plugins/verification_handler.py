# Credit: @Hanimes_Hindi

import logging
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import (
    check_token, get_token, verify_user_system_1, verify_user_system_2,
    check_verification, need_second_verification, reset_user_verification
)
from config import VERIFY_IMG, VERIFY_MODE_1, VERIFY_MODE_2

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.incoming)
async def handle_verification(client: Client, message):
    """Handle both verification systems when user clicks verify link"""
    if len(message.command) != 2:
        return  # Not a verify link, let other handlers process
    
    data = message.command[1]
    if not data.startswith("verify"):
        return  # Not a verify link
    
    try:
        parts = data.split("-")
        if len(parts) < 4:
            return
        
        userid = parts[1]
        token = parts[2]
        system = int(parts[3]) if len(parts) > 3 else 1
        
        # Verify userid matches sender
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link!</b>",
                protect_content=True
            )
        
        # Check which system to verify
        if system == 1:
            is_valid = await check_token(client, userid, token, system=1)
            if is_valid:
                await verify_user_system_1(client, userid, token)
                await message.reply_text(
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified (Stage 1)!\nNow you have full bot access for the next period.</b>",
                    protect_content=True
                )
            else:
                return await message.reply_text(
                    text="<b>Invalid link or Expired link!</b>",
                    protect_content=True
                )
        
        elif system == 2:
            is_valid = await check_token(client, userid, token, system=2)
            if is_valid:
                await verify_user_system_2(client, userid, token)
                await message.reply_text(
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified (Stage 2)!\nYou now have unlimited access again!</b>",
                    protect_content=True
                )
            else:
                return await message.reply_text(
                    text="<b>Invalid link or Expired link!</b>",
                    protect_content=True
                )
    
    except Exception as e:
        logger.error(f"Verification error: {e}")
        await message.reply_text("<b>An error occurred during verification.</b>")


async def get_verification_status(client, user_id):
    """
    Returns verification status:
    - 0: Not verified
    - 1: Verified system 1, can access
    - 2: Needs system 2 verification
    - 3: Verified system 2, full access
    """
    if not VERIFY_MODE_1 and not VERIFY_MODE_2:
        return 3  # Both disabled, full access
    
    is_verified = await check_verification(client, user_id)
    if is_verified:
        needs_second = await need_second_verification(client, user_id)
        return 1 if not needs_second else 2
    return 0
