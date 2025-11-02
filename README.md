# Ron's Personal Blog

A minimalist blog inspired by Guillermo Rauch's design, built with Flask and tailored for product management and AI content.

## Features

- Clean, minimalist design inspired by rauchg.com
- Dark/light mode toggle with system preference detection
- Responsive design that works on all devices
- View counter for articles (like Rauch's impressive metrics)
- Newsletter subscription
- SEO optimized with Open Graph and Twitter Card support
- Fast loading with optimized CSS and JavaScript

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd ron-blog
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the development server:**
   ```bash
   python app.py
   ```

6. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## Project Structure

```
ron-blog/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env                  # Environment variables (create this)
├── .gitignore            # Git ignore file
├── app/
│   ├── templates/        # Jinja2 templates
│   │   ├── base.html     # Base template
│   │   ├── index.html    # Homepage
│   │   ├── post.html     # Individual post
│   │   ├── about.html    # About page
│   │   └── 404.html      # Error page
│   └── static/           # Static files
│       ├── css/
│       │   └── style.css # Custom styles
│       └── js/
│           └── main.js   # JavaScript functionality
└── content/
    └── posts/            # Blog posts (future markdown files)
```

## Adding New Posts

Currently, posts are defined in `app.py` as sample data. To add a new post:

1. Add a new post dictionary to the `sample_posts` list in the `load_posts()` function
2. Include: slug, title, date, views, content
3. Restart the development server

In the future, this will be enhanced to load posts from Markdown files in the `content/posts/` directory.

## Customization

### Changing Colors
- Edit the gradient in `static/css/style.css` (`.gradient-text`)
- Modify Tailwind classes in templates for theme colors

### Adding Analytics
- Replace placeholder tracking in `static/js/main.js`
- Add Google Analytics, Mixpanel, or your preferred service

### Newsletter Integration
- Update the `subscribeNewsletter()` function in `main.js`
- Connect to ConvertKit, Mailchimp, or your email service

## Deployment

This blog is designed to deploy easily to Vercel, Netlify, or any platform that supports Flask applications.

### Vercel Deployment (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Vercel will automatically detect Flask and deploy

### Environment Variables

Create a `.env` file for local development:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

For production, set these in your hosting platform's environment settings.

## Content Strategy

The blog is optimized for product management and AI content, with sample articles covering:

- Product strategy and growth (Cineplex case study)
- AI and technical innovation (Memory systems)
- Customer research methodologies
- Career development and learning
- Industry insights

## Performance

- Lightweight design with minimal JavaScript
- Optimized images and CSS
- Fast loading times (target: <2 seconds)
- Responsive design for all devices

## License

MIT License - feel free to use this as a template for your own blog.

## Contact

Ron Mashate
- Email: rmashate@gmail.com
- LinkedIn: [linkedin.com/in/rmashate](https://linkedin.com/in/rmashate)
- Location: Toronto, ON, Canada
