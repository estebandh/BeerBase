import os
from flask import Flask, session, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# define database tables
class Style(db.Model):
    __tablename__ = 'styles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    beers = db.relationship('Beer', backref='style', cascade="delete")


class Beer(db.Model):
    __tablename__ = 'beers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    hops = db.Column(db.Text)
    brewery = db.Column(db.Text)
    style_id = db.Column(db.Integer, db.ForeignKey('styles.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/styles')
def show_all_styles():
    styles = Style.query.all()
    return render_template('styles-all.html', styles=styles)


@app.route('/style/add', methods=['GET', 'POST'])
def add_styles():
    if request.method == 'GET':
        return render_template('styles-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        about = request.form['about']

        # insert the data into the database
        style = Style(name=name, about=about)
        db.session.add(style)
        db.session.commit()
        return redirect(url_for('show_all_styles'))


@app.route('/api/style/add', methods=['POST'])
def add_ajax_styles():
    # get data from the form
    name = request.form['name']
    about = request.form['about']

    # insert the data into the database
    style = Style(name=name, about=about)
    db.session.add(style)
    db.session.commit()
    # flash message type: success, info, warning, and danger from bootstrap
    flash('Style Inserted', 'success')
    return jsonify({"id": str(style.id), "name": style.name})


@app.route('/style/edit/<int:id>', methods=['GET', 'POST'])
def edit_style(id):
    style = Style.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('style-edit.html', style=style)
    if request.method == 'POST':
        # update data based on the form data
        style.name = request.form['name']
        style.about = request.form['about']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_styles'))


@app.route('/style/delete/<int:id>', methods=['GET', 'POST'])
def delete_style(id):
    style = Style.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('styles-delete.html', style=style)
    if request.method == 'POST':
        # delete the style by id
        # all related beers are deleted as well
        db.session.delete(style)
        db.session.commit()
        return redirect(url_for('show_all_styles'))


@app.route('/api/style/<int:id>', methods=['DELETE'])
def delete_ajax_style(id):
    style = Style.query.get_or_404(id)
    db.session.delete(style)
    db.session.commit()
    return jsonify({"id": str(style.id), "name": style.name})


# beer-all.html adds beer id to the edit button using a hidden input
@app.route('/beers')
def show_all_beers():
    beers = Beer.query.all()
    return render_template('beer-all.html', beers=beers)


@app.route('/beer/add', methods=['GET', 'POST'])
def add_beers():
    if request.method == 'GET':
        styles = Style.query.all()
        return render_template('beer-add.html', styles=styles)
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        hops = request.form['hops']
        brewery = request.form['brewery']
        style_name = request.form['style']
        style = Style.query.filter_by(name=style_name).first()
        beer = Beer(name=name, hops=hops, brewery=brewery, style=style)

        # insert the data into the database
        db.session.add(beer)
        db.session.commit()
        return redirect(url_for('show_all_beers'))


@app.route('/beer/edit/<int:id>', methods=['GET', 'POST'])
def edit_beer(id):
    beer = Beer.query.filter_by(id=id).first()
    styles = Style.query.all()
    if request.method == 'GET':
        return render_template('beer-edit.html', beer=beer, styles=styles)
    if request.method == 'POST':
        # update data based on the form data
        beer.name = request.form['name']
        beer.hops = request.form['hops']
        beer.brewery = request.form['brewery']
        style_name = request.form['style']
        style = Style.query.filter_by(name=style_name).first()
        beer.style = style
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_beers'))


@app.route('/beer/delete/<int:id>', methods=['GET', 'POST'])
def delete_beer(id):
    beer = Beer.query.filter_by(id=id).first()
    styles = Style.query.all()
    if request.method == 'GET':
        return render_template('beer-delete.html', beer=beer, styles=styles)
    if request.method == 'POST':
        # use the id to delete the beer
        # beer.query.filter_by(id=id).delete()
        db.session.delete(beer)
        db.session.commit()
        return redirect(url_for('show_all_beers'))


@app.route('/api/beer/<int:id>', methods=['DELETE'])
def delete_ajax_beer(id):
    beer = Beer.query.get_or_404(id)
    db.session.delete(beer)
    db.session.commit()
    return jsonify({"id": str(beer.id), "name": beer.name})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def show_all_users():
    return render_template('user-all.html')


@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    # how to get form data is different for GET vs. POST
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        # return render_template('form-demo.html', first_name=first_name)
        return redirect(url_for('form_demo'))


@app.route('/user/<string:name>/')
def get_user_name(name):
    # return "hello " + name
    # return "Hello %s, this is %s" % (name, 'administrator')
    return render_template('user.html', name=name)


@app.route('/beer/<int:id>/')
def get_beer_id(id):
    # return "This beers's ID is " + str(id)
    return "Hi, this is %s and the beer's id is %d" % ('administrator', id)


# https://goo.gl/Pc39w8 explains the following line
if __name__ == '__main__':

    # activates the debugger and the reloader during development
    # app.run(debug=True)
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)
