#!/usr/bin/env python3
"""
Database initialization script
"""
from app import app, db
from models import Event, Resource, Contact, Newsletter
from datetime import datetime, timedelta

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if Event.query.first():
            print("Database already initialized")
            return
        
        # Create sample events
        events = [
            Event(
                title="Innovation Summit 2025",
                description="Join us for the biggest innovation event of the year featuring industry leaders, startup showcases, and networking opportunities.",
                date=datetime.now() + timedelta(days=30),
                location="MAHE Campus Auditorium",
                attendees=500,
                price="Free",
                status="upcoming"
            ),
            Event(
                title="Startup Pitch Competition",
                description="Witness innovative startups pitch their ideas to investors and industry experts. Winner gets funding and mentorship.",
                date=datetime.now() + timedelta(days=45),
                location="Innovation Hub",
                attendees=200,
                price="Free",
                status="upcoming"
            ),
            Event(
                title="AI & ML Workshop",
                description="Hands-on workshop covering the latest trends in Artificial Intelligence and Machine Learning with practical applications.",
                date=datetime.now() + timedelta(days=60),
                location="Computer Lab 3",
                attendees=50,
                price="Free",
                status="upcoming"
            )
        ]
        
        for event in events:
            db.session.add(event)
        
        # Create sample resources
        resources = [
            Resource(
                title="Innovation Toolkit",
                description="Complete toolkit for innovators including design thinking frameworks, prototyping tools, and validation methods.",
                category="toolkit",
                format="PDF",
                duration="2 Hours Read",
                rating=4.8,
                is_featured=True
            ),
            Resource(
                title="Startup Guide",
                description="Comprehensive guide covering business model canvas, funding strategies, and market analysis techniques.",
                category="guide",
                format="PDF",
                duration="3 Hours Read",
                rating=4.9,
                is_featured=True
            ),
            Resource(
                title="Mentorship Program",
                description="Connect with industry mentors and get personalized guidance for your entrepreneurial journey.",
                category="mentorship",
                format="Video",
                duration="Monthly Meetings",
                rating=4.7,
                is_featured=True
            )
        ]
        
        for resource in resources:
            db.session.add(resource)
        
        # Create sample newsletter subscribers
        newsletters = [
            Newsletter(email="subscriber1@example.com"),
            Newsletter(email="subscriber2@example.com"),
            Newsletter(email="subscriber3@example.com")
        ]
        
        for newsletter in newsletters:
            db.session.add(newsletter)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully with sample data")

if __name__ == '__main__':
    init_database()
