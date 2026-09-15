#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
সহজ Telegram Bot - US Student Email Registration
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_ID
from database import DatabaseConnection
from datetime import datetime
import asyncio

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_FOR_EMAIL, WAITING_FOR_NAME, WAITING_FOR_DOB, WAITING_FOR_SSN, WAITING_FOR_ADDRESS, WAITING_FOR_PHONE, WAITING_FOR_CONFIRMATION = range(7)

class StudentEmailBot:
    def __init__(self):
        self.db = DatabaseConnection()
        self.user_data = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """স্টার্ট কমান্ড"""
        try:
            welcome_text = """🎓 স্বাগতম US Student Email Bot এ!

এই বট আপনাকে সাহায্য করবে US শিক্ষা ইমেইল রেজিস্ট্রেশন অটোমেট করতে।

উপলব্ধ কমান্ড:
/start - এই বার্তা দেখান
/register - রেজিস্ট্রেশন শুরু করুন
/status - স্ট্যাটাস চেক করুন
/help - সাহায্য পান"""

            keyboard = [
                [InlineKeyboardButton("📝 রেজিস্ট্রেশন শুরু করুন", callback_data='start_reg')],
                [InlineKeyboardButton("📊 স্ট্যাটাস চেক করুন", callback_data='check_status')],
                [InlineKeyboardButton("❓ সাহায্য", callback_data='help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
            logger.info(f"User {update.effective_user.id} started the bot")
        except Exception as e:
            logger.error(f"Error in start: {e}")
            await update.message.reply_text("❌ কোনো সমস্যা হয়েছে। পুনরায় চেষ্টা করুন।")

    async def register_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """রেজিস্ট্রেশন শুরু করুন"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_id = update.effective_user.id
            self.user_data[user_id] = {}

            await query.edit_message_text(
                text="📧 আপনার ইমেইল এড্রেস দিন:"
            )
            return WAITING_FOR_EMAIL
        except Exception as e:
            logger.error(f"Error in register_start: {e}")
            return ConversationHandler.END

    async def get_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ইমেইল নিন"""
        try:
            email = update.message.text.strip()
            
            if '@' not in email:
                await update.message.reply_text("❌ সঠিক ইমেইল ফরম্যাট নয়। আবার চেষ্টা করুন।")
                return WAITING_FOR_EMAIL
            
            user_id = update.effective_user.id
            self.user_data[user_id]['email'] = email
            
            await update.message.reply_text("👤 এখন আপনার সম্পূর্ণ নাম দিন (First Middle Last):")
            return WAITING_FOR_NAME
        except Exception as e:
            logger.error(f"Error in get_email: {e}")
            return WAITING_FOR_EMAIL

    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """নাম নিন"""
        try:
            full_name = update.message.text.strip()
            
            if len(full_name.split()) < 2:
                await update.message.reply_text("❌ কমপক্ষে দুটি অংশ দিয়ে নাম দিন (First Last):")
                return WAITING_FOR_NAME
            
            user_id = update.effective_user.id
            self.user_data[user_id]['fullName'] = full_name
            
            await update.message.reply_text("📅 জন্মতারিখ দিন (MM/DD/YYYY):")
            return WAITING_FOR_DOB
        except Exception as e:
            logger.error(f"Error in get_name: {e}")
            return WAITING_FOR_NAME

    async def get_dob(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """জন্মতারিখ নিন"""
        try:
            dob = update.message.text.strip()
            
            try:
                datetime.strptime(dob, '%m/%d/%Y')
            except ValueError:
                await update.message.reply_text("❌ সঠিক ফরম্যাট নয়। MM/DD/YYYY দিয়ে আবার চেষ্টা করুন:")
                return WAITING_FOR_DOB
            
            user_id = update.effective_user.id
            self.user_data[user_id]['birthday'] = dob
            
            await update.message.reply_text("🔐 সোশ্যাল সিকিউরিটি নম্বর দিন (XXX-XX-XXXX):")
            return WAITING_FOR_SSN
        except Exception as e:
            logger.error(f"Error in get_dob: {e}")
            return WAITING_FOR_DOB

    async def get_ssn(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """SSN নিন"""
        try:
            ssn = update.message.text.strip()
            
            if len(ssn.replace('-', '')) != 9:
                await update.message.reply_text("❌ সঠিক SSN ফরম্যাট নয়। XXX-XX-XXXX দিয়ে আবার চেষ্টা করুন:")
                return WAITING_FOR_SSN
            
            user_id = update.effective_user.id
            self.user_data[user_id]['ssn'] = ssn
            
            await update.message.reply_text("📍 আপনার রাস্তার ঠিকানা দিন:")
            return WAITING_FOR_ADDRESS
        except Exception as e:
            logger.error(f"Error in get_ssn: {e}")
            return WAITING_FOR_SSN

    async def get_address(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ঠিকানা নিন"""
        try:
            address = update.message.text.strip()
            
            user_id = update.effective_user.id
            self.user_data[user_id]['address'] = address
            
            await update.message.reply_text("📞 আপনার ফোন নম্বর দিন:")
            return WAITING_FOR_PHONE
        except Exception as e:
            logger.error(f"Error in get_address: {e}")
            return WAITING_FOR_ADDRESS

    async def get_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ফোন নম্বর নিন"""
        try:
            phone = update.message.text.strip()
            
            user_id = update.effective_user.id
            self.user_data[user_id]['phone'] = phone
            
            # নিশ্চিতকরণ
            user_info = self.user_data[user_id]
            confirmation_text = f"""✅ আপনার তথ্য নিশ্চিত করুন:

📧 ইমেইল: {user_info['email']}
👤 নাম: {user_info['fullName']}
📅 জন্মতারিখ: {user_info['birthday']}
📍 ঠিকানা: {user_info['address']}
📞 ফোন: {user_info['phone']}

এটি সঠিক কিনা?"""
            
            keyboard = [
                [InlineKeyboardButton("✅ হাঁ, জমা দিন", callback_data='confirm_yes')],
                [InlineKeyboardButton("❌ না, বাতিল করুন", callback_data='confirm_no')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(confirmation_text, reply_markup=reply_markup)
            return WAITING_FOR_CONFIRMATION
        except Exception as e:
            logger.error(f"Error in get_phone: {e}")
            return WAITING_FOR_PHONE

    async def confirm_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """রেজিস্ট্রেশন নিশ্চিত করুন"""
        try:
            query = update.callback_query
            await query.answer()
            
            if query.data == 'confirm_no':
                await query.edit_message_text(
                    text="❌ রেজিস্ট্রেশন বাতিল করা হয়েছে। /register দিয়ে আবার শুরু করুন।"
                )
                return ConversationHandler.END
            
            user_id = update.effective_user.id
            user_info = self.user_data[user_id]
            
            # ডাটাবেসে সেভ করুন
            data = [
                user_info['email'],
                user_info['fullName'],
                'M',
                'Mr.',
                'White',
                user_info['birthday'],
                user_info['ssn'],
                user_info['address'],
                'City',
                'CA',
                'California',
                '90000',
                user_info['phone'],
                user_info['phone'],
                user_info['email'],
                '',
                '',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            
            if self.db.add_user_detail(data):
                await query.edit_message_text(
                    text="✅ রেজিস্ট্রেশন সফল হয়েছে!\n\nআপনার তথ্য সংরক্ষিত হয়েছে এবং শীঘ্রই প্রক্রিয়া করা হবে।"
                )
                logger.info(f"User {user_id} registered with email {user_info['email']}")
            else:
                await query.edit_message_text(
                    text="❌ তথ্য সংরক্ষণে ব্যর্থ। আবার চেষ্টা করুন।"
                )
            
            return ConversationHandler.END
        except Exception as e:
            logger.error(f"Error in confirm_registration: {e}")
            await query.edit_message_text("❌ কোনো সমস্যা হয়েছে। আবার চেষ্টা করুন।")
            return ConversationHandler.END

    async def check_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """স্ট্যাটাস চেক করুন"""
        try:
            query = update.callback_query
            await query.answer()
            await query.edit_message_text(
                text="📊 স্ট্যাটাস চেক\n\nস্ট্যাটাস: 0 = চলমান\nস্ট্যাটাস: 1 = আবেদন করা হয়েছে\nস্ট্যাটাস: 2 = রেজিস্টার করা হয়েছে\nস্ট্যাটাস: 3 = ব্যর্থ"
            )
        except Exception as e:
            logger.error(f"Error in check_status: {e}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """সাহায্য দেখান"""
        try:
            query = update.callback_query
            await query.answer()
            help_text = """❓ সাহায্য তথ্য

📝 রেজিস্ট্রেশন: /register দিয়ে শুরু করুন
📊 স্ট্যাটাস: /status দিয়ে দেখুন
⚙️ প্রক্রিয়া:
1. আপনার ব্যক্তিগত তথ্য পূরণ করুন
2. যাচাইয়ের জন্য জমা দিন
3. বট কলেজ ওয়েবসাইটে অটোমেটিক নিবন্ধন করবে
4. আপনি শিক্ষার্থী ইমেইল পাবেন

সহায়তার জন্য অ্যাডমিনিস্ট্রেটরের সাথে যোগাযোগ করুন।"""
            await query.edit_message_text(help_text)
        except Exception as e:
            logger.error(f"Error in help_command: {e}")

    async def error_handler(self, update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """এরর হ্যান্ডলার"""
        logger.error(f"Update {update} caused error {context.error}")


async def main():
    """মূল ফাংশন"""
    
    # অ্যাপ্লিকেশন তৈরি করুন
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot = StudentEmailBot()
    
    # হ্যান্ডলার যোগ করুন
    application.add_handler(CommandHandler("start", bot.start))
    
    # কনভার্সেশন হ্যান্ডলার
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot.register_start, pattern='^start_reg$')],
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
    
    # কলব্যাক হ্যান্ডলার
    application.add_handler(CallbackQueryHandler(bot.check_status, pattern='^check_status$'))
    application.add_handler(CallbackQueryHandler(bot.help_command, pattern='^help$'))
    
    application.add_handler(conv_handler)
    
    # এরর হ্যান্ডলার
    application.add_error_handler(bot.error_handler)
    
    logger.info("Telegram Bot শুরু হচ্ছে...")
    
    # বট চালান
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
