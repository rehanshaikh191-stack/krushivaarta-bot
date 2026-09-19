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

    market_title = f"आजचे कृषी उत्पन्न बाजारभाव (दैनिक सरासरी) - {today_date}"
    
    market_table_html = "<p>आजचा बाजारभाव डेटा उपलब्ध आहे.</p>"
    try:
        if SHEET_CSV_URL:
            df = pd.read_csv(SHEET_CSV_URL)
            market_table_html = "<table border='1' style='border-collapse: collapse; width: 100%; text-align: center;'><tr><th>तारीख</th><th>बाजार समिती</th><th>शेतमाल</th><th>किमान दर</th><th>कमाल दर</th><th>सरासरी दर</th></tr>"
            for _, row in df.head(30).iterrows():
                market_table_html += f"<tr><td>{row.iloc[0]}</td><td>{row.iloc[1]}</td><td>{row.iloc[2]}</td><td>{row.iloc[3]}</td><td>{row.iloc[4]}</td><td>{row.iloc[5]}</td></tr>"
            market_table_html += "</table>"
    except Exception as e:
        market_table_html = f"<p>डेटा लोड करताना अडचण आली: {e}</p>"

    market_content = f"""
    <p><b>शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: green;"><b>{today_date}</b></span>) संध्याकाळच्या मार्केट अपडेटमध्ये प्रमुख शेतमाल बाजारभाव खालीलप्रमाणे आहेत:</p>
    <hr>
    <h3>📈 प्रमुख शेतमाल बाजारभाव तक्ता</h3>
    {market_table_html}
    <p><i>टीप: हे दर थेट कृषी उत्पन्न बाजार समितीच्या अधिकृत डेटावरून घेण्यात आले आहेत.</i></p>
    """

    res_m = service.posts().insert(blogId=BLOG_ID, body={'title': market_title, 'content': market_content}).execute()
    print(f"संध्याकाळची बाजारभाव पोस्ट पब्लिश झाली! ID: {res_m.get('id')}")

if __name__ == '__main__':
    main()
