import graphene
from datetime import datetime
import uuid
from graphene.types.enum import Enum

# Define enums
class ActionStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# GraphQL Types
class Attendee(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    title = graphene.String()
    role = graphene.String()
    email = graphene.String()
    meetings = graphene.List(lambda: Meeting)

    def resolve_meetings(self, info):
        return [Meeting(**meeting) for meeting in get_meetings_by_attendee(self.id)]

class PartialAttendee(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    title = graphene.String()
    role = graphene.String()
    notes = graphene.String()

class Section(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    order = graphene.Int()
    meeting_id = graphene.ID()
    meeting = graphene.Field(lambda: Meeting)
    content = graphene.String()
    sub_sections = graphene.List(lambda: SubSection)

    def resolve_meeting(self, info):
        meeting = get_meeting(self.meeting_id)
        if meeting:
            return Meeting(**meeting)
        return None

    def resolve_sub_sections(self, info):
        return [SubSection(**subsection) for subsection in get_section_subsections(self.id)]

class SubSection(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    order = graphene.Int()
    section_id = graphene.ID()
    section = graphene.Field(Section)
    content = graphene.String()
    recommendations = graphene.List(lambda: Recommendation)
    decisions = graphene.List(lambda: Decision)

    def resolve_section(self, info):
        section = get_section(self.section_id)
        if section:
            return Section(**section)
        return None

    def resolve_recommendations(self, info):
        return [Recommendation(**recommendation) for recommendation in get_subsection_recommendations(self.id)]

    def resolve_decisions(self, info):
        return [Decision(**decision) for decision in get_subsection_decisions(self.id)]

class Recommendation(graphene.ObjectType):
    id = graphene.ID()
    recommendation_id = graphene.String()
    source = graphene.String()
    date = graphene.String()
    content = graphene.String()
    subsection_id = graphene.ID()
    subsection = graphene.Field(SubSection)
    related_recommendations = graphene.List(lambda: Recommendation)

    def resolve_subsection(self, info):
        subsection = get_subsection(self.subsection_id)
        if subsection:
            return SubSection(**subsection)
        return None

    def resolve_related_recommendations(self, info):
        # This would be implemented to fetch related recommendations
        return []

class Decision(graphene.ObjectType):
    id = graphene.ID()
    decision_id = graphene.String()
    date = graphene.String()
    content = graphene.String()
    subsection_id = graphene.ID()
    subsection = graphene.Field(SubSection)
    based_on_recommendations = graphene.List(Recommendation)
    financial_impact = graphene.Field(lambda: FinancialImpact)
    action_items = graphene.List(lambda: ActionItem)

    def resolve_subsection(self, info):
        subsection = get_subsection(self.subsection_id)
        if subsection:
            return SubSection(**subsection)
        return None

    def resolve_based_on_recommendations(self, info):
        # This would be implemented to fetch recommendations this decision is based on
        return []

    def resolve_financial_impact(self, info):
        financial_impacts = get_decision_financial_impacts(self.id)
        if financial_impacts:
            return FinancialImpact(**financial_impacts[0])
        return None

    def resolve_action_items(self, info):
        return [ActionItem(**action_item) for action_item in get_decision_action_items(self.id)]

class FinancialImpact(graphene.ObjectType):
    id = graphene.ID()
    amount = graphene.Float()
    currency = graphene.String()
    description = graphene.String()
    budget_source = graphene.String()
    decision_id = graphene.ID()
    decision = graphene.Field(Decision)

    def resolve_decision(self, info):
        decision = get_decision(self.decision_id)
        if decision:
            return Decision(**decision)
        return None

class ActionItem(graphene.ObjectType):
    id = graphene.ID()
    description = graphene.String()
    assignee = graphene.String()
    due_date = graphene.String()
    status = graphene.String()
    decision_id = graphene.ID()
    decision = graphene.Field(Decision)

    def resolve_decision(self, info):
        decision = get_decision(self.decision_id)
        if decision:
            return Decision(**decision)
        return None

class Meeting(graphene.ObjectType):
    id = graphene.ID()
    meeting_number = graphene.String()
    meeting_title = graphene.String()
    meeting_date = graphene.String()
    meeting_time = graphene.String()
    meeting_location = graphene.String()
    meeting_chairman = graphene.String()
    created_at = graphene.String()
    pdf_source = graphene.String()
    language = graphene.String()
    attendees = graphene.List(Attendee)
    partial_attendees = graphene.List(PartialAttendee)
    sections = graphene.List(Section)

    def resolve_attendees(self, info):
        return [Attendee(**attendee) for attendee in get_attendee_by_meeting(self.id)]

    def resolve_partial_attendees(self, info):
        return [PartialAttendee(**partial_attendee) for partial_attendee in get_partial_attendees_by_meeting(self.id)]

    def resolve_sections(self, info):
        return [Section(**section) for section in get_meeting_sections(self.id)]

# Input Types
class AttendeeInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    title = graphene.String()
    role = graphene.String(required=True)
    email = graphene.String()

class PartialAttendeeInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    title = graphene.String()
    role = graphene.String(required=True)
    notes = graphene.String()

class MeetingInput(graphene.InputObjectType):
    meeting_number = graphene.String(required=True)
    meeting_title = graphene.String(required=True)
    meeting_date = graphene.String(required=True)
    meeting_time = graphene.String(required=True)
    meeting_location = graphene.String(required=True)
    meeting_chairman = graphene.String(required=True)
    pdf_source = graphene.String()
    language = graphene.String(required=True)

class SectionInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    order = graphene.Int(required=True)
    meeting_id = graphene.ID(required=True)
    content = graphene.String()

class SubSectionInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    order = graphene.Int(required=True)
    section_id = graphene.ID(required=True)
    content = graphene.String()

class RecommendationInput(graphene.InputObjectType):
    recommendation_id = graphene.String(required=True)
    source = graphene.String(required=True)
    date = graphene.String()
    content = graphene.String(required=True)
    subsection_id = graphene.ID(required=True)
    related_recommendation_ids = graphene.List(graphene.ID)

class DecisionInput(graphene.InputObjectType):
    decision_id = graphene.String(required=True)
    date = graphene.String(required=True)
    content = graphene.String(required=True)
    subsection_id = graphene.ID(required=True)
    based_on_recommendation_ids = graphene.List(graphene.ID)

class FinancialImpactInput(graphene.InputObjectType):
    amount = graphene.Float()
    currency = graphene.String()
    description = graphene.String(required=True)
    budget_source = graphene.String()
    decision_id = graphene.ID(required=True)

class ActionItemInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    assignee = graphene.String()
    due_date = graphene.String()
    status = graphene.String(required=True)
    decision_id = graphene.ID(required=True)

# Sample data for demonstration
sample_meetings = [
    {
        "id": "m1",
        "meeting_number": "8",
        "meeting_title": "مجلس الإدارة - الجلسة الثامنة من الدورة السادسة",
        "meeting_date": "2024-05-05",
        "meeting_time": "12:30",
        "meeting_location": "قاعة الاجتماعات الرئيسية",
        "meeting_chairman": "د. عبدالله المهندس",
        "created_at": "2024-05-06T10:00:00",
        "pdf_source": "meeting_8_minutes.pdf",
        "language": "ar"
    }
]

sample_attendees = [
    {
        "id": "a1",
        "name": "د. عبدالله المهندس",
        "title": "رئيس مجلس الإدارة",
        "role": "رئيس الجلسة",
        "email": "abdullah@example.com"
    },
    {
        "id": "a2",
        "name": "م. سارة الأحمد",
        "title": "نائب رئيس مجلس الإدارة",
        "role": "عضو",
        "email": "sara@example.com"
    }
]

sample_partial_attendees = [
    {
        "id": "pa1",
        "name": "د. محمد الخبير",
        "title": "مستشار قانوني",
        "role": "مستشار",
        "notes": "حضر لمناقشة البند الثالث فقط"
    }
]

sample_sections = [
    {
        "id": "s1",
        "title": "افتتاح الاجتماع",
        "order": 1,
        "meeting_id": "m1",
        "content": "افتتح رئيس مجلس الإدارة الاجتماع بالترحيب بالحضور"
    },
    {
        "id": "s2",
        "title": "مراجعة قرارات الاجتماع السابق",
        "order": 2,
        "meeting_id": "m1",
        "content": "تمت مراجعة القرارات السابقة والتأكد من تنفيذها"
    }
]

sample_subsections = [
    {
        "id": "ss1",
        "title": "كلمة الرئيس الافتتاحية",
        "order": 1,
        "section_id": "s1",
        "content": "رحب الرئيس بالحضور وشكرهم على الانضمام للاجتماع"
    },
    {
        "id": "ss2",
        "title": "متابعة تنفيذ القرار رقم 45",
        "order": 1,
        "section_id": "s2",
        "content": "تم استعراض حالة تنفيذ القرار رقم 45 المتعلق بتطوير النظام الإلكتروني"
    }
]

sample_recommendations = [
    {
        "id": "r1",
        "recommendation_id": "22",
        "source": "لجنة إدارة المخاطر",
        "date": "2024-04-20",
        "content": "توصي اللجنة بتحديث سياسة إدارة المخاطر لتشمل المخاطر السيبرانية",
        "subsection_id": "ss2"
    }
]

sample_decisions = [
    {
        "id": "d1",
        "decision_id": "D-45",
        "date": "2024-05-05",
        "content": "الموافقة على تحديث سياسة إدارة المخاطر وفقاً لتوصية اللجنة",
        "subsection_id": "ss2"
    }
]

sample_financial_impacts = [
    {
        "id": "fi1",
        "amount": 250000.00,
        "currency": "SAR",
        "description": "تكلفة تطوير وتنفيذ السياسة الجديدة",
        "budget_source": "ميزانية تكنولوجيا المعلومات",
        "decision_id": "d1"
    }
]

sample_action_items = [
    {
        "id": "ai1",
        "description": "إعداد مسودة السياسة الجديدة",
        "assignee": "م. سارة الأحمد",
        "due_date": "2024-06-15",
        "status": "PENDING",
        "decision_id": "d1"
    }
]

# Helper functions for data access
def get_meeting(meeting_id):
    for meeting in sample_meetings:
        if meeting["id"] == meeting_id:
            return meeting
    return None

def get_attendee(attendee_id):
    for attendee in sample_attendees:
        if attendee["id"] == attendee_id:
            return attendee
    return None

def get_partial_attendee(partial_attendee_id):
    for partial_attendee in sample_partial_attendees:
        if partial_attendee["id"] == partial_attendee_id:
            return partial_attendee
    return None

def get_section(section_id):
    for section in sample_sections:
        if section["id"] == section_id:
            return section
    return None

def get_subsection(subsection_id):
    for subsection in sample_subsections:
        if subsection["id"] == subsection_id:
            return subsection
    return None

def get_recommendation(recommendation_id):
    for recommendation in sample_recommendations:
        if recommendation["id"] == recommendation_id:
            return recommendation
    return None

def get_decision(decision_id):
    for decision in sample_decisions:
        if decision["id"] == decision_id:
            return decision
    return None

def get_financial_impact(financial_impact_id):
    for financial_impact in sample_financial_impacts:
        if financial_impact["id"] == financial_impact_id:
            return financial_impact
    return None

def get_action_item(action_item_id):
    for action_item in sample_action_items:
        if action_item["id"] == action_item_id:
            return action_item
    return None

def get_meeting_sections(meeting_id):
    return [section for section in sample_sections if section["meeting_id"] == meeting_id]

def get_section_subsections(section_id):
    return [subsection for subsection in sample_subsections if subsection["section_id"] == section_id]

def get_subsection_recommendations(subsection_id):
    return [recommendation for recommendation in sample_recommendations if recommendation["subsection_id"] == subsection_id]

def get_subsection_decisions(subsection_id):
    return [decision for decision in sample_decisions if decision["subsection_id"] == subsection_id]

def get_decision_financial_impacts(decision_id):
    return [financial_impact for financial_impact in sample_financial_impacts if financial_impact["decision_id"] == decision_id]

def get_decision_action_items(decision_id):
    return [action_item for action_item in sample_action_items if action_item["decision_id"] == decision_id]

def get_attendee_by_meeting(meeting_id):
    # In a real implementation, this would query a database
    return sample_attendees

def get_partial_attendees_by_meeting(meeting_id):
    # In a real implementation, this would query a database
    return sample_partial_attendees

def get_meetings_by_attendee(attendee_id):
    # In a real implementation, this would query a database
    return sample_meetings

# Query class for GraphQL schema
class Query(graphene.ObjectType):
    meeting = graphene.Field(Meeting, id=graphene.ID(required=True))
    meetings = graphene.List(Meeting, limit=graphene.Int(), offset=graphene.Int())
    meetings_by_date = graphene.List(Meeting, start_date=graphene.String(required=True), end_date=graphene.String())
    
    attendee = graphene.Field(Attendee, id=graphene.ID(required=True))
    attendees = graphene.List(Attendee, limit=graphene.Int(), offset=graphene.Int())
    
    section = graphene.Field(Section, id=graphene.ID(required=True))
    sections_by_meeting = graphene.List(Section, meeting_id=graphene.ID(required=True))
    
    subsection = graphene.Field(SubSection, id=graphene.ID(required=True))
    subsections_by_section = graphene.List(SubSection, section_id=graphene.ID(required=True))
    
    recommendation = graphene.Field(Recommendation, id=graphene.ID(required=True))
    recommendations_by_source = graphene.List(Recommendation, source=graphene.String(required=True))
    recommendations_by_subsection = graphene.List(Recommendation, subsection_id=graphene.ID(required=True))
    
    decision = graphene.Field(Decision, id=graphene.ID(required=True))
    decisions_by_meeting = graphene.List(Decision, meeting_id=graphene.ID(required=True))
    decisions_by_decision_id = graphene.List(Decision, decision_id=graphene.String(required=True))
    
    financial_impact = graphene.Field(FinancialImpact, id=graphene.ID(required=True))
    financial_impacts_by_amount = graphene.List(FinancialImpact, min_amount=graphene.Float(required=True), max_amount=graphene.Float())
    
    action_item = graphene.Field(ActionItem, id=graphene.ID(required=True))
    action_items_by_status = graphene.List(ActionItem, status=graphene.String(required=True))
    action_items_by_assignee = graphene.List(ActionItem, assignee=graphene.String(required=True))

    def resolve_meeting(self, info, id):
        return Meeting(**get_meeting(id)) if get_meeting(id) else None

    def resolve_meetings(self, info, limit=None, offset=0):
        meetings = sample_meetings
        if limit:
            return [Meeting(**meeting) for meeting in meetings[offset:offset+limit]]
        return [Meeting(**meeting) for meeting in meetings[offset:]]

    def resolve_meetings_by_date(self, info, start_date, end_date=None):
        # This would filter meetings by date range
        return [Meeting(**meeting) for meeting in sample_meetings]

    def resolve_attendee(self, info, id):
        return Attendee(**get_attendee(id)) if get_attendee(id) else None

    def resolve_attendees(self, info, limit=None, offset=0):
        attendees = sample_attendees
        if limit:
            return [Attendee(**attendee) for attendee in attendees[offset:offset+limit]]
        return [Attendee(**attendee) for attendee in attendees[offset:]]

    def resolve_section(self, info, id):
        return Section(**get_section(id)) if get_section(id) else None

    def resolve_sections_by_meeting(self, info, meeting_id):
        return [Section(**section) for section in get_meeting_sections(meeting_id)]

    def resolve_subsection(self, info, id):
        return SubSection(**get_subsection(id)) if get_subsection(id) else None

    def resolve_subsections_by_section(self, info, section_id):
        return [SubSection(**subsection) for subsection in get_section_subsections(section_id)]

    def resolve_recommendation(self, info, id):
        return Recommendation(**get_recommendation(id)) if get_recommendation(id) else None

    def resolve_recommendations_by_source(self, info, source):
        recommendations = [rec for rec in sample_recommendations if rec["source"] == source]
        return [Recommendation(**rec) for rec in recommendations]

    def resolve_recommendations_by_subsection(self, info, subsection_id):
        return [Recommendation(**rec) for rec in get_subsection_recommendations(subsection_id)]

    def resolve_decision(self, info, id):
        return Decision(**get_decision(id)) if get_decision(id) else None

    def resolve_decisions_by_meeting(self, info, meeting_id):
        # This would need to be implemented to find decisions for a meeting
        return [Decision(**decision) for decision in sample_decisions]

    def resolve_decisions_by_decision_id(self, info, decision_id):
        decisions = [dec for dec in sample_decisions if dec["decision_id"] == decision_id]
        return [Decision(**dec) for dec in decisions]

    def resolve_financial_impact(self, info, id):
        return FinancialImpact(**get_financial_impact(id)) if get_financial_impact(id) else None

    def resolve_financial_impacts_by_amount(self, info, min_amount, max_amount=None):
        if max_amount:
            impacts = [fi for fi in sample_financial_impacts if min_amount <= fi["amount"] <= max_amount]
        else:
            impacts = [fi for fi in sample_financial_impacts if min_amount <= fi["amount"]]
        return [FinancialImpact(**fi) for fi in impacts]

    def resolve_action_item(self, info, id):
        return ActionItem(**get_action_item(id)) if get_action_item(id) else None

    def resolve_action_items_by_status(self, info, status):
        items = [ai for ai in sample_action_items if ai["status"] == status]
        return [ActionItem(**ai) for ai in items]

    def resolve_action_items_by_assignee(self, info, assignee):
        items = [ai for ai in sample_action_items if ai["assignee"] == assignee]
        return [ActionItem(**ai) for ai in items]

# Mutation class for GraphQL schema
class Mutation(graphene.ObjectType):
    create_meeting = graphene.Field(Meeting, meeting_input=MeetingInput(required=True))
    update_meeting = graphene.Field(Meeting, id=graphene.ID(required=True), meeting_input=MeetingInput(required=True))
    delete_meeting = graphene.Boolean(id=graphene.ID(required=True))
    
    create_attendee = graphene.Field(Attendee, attendee_input=AttendeeInput(required=True))
    update_attendee = graphene.Field(Attendee, id=graphene.ID(required=True), attendee_input=AttendeeInput(required=True))
    delete_attendee = graphene.Boolean(id=graphene.ID(required=True))
    
    create_partial_attendee = graphene.Field(PartialAttendee, partial_attendee_input=PartialAttendeeInput(required=True))
    update_partial_attendee = graphene.Field(PartialAttendee, id=graphene.ID(required=True), partial_attendee_input=PartialAttendeeInput(required=True))
    delete_partial_attendee = graphene.Boolean(id=graphene.ID(required=True))
    
    create_section = graphene.Field(Section, section_input=SectionInput(required=True))
    update_section = graphene.Field(Section, id=graphene.ID(required=True), section_input=SectionInput(required=True))
    delete_section = graphene.Boolean(id=graphene.ID(required=True))
    
    create_subsection = graphene.Field(SubSection, subsection_input=SubSectionInput(required=True))
    update_subsection = graphene.Field(SubSection, id=graphene.ID(required=True), subsection_input=SubSectionInput(required=True))
    delete_subsection = graphene.Boolean(id=graphene.ID(required=True))
    
    create_recommendation = graphene.Field(Recommendation, recommendation_input=RecommendationInput(required=True))
    update_recommendation = graphene.Field(Recommendation, id=graphene.ID(required=True), recommendation_input=RecommendationInput(required=True))
    delete_recommendation = graphene.Boolean(id=graphene.ID(required=True))
    
    create_decision = graphene.Field(Decision, decision_input=DecisionInput(required=True))
    update_decision = graphene.Field(Decision, id=graphene.ID(required=True), decision_input=DecisionInput(required=True))
    delete_decision = graphene.Boolean(id=graphene.ID(required=True))
    
    create_financial_impact = graphene.Field(FinancialImpact, financial_impact_input=FinancialImpactInput(required=True))
    update_financial_impact = graphene.Field(FinancialImpact, id=graphene.ID(required=True), financial_impact_input=FinancialImpactInput(required=True))
    delete_financial_impact = graphene.Boolean(id=graphene.ID(required=True))
    
    create_action_item = graphene.Field(ActionItem, action_item_input=ActionItemInput(required=True))
    update_action_item = graphene.Field(ActionItem, id=graphene.ID(required=True), action_item_input=ActionItemInput(required=True))
    delete_action_item = graphene.Boolean(id=graphene.ID(required=True))

    def resolve_create_meeting(self, info, meeting_input):
        # In a real implementation, this would create a new meeting in the database
        meeting_data = {
            "id": str(uuid.uuid4()),
            "meeting_number": meeting_input.meeting_number,
            "meeting_title": meeting_input.meeting_title,
            "meeting_date": meeting_input.meeting_date,
            "meeting_time": meeting_input.meeting_time,
            "meeting_location": meeting_input.meeting_location,
            "meeting_chairman": meeting_input.meeting_chairman,
            "created_at": datetime.now().isoformat(),
            "pdf_source": meeting_input.pdf_source,
            "language": meeting_input.language
        }
        sample_meetings.append(meeting_data)
        return Meeting(**meeting_data)

    # Other mutation resolvers would be implemented similarly

# Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
