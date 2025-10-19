#!/usr/bin/env python3
"""
Interactive database viewer
"""

from app import app, db
from models import Event, Resource, Contact, Newsletter, ChatSession, ChatMessage

def view_database():
    """Interactive database viewer"""
    with app.app_context():
        while True:
            print("\n" + "="*50)
            print("MIC INNOVATION DATABASE VIEWER")
            print("="*50)
            print("1. View Events")
            print("2. View Resources") 
            print("3. View Contacts")
            print("4. View Newsletter Subscribers")
            print("5. View All Data Summary")
            print("6. Add New Event")
            print("7. Add New Resource")
            print("8. Exit")
            print("="*50)
            
            choice = input("Choose an option (1-8): ").strip()
            
            if choice == "1":
                print("\nEVENTS:")
                print("-" * 30)
                events = Event.query.all()
                if events:
                    for event in events:
                        print(f"ID: {event.id}")
                        print(f"Title: {event.title}")
                        print(f"Date: {event.date}")
                        print(f"Location: {event.location}")
                        print(f"Status: {event.status}")
                        print(f"Description: {event.description[:100]}...")
                        print("-" * 30)
                else:
                    print("No events found.")
                    
            elif choice == "2":
                print("\nRESOURCES:")
                print("-" * 30)
                resources = Resource.query.all()
                if resources:
                    for resource in resources:
                        print(f"ID: {resource.id}")
                        print(f"Title: {resource.title}")
                        print(f"Category: {resource.category}")
                        print(f"Featured: {resource.is_featured}")
                        print(f"Description: {resource.description[:100]}...")
                        print("-" * 30)
                else:
                    print("No resources found.")
                    
            elif choice == "3":
                print("\nCONTACTS:")
                print("-" * 30)
                contacts = Contact.query.all()
                if contacts:
                    for contact in contacts:
                        print(f"ID: {contact.id}")
                        print(f"Name: {contact.name}")
                        print(f"Email: {contact.email}")
                        print(f"Subject: {contact.subject}")
                        print(f"Read: {contact.is_read}")
                        print(f"Message: {contact.message[:100]}...")
                        print("-" * 30)
                else:
                    print("No contacts found.")
                    
            elif choice == "4":
                print("\nNEWSLETTER SUBSCRIBERS:")
                print("-" * 30)
                newsletters = Newsletter.query.all()
                if newsletters:
                    for newsletter in newsletters:
                        print(f"ID: {newsletter.id}")
                        print(f"Email: {newsletter.email}")
                        print(f"Active: {newsletter.is_active}")
                        print(f"Subscribed: {newsletter.subscribed_at}")
                        print("-" * 30)
                else:
                    print("No newsletter subscribers found.")
                    
            elif choice == "5":
                print("\nALL DATA SUMMARY:")
                print("-" * 30)
                print(f"Events: {Event.query.count()}")
                print(f"Resources: {Resource.query.count()}")
                print(f"Contacts: {Contact.query.count()}")
                print(f"Newsletter Subscribers: {Newsletter.query.count()}")
                print(f"Chat Sessions: {ChatSession.query.count()}")
                print(f"Chat Messages: {ChatMessage.query.count()}")
                
            elif choice == "6":
                print("\nADD NEW EVENT:")
                print("-" * 30)
                title = input("Event Title: ")
                description = input("Description: ")
                location = input("Location: ")
                
                from datetime import datetime, timedelta
                new_event = Event(
                    title=title,
                    description=description,
                    location=location,
                    date=datetime.now() + timedelta(days=30),
                    status="upcoming"
                )
                db.session.add(new_event)
                db.session.commit()
                print("Event added successfully!")
                
            elif choice == "7":
                print("\nADD NEW RESOURCE:")
                print("-" * 30)
                title = input("Resource Title: ")
                description = input("Description: ")
                category = input("Category: ")
                
                new_resource = Resource(
                    title=title,
                    description=description,
                    category=category,
                    is_featured=False
                )
                db.session.add(new_resource)
                db.session.commit()
                print("Resource added successfully!")
                
            elif choice == "8":
                print("\nGoodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    view_database()
