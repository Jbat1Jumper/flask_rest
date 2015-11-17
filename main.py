#!/usr/bin/env python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})




class Attribute(object):
    def __init__(self, required=True, default=None, validator=None, v=None):
        self.required = required
        self.default = default
        self.validator = validator or v


class Method(object):
    def __init__(self):
        pass


class Book(object):
    def __init__(self):
        self.name = ""
        self.author = ""
        self.amount = 0
    
    # Si no tiene un parametro rest no se puede rest'erizar
    def rest(self):
        return {
            'name': Attribute(required=True,
                              v=lambda x: x is unicode and x),
            'author': Attribute(required=False, default='Unknown',
                                v=lambda x: x is unicode and x),
            'amount': Attribute(required=False, default=0,
                                v=lambda x: x is int and x >= 0)
        }

    # Este metodo es opcional y se genera automaticamente
    def load(self, json):
        self.name = json.name
        self.author = json.author
        self.amount = json.amount 

    # Este metodo es opcional y se genera automaticamente
    def save(self):
        # Aca se puede modificar algo de las variables
        return {
            'name': self.name,
            'author': self.author,
            'amount': self.amount
        }


Something.generateRest('/books', key='name')


if __name__ == '__main__':
    app.run(debug=True)
