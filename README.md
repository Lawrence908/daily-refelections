# Daily Reflections
Daily wisdom, one focused reflection at a time.

A simple Flask web application that serves inspirational quotes with a deterministic "quote of the day" feature and allows users to contribute their own quotes.

## Features

- 📅 **Quote of the Day**: Deterministic daily quotes that remain consistent throughout the day
- ✏️ **Quote Submission**: Add your own inspirational quotes to the collection
- 🌐 **JSON API**: RESTful endpoint for programmatic access
- 📱 **Mobile-First Design**: Responsive design that works on all devices
- 🌙 **Theme Aware**: Automatic dark/light mode based on user preferences
- 💾 **Simple Storage**: JSON-based storage for easy deployment and portability

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lawrence908/daily-refelections.git
   cd daily-refelections
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env .env.local
   # Edit .env.local and set a secure SECRET_KEY
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## API Usage

### Get Quote of the Day
```bash
curl http://localhost:5000/api/quote
```

Response:
```json
{
  "text": "The journey of a thousand miles begins with one step.",
  "author": "Lao Tzu"
}
```

## Project Structure

```
daily-refelections/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (template)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage template
│   └── add.html          # Quote submission form
├── static/               # Static assets
│   └── styles.css        # CSS with dark/light theme support
├── data/                 # Data storage
│   ├── quotes.json       # Master quotes collection
│   └── user_entries.json # User-submitted quotes backup
└── docs/                 # Documentation
    └── planning.md       # Planning notes and architecture decisions
```

## Roadmap

### Phase 1 - Core Features ✅
- [x] Basic Flask application structure
- [x] Quote of the day functionality
- [x] Quote submission form
- [x] JSON API endpoint
- [x] Responsive design
- [x] Dark/light theme support

### Phase 2 - Enhanced Features (Future)
- [ ] User authentication and profiles
- [ ] Quote rating and favorites system
- [ ] Categories and tags for quotes
- [ ] Search functionality
- [ ] Admin panel for quote management
- [ ] Email notifications for daily quotes

### Phase 3 - Advanced Features (Future)
- [ ] Database migration (PostgreSQL/SQLite)
- [ ] Quote sharing on social media
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Mobile app companion
- [ ] Quote subscription service

## Contributing

We welcome contributions! Here's how you can help:

1. **Add Quotes**: Use the web interface to submit inspirational quotes
2. **Report Issues**: Create GitHub issues for bugs or feature requests
3. **Submit PRs**: Fork the repo and submit pull requests for improvements
4. **Documentation**: Help improve documentation and examples

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/) 
- Styled with modern CSS and responsive design principles
- Inspired by the need for daily wisdom and reflection
