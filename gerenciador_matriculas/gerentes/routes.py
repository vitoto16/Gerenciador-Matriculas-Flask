from flask import render_template, redirect, url_for, flash, request, Blueprint
from gerenciador_matriculas import db, bcrypt
from gerenciador_matriculas.gerentes.forms import FormRegistrar, FormLogin
from gerenciador_matriculas.models import Gerente
from flask_login import login_user, current_user, logout_user

gerentes = Blueprint('gerentes', __name__)


@gerentes.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = FormRegistrar()
    if form.validate_on_submit():
        flash(f"Usuário {form.username.data} criado!", 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        gerente = Gerente(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(gerente)
        db.session.commit()
        return redirect(url_for('gerentes.login'))
    return render_template('registrar.html', form=form, title='Registrar')


@gerentes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = FormLogin()
    if form.validate_on_submit():
        user = Gerente.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login não realizado. Verifique seu nome de usuário e senha.', 'danger')
    return render_template('login.html', form=form, title='Login')


@gerentes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
