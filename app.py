"""Blog application 
This script generates webpages with flask displaying blog posts, a form to create new posts.
It reads all posts from a JSON file, allows the user to create, delete, update and like posts."""


import json
import os
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


def load_posts():
    """Loads the saved posts from blog_posts.json as a list of dictionaries. 
    each post is a dictionary. It returns the list of dictionaries 
    if the json file exists, otherwise returns an empty list.
    :return: list
    """
    if os.path.exists("blog_posts.json"):
        with open("blog_posts.json", "r", encoding="utf-8") as blog_file:
            return json.load(blog_file)
    else:
        return []


def save_posts(posts):
    """Saves all posts in blog_posts.json.
    :param posts: list of dictionaries, each dictionary containing the information of a post.
    """
    with open ("blog_posts.json", "w", encoding="utf-8") as blog_file:
        json.dump(posts, blog_file, indent=4, ensure_ascii=False)


def fetch_post_by_id(id_num):
    """Fetches the post with the given id.
    :param id_num: integer id_number of a post
    """
    posts = load_posts()
    for post in posts:
        if post["id"] == id_num:
            return post
    return None


@app.route('/')
def index():
    """Home page of the Blog application. 
    This function reads blog posts from a JSON file and renders them on the index page.
    :return: index.html
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Adds a new blog post.
    This function handles the logic for handling new blog posts.
    It renders the form for creating a new post on the add page.
    Also redirects back to the home page after sending the new post.
    :return: redirection to index.html if a new post is sends otherwise add.html
    """
    if request.method == "POST":
        blog_posts = load_posts()
        author = request.form.get("post_author")
        title = request.form.get("post_title")
        content = request.form.get("post_message")

        if blog_posts:
            post_id = len(blog_posts) + 1
        else:
            post_id = 1

        new_post = {
            "id" : post_id,
            "author" : author,
            "title" : title,
            "content" : content,
            "likes" : 0
        }
        blog_posts.append(new_post)

        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """Deletes a current blog posts. 
    This function finds the blog post with the given id and remove it from the list.
    Also redirects back to the home page.
    :param post_id: unique id number of a blog post
    """
    blog_posts = load_posts()

    blog_posts = [post for post in blog_posts if post["id"] != post_id]

    for post in blog_posts:
        if post["id"] > post_id:
            post["id"] -= 1

    save_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update a current blog posts. 
    This function finds the blog post with the given id and update it in the list.
    Also redirects back to the home page.
    :param post_id: unique id number of a blog post
    """
    # Fetch the blog posts from the JSON file
    old_post = fetch_post_by_id(post_id)
    blog_posts = load_posts()
    if old_post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        author = request.form.get("post_author")
        title = request.form.get("post_title")
        content = request.form.get("post_message")

        update_post = {
            "id" : post_id,
            "author" : author,
            "title" : title,
            "content" : content,
            "likes" : old_post["likes"] 
        }

        blog_posts = [update_post if post["id"] == post_id else post for post in blog_posts]

        save_posts(blog_posts)

        return redirect(url_for('index'))
    #it's a GET request
    return render_template('update.html', post=old_post)


@app.route('/likes/<int:post_id>', methods=['POST'])
def likes(post_id):
    """Increase the likes of the post with the given post id.
    Also redirects back to the home page.
    :param post_id: unique id number of a blog post
    """
    like_post = fetch_post_by_id(post_id)
    like_post['likes'] +=1

    blog_posts = load_posts()
    blog_posts = [post if post['id'] != post_id else like_post for post in blog_posts]
    save_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
