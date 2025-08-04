"""Blog application """


import json
import os
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


def load_posts():
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r", encoding="utf-8") as blog_file:
            return json.load(blog_file)
    else:
        return []


def save_posts(posts):
    with open ("blog_posts.json", "w", encoding="utf-8") as blog_file:
        json.dump(posts, blog_file, indent=4, ensure_ascii=False)



@app.route('/')
def index():
    """
    Home page of the Blog application. 
    This function reads blog posts from a JSON file and renders them on the index page.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Add a new blog post.
    This function handles the logic for handling new blog posts.
    """
    if request.method == 'POST':
        blog_posts = load_posts()
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.formget("msg")
        if blog_posts:
            post_id = len(blog_posts) + 1
        else:
            post_id = 1

        new_post = {
            "id" : post_id,
            "author" : author,
            "title" : title,
            "content" : content 
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
