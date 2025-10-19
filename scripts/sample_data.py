#!/usr/bin/env python3
"""
Sample data initialization script for MAHE Innovation Centre
This script adds sample events, resources, and other data to the database
"""

import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from the backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Event, Resource, Contact, Newsletter

def create_sample_data():
    """Create sample data for the database"""
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(Event).delete()
        db.session.query(Resource).delete()
        db.session.query(Contact).delete()
        db.session.query(Newsletter).delete()
        db.session.commit()
        
        # Create sample events
        print("Creating sample events...")
        events = [
            Event(
                title="Innovation Summit 2025",
                description="Join us for the biggest innovation event of the year featuring industry leaders, startup showcases, and networking opportunities. This summit brings together entrepreneurs, investors, and innovators from across the region.",
                date=datetime.now() + timedelta(days=30),
                location="MAHE Campus Auditorium",
                attendees=500,
                price="Free",
                status="upcoming",
                image_url="https://placehold.co/400x300?text=Innovation+Summit"
            ),
            Event(
                title="Startup Pitch Competition",
                description="Witness innovative startups pitch their ideas to investors and industry experts. Winner gets funding and mentorship opportunities.",
                date=datetime.now() + timedelta(days=45),
                location="Innovation Hub",
                attendees=200,
                price="Free",
                status="upcoming",
                image_url="https://placehold.co/400x300?text=Pitch+Competition"
            ),
            Event(
                title="AI & ML Workshop",
                description="Hands-on workshop covering the latest trends in Artificial Intelligence and Machine Learning with practical applications and real-world projects.",
                date=datetime.now() + timedelta(days=60),
                location="Computer Lab 3",
                attendees=50,
                price="Free",
                status="upcoming",
                image_url="https://placehold.co/400x300?text=AI+Workshop"
            ),
            Event(
                title="Entrepreneurship Bootcamp",
                description="Intensive 3-day bootcamp covering business planning, funding strategies, and market validation techniques for aspiring entrepreneurs.",
                date=datetime.now() + timedelta(days=75),
                location="Business School",
                attendees=30,
                price="₹2,000",
                status="upcoming",
                image_url="https://placehold.co/400x300?text=Bootcamp"
            ),
            Event(
                title="Innovation Networking Mixer",
                description="Connect with fellow innovators, entrepreneurs, and industry professionals in a relaxed networking environment with refreshments.",
                date=datetime.now() + timedelta(days=90),
                location="Innovation Center",
                attendees=150,
                price="Free",
                status="upcoming",
                image_url="https://placehold.co/400x300?text=Networking"
            )
        ]
        
        for event in events:
            db.session.add(event)
        
        # Create sample resources
        print("Creating sample resources...")
        resources = [
            Resource(
                title="Innovation Toolkit",
                description="Complete toolkit for innovators including design thinking frameworks, prototyping tools, and validation methods. Perfect for students and entrepreneurs starting their innovation journey.",
                category="toolkit",
                file_url="https://example.com/innovation-toolkit.pdf",
                download_count=150,
                rating=4.8,
                format="PDF",
                duration="2 Hours Read",
                is_featured=True
            ),
            Resource(
                title="Startup Guide",
                description="Comprehensive guide covering business model canvas, funding strategies, and market analysis techniques. Essential reading for any aspiring entrepreneur.",
                category="guide",
                file_url="https://example.com/startup-guide.pdf",
                download_count=200,
                rating=4.9,
                format="PDF",
                duration="3 Hours Read",
                is_featured=True
            ),
            Resource(
                title="Mentorship Program",
                description="Connect with industry mentors and get personalized guidance for your entrepreneurial journey. One-on-one sessions with experienced professionals.",
                category="mentorship",
                file_url="https://example.com/mentorship-program.pdf",
                download_count=75,
                rating=4.7,
                format="PDF",
                duration="1 Hour Read",
                is_featured=True
            ),
            Resource(
                title="Design Thinking Workshop Materials",
                description="Learn human-centered design approach to solve complex problems and create innovative solutions. Includes templates and exercises.",
                category="workshop",
                file_url="https://example.com/design-thinking.pdf",
                download_count=120,
                rating=4.9,
                format="PDF",
                duration="2 Hours Read",
                is_featured=False
            ),
            Resource(
                title="Funding Strategies Guide",
                description="Comprehensive guide to funding options, investor relations, and financial planning for startups. Includes templates and examples.",
                category="guide",
                file_url="https://example.com/funding-guide.pdf",
                download_count=180,
                rating=4.8,
                format="PDF",
                duration="2.5 Hours Read",
                is_featured=False
            ),
            Resource(
                title="Market Research Tools",
                description="Access to premium market research tools and databases to validate your business ideas. Includes step-by-step guides.",
                category="toolkit",
                file_url="https://example.com/market-research.pdf",
                download_count=90,
                rating=4.6,
                format="PDF",
                duration="1.5 Hours Read",
                is_featured=False
            ),
            Resource(
                title="Prototyping Lab Access",
                description="Access to 3D printers, laser cutters, and other prototyping equipment for product development. Includes safety guidelines and tutorials.",
                category="workshop",
                file_url="https://example.com/prototyping-lab.pdf",
                download_count=60,
                rating=4.9,
                format="PDF",
                duration="1 Hour Read",
                is_featured=False
            )
        ]
        
        for resource in resources:
            db.session.add(resource)
        
        # Create sample contacts
        print("Creating sample contacts...")
        contacts = [
            Contact(
                name="John Doe",
                email="john.doe@example.com",
                subject="general",
                message="I'm interested in learning more about your innovation programs. Can you provide more information about the mentorship opportunities?",
                phone="+91-9876543210",
                company="Tech Startup Inc.",
                is_read=False
            ),
            Contact(
                name="Jane Smith",
                email="jane.smith@example.com",
                subject="partnership",
                message="We would like to explore partnership opportunities with MAHE Innovation Centre. Our company specializes in AI and machine learning solutions.",
                phone="+91-9876543211",
                company="AI Solutions Ltd.",
                is_read=True
            ),
            Contact(
                name="Mike Johnson",
                email="mike.johnson@example.com",
                subject="mentorship",
                message="I'm an experienced entrepreneur and would like to volunteer as a mentor for your programs. How can I get involved?",
                phone="+91-9876543212",
                company="Johnson Enterprises",
                is_read=False
            )
        ]
        
        for contact in contacts:
            db.session.add(contact)
        
        # Create sample newsletter subscriptions
        print("Creating sample newsletter subscriptions...")
        newsletters = [
            Newsletter(email="subscriber1@example.com", is_active=True),
            Newsletter(email="subscriber2@example.com", is_active=True),
            Newsletter(email="subscriber3@example.com", is_active=True),
            Newsletter(email="subscriber4@example.com", is_active=False),  # Unsubscribed
            Newsletter(email="subscriber5@example.com", is_active=True)
        ]
        
        for newsletter in newsletters:
            db.session.add(newsletter)
        
        # Commit all changes
        print("Committing changes to database...")
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print(f"   - {len(events)} events")
        print(f"   - {len(resources)} resources")
        print(f"   - {len(contacts)} contacts")
        print(f"   - {len(newsletters)} newsletter subscriptions")

if __name__ == "__main__":
    create_sample_data()
