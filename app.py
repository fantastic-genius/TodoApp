from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hamzah:password@localhost:5432/todoapp'
db = SQLAlchemy(app)


migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo id: {self.id},  description: {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    db.relationship('Todo', backref='list', lazy=True, cascade='all, delete-orphan')

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}

    try:
        description =  request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({'success': True})

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
        active_list=TodoList.query.get(list_id),
        lists=TodoList.query.all()
    )

@app.route('/lists', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todoList = TodoList(name=name)
        db.session.add(todoList)
        db.session.commit()
        body['name'] = todoList.name
        body['id'] = todoList.id
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    
    if(error):
        abort(500)
    else:
        return jsonify(body)

@app.route('/lists/<list_id>/set-completed', methods=['POST'])
def complete_list(list_id):
    try:
        completed = request.get_json()['completed']
        todoList = TodoList.query.get(list_id)
        todoList.completed = completed
        todos = Todo.query.filter_by(list_id=list_id).all()
        todosArr = []
        for todo in todos:
            todo.completed = completed
            todosArr.append(todo)
        
        db.session.add(todoList)
        db.session.add_all(todosArr)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('get_list_todos', list_id=list_id))

@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    try:
        todoList = TodoList.query.get(list_id)
        db.session.delete(todoList)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify({'success': True})

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))
