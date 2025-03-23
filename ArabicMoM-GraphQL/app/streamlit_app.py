import streamlit as st
import requests
import json
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Arabic MoM GraphQL Explorer",
    page_icon="📝",
    layout="wide"
)

# GraphQL API endpoint
GRAPHQL_PORT = os.getenv('GRAPHQL_SERVER_PORT', '5001')
GRAPHQL_URL = f"http://localhost:{GRAPHQL_PORT}/graphql"

# Helper function to execute GraphQL queries
def run_query(query, variables=None):
    """Execute a GraphQL query and return the response"""
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables}
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to GraphQL API: {str(e)}")
        return None

# Helper function to format dates
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except:
        return date_str

# Main app
def main():
    st.title("Arabic Minutes of Meeting Explorer")
    st.write("Explore and visualize Minutes of Meeting data using GraphQL")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select a page",
            ["Meetings", "Attendees", "Sections & Subsections", "Recommendations", "Decisions", "Action Items"]
        )
    
    # Check API connection
    with st.spinner("Connecting to GraphQL API..."):
        test_query = """
        query {
            meetings {
                id
            }
        }
        """
        response = run_query(test_query)
        
        if not response:
            st.error("Failed to connect to the GraphQL API. Please make sure the server is running.")
            st.info("Run the server with: `python mom_graphql_server.py`")
            return
    
    # Display different pages based on selection
    if page == "Meetings":
        display_meetings_page()
    elif page == "Attendees":
        display_attendees_page()
    elif page == "Sections & Subsections":
        display_sections_page()
    elif page == "Recommendations":
        display_recommendations_page()
    elif page == "Decisions":
        display_decisions_page()
    elif page == "Action Items":
        display_action_items_page()

def display_meetings_page():
    st.header("Meetings")
    
    # Query all meetings
    meetings_query = """
    query {
        meetings {
            id
            meetingNumber
            meetingTitle
            meetingDate
            meetingTime
            meetingLocation
            meetingChairman
            language
        }
    }
    """
    
    response = run_query(meetings_query)
    
    if response and "data" in response and "meetings" in response["data"]:
        meetings = response["data"]["meetings"]
        
        if not meetings:
            st.info("No meetings found in the database.")
            return
        
        # Display meetings in a dataframe with renamed columns for display
        meetings_df = pd.DataFrame(meetings)
        # Rename columns for display
        meetings_df = meetings_df.rename(columns={
            "meetingNumber": "Meeting Number",
            "meetingTitle": "Title",
            "meetingDate": "Date",
            "meetingTime": "Time",
            "meetingLocation": "Location",
            "meetingChairman": "Chairman",
            "language": "Language"
        })
        meetings_df["Date"] = meetings_df["Date"].apply(format_date)
        
        st.dataframe(meetings_df)
        
        # Meeting details section
        st.subheader("Meeting Details")
        
        selected_meeting_id = st.selectbox(
            "Select a meeting to view details",
            options=[m["id"] for m in meetings],
            format_func=lambda x: next((m["meetingTitle"] for m in meetings if m["id"] == x), x)
        )
        
        if selected_meeting_id:
            display_meeting_details(selected_meeting_id)
    else:
        st.error("Failed to retrieve meetings data.")

def display_meeting_details(meeting_id):
    # Query meeting details with attendees and sections
    meeting_query = f"""
    query {{
        meeting(id: "{meeting_id}") {{
            id
            meetingNumber
            meetingTitle
            meetingDate
            meetingTime
            meetingLocation
            meetingChairman
            language
            attendees {{
                id
                name
                title
                role
            }}
            partialAttendees {{
                id
                name
                title
                role
                notes
            }}
            sections {{
                id
                title
                order
                content
            }}
        }}
    }}
    """
    
    response = run_query(meeting_query)
    
    if response and "data" in response and "meeting" in response["data"]:
        meeting = response["data"]["meeting"]
        
        # Display meeting info
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Meeting Number:** {meeting['meetingNumber']}")
            st.write(f"**Title:** {meeting['meetingTitle']}")
            st.write(f"**Date:** {format_date(meeting['meetingDate'])}")
            st.write(f"**Time:** {meeting['meetingTime']}")
        
        with col2:
            st.write(f"**Location:** {meeting['meetingLocation']}")
            st.write(f"**Chairman:** {meeting['meetingChairman']}")
            st.write(f"**Language:** {meeting['language']}")
        
        # Display attendees in tabs
        if meeting["attendees"] or meeting["partialAttendees"]:
            attendees_tabs = st.tabs(["Full Attendees", "Partial Attendees"])
            
            with attendees_tabs[0]:
                if meeting["attendees"]:
                    st.dataframe(pd.DataFrame(meeting["attendees"]))
                else:
                    st.info("No full attendees for this meeting.")
            
            with attendees_tabs[1]:
                if meeting["partialAttendees"]:
                    st.dataframe(pd.DataFrame(meeting["partialAttendees"]))
                else:
                    st.info("No partial attendees for this meeting.")
        
        # Display sections
        if meeting["sections"]:
            st.subheader("Meeting Sections")
            
            for section in sorted(meeting["sections"], key=lambda x: x["order"]):
                with st.expander(f"{section['order']}. {section['title']}"):
                    st.write(section["content"])
                    
                    # Query subsections for this section
                    subsections_query = f"""
                    query {{
                        subsectionsBySection(sectionId: "{section['id']}") {{
                            id
                            title
                            order
                            content
                        }}
                    }}
                    """
                    
                    subsections_response = run_query(subsections_query)
                    
                    if subsections_response and "data" in subsections_response and "subsectionsBySection" in subsections_response["data"]:
                        subsections = subsections_response["data"]["subsectionsBySection"]
                        
                        if subsections:
                            st.write("**Subsections:**")
                            
                            for subsection in sorted(subsections, key=lambda x: x["order"]):
                                with st.expander(f"{subsection['order']}. {subsection['title']}"):
                                    st.write(subsection["content"])
                                    
                                    # Get recommendations and decisions for this subsection
                                    display_subsection_items(subsection["id"])
        else:
            st.info("No sections found for this meeting.")

def display_subsection_items(subsection_id):
    # Query recommendations for this subsection - note we don't have recommendations_by_subsection in our schema
    # so we'll use recommendations_by_source and filter client-side
    recommendations_query = f"""
    query {{
        recommendationsBySource(source: "لجنة إدارة المخاطر") {{
            id
            recommendationId
            source
            date
            content
            subsectionId
        }}
    }}
    """
    
    recommendations_response = run_query(recommendations_query)
    
    if recommendations_response and "data" in recommendations_response and "recommendationsBySource" in recommendations_response["data"]:
        # Filter recommendations for this subsection
        all_recommendations = recommendations_response["data"]["recommendationsBySource"]
        recommendations = [r for r in all_recommendations if r.get("subsectionId") == subsection_id]
        
        if recommendations:
            st.write("**Recommendations:**")
            
            for recommendation in recommendations:
                st.markdown(f"""
                **ID:** {recommendation['recommendationId']}  
                **Source:** {recommendation['source']}  
                **Date:** {format_date(recommendation['date']) if recommendation['date'] else 'N/A'}  
                **Content:** {recommendation['content']}
                """)
                st.markdown("---")
    
    # Query decisions for this subsection - note we don't have decisions_by_subsection in our schema
    # so we'll use a workaround by getting all decisions and filtering client-side
    decisions_query = f"""
    query {{
        decisionsByMeeting(meetingId: "m1") {{
            id
            decisionId
            date
            content
            subsectionId
            financial_impact {{
                amount
                currency
                description
                budget_source
            }}
            action_items {{
                id
                description
                assignee
                due_date
                status
            }}
        }}
    }}
    """
    
    decisions_response = run_query(decisions_query)
    
    if decisions_response and "data" in decisions_response and "decisionsByMeeting" in decisions_response["data"]:
        # Filter decisions for this subsection
        all_decisions = decisions_response["data"]["decisionsByMeeting"]
        decisions = [d for d in all_decisions if d.get("subsectionId") == subsection_id]
        
        if decisions:
            st.write("**Decisions:**")
            
            for decision in decisions:
                st.markdown(f"""
                **ID:** {decision['decisionId']}  
                **Date:** {format_date(decision['date'])}  
                **Content:** {decision['content']}
                """)
                
                # Display financial impact if available
                if decision["financial_impact"]:
                    fi = decision["financial_impact"]
                    st.markdown(f"""
                    **Financial Impact:**  
                    Amount: {fi['amount']} {fi['currency']}  
                    Description: {fi['description']}  
                    Budget Source: {fi['budget_source']}
                    """)
                
                # Display action items if available
                if decision["action_items"]:
                    st.write("**Action Items:**")
                    action_items_df = pd.DataFrame(decision["action_items"])
                    action_items_df["due_date"] = action_items_df["due_date"].apply(lambda x: format_date(x) if x else "N/A")
                    st.dataframe(action_items_df)
                
                st.markdown("---")

def display_attendees_page():
    st.header("Attendees")
    
    # Query all attendees
    attendees_query = """
    query {
        attendees {
            id
            name
            title
            role
            email
        }
    }
    """
    
    response = run_query(attendees_query)
    
    if response and "data" in response and "attendees" in response["data"]:
        attendees = response["data"]["attendees"]
        
        if not attendees:
            st.info("No attendees found in the database.")
            return
        
        # Display attendees in a dataframe
        st.dataframe(pd.DataFrame(attendees))
        
        # Attendee details section
        st.subheader("Attendee Details")
        
        selected_attendee_id = st.selectbox(
            "Select an attendee to view details",
            options=[a["id"] for a in attendees],
            format_func=lambda x: next((a["name"] for a in attendees if a["id"] == x), x)
        )
        
        if selected_attendee_id:
            # Query attendee details with meetings
            attendee_query = f"""
            query {{
                attendee(id: "{selected_attendee_id}") {{
                    id
                    name
                    title
                    role
                    email
                    meetings {{
                        id
                        meetingTitle
                        meetingDate
                    }}
                }}
            }}
            """
            
            attendee_response = run_query(attendee_query)
            
            if attendee_response and "data" in attendee_response and "attendee" in attendee_response["data"]:
                attendee = attendee_response["data"]["attendee"]
                
                # Display attendee info
                st.write(f"**Name:** {attendee['name']}")
                st.write(f"**Title:** {attendee['title']}")
                st.write(f"**Role:** {attendee['role']}")
                st.write(f"**Email:** {attendee['email']}")
                
                # Display meetings
                if attendee["meetings"]:
                    st.subheader("Meetings Attended")
                    
                    meetings_df = pd.DataFrame(attendee["meetings"])
                    # Rename columns for display
                    meetings_df = meetings_df.rename(columns={
                        "meetingTitle": "Title",
                        "meetingDate": "Date"
                    })
                    meetings_df["Date"] = meetings_df["Date"].apply(format_date)
                    st.dataframe(meetings_df[["Title", "Date"]])
                else:
                    st.info("This attendee has not attended any meetings.")
    else:
        st.error("Failed to retrieve attendees data.")

def display_sections_page():
    st.header("Sections & Subsections")
    
    # Query all meetings for selection
    meetings_query = """
    query {
        meetings {
            id
            meeting_title
            meeting_date
        }
    }
    """
    
    response = run_query(meetings_query)
    
    if response and "data" in response and "meetings" in response["data"]:
        meetings = response["data"]["meetings"]
        
        if not meetings:
            st.info("No meetings found in the database.")
            return
        
        # Select a meeting
        selected_meeting_id = st.selectbox(
            "Select a meeting",
            options=[m["id"] for m in meetings],
            format_func=lambda x: next((f"{m['meeting_title']} ({format_date(m['meeting_date'])})" for m in meetings if m["id"] == x), x)
        )
        
        if selected_meeting_id:
            # Query sections for the selected meeting
            sections_query = f"""
            query {{
                sections_by_meeting(meeting_id: "{selected_meeting_id}") {{
                    id
                    title
                    order
                    content
                }}
            }}
            """
            
            sections_response = run_query(sections_query)
            
            if sections_response and "data" in sections_response and "sections_by_meeting" in sections_response["data"]:
                sections = sections_response["data"]["sections_by_meeting"]
                
                if not sections:
                    st.info("No sections found for this meeting.")
                    return
                
                # Display sections
                for section in sorted(sections, key=lambda x: x["order"]):
                    with st.expander(f"{section['order']}. {section['title']}"):
                        st.write(section["content"])
                        
                        # Query subsections for this section
                        subsections_query = f"""
                        query {{
                            subsectionsBySection(sectionId: "{section['id']}") {{
                                id
                                title
                                order
                                content
                            }}
                        }}
                        """
                        
                        subsections_response = run_query(subsections_query)
                        
                        if subsections_response and "data" in subsections_response and "subsectionsBySection" in subsections_response["data"]:
                            subsections = subsections_response["data"]["subsectionsBySection"]
                            
                            if subsections:
                                st.write("**Subsections:**")
                                
                                for subsection in sorted(subsections, key=lambda x: x["order"]):
                                    with st.expander(f"{subsection['order']}. {subsection['title']}"):
                                        st.write(subsection["content"])
                            else:
                                st.info("No subsections found for this section.")
            else:
                st.error("Failed to retrieve sections data.")
    else:
        st.error("Failed to retrieve meetings data.")

def display_recommendations_page():
    st.header("Recommendations")
    
    # Query all recommendations
    recommendations_query = """
    query {
        recommendationsBySource(source: "لجنة إدارة المخاطر") {
            id
            recommendationId
            source
            date
            content
            subsectionId
        }
    }
    """
    
    response = run_query(recommendations_query)
    
    if response and "data" in response and "recommendationsBySource" in response["data"]:
        recommendations = response["data"]["recommendationsBySource"]
        
        if not recommendations:
            st.info("No recommendations found in the database.")
            return
        
        # Rename columns for display
        recommendations_df = pd.DataFrame(recommendations)
        recommendations_df = recommendations_df.rename(columns={
            "recommendationId": "Recommendation ID",
            "source": "Source",
            "date": "Date",
            "content": "Content"
        })
        recommendations_df["Date"] = recommendations_df["Date"].apply(lambda x: format_date(x) if x else "N/A")
        
        # Display columns for dataframe
        display_columns = ["Recommendation ID", "Source", "Date", "Content"]
        st.dataframe(recommendations_df[display_columns])
        
        # Recommendation details
        st.subheader("Recommendation Details")
        
        selected_recommendation_id = st.selectbox(
            "Select a recommendation to view details",
            options=[r["id"] for r in recommendations],
            format_func=lambda x: next((f"{r['recommendationId']} - {r['content'][:50]}..." for r in recommendations if r["id"] == x), x)
        )
        
        if selected_recommendation_id:
            recommendation = next((r for r in recommendations if r["id"] == selected_recommendation_id), None)
            
            if recommendation:
                st.write(f"**ID:** {recommendation['recommendationId']}")
                st.write(f"**Source:** {recommendation['source']}")
                st.write(f"**Date:** {format_date(recommendation['date']) if recommendation['date'] else 'N/A'}")
                st.write(f"**Content:** {recommendation['content']}")
                
                # Get subsection info if needed
                if recommendation["subsectionId"]:
                    st.write(f"**Subsection ID:** {recommendation['subsectionId']}")
    else:
        st.error("Failed to retrieve recommendations data.")

def display_decisions_page():
    st.header("Decisions")
    
    # Query all decisions
    decisions_query = """
    query {
        decisionsByMeeting(meetingId: "m1") {
            id
            decisionId
            date
            content
            subsectionId
        }
    }
    """
    
    response = run_query(decisions_query)
    
    if response and "data" in response and "decisionsByMeeting" in response["data"]:
        decisions = response["data"]["decisionsByMeeting"]
        
        if not decisions:
            st.info("No decisions found in the database.")
            return
        
        # Rename columns for display
        decisions_df = pd.DataFrame(decisions)
        decisions_df = decisions_df.rename(columns={
            "decisionId": "Decision ID",
            "date": "Date",
            "content": "Content"
        })
        decisions_df["Date"] = decisions_df["Date"].apply(format_date)
        
        # Display columns for dataframe
        display_columns = ["Decision ID", "Date", "Content"]
        st.dataframe(decisions_df[display_columns])
        
        # Decision details
        st.subheader("Decision Details")
        
        selected_decision_id = st.selectbox(
            "Select a decision to view details",
            options=[d["id"] for d in decisions],
            format_func=lambda x: next((f"{d['decisionId']} - {d['content'][:50]}..." for d in decisions if d["id"] == x), x)
        )
        
        if selected_decision_id:
            decision = next((d for d in decisions if d["id"] == selected_decision_id), None)
            
            if decision:
                st.write(f"**ID:** {decision['decisionId']}")
                st.write(f"**Date:** {format_date(decision['date'])}")
                st.write(f"**Content:** {decision['content']}")
                
                # Get subsection info if needed
                if decision["subsectionId"]:
                    st.write(f"**Subsection ID:** {decision['subsectionId']}")
                
                # Note: We would need to make separate queries to get financial impact and action items
                st.info("Financial impact and action items data requires additional queries.")
    else:
        st.error("Failed to retrieve decisions data.")

def display_action_items_page():
    st.header("Action Items")
    
    # Query all action items
    action_items_query = """
    query {
        action_items_by_status(status: "PENDING") {
            id
            description
            assignee
            due_date
            status
            decision_id
        }
    }
    """
    
    response = run_query(action_items_query)
    
    if response and "data" in response and "action_items_by_status" in response["data"]:
        action_items = response["data"]["action_items_by_status"]
        
        if not action_items:
            st.info("No action items found in the database.")
            return
        
        # Rename columns for display
        action_items_df = pd.DataFrame(action_items)
        action_items_df = action_items_df.rename(columns={
            "description": "Description",
            "assignee": "Assignee",
            "due_date": "Due Date",
            "status": "Status"
        })
        action_items_df["Due Date"] = action_items_df["Due Date"].apply(lambda x: format_date(x) if x else "N/A")
        
        # Display columns for dataframe
        display_columns = ["Description", "Assignee", "Due Date", "Status"]
        st.dataframe(action_items_df[display_columns])
        
        # Action item details
        st.subheader("Action Item Details")
        
        selected_action_item_id = st.selectbox(
            "Select an action item to view details",
            options=[a["id"] for a in action_items],
            format_func=lambda x: next((f"{a['description'][:50]}... ({a['status']})" for a in action_items if a["id"] == x), x)
        )
        
        if selected_action_item_id:
            action_item = next((a for a in action_items if a["id"] == selected_action_item_id), None)
            
            if action_item:
                st.write(f"**Description:** {action_item['description']}")
                st.write(f"**Assignee:** {action_item['assignee']}")
                st.write(f"**Due Date:** {format_date(action_item['due_date']) if action_item['due_date'] else 'N/A'}")
                st.write(f"**Status:** {action_item['status']}")
                
                # Display related decision ID
                if action_item["decisionId"]:
                    st.write(f"**Related Decision ID:** {action_item['decisionId']}")
    else:
        st.error("Failed to retrieve action items data.")

if __name__ == "__main__":
    main()
