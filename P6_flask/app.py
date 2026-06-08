from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "votre_cle_secrete_ici"

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

# Affichage et Recherche de contacts
@app.route('/')
def index():
    conn = get_db_connection()
    search_query = request.args.get('search', '')
    
    if search_query:
        # Recherche par nom ou prénom
        cur = conn.execute("""
            SELECT * FROM contacts 
            WHERE nom LIKE ? OR prenom LIKE ?
        """, (f'%{search_query}%', f'%{search_query}%'))
    else:
        cur = conn.execute('SELECT * FROM contacts')
        
    contacts = cur.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts, search=search_query)

# Ajout d'un contact
@app.route('/ajouter', methods=('GET', 'POST'))
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom'].strip()
        prenom = request.form['prenom'].strip()
        telephone = request.form['telephone'].strip()
        email = request.form['email'].strip()

        # 1. Condition : Exactement 10 chiffres
        if not (telephone.isdigit() and len(telephone) == 10):
            flash('Erreur : Le numéro de téléphone doit contenir exactement 10 chiffres.', 'danger')
            return render_template('ajouter.html')

        conn = get_db_connection()
        
        # 2. Condition : Éviter les doublons (Même téléphone ou même Email)
        doublon = conn.execute(
            'SELECT id FROM contacts WHERE telephone = ? OR email = ?', 
            (telephone, email)
        ).fetchone()

        if doublon:
            conn.close()
            flash('Erreur : Un contact avec ce numéro ou cet email existe déjà.', 'danger')
            return render_template('ajouter.html')

        # Insertion si valide
        conn.execute('INSERT INTO contacts (nom, prenom, telephone, email) VALUES (?, ?, ?, ?)',
                     (nom, prenom, telephone, email))
        conn.commit()
        conn.close()
        flash('Contact ajouté avec succès !', 'success')
        return redirect(url_for('index'))
        
    return render_template('ajouter.html')

# Modification d'un contact
@app.route('/modifier/<int:id>', methods=('GET', 'POST'))
def modifier(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nom = request.form['nom'].strip()
        prenom = request.form['prenom'].strip()
        telephone = request.form['telephone'].strip()
        email = request.form['email'].strip()

        # 1. Condition : Exactement 10 chiffres
        if not (telephone.isdigit() and len(telephone) == 10):
            flash('Erreur : Le numéro de téléphone doit contenir exactement 10 chiffres.', 'danger')
            return render_template('modifier.html', contact=contact)

        # 2. Condition : Éviter les doublons (en excluant le contact actuel)
        doublon = conn.execute(
            'SELECT id FROM contacts WHERE (telephone = ? OR email = ?) AND id != ?', 
            (telephone, email, id)
        ).fetchone()

        if doublon:
            flash('Erreur : Un autre contact possède déjà ce numéro ou cet email.', 'danger')
            return render_template('modifier.html', contact=contact)

        conn.execute('UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, email = ? WHERE id = ?',
                     (nom, prenom, telephone, email, id))
        conn.commit()
        conn.close()
        flash('Contact modifié avec succès !', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('modifier.html', contact=contact)


# Suppression d'un contact
@app.route('/supprimer/<int:id>', methods=('POST',))
def supprimer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Contact supprimé avec succès !')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# Exemple de gestion d'erreur dans app.py
if not nom or not telephone:
    flash("Le nom et le téléphone sont obligatoires !", "danger")