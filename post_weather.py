import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BLOG_ID = os.environ.get('BLOG_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')

def main():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )

    service = build('blogger', 'v3', credentials=creds)
    today_date = datetime.now().strftime('%d %B %Y')

    weather_title = f"हवामान अंदाज आणि पिकांचे व्यवस्थापन (IMD & पंजाब डख अपडेट) - {today_date}"
    weather_content = f"""
    <p><b>हॅलो शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: blue;"><b>{today_date}</b></span>) हवामान विशेष अपडेटमध्ये आपले स्वागत आहे.</p>
    <hr>
    <h3>🌦️ हवामान अंदाज</h3>
    <p>हवामान विभागाच्या आणि पंजाब डख यांच्या अंदाजानुसार, आज राज्यातील हवामान कोरडे तसेच काही भागांत ढगाळ राहण्याची शक्यता आहे. शेतकऱ्यांनी आपल्या पिकांचे योग्य नियोजन करावे.</p>
    <p><i>नियमित हवामान अपडेटसाठी 'कृषिवार्ता'ला भेट देत राहा.</i></p>
    """

    res_w = service.posts().insert(blogId=BLOG_ID, body={'title': weather_title, 'content': weather_content}).execute()
    print(f"सकाळची हवामान पोस्ट पब्लिश झाली! ID: {res_w.get('id')}")

if __name__ == '__main__':
    main()
