from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from automarket.models import Url, Article

#Initialize Flask app
app = Flask(__name__)

# UrlManager class to manage URLs
class UrlManager:
    def __init__(self, session):
        self.session = session()
    
    def add_url(self, url):
        """Add a new URL to the URL's table if it doesn't already exist."""
        if not self.session.query(Url).filter_by(url=url).first():
            new_url = Url(url=url)
            self.session.add(new_url)
            self.session.commit()
            return f"URL '{url}' added successfully."
        return f"URL '{url}' already exists."
    
    def get_unprocessed_urls(self):
        return self.session.query(Url).fiter_by(processed=False).all()
    
    def mark_as_processed(self, url):
        url_entry = self.session.query(Url).filter_by(url=url).first()
        if url_entry:
            url_entry.processed = True
            self.session.commit()
    
    def close_session(self):
        self.session.close()


# ArticleFetcher class to fetch, parse and save articles
class ArticleFetcher:
    def __init__(self):
        self.session = Session()
        self.url_manager = UrlManager()

    def fetch_and_save_article(self):
        # Fetch article content from URL
        urls = self.url_manager.get_unprocessed_urls()

        for url_entry in urls:
            url = url_entry.url

            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch article")
                continue
        
        # Parse the article content
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        content = soup.find('div', {'class': 'article-content'}).text

        # Save article to database
        article = Article(title=title, content=content, url=url)
        self.session.add(article)
        self.session.commit()

        # Mark the URL as processed
        self.url_manager.mark_as_processed(url)
        print(f"Article '{title}' saved and URL '{url}' marked as processed.")
    
    def close_session(self):
        self.session.close()
        self.url_manager.close_session()

#Flask route to add a URL to the database
@app.route('/add_url', methods=['POST'])
def add_url():
    data = request.json
    url = data.get('url')

    if not url: 
        return jsonify({"error": "URL is required"}), 400
    
    url_manager = UrlManager()
    result = url_manager.add_url(url)
    url_manager.close_session()

    return jsonify({"message": result})

@app.route('/fetcharticle', methods=['POST'])
def fetch_article():
    fetcher = ArticleFetcher()
    result = fetcher.fetch_and_save_article()
    fetcher.close_session()
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)
