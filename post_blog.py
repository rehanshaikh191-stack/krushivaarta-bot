import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# GitHub Secrets मधून क्रेडेंशियल्स मिळवणे
BLOG_ID = os.environ.get('BLOG_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')

def main():
    # ऑथेंटिकेशन सेट करणे
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )

    # Blogger API सर्विस सुरू करणे
    service = build('blogger', 'v3', credentials=creds)
    today_date = datetime.now().strftime('%d %B %Y')

    # ==========================================
    # १. हवामान अंदाज स्वतंत्र लेख (Weather Article)
    # ==========================================
    weather_title = f"हवामान अंदाज आणि पिकांचे व्यवस्थापन - {today_date}"
    weather_content = f"""
    <p><b>हॅलो शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: blue;"><b>{today_date}</b></span>) हवामान विशेष अपडेटमध्ये आपले स्वागत आहे.</p>
    
    <hr>
    
    <h3>🌦️ सविस्तर हवामान अंदाज</h3>
    <p>आज राज्यातील हवामानाची स्थिती समाधानकारक राहण्याचा अंदाज आहे. बऱ्याच भागात ऊन आणि काही ठिकाणी हलक्या स्वरूपाचे ढगाळ वातावरण राहू शकते. शेतकऱ्यांनी आपल्या पिकांची मशागत आणि काढणीचे नियोजन हवामानाचा अंदाज घेऊन करावे.</p>
    
    <p><b>विशेष शेती सल्ला:</b> काढणीला आलेल्या पिकांचे योग्य व्यवस्थापन ठेवावे.</p>
    <p><i>नियमित हवामान अपडेट्ससाठी 'कृषिवार्ता'ला भेट देत राहा.</i></p>
    """

    weather_body = {
        'title': weather_title,
        'content': weather_content
    }
    
    res_weather = service.posts().insert(blogId=BLOG_ID, body=weather_body).execute()
    print(f"यशस्वी! हवामान अंदाज पोस्ट तयार झाली. Post ID: {res_weather.get('id')}")

    # ==========================================
    # २. दैनिक बाजारभाव स्वतंत्र लेख (Market Rate Article)
    # ==========================================
    market_title = f"आजचे कृषी उत्पन्न बाजारभाव (दैनिक सरासरी) - {today_date}"
    market_content = f"""
    <p><b>शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: green;"><b>{today_date}</b></span>) दैनिक बाजारभाव अहवालात आपले स्वागत आहे. प्रमुख शेतमाल बाजारभाव खालीलप्रमाणे आहेत:</p>
    
    <hr>
    
    <h3>📈 प्रमुख शेतमाल बाजारभाव (सरासरी दर)</h3>
    <ul>
        <li><b>कांदा:</b> आवक चांगली असून सरासरी भाव स्थिर आहेत.</li>
        <li><b>हरभरा:</b> बाजारात मागणी टिकून आहे.</li>
        <li><b>गहू व ज्वारी:</b> स्थानिक बाजारात चांगला उठाव मिळत आहे.</li>
        <li><b>बाजरी व मका:</b> व्यवहार सुरळीत सुरू आहेत.</li>
    </ul>
    
    <p><i>टीप: हे बाजारभाव विविध कृषी उत्पन्न बाजार समितीच्या अंदाजे ट्रेंडवर आधारित आहेत. अचूक दरांसाठी जवळील बाजार समितीशी संपर्क साधावा.</i></p>
    """

    market_body = {
        'title': market_title,
        'content': market_content
    }

    res_market = service.posts().insert(blogId=BLOG_ID, body=market_body).execute()
    print(f"यशस्वी! बाजारभाव पोस्ट तयार झाली. Post ID: {res_market.get('id')}")

if __name__ == '__main__':
    main()
