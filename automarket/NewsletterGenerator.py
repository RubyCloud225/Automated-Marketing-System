import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Fetch_articles import Article

openai.api_key = 'your_openai_api_key'

class NewsletterGenerator:
    def __init__(self, database_url):
        # Setup SQLAlchemy connection
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def fetch_articles(self, limit=5):
        """Fetch recient articles from the database."""
        session = self.Session()
        articles = session.query(Article).order_by(Article.date.desc()).limit(limit).all()
        session.close()
        return articles
    

    def generate_summary(self, content):
        """Generate a summary of the content using OpenAI's API."""
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summerize the following content for a newsletter"},
                {"role": "user", "content": content}
            ],
            max_tokens=256
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    
    def create_newsletter(self)
        """Create a newsletter by fetching articles and generating summaries."""
        articles = self.fetch_articles()
        newsletter_sections = []
        for article in articles:
            summary = self.generate_summary(article.content)
            newsletter_sections.append(f"**{article.title}**\n\n{summary}\n\n")
        
        
