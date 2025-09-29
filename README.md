# A Multi-Channel Messaging System for Placement Communication

A streamlined Flask web application for managing placement opportunities at KARE. The application provides an admin interface for creating placement messages and sending notifications via Excel file uploads, Telegram, and Email.

## Features

### Admin Features
- **Dashboard**: Overview of system status and quick actions
- **Create Messages**: Form-based interface to create placement opportunity messages
- **Excel Upload**: Upload student lists via Excel files (no database storage required)
- **Multi-Channel Sending**: Send messages to Telegram group and individual emails
- **Template Download**: Get Excel template for proper formatting
- **Test Configuration**: Test email and Telegram setup before sending

### Technical Features
- **Excel Processing**: Read student data from Excel files using pandas
- **Telegram Integration**: Send messages to placement group
- **Email Integration**: Send individual emails via Gmail SMTP
- **No Database**: Direct processing without storing student data
- **Responsive Design**: Modern UI with Bootstrap 5

## Prerequisites

- Python 3.8 or higher
- Gmail account with App Password
- Telegram Bot Token
- Telegram Group ID (optional)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/linuzenas/multi-channel-placement-notify.git
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Copy `env_example.txt` to `.env`
   - Fill in your configuration values:
     ```env
     SECRET_KEY=your-secret-key-here
     GMAIL_USER=your-email@gmail.com
     GMAIL_APP_PASSWORD=your-gmail-app-password
     TELEGRAM_TOKEN=your-telegram-bot-token
     TELEGRAM_GROUP_ID=your-group-id
     ```

## Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Enable 2FA for your Gmail account

2. **Generate App Password**
   - Go to Google Account > Security
   - Under "2-Step Verification", click "App passwords"
   - Generate a new app password for "Mail"
   - Use this password in your `.env` file

## Telegram Bot Setup

1. **Create Telegram Bot**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use `/newbot` command
   - Follow instructions to create your bot
   - Save the bot token

2. **Add Bot to Group**
   - Add your bot to the placement group
   - Get the group ID using [@userinfobot](https://t.me/userinfobot)
   - Use the group ID in your `.env` file

## Running the Application

1. **Test Setup**
   ```bash
   python test_setup.py
   ```

2. **Start the Application**
   ```bash
   python run.py
   ```

3. **Access the Application**
   - Open your browser and go to `http://localhost:5000`
   - Use the admin panel to create and send messages

## Usage

### Creating Placement Messages

1. **Access Create Message**
   - Click "Create Message" on the dashboard
   - Fill in the placement opportunity details:
     - Message title
     - Company name and job title
     - CTC details for UG/PG students
     - Stipend information
     - Eligibility criteria
     - Registration links
     - Additional notes

2. **Preview Message**
   - Use the preview button to see how the message will look
   - Make adjustments as needed

### Uploading Student Lists

1. **Prepare Excel File**
   - Download the template from the dashboard
   - Create Excel file with columns: `name` and `email`
   - Add student data (no database storage required)

2. **Upload and Send**
   - Go to "Upload Students" page
   - Select your Excel file
   - Click "Send Messages"
   - Messages are sent to Telegram group and individual emails

### Excel File Format

Your Excel file should have the following structure:

| name | email |
|------|-------|
| Linu Zenas | 9923008040@klu.ac.in |
| K Shyam Sunder | 9923008038@klu.ac.in |

**Important:**
- Column names must be exactly "name" and "email" (case-sensitive)
- No empty rows between data
- Valid email addresses required

## Sample Placement Message

The application supports messages in the following format:

```
Dear PDs (CSE ECE EEE IT BCA B.Sc (CS&IT) MCA M.Sc (CS,DS))

Hire3x!! has confirmed the campus drive for 2026 batch students.

Job Title: Graduate Trainee – Developer (Front-End / Back-End)

CTC details:
- For UG - 3.5 to 5 LPA based on overall performance rating during the training
- For PG - 4.5 to 6 LPA based on overall performance rating during the training

All candidates will be paid a stipend of Rs. 15k/- Per month during their Training period.

Eligibility Criteria: Unplaced Students with no standing arrear are eligible.

Registration Link: [Link to registration form]

Note: It is mandatory that every interested students must register on both the links mentioned above.
```

## Project Structure

```
placement-messenger/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── run.py                # Startup script
├── test_setup.py         # Setup verification
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables template
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   └── admin/            # Admin templates
│       ├── dashboard.html
│       ├── create_message.html
│       └── upload_students.html
└── static/               # CSS, JS, images (if needed)
```

## API Endpoints

- `GET /` - Home page (redirects to admin dashboard)
- `GET /admin` - Admin dashboard
- `GET /admin/create-message` - Create message form
- `POST /admin/create-message` - Create new message
- `GET /admin/upload-students` - Upload students page
- `POST /admin/upload-students` - Upload and send messages
- `GET /admin/template` - Download Excel template
- `POST /admin/send-test` - Send test message

## Security Features

- **File Validation**: Only Excel files allowed with size limits
- **Input Sanitization**: Form validation and data cleaning
- **Error Handling**: Comprehensive error handling and logging
- **Admin Only**: No user authentication required (admin panel only)

## Troubleshooting

### Common Issues

1. **Import errors**: Run `pip install -r requirements.txt`
2. **Email not sending**: Verify Gmail app password
3. **Telegram not working**: Check bot token and group ID
4. **Excel processing errors**: Ensure proper column names and format

### File Upload Issues

1. **File too large**: Maximum size is 16MB
2. **Invalid format**: Only .xlsx and .xls files allowed
3. **Column errors**: Ensure "name" and "email" columns exist
4. **Empty data**: Check for empty rows or invalid emails

## Deployment

### Local Development
```bash
python run.py
```

### Production Deployment
1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn
3. Set up reverse proxy with Nginx
4. Configure SSL certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the logs in `placement_messenger.log`

## Future Enhancements

- [ ] Message templates and presets
- [ ] Delivery status tracking
- [ ] Advanced Excel validation
- [ ] Message scheduling
- [ ] Analytics dashboard
- [ ] Multiple group support
