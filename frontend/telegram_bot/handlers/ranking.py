from telegram import Update
from telegram.ext import ContextTypes
from config import BACKEND_URL
import httpx

async def ranking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user rankings"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/rankings")
            rankings = response.json()
        
        if not rankings:
            text = "No rankings available yet."
        else:
            text = "🏆 Top Rankings:\n\n"
            for i, user in enumerate(rankings[:10], 1):
                text += f"{i}. {user.get('name', 'Anonymous')} - {user.get('score', 0)} points\n"
            
            text += "\nUse /start to go back to menu."
            
    except Exception as e:
        text = f"Error loading rankings: {str(e)}"
    
    if hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(text)
    else:
        await update.message.reply_text(text)
