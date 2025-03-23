@echo off
echo Starting Arabic MoM GraphQL Explorer...

REM Start the GraphQL server in a new window
start cmd /k "cd /d %~dp0 && python app/graphql_server.py"

REM Wait for GraphQL server to start
timeout /t 3 /nobreak

REM Start the Streamlit app
echo Starting Streamlit app...
streamlit run app/streamlit_app.py

echo Application stopped.
