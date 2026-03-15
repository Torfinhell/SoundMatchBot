from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import BACKEND_URL
import httpx

async def polls_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available polls"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/polls/active")
            polls = response.json()
        
        if not polls:
            text = "No active polls available right now."
        else:
            text = "Active Polls:\n\n"
            keyboard = []
            for poll in polls:
                text += f"• {poll['question']}\n"
                keyboard.append([InlineKeyboardButton(f"Answer: {poll['question'][:30]}...", callback_data=f"poll_{poll['id']}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if hasattr(update, 'callback_query') and update.callback_query:
                await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
            else:
                await update.message.reply_text(text, reply_markup=reply_markup)
            return
            
    except Exception as e:
        text = f"Error loading polls: {str(e)}"
    
    if hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(text)
    else:
        await update.message.reply_text(text)

async def poll_answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle poll answers"""
    message = update.message.text
    if message.startswith("ans:"):
        answer = message[4:].strip()
        # For demo, just acknowledge
        await update.message.reply_text(f"You answered: {answer}")
    else:
        await update.message.reply_text("Please use the format: ans: your_answer")
