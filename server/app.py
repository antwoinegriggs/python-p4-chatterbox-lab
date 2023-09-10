from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_list = [{"id": message.id, "body": message.body}
                         for message in messages]

        return jsonify(messages_list)

    elif request.method == 'POST':
        data = request.json
        body = data.get('body')
        username = data.get('username')

        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({"id": new_message.id, "body": new_message.body, "username": new_message.username, "created_at": new_message.created_at})


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        data = request.json
        updated_body = data.get('body')

        message = Message.query.get(id)

        message.body = updated_body
        db.session.commit()

        return jsonify({"id": message.id, "body": message.body, "username": message.username, "created_at": message.created_at})

    elif request.method == 'DELETE':
        message = Message.query.get(id)

        db.session.delete(message)
        db.session.commit()

        return jsonify({"message": "Message deleted."})


if __name__ == '__main__':
    app.run(port=5555)
