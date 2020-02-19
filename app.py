from preader import create_app, db
from preader.models import File, Package

app = create_app()
context = app.app_context()
context.push()
db.create_all()
context.pop()


if __name__ == "__main__":
    app.run(debug=True)
