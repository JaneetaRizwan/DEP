from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('items', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id
        }

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    user_id = get_jwt_identity()
    
    new_item = Item(name=name, description=description, user_id=user_id)
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({'message': 'Item created successfully'}), 201

@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    user_id = get_jwt_identity()
    items = Item.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in items]), 200

@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get_or_404(item_id)
    if item.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()

    return jsonify({'message': 'Item updated successfully'}), 200

@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)
