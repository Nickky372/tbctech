from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Post, ContactMessage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        new_user = User(username=username, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'There was an issue adding your account.'

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect(url_for('home'))
        else:
            return 'Login failed. Please check your username and password.'

    return render_template('login.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = Post(title=title, content=content, author='Anonymous')

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'There was an issue adding your post.'

    return render_template('POST.html')

@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        new_message = ContactMessage(name=name, email=email, subject=subject, message=message)

        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'There was an issue submitting your message.'

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
