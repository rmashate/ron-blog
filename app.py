import os
from datetime import datetime
from flask import Flask, render_template, abort, request, jsonify
import markdown
import yaml
import json
from pathlib import Path
import re

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

class BlogPost:
    def __init__(self, slug, title, date, content, views=0, featured=False):
        self.slug = slug
        self.title = title
        self.date = date
        self.content = content
        self.views = views
        self.featured = featured
        self.year = date.year

def load_posts():
    """Load all blog posts from the content directory"""
    posts = []
    content_dir = Path('content/posts')
    
    if content_dir.exists():
        for md_file in content_dir.glob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = yaml.safe_load(parts[1])
                        post_content = parts[2].strip()
                        
                        # Parse date
                        date_str = frontmatter.get('date', '2025-01-01')
                        if isinstance(date_str, str):
                            date = datetime.strptime(date_str, '%Y-%m-%d')
                        else:
                            date = date_str
                        
                        post = BlogPost(
                            slug=frontmatter.get('slug', md_file.stem),
                            title=frontmatter.get('title', 'Untitled'),
                            date=date,
                            content=post_content,
                            views=frontmatter.get('views', 0),
                            featured=frontmatter.get('featured', False)
                        )
                        posts.append(post)
            except Exception as e:
                print(f"Error loading {md_file}: {e}")
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x.date, reverse=True)
    return posts

def group_posts_by_year(posts):
    """Group posts by year for display"""
    grouped = {}
    for post in posts:
        year = post.year
        if year not in grouped:
            grouped[year] = []
        grouped[year].append(post)
    return grouped

@app.route('/')
def index():
    posts = load_posts()
    grouped_posts = group_posts_by_year(posts)
    return render_template('index.html', grouped_posts=grouped_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/<slug>')
def post(slug):
    posts = load_posts()
    post = next((p for p in posts if p.slug == slug), None)
    if not post:
        abort(404)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(post.content, extensions=['codehilite', 'fenced_code'])
    post.html_content = html_content
    
    # Increment view count (in a real app, you'd save this to a database)
    post.views += 1
    
    return render_template('post.html', post=post)

@app.route('/api/views/<slug>', methods=['POST'])
def increment_views(slug):
    """API endpoint to increment post views"""
    # In a real implementation, this would update a database
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
