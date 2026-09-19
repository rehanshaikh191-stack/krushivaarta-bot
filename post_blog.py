import os
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

    # कृषिवार्ता ब्लॉगसाठी पोस्टचा मजकूर
    post_body = {
        'title': 'कृषिवार्ता स्वयंचलित अपडेट',
        'content': '<p>हॅलो शेतकरी बंधूंनो, ही GitHub Actions द्वारे स्वयंचलितपणे पब्लिश केलेली टेस्ट पोस्ट आहे.</p>'
    }

    # ब्लॉगरवर पोस्ट पब्लिश करणे
    request = service.posts().insert(blogId=BLOG_ID, body=post_body)
    response = request.execute()
    
    print(f"यशस्वी! पोस्ट पब्लिश झाली आहे. Post ID: {response.get('id')}")

if __name__ == '__main__':
    main()
