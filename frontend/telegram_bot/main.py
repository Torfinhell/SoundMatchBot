from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from handlers.start import start_command, main_menu_handler
from handlers.polls import polls_menu, poll_answer_handler
from handlers.ranking import ranking_handler
from handlers.admin import admin_request_handler, admin_password_handler, ASK_PASS

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(main_menu_handler, pattern="^menu_"))
    
    # Simple poll flow for demo (text based answers)
    app.add_handler(CommandHandler("polls", polls_menu))
    app.add_handler(MessageHandler(filters.Regex(r"^ans:"), poll_answer_handler))
    
    # Rankings
    app.add_handler(CommandHandler("rankings", ranking_handler))
    
    # Admin Conversation
    conv_admin = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_request_handler, pattern="^menu_admin")],
        states={
            ASK_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_password_handler)]
        },
        fallbacks=[]
    )
    app.add_handler(conv_admin)

    print("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()