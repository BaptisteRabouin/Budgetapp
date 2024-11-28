from flask import render_template, redirect, url_for, flash, request, session, current_app as app
from . import db
from .models import Charge, Revenue
from .forms import ChargeForm, RevenueForm, DeleteForm, LoginForm
from functools import wraps

# Définition du décorateur d'authentification
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            flash('Veuillez saisir le mot de passe pour accéder à cette page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route pour la page d'accueil
@app.route('/')
@login_required
def index():
    charges = Charge.query.all()
    revenues = Revenue.query.all()
    total_charges = sum(charge.amount for charge in charges)
    total_revenues = sum(revenue.amount for revenue in revenues)
    balance = total_revenues - total_charges
    delete_form = DeleteForm()
    return render_template(
        'index.html',
        charges=charges,
        revenues=revenues,
        total_charges=total_charges,
        total_revenues=total_revenues,
        balance=balance,
        delete_form=delete_form
    )

# Route pour ajouter une charge
@app.route('/add_charge', methods=['GET', 'POST'])
@login_required
def add_charge():
    form = ChargeForm()
    if form.validate_on_submit():
        charge = Charge(
            description=form.description.data,
            amount=form.amount.data,
            date=form.date.data
        )
        db.session.add(charge)
        db.session.commit()
        flash('Charge ajoutée avec succès.')
        return redirect(url_for('index'))
    return render_template('add_charge.html', form=form)

# Route pour modifier une charge
@app.route('/edit_charge/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_charge(id):
    charge = Charge.query.get_or_404(id)
    form = ChargeForm(obj=charge)
    if form.validate_on_submit():
        charge.description = form.description.data
        charge.amount = form.amount.data
        charge.date = form.date.data
        db.session.commit()
        flash('Charge mise à jour avec succès.')
        return redirect(url_for('index'))
    return render_template('edit_charge.html', form=form, charge=charge)

# Route pour supprimer une charge
@app.route('/delete_charge/<int:id>', methods=['POST'])
@login_required
def delete_charge(id):
    form = DeleteForm()
    if form.validate_on_submit():
        charge = Charge.query.get_or_404(id)
        db.session.delete(charge)
        db.session.commit()
        flash('Charge supprimée avec succès.')
    else:
        flash('Requête non valide.')
    return redirect(url_for('index'))

# Route pour ajouter un revenu
@app.route('/add_revenue', methods=['GET', 'POST'])
@login_required
def add_revenue():
    form = RevenueForm()
    if form.validate_on_submit():
        revenue = Revenue(
            description=form.description.data,
            amount=form.amount.data,
            date=form.date.data
        )
        db.session.add(revenue)
        db.session.commit()
        flash('Revenu ajouté avec succès.')
        return redirect(url_for('index'))
    return render_template('add_revenue.html', form=form)

# Route pour modifier un revenu
@app.route('/edit_revenue/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_revenue(id):
    revenue = Revenue.query.get_or_404(id)
    form = RevenueForm(obj=revenue)
    if form.validate_on_submit():
        revenue.description = form.description.data
        revenue.amount = form.amount.data
        revenue.date = form.date.data
        db.session.commit()
        flash('Revenu mis à jour avec succès.')
        return redirect(url_for('index'))
    return render_template('edit_revenue.html', form=form, revenue=revenue)

# Route pour supprimer un revenu
@app.route('/delete_revenue/<int:id>', methods=['POST'])
@login_required
def delete_revenue(id):
    form = DeleteForm()
    if form.validate_on_submit():
        revenue = Revenue.query.get_or_404(id)
        db.session.delete(revenue)
        db.session.commit()
        flash('Revenu supprimé avec succès.')
    else:
        flash('Requête non valide.')
    return redirect(url_for('index'))

# Route pour la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == app.config['APP_PASSWORD']:
            session['authenticated'] = True
            flash('Connexion réussie.')
            return redirect(url_for('index'))
        else:
            flash('Mot de passe incorrect.')
    return render_template('login.html', form=form)

# Route pour la déconnexion
@app.route('/logout')
@login_required
def logout():
    session.pop('authenticated', None)
    flash('Vous avez été déconnecté.')
    return redirect(url_for('login'))
