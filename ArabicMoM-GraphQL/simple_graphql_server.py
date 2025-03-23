#!/usr/bin/env python
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv
import graphene
from graphene import ObjectType, String, Schema, Field, List, ID, Int

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data for demonstration
sample_meetings = [
    {
        "id": "m1",
        "meeting_number": "BOD-2023-01",
        "meeting_title": "مجلس الإدارة الاجتماع الأول",
        "meeting_date": "2023-01-15",
        "meeting_time": "10:00",
        "meeting_location": "قاعة الاجتماعات الرئيسية",
        "meeting_chairman": "أحمد محمد",
        "created_at": "2023-01-10",
        "pdf_source": "meeting_m1.pdf",
        "language": "ar"
    },
    {
        "id": "m2",
        "meeting_number": "BOD-2023-02",
        "meeting_title": "مجلس الإدارة الاجتماع الثاني",
        "meeting_date": "2023-02-20",
        "meeting_time": "14:30",
        "meeting_location": "قاعة المؤتمرات",
        "meeting_chairman": "أحمد محمد",
        "created_at": "2023-02-15",
        "pdf_source": "meeting_m2.pdf",
        "language": "ar"
    }
]

sample_attendees = [
    {
        "id": "a1",
        "name": "أحمد محمد",
        "title": "رئيس مجلس الإدارة",
        "role": "رئيس",
        "email": "ahmed@example.com"
    },
    {
        "id": "a2",
        "name": "محمد علي",
        "title": "نائب رئيس مجلس الإدارة",
        "role": "عضو",
        "email": "mohammed@example.com"
    },
    {
        "id": "a3",
        "name": "فاطمة أحمد",
        "title": "المدير المالي",
        "role": "عضو",
        "email": "fatima@example.com"
    }
]

sample_partial_attendees = [
    {
        "id": "pa1",
        "name": "خالد عبدالله",
        "title": "مستشار قانوني",
        "role": "مستشار",
        "notes": "حضر جزء من الاجتماع",
        "email": "khaled@example.com"
    },
    {
        "id": "pa2",
        "name": "سارة يوسف",
        "title": "مديرة الموارد البشرية",
        "role": "مدعوة",
        "notes": "حضرت لعرض تقرير الموارد البشرية",
        "email": "sarah@example.com"
    }
]

sample_sections = [
    {
        "id": "s1",
        "title": "مراجعة القرارات السابقة",
        "order": 1,
        "meeting_id": "m1",
        "content": "تمت مراجعة القرارات السابقة ومتابعة تنفيذها."
    },
    {
        "id": "s2",
        "title": "التقرير المالي",
        "order": 2,
        "meeting_id": "m1",
        "content": "تم عرض التقرير المالي للربع الأول من العام."
    },
    {
        "id": "s3",
        "title": "الخطة الاستراتيجية",
        "order": 1,
        "meeting_id": "m2",
        "content": "تمت مناقشة الخطة الاستراتيجية للعام القادم."
    }
]

sample_decisions = [
    {
        "id": "d1",
        "decision_id": "DEC-2023-01-01",
        "date": "2023-01-15",
        "content": "الموافقة على التقرير المالي للربع الأول",
        "subsection_id": "s2"
    },
    {
        "id": "d2",
        "decision_id": "DEC-2023-02-01",
        "date": "2023-02-20",
        "content": "الموافقة على الخطة الاستراتيجية للعام القادم",
        "subsection_id": "s3"
    }
]

sample_action_items = [
    {
        "id": "ai1",
        "description": "إعداد تقرير مفصل عن الميزانية",
        "assignee": "فاطمة أحمد",
        "due_date": "2023-02-15",
        "status": "COMPLETED",
        "decision_id": "d1"
    },
    {
        "id": "ai2",
        "description": "تطوير خطة تنفيذية للاستراتيجية",
        "assignee": "محمد علي",
        "due_date": "2023-03-30",
        "status": "IN_PROGRESS",
        "decision_id": "d2"
    }
]

# Define GraphQL schema
class Attendee(ObjectType):
    id = ID()
    name = String()
    title = String()
    role = String()
    email = String()

class PartialAttendee(ObjectType):
    id = ID()
    name = String()
    title = String()
    role = String()
    notes = String()
    email = String()

class Section(ObjectType):
    id = ID()
    title = String()
    order = Int()
    meeting_id = ID(name='meetingId')
    content = String()

class Decision(ObjectType):
    id = ID()
    decision_id = String(name='decisionId')
    date = String()
    content = String()
    subsection_id = ID(name='subsectionId')

class ActionItem(ObjectType):
    id = ID()
    description = String()
    assignee = String()
    due_date = String(name='dueDate')
    status = String()
    decision_id = ID(name='decisionId')

class Meeting(ObjectType):
    id = ID()
    meeting_number = String(name='meetingNumber')
    meeting_title = String(name='meetingTitle')
    meeting_date = String(name='meetingDate')
    meeting_time = String(name='meetingTime')
    meeting_location = String(name='meetingLocation')
    meeting_chairman = String(name='meetingChairman')
    created_at = String(name='createdAt')
    pdf_source = String(name='pdfSource')
    language = String()
    attendees = List(Attendee)
    partial_attendees = List(PartialAttendee, name='partialAttendees')
    sections = List(Section)
    
    def resolve_attendees(self, info):
        return sample_attendees
    
    def resolve_partial_attendees(self, info):
        return sample_partial_attendees
    
    def resolve_sections(self, info):
        return [section for section in sample_sections if section['meeting_id'] == self['id']]

class Query(ObjectType):
    meetings = List(Meeting)
    meeting = Field(Meeting, id=ID(required=True))
    attendees = List(Attendee)
    attendee = Field(Attendee, id=ID(required=True))
    partial_attendees = List(PartialAttendee, name='partialAttendees')
    partial_attendee = Field(PartialAttendee, id=ID(required=True), name='partialAttendee')
    sections = List(Section)
    section = Field(Section, id=ID(required=True))
    sections_by_meeting = List(Section, meeting_id=ID(required=True, name='meetingId'))
    decisions = List(Decision)
    decision = Field(Decision, id=ID(required=True))
    action_items = List(ActionItem)
    action_item = Field(ActionItem, id=ID(required=True))
    action_items_by_status = List(ActionItem, status=String(required=True))
    
    def resolve_meetings(self, info):
        return sample_meetings
    
    def resolve_meeting(self, info, id):
        for meeting in sample_meetings:
            if meeting["id"] == id:
                return meeting
        return None
    
    def resolve_attendees(self, info):
        return sample_attendees
    
    def resolve_attendee(self, info, id):
        for attendee in sample_attendees:
            if attendee["id"] == id:
                return attendee
        return None
    
    def resolve_partial_attendees(self, info):
        return sample_partial_attendees
    
    def resolve_partial_attendee(self, info, id):
        for attendee in sample_partial_attendees:
            if attendee["id"] == id:
                return attendee
        return None
    
    def resolve_sections(self, info):
        return sample_sections
    
    def resolve_section(self, info, id):
        for section in sample_sections:
            if section["id"] == id:
                return section
        return None
    
    def resolve_sections_by_meeting(self, info, meeting_id):
        return [section for section in sample_sections if section["meeting_id"] == meeting_id]
    
    def resolve_decisions(self, info):
        return sample_decisions
    
    def resolve_decision(self, info, id):
        for decision in sample_decisions:
            if decision["id"] == id:
                return decision
        return None
    
    def resolve_action_items(self, info):
        return sample_action_items
    
    def resolve_action_item(self, info, id):
        for action_item in sample_action_items:
            if action_item["id"] == id:
                return action_item
        return None
    
    def resolve_action_items_by_status(self, info, status):
        return [action_item for action_item in sample_action_items if action_item["status"] == status]

schema = Schema(query=Query)

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Arabic MoM GraphQL API",
        "endpoints": {
            "graphql": "/graphql",
            "graphiql": "/graphql"
        }
    })

# GraphQL endpoint
@app.route('/graphql', methods=['GET', 'POST'])
def graphql_server():
    # Handle GET request (for GraphiQL interface)
    if request.method == 'GET':
        return "<html><body><h1>GraphQL API</h1><p>This is a GraphQL API endpoint. Please use POST requests to query the API.</p></body></html>"
    
    # Handle POST request (for GraphQL queries)
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"errors": [{"message": "No GraphQL query found in the request"}]}), 400
    
    query = data.get('query')
    variables = data.get('variables')
    
    # Log the incoming query for debugging
    logging.info(f"Received GraphQL Query: {query}")
    logging.info(f"Variables: {variables}")
    
    # Execute the query
    result = schema.execute(query, variable_values=variables)
    
    # Handle errors
    if result.errors:
        logging.error(f"GraphQL Error: {result.errors}")
        return jsonify({"errors": [{"message": str(error)} for error in result.errors]}), 400
    
    # Return the result
    return jsonify({"data": result.data})

# Health check
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('GRAPHQL_SERVER_PORT', 5001))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
