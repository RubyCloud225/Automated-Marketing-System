from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from automarket.data.models import Newsletter
import automarket.newsletter_creation.NewsletterGenerator as NewsletterGenerator

app = Flask(__name__)

#Initialise the generator with the database Url
database_url = 'mysql+pymysql://username:password@localhost/db_name'
newsletter_generator = NewsletterGenerator(database_url)

@app.route('/newsletters', methods=['POST'])
def create_newsletters():
    """Create a new newsletter"""
    try: 
        newsletter_content = newsletter_generator.create_newsletter()
        newsletter_id = newsletter_generator.save_newsletter(newsletter_content)
        return jsonify({"id": newsletter_id, "status": "created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/newsletters', methods=['GET'])
def get_pending_newsletters():
    """Get all pending newsletters"""
    try:
        pending_newsletters = newsletter_generator.get_pending_newsletters()
        newsletters_list = [{"id": nl.id, "content": nl.content, "status": nl.status} for nl in pending_newsletters]
        return jsonify(newsletters_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/newsletters', methods=['GET'])
def get_approved_newsletters():
    """Get all approved newsletters"""
    try:
        approved_newsletters = newsletter_generator.get_approved_newsletters()
        newsletters_list = [{"id": nl.id, "content": nl.content, "status": nl.status} for nl in approved_newsletters]
        return jsonify(newsletters_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/newsletters/<int:newsletter_id>', methods=['DELETE'])
def delete_newsletter(newsletter_id):
    """Delete a newsletter by ID"""
    session = newsletter_generator.Session()
    try:
        newsletter = session.query(Newsletter).filter_by(id=newsletter_id).first()
        if newsletter:
            session.delete(newsletter)
            session.commit()
            return jsonify({"status": "deleted"}), 200
        else:
            return jsonify({"status": "Newsletter not found"}), 404
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Newsletter not found"}), 500
    finally:
        session.close()

@app.route('/newsletters/approve/<int:newsletter_id>', methods=['POST'])
def approve_newsletter(newsletter_id):
    """Approve newsletter by Id"""
    try: 
        newsletter = newsletter_generator.approve_newsletter(newsletter_id)
        if newsletter:
            return jsonify({"status": "approved", "id": newsletter_id}), 200
        else:
            return jsonify({"error": "Newsletter not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)