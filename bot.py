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

from bs4 import BeautifulSoup # Add this to your imports

def get_news_headlines():
    # Example using a site that allows scraping
    url = "https://news.ycombinator.com/" 
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Scrape titles from Hacker News
        headlines = [item.text for item in soup.select('.titleline > a')[:5]]
        return headlines
    except Exception as e:
        return [f"Error fetching news: {e}"]

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
    headlines = get_news_headlines()

    # Build the HTML string
    html = f"<html><body>"
    html += f"<h1>Pulse Daily Summary - {today}</h1>"
    
    html += f"<h2>Weather</h2><p>Temp: {weather_temp:.1f}°C, Condition: {weather_cond}</p>"
    
    html += f"<h2>Quote of the Day</h2><p><i>{quote}</i></p>"
    
    html += f"<h2>This Day in History</h2><p>{history}</p>"
    
    html += "<h2>Top News</h2><ul>"
    for h in headlines:
        html += f"<li>{h}</li>"
    html += "</ul>"
    
    html += "</body></html>"
    
    return html

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
   def send_email(subject, html_content):
    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")
    
    msg = MIMEText(html_content, 'html') # Set type to 'html'
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg) 
 


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


    
