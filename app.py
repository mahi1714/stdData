from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aa3348fdc60e49779a658d43e231a527'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable= False)
    made = db.Column(db.String(50), nullable= False)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/home', methods=["GET", "POST"])
@app.route('/')
def home():
    if request.method == 0:
        print("please put information")
    
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        made = request.form['made']
        todo = Todo(title=title, price=price, made=made)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def showData():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is product page'
    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
# def delete(sno):
#     todo = Todo.query.get_or_404(sno)

#     try:
#         db.session.delete(todo)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that element'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        made = request.form['made']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.price = price
        todo.made = made
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
if __name__ == "__main__":
    app.run(debug=True, port=5000)



