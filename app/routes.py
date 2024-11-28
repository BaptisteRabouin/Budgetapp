from flask import render_template, redirect, url_for, flash, request
from . import db
from .models import Charge, Revenue
from .forms import ChargeForm, RevenueForm, DeleteForm
from datetime import datetime
from flask import current_app as app

@app.route('/')
def index():
    charges = Charge.query.all()
    revenues = Revenue.query.all()
    total_charges = sum(charge.amount for charge in charges)
    total_revenues = sum(revenue.amount for revenue in revenues)
    balance = total_revenues - total_charges
    delete_form = DeleteForm()
    return render_template('index.html', charges=charges, revenues=revenues, balance=balance, delete_form=delete_form)

@app.route('/add_charge', methods=['GET', 'POST'])
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

@app.route('/edit_charge/<int:id>', methods=['GET', 'POST'])
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

@app.route('/delete_charge/<int:id>', methods=['POST'])
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

@app.route('/add_revenue', methods=['GET', 'POST'])
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

@app.route('/edit_revenue/<int:id>', methods=['GET', 'POST'])
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

@app.route('/delete_revenue/<int:id>', methods=['POST'])
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
