# Sample Data

This directory is for storing sample data files for the Arabic MoM GraphQL Explorer.

## Data Format

The application currently uses in-memory sample data defined in the schema.py file. If you want to use external data files:

1. Place your JSON data files in this directory
2. Update the data loading functions in schema.py to read from these files
3. Restart the application

## Sample Data Structure

The expected structure for data files would be:

- meetings.json - Contains meeting information
- attendees.json - Contains attendee information
- sections.json - Contains section information
- recommendations.json - Contains recommendation information
- decisions.json - Contains decision information
- action_items.json - Contains action item information
