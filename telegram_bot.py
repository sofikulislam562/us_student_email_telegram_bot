#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot for US Student Email Automation
Modern implementation using python-telegram-bot 20.x
"""

import logging
from datetime import datetime
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_ID
from database import DatabaseConnection
import asyncio

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_FOR_EMAIL, WAITING_FOR_NAME, WAITING_FOR_DOB, WAITING_FOR_SSN, \
    WAITING_FOR_ADDRESS, WAITING_FOR_PHONE, WAITING_FOR_CONFIRMATION = range(7)

class StudentEmailBot:
    """Telegram bot for student email automation"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.user_data = {}
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start command handler"""
        try:
            welcome_text = """🎓 Welcome to US Student Email Bot!

This bot helps you automate the registration for US educational email addresses.

Available commands:
/start - Show this welcome message
/register - Start registration process
/status - Check registration status
/help - Get help information
/admin - Admin commands (admins only)
            """
            
            keyboard = [
                [InlineKeyboardButton("📝 Start Registration", callback_data='start_reg')],
                [InlineKeyboardButton("📊 Check Status", callback_data='check_status')],
                [InlineKeyboardButton("❓ Help", callback_data='help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
            logger.info(f"User {update.effective_user.id} started the bot")
        except TelegramError as e:
            logger.error(f"Telegram error in start: {e}")
    
    async def register_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start registration process"""
        try:
            if update.callback_query:
                await update.callback_query.answer()
            
            user_id = update.effective_user.id
            self.user_data[user_id] = {}
            
            msg = await update.effective_message.edit_text(
                "📧 Please enter your email address:",
                reply_markup=None
            )
            context.user_data['message_id'] = msg.message_id
            
            return WAITING_FOR_EMAIL
        except TelegramError as e:
            logger.error(f"Telegram error in register_start: {e}")
            return ConversationHandler.END
    
    async def get_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get email from user"""
        try:
            email = update.message.text.strip()
            
            if '@' not in email:
                await update.message.reply_text("❌ Invalid email format. Please try again.")
                return WAITING_FOR_EMAIL
            
            user_id = update.effective_user.id
            self.user_data[user_id]['email'] = email
            
            await update.message.reply_text(
                "👤 Now enter your full name (First Middle Last):"
            )
            return WAITING_FOR_NAME
        except Exception as e:
            logger.error(f"Error in get_email: {e}")
            return WAITING_FOR_EMAIL
    
    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get full name from user"""
        try:
            full_name = update.message.text.strip()
            
            if len(full_name.split()) < 2:
                await update.message.reply_text(
                    "❌ Please enter full name with at least 2 parts (First Last):"
                )
                return WAITING_FOR_NAME
            
            user_id = update.effective_user.id
            self.user_data[user_id]['fullName'] = full_name
            
            await update.message.reply_text(
                "📅 Enter your date of birth (MM/DD/YYYY):"
            )
            return WAITING_FOR_DOB
        except Exception as e:
            logger.error(f"Error in get_name: {e}")
            return WAITING_FOR_NAME
    
    async def get_dob(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get date of birth from user"""
        try:
            dob = update.message.text.strip()
            
            # Validate date format
            try:
                datetime.strptime(dob, '%m/%d/%Y')
            except ValueError:
                await update.message.reply_text(
                    "❌ Invalid date format. Use MM/DD/YYYY:"
                )
                return WAITING_FOR_DOB
            
            user_id = update.effective_user.id
            self.user_data[user_id]['birthday'] = dob
            
            await update.message.reply_text(
                "🔐 Enter your Social Security Number (XXX-XX-XXXX):"
            )
            return WAITING_FOR_SSN
        except Exception as e:
            logger.error(f"Error in get_dob: {e}")
            return WAITING_FOR_DOB
    
    async def get_ssn(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get SSN from user"""
        try:
            ssn = update.message.text.strip()
            
            # Validate SSN format
            if len(ssn.replace('-', '')) != 9:
                await update.message.reply_text(
                    "❌ Invalid SSN format. Use XXX-XX-XXXX:"
                )
                return WAITING_FOR_SSN
            
            user_id = update.effective_user.id
            self.user_data[user_id]['ssn'] = ssn
            
            await update.message.reply_text(
                "📍 Enter your street address:"
            )
            return WAITING_FOR_ADDRESS
        except Exception as e:
            logger.error(f"Error in get_ssn: {e}")
            return WAITING_FOR_SSN
    
    async def get_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get address from user"""
        try:
            address = update.message.text.strip()
            
            user_id = update.effective_user.id
            self.user_data[user_id]['address'] = address
            
            await update.message.reply_text(
                "📞 Enter your phone number:"
            )
            return WAITING_FOR_PHONE
        except Exception as e:
            logger.error(f"Error in get_address: {e}")
            return WAITING_FOR_ADDRESS
    
    async def get_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get phone number from user"""
        try:
            phone = update.message.text.strip()
            
            user_id = update.effective_user.id
            self.user_data[user_id]['phone'] = phone
            
            # Show confirmation
            user_info = self.user_data[user_id]
            confirmation_text = f"""✅ Please confirm your information:

📧 Email: {user_info['email']}
👤 Name: {user_info['fullName']}
📅 DOB: {user_info['birthday']}
📍 Address: {user_info['address']}
📞 Phone: {user_info['phone']}

Is this correct?
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ Yes, Submit", callback_data='confirm_yes')],
                [InlineKeyboardButton("❌ No, Cancel", callback_data='confirm_no')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(confirmation_text, reply_markup=reply_markup)
            return WAITING_FOR_CONFIRMATION
        except Exception as e:
            logger.error(f"Error in get_phone: {e}")
            return WAITING_FOR_PHONE
    
    async def confirm_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Confirm and submit registration"""
        try:
            query = update.callback_query
            await query.answer()
            
            if query.data == 'confirm_no':
                await query.edit_message_text(
                    "❌ Registration cancelled. Use /register to start again."
                )
                return ConversationHandler.END
            
            user_id = update.effective_user.id
            user_info = self.user_data[user_id]
            
            # Save to database
            data = [
                user_info['email'],  # userName (email as username)
                user_info['fullName'],
                'M',  # gender (default)
                'Mr.',  # title (default)
                'White',  # race (default)
                user_info['birthday'],
                user_info['ssn'],
                user_info['address'],
                'City',  # city (placeholder)
                'CA',  # state (default)
                'California',
                '90000',  # zip (placeholder)
                user_info['phone'],
                user_info['phone'],  # mobile
                user_info['email'],
                '',  # email_pwd
                '',  # email_server
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            
            if self.db.add_user_detail(data):
                await query.edit_message_text(
                    "✅ Registration submitted successfully!\n\n" 
                    "Your information has been saved and will be processed soon.\n"
                    "You will receive updates on your status."
                )
                logger.info(f"User {user_id} registered with email {user_info['email']}")
            else:
                await query.edit_message_text(
                    "❌ Failed to save registration. Please try again."
                )
            
            return ConversationHandler.END
        except Exception as e:
            logger.error(f"Error in confirm_registration: {e}")
            await query.edit_message_text("❌ An error occurred. Please try again.")
            return ConversationHandler.END
    
    async def check_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Check registration status"""
        try:
            if update.callback_query:
                query = update.callback_query
                await query.answer()
                await query.edit_message_text(
                    "📊 Status Check\n\n"
                    "Status: 0 = Pending\n"
                    "Status: 1 = Applied\n"
                    "Status: 2 = Registered\n"
                    "Status: 3 = Failed\n\n"
                    "Use /admin to check specific users."
                )
            else:
                await update.message.reply_text(
                    "📊 To check status, use the inline buttons from /start"
                )
        except TelegramError as e:
            logger.error(f"Telegram error in check_status: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show help information"""
        try:
            if update.callback_query:
                query = update.callback_query
                await query.answer()
                help_text = """❓ Help Information

📝 Registration: Use /register to start the registration process
📊 Status: Use /status to check your registration status
🔄 Process:
1. Fill in your personal information
2. Submit for verification
3. Bot will automate the registration on the college website
4. You'll receive your student email address

For support, contact the administrator.
                """
                await query.edit_message_text(help_text)
            else:
                await update.message.reply_text(
                    "❓ Use /start for help and options."
                )
        except TelegramError as e:
            logger.error(f"Telegram error in help_command: {e}")
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Admin commands"""
        try:
            if update.effective_user.id != TELEGRAM_ADMIN_ID:
                await update.message.reply_text(
                    "❌ You don't have permission to use admin commands."
                )
                return
            
            admin_text = """👨‍💼 Admin Panel

Commands:
/admin_stats - Show statistics
/admin_users - List pending users
/admin_process - Start processing queue
            """
            await update.message.reply_text(admin_text)
        except Exception as e:
            logger.error(f"Error in admin_command: {e}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Error handler"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "❌ An error occurred. Please try again or contact support."
                )
            except TelegramError as e:
                logger.error(f"Failed to send error message: {e}")


async def main():
    """Main function to start the bot"""
    
    # Create bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot = StudentEmailBot()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("status", bot.check_status))
    application.add_handler(CommandHandler("admin", bot.admin_command))
    
    # Conversation handler for registration
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("register", bot.register_start)],
        states={
            WAITING_FOR_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_email)],
            WAITING_FOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_name)],
            WAITING_FOR_DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_dob)],
            WAITING_FOR_SSN: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_ssn)],
            WAITING_FOR_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_address)],
            WAITING_FOR_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_phone)],
            WAITING_FOR_CONFIRMATION: [CallbackQueryHandler(bot.confirm_registration)]
        },
        fallbacks=[CommandHandler("start", bot.start)]
    )
    
    # Callback query handler for buttons
    application.add_handler(CallbackQueryHandler(bot.register_start, pattern='^start_reg$'))
    application.add_handler(CallbackQueryHandler(bot.check_status, pattern='^check_status$'))
    application.add_handler(CallbackQueryHandler(bot.help_command, pattern='^help$'))
    
    application.add_handler(conv_handler)
    
    # Error handler
    application.add_error_handler(bot.error_handler)
    
    logger.info("Starting US Student Email Telegram Bot...")
    
    # Start bot
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
