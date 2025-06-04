from flask import render_template, request, jsonify
from flask_app import app
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Load environment variables

# Use the GOOGLE_API_KEY from your .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route('/places')
def places():
    return render_template('places.html')

@app.route('/search_places')
def search_places():
    # Get the search query from the request's arguments
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Construct the Google Places API URL using the textsearch endpoint
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Debug output to the console
        print(data)

        # Return the data (which should include a 'results' field) as JSON
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch places", "details": str(e)}), 500
