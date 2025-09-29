#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Placement Messenger

A simple script to send placement messages to students via Telegram and Gmail.
This is a standalone script before integrating with a database or frontend.
"""

import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import sys

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
TELEGRAM_TOKEN = ""  # Replace with your actual token
GMAIL_USER = ""  # Replace with your Gmail address
GMAIL_APP_PASSWORD = ""  # Replace with your Gmail App Password

# Sample student data - In a real application, this would come from a database
STUDENTS = [
    {
        "name": "P Linu Zenas Paul",
        "email": "9923008040@klu.ac.in",
        "telegram_chat_id": "5554791589",  # This must be obtained when student messages the bot first
        "placement": {
            "company": "Tech Solutions Inc.",
            "position": "Software Developer Intern",
            "start_date": "2023-06-01",
            "details": "Congratulations on your placement! Please report to the HR office at 9 AM on your start date."
        }
    },
    {
        "name": "G Hasini",
        "email": "9923008035@klu.ac.in",
        "telegram_chat_id": "5554791589",  # This must be obtained when student messages the bot first
        "placement": {
            "company": "Tech Solutions Inc.",
            "position": "Software Developer Intern",
            "start_date": "2023-06-01",
            "details": "Congratulations on your placement! Please report to the HR office at 9 AM on your start date."
        }
    },
    {
        "name": "T Mahaveer",
        "email": "99220041585@klu.ac.in",
        "telegram_chat_id": "5554791589",
        "placement": {
            "company": "Data Analytics Co.",
            "position": "Data Science Intern",
            "start_date": "2023-06-15",
            "details": "Congratulations on your placement! Please bring your ID and offer letter on your first day."
        }
    }
    
]


async def send_telegram_message(chat_id, message):
    """
    Send a message via Telegram bot.
    
    Args:
        chat_id (str): The chat ID of the recipient
        message (str): The message to send
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Telegram message sent successfully to chat ID: {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send Telegram message to {chat_id}: {e}")
        return False


def send_email(recipient_email, subject, html_content):
    """
    Send an email via Gmail.
    
    Args:
        recipient_email (str): The email address of the recipient
        subject (str): The subject of the email
        html_content (str): The HTML content of the email
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = GMAIL_USER
        message["To"] = recipient_email
        
        # Turn the HTML content into a MIME part
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Create a secure SSL context
        context = ssl.create_default_context()
        
        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipient_email, message.as_string())
        
        logger.info(f"Email sent successfully to: {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {e}")
        return False


def create_placement_message(student):
    """
    Create a placement message for a student.
    
    Args:
        student (dict): The student data
        
    Returns:
        tuple: (telegram_message, email_subject, email_html)
    """
    # Create Telegram message
    telegram_message = f"Hello {student['name']},\n\n"
    telegram_message += f"Congratulations on your placement at {student['placement']['company']} "
    telegram_message += f"as {student['placement']['position']}!\n\n"
    telegram_message += f"Start Date: {student['placement']['start_date']}\n"
    telegram_message += f"Details: {student['placement']['details']}"
    
    # Create email subject
    email_subject = f"Congratulations on your placement at {student['placement']['company']}"
    
    # Create email HTML content
    email_html = f"""
    <html>
    <body>
        <h2>Congratulations, {student['name']}!</h2>
        <p>We are pleased to inform you about your placement:</p>
        <ul>
            <li><strong>Company:</strong> {student['placement']['company']}</li>
            <li><strong>Position:</strong> {student['placement']['position']}</li>
            <li><strong>Start Date:</strong> {student['placement']['start_date']}</li>
        </ul>
        <p>{student['placement']['details']}</p>
        <p>Best regards,<br>Placement Cell</p>
    </body>
    </html>
    """
    
    return telegram_message, email_subject, email_html


async def notify_student(student):
    """
    Send placement notification to a student via both Telegram and email.
    
    Args:
        student (dict): The student data
        
    Returns:
        tuple: (telegram_success, email_success)
    """
    telegram_message, email_subject, email_html = create_placement_message(student)
    
    # Send Telegram message
    telegram_success = await send_telegram_message(
        student["telegram_chat_id"], telegram_message
    )
    
    # Send email
    email_success = send_email(
        student["email"], email_subject, email_html
    )
    
    return telegram_success, email_success


async def main():
    """
    Main function to send placement messages to all students.
    """
    logger.info("Starting placement message delivery")
    
    for student in STUDENTS:
        logger.info(f"Processing student: {student['name']}")
        telegram_success, email_success = await notify_student(student)
        
        if telegram_success and email_success:
            logger.info(f"Successfully notified {student['name']} via both channels")
        elif telegram_success:
            logger.warning(f"Only Telegram notification succeeded for {student['name']}")
        elif email_success:
            logger.warning(f"Only Email notification succeeded for {student['name']}")
        else:
            logger.error(f"Failed to notify {student['name']} via any channel")
    
    logger.info("Placement message delivery completed")


if __name__ == "__main__":
    try:
        # Check if token and email credentials are set
        if TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
            logger.error("Please set your Telegram bot token")
            sys.exit(1)
        if GMAIL_USER == "your.email@gmail.com" or GMAIL_APP_PASSWORD == "your-app-password":
            logger.error("Please set your Gmail credentials")
            sys.exit(1)
            
        # Run the main function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        sys.exit(1)