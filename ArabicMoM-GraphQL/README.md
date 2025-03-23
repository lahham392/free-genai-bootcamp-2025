# Arabic Minutes of Meeting (MoM) GraphQL Explorer

This application provides a GraphQL API and Streamlit interface for exploring and analyzing Arabic Minutes of Meeting data. It allows users to view meetings, attendees, sections, recommendations, decisions, and action items.

## Project Structure

```
ArabicMoM-GraphQL/
├── app/
│   ├── graphql_server.py    # Flask GraphQL server
│   ├── streamlit_app.py     # Streamlit web interface
│   └── schema.py            # GraphQL schema definitions
├── data/                    # Sample data directory
├── docs/                    # Documentation
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Setup and Installation

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables (already configured in .env file)

## Running the Application

1. Start the GraphQL server:
   ```
   python app/graphql_server.py
   ```
   The server will run on http://localhost:5001/graphql

2. Start the Streamlit app:
   ```
   streamlit run app/streamlit_app.py
   ```
   The Streamlit interface will be available at http://localhost:8501

## Features

- **GraphQL API**: Provides a flexible API for querying meeting data
- **Streamlit Interface**: User-friendly web interface for exploring data
- **Meeting Explorer**: View meeting details, attendees, and sections
- **Recommendations**: View and filter recommendations by source
- **Decisions**: View and filter decisions by meeting
- **Action Items**: Track action items and their status

## GraphQL Schema

The application uses a GraphQL schema that includes the following main types:
- Meeting
- Attendee
- Section
- SubSection
- Recommendation
- Decision
- FinancialImpact
- ActionItem

## Troubleshooting

If you encounter 400 errors when using the application:
1. Check the GraphQL server logs for detailed error information
2. Ensure that query names and field names match the schema exactly (camelCase vs snake_case)
3. Verify that all required fields are included in your queries

## License

This project is licensed under the MIT License - see the LICENSE file for details.
