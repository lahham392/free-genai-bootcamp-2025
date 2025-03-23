#!/bin/bash

# Start the GraphQL server in the background
echo "Starting GraphQL server..."
python app/graphql_server.py &
GRAPHQL_PID=$!

# Wait for GraphQL server to start
sleep 3

# Start the Streamlit app
echo "Starting Streamlit app..."
streamlit run app/streamlit_app.py

# When Streamlit is closed, also kill the GraphQL server
kill $GRAPHQL_PID
