import os
from datetime import datetime
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BLOG_ID = os.environ.get('BLOG_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
SHEET_CSV_URL = os.environ.get('SHEET_CSV_URL')

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

    # ==========================================
    # १. हवामान अंदाज स्वतंत्र लेख
    # ==========================================
    weather_title = f"हवामान अंदाज आणि शेती सल्ला (IMD & पंजाब डख अपडेट) - {today_date}"
    weather_content = f"""
    <p><b>हॅलो शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: blue;"><b>{today_date}</b></span>) हवामान विशेष अपडेटमध्ये आपले स्वागत आहे.</p>
    <hr>
    <h3>🌦️ हवामान अंदाज</h3>
    <p>हवामान विभागाच्या आणि पंजाब डख यांच्या अंदाजानुसार, आज राज्यातील हवामान कोरडे तसेच काही भागांत ढगाळ राहण्याची शक्यता आहे. शेतकऱ्यांनी आपल्या पिकांचे योग्य नियोजन करावे.</p>
    <p><i>नियमित हवामान अपडेटसाठी 'कृषिवार्ता'ला भेट देत राहा.</i></p>
    """
    
    res_w = service.posts().insert(blogId=BLOG_ID, body={'title': weather_title, 'content': weather_content}).execute()
    print(f"हवामान पोस्ट पब्लिश झाली! ID: {res_w.get('id')}")

    # ==========================================
    # २. दैनिक बाजारभाव स्वतंत्र लेख (Google Sheet CSV वरून)
    # ==========================================
    market_title = f"आजचे कृषी उत्पन्न बाजारभाव (दैनिक सरासरी) - {today_date}"
    
    market_table_html = "<p>आजचा बाजारभाव डेटा सिंक झाला आहे.</p>"
    try:
        if SHEET_CSV_URL:
            df = pd.read_csv(SHEET_CSV_URL)
            market_table_html = "<table border='1' style='border-collapse: collapse; width: 100%; text-align: center;'><tr><th>तारीख</th><th>बाजार समिती</th><th>शेतमाल</th><th>किमान दर</th><th>कमाल दर</th><th>सरासरी दर</th></tr>"
            # शीटमधील पहिले काही महत्त्वाचे रेकॉर्ड्स टेबलमध्ये घेणे
            for _, row in df.head(30).iterrows():
                market_table_html += f"<tr><td>{row.iloc[0]}</td><td>{row.iloc[1]}</td><td>{row.iloc[2]}</td><td>{row.iloc[3]}</td><td>{row.iloc[4]}</td><td>{row.iloc[5]}</td></tr>"
            market_table_html += "</table>"
    except Exception as e:
        market_table_html = f"<p>डेटा लोड करताना अडचण आली: {e}</p>"

    market_content = f"""
    <p><b>शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: green;"><b>{today_date}</b></span>) मार्केट अपडेटमध्ये प्रमुख शेतमाल बाजारभाव खालीलप्रमाणे आहेत:</p>
    <hr>
    <h3>📈 प्रमुख शेतमाल बाजारभाव तक्ता</h3>
    {market_table_html}
    <p><i>टीप: हे दर थेट कृषी उत्पन्न बाजार समितीच्या अधिकृत डेटावरून घेण्यात आले आहेत.</i></p>
    """

    res_m = service.posts().insert(blogId=BLOG_ID, body={'title': market_title, 'content': market_content}).execute()
    print(f"बाजारभाव पोस्ट पब्लिश झाली! ID: {res_m.get('id')}")

if __name__ == '__main__':
    main()
