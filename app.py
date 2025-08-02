"""Blog application """


import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    """
    Home page of the Blog application. 
    This function reads blog posts from a JSON file and renders them on the index page.
    """
    with open("blog_posts.json", "r", encoding="utf-8") as blog_file:
        blog_posts = json.load(blog_file)
    return render_template('index.html', posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
