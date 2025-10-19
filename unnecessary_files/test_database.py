#!/usr/bin/env python3
"""
Database connection and data verification script
"""

from app import app, db
from models import Event, Resource, Contact, Newsletter, ChatSession, ChatMessage
from datetime import datetime

def test_database():
    """Test database connection and show stored data"""
    print("=== DATABASE CONNECTION TEST ===")
    
    with app.app_context():
        try:
            # Test connection
            result = db.session.execute(db.text('SELECT 1')).fetchone()
            print("Database connection: SUCCESS")
            
            # Check tables
            print("\n=== DATABASE TABLES ===")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables found: {tables}")
            
            # Count records in each table
            print("\n=== DATA COUNTS ===")
            event_count = Event.query.count()
            resource_count = Resource.query.count()
            contact_count = Contact.query.count()
            newsletter_count = Newsletter.query.count()
            chat_session_count = ChatSession.query.count()
            chat_message_count = ChatMessage.query.count()
            
            print(f"Events: {event_count}")
            print(f"Resources: {resource_count}")
            print(f"Contacts: {contact_count}")
            print(f"Newsletter subscribers: {newsletter_count}")
            print(f"Chat sessions: {chat_session_count}")
            print(f"Chat messages: {chat_message_count}")
            
            # Show sample data
            print("\n=== SAMPLE DATA ===")
            if event_count > 0:
                print("\n--- EVENTS ---")
                events = Event.query.limit(3).all()
                for event in events:
                    print(f"ID: {event.id}, Title: {event.title}")
                    print(f"    Date: {event.date}, Location: {event.location}")
                    print(f"    Description: {event.description[:100]}...")
                    print()
            
            if resource_count > 0:
                print("\n--- RESOURCES ---")
                resources = Resource.query.limit(3).all()
                for resource in resources:
                    print(f"ID: {resource.id}, Title: {resource.title}")
                    print(f"    Category: {resource.category}")
                    print(f"    Description: {resource.description[:100]}...")
                    print()
            
            if contact_count > 0:
                print("\n--- CONTACTS ---")
                contacts = Contact.query.limit(3).all()
                for contact in contacts:
                    print(f"ID: {contact.id}, Name: {contact.name}")
                    print(f"    Email: {contact.email}, Subject: {contact.subject}")
                    print(f"    Message: {contact.message[:100]}...")
                    print()
            
            if newsletter_count > 0:
                print("\n--- NEWSLETTER SUBSCRIBERS ---")
                newsletters = Newsletter.query.limit(5).all()
                for newsletter in newsletters:
                    print(f"ID: {newsletter.id}, Email: {newsletter.email}")
                    print(f"    Active: {newsletter.is_active}, Subscribed: {newsletter.subscribed_at}")
                    print()
            
            if chat_session_count > 0:
                print("\n--- CHAT SESSIONS ---")
                sessions = ChatSession.query.limit(3).all()
                for session in sessions:
                    print(f"ID: {session.id}, Session ID: {session.session_id}")
                    print(f"    Started: {session.started_at}, Active: {session.is_active}")
                    print()
            
            if chat_message_count > 0:
                print("\n--- CHAT MESSAGES ---")
                messages = ChatMessage.query.limit(5).all()
                for message in messages:
                    print(f"ID: {message.id}, Session: {message.session_id}")
                    print(f"    Role: {message.role}, Content: {message.content[:100]}...")
                    print(f"    Timestamp: {message.timestamp}")
                    print()
                    
        except Exception as e:
            print(f"Database connection failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_database()
