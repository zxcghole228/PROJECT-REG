from flask import Flask
from flask import render_template, abort, request
from data import db_session
from forms.user import RegisterForm, LoginForm
from data.user import User
from data.category import Category
from data.type import Type
from data.attarcts import Attractions
from forms.attracts import AttractForm
from flask import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.commentform import CommentForm
from data.comments import Comments
from data.image import Image
import base64
import attracts_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
@app.route('/аttractions')
def аttractions():
    db_sess = db_session.create_session()
    attractions = db_sess.query(Attractions).all()
    context = {'items': attractions}
    return render_template('attractions.html', context=context)


@app.route('/new_attract', methods=['GET', 'POST'])
@login_required
def new_attract():
    db_sess = db_session.create_session()
    choices1 = [(i.id, i.name) for i in db_sess.query(Category).all()]
    choices2 = [(i.id, i.name) for i in db_sess.query(Type).all()]
    form = AttractForm()
    form.categories.choices = choices1
    form.types.choices = choices2
    if form.validate_on_submit():
        attract = Attractions()
        db_sess.add(attract)
        db_sess.commit()
        if attract:
            file = request.files['file']
            if file:
                new_file = Image()
                new_file.name = file.filename
                new_file.data = file.read()
                new_file.attract_id = attract.id
                db_sess.add(new_file)
                db_sess.commit()

            attract.title = form.title.data
            attract.number = form.number.data
            attract.region = form.region.data
            attract.addres = form.addres.data
            attract.categories = form.categories.data
            attract.types = form.types.data
            attract.Unesko = form.unesko.data
            attract.Rare_obj = form.rare_obj.data
            attract.user_id = current_user.id
            db_sess.commit()

        return redirect('/')
    return render_template('new_attract.html',
                           form=form)


@app.route('/аttractions/<int:obj_id>', methods=['GET', 'POST'])
def attraction(obj_id):
    db_sess = db_session.create_session()
    comment_form = CommentForm()
    object = db_sess.query(Attractions).filter(Attractions.id==obj_id).first()
    if not object:
        abort(404)
    if comment_form.validate_on_submit():
        comment = Comments()
        comment.comment = comment_form.comment.data
        comment.user_id = current_user.id
        comment.attract_id = object.id
        db_sess.add(comment)
        db_sess.commit()
    comments = db_sess.query(Comments).filter(Comments.attract_id==obj_id)
    data = db_sess.query(Image).filter(Image.attract_id==obj_id).first()
    if data:
        image = base64.b64encode(data.data).decode('ascii')
    else:
        image = None
    context = {'item': object,
               'comments': comments,
               'image': image}
    return render_template('attract.html', context=context, form=comment_form)


@app.route('/edit_attractions/<int:obj_id>', methods=['GET', 'POST'])
def edit_attract(obj_id):
    db_sess = db_session.create_session()
    choices1 = [(i.id, i.name) for i in db_sess.query(Category).all()]
    choices2 = [(i.id, i.name) for i in db_sess.query(Type).all()]
    form = AttractForm()
    form.categories.choices = choices1
    form.types.choices = choices2
    attract = db_sess.query(Attractions).filter(Attractions.id == obj_id).first()
    image = db_sess.query(Image).filter(Image.attract_id == obj_id).first()
    if request.method == "GET":
        if attract:
            form.title.data = attract.title
            form.number.data = attract.number
            form.region.data = attract.region
            form.addres.data = attract.addres
            form.categories.data = attract.categories
            form.types.data = attract.types
            form.unesko.data = attract.Unesko
            form.rare_obj.data = attract.Rare_obj
        else:
            abort(404)
    if form.validate_on_submit():
        if attract:
            if image:
                db_sess.delete(image)
                db_sess.commit()
            file = request.files['file']
            new_file = Image()
            new_file.name = file.filename
            new_file.data = file.read()
            new_file.attract_id = obj_id
            db_sess.add(new_file)
            db_sess.commit()

            attract.title = form.title.data
            attract.number = form.number.data
            attract.region = form.region.data
            attract.addres = form.addres.data
            attract.categories = form.categories.data
            attract.types = form.types.data
            attract.Unesko = form.unesko.data
            attract.Rare_obj = form.rare_obj.data
            attract.user_id = current_user.id
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit_attract.html', form=form)


@app.route('/delete_attractions/<int:obj_id>', methods=['GET', 'POST'])
@login_required
def news_delete(obj_id):
    db_sess = db_session.create_session()
    attract = db_sess.query(Attractions).filter(Attractions.id == obj_id).first()
    image = db_sess.query(Image).filter(Image.attract_id == obj_id).first()
    if attract:
        db_sess.delete(attract)
        db_sess.commit()
    else:
        abort(404)
    if image:
        db_sess.delete(image)
        db_sess.commit()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/upload_im', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        file = request.files['file']
        new_file = Image()
        new_file.name = file.filename
        new_file.data = file.read()
        new_file.attract_id = 1
        db_sess.add(new_file)
        db_sess.commit()
    return render_template('upload_image.html')

if __name__ == '__main__':
    db_session.global_init("аttractions.db")
    app.register_blueprint(attracts_api.blueprint)
    app.run(port=8080, host='127.0.0.1')