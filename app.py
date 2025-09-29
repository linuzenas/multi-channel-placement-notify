#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Placement Messenger - Admin Panel

A Flask web application for managing placement messages with Excel file upload functionality.
Admins can upload student lists and send placement notifications via Telegram and Email.
"""

import os
import logging
import asyncio
import smtplib
import ssl
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from telegram.error import TelegramError
import pandas as pd
import tempfile
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_messenger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'
login_manager.login_message = 'Please login to access this page.'

# Message history storage (in-memory for now)
message_history = []

# Simple admin credentials (in production, use proper authentication)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=True)
    department = db.Column(db.String(50), nullable=True)
    year = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    telegram_chat_id = db.Column(db.String(50), nullable=True)
    placement_status = db.Column(db.String(20), default='unplaced')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_completed = db.Column(db.Boolean, default=False)

class PlacementMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    ctc_ug = db.Column(db.String(50), nullable=True)
    ctc_pg = db.Column(db.String(50), nullable=True)
    stipend = db.Column(db.String(50), nullable=True)
    eligibility = db.Column(db.Text, nullable=True)
    registration_link = db.Column(db.String(500), nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_to_telegram = db.Column(db.Boolean, default=False)
    sent_to_email = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("placement_messenger.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8462103585:AAE_oaonQCq2Dt9FncbpdIatjSaFSXnKlAM')
GMAIL_USER = os.getenv('GMAIL_USER', 'petluzenas@gmail.com')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', 'bsen xzcp mdjf jwej')
TELEGRAM_GROUP_ID = '-1003096231693'  # Your placement group ID

# Utility Functions
async def send_telegram_message(chat_id, message):
    """Send a message via Telegram bot."""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Telegram message sent successfully to chat ID: {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send Telegram message to {chat_id}: {e}")
        return False

def send_email(recipient_email, subject, html_content):
    """Send an email via Gmail."""
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = GMAIL_USER
        message["To"] = recipient_email
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipient_email, message.as_string())
        
        logger.info(f"Email sent successfully to: {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        return False

def create_placement_message_content(message_data, student_name):
    """Create placement message content for a student."""
    # Telegram message
    telegram_message = f"Hello {student_name},\n\n"
    telegram_message += f"New placement opportunity at {message_data['company_name']}!\n\n"
    telegram_message += f"Job Title: {message_data['job_title']}\n\n"
    
    if message_data.get('ctc_ug'):
        telegram_message += f"CTC for UG: {message_data['ctc_ug']}\n"
    if message_data.get('ctc_pg'):
        telegram_message += f"CTC for PG: {message_data['ctc_pg']}\n"
    if message_data.get('stipend'):
        telegram_message += f"Stipend: {message_data['stipend']}\n"
    
    if message_data.get('eligibility'):
        telegram_message += f"\nEligibility: {message_data['eligibility']}\n"
    
    if message_data.get('registration_link'):
        telegram_message += f"\nRegistration Link: {message_data['registration_link']}\n"
    
    if message_data.get('additional_notes'):
        telegram_message += f"\nAdditional Notes: {message_data['additional_notes']}\n"
    
    # Email content
    email_subject = f"New Placement Opportunity - {message_data['company_name']}"
    
    email_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">Hello {student_name}!</h2>
            <p>We have a new placement opportunity for you:</p>
            
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin-top: 0;">{message_data['title']}</h3>
                <p><strong>Company:</strong> {message_data['company_name']}</p>
                <p><strong>Job Title:</strong> {message_data['job_title']}</p>
                
                {f'<p><strong>CTC for UG:</strong> {message_data["ctc_ug"]}</p>' if message_data.get('ctc_ug') else ''}
                {f'<p><strong>CTC for PG:</strong> {message_data["ctc_pg"]}</p>' if message_data.get('ctc_pg') else ''}
                {f'<p><strong>Stipend:</strong> {message_data["stipend"]}</p>' if message_data.get('stipend') else ''}
                
                {f'<p><strong>Eligibility:</strong> {message_data["eligibility"]}</p>' if message_data.get('eligibility') else ''}
                
                {f'<p><strong>Registration Link:</strong> <a href="{message_data["registration_link"]}" style="color: #3498db;">Click here to register</a></p>' if message_data.get('registration_link') else ''}
                
                {f'<p><strong>Additional Notes:</strong> {message_data["additional_notes"]}</p>' if message_data.get('additional_notes') else ''}
            </div>
            
            <p>Best regards,<br>Placement Cell - KLU</p>
        </div>
    </body>
    </html>
    """
    
    return telegram_message, email_subject, email_html

def process_excel_file(file_path):
    """Process uploaded Excel file and extract student data."""
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Check if required columns exist
        required_columns = ['name', 'email']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return None, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Clean data
        df = df.dropna(subset=['name', 'email'])
        df['name'] = df['name'].astype(str).str.strip()
        df['email'] = df['email'].astype(str).str.strip()
        
        # Filter valid emails
        df = df[df['email'].str.contains('@', na=False)]
        
        if df.empty:
            return None, "No valid student data found in the file"
        
        # Convert to list of dictionaries
        students = df[['name', 'email']].to_dict('records')
        
        return students, f"Successfully processed {len(students)} students"
        
    except Exception as e:
        return None, f"Error processing Excel file: {str(e)}"

# Routes
@app.route('/')
def index():
    """Home page - shows project information and features."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login successful! Welcome to the admin panel.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Admin logout."""
    session.pop('admin_logged_in', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# User Authentication Routes
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    """User login page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # For demo purposes, we'll use a simple check
        # In production, use proper password hashing
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                login_user(user)
                flash('Login successful! Welcome back.', 'success')
                return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid email or password. Please try again.', 'error')
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('user_login.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    """User registration page."""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        if email and name and password:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered. Please login instead.', 'error')
                return redirect(url_for('user_login'))
            
            # Create new user
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            flash('Registration successful! Please complete your profile.', 'success')
            return redirect(url_for('profile_setup'))
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('user_register.html')

@app.route('/user/logout')
@login_required
def user_logout():
    """User logout."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/profile-setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    """User profile setup page."""
    if request.method == 'POST':
        current_user.student_id = request.form.get('student_id')
        current_user.department = request.form.get('department')
        current_user.year = request.form.get('year')
        current_user.phone = request.form.get('phone')
        current_user.telegram_chat_id = request.form.get('telegram_chat_id')
        current_user.profile_completed = True
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('profile_setup.html')

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """User dashboard."""
    # Get all placement messages
    messages = PlacementMessage.query.order_by(PlacementMessage.created_at.desc()).all()
    return render_template('student/dashboard.html', messages=messages)

@app.route('/career-guidance')
@login_required
def career_guidance():
    """Career guidance page."""
    return render_template('student/career_guidance.html')

@app.route('/api/update-placement-status', methods=['POST'])
@login_required
def update_placement_status():
    """Update user's placement status."""
    data = request.get_json()
    status = data.get('status')
    
    if status in ['placed', 'unplaced']:
        current_user.placement_status = status
        db.session.commit()
        return jsonify({'success': True, 'message': 'Status updated successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid status'})

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard."""
    # Check if admin is logged in
    if not session.get('admin_logged_in'):
        flash('Please login to access the admin panel.', 'error')
        return redirect(url_for('login'))
    
    # Get recent messages (last 10)
    recent_messages = message_history[-10:] if message_history else []
    return render_template('admin/dashboard.html', recent_messages=recent_messages)

@app.route('/admin/create-message', methods=['GET', 'POST'])
def create_message():
    """Create new placement message."""
    # Check if admin is logged in
    if not session.get('admin_logged_in'):
        flash('Please login to access the admin panel.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        message_data = {
            'title': request.form.get('title'),
            'company_name': request.form.get('company_name'),
            'job_title': request.form.get('job_title'),
            'ctc_ug': request.form.get('ctc_ug'),
            'ctc_pg': request.form.get('ctc_pg'),
            'stipend': request.form.get('stipend'),
            'eligibility': request.form.get('eligibility'),
            'registration_link': request.form.get('registration_link'),
            'additional_notes': request.form.get('additional_notes')
        }
        
        # Save message to database
        placement_message = PlacementMessage(
            title=message_data['title'],
            company_name=message_data['company_name'],
            job_title=message_data['job_title'],
            ctc_ug=message_data['ctc_ug'],
            ctc_pg=message_data['ctc_pg'],
            stipend=message_data['stipend'],
            eligibility=message_data['eligibility'],
            registration_link=message_data['registration_link'],
            additional_notes=message_data['additional_notes']
        )
        db.session.add(placement_message)
        db.session.commit()
        
        # Store message data in session for sending
        session['message_data'] = message_data
        
        flash('Message created successfully! Now upload student list to send notifications.', 'success')
        return redirect(url_for('upload_students'))
    
    return render_template('admin/create_message.html')

@app.route('/admin/upload-students', methods=['GET', 'POST'])
def upload_students():
    """Upload student list and send messages."""
    # Check if admin is logged in
    if not session.get('admin_logged_in'):
        flash('Please login to access the admin panel.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Check if file is uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('upload_students'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('upload_students'))
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            flash('Please upload an Excel file (.xlsx or .xls)', 'error')
            return redirect(url_for('upload_students'))
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            file.save(tmp_file.name)
            tmp_file.close()  # Close the file handle to release it
            
            # Process Excel file
            students, message = process_excel_file(tmp_file.name)
            
            if students is None:
                flash(f'Error: {message}', 'error')
                return redirect(url_for('upload_students'))
            
            # Get message data from session
            message_data = session.get('message_data')
            if not message_data:
                flash('Please create a message first', 'error')
                return redirect(url_for('create_message'))
            
            # Send messages
            send_messages_to_students(students, message_data)
            
            # Store message in history
            message_record = {
                'id': len(message_history) + 1,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'company_name': message_data['company_name'],
                'job_title': message_data['job_title'],
                'student_count': len(students),
                'status': 'sent'
            }
            message_history.append(message_record)
            
            # Clean up temporary file
            try:
                os.unlink(tmp_file.name)
            except PermissionError:
                # File might still be in use, ignore the error
                logger.warning(f"Could not delete temporary file: {tmp_file.name}")
            except Exception as e:
                logger.warning(f"Error deleting temporary file: {e}")
            
            flash(f'Successfully sent messages to {len(students)} students!', 'success')
            return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/upload_students.html')

def send_messages_to_students(students, message_data):
    """Send messages to all students."""
    async def send_all_messages():
        telegram_success_count = 0
        email_success_count = 0
        
        # Send to Telegram group
        if TELEGRAM_GROUP_ID:
            logger.info(f"Attempting to send Telegram message to group: {TELEGRAM_GROUP_ID}")
            telegram_message = f"📢 **New Placement Opportunity!**\n\n"
            telegram_message += f"**Company:** {message_data['company_name']}\n"
            telegram_message += f"**Job Title:** {message_data['job_title']}\n"
            
            if message_data.get('ctc_ug'):
                telegram_message += f"**UG CTC:** {message_data['ctc_ug']}\n"
            if message_data.get('ctc_pg'):
                telegram_message += f"**PG CTC:** {message_data['ctc_pg']}\n"
            if message_data.get('stipend'):
                telegram_message += f"**Stipend:** {message_data['stipend']}\n"
            
            if message_data.get('eligibility'):
                telegram_message += f"\n**Eligibility:** {message_data['eligibility']}\n"
            
            if message_data.get('registration_link'):
                telegram_message += f"\n**Registration Link:** {message_data['registration_link']}\n"
            
            if message_data.get('additional_notes'):
                telegram_message += f"\n**Additional Notes:** {message_data['additional_notes']}\n"
            
            # Add student count info
            telegram_message += f"\n📊 **Total Students Notified:** {len(students)}"
            
            telegram_success = await send_telegram_message(TELEGRAM_GROUP_ID, telegram_message)
            if telegram_success:
                telegram_success_count = 1
                logger.info(f"Telegram message sent successfully to group {TELEGRAM_GROUP_ID}")
            else:
                logger.error(f"Failed to send Telegram message to group {TELEGRAM_GROUP_ID}")
        else:
            logger.warning("Telegram group ID not configured")
        
        # Send individual emails
        for student in students:
            telegram_msg, email_subject, email_html = create_placement_message_content(message_data, student['name'])
            
            # Send email
            email_success = send_email(student['email'], email_subject, email_html)
            if email_success:
                email_success_count += 1
        
        logger.info(f"Message delivery completed: {telegram_success_count} Telegram, {email_success_count} Emails")
    
    # Run async function
    asyncio.run(send_all_messages())

@app.route('/admin/send-test', methods=['POST'])
def send_test_message():
    """Send test message to verify configuration."""
    # Check if admin is logged in
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Please login to access the admin panel.'})
    
    try:
        test_data = {
            'title': 'Test Message',
            'company_name': 'Test Company',
            'job_title': 'Test Position',
            'ctc_ug': '3-5 LPA',
            'stipend': 'Rs. 15k/month',
            'eligibility': 'Test eligibility criteria',
            'registration_link': 'https://example.com',
            'additional_notes': 'This is a test message'
        }
        
        # Send to Telegram group
        if TELEGRAM_GROUP_ID:
            logger.info(f"Attempting to send test message to group: {TELEGRAM_GROUP_ID}")
            telegram_message = f"🧪 **Test Message**\n\nThis is a test message to verify the system is working correctly.\n\n**Company:** {test_data['company_name']}\n**Job Title:** {test_data['job_title']}\n\n✅ If you see this message, Telegram is working properly!"
            telegram_success = asyncio.run(send_telegram_message(TELEGRAM_GROUP_ID, telegram_message))
            if telegram_success:
                logger.info(f"Test message sent successfully to group {TELEGRAM_GROUP_ID}")
            else:
                logger.error(f"Failed to send test message to group {TELEGRAM_GROUP_ID}")
        else:
            logger.warning("Telegram group ID not configured for test message")
        
        # Send test email
        test_email = request.json.get('test_email', GMAIL_USER)
        telegram_msg, email_subject, email_html = create_placement_message_content(test_data, 'Test User')
        send_email(test_email, email_subject, email_html)
        
        return jsonify({'success': True, 'message': 'Test message sent successfully'})
        
    except Exception as e:
        logger.error(f"Test message error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/template')
def download_template():
    """Download Excel template for student list."""
    # Check if admin is logged in
    if not session.get('admin_logged_in'):
        flash('Please login to access the admin panel.', 'error')
        return redirect(url_for('login'))
    
    # Create a simple template
    template_data = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'email': ['john@klu.ac.in', 'jane@klu.ac.in', 'bob@klu.ac.in']
    }
    
    df = pd.DataFrame(template_data)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        df.to_excel(tmp_file.name, index=False)
        
        from flask import send_file
        return send_file(
            tmp_file.name,
            as_attachment=True,
            download_name='student_list_template.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)