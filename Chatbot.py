import datetime
import time
import os
import sys
import sqlite3
import json
import uuid
import hashlib

# Optional imports - handle gracefully if not available
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    print("Warning: Groq package not available")
    GROQ_AVAILABLE = False
    Groq = None

try:
    from flask import current_app, request
    from models import Event, Resource, Contact, Newsletter, ChatSession, ChatMessage, db
    FLASK_AVAILABLE = True
except ImportError:
    print("Warning: Flask or models not available")
    FLASK_AVAILABLE = False

Username = os.environ.get("Username", "User")
Assistantname = os.environ.get("Assistantname", "MAHE Innovation Centre Assistant")
GroqAPIKey = os.environ.get("GroqAPIKey")
DB_PATH = os.path.join("instance", "mic_innovation.db")

client = None
if GROQ_AVAILABLE and GroqAPIKey and GroqAPIKey != "your-groq-api-key-here":
    try:
        client = Groq(api_key=GroqAPIKey)
    except Exception as e:
        print(f"Failed to initialize Groq client: {e}")
        client = None
else:
    print("Groq client not available - API key missing or package not installed")

System = f"""You are {Assistantname}, the official AI assistant for MAHE Innovation Centre (MiC).

Your role is to help visitors and users with information about:
- MAHE Innovation Centre (MiC) - Manipal's Innovation Centre
- Events, workshops, and programs organized by MiC
- Resources, toolkits, guides, and mentorship programs
- Contact information and how to get involved
- Innovation, creation, and incubation programs
- MAHE SID and SCHAP e-Cell initiatives

Key guidelines:
- ONLY answer questions related to MAHE Innovation Centre and its website content
- If asked about topics unrelated to MiC, politely redirect: "I'm here to help with questions about MAHE Innovation Centre. Please ask me about our events, resources, programs, or how to get involved with MiC."
- Use information from the website database when available
- Respond only in English, even if questions are in other languages
- Keep responses DIRECT and CONCISE - avoid lengthy explanations
- Do NOT use asterisks (*) for formatting - they don't work in this context
- Maintain a warm, friendly, and professional tone
- Answer questions directly without mentioning training data or implementation notes
- Keep responses under 3-4 sentences when possible
- When asked "what is MiC" or "what exactly is MiC", provide a clear explanation

About MAHE Innovation Centre (MiC):
- MiC stands for MAHE Innovation Centre, located at Manipal Academy of Higher Education (MAHE)
- It's Manipal's premier hub for innovation, entrepreneurship, and interdisciplinary collaboration
- Provides financial aid and funding opportunities to aspiring entrepreneurs
- Offers incubation programs through MAHE SID (Society for Innovation and Development)
- Provides mentorship and guidance through SCHAP e-Cell initiatives
- Organizes events, workshops, hackathons, and provides resources for innovators
- Focuses on fostering creativity, supporting startups, and building an innovation ecosystem

IMPORTANT: You have access to the website database containing information about events, resources, and contacts. Use this data to provide accurate, up-to-date information about MiC's offerings.

LINK PROVISION: When appropriate, suggest relevant pages in a simple format:
- For events: "Check our Events page at /events"
- For resources: "Visit our Resources page at /resources"  
- For general info: "Learn more on our About page at /about"
- For contact: "Get in touch via our Contact page at /contact"
- For home: "Return to our Home page at /" """

SystemChatBot = [
    {"role": "system", "content": System}
]

def get_or_create_session():
    """Get or create a chat session"""
    try:
        session_id = request.headers.get('X-Session-ID')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session = ChatSession.query.filter_by(session_id=session_id).first()
        if not session:
            session = ChatSession(
                session_id=session_id,
                user_ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                context_data=json.dumps({
                    'current_topic': None,
                    'last_question_type': None,
                    'mentioned_events': [],
                    'mentioned_resources': [],
                    'user_interests': []
                })
            )
            db.session.add(session)
            db.session.commit()
        else:
            session.last_activity = datetime.datetime.now()
            db.session.commit()
        
        return session
    except Exception as e:
        print(f"Error managing session: {e}")
        return None

def save_message(session_id, role, content, metadata=None, context_used=None):
    """Save message with metadata and context"""
    try:
        with current_app.app_context():
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                message_metadata=json.dumps(metadata) if metadata else None,
                context_used=context_used
            )
            db.session.add(message)
            db.session.commit()
    except Exception as e:
        print(f"Error saving message: {e}")

def get_chat_history(session_id, limit=10):
    """Retrieve recent chat history for a session"""
    try:
        with current_app.app_context():
            messages = ChatMessage.query.filter_by(session_id=session_id)\
                .order_by(ChatMessage.timestamp.desc())\
                .limit(limit).all()
            
            return [{"role": msg.role, "content": msg.content} for msg in reversed(messages)]
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []

def update_session_context(session_id, context_updates):
    """Update session context with new information"""
    try:
        with current_app.app_context():
            session = ChatSession.query.filter_by(session_id=session_id).first()
            if session:
                current_context = json.loads(session.context_data or '{}')
                current_context.update(context_updates)
                session.context_data = json.dumps(current_context)
                db.session.commit()
    except Exception as e:
        print(f"Error updating session context: {e}")

def get_session_context(session_id):
    """Get current session context"""
    try:
        with current_app.app_context():
            session = ChatSession.query.filter_by(session_id=session_id).first()
            if session:
                return json.loads(session.context_data or '{}')
            return {}
    except Exception as e:
        print(f"Error getting session context: {e}")
        return {}

def analyze_query_context(query, session_context):
    """Analyze query to understand context and intent"""
    query_lower = query.lower()
    
    question_type = None
    if any(word in query_lower for word in ['what', 'tell me about', 'explain']):
        question_type = 'information'
    elif any(word in query_lower for word in ['when', 'where', 'time', 'date', 'location']):
        question_type = 'details'
    elif any(word in query_lower for word in ['how', 'how to', 'how can']):
        question_type = 'process'
    elif any(word in query_lower for word in ['who', 'contact', 'reach']):
        question_type = 'contact'
    elif any(word in query_lower for word in ['more', 'additional', 'else', 'other']):
        question_type = 'follow_up'
    
    topic = None
    if any(word in query_lower for word in ['event', 'events', 'workshop', 'program']):
        topic = 'events'
    elif any(word in query_lower for word in ['resource', 'resources', 'toolkit', 'guide']):
        topic = 'resources'
    elif any(word in query_lower for word in ['mic', 'innovation centre', 'about']):
        topic = 'about'
    elif any(word in query_lower for word in ['contact', 'reach', 'email', 'phone']):
        topic = 'contact'
    elif any(word in query_lower for word in ['incubation', 'startup', 'funding']):
        topic = 'programs'
    
    is_follow_up = any(word in query_lower for word in [
        'more', 'additional', 'else', 'other', 'also', 'and', 'what about',
        'tell me more', 'can you tell me more', 'what else'
    ])
    
    return {
        'question_type': question_type,
        'topic': topic,
        'is_follow_up': is_follow_up,
        'keywords': [word for word in query_lower.split() if len(word) > 3]
    }

def generate_context_aware_response(query, session_context, context_analysis):
    """Generate context-aware system prompt"""
    context_prompt = ""
    
    if session_context.get('current_topic'):
        context_prompt += f"\nCurrent conversation topic: {session_context['current_topic']}\n"
    
    if session_context.get('last_question_type'):
        context_prompt += f"Last question type: {session_context['last_question_type']}\n"
    
    if context_analysis['is_follow_up'] and session_context.get('mentioned_events'):
        context_prompt += f"\nPreviously mentioned events: {', '.join(session_context['mentioned_events'])}\n"
    
    if context_analysis['is_follow_up'] and session_context.get('mentioned_resources'):
        context_prompt += f"\nPreviously mentioned resources: {', '.join(session_context['mentioned_resources'])}\n"
    
    if session_context.get('user_interests'):
        context_prompt += f"\nUser interests: {', '.join(session_context['user_interests'])}\n"
    
    if context_analysis['is_follow_up']:
        context_prompt += "\nThis is a follow-up question. Reference previous conversation and provide additional relevant information.\n"
    
    if context_analysis['question_type'] == 'details':
        context_prompt += "\nUser is asking for specific details. Provide precise information with dates, times, locations, etc.\n"
    
    if context_analysis['question_type'] == 'process':
        context_prompt += "\nUser is asking about processes or procedures. Provide step-by-step guidance.\n"
    
    return context_prompt

def get_events(limit=10):
    """Retrieve events from the website database"""
    try:
        with current_app.app_context():
            events_query = Event.query.order_by(Event.date.desc()).limit(limit)
            events = []
            for event in events_query:
                events.append({
                    'title': event.title,
                    'description': event.description,
                    'date': event.date.strftime('%Y-%m-%d') if event.date else None,
                    'location': event.location,
                    'attendees': event.attendees,
                    'price': event.price,
                    'status': event.status
                })
            return events
    except Exception as e:
        print(f"Error retrieving events: {e}")
        return []

def get_resources(limit=10):
    """Retrieve resources from the website database"""
    try:
        with current_app.app_context():
            resources_query = Resource.query.order_by(Resource.created_at.desc()).limit(limit)
            resources = []
            for resource in resources_query:
                resources.append({
                    'title': resource.title,
                    'description': resource.description,
                    'category': resource.category,
                    'file_url': resource.file_url,
                    'download_count': resource.download_count,
                    'rating': resource.rating,
                    'format': resource.format,
                    'duration': resource.duration,
                    'is_featured': resource.is_featured
                })
            return resources
    except Exception as e:
        print(f"Error retrieving resources: {e}")
        return []

def get_contact_info():
    """Retrieve contact information from the website database"""
    try:
        with current_app.app_context():
            contacts_query = Contact.query.order_by(Contact.created_at.desc()).limit(5)
            contacts = []
            for contact in contacts_query:
                contacts.append({
                    'name': contact.name,
                    'email': contact.email,
                    'subject': contact.subject,
                    'message': contact.message,
                    'created_at': contact.created_at.strftime('%Y-%m-%d') if contact.created_at else None
                })
            return contacts
    except Exception as e:
        print(f"Error retrieving contact info: {e}")
        return []

def clear_chat_history():
    """Clear chat history to start fresh"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM chat_messages")
        conn.commit()
        conn.close()
        print("Chat history cleared successfully.")
    except Exception as e:
        print(f"Error clearing chat history: {e}")

def is_website_related(query):
    """Check if the query is related to MAHE Innovation Centre website"""
    query_lower = query.lower()
    
    mic_keywords = [
        'mahe', 'mic', 'innovation centre', 'innovation center', 'manipal',
        'event', 'events', 'workshop', 'workshops', 'program', 'programs',
        'resource', 'resources', 'toolkit', 'toolkits', 'guide', 'guides',
        'mentorship', 'incubation', 'incubator', 'entrepreneur', 'entrepreneurship',
        'sid', 'schap', 'e-cell', 'ecell', 'contact', 'about', 'team',
        'funding', 'financial aid', 'startup', 'startups', 'collaboration',
        'what is', 'what exactly is', 'what does', 'explain', 'tell me about'
    ]
    
    return any(keyword in query_lower for keyword in mic_keywords)

def get_website_urls():
    """Get the base URLs for different website sections"""
    return {
        'home': '/',
        'about': '/about',
        'events': '/events', 
        'resources': '/resources',
        'contact': '/contact'
    }

def generate_relevant_links(query):
    """Generate relevant links based on the query content"""
    query_lower = query.lower()
    urls = get_website_urls()
    relevant_links = []
    
    if any(word in query_lower for word in ['event', 'events', 'workshop', 'program', 'schedule', 'calendar']):
        relevant_links.append(f"Check our Events page at {urls['events']}")
    
    if any(word in query_lower for word in ['resource', 'resources', 'toolkit', 'guide', 'download', 'material']):
        relevant_links.append(f"Visit our Resources page at {urls['resources']}")
    
    if any(word in query_lower for word in ['about', 'team', 'mission', 'vision', 'who we are']):
        relevant_links.append(f"Learn more on our About page at {urls['about']}")
    
    if any(word in query_lower for word in ['contact', 'reach', 'get in touch', 'email', 'phone', 'address']):
        relevant_links.append(f"Get in touch via our Contact page at {urls['contact']}")
    
    if any(word in query_lower for word in ['home', 'main', 'start', 'overview']):
        relevant_links.append(f"Return to our Home page at {urls['home']}")
    
    return relevant_links

def format_website_context(events, resources, contacts):
    """Format website data into context for the AI"""
    context = "MAHE Innovation Centre Website Information:\n\n"
    
    if events:
        context += "Recent Events:\n"
        for event in events[:3]:  
            context += f"- {event['title']} ({event['date']}) at {event['location']}\n"
            context += f"  {event['description'][:150]}...\n"
            context += f"  Attendees: {event['attendees']}, Price: {event['price']}, Status: {event['status']}\n\n"
    
    if resources:
        context += "Available Resources:\n"
        for resource in resources[:3]: 
            context += f"- {resource['title']} ({resource['category']})\n"
            context += f"  {resource['description'][:150]}...\n"
            context += f"  Format: {resource['format']}, Duration: {resource['duration']}, Rating: {resource['rating']}/5\n\n"
    
    if contacts:
        context += "Recent Contact Inquiries:\n"
        for contact in contacts[:2]: 
            context += f"- {contact['subject']} from {contact['name']} ({contact['email']})\n"
            context += f"  {contact['message'][:100]}...\n\n"
    
    return context

def get_realtime_information():
    """Get current date and time information"""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    
    return f"""Current real-time information:
Day: {day}
Date: {date} {month} {year}
Time: {hour}:{minute}"""

def clean_response(response):
    """Remove repetitive sentences or phrases"""
    if not response:
        return response
        
    sentences = response.split('. ')
    unique_sentences = []
    seen = set()
    
    for sentence in sentences:
        normalized = sentence.lower().strip()
        if normalized not in seen and len(normalized.split()) > 3:
            unique_sentences.append(sentence)
            seen.add(normalized)
    
    cleaned = '. '.join(unique_sentences)
    return cleaned if cleaned else response

def format_answer(answer):
    """Format answer with proper structure and convert links to buttons"""
    if not answer:
        return "I didn't generate a proper response. Please try rephrasing your question."
    
    answer = answer.replace("</s>", "").replace("</s", "").strip()
    
    answer = answer.replace("**", "").replace("*", "")
    
    answer = clean_response(answer)
    
    answer = convert_links_to_buttons(answer)
    
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    return '\n'.join(non_empty_lines)

def convert_links_to_buttons(text):
    """Convert text links to button format for frontend rendering"""
    import re
    
    if '[BUTTON:' in text:
        return text 
    
    link_patterns = [
        (r'Check our Events page[:\s]+at\s+(/events)', r' [BUTTON:Events Page|/events]'),
        (r'Check our Events page[:\s]+(/events)', r' [BUTTON:Events Page|/events]'),
        (r'Visit our Events page[:\s]+at\s+(/events)', r' [BUTTON:Events Page|/events]'),
        (r'Visit our Events page[:\s]+(/events)', r' [BUTTON:Events Page|/events]'),
        (r'Events page[:\s]+at\s+(/events)', r' [BUTTON:Events Page|/events]'),
        (r'Events page[:\s]+(/events)', r' [BUTTON:Events Page|/events]'),
        (r'(?<!\[BUTTON:)[^[]/events(?!\])', r' [BUTTON:Events Page|/events]'),
        
        (r'Visit our Resources page[:\s]+at\s+(/resources)', r' [BUTTON:Resources Page|/resources]'),
        (r'Visit our Resources page[:\s]+(/resources)', r' [BUTTON:Resources Page|/resources]'),
        (r'Check our Resources page[:\s]+at\s+(/resources)', r' [BUTTON:Resources Page|/resources]'),
        (r'Check our Resources page[:\s]+(/resources)', r' [BUTTON:Resources Page|/resources]'),
        (r'Resources page[:\s]+at\s+(/resources)', r' [BUTTON:Resources Page|/resources]'),
        (r'Resources page[:\s]+(/resources)', r' [BUTTON:Resources Page|/resources]'),
        (r'(?<!\[BUTTON:)[^[]/resources(?!\])', r' [BUTTON:Resources Page|/resources]'),
        
        (r'Learn more on our About page[:\s]+at\s+(/about)', r' [BUTTON:About Page|/about]'),
        (r'Learn more on our About page[:\s]+(/about)', r' [BUTTON:About Page|/about]'),
        (r'Visit our About page[:\s]+at\s+(/about)', r' [BUTTON:About Page|/about]'),
        (r'Visit our About page[:\s]+(/about)', r' [BUTTON:About Page|/about]'),
        (r'About page[:\s]+at\s+(/about)', r' [BUTTON:About Page|/about]'),
        (r'About page[:\s]+(/about)', r' [BUTTON:About Page|/about]'),
        (r'(?<!\[BUTTON:)[^[]/about(?!\])', r' [BUTTON:About Page|/about]'),
        
        (r'Get in touch via our Contact page[:\s]+at\s+(/contact)', r' [BUTTON:Contact Page|/contact]'),
        (r'Get in touch via our Contact page[:\s]+(/contact)', r' [BUTTON:Contact Page|/contact]'),
        (r'Visit our Contact page[:\s]+at\s+(/contact)', r' [BUTTON:Contact Page|/contact]'),
        (r'Visit our Contact page[:\s]+(/contact)', r' [BUTTON:Contact Page|/contact]'),
        (r'Contact page[:\s]+at\s+(/contact)', r' [BUTTON:Contact Page|/contact]'),
        (r'Contact page[:\s]+(/contact)', r' [BUTTON:Contact Page|/contact]'),
        (r'(?<!\[BUTTON:)[^[]/contact(?!\])', r' [BUTTON:Contact Page|/contact]'),
        
        (r'Return to our Home page[:\s]+at\s+(/)', r' [BUTTON:Home Page|/]'),
        (r'Return to our Home page[:\s]+(/)', r' [BUTTON:Home Page|/]'),
        (r'Visit our Home page[:\s]+at\s+(/)', r' [BUTTON:Home Page|/]'),
        (r'Visit our Home page[:\s]+(/)', r' [BUTTON:Home Page|/]'),
        (r'Home page[:\s]+at\s+(/)', r' [BUTTON:Home Page|/]'),
        (r'Home page[:\s]+(/)', r' [BUTTON:Home Page|/]'),
    ]
    
    for pattern, replacement in link_patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def is_asking_about_events(query):
    """Check if the user is asking about events"""
    query_lower = query.lower()
    event_keywords = [
        "event", "events", "workshop", "workshops", "program", "programs",
        "upcoming", "schedule", "calendar", "when", "where", "date", "time"
    ]
    return any(keyword in query_lower for keyword in event_keywords)

def is_asking_about_resources(query):
    """Check if the user is asking about resources"""
    query_lower = query.lower()
    resource_keywords = [
        "resource", "resources", "toolkit", "toolkits", "guide", "guides",
        "download", "material", "materials", "document", "documents"
    ]
    return any(keyword in query_lower for keyword in resource_keywords)
def get_fallback_response(query):
    """Provide fallback responses when API is not available"""
    query_lower = query.lower()
    
    if any(phrase in query_lower for phrase in ['what is mic', 'what exactly is mic', 'what does mic stand for', 'what is mahe innovation centre']):
        return "MiC stands for MAHE Innovation Centre, Manipal's premier hub for innovation and entrepreneurship. We provide funding, incubation programs, and mentorship to aspiring entrepreneurs. Learn more on our About page at /about."
    
    elif any(word in query_lower for word in ['event', 'events', 'workshop', 'program']):
        try:
            events = get_events(limit=3)
            if events:
                response = "We have several exciting events coming up:\n"
                for event in events:
                    response += f"• {event['title']} on {event['date']} at {event['location']} ({event['price']})\n"
                response += "Check our Events page at /events for more details."
                return response
        except Exception as e:
            print(f"Error getting events: {e}")
        
        return "We host various events including workshops, hackathons, and innovation showcases. Check our Events page at /events for upcoming events."
    
    elif any(word in query_lower for word in ['resource', 'resources', 'toolkit', 'guide']):
        try:
            resources = get_resources(limit=3)
            if resources:
                response = "We offer these valuable resources:\n"
                for resource in resources:
                    response += f"• {resource['title']} ({resource['category']}) - Rating: {resource['rating']}/5\n"
                response += "Visit our Resources page at /resources for detailed information."
                return response
        except Exception as e:
            print(f"Error getting resources: {e}")
        
        return "We provide numerous resources for innovators and entrepreneurs. Visit our Resources page at /resources for tools and materials."
    
    elif any(word in query_lower for word in ['contact', 'reach', 'get in touch']):
        return "You can contact us through our Contact page at /contact or reach out via email. We're here to help!"
    
    elif any(word in query_lower for word in ['about', 'who we are']):
        return "MAHE Innovation Centre is Manipal's hub for innovation and entrepreneurship. Learn more on our About page at /about."
    
    elif any(word in query_lower for word in ['incubation', 'startup', 'funding']):
        return "We offer incubation support through MAHE SID and provide financial aid to entrepreneurs. Check our Resources page at /resources for details."
    
    else:
        return "I'm here to help with questions about MAHE Innovation Centre. Please ask me about our events, resources, programs, or how to get involved with MiC."

def ChatBot(query, session_id=None):
    """Main chatbot function with enhanced logging and context awareness"""
    try:
        if not query or not query.strip():
            return "Please provide a valid question or message."
        
        session = get_or_create_session()
        if not session:
            session_id = str(uuid.uuid4())
        else:
            session_id = session.session_id
        
        session_context = get_session_context(session_id)
        
        context_analysis = analyze_query_context(query, session_context)
        
        if not is_website_related(query):
            save_message(session_id, "user", query, {"context_analysis": context_analysis})
            save_message(session_id, "assistant", "I'm here to help with questions about MAHE Innovation Centre. Please ask me about our events, resources, programs, or how to get involved with MiC.")
            return "I'm here to help with questions about MAHE Innovation Centre. Please ask me about our events, resources, programs, or how to get involved with MiC."
        
        if not client:
            response = get_fallback_response(query)
            formatted_response = format_answer(response)
            save_message(session_id, "user", query, {"context_analysis": context_analysis})
            save_message(session_id, "assistant", formatted_response, {"fallback": True})
            return formatted_response
        
        context_messages = get_chat_history(session_id, limit=10)
        
        messages_for_api = SystemChatBot.copy()
        
        messages_for_api.append({
            "role": "system", 
            "content": get_realtime_information()
        })
        
        context_prompt = generate_context_aware_response(query, session_context, context_analysis)
        if context_prompt:
            messages_for_api.append({
                "role": "system",
                "content": context_prompt
            })
        
        events = []
        resources = []
        contacts = []
        context_used = []
        
        if is_asking_about_events(query) or context_analysis['topic'] == 'events':
            events = get_events(limit=5)
            context_used.append('events')
        elif is_asking_about_resources(query) or context_analysis['topic'] == 'resources':
            resources = get_resources(limit=5)
            context_used.append('resources')
        else:
            events = get_events(limit=3)
            resources = get_resources(limit=3)
            contacts = get_contact_info()
            context_used.extend(['events', 'resources', 'contacts'])
        
        if events or resources or contacts:
            website_context = format_website_context(events, resources, contacts)
            messages_for_api.append({
                "role": "system",
                "content": website_context
            })
        
        relevant_links = generate_relevant_links(query)
        if relevant_links:
            links_context = "Relevant website pages for this query:\n" + "\n".join(relevant_links)
            messages_for_api.append({
                "role": "system",
                "content": links_context
            })
        
        messages_for_api.extend(context_messages)
        messages_for_api.append({"role": "user", "content": query})
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=messages_for_api,
                max_tokens=512,
                temperature=0.3,  
                top_p=0.8,        
                stream=True,
                stop=None
            )

            answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    answer += chunk.choices[0].delta.content
            
            formatted_answer = format_answer(answer)
            
            if formatted_answer and formatted_answer != query and not formatted_answer.startswith("I didn't generate"):
                save_message(session_id, "user", query, {
                    "context_analysis": context_analysis,
                    "session_context": session_context
                })
                save_message(session_id, "assistant", formatted_answer, {
                    "context_used": context_used,
                    "events_count": len(events),
                    "resources_count": len(resources)
                }, context_used)
                
                context_updates = {
                    'current_topic': context_analysis['topic'],
                    'last_question_type': context_analysis['question_type']
                }
                
                if events:
                    mentioned_events = session_context.get('mentioned_events', [])
                    for event in events[:3]: 
                        if event['title'] not in mentioned_events:
                            mentioned_events.append(event['title'])
                    context_updates['mentioned_events'] = mentioned_events[-5:]  
                
                if resources:
                    mentioned_resources = session_context.get('mentioned_resources', [])
                    for resource in resources[:3]:  
                        if resource['title'] not in mentioned_resources:
                            mentioned_resources.append(resource['title'])
                    context_updates['mentioned_resources'] = mentioned_resources[-5:]  
                
                if context_analysis['keywords']:
                    user_interests = session_context.get('user_interests', [])
                    for keyword in context_analysis['keywords']:
                        if keyword not in user_interests and len(keyword) > 3:
                            user_interests.append(keyword)
                    context_updates['user_interests'] = user_interests[-10:] 
                
                update_session_context(session_id, context_updates)
                
                return formatted_answer
            else:
                error_msg = "I didn't generate a proper response. Please try rephrasing your question."
                save_message(session_id, "user", query, {"context_analysis": context_analysis})
                save_message(session_id, "assistant", error_msg, {"error": "no_response"})
                return error_msg

        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                print("Rate limit hit, waiting 30 seconds...")
                time.sleep(30)
                return ChatBot(query, session_id)
            elif "context length" in str(e).lower():
                print("Context too long, clearing some history...")
                with current_app.app_context():
                    ChatMessage.query.filter_by(session_id=session_id)\
                        .order_by(ChatMessage.timestamp.desc())\
                        .limit(5).delete()
                    db.session.commit()
                return ChatBot(query, session_id)
            else:
                raise e

    except Exception as e:
        print(f"ChatBot Error: {e}")
        error_msg = f"I encountered an error: {str(e)}. Please try again."
        if session_id:
            save_message(session_id, "user", query, {"error": str(e)})
            save_message(session_id, "assistant", error_msg, {"error": "system_error"})
        return error_msg

def show_commands():
    """Display available commands"""
    commands = """
Available commands:
- 'clear' or 'reset' - Clear chat history
- 'exit' or 'quit' - Exit the program
- Any other input will be treated as a question/message
    """
    print(commands)

def main():
    """Main program loop"""
    print("=" * 60)
    print(f"MAHE Innovation Centre Assistant Active")
    
    print("Type 'help' for commands or start chatting!")
    print("-" * 60)
    
    while True:
        try:
            user_input = input(f"\n{Username}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print(f"\nGoodbye! Thanks for chatting with {Assistantname}!")
                break
            elif user_input.lower() in ['clear', 'reset']:
                clear_chat_history()
                continue
            elif user_input.lower() in ['help', 'commands']:
                show_commands()
                continue
            
            print(f"\n{Assistantname}: ", end="", flush=True)
            response = ChatBot(user_input)
            print(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            continue

if __name__ == "__main__":
    main()