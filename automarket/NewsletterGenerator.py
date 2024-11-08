import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Fetch_articles import Article
from models import Newsletter

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
    
    def create_newsletter(self):
        """Create a newsletter by fetching articles and generating summaries."""
        articles = self.fetch_articles()
        newsletter_sections = []
        for article in articles:
            summary = self.generate_summary(article.content) # Generate a summary for each article
            #Format article title and summary to the newsletter sections
            newsletter_sections.append(f"**{article.title}**\n\n{summary}\n\n")
        # Join all the sections into a single string to form the complete newsletter
        newsletter_content = "/n".join(newsletter_sections)

        #Add header and footer, content and footer
        header = "### Your Weekly Newsletter \n\n"
        footer = "\n---\nThank you for reading! feel free to email for how we can help you.\n"
        complete_newsletter = f"{header}{newsletter_content}{footer}"
        return complete_newsletter # return the complete newsletter
    
    def save_newsletter(self, newsletter_content):
        """Save the newsletter content to the SQL Server database"""
        #Create a new Newsletter instance
        new_newsletter = Newsletter(content=newsletter_content)
        #add and commit the new newsletter to the database
        session = self.session.add(new_newsletter)
        session.commit()
        return new_newsletter.id #Return the ID of the saved newsletter
    
    def get_pending_newsletters(self):
        pending_newsletters = self.session.query(Newsletter).filter_by(status='pending').all()
        return pending_newsletters
    
    def approve_newsletter(self, newsletter_id):
        newsletter = self.session.query(Newsletter).filter_by(id=newsletter_id).first()
        if newsletter:
            newsletter.status = 'approved'
            self.session.commit()
        return newsletter
    
    def get_approved_newsletters(self):
        approved_newsletters = self.session.query(Newsletter).filter_by(status='approved').all()
        return approved_newsletters

