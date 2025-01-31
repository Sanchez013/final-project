from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)

@app.route('/add', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        platform = request.form['platform']
        description = request.form['description']
        new_game = Game(title=title, genre=genre, platform=platform, description=description)
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_game.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    game = Game.query.get_or_404(id)
    if request.method == 'POST':
        game.title = request.form['title']
        game.genre = request.form['genre']
        game.platform = request.form['platform']
        game.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_game.html', game=game)

@app.route('/delete/<int:id>')
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
