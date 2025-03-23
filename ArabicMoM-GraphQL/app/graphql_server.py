from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()



# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Import schema after Flask is initialized
from schema import schema

# Import GraphQLView after schema to avoid circular imports
from flask_graphql import GraphQLView

# Custom GraphQL view with error logging
class CustomGraphQLView(GraphQLView):
    def dispatch_request(self):
        try:
            request_data = self.parse_body()
            if request_data and 'query' in request_data:
                query = request_data.get('query', '')
                variables = request_data.get('variables', {})
                operation_name = request_data.get('operationName', None)
                
                # Log the incoming query for debugging
                logging.info(f"Received GraphQL Query: {query}")
                logging.info(f"Variables: {variables}")
                
                # Let the parent class handle the execution
                result = super().dispatch_request()
                
                # Check for errors in the response
                if hasattr(result, 'status_code') and result.status_code != 200:
                    logging.error(f"GraphQL Error: Status code {result.status_code}")
                    logging.error(f"Failed Query: {query}")
                    logging.error(f"Variables: {variables}")
                
                return result
            return super().dispatch_request()
        except Exception as e:
            logging.error(f"Exception in GraphQL request: {str(e)}")
            return super().dispatch_request()

# Add GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=CustomGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

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

# Health check
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.environ.get('GRAPHQL_SERVER_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
