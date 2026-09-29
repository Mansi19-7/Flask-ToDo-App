from app import createApp, db
from app.models import Task, User
from sqlalchemy import inspect

app = createApp()

with app.app_context():
    db.create_all()

    print("Database:", db.engine.url)
    print("Tables:", inspect(db.engine).get_table_names())

if __name__ == '__main__':
    app.run(debug=True)