#Assignment 11

from flask import Flask, redirect, url_for, request, render_template
import pickle

app = Flask(__name__)

todo_list = []
next_item_id = 1

def load_todos():
    global todo_list
    try:
        with open('todo.pickle', 'rb') as f:
            todo_list = pickle.load(f)
    except FileNotFoundError:
        todo_list = []

def save_todos():
    with open('todo.pickle', 'wb') as f:
        pickle.dump(todo_list, f)

@app.route('/')
def index():
    load_todos()
    return render_template('index.html', todo_list=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    global next_item_id
    task = request.form.get('task')
    email = request.form.get('email')
    priority = request.form.get('priority')

    if '@' not in email:
        return redirect(url_for('index'))

    if priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('index'))

    todo_list.append({'id': next_item_id, 'task': task, 'email': email, 'priority':priority})
    next_item_id += 1

    save_todos()
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    global todo_list
    todo_list = []
    save_todos()
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    save_todos()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    global todo_list
    todo_list = [item for item in todo_list if item['id'] != item_id]
    save_todos()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)