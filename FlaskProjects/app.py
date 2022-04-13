from flask import Flask, request, json, jsonify
from mongoengine import connect, Document, StringField, IntField, FloatField

connect(host='mongodb://127.0.0.1:27017/Emp_Details')

app = Flask(__name__)


class Employee(Document):
    name = StringField(required=True)
    age = IntField(required=True)
    sal = FloatField(required=True)


def to_json(self):
    return {"name": self.name,
            "age": self.age,
            "sal": self.sal}


@app.route('/read', methods=['GET'])
def get():
    name = request.args.get('name')
    emp = Employee.objects(name=name).first()
    if not emp:
        return jsonify({'error': 'Employee Details Not Found'})
    else:
        return jsonify(emp.to_json())


@app.route('/create', methods=['POST'])
def create_records():
    record = json.loads(request.data)
    user = Employee(name=record['name'], age=record['age'], sal=record['sal'])
    user.save()
    return jsonify(user.to_json())


@app.route('/update', methods=['PUT'])
def update_records():
    record = json.loads(request.data)
    emp = Employee.objects.filter(name=record['name']).first()
    if not emp:
        return jsonify({'error': 'Employee details not found'})
    else:
        emp.update(age=record['age'], sal=record['sal'])
    return jsonify(emp.to_json())


@app.route('/delete', methods=['DELETE'])
def delete_records():
    record = json.loads(request.data)
    emp = Employee.objects(name=record['name']).first()
    if not emp:
        return jsonify({'error': 'Employee details not found'})
    else:
        emp.delete()
    return jsonify(emp.to_json())


if __name__ == '__main__':
    app.run(debug=True)
