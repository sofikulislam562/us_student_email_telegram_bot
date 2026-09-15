# US Student Email Telegram Bot 🎓

Modern automation bot for US educational email registration with Telegram integration.

## Overview

This project automates the registration process for US student educational email addresses. It has been completely modernized from the original 2020 codebase with:

- ✅ Updated Python 3.11+ support
- ✅ Telegram Bot integration (python-telegram-bot 20.x)
- ✅ Modern async/await patterns
- ✅ Improved error handling and logging
- ✅ Better database connection management
- ✅ Enhanced security features
- ✅ Clean, maintainable code structure

## Features

### Core Functionality
1. **Student Information Registration** - Collect and validate student data via Telegram
2. **Automated Web Registration** - Auto-fill and submit college application forms
3. **Email Extraction** - Extract and store generated student emails
4. **Database Management** - Store and track registration status
5. **Admin Dashboard** - Monitor registration progress

### Telegram Bot Commands

- `/start` - Welcome and show main menu
- `/register` - Begin registration process
- `/status` - Check registration status
- `/help` - Show help information
- `/admin` - Admin controls (admin only)

## Installation

### Prerequisites
- Python 3.11+
- MySQL 5.7+
- Telegram Bot Token (from @BotFather)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/sofikulislam562/us_student_email_telegram_bot.git
cd us_student_email_telegram_bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup database**
```bash
mysql -u root -p < database_schema.sql
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run the bot**
```bash
python telegram_bot.py
```

## Configuration

### Environment Variables (.env)
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_ID=your_admin_id
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=student_email
DEFAULT_PASSWORD=qaz2020
DEFAULT_PIN=9210
```

## Project Structure

```
.
├── telegram_bot.py          # Main Telegram bot implementation
├── browser_automation.py    # Browser automation with pyppeteer
├── database.py              # Database operations
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
└── database_schema.sql      # Database schema
```

## Module Descriptions

### telegram_bot.py
Main bot implementation with:
- Welcome and registration flow
- Conversation state management
- User input validation
- Database integration
- Admin commands

### browser_automation.py
Browser automation module:
- Modern pyppeteer integration
- Anti-detection mechanisms
- Page setup and navigation
- Async context manager support

### database.py
Database operations:
- Connection pooling with context managers
- CRUD operations
- Error handling and logging
- Prepared statements for SQL injection protection

### config.py
Centralized configuration:
- Environment variable loading
- Telegram settings
- Database credentials
- Application constants

## Usage

### Starting Registration
1. User sends `/register` command
2. Bot asks for personal information step by step
3. User confirms the entered data
4. Bot stores information in database
5. Automation process begins automatically

### Admin Operations
```bash
# Check pending registrations
/admin_stats

# List users waiting for processing
/admin_users

# Start automated processing
/admin_process
```

## Database Schema

### user_detail_our_email
- Stores initial student registration information
- Tracks processing status with tags

### email_detail
- Stores generated student email credentials
- Contains college-specific information

## Status Codes
- **0** - Pending registration
- **1** - Applied (form submitted)
- **2** - Registered (email generated)
- **3** - Failed
- **4** - Processing error

## Error Handling

- Comprehensive try-catch blocks
- Detailed logging with bot.log
- User-friendly error messages
- Admin notifications on critical errors

## Improvements from Original

| Feature | Original | Updated |
|---------|----------|----------|
| Python Version | 3.7 | 3.11+ |
| Bot Interface | Custom CLI | Telegram Bot |
| Dependencies | Outdated | Latest stable |
| Error Handling | Basic | Comprehensive |
| Database | Direct SQL | ORM-like wrapper |
| Async Support | Limited | Full async/await |
| Logging | Basic file | Structured logging |
| Security | None | Input validation |

## API Updates

### Pyppeteer
- Updated from 0.2.5 to latest
- New anti-detection methods
- Improved reliability

### python-telegram-bot
- Migrated from old to 20.x
- Better error handling
- Type hints support

### Database
- Modern connection handling
- Automatic resource cleanup
- Dictionary cursors for better data handling

## Troubleshooting

### Database Connection Error
```
Check MySQL is running and credentials in .env are correct
```

### Bot Not Responding
```
Verify TELEGRAM_BOT_TOKEN is correct
Check internet connection
View logs in bot.log
```

### Browser Automation Issues
```
Ensure Chromium is installed: pip install pyppeteer-new
Check if running in headless mode causes issues
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Contact admin via Telegram bot
- Check documentation in code comments

## Changelog

### v2.0.0 (2026-09-15)
- Complete rewrite with Telegram integration
- Updated all dependencies
- Improved code structure and documentation
- Added comprehensive error handling
- Enhanced security features

### v1.0.0 (2020-2021)
- Original automation system
- CLI-based interface
- Legacy dependencies

---

**Made with ❤️ for automation enthusiasts**
