from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# TODO: add CORS

# create flask appliaction
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        res=[]
        for usr in User.query.all():
            res.append({"username":usr.username, "email":usr.email,"id":usr.id})
        return jsonify(res)
    elif request.method == 'POST': #add row
        user_data = request.get_json()
        user = User(username=user_data['username'], email=user_data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id})

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return   {"username":user.username, "email":user.email,"id":user_id}
        # return jsonify(res)
        # return json.dumps(user.__dict__)
    elif request.method == 'PUT':
        user_data = request.get_json()
        user.username = user_data['username']
        user.email = user_data['email']
        db.session.commit()
        return jsonify({'id': user.id})
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'result': 'User deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
