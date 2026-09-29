from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_no = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    field = db.Column(db.String(200), nullable=False)
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(20), default = "pending")
    