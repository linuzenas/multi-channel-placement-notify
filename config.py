#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for Placement Messenger application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Email Configuration
    GMAIL_USER = os.getenv('GMAIL_USER')
    GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
    
    # Telegram Configuration
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
    
    # Application Settings
    ALLOWED_FILE_EXTENSIONS = ['.xlsx', '.xls']
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    # Excel Processing
    REQUIRED_COLUMNS = ['name', 'email']
    EXCEL_SHEET_NAME = 0  # First sheet

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}