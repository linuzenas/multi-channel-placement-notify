# Telegram Setup Guide

## 🤖 Setting Up Telegram Bot for Placement Group

### Step 1: Create Telegram Bot (if not done already)

1. **Open Telegram** and search for [@BotFather](https://t.me/botfather)
2. **Start a conversation** with BotFather
3. **Send command:** `/newbot`
4. **Follow the instructions:**
   - Enter bot name: `Placement Helper Bot`
   - Enter bot username: `your_placement_bot` (must end with 'bot')
5. **Save the token** that BotFather gives you

### Step 2: Add Bot to Placement Group

1. **Create or open your placement group** in Telegram
2. **Add the bot** to the group:
   - Click on group name → Add Members
   - Search for your bot username
   - Add the bot to the group
3. **Make bot an admin:**
   - Go to group settings → Administrators
   - Add your bot as admin
   - Give it permission to send messages

### Step 3: Get Group ID

1. **Run the helper script:**
   ```bash
   python get_telegram_group_id.py
   ```

2. **Send a test message** in your placement group

3. **Run the script again** to get the group ID:
   ```bash
   python get_telegram_group_id.py
   ```

4. **Copy the group ID** (it will look like `-1001234567890`)

### Step 4: Configure Environment

1. **Open your `.env` file**
2. **Update the Telegram settings:**
   ```env
   TELEGRAM_TOKEN=your-bot-token-here
   TELEGRAM_GROUP_ID=-1001234567890
   ```

### Step 5: Test Configuration

1. **Start the application:**
   ```bash
   python run.py
   ```

2. **Go to admin dashboard:** http://localhost:5000

3. **Click "Test Configuration"** and enter your email

4. **Check both email and Telegram group** for test messages

## ✅ Verification

You should see:
- ✅ **Email received** in your inbox
- ✅ **Message posted** in your Telegram group
- ✅ **Success message** in the admin panel

## 🔧 Troubleshooting

### Bot Not Receiving Messages
- Make sure bot is added to the group
- Check if bot has admin permissions
- Verify bot token is correct

### Group ID Not Found
- Send a message in the group first
- Make sure bot can read messages
- Try running the helper script again

### Permission Errors
- The application now handles file cleanup automatically
- No action needed for temporary file errors

## 📱 Example Group Message

When working correctly, your placement group will receive messages like:

```
📢 New Placement Opportunity!

Company: Hire3x!!
Job Title: Graduate Trainee – Developer

UG CTC: 3.5 to 5 LPA based on performance
PG CTC: 4.5 to 6 LPA based on performance
Stipend: Rs. 15k/- Per month during training

Eligibility: Unplaced Students with no standing arrear

Registration Link: https://example.com/registration

Additional Notes: It is mandatory that every interested students must register
```

## 🎉 Ready to Use!

Once configured, the system will:
1. Send messages to your Telegram group
2. Send individual emails to all students
3. Process Excel files without database storage
4. Handle all file operations safely
