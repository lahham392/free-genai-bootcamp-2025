#!/bin/bash

# Start the GraphQL server in the background
echo "Starting GraphQL server..."
python simple_graphql_server.py &
GRAPHQL_PID=$!

# Wait for GraphQL server to start
sleep 3

# Start the Streamlit app
echo "Starting Streamlit app..."
streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0

# When Streamlit is closed, also kill the GraphQL server
kill $GRAPHQL_PID
