# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) & a quote (zenquotes.io)
# Runs: every day at 8 AM IST via GitHub Actions
# APIs: both free, no API keys needed

import requests
from datetime import date
import os
import smtplib
from email.mime.text import MIMEText
import os
api_key = os.environ.get("WEATHER_API_KEY")

# --- FUNCTION 1: Weather ---
def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

        # Inside your script:
        temp_celsius = kelvin - 273.15
        condition = weather_data['weather'][0]['main'] # Example: "Rain"

        if temp_celsius > 35 or condition == "Rain":
          send_email(f"Alert: Weather is {temp_celsius}°C and it is {condition}!")
          print("Alert send")
    except Exception as e:
        return f"Weather unavailable ({e})"

# --- FUNCTION 2: Quote ---
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}" - {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"
 #----Function 4.the history fact----------#
def get_history_fact():
    try:
        url="https://history.muffinlabs.com/date"
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        data=response.json()
        events_list=data['data']['Events']
        if events_list:
            event_text=events_list[0]['text']
            return f"On this day:{event_text}"
        else:
            return "History fact:No events found for today."
    except Exception as e:
        return f"History fact unavailable {e}"
    

# --- FUNCTION 3: Build the summary ---
def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime('%A, %d %B %Y')
    weather = get_weather()
    quote = get_quote()
    history=get_history_fact()

    # Triple quoted strings span multiple lines - great for formatted output
    summary = f"""
-----------------------------------------
PULSE - Daily Summary
{today}
-----------------------------------------

WEATHER
{weather}

TODAY'S QUOTE
{quote}


THIS DAY IN HISTORY
{history}


=========================================
"""
    return summary
    
#----send email defined--------#
def send_email(summary_text):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")
    
    msg = MIMEText(summary_text) 
    msg['Subject'] = "Pulse-Daily Summary"
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg) 
    print("Email sent.")
 


# --- FUNCTION 4: Run everything ---
def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()

    # Print to the GitHub Actions log (visible in the Actions tab)
    print(summary)

    # Save to a file uploaded as a downloadable artifact by the workflow
    with open('daily_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    send_email(summary)

    print("Pulse ran successfully.")

# --- Entry point guard ---
# Only runs when you execute: python bot.py
# Does NOT run when another file imports bot.py
if __name__ == "__main__":
    run()


    
