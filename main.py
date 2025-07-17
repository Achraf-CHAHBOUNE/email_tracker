from flask import Flask, request, redirect, Response
import requests
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Flask
app = Flask(__name__)

# Setup Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === GeoIP Resolver ===
def get_geo(ip):
    try:
        response = requests.get(f"https://ipwho.is/{ip}", timeout=5).json()
        if not response.get("success", True):
            return "Unknown", "Unknown"
        return response.get("country", "Unknown"), response.get("city", "Unknown")
    except:
        return "Unknown", "Unknown"

# === Open Tracking ===
@app.route('/open')
def open_tracking():
    email = request.args.get('email')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    country, city = get_geo(ip)
    user_agent = request.headers.get('User-Agent')

    # Save to Supabase
    supabase.table("email_tracking").insert({
        "type": "open",
        "email": email,
        "ip": ip,
        "country": country,
        "city": city,
        "user_agent": user_agent
    }).execute()

    # Return 1x1 transparent GIF
    pixel = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!" \
            b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01" \
            b"\x00\x00\x02\x02D\x01\x00;"
    return Response(pixel, mimetype='image/gif')

# === Click Tracking ===
@app.route('/click')
def click_tracking():
    email = request.args.get('email')
    url = request.args.get('url')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    country, city = get_geo(ip)
    user_agent = request.headers.get('User-Agent')

    # Save to Supabase
    supabase.table("email_tracking").insert({
        "type": "click",
        "email": email,
        "url": url,
        "ip": ip,
        "country": country,
        "city": city,
        "user_agent": user_agent
    }).execute()

    return redirect(url)

# === Run Flask App ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
