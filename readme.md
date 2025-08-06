# Interactive News App

This is a Python Flask web application that fetches and displays news articles based on user input using the News API.

## Features
- Search for news articles by keyword.
- Displays article title, source, description, and a link to the full article.
- Option to save displayed articles to a text file.
- Responsive UI using Tailwind CSS.

## Setup and Run
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/interactive-news-app.git](https://github.com/your-username/interactive-news-app.git)
    cd interactive-news-app
    ```
2.  **Install dependencies:**
    ```bash
    pip install Flask requests
    ```
3.  **Get your News API Key:**
    * Register for a free API key at [News API](https://newsapi.org/).
    * Replace `"YOUR_API_KEY"` in `app.py` with your actual key. (Note: In this project, the key is already hardcoded for simplicity, but for real-world apps, use environment variables.)
4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
5.  **Access the app:** Open your web browser and go to `http://127.0.0.1:5000/`.

## API Used
This project uses the [News API](https://newsapi.org/) `/v2/everything` endpoint.

## Submission Requirements
This project fulfills the requirements for the ProSensia Python Internship Day 21 task.