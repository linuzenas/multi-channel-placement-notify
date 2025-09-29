import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check what values are loaded
print("Environment Variables:")
print(f"SUPABASE_URL: '{os.getenv('SUPABASE_URL')}'")
print(f"SUPABASE_KEY: '{os.getenv('SUPABASE_KEY')[:20]}...'" if os.getenv('SUPABASE_KEY') else "None")

# Test URL format
supabase_url = os.getenv('SUPABASE_URL')
if supabase_url:
    print(f"URL starts with https://: {supabase_url.startswith('https://')}")
    print(f"URL length: {len(supabase_url)}")
else:
    print("SUPABASE_URL is None")