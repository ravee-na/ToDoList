from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# set up application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    complete = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

# index route
# set up route with app route decorator
# pass in url string of route ('/')


@app.route('/', methods=['POST', 'GET'])
# define function for that route
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delte(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task'

    else:
        return render_template('index.html', task=task)


@app.route('/complete/<int:id>')
def complete(id):
    task = ToDo.query.get_or_404(id)

    try:
        if task.complete == 0:
            task.complete = 1
            db.session.commit()
            return redirect('/')
        else:
            task.complete = 0
            db.session.commit()
            return redirect('/')
    except:
        return 'There was a problem completing the task'


@app.route('/images/xmark.png')
def get_xmark():
    file_path = './templates/images/xmark.png'

    return send_file(file_path, mimetype='image/png')


@app.route('/images/todo.png')
def get_todolist():
    file_path = './templates/images/todo.png'

    return send_file(file_path, mimetype='image/png')


@app.route('/images/unchecked.png')
def get_unchecked():
    file_path = './templates/images/unchecked.png'

    return send_file(file_path, mimetype='image/png')


@app.route('/images/checked.png')
def get_checked():
    file_path = './templates/images/checked.png'

    return send_file(file_path, mimetype='image/png')


# if there are any errors, show on webpage
if __name__ == "__main__":
    # Create the application context
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Run the development server
    app.run(debug=True)
