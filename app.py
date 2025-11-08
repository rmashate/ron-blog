from datetime import datetime
from flask import Flask, render_template, abort
import markdown
import yaml
from pathlib import Path
import re
from dateutil import parser as date_parser


_POSTS_CACHE = {
    "signature": None,
    "posts": None,
}

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

class BlogPost:
    def __init__(
        self,
        slug,
        title,
        date,
        content,
        views=0,
        featured=False,
        description=None,
        excerpt=None,
    ):
        self.slug = slug
        self.title = title
        self.date = date
        self.content = content
        self.views = views
        self.featured = featured
        self.year = date.year
        self.description = description or None
        self.excerpt = excerpt or None

    @property
    def meta_description(self):
        return self.description or self.excerpt or ""

def load_posts():
    """Load all blog posts from the content directory"""
    content_dir = Path('content/posts')

    def _build_signature():
        signature = []
        for md_file in content_dir.glob('*.md'):
            try:
                signature.append((md_file.resolve(), md_file.stat().st_mtime))
            except OSError:
                continue
        return tuple(sorted(signature))

    if not content_dir.exists():
        return []

    signature = _build_signature()
    if (
        signature
        and signature == _POSTS_CACHE["signature"]
        and _POSTS_CACHE["posts"] is not None
    ):
        return _POSTS_CACHE["posts"]

    posts = []

    for md_file in content_dir.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    if not isinstance(frontmatter, dict):
                        raise ValueError("Front matter must be a mapping")

                    post_content = parts[2].strip()

                    date_value = frontmatter.get('date', '2025-01-01')
                    date = _parse_post_date(date_value)

                    views = _parse_views(frontmatter.get('views', 0))
                    description = frontmatter.get('description')
                    if not isinstance(description, str):
                        description = None

                    excerpt = _generate_excerpt(post_content)

                    post = BlogPost(
                        slug=frontmatter.get('slug', md_file.stem),
                        title=frontmatter.get('title', 'Untitled'),
                        date=date,
                        content=post_content,
                        views=views,
                        featured=bool(frontmatter.get('featured', False)),
                        description=description,
                        excerpt=excerpt,
                    )
                    posts.append(post)
        except Exception as e:
            print(f"Error loading {md_file}: {e}")

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x.date, reverse=True)
    _POSTS_CACHE["signature"] = signature
    _POSTS_CACHE["posts"] = posts
    return posts


def _parse_post_date(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            parsed = date_parser.parse(value)
            if parsed.tzinfo:
                parsed = parsed.astimezone(tz=None).replace(tzinfo=None)
            return parsed
        except (ValueError, TypeError):
            pass
    return datetime(2025, 1, 1)


def _parse_views(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _generate_excerpt(markdown_text, length=200):
    if not markdown_text:
        return None

    html = markdown.markdown(markdown_text)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()

    if not text:
        return None

    if len(text) <= length:
        return text

    truncated = text[:length].rstrip()
    return f"{truncated}…"

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

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
