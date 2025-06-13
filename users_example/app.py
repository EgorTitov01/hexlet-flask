from flask import Flask, redirect, render_template, request, url_for, flash, get_flashed_messages
from users_example.validator import validate
import psycopg2
from users_example.repository import UserRepository


template_dir = '../templates'
app = Flask(__name__, template_folder=template_dir)
app.secret_key = "SECRET KEY"
conn = psycopg2.connect(
        dbname="hexlet", user="egor-t", host="localhost", password='qwerty'
    )
repo = UserRepository(conn)


@app.route('/users/new/')
def users_new():
    user = {}
    errors = []
    return render_template('users/new.html', user=user, errors=errors)

@app.post("/users/")
def users_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template('users/new.html', user=user, errors=errors), 422

    repo._create(user)
    flash("User added", "success")
    return redirect(url_for('users_index'), 302)

@app.route('/users/<id>')
def users_show(id):
    user = repo.find(id)
    if user:
        messages = get_flashed_messages(with_categories=True)
        return render_template('users/show.html', user=user, messages=messages)
    else:
        return 'No such user', 404

@app.route('/users/')
def users_index():
    query = request.args.get('query', '')
    if query:
        users = repo.get_by_term(query)
    else:
        users = repo.get_content()
    messages = get_flashed_messages(with_categories=True)
    return render_template('users/index.html', users=users,
                           search=query, messages=messages)

@app.route('/users/<id>/edit')
def users_edit(id):
    user = repo.find(id)
    if user:
        errors = []
        return render_template('users/edit.html', user=user, errors=errors)
    else:
        return 'User not found', 404

@app.route('/users/<id>/patch', methods=['POST'])
def users_patch(id):
    user = repo.find(id)
    if not user:
        return 'User not found', 404

    new_data = request.form.to_dict()
    errors = validate(new_data)
    if errors:
        return render_template('users/edit.html', errors=errors, user=user)

    user['email'] = new_data['email']
    repo._update(user)
    flash('User info updated')

    return redirect(url_for('users_show', id=id))

@app.post('/users/<id>/delete')
def users_delete(id):
    user = repo.find(id)
    if user:
        repo._delete(id)

    return redirect(url_for('users_index'))




