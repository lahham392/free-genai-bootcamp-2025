# Arabic MoM GraphQL Explorer - User Guide

This guide will help you navigate and use the Arabic Minutes of Meeting (MoM) GraphQL Explorer application.

## Getting Started

1. Start the application using one of the provided scripts:
   - On Linux/Mac: `./run.sh`
   - On Windows: Double-click `run.bat`

2. The application consists of two main components:
   - GraphQL Server (http://localhost:5001/graphql)
   - Streamlit Web Interface (http://localhost:8501)

## Using the Streamlit Interface

The Streamlit interface provides an easy-to-use web application for exploring the Arabic MoM data.

### Main Menu

The sidebar menu allows you to navigate between different sections of the application:

- **Home**: Overview of the application
- **Meetings**: View and explore meeting details
- **Attendees**: View attendee information and their associated meetings
- **Sections**: Explore meeting sections and subsections
- **Recommendations**: View and filter recommendations
- **Decisions**: View and filter decisions
- **Action Items**: Track action items and their status

### Meetings Page

- View a list of all meetings in the system
- Select a specific meeting to view its details
- Explore attendees, sections, and other meeting information

### Recommendations Page

- View all recommendations in the system
- Filter recommendations by source
- Select a recommendation to view its details
- See related information such as the subsection it belongs to

### Decisions Page

- View all decisions made in meetings
- Filter decisions by meeting
- Select a decision to view its details
- See related information such as financial impact and action items

### Action Items Page

- View all action items
- Filter action items by status (pending, completed, etc.)
- See details including assignee, due date, and related decisions

## Using the GraphQL API Directly

For developers or advanced users who want to query the data directly:

1. Access the GraphiQL interface at http://localhost:5001/graphql
2. Use this interface to write and test GraphQL queries
3. Copy successful queries to use in your own applications

### Example Queries

Here are some example queries you can try in the GraphiQL interface:

```graphql
# Get all meetings
query {
  meetings {
    id
    meetingTitle
    meetingDate
  }
}

# Get recommendations by source
query {
  recommendationsBySource(source: "لجنة إدارة المخاطر") {
    id
    recommendationId
    content
  }
}

# Get decisions for a meeting
query {
  decisionsByMeeting(meetingId: "m1") {
    id
    decisionId
    content
  }
}
```

## Troubleshooting

If you encounter issues with the application:

1. **400 Errors in API Calls**: 
   - Check that your query names use camelCase (e.g., `recommendationsBySource`)
   - Ensure field names also use camelCase (e.g., `recommendationId`)
   - Verify that all required parameters are provided

2. **Application Won't Start**:
   - Check that ports 5001 and 8501 are not in use by other applications
   - Ensure all dependencies are installed (`pip install -r requirements.txt`)
   - Check the console for error messages

3. **No Data Displayed**:
   - Verify that the GraphQL server is running
   - Check the connection between Streamlit and the GraphQL server
   - Look at the server logs for any error messages

## Getting Help

If you need additional help:

1. Refer to the documentation in the `docs` folder
2. Check the GraphQL schema documentation for query structure
3. Examine the server logs for detailed error information
