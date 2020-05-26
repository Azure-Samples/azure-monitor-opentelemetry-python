import json
import requests

from flask import flash, make_response, redirect, render_template, request, url_for

from app import app, db
from app.forms import ToDoForm
from app.metric import entries_counter, testing_labels
from app.models import Todo

# Hitting any endpoint will track an incoming request (requests)

@app.route('/')
@app.route('/error')
def index():
    form = ToDoForm()
    # Queries to the data base will track an outgoing request (dependencies)
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    path = request.url_rule
    if path and 'error' in path.rule:
        flash('ERROR: String must be less than 11 characters.')
    return render_template(
        'index.html',
        title='Home',
        form=form,
        complete=complete,
        incomplete=incomplete
    )


@app.route('/save', methods=['POST'])
def save():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    incomplete.extend(complete)
    url = "http://localhost:5001/api/save"
    entries = ["Id: " + str(entry.id) + " Task: " + entry.text + " Complete: " + str(entry.complete) \
        for entry in incomplete]
    response = requests.post(url=url, data=json.dumps(entries))
    if response.ok:
        flash("Todo saved to file.")
    else:
        flash("Exception occurred while saving")
    return redirect('/')


@app.route('/add', methods=['POST'])
def add():
    add_input = request.form['add_input']
    # Fail if string greater than 10 characters
    try:
        if len(add_input) > 10:
            raise Exception
        todo = Todo(text=add_input, complete=False)
        db.session.add(todo)
        db.session.commit()
        # Records a counter metric to be sent as telemetry
        entries_counter.add(1, testing_labels)
    except Exception:
        return redirect('/error')
    return redirect('/')


@app.route('/complete/<id>', methods=['POST'])
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect('/')
