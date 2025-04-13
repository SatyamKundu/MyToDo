from flask import Flask, render_template, request
from flask import redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form.get('title')  # ✅ Use .get() to avoid KeyError
        desc = request.form.get('desc')

        if title and desc:  # ✅ Validate input to avoid empty entries
            todo = Todo(title=title, desc=desc)  # ✅ Use actual values
            db.session.add(todo)
            db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is the product page"
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        title = request.form.get('title')  
        desc = request.form.get('desc')

        if title and desc:
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect("/")

    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('hello_world'))  

if __name__ == "__main__":
    with app.app_context():  # ✅ Ensure this runs within context
        db.create_all()
        print("Database created successfully!")  # ✅ Debugging log
    app.run(debug=True, port=8000)
