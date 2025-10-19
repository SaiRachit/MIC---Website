#!/usr/bin/env python3
"""
Simple database initialization script
Creates tables and optionally populates with sample data
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    """Initialize database with tables"""
    try:
        from app import app, db
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("Database tables created successfully")
            
            # Check if we have any data
            from models import Event, Resource, Contact, Newsletter
            
            event_count = Event.query.count()
            resource_count = Resource.query.count()
            contact_count = Contact.query.count()
            newsletter_count = Newsletter.query.count()
            
            print(f"Current data counts:")
            print(f"  - Events: {event_count}")
            print(f"  - Resources: {resource_count}")
            print(f"  - Contacts: {contact_count}")
            print(f"  - Newsletter subscribers: {newsletter_count}")
            
            # Add sample data if no data exists
            if event_count == 0 and resource_count == 0:
                print("\nAdding sample data...")
                add_sample_data()
            
            return True
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def add_sample_data():
    """Add sample data to the database"""
    try:
        from models import Event, Resource, Contact, Newsletter, db
        from datetime import datetime, timedelta
        
        # Sample events
        events = [
            Event(
                title="Innovation Workshop 2024",
                description="Join us for an exciting workshop on innovation and technology.",
                date=datetime.now() + timedelta(days=30),
                location="MIC Innovation Center",
                image_url="",
                status="upcoming"
            ),
            Event(
                title="Tech Talk: AI and Machine Learning",
                description="Learn about the latest trends in AI and machine learning.",
                date=datetime.now() + timedelta(days=45),
                location="Online",
                image_url="",
                status="upcoming"
            )
        ]
        
        # Sample resources
        resources = [
            Resource(
                title="Innovation Guide 2024",
                description="A comprehensive guide to innovation in the modern world.",
                category="Guide",
                file_url="",
                is_featured=True
            ),
            Resource(
                title="Technology Trends Report",
                description="Latest technology trends and predictions.",
                category="Report",
                file_url="",
                is_featured=False
            )
        ]
        
        # Sample contacts
        contacts = [
            Contact(
                name="John Doe",
                email="john@example.com",
                subject="Inquiry about Innovation Programs",
                message="I'm interested in learning more about your innovation programs.",
                phone="+1234567890",
                company="Tech Corp"
            ),
            Contact(
                name="Jane Smith",
                email="jane@example.com",
                subject="Partnership Opportunity",
                message="We would like to explore partnership opportunities with MIC.",
                phone="+0987654321",
                company="Innovation Labs"
            )
        ]
        
        # Sample newsletter subscribers
        newsletters = [
            Newsletter(email="subscriber1@example.com"),
            Newsletter(email="subscriber2@example.com"),
            Newsletter(email="subscriber3@example.com")
        ]
        
        # Add to database
        for event in events:
            db.session.add(event)
        
        for resource in resources:
            db.session.add(resource)
            
        for contact in contacts:
            db.session.add(contact)
            
        for newsletter in newsletters:
            db.session.add(newsletter)
        
        db.session.commit()
        print("Sample data added successfully")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.session.rollback()

def main():
    """Main function"""
    print("MIC Innovation Database Initialization")
    print("=" * 45)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print(".env file not found. Please create one first.")
        return False
    
    # Initialize database
    if init_database():
        print("\nDatabase initialization completed successfully!")
        print("You can now run your Flask application with: python run.py")
        return True
    else:
        print("\nDatabase initialization failed!")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
