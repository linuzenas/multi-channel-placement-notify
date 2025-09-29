# Quick Setup Guide - Placement Messenger Admin Panel

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env with your credentials
# Required:
SECRET_KEY=your-secret-key-here
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
TELEGRAM_TOKEN=your-telegram-bot-token

# Optional:
TELEGRAM_GROUP_ID=-1001234567890
```

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Run Application
```bash
python run.py
```

### 5. Access Admin Panel
- Open browser: http://localhost:5000
- Start creating placement messages!

## 🔧 Required Setup

### Gmail Setup
1. Enable 2FA on Gmail
2. Generate App Password
3. Add to `.env` file

### Telegram Bot (Optional)
1. Message [@BotFather](https://t.me/botfather)
2. Create bot with `/newbot`
3. Add bot to placement group
4. Get group ID from [@userinfobot](https://t.me/userinfobot)
5. Add token and group ID to `.env`

## 📁 Project Structure
```
placement-messenger/
├── app.py                 # Main Flask app
├── config.py             # Configuration
├── run.py                # Startup script
├── test_setup.py         # Setup verification
├── requirements.txt      # Dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── admin/
│       ├── dashboard.html
│       ├── create_message.html
│       └── upload_students.html
└── static/               # CSS, JS, images
```

## 🎯 How It Works

### 1. Create Message
- Fill in placement opportunity details
- Preview the message
- Save for sending

### 2. Upload Students
- Download Excel template
- Add student names and emails
- Upload file to send messages

### 3. Send Messages
- Messages sent to Telegram group
- Individual emails sent to students
- No database storage required

## 📊 Excel Format
| name | email |
|------|-------|
| John Doe | john@klu.ac.in |
| Jane Smith | jane@klu.ac.in |

**Important:** Column names must be exactly "name" and "email"

## 🆘 Troubleshooting

### Common Issues
1. **Import errors**: Run `pip install -r requirements.txt`
2. **Email not sending**: Check Gmail app password
3. **Telegram not working**: Verify bot token and group ID
4. **Excel errors**: Check column names and format

### Test Configuration
- Use "Test Configuration" on dashboard
- Send test message to verify setup
- Check logs in `placement_messenger.log`

## 🎉 You're Ready!
The admin panel is now ready to use. Create messages, upload student lists, and send notifications efficiently!