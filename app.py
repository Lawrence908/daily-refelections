import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

# Data file paths
QUOTES_FILE = os.path.join('data', 'quotes.json')
ENTRIES_FILE = os.path.join('data', 'user_entries.json')

def load_json_file(filepath, default=None):
    """Load JSON file with error handling"""
    if default is None:
        default = []
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json_file(filepath, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_quote_of_the_day():
    """Get deterministic quote based on current date"""
    quotes = load_json_file(QUOTES_FILE, [])
    if not quotes:
        return {"text": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu"}
    
    # Use day of year for deterministic selection
    day_of_year = datetime.now().timetuple().tm_yday
    quote_index = (day_of_year - 1) % len(quotes)
    return quotes[quote_index]

@app.route('/')
def index():
    """Homepage with quote of the day"""
    quote = get_quote_of_the_day()
    return render_template('index.html', quote=quote)

@app.route('/add', methods=['GET', 'POST'])
def add_quote():
    """Add new quote"""
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        author = request.form.get('author', '').strip()
        
        if not text:
            flash('Quote text is required.', 'error')
            return render_template('add.html')
        
        if not author:
            author = 'Anonymous'
        
        # Load existing quotes
        quotes = load_json_file(QUOTES_FILE, [])
        
        # Add new quote
        new_quote = {
            'text': text,
            'author': author,
            'added_date': datetime.now().isoformat()
        }
        quotes.append(new_quote)
        
        # Save updated quotes
        save_json_file(QUOTES_FILE, quotes)
        
        # Save to user entries as well
        entries = load_json_file(ENTRIES_FILE, [])
        entries.append(new_quote)
        save_json_file(ENTRIES_FILE, entries)
        
        flash('Quote added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/api/quote')
def api_quote():
    """API endpoint to return quote of the day as JSON"""
    quote = get_quote_of_the_day()
    return jsonify(quote)

if __name__ == '__main__':
    app.run(debug=True)