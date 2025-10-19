#!/usr/bin/env python3
"""
Production database initialization script for Railway deployment
Creates tables and populates with essential data
"""

import os
import sys
from datetime import datetime, timedelta

def init_production_database():
    """Initialize production database with tables and sample data"""
    try:
        from app import app, db
        from models import Event, Resource, Contact, Newsletter
        
        with app.app_context():
            print("Creating database tables...")
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Check if we have any data
            event_count = Event.query.count()
            resource_count = Resource.query.count()
            newsletter_count = Newsletter.query.count()
            
            print(f"Current data counts:")
            print(f"  - Events: {event_count}")
            print(f"  - Resources: {resource_count}")
            print(f"  - Newsletter subscribers: {newsletter_count}")
            
            # Add sample data if no data exists
            if event_count == 0:
                print("\nAdding sample events...")
                add_sample_events()
            
            if resource_count == 0:
                print("Adding sample resources...")
                add_sample_resources()
            
            print("✓ Production database initialized successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error initializing production database: {e}")
        import traceback
        traceback.print_exc()
        return False

def add_sample_events():
    """Add sample events to the database"""
    from app import app, db
    from models import Event
    
    with app.app_context():
        sample_events = [
            {
                'title': 'Innovation Workshop 2024',
                'description': 'Join us for an exciting innovation workshop where we explore cutting-edge technologies and entrepreneurial thinking.',
                'date': datetime.now() + timedelta(days=30),
                'location': 'MAHE Innovation Centre',
                'attendees': 50,
                'price': 'Free',
                'status': 'upcoming'
            },
            {
                'title': 'Startup Pitch Competition',
                'description': 'Showcase your startup idea to industry experts and win exciting prizes.',
                'date': datetime.now() + timedelta(days=45),
                'location': 'MAHE Auditorium',
                'attendees': 100,
                'price': '₹500',
                'status': 'upcoming'
            },
            {
                'title': 'Tech Talk: AI in Healthcare',
                'description': 'Learn about the latest applications of AI in healthcare from industry experts.',
                'date': datetime.now() + timedelta(days=60),
                'location': 'MAHE Innovation Centre',
                'attendees': 75,
                'price': 'Free',
                'status': 'upcoming'
            }
        ]
        
        for event_data in sample_events:
            event = Event(**event_data)
            db.session.add(event)
        
        db.session.commit()
        print(f"✓ Added {len(sample_events)} sample events")

def add_sample_resources():
    """Add sample resources to the database"""
    from app import app, db
    from models import Resource
    
    with app.app_context():
        sample_resources = [
            {
                'title': 'Innovation Toolkit',
                'description': 'Complete toolkit for innovators and entrepreneurs to kickstart their journey.',
                'category': 'toolkit',
                'format': 'PDF',
                'duration': '2 Hours Read',
                'is_featured': True,
                'download_count': 0,
                'rating': 4.5
            },
            {
                'title': 'Startup Guide 2024',
                'description': 'Comprehensive guide to building and scaling your startup in 2024.',
                'category': 'guide',
                'format': 'PDF',
                'duration': '3 Hours Read',
                'is_featured': True,
                'download_count': 0,
                'rating': 4.8
            },
            {
                'title': 'Mentorship Program',
                'description': 'Connect with industry mentors for guidance and support.',
                'category': 'mentorship',
                'format': 'Online',
                'duration': 'Ongoing',
                'is_featured': False,
                'download_count': 0,
                'rating': 4.9
            }
        ]
        
        for resource_data in sample_resources:
            resource = Resource(**resource_data)
            db.session.add(resource)
        
        db.session.commit()
        print(f"✓ Added {len(sample_resources)} sample resources")

if __name__ == "__main__":
    success = init_production_database()
    sys.exit(0 if success else 1)