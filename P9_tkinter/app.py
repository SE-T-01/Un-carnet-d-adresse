from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from email.message import EmailMessage
import subprocess
import sys

app = Flask(__name__)
app.secret_key = "cle_secrete_medicale"

# Connexion à la base SQLite
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Page d'accueil : Liste & Recherche
@app.route('/')
def index():
    conn = get_db_connection()
    search_query = request.args.get('search', '')
    if search_query:
        cur = conn.execute(
            "SELECT * FROM contacts WHERE nom LIKE ? OR prenom LIKE ? OR categorie LIKE ?", 
            (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
        )
    else:
        cur = conn.execute('SELECT * FROM contacts')
    contacts = cur.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts, search=search_query)

# Ajouter un contact
@app.route('/ajouter', methods=('GET', 'POST'))
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom'].strip()
        prenom = request.form['prenom'].strip()
        telephone = request.form['telephone'].strip()
        email = request.form['email'].strip()
        categorie = request.form['categorie']
        adresse = request.form['adresse'].strip()
        fonction = request.form['fonction'].strip()
        entreprise = request.form['entreprise'].strip()

        # Condition : Exactement 10 chiffres
        if not (telephone.isdigit() and len(telephone) == 10):
            flash('Erreur : Le numéro doit contenir exactement 10 chiffres.', 'danger')
            return render_template('ajouter.html')

        # Condition : Éviter les doublons
        conn = get_db_connection()
        doublon = conn.execute('SELECT id FROM contacts WHERE telephone = ? OR email = ?', (telephone, email)).fetchone()
        if doublon:
            conn.close()
            flash('Erreur : Ce numéro ou cet email existe déjà.', 'danger')
            return render_template('ajouter.html')

        conn.execute(
            'INSERT INTO contacts (nom, prenom, telephone, email, categorie, adresse, fonction, entreprise) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (nom, prenom, telephone, email, categorie, adresse, fonction, entreprise)
        )
        conn.commit()
        conn.close()
        flash('Contact enregistré avec succès !', 'success')
        return redirect(url_for('index'))
        
    return render_template('ajouter.html')

# Modifier un contact
@app.route('/modifier/<int:id>', methods=('GET', 'POST'))
def modifier(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nom = request.form['nom'].strip()
        prenom = request.form['prenom'].strip()
        telephone = request.form['telephone'].strip()
        email = request.form['email'].strip()
        categorie = request.form['categorie']
        adresse = request.form['adresse'].strip()
        fonction = request.form['fonction'].strip()
        entreprise = request.form['entreprise'].strip()

        # Condition : Exactement 10 chiffres
        if not (telephone.isdigit() and len(telephone) == 10):
            flash('Erreur : Le numéro doit contenir exactement 10 chiffres.', 'danger')
            return render_template('modifier.html', contact=contact)

        # Condition : Éviter les doublons (exclure le contact actuel)
        doublon = conn.execute(
            'SELECT id FROM contacts WHERE (telephone = ? OR email = ?) AND id != ?', 
            (telephone, email, id)
        ).fetchone()

        if doublon:
            flash('Erreur : Un autre contact possède déjà ce numéro ou cet email.', 'danger')
            return render_template('modifier.html', contact=contact)

        conn.execute(
            'UPDATE contacts SET nom=?, prenom=?, telephone=?, email=?, categorie=?, adresse=?, fonction=?, entreprise=? WHERE id=?',
            (nom, prenom, telephone, email, categorie, adresse, fonction, entreprise, id)
        )
        conn.commit()
        conn.close()
        flash('Contact modifié avec succès !', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('modifier.html', contact=contact)

# Module d'envoi d'email
@app.route('/email/<int:id>', methods=('GET', 'POST'))
def envoyer_email(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()
    conn.close()

    if request.method == 'POST':
        sujet = request.form['sujet']
        contenu = request.form['message']
        try:
            msg = EmailMessage()
            msg.set_content(contenu)
            msg['Subject'] = sujet
            msg['From'] = "votre_email@gmail.com"
            msg['To'] = contact['email']
            
            flash(f"Message préparé avec succès pour {contact['email']} !", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Erreur lors de la préparation de l'email : {str(e)}", "danger")

    return render_template('email.html', contact=contact)

# Supprimer un contact
@app.route('/supprimer/<int:id>', methods=('POST',))
def supprimer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Contact supprimé !', 'success')
    return redirect(url_for('index'))

@app.route('/ouvrir_agenda')
def ouvrir_agenda():
    try:
        # Lance le script de l'agenda Tkinter en arrière-plan
        subprocess.Popen(["python", "agenda.py"])
        flash("L'agenda Tkinter a été ouvert avec succès !", "success")
    except Exception as e:
        flash(f"Erreur lors de l'ouverture de l'agenda : {str(e)}", "danger")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
