from flask import render_template, redirect, url_for, flash, request, session, current_app as app
from . import db
from .models import Charge, Revenue, Person, Budget
from .forms import ChargeForm, RevenueForm, DeleteForm, LoginForm, AllocationForm, PersonForm, BudgetForm, ChangePasswordForm
from functools import wraps

# Définition du décorateur d'authentification
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
           # flash('Veuillez saisir le mot de passe pour accéder à cette page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route pour la page d'accueil
@app.route('/')
@login_required
def index():
    # Récupère le budget actif depuis la session
    active_budget_id = session.get('active_budget_id')
    active_budget = Budget.query.get(active_budget_id) if active_budget_id else None
    if not active_budget_id:
        flash("Veuillez créer puis seléctionner  un budget avant de continuer.", 'info')
        return redirect(url_for('budgets'))

    # Récupère les données liées au budget actif
    charges = Charge.query.filter_by(budget_id=active_budget_id).all()
    revenues = Revenue.query.filter_by(budget_id=active_budget_id).all()

    # Filtrer les personnes ayant au moins un revenu associé
    persons = [
        person for person in Person.query.filter_by(budget_id=active_budget_id).all()
        if any(revenue.person_id == person.id for revenue in revenues)
    ]

    total_charges = sum(charge.amount for charge in charges)
    total_revenues = sum(revenue.amount for revenue in revenues)

    # Calcul du solde
    balance = total_revenues - total_charges

    # Calcul des contributions : salaires avec pourcentage + autres revenus
    contributions = {}
    remains = {}  # Nouveau dictionnaire pour stocker le reste de salaire
    total_contributions = 0  # Somme totale des contributions pour les charges

    for person in persons:
        allocated_revenue = sum(
            revenue.amount for revenue in revenues if revenue.person_id == person.id
        )
        contribution = round((person.allocation_percentage / 100) * allocated_revenue, 2)
        contributions[person.name] = contribution
        remains[person.name] = round(allocated_revenue - contribution, 2)  # Calcul du reste
        total_contributions += contribution

    # Ajouter tous les revenus non associés à une personne dans les contributions
    unallocated_revenues = sum(revenue.amount for revenue in revenues if revenue.person_id is None)
    total_contributions += unallocated_revenues

    # Calcul du montant restant ou excédent
    remaining_to_cover = total_contributions - total_charges  # Positif = excédent, Négatif = montant à couvrir

    delete_form = DeleteForm()
    return render_template(
        'index.html',
        active_budget=active_budget,  # Passe le budget actif au template
        charges=charges,
        revenues=revenues,
        total_charges=total_charges,
        total_revenues=total_revenues,
        balance=balance,
        contributions=contributions,
        remains=remains,  # Passe les restes de salaire au template
        total_contributions=total_contributions,
        remaining_to_cover=remaining_to_cover,
        unallocated_revenues=unallocated_revenues,  # Revenus non alloués
        delete_form=delete_form,
        persons=persons,
    )


# Route pour ajouter une charge
@app.route('/add_charge', methods=['GET', 'POST'])
@login_required
def add_charge():
    # Vérifie s'il existe au moins un budget dans la base
    if Budget.query.count() == 0:
        flash("Aucun budget n'a été créé. Veuillez créer un budget avant d'ajouter une charge.", "info")
        return redirect(url_for('create_budget'))

    form = ChargeForm()
    active_budget_id = session.get('active_budget_id')  # Récupère l'ID du budget actif
    active_budget = Budget.query.get(active_budget_id) if active_budget_id else None
    if not active_budget_id:
        flash("Veuillez créer puis sélectionner  un budget avant d'ajouter une charge.", "info")
        return redirect(url_for('budgets'))

    if form.validate_on_submit():
        try:
            charge = Charge(
                description=form.description.data,
                amount=form.amount.data,
                date=form.date.data,
                budget_id=active_budget_id  # Associe la charge au budget actif
            )
            db.session.add(charge)
            db.session.commit()
            flash('Charge ajoutée avec succès.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout de la charge : {str(e)}", "error")

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
        flash('Charge mise à jour avec succès.', 'success')
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
        flash('Charge supprimée avec succès.', 'success')
    else:
        flash('Requête non valide.', 'error')
    return redirect(url_for('index'))

# Route pour ajouter un revenu
@app.route('/add_revenue', methods=['GET', 'POST'])
@login_required
def add_revenue():
    # Vérifie s'il existe au moins un budget dans la base
    if Budget.query.count() == 0:
        flash("Aucun budget n'a été créé. Veuillez créer un budget avant d'ajouter un revenu.", "info")
        return redirect(url_for('create_budget'))

    active_budget_id = session.get('active_budget_id')  # Récupère l'ID du budget actif
    active_budget = Budget.query.get(active_budget_id) if active_budget_id else None
    if not active_budget_id:
        flash("Veuillez créer puis sélectionner  un budget avant d'ajouter un revenu.", 'info')
        return redirect(url_for('budgets'))

    # Récupère les personnes liées au budget actif
    persons = Person.query.filter_by(budget_id=active_budget_id).all()

    form = RevenueForm()
    form.person_id.choices = [(0, 'Aucune')] + [(person.id, person.name) for person in persons]

    if form.validate_on_submit():
        try:
            # Si "Aucune" est sélectionné, assigne None à person_id
            person_id = form.person_id.data if form.person_id.data != 0 else None
            revenue = Revenue(
                description=form.description.data,
                amount=form.amount.data,
                date=form.date.data,
                person_id=person_id,
                budget_id=active_budget_id  # Associe au budget actif
            )
            db.session.add(revenue)
            db.session.commit()
            flash('Revenu ajouté avec succès.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout du revenu : {str(e)}", "error")

    return render_template('add_revenue.html', form=form)

# Route pour modifier un revenu
@app.route('/edit_revenue/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_revenue(id):
    revenue = Revenue.query.get_or_404(id)
    form = RevenueForm(obj=revenue)
    form.person_id.choices = [(person.id, person.name) for person in Person.query.all()]
    if form.validate_on_submit():
        revenue.description = form.description.data
        revenue.amount = form.amount.data
        revenue.date = form.date.data
        revenue.person_id = form.person_id.data
        db.session.commit()
        flash('Revenu mis à jour avec succès.', 'success')
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
        flash('Revenu supprimé avec succès.', 'success')
    else:
        flash('Requête non valide.', 'error')
    return redirect(url_for('index'))

# Route pour gérer les allocations
@app.route('/manage_allocations', methods=['GET', 'POST'])
@login_required
def manage_allocations():
    form = AllocationForm()
    form.person_id.choices = [(person.id, person.name) for person in Person.query.all()]
    if form.validate_on_submit():
        person = Person.query.get(form.person_id.data)
        if person:
            person.allocation_percentage = form.allocation_percentage.data
            db.session.commit()
            flash(f"Allocation de {person.name} mise à jour avec succès.", 'success')
        return redirect(url_for('index'))
    return render_template('manage_allocations.html', form=form)

# Route pour la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == app.config['APP_PASSWORD']:
            session['authenticated'] = True
            flash('Connexion réussie.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Mot de passe incorrect.', 'error')
    return render_template('login.html', form=form)

# Route pour la déconnexion
@app.route('/logout')
@login_required
def logout():
    session.pop('authenticated', None)
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('login'))


@app.route('/add_person', methods=['GET', 'POST'])
@login_required
def add_person():
    form = PersonForm()
    active_budget_id = session.get('active_budget_id')
    if not active_budget_id:
        flash("Veuillez créer puis sélectionner un budget avant d'ajouter une personne.", 'error')
        return redirect(url_for('budgets'))

    if form.validate_on_submit():
        person = Person(
            name=form.name.data,
            allocation_percentage=form.allocation_percentage.data,
            budget_id=active_budget_id  # Associe au budget actif
        )
        db.session.add(person)
        db.session.commit()
        flash(f"Personne {person.name} ajoutée avec succès.", 'success')
        return redirect(url_for('index'))
    return render_template('add_person.html', form=form)

# SUpprimer une personne
@app.route('/delete_person/<int:person_id>', methods=['POST'])
@login_required
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    if not person.can_be_deleted():
        flash(f"La personne {person.name} ne peut pas être supprimée car elle a des revenus associés.", "error")
        return redirect(url_for('manage_persons'))

    db.session.delete(person)
    db.session.commit()
    flash(f"La personne {person.name} a été supprimée avec succès.", 'success')
    return redirect(url_for('manage_persons'))


# Update allocation
@app.route('/update_allocation/<int:person_id>', methods=['POST'])
@login_required
def update_allocation(person_id):
    person = Person.query.get_or_404(person_id)
    allocation_percentage = request.form.get('allocation_percentage')
    try:
        person.allocation_percentage = float(allocation_percentage)
        db.session.commit()
        flash(f"Allocation de {person.name} mise à jour avec succès.", 'success')
    except ValueError:
        flash("Le pourcentage doit être un nombre valide.", "error")
    return redirect(url_for('index'))


@app.route('/create_budget', methods=['GET', 'POST'])
@login_required
def create_budget():
    form = BudgetForm()
    if form.validate_on_submit():
        try:
            budget = Budget(name=form.name.data)
            db.session.add(budget)
            db.session.commit()
            flash(f"Budget '{budget.name}' créé avec succès.", 'success')
            return redirect(url_for('budgets'))  # Redirige vers la liste des budgets
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la création du budget : {str(e)}", "error")
    return render_template('create_budget.html', form=form)


@app.route('/budgets', methods=['GET'])
@login_required
def budgets():
    budgets = Budget.query.order_by(Budget.created_at.desc()).all()
    delete_form = DeleteForm()  # Crée une instance de DeleteForm

     # Récupère le budget actif depuis la session
    active_budget_id = session.get('active_budget_id')
    active_budget = Budget.query.get(active_budget_id) if active_budget_id else None

    return render_template(
    	'budgets.html',
	budgets=budgets,
	delete_form=delete_form,
	active_budget=active_budget
    )



# Route pour afficher un budget spécifique
@app.route('/view_budget/<int:budget_id>')
@login_required
def view_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)  # Récupère le budget ou renvoie une 404
    charges = Charge.query.filter_by(budget_id=budget_id).all()  # Charges liées au budget
    revenues = Revenue.query.filter_by(budget_id=budget_id).all()  # Revenus liés au budget
    persons = Person.query.filter_by(budget_id=budget_id).all()  # Personnes liées au budget

    # Calculs
    total_charges = sum(charge.amount for charge in charges)
    total_revenues = sum(revenue.amount for revenue in revenues)
    balance = total_revenues - total_charges

    # Préparer la vue
    return render_template(
        'view_budget.html',
        budget=budget,
        charges=charges,
        revenues=revenues,
        persons=persons,
        total_charges=total_charges,
        total_revenues=total_revenues,
        balance=balance
    )

# Route pour le budget actif
@app.route('/select_budget/<int:budget_id>', methods=['GET'])
@login_required
def select_budget(budget_id):
    # Vérifie si le budget existe
    budget = Budget.query.get(budget_id)
    if not budget:
        flash("Le budget sélectionné n'existe pas.", "error")
        return redirect(url_for('budgets'))
    
    # Définit le budget actif dans la session
    session['active_budget_id'] = budget_id
    #flash(f"Le budget '{budget.name}' est maintenant actif.", 'info')
    
    # Redirige vers la page d'accueil
    return redirect(url_for('index'))


# Route pour modifier un budget
@app.route('/edit_budget/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)  # Récupère le budget ou lève une erreur 404
    form = BudgetForm(obj=budget)  # Pré-remplit le formulaire avec les données du budget

    if form.validate_on_submit():
        try:
            budget.name = form.name.data  # Met à jour le nom du budget
            db.session.commit()  # Enregistre les modifications
            flash(f"Budget '{budget.name}' modifié avec succès.", 'success')
            return redirect(url_for('budgets'))  # Redirige vers la liste des budgets
        except Exception as e:
            db.session.rollback()  # Annule les changements en cas d'erreur
            flash(f"Erreur lors de la modification du budget : {str(e)}", "error")

    return render_template('edit_budget.html', form=form, budget=budget)


# Route pour supprimer un budget
@app.route('/delete_budget/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    
    # Vérifie si le budget est actif avant de le supprimer
    if session.get('active_budget_id') == budget_id:
        session.pop('active_budget_id', None)  # Supprime le budget actif de la session

    # Supprime toutes les charges et revenus associés au budget
    Charge.query.filter_by(budget_id=budget_id).delete()
    Revenue.query.filter_by(budget_id=budget_id).delete()
    Person.query.filter_by(budget_id=budget_id).delete()

    # Supprime le budget lui-même
    db.session.delete(budget)
    db.session.commit()
    flash(f"Le budget '{budget.name}' a été supprimé avec succès.", "success")
    return redirect(url_for('budgets'))


# Route pour copier un budget
@app.route('/copy_budget/<int:budget_id>', methods=['POST'])
@login_required
def copy_budget(budget_id):
    original_budget = Budget.query.get_or_404(budget_id)

    try:
        # Étape 1 : Créer un nouveau budget
        copied_budget = Budget(name=f"{original_budget.name} (Copie)")
        db.session.add(copied_budget)
        db.session.commit()  # Commit pour obtenir l'ID du nouveau budget

        # Dictionnaire pour mapper les personnes copiées
        person_mapping = {}

        # Étape 2 : Copier les personnes
        for person in original_budget.persons:
            new_person = Person(
                name=person.name,
                allocation_percentage=person.allocation_percentage,
                budget_id=copied_budget.id
            )
            db.session.add(new_person)
            db.session.flush()  # Récupère l'ID de la nouvelle personne
            person_mapping[person.id] = new_person.id  # Map l'ancien ID vers le nouveau

        # Étape 3 : Copier les revenus
        for revenue in original_budget.revenues:
            new_revenue = Revenue(
                description=revenue.description,
                amount=revenue.amount,
                date=revenue.date,
                person_id=person_mapping.get(revenue.person_id),  # Map vers la nouvelle personne
                budget_id=copied_budget.id
            )
            db.session.add(new_revenue)

        # Étape 4 : Copier les charges
        for charge in original_budget.charges:
            new_charge = Charge(
                description=charge.description,
                amount=charge.amount,
                date=charge.date,
                budget_id=copied_budget.id
            )
            db.session.add(new_charge)

        db.session.commit()
        flash(f"Le budget '{original_budget.name}' a été copié avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la copie du budget : {str(e)}", "error")

    return redirect(url_for('budgets'))



# Route pour changer le mot de passe
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Vérification de l'ancien mot de passe
        if form.old_password.data != app.config['APP_PASSWORD']:
            flash("L'ancien mot de passe est incorrect.", "error")
            return redirect(url_for('change_password'))

        # Mettre à jour le mot de passe dans la configuration
        app.config['APP_PASSWORD'] = form.new_password.data
        flash("Le mot de passe a été modifié avec succès.", "success")
        return redirect(url_for('index'))

    return render_template('change_password.html', form=form)


# Route pour gérer les personnes
@app.route('/manage_persons', methods=['GET'])
@login_required
def manage_persons():
    active_budget_id = session.get('active_budget_id')
    active_budget = Budget.query.get(active_budget_id) if active_budget_id else None
    if not active_budget_id:
        flash("Veuillez créer puis sélectionner un budget avant de gérer les personnes.", "info")
        return redirect(url_for('budgets'))

    # Récupère les personnes liées au budget actif
    persons = Person.query.filter_by(budget_id=active_budget_id).all()
    delete_form = DeleteForm()  # Crée une instance de formulaire de suppression
    return render_template('manage_persons.html', persons=persons, active_budget=active_budget, delete_form=delete_form)
