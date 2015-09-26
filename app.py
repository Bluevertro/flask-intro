# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'
app.database = 'sample.db'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    #print cur
    #print cur.fetchall()
    #DATA = cur.fetchall() #[(u'Well', u"I'm well."), (u'Good', u"I'm good.")]

    # list comp

    #posts_list_comp = [dict(title=row[0], description=row[1]) for row in DATA]

    #print "\nlist comp:\n{}\n".format(posts_list_comp)

    # for loop

    posts_dict = {}
    posts = []
    cur.fetchall()
    for item in cur.fetchall():
        posts_dict['title'] = item[0]
        posts_dict['description'] = item[1]
        posts.append(posts_dict)
        posts_dict = {}

    print "\nfor loop:\n{}\n".format(posts)
    g.db.close()
    return render_template('index.html', posts=posts)  # render a template

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

# connect to database
def connect_db():
    return sqlite3.connect(app.database)


@app.route('/overwrite')
def overwrite_db():
    with sqlite3.connect("sample.db") as connection:
        c = connection.cursor()
        c.execute("DROP TABLE posts")
        c.execute("CREATE TABLE posts(title TEXT, description TEXT)")
        c.execute('INSERT INTO posts VALUES ("Good", "I\'m good.")')
        c.execute('INSERT INTO posts VALUES ("Well", "I\'m well.")')
        c.execute('INSERT INTO posts VALUES ("Hello from the shell", "Hello")')
    return redirect(url_for('welcome'))

@app.route('/test')
def post_things():
    DATA = [(u'Well', u"I'm well."), (u'Good', u"I'm good.")]

    # list comp

    posts_list_comp = [dict(title=row[0], description=row[1]) for row in DATA]

    print "\nlist comp:\n{}\n".format(posts_list_comp)

    # for loop

    posts_dict = {}
    posts = []

    for item in DATA:
        posts_dict['title'] = item[0]
        posts_dict['description'] = item[1]
        posts.append(posts_dict)
        posts_dict = {}

    print "\nfor loop:\n{}\n".format(posts)
    return render_template('index.html', posts=posts)  # render a template
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)