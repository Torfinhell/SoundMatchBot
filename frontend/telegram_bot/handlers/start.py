from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import BACKEND_URL
import httpx
from handlers.admin import ASK_PASS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📊 Rankings", callback_data="menu_rankings")],
        [InlineKeyboardButton("📝 Polls", callback_data="menu_polls")],
        [InlineKeyboardButton("👑 Admin", callback_data="menu_admin")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Welcome to SoundMatchBot, {user.first_name}!\n\n"
        "Find your music soulmate through polls and rankings.",
        reply_markup=reply_markup
    )

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu_rankings":
        await query.edit_message_text("Use /rankings to see rankings.")
    elif query.data == "menu_polls":
        await query.edit_message_text("Use /polls to see available polls.")
    elif query.data == "menu_admin":
        await query.edit_message_text("Admin access required. Please enter password:")
        return ASK_PASS  # This will be handled by the conversation handler
