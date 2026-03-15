from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import BACKEND_URL
import httpx

ASK_PASS = 0

async def admin_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Request admin password"""
    await update.callback_query.message.reply_text("Please enter admin password:")
    return ASK_PASS

async def admin_password_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin password"""
    password = update.message.text
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/admin/verify",
                json={"password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                await update.message.reply_text(f"Admin access granted!\nToken: {data.get('token', 'N/A')}")
            else:
                await update.message.reply_text("Invalid password.")
                
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
    
    return ConversationHandler.END
