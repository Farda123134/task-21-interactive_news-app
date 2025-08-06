import os
import requests
from flask import Flask, render_template, request, send_file
import json
from datetime import datetime

app = Flask(__name__)

# Replace with your actual News API key
NEWS_API_KEY = "f031b759fd5945f5801df9dca1312916"
# Corrected: Removed Markdown formatting from the URL string
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page and news search functionality.
    GET: Displays the search form.
    POST: Processes the search query, fetches news, and displays results.
    """
    articles = []
    error_message = None
    query = ""

    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            error_message = "Please enter a search query."
        else:
            params = {
                'q': query,
                'apiKey': NEWS_API_KEY,
                'sortBy': 'relevancy',
                'language': 'en', # You can change or make this user-selectable
                'pageSize': 10    # Limit to 10 articles for brevity
            }
            try:
                response = requests.get(NEWS_API_BASE_URL, params=params)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
                data = response.json()

                if data['status'] == 'ok' and data['totalResults'] > 0:
                    articles = data['articles']
                    # Store articles in session or a temporary file if you want to save them later
                    # For simplicity, we'll pass them directly to the template for display
                else:
                    error_message = "No articles found for your query. Please try a different keyword."

            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 401:
                    error_message = "API Key Invalid or Missing. Please check your API key."
                elif response.status_code == 429:
                    error_message = "Too many requests. You have hit your API rate limit. Please try again later."
                else:
                    error_message = f"HTTP error occurred: {http_err} - Status Code: {response.status_code}"
            except requests.exceptions.ConnectionError:
                error_message = "Network error: Could not connect to the News API. Please check your internet connection."
            except requests.exceptions.Timeout:
                error_message = "The request to the News API timed out. Please try again."
            except requests.exceptions.RequestException as e:
                error_message = f"An unexpected error occurred: {e}"

    return render_template('index.html', articles=articles, error_message=error_message, query=query)

@app.route('/save_articles', methods=['POST'])
def save_articles():
    """
    Saves the currently displayed articles to a text file and allows the user to download it.
    """
    articles_json = request.form.get('articles_data')
    if not articles_json:
        return "No articles to save.", 400

    try:
        articles = json.loads(articles_json)
    except json.JSONDecodeError:
        return "Invalid article data.", 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"news_articles_{timestamp}.txt"
    filepath = os.path.join(app.root_path, 'temp', filename) # Save to a 'temp' directory

    # Ensure the 'temp' directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"News Articles - Query: {request.form.get('original_query', 'N/A')}\n")
        f.write("="*50 + "\n\n")
        for i, article in enumerate(articles):
            f.write(f"--- Article {i+1} ---\n")
            f.write(f"Title: {article.get('title', 'N/A')}\n")
            f.write(f"Source: {article.get('source', {}).get('name', 'N/A')}\n")
            f.write(f"Author: {article.get('author', 'N/A')}\n")
            f.write(f"Published At: {article.get('publishedAt', 'N/A')}\n")
            f.write(f"URL: {article.get('url', 'N/A')}\n")
            f.write(f"Description: {article.get('description', 'N/A')}\n")
            f.write("\n" + "="*50 + "\n\n")

    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    # Create the 'temp' directory if it doesn't exist
    os.makedirs(os.path.join(app.root_path, 'temp'), exist_ok=True)
    app.run(debug=True) # debug=True allows auto-reloading and better error messages
