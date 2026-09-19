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

    # आजची तारीख मिळवणे
    today_date = datetime.now().strftime('%d %B %Y')

    # दैनिक कृषी बाजारभाव आणि हवामान अहवाल (मजकूर)
    title = f"आजचे कृषी बाजारभाव आणि हवामान अंदाज - {today_date}"
    
    content = f"""
    <p><b>हॅलो शेतकरी बंधूंनो,</b></p>
    <p>कृषिवार्ताच्या आजच्या (<span style="color: green;"><b>{today_date}</b></span>) दैनिक अपडेटमध्ये आपले स्वागत आहे. आजचे प्रमुख शेतमाल बाजारभाव आणि हवामान अंदाज खालीलप्रमाणे आहेत:</p>
    
    <hr>
    
    <h3>🌦️ हवामान अंदाज</h3>
    <p>आज राज्यातील हवामानाची स्थिती समाधानकारक राहण्याचा अंदाज आहे. बऱ्याच भागात ऊन आणि काही ठिकाणी हलक्या स्वरूपाचे ढगाळ वातावरण राहू शकते. शेतकऱ्यांनी आपल्या पिकांची मशागत आणि काढणीचे नियोजन हवामानाचा अंदाज घेऊन करावे.</p>
    
    <hr>
    
    <h3>📈 प्रमुख शेतमाल बाजारभाव (दैनिक सरासरी)</h3>
    <ul>
        <li><b>कांदा:</b> आवक चांगली असून सरासरी भाव स्थिर आहेत.</li>
        <li><b>हरभरा:</b> बाजारात मागणी टिकून आहे.</li>
        <li><b>गहू व ज्वारी:</b> स्थानिक बाजारात चांगला उठाव मिळत आहे.</li>
        <li><b>बाजरी व मका:</b> व्यवहार सुरळीत सुरू आहेत.</li>
    </ul>
    
    <p><i>टीप: हे बाजारभाव विविध कृषी उत्पन्न बाजार समितीच्या अंदाजे ट्रेंडवर आधारित आहेत. अचूक आणि सविस्तर दरांसाठी आपल्या जवळील बाजार समितीशी संपर्क साधावा.</i></p>
    
    <p><b>आपला दिवस शुभ जावो! नियमित अपडेटसाठी 'कृषिवार्ता'ला भेट देत राहा.</b></p>
    """

    post_body = {
        'title': title,
        'content': content
    }

    # ब्लॉगरवर पोस्ट पब्लिश करणे
    request = service.posts().insert(blogId=BLOG_ID, body=post_body)
    response = request.execute()
    
    print(f"यशस्वी! बाजारभाव आणि हवामान पोस्ट पब्लिश झाली आहे. Post ID: {response.get('id')}")

if __name__ == '__main__':
    main()
