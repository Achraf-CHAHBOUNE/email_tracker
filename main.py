from flask import Flask, request, redirect, Response
import requests
from supabase import create_client, Client

app = Flask(__name__)

# Replace with your real Supabase credentials
SUPABASE_URL = "https://tqdxelnbesictgfapwca.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRxZHhlbG5iZXNpY3RnZmFwd2NhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NzU5MTIsImV4cCI6MjA2ODI1MTkxMn0._iE9tgg5G1BAiJOMxo2RqmtkKhwABzDZlHDIo5rhOIM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_geo(ip):
    try:
        r = requests.get(f"https://ipwho.is/{ip}").json()
        return r.get("country"), r.get("city")
    except:
        return "Unknown", "Unknown"

@app.route('/open')
def open_tracking():
    email = request.args.get('email')
    ip = request.remote_addr
    country, city = get_geo(ip)
    user_agent = request.headers.get('User-Agent')

    supabase.table("email_tracking").insert({
        "type": "open",
        "email": email,
        "ip": ip,
        "country": country,
        "city": city,
        "user_agent": user_agent
    }).execute()

    pixel = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!" \
            b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01" \
            b"\x00\x00\x02\x02D\x01\x00;"
    return Response(pixel, mimetype='image/gif')

@app.route('/click')
def click_tracking():
    email = request.args.get('email')
    url = request.args.get('url')
    ip = request.remote_addr
    country, city = get_geo(ip)
    user_agent = request.headers.get('User-Agent')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
