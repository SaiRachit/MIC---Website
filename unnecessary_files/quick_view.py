#!/usr/bin/env python3
"""
Quick database viewer - shows all data without interaction
"""

from app import app, db
from models import Event, Resource, Contact, Newsletter

def quick_view():
    """Show all database data quickly"""
    with app.app_context():
        print("=" * 60)
        print("MIC INNOVATION DATABASE - QUICK VIEW")
        print("=" * 60)
        
        # Events
        print("\nEVENTS:")
        print("-" * 40)
        events = Event.query.all()
        for event in events:
            print(f"• {event.title}")
            print(f"  Date: {event.date.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Location: {event.location}")
            print(f"  Status: {event.status}")
            print()
        
        # Resources
        print("\nRESOURCES:")
        print("-" * 40)
        resources = Resource.query.all()
        for resource in resources:
            print(f"• {resource.title}")
            print(f"  Category: {resource.category}")
            print(f"  Featured: {'Yes' if resource.is_featured else 'No'}")
            print()
        
        # Contacts
        print("\nCONTACTS:")
        print("-" * 40)
        contacts = Contact.query.all()
        for contact in contacts:
            print(f"• {contact.name} ({contact.email})")
            print(f"  Subject: {contact.subject}")
            print(f"  Read: {'Yes' if contact.is_read else 'No'}")
            print()
        
        # Newsletter
        print("\nNEWSLETTER SUBSCRIBERS:")
        print("-" * 40)
        newsletters = Newsletter.query.all()
        for newsletter in newsletters:
            print(f"• {newsletter.email}")
            print(f"  Active: {'Yes' if newsletter.is_active else 'No'}")
            print(f"  Subscribed: {newsletter.subscribed_at.strftime('%Y-%m-%d')}")
            print()
        
        # Summary
        print("\nSUMMARY:")
        print("-" * 40)
        print(f"Total Events: {Event.query.count()}")
        print(f"Total Resources: {Resource.query.count()}")
        print(f"Total Contacts: {Contact.query.count()}")
        print(f"Total Newsletter Subscribers: {Newsletter.query.count()}")
        print("=" * 60)

if __name__ == '__main__':
    quick_view()
