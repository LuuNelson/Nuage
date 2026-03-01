from datetime import datetime, timedelta
from random import randint
import db
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.context import CryptContext

app = Flask(__name__)

app.secret_key = b'd2b01c987b6f7f0d5896aae06c4f318c9772d6651abff24aec19297cdf5eb199'

@app.route("/") 
def home():
    return redirect(url_for("accueil"))

@app.route("/accueil")
def accueil():
    if "login" not in session:
        return render_template("accueil.html")
    return render_template("accueilC.html", pseudo = session["login"])
    
@app.route("/connexion")
def connexion():
    if "login" in session:
        return redirect(url_for("accueil"))
    return render_template("connexion.html")

@app.route("/verification", methods = ['POST'])
def ver():
    message = ""
    lst_pseudo = []
    login = request.form.get("login",None)
    mdp = request.form.get("mdp",None)
    if not login:
        return redirect(url_for("connexion"))
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pseudo, nom, mdp FROM joueur;")
            for result in cur:
                lst_pseudo.append(result.pseudo)
                if result.pseudo == login:
                    if result.mdp is None:
                        return redirect(url_for("creermdp"))
                    vrailogin = result.pseudo
                    vraimdp = result.mdp
            if login not in lst_pseudo:
                message = "On ne te reconnais pas.. Qui est-tu?"
                return render_template("erreurconnexion.html", message = message)
            if login == vrailogin:
                password_ctx = CryptContext(schemes=['bcrypt']) 
                test = password_ctx.verify(mdp, vraimdp)
                if test is True:
                    session["login"] = login
                    return redirect(url_for("accueil"))
                else:
                    message = "Mot de Passe Incorrect.."
                    return render_template("erreurconnexion.html", message = message)
            return render_template("erreurconnexion.html", message = message)

@app.route("/creation_mdp")
def creermdp():
    return render_template("creationMDP.html")
    
@app.route("/verrMDP", methods = ['POST'])
def vermdp():
    mdp1 = request.form.get("mdp1",None)
    mdp2 = request.form.get("mdp2",None)
    pseudo = request.form.get("pseudo", None)
    lst_pseudo = []
    message = ""
    if mdp1 != mdp2:
        message = "Les deux mots de passes doivent etre similaire"
        return render_template("erreurcreationMDP.html", message = message)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pseudo FROM joueur;")
            for result in cur:
                lst_pseudo.append(result.pseudo)
    if pseudo not in lst_pseudo:
        message = "On ne vous reconnais plus.. Vous vous etes trompé sur votre pseudo?"
        return render_template("erreurcreationMDP.html", message = message)
    password_ctx = CryptContext(schemes=['bcrypt'])
    hash_pw = password_ctx.hash(mdp1)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE joueur SET mdp = %s WHERE pseudo = %s;", (hash_pw, pseudo))
    conn.commit()
    conn.close()
    return render_template("succescreationMDP.html")

@app.route("/inscription")
def inscription():
    return render_template("inscription.html")

@app.route("/verinscr", methods = ['POST'])
def verinscr():
    pseudo = request.form.get("pseudo",None)
    nom = request.form.get("nom",None)
    email = request.form.get("email",None)
    dateN = request.form.get("datenaissance",None)
    mdp1 = request.form.get("mdp1",None)
    mdp2 = request.form.get("mdp2",None)
    message = ""
    idm = 0
    if not pseudo or not nom or not email or not dateN or not mdp1 or not mdp2:
        message = "Un champ n'a pas été rempli.. Tous les champs sont obligatoire !"
        return render_template("erreurinscription.html", message = message)
    date_naissance = datetime.strptime(dateN, "%Y-%m-%d").date()
    age = (datetime.now().date() - date_naissance).days // 365
    if age < 8: 
        message = "Vous devez avoir au moins 8 ans pour vous inscrire." 
        return render_template("erreurinscription.html", message=message)
    lst_pseudo = []
    lst_email = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pseudo, email FROM joueur;")
            for result in cur:
                lst_pseudo.append(result.pseudo)
                lst_email.append(result.email)
    conn.close()
    if pseudo in lst_pseudo:
        message = "Le pseudo que vous avez choisi est deja utilisé.. Choisis-en un autre !"
        return render_template("erreurinscription.html", message = message)
    if email in lst_email:
        message = "L'e-mail que vous avez utilisé est deja utilisé.. Donc théoriquement votre compte existe deja :)"
        return render_template("erreurinscription.html", message = message)
    if "@" not in email or "." not in email:
        message = "L'e-mail que vous avez utilisé n'est pas valide.. Vous vous etes trompé?"
        return render_template("erreurinscription.html", message = message)
    if len(pseudo) > 10:
        message = "Le pseudo que vous avez choisi est trop long.."
        return render_template("erreurinscription.html", message = message)
    if len(nom) > 20:
        message = "Le nom que vous avez est trop long.. Vous avez un surnom?"
        return render_template("erreurinscription.html", message = message)
    if len(email) > 100:
        message = "L'email que vous avez utilisé est trop long.."
        return render_template("erreurinscription.html", message = message)
    if mdp1 != mdp2:
        message = "Les deux mots de passes doivent etre similaire!"
        return render_template("erreurinscription.html", message = message)
    date = datetime.strptime(dateN, "%Y-%m-%d").date()
    
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO monnaie (solde) VALUES (0.00);")
    conn.commit()
    conn.close()
    
    password_ctx = CryptContext(schemes=['bcrypt'])
    hash_pw = password_ctx.hash(mdp1)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT idm FROM monnaie ORDER BY idM DESC LIMIT 1;")
            for result in cur:
                idm = result.idm
            cur.execute("INSERT INTO joueur (pseudo, nom, email, dateN, idM, mdp) VALUES (%s, %s, %s, %s, %s, %s);", (pseudo, nom, email, date, idm, hash_pw))
    conn.commit()
    conn.close()
    return render_template("succesinscription.html")
    
@app.route("/deconnexion")
def deconnexion():
    if "login" in session:
        session.pop("login")
    return redirect(url_for("accueil"))

@app.route("/<liste_jeux>")
def lstjeux(liste_jeux):
    lstJ = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            if liste_jeux == "liste_jeux":
                cur.execute("SELECT titre FROM jeux ORDER BY titre;")
            elif liste_jeux == "tridateV":
                cur.execute("SELECT titre, datesortie FROM jeux ORDER BY datesortie;")
            elif liste_jeux == "tridateJ":
                cur.execute("SELECT titre, datesortie FROM jeux ORDER BY datesortie DESC;")
            elif liste_jeux == "triventes":
                cur.execute("""SELECT titre, count(idj) AS nbventes FROM jeux NATURAL JOIN achete 
                            GROUP BY titre ORDER BY nbventes DESC;""")
            elif liste_jeux == "trinote":
                cur.execute("""SELECT titre, avg(note) AS notemoyenne 
                            FROM jeux NATURAL JOIN note 
                            GROUP BY titre ORDER BY notemoyenne DESC;""")
            elif liste_jeux == "triediteur":
                cur.execute("""SELECT titre, nom FROM jeux NATURAL JOIN edite NATURAL JOIN entreprise 
                            ORDER BY nom;""")
            elif liste_jeux == "tridev":
                cur.execute("""SELECT titre, nom FROM jeux NATURAL JOIN developpe NATURAL JOIN entreprise 
                            ORDER BY nom;""")
            else:
                cur.execute("""SELECT titre, nom FROM jeux NATURAL JOIN appartient NATURAL JOIN genre 
                            WHERE nom = %s;""", (liste_jeux,))
            for result in cur:
                if liste_jeux == "liste_jeux":
                    lstJ.append(result.titre)
                elif liste_jeux == "tridateV" or liste_jeux == "tridateJ":
                    lstJ.append(result.titre + " - " + str(result.datesortie))
                elif liste_jeux == "triventes":
                    lstJ.append(result.titre + " - " + str(result.nbventes))
                elif liste_jeux == "trinote":
                    lstJ.append(result.titre + " - " + str(round(float(result.notemoyenne), 1)) + "/10")
                else:
                    lstJ.append(result.titre + " - " + str(result.nom))
    conn.close()
    if liste_jeux == "trinote":
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT titre FROM jeux;")
                for result in cur:
                    presence = 0
                    for i in range(len(lstJ)):
                        if result.titre in lstJ[i]:
                            presence = 1
                    if presence == 0:
                        lstJ.append(result.titre + " - Aucune donnée")

    if "login" not in session:
        return render_template("lstjeux.html", jeux = lstJ)
    return render_template("lstjeuxC.html", jeux = lstJ)

@app.route("/liste_jeux/<titre>")
def jeux(titre):
    if titre == 'liste_jeux':
      return redirect(url_for("lstjeux", liste_jeux = "liste_jeux"))
    if titre == 'connexion':
      return redirect(url_for("connexion"))
    if titre == 'inscription':
      return redirect(url_for("inscription"))
    i = 1
    titren = ""
    if "-" in titre:
        while titre[i] != "-":
            titren += titre[i-1]
            i+=1
    else:
        titren = titre
    info = []
    commentaires = []
    notemoyenne = 0
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM jeux NATURAL JOIN developpe NATURAL JOIN entreprise;")
            for result in cur:
                if result.titre == titren:
                    nomjeu = result.titre
                    info.append(result.descriptionj)
                    info.append(result.agerequis)
                    info.append(result.datesortie)
                    info.append(result.prix)
                    info.append(result.nom)
            cur.execute("SELECT * FROM jeux NATURAL JOIN edite NATURAL JOIN entreprise;")
            for result2 in cur:
                if result2.titre == titren:
                    info.append(result2.nom)
            cur.execute("""SELECT nom FROM jeux NATURAL JOIN appartient NATURAL JOIN genre 
                        WHERE titre = %s;""", (titren,))
            i = 0
            for result3 in cur:
                if i == 0:
                    info.append(result3.nom)
                    i += 1
                else:
                    info[6] = info[6] + " - " + result3.nom
                    
    conn.close()
    if "login" not in session:
        action = 1
        return render_template("infojeux.html", info = info, jeu = nomjeu, action = action)
    action = 2
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pseudo, titre, datea FROM joueur NATURAL JOIN achete NATURAL JOIN jeux;")
            for result4 in cur:
                if result4.titre == titren:
                    if result4.pseudo == session["login"]:
                        info.append(result4.datea)
                        action = 3
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT note, commentaire, pseudo FROM joueur NATURAL JOIN note NATURAL JOIN jeux 
                        WHERE titre = %s;""", (titren,))
            for result in cur:
                if result.pseudo == session["login"]:
                    noteur = "Vous"
                else:
                    noteur = result.pseudo
                commentaires.append(str(result.note) + "/10.  " + result.commentaire + " Par " + noteur)
    conn.close()
    if commentaires == []:
        commentaires = ["Aucun commentaire"]
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, avg(note) as notemoyenne 
                        FROM jeux natural join note WHERE titre = %s 
                        GROUP BY titre ORDER BY notemoyenne DESC;""", (titren,))
            for result in  cur:
                notemoyenne = round(result.notemoyenne, 1)
    return render_template("infojeux.html", info = info, jeu = nomjeu, action = action, commentaires = commentaires, moyenne = notemoyenne)

@app.route("/liste_jeux/<jeu>/achat")
def achat(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    prix = ""
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT prix FROM jeux WHERE titre = %s;", (jeu,))
            for result in cur:
                prix = result.prix
    conn.close()
    titre = "Achat de " + jeu
    head = "Achat"
    return render_template("validation.html", jeu = jeu, prix = prix, titre = titre, header = head)

@app.route("/liste_jeux/<jeu>/<verachat>", methods = ['GET', 'POST'])
def verifachat(jeu, verachat):
    if "login" not in session:
        return redirect(url_for("connexion"))
    Anon = request.form.get("Anon")
    Aoui = request.form.get("Aoui")
    if request.method == 'GET' or (request.method == 'POST' and Anon is not None):
        return redirect(url_for("jeux", titre = jeu))
    message  = ""
    titre = "Achat de " + jeu
    head = "Achat"
    action = 1
    if Aoui is not None:
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT idj, prix, agerequis FROM jeux WHERE titre = %s;", (jeu,))
                for result in cur:
                    prixjeu = result.prix
                    idjeux =  result.idj
                    agerequis = result.agerequis
                cur.execute("""SELECT solde, idp, idm, daten FROM joueur NATURAL JOIN monnaie 
                            WHERE pseudo = %s;""", (session['login'],))
                for result2 in cur:
                    soldejoueur = result2.solde
                    idjoueur = result2.idp
                    idmonnaie = result2.idm
                    datenaissace = result2.daten
                if soldejoueur < prixjeu:
                    message = "Vous n'avez pas assez de Nuage-Money pour acheter ce jeu. Veuillez ajouter de l'argent à votre compte."
                    return render_template("erreur.html", message = message, action = action, head = head, titre = titre)
                date_actuelle = datetime.now().date()
                age = date_actuelle.year - datenaissace.year
                if (date_actuelle.month, date_actuelle.day) < (datenaissace.month, datenaissace.day):
                    age -= 1
                if age < agerequis:
                    message = "Vous n'êtes pas assez grand pour jouer a ce jeu. Revenez dans quelques années :)"
                    return render_template("erreur.html", message = message, action = action, head = head, titre = titre)
                date_actuelle = datetime.now()
                date = date_actuelle.strftime("%Y-%m-%d")
                cur.execute("INSERT INTO achete (idJ, idP, dateA) VALUES (%s, %s, %s)", (idjeux, idjoueur, date))
                cur.execute("UPDATE monnaie SET solde = %s WHERE idM = %s;", (soldejoueur - prixjeu, idmonnaie))
        conn.commit()
        conn.close()
        message = "Vous possedez maintenant le jeu " + jeu + "! -" + str(prixjeu) + " $ sur votre compte."
        return render_template("succes.html", message = message, titre = titre, action = action, head = head)
    message = "Echec de l'achat"
    return render_template("erreur.html", message = message, action = action, head = head, titre = titre)

@app.route("/jeuxjoueur")
def jeuxdujoueur():
    if "login" not in session:
        return redirect(url_for("connexion"))
    jeux = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT idP FROM joueur WHERE pseudo = %s;", (session["login"],))
            joueur_id = cur.fetchone()
            if joueur_id:
                cur.execute("""SELECT j.titre FROM jeux j 
                            JOIN achete a ON j.idJ = a.idJ 
                            WHERE a.idP = %s;""", (joueur_id[0],))
                jeux = [result.titre for result in cur.fetchall()]
            cur.execute("""SELECT titre, idp1, idp2, pseudo 
                        FROM partage NATURAL JOIN jeux JOIN joueur ON idp2 = joueur.idp 
                        WHERE pseudo = %s""", (session["login"],))
            for result in cur:
                if result.titre not in jeux:
                    jeux.append(result.titre + " (partagé)")
    conn.close()
    return render_template("jeuxjoueur.html", jeux=jeux)

@app.route("/jeuxjoueur/<jeu>")
def pageparjeu(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    if "(" in jeu:
        jeureduit = ""
        i = 1
        while jeu[i] != "(":
            jeureduit += jeu[i-1]
            i += 1
        return redirect(url_for("pageparjeu", jeu = jeureduit))
    info = []
    lstsucces = []
    premier = 1
    second = 1
    infonote = []
    partage = 1
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM jeux NATURAL JOIN developpe NATURAL JOIN entreprise;")
            for result in cur:
                if result.titre == jeu:
                    idjeu = result.idj
                    info.append(result.descriptionj)
                    info.append(result.agerequis)
                    info.append(result.datesortie)
                    info.append(result.prix)
                    info.append(result.nom)
            cur.execute("SELECT * FROM jeux NATURAL JOIN edite NATURAL JOIN entreprise;")
            for result2 in cur:
                if result2.titre == jeu:
                    info.append(result2.nom)
            cur.execute("""SELECT nom FROM jeux NATURAL JOIN appartient NATURAL JOIN genre 
                        WHERE titre = %s;""", (jeu,))
            i = 0
            for result2 in cur:
                if i == 0:
                    info.append(result2.nom)
                    i += 1
                else:
                    info[6] = info[6] + " - " + result2.nom
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT pseudo, titre, datea 
                        FROM joueur NATURAL JOIN achete NATURAL JOIN jeux;""")
            for result4 in cur:
                if result4.titre == jeu:
                    if result4.pseudo == session["login"]:
                        info.append(result4.datea)
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT intitule, descriptionS 
                        FROM succes WHERE idj = %s;""", (idjeu,))
            for result in cur:
                lstsucces.append(result.intitule + ": " + result.descriptions)
            cur.execute("""SELECT intitule, descriptions, dater, pseudo 
                        FROM succes NATURAL JOIN reussi NATURAL JOIN joueur""")
            for result2 in cur:
                for i in range(len(lstsucces)):
                    if result2.intitule + ": " + result2.descriptions == lstsucces[i]:
                        if result2.pseudo == session["login"]:
                            lstsucces[i] = lstsucces[i] + "   (reussi le: " + str(result2.dater) + ")"
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT note, commentaire, pseudo 
                        FROM note NATURAL JOIN joueur 
                        WHERE pseudo = %s and idj = %s;""", (session["login"],idjeu))
            for result in cur:
                premier = 2
                infonote.append(result.note)
                infonote.append(result.commentaire)
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, idp1, idp2, pseudo 
                        FROM partage NATURAL JOIN jeux JOIN joueur ON idp1 = joueur.idp 
                        WHERE pseudo = %s;""", (session["login"],))
            for result in cur:
                second = 2
                if result.titre == jeu:
                    second = 3
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, idp1, idp2, pseudo 
                        FROM partage NATURAL JOIN jeux JOIN joueur ON idp2 = joueur.idp 
                        WHERE pseudo = %s""", (session["login"],))
            for result in cur:
                if result.titre == jeu:
                    partage = 2
                    second = 4
    conn.close()
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT count(code) as nbtotal 
                        FROM succes NATURAL JOIN jeux WHERE titre = %s""", (jeu,))
            for result in cur:
                nbsucces = result.nbtotal
            cur.execute("""SELECT count(code) as reussi 
                        FROM jeux NATURAL JOIN succes 
                        NATURAL JOIN reussi NATURAL JOIN joueur 
                        WHERE titre = %s and pseudo = %s""", (jeu, session["login"]))
            for result2 in cur:
                nbreussi = result2.reussi
            completion = int((nbreussi/nbsucces)*100)
    conn.close()
    return render_template("pageparjeu.html", jeu = jeu, info = info, liste_succes = lstsucces, premier = premier, second = second, info_note = infonote, partage = partage, completion = completion)

@app.route("/jeuxjoueur/<jeu>/jouer")
def jouerjeux(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    amis = []
    head = jeu
    titre = "Jouer à " + jeu
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p1.pseudo AS pseudo1, p2.pseudo AS pseudo2
                FROM amis
                JOIN joueur AS p1 ON idp1 = p1.idp
                JOIN joueur AS p2 ON idp2 = p2.idp
                WHERE (p1.pseudo = %s OR p2.pseudo = %s) AND demande = 1
            """, (session["login"], session["login"]))
            for result in cur:
                if result.pseudo1 != session["login"] and result.pseudo1 not in amis:
                    amis.append(result.pseudo1)
                if result.pseudo2 != session["login"] and result.pseudo2 not in amis:
                    amis.append(result.pseudo2)
    conn.close()
    if not amis:
        return redirect(url_for("lancement", jeu=jeu, lancement_jeu="solo"))
    return render_template("jouer.html", header=head, titre=titre, amis=amis)

@app.route("/jeuxjoueur/<jeu>/<lancement_jeu>", methods = ['GET', 'POST'])
def lancement(jeu, lancement_jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    message = "Vous êtes en train de jouer a " + jeu
    if request.method == 'GET':
        if lancement_jeu == "quitter":
            return redirect(url_for("pageparjeu", jeu = jeu))
        return render_template("succes.html", head = jeu, titre = jeu, message = message, action = 2)
    else:
        ami = request.form.get("ami", None)
        message += " avec " + ami
        return render_template("succes.html", head = jeu, titre = jeu, message = message, action = 2)

@app.route("/jeuxjoueur/<jeu>/noter")
def noter(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    return render_template("noter.html", header = jeu, titre = "Avis sur " + jeu, action = 1)

@app.route("/jeuxjoueur/<jeu>/notation", methods = ['POST'])
def notation(jeu):
    note = request.form.get("note", None)
    commentaire = request.form.get("commentaire")
    with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
                for result in cur:
                    idjoueur = result.idp
                cur.execute("SELECT idj FROM jeux WHERE titre = %s", (jeu,))
                for result in cur:
                    idjeux = result.idj
                if commentaire is None or commentaire == "Ecrivez votre commentaire ici !" or commentaire == "":
                    commentaire = "Aucun commentaire"
                cur.execute("INSERT INTO note (idj, idp, commentaire, note) VALUES (%s, %s, %s, %s)", (idjeux, idjoueur, commentaire, note))
    conn.commit()
    conn.close()
    message = "Avis ajouté avec succes!"
    return render_template("succes.html", head = jeu, titre = "Avis sur " + jeu, action = 3, message = message)

@app.route("/jeuxjoueur/<jeu>/modifier")
def modifier(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    return render_template("noter.html", header = jeu, titre = "Avis sur " + jeu, action = 2)

@app.route("/jeuxjoueur/<jeu>/notemodif", methods = ['POST'])
def notemodif(jeu):
    note = request.form.get("note", None)
    commentaire = request.form.get("commentaire")
    with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
                for result in cur:
                    idjoueur = result.idp
                cur.execute("SELECT idj FROM jeux WHERE titre = %s", (jeu,))
                for result in cur:
                    idjeux = result.idj
                if commentaire is None or commentaire == "Ecrivez votre commentaire ici !" or commentaire == "":
                    commentaire = "Aucun commentaire"
                cur.execute("UPDATE note SET commentaire = %s WHERE idj = %s and idp = %s;", (commentaire, idjeux, idjoueur))
                cur.execute("UPDATE note SET note = %s WHERE idj = %s and idp = %s;", (note, idjeux, idjoueur))
    conn.commit()
    conn.close()
    message = "Avis modifié avec succes!"
    return render_template("succes.html", head = jeu, titre = "Avis sur " + jeu, action = 3, message = message)

@app.route("/jeuxjoueur/<jeu>/partager")
def partager(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    amis = []
    head = jeu
    titre = "Partager " + jeu
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT p1.pseudo AS pseudo1, idp1, idp2, p2.pseudo AS pseudo2 
                        FROM amis 
                        JOIN joueur AS p1 ON idp1 = p1.idp 
                        JOIN joueur AS p2 ON idp2 = p2.idp 
                        WHERE (p1.pseudo = %s OR p2.pseudo = %s) 
                        AND demande = 1;""", (session["login"], session["login"]))
            for result in cur:
                if result.pseudo1 != session["login"] and result.pseudo1 not in amis:
                    amis.append(result.pseudo1)
                if result.pseudo2 != session["login"] and result.pseudo2 not in amis:
                    amis.append(result.pseudo2)
    conn.close()
    if amis == []:
        message = "Vous avez aucun amis.. Ca va venir!"
        return render_template("erreur.html", message = message, action = 2, titre = titre, head = jeu)
    return render_template("partager.html", header = head, titre = titre, amis = amis)

@app.route("/jeuxjoueur/<jeu>/partage", methods = ['POST'])
def partage(jeu):
    if "login" not in session:
        return redirect(url_for("connexion"))
    ami = request.form.get("ami", None)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre FROM joueur NATURAL JOIN achete NATURAL JOIN jeux 
                        WHERE pseudo = %s;""", (ami,))
            for result3 in cur:
                if result3.titre == jeu:
                    message = "Vous ne pouvez pas partager ce jeu a votre amis car il le possede deja !"
                    return render_template("erreur.html", message = message, head = jeu, titre = "Partager " + jeu, action = 2)
            cur.execute("SELECT daten FROM joueur WHERE pseudo = %s", (ami,))
            for result in cur:
                datenamis = result.daten
            cur.execute("SELECT agerequis FROM jeux WHERE titre = %s", (jeu,))
            for result2 in cur:
                agerequis = result2.agerequis
    conn.close()
    date_actuelle = datetime.now().date()
    ageamis = date_actuelle.year - datenamis .year
    if (date_actuelle.month, date_actuelle.day) < (datenamis .month, datenamis .day):
        ageamis -= 1
    if ageamis < agerequis:
        message = "Votre amis n'est pas assez grand pour jouer a ce jeu.. Partagez lui dans quelques années :)"
        return render_template("erreur.html", message = message, head = jeu, titre = "Partager " + jeu, action = 2)
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT idj FROM jeux WHERE titre = %s", (jeu,))
            for result in cur:
                idjeu = result.idj
            cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
            for result2 in cur:
                idjoueur1 = result2.idp
            cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (ami,))
            for result3 in cur:
                idjoueur2 = result3.idp   
            cur.execute("INSERT INTO partage (idj, idp1, idp2) VALUES (%s, %s, %s)", (idjeu, idjoueur1, idjoueur2))
    conn.commit()
    conn.close()
    message = "Jeu partagé avec succes !"
    return render_template("succes.html", message = message, action = 3, head = jeu, titre = "Partager " + jeu)  

@app.route("/compte")
def compte():
    if "login" not in session:
        return redirect(url_for("connexion"))
    informations = []
    date_naissance = ""
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM joueur NATURAL JOIN monnaie;")
            for result in cur:
                if result.pseudo == session["login"]:
                    informations.append(result.nom)
                    informations.append(result.email)
                    informations.append(result.daten)
                    informations.append(result.solde)
                    informations.append(result.pseudo)
                    date_naissance = result.daten
    date_actuelle = datetime.now().date()
    age = date_actuelle.year - date_naissance.year
    if (date_actuelle.month, date_actuelle.day) < (date_naissance.month, date_naissance.day):
        age -= 1
    informations.append(age)
    return render_template("compte.html", prenom = session["login"], info = informations)

@app.route("/modification", methods = ['GET', 'POST'])
def modification():
    if "login" not in session:
        return redirect(url_for("connexion"))
    head = ""
    titre = ""
    message = ""
    action = 0
    if request.method == 'GET':
        action = 1
        head = "Suppression"
        titre = "Suppression de votre compte.."
        message = "Êtes vous vraiment sur de vouloir nous quitter?"
        return render_template("modification.html", header = head, titre = titre, message = message, action = action)
    nom = request.form.get("nom")
    email = request.form.get("email")
    mdp = request.form.get("mdp")
    argent = request.form.get("money")
    pseudo = request.form.get("pseudo")
    head = "Modification"
    titre = "Modification de vos informations"
    if nom is not None:
        action = 2
        message = "Saisissez le nouveau nom que vous voulez."
        return render_template("modification.html", header = head, titre = titre, message = message, action = action)
    if email is not None:
        action = 3
        message = "Saisissez votre nouvel adresse e-mail."
        return render_template("modification.html", header = head, titre = titre, message = message, action = action)
    if argent is not None:
        action = 4
        message = "Saisissez le montant que vous voulez ajouter."
        return render_template("modification.html", header = head, titre = titre, message = message, action = action)
    if mdp is not None:
        action = 5
        message = "Saisissez les informations demandées pour modifier votre mot de passe."
        return render_template("modification.html", header = head, titre = titre, message = message, action = action)
    if pseudo is not None:
        action = 6
        message = "Saisissez le nouveau pseudo que vous voulez utiliser."
        return render_template("modification.html", header = head, titre = titre, message = message, action = action)
    
@app.route("/vermodif", methods = ['POST'])
def vermodif():
    if "login" not in session:
        return redirect(url_for("connexion"))
    nom = request.form.get("nom")
    Soui = request.form.get("supp_oui")
    Snon = request.form.get("supp_non")
    email = request.form.get("email")
    argent = request.form.get("money")
    pseudo = request.form.get("pseudo")
    mdpA = request.form.get("mdpA")
    mdp1 = request.form.get("mdp1")
    mdp2 = request.form.get("mdp2")
    head = ""
    titre = ""
    message = ""
    action = 0
    if Snon is not None:
        return redirect(url_for("compte"))
    if Soui is not None:
        message = "Votre compte a bien été supprimé.. Vous allez nous manquer !"
        action = 1
        head = "Suppression"
        titre = "Suppression de votre compte.."
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM joueur WHERE pseudo = %s;", (session["login"],))
        conn.commit()
        conn.close()
        return render_template("succesmodif.html", message = message, action =  action, head = head, titre = titre)
    head = "Modification"
    titre = "Modification de vos informations"
    action = 2
    message = "Modification réussi!"
    if pseudo is not None:
        lst_pseudo = []
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT pseudo FROM joueur;")
                for result in cur:
                    lst_pseudo.append(result.pseudo)
        conn.close()
        if pseudo in lst_pseudo:
            message = "Le pseudo que vous avez choisi est deja utilisé.. Choisis-en un autre !"
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        if len(pseudo) > 10:
            message = "Le pseudo que vous avez choisi est trop long.."
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE joueur SET pseudo = %s WHERE pseudo = %s;", (pseudo, session["login"]))
        conn.commit()
        conn.close()
        action = 3
        return render_template("succesmodif.html", message = message, action = action, head = head, titre = titre)
    if nom is not None:
        if len(nom) > 20:
            message = "Le nom que vous avez est trop long.. Vous avez un surnom?"
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE joueur SET nom = %s WHERE pseudo = %s;", (nom, session["login"]))
        conn.commit()
        conn.close()
        return render_template("succesmodif.html", message = message, action = action, head = head, titre = titre)
    if email is not None:
        lst_email = []
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT email FROM joueur;")
                for result in cur:
                    lst_email.append(result.email)
        conn.close()
        if email in lst_email:
            message = "L'e-mail que vous avez utilisé est deja utilisé.."
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        if "@" not in email or "." not in email:
            message = "L'e-mail que vous avez utilisé n'est pas valide.. Vous vous etes trompé?"
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE joueur SET email = %s WHERE pseudo = %s;", (email, session["login"]))
        conn.commit()
        conn.close()
        return render_template("succesmodif.html", message = message, action = action, head = head, titre = titre)
    if argent is not None:
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT pseudo, solde, idm FROM monnaie NATURAL JOIN joueur;")
                for result in cur:
                    if result.pseudo == session["login"]:
                        solde = float(result.solde) + float(argent)
                        idmonnaie = result.idm
                if solde > 9999:
                    message = "Vous ne pouvez pas ajouter une telle somme.. Il ne doit pas avoir plus de 9999.99$ sur votre compte !"
                    return render_template("erreurmodif.html", message = message, head = head, titre = titre)
                cur.execute("UPDATE monnaie SET solde = %s WHERE idm = %s;", (solde, idmonnaie))
        conn.commit()
        conn.close()
        return render_template("succesmodif.html", message = message, action = action, head = head, titre = titre)
    if mdpA is not None:
        if mdp1 != mdp2:
            message = "Les deux mots de passes doivent etre similaire!"
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT pseudo, mdp FROM joueur;")
                for result in cur:
                    if result.pseudo == session["login"]:
                        mdp = result.mdp
        conn.close()
        password_ctx = CryptContext(schemes=['bcrypt']) 
        test = password_ctx.verify(mdpA, mdp)
        if test == False:
            message = "Votre ancien mot de passe est incorrect !"
            return render_template("erreurmodif.html", message = message, head = head, titre = titre)
        hash_pw = password_ctx.hash(mdp1)
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE joueur SET mdp = %s WHERE pseudo = %s;", (hash_pw, session["login"]))
        conn.commit()
        conn.close()
        action = 3
        return render_template("succesmodif.html", message = message, action = action, head = head, titre = titre)
    message = "Erreur dans la modification."
    return render_template("erreurmodif.html", message = message, head = head, titre = titre)

@app.route("/amis")
def lstamis():
    if "login" not in session:
        return redirect(url_for("connexion"))
    
    joueurs = []
    user_login = session["login"]
    
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT p1.pseudo AS pseudo1, idp1, idp2, p2.pseudo AS pseudo2 
                        FROM amis 
                        JOIN joueur AS p1 ON idp1 = p1.idp 
                        JOIN joueur AS p2 ON idp2 = p2.idp 
                        WHERE (p1.pseudo = %s OR p2.pseudo = %s) 
                        AND demande = 1;""", (session["login"], session["login"]))
            for result in cur:
                if result.pseudo1 != session["login"] and result.pseudo1 not in joueurs:
                    joueurs.append(result.pseudo1)
                if result.pseudo2 != session["login"] and result.pseudo2 not in joueurs:
                    joueurs.append(result.pseudo2)
            cur.execute("""SELECT count(demande) AS nbdemandes 
                        FROM amis JOIN joueur ON idp = idp2 
                        WHERE pseudo = %s AND demande = 0""", (user_login,))
            for result2 in cur:
                nbdemandes = result2.nbdemandes
    conn.close()
    if joueurs == []:
        joueurs.append(0)
    return render_template("lstamis.html", joueurs=joueurs, demandes = nbdemandes)

@app.route("/amis/ajouter")
def ajouteramis():
    if "login" not in session:
        return redirect(url_for("connexion"))
    
    lstamis = []
    joueurs = []
    user_login = session["login"]
    
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT p1.pseudo AS pseudo1, idp1, idp2, p2.pseudo AS pseudo2 
                        FROM amis 
                        JOIN joueur AS p1 ON idp1 = p1.idp 
                        JOIN joueur AS p2 ON idp2 = p2.idp 
                        WHERE (p1.pseudo = %s OR p2.pseudo = %s);""", (session["login"], session["login"]))
            for result in cur:
                if result.pseudo1 != session["login"] and result.pseudo1 not in lstamis:
                    lstamis.append(result.pseudo1)
                if result.pseudo2 != session["login"] and result.pseudo2 not in lstamis:
                    lstamis.append(result.pseudo2)
            cur.execute("SELECT pseudo FROM joueur;")
            for result in cur:
                if result.pseudo not in lstamis and result.pseudo != user_login:
                    joueurs.append(result.pseudo)
            cur.execute("""SELECT count(demande) AS nbdemandes 
                        FROM amis JOIN joueur ON idp = idp1 
                        WHERE pseudo = %s AND demande = 0""", (user_login,))
            for result2 in cur:
                nbdemandes = result2.nbdemandes
    conn.close()
    return render_template("amis.html", joueurs=joueurs, demandes = nbdemandes)

@app.route("/amis/<ami>")
def ami(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    lstjeux = []
    lstsucces = []
    lstnotes = []
    partage = 0
    titre = ""
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, datea FROM jeux NATURAL JOIN achete NATURAL JOIN joueur 
                        WHERE pseudo = %s;""", (ami,))
            for result in cur:
                lstjeux.append(result.titre + " - Depuis le " + str(result.datea))
            cur.execute("""SELECT titre, p1.pseudo AS partageur 
                        FROM jeux NATURAL JOIN partage 
                        JOIN joueur AS p1 ON p1.idp = idp1 
                        JOIN joueur AS p2 ON p2.idp = idp2 
                        WHERE p2.pseudo = %s""", (ami,))
            for result2 in cur:
                lstjeux.append(result2.titre)
                if result2.partageur == session["login"]:
                    partage = 1
                    titre = result2.titre
            cur.execute("""SELECT titre, intitule, dater 
                        FROM jeux NATURAL JOIN succes 
                        NATURAL JOIN reussi NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for resutl3 in cur:
                lstsucces.append(resutl3.titre + " - " + resutl3.intitule + " - Reussi le " + str(resutl3.dater))
            cur.execute("""SELECT note, commentaire, titre 
                        FROM jeux NATURAL JOIN note NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for result4 in cur:
                lstnotes.append(result4.titre + " - " + str(result4.note) + "/10  " + result4.commentaire)
    conn.close()
    if lstjeux == []:
        lstjeux.append("Aucun jeu possédé")
    if lstsucces == []:
        lstsucces.append("Aucun succès reussi")
    if lstnotes == []:
        lstnotes.append("Aucune note laissé")
    return render_template("pageparami.html", jeu = ami, partage = partage, action = 1, liste_jeux = lstjeux, liste_succes = lstsucces, liste_notes = lstnotes, titre = titre)

@app.route("/amis/<ami>/arret")
def arretpartage(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    return render_template("confirmation.html", header = ami, action = 3, titre = "Arret du partage")

@app.route("/amis/<ami>/arreter", methods = ['POST'])
def arreter(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    oui = request.form.get("Aoui")
    non = request.form.get("Anon")
    if non is not None:
        return redirect(url_for("ami", ami = ami))
    if oui is not None:
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
                for result in cur:
                    idjoueur = result.idp
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (ami,))
                for result in cur:
                    idami = result.idp
                cur.execute("DELETE FROM partage WHERE idp1 = %s AND idp2 = %s", (idjoueur, idami))
        conn.commit()
        conn.close()
        message = "Partage bien arreté.."
        return render_template("succes.html", message = message, action = 6, head = ami, titre = "Arret du partage")
    message = "Erreur dans la 'larret du partage.."
    return render_template("erreur.html", message = message, action = 5, head = ami, titre = "Arret du partage")

@app.route("/amis/<ami>/supprimer")
def arretamis(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    return render_template("confirmation.html", header = ami, action = 2, titre = "Suppression d'un ami")

@app.route("/amis/<ami>/suppr", methods = ['POST'])
def supprimer(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    oui = request.form.get("Aoui")
    non = request.form.get("Anon")
    if non is not None:
        return redirect(url_for("ami", ami = ami))
    if oui is not None:
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
                for result in cur:
                    idjoueur = result.idp
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (ami,))
                for result in cur:
                    idami = result.idp
                cur.execute("DELETE FROM amis WHERE (idp1 = %s AND idp2 = %s) OR (idp1 = %s AND idp2 = %s)", (idjoueur, idami, idami, idjoueur))
                cur.execute("DELETE FROM partage WHERE (idp1 = %s AND idp2 = %s) OR (idp1 = %s AND idp2 = %s)", (idjoueur, idami, idami, idjoueur))
        conn.commit()
        conn.close()
        message = "Ami bien supprimé.."
        return render_template("succes.html", message = message, action = 5, head = ami, titre = "Suppression d'un ami")
    message = "Erreur dans la suppression de l'ami.."
    return render_template("erreur.html", message = message, action = 4, head = ami, titre = "Suppression d'un ami")

@app.route("/amis/ajouter/<ami>")
def amisaajouter(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    lstjeux = []
    lstsucces = []
    lstnotes = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, datea FROM jeux 
                        NATURAL JOIN achete NATURAL JOIN joueur 
                        WHERE pseudo = %s;""", (ami,))
            for result in cur:
                lstjeux.append(result.titre + " - Depuis le " + str(result.datea))
            cur.execute("""SELECT titre FROM jeux NATURAL JOIN partage 
                        JOIN joueur ON idp = idp2 WHERE pseudo = %s""", (ami,))
            for result2 in cur:
                lstjeux.append(result2.titre)
            cur.execute("""SELECT titre, intitule, dater 
                        FROM jeux NATURAL JOIN succes 
                        NATURAL JOIN reussi NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for resutl3 in cur:
                lstsucces.append(resutl3.titre + " - " + resutl3.intitule + " - Reussi le " + str(resutl3.dater))
            cur.execute("""SELECT note, commentaire, titre 
                        FROM jeux NATURAL JOIN note NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for result4 in cur:
                lstnotes.append(result4.titre + " - " + str(result4.note) + "/10  " + result4.commentaire)
    conn.close()
    if lstjeux == []:
        lstjeux.append("Aucun jeu possédé")
    if lstsucces == []:
        lstsucces.append("Aucun succès reussi")
    if lstnotes == []:
        lstnotes.append("Aucune note laissé")
    return render_template("pageparami.html", jeu = ami, action = 2, liste_jeux = lstjeux, liste_succes = lstsucces, liste_notes = lstnotes)

@app.route("/amis/demande")
def demandeenvoye():
    if "login" not in session:
        return redirect(url_for("connexion"))
    amis = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT p2.pseudo AS demande 
                        FROM amis 
                        JOIN joueur AS p1 ON p1.idp = idp1 
                        JOIN joueur AS p2 ON p2.idp = idp2 
                        WHERE p1.pseudo = %s 
                        AND demande = 0""", (session["login"],))
            for result in cur:
                amis.append(result.demande)
    conn.close()
    if amis == []:
        amis.append(0)
    return render_template("lstdemandes.html", action = 2, head = "Demandes d'amis reçus", joueurs = amis)
    
@app.route("/amis/demande/<ami>")
def amienvoye(ami):
    lstjeux = []
    lstsucces = []
    lstnotes = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, datea 
                        FROM jeux NATURAL JOIN achete NATURAL JOIN joueur 
                        WHERE pseudo = %s;""", (ami,))
            for result in cur:
                lstjeux.append(result.titre + " - Depuis le " + str(result.datea))
            cur.execute("""SELECT titre FROM jeux NATURAL JOIN partage 
                        JOIN joueur ON idp = idp2 WHERE pseudo = %s""", (ami,))
            for result2 in cur:
                lstjeux.append(result2.titre)
            cur.execute("""SELECT titre, intitule, dater 
                        FROM jeux NATURAL JOIN succes 
                        NATURAL JOIN reussi NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for resutl3 in cur:
                lstsucces.append(resutl3.titre + " - " + resutl3.intitule + " - Reussi le " + str(resutl3.dater))
            cur.execute("""SELECT note, commentaire, titre 
                        FROM jeux NATURAL JOIN note NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for result4 in cur:
                lstnotes.append(result4.titre + " - " + str(result4.note) + "/10  " + result4.commentaire)
    conn.close()
    if lstjeux == []:
        lstjeux.append("Aucun jeu possédé")
    if lstsucces == []:
        lstsucces.append("Aucun succès reussi")
    if lstnotes == []:
        lstnotes.append("Aucune note laissé")
    return render_template("pageparami.html", jeu = ami, action = 4, liste_jeux = lstjeux, liste_succes = lstsucces, liste_notes = lstnotes)
    
@app.route("/amis/ajouter/<ami>/confirmation")
def confirmation(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    return render_template("confirmation.html", header = ami, action = 1, titre = "Ajout d'ami")

@app.route("/amis/ajouter/<ami>/confirmer", methods = ['POST'])
def confirmerami(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    oui = request.form.get("Aoui")
    non = request.form.get("Anon")
    if non is not None:
        return redirect(url_for("amisaajouter", ami = ami))
    if oui is not None:
        with db.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
                for result in cur:
                    idjoueur = result.idp
                cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (ami,))
                for result in cur:
                    idami = result.idp
                cur.execute("INSERT INTO amis (idp1, idp2, demande) VALUES (%s, %s, 0)", (idjoueur, idami))
        conn.commit()
        conn.close()
        message = "Demande d'ami bien envoyé!"
        return render_template("succes.html", message = message, action = 4, head = ami, titre = "Ajout d'amis")
    message = "Erreur dans l'ajout d'amis"
    return render_template("erreur.html", message = message, action = 3, head = ami, titre = "Ajout d'amis")

@app.route("/demande")
def demanderecu():
    if "login" not in session:
        return redirect(url_for("connexion"))
    amis = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT p1.pseudo AS demande 
                        FROM amis 
                        JOIN joueur AS p1 ON p1.idp = idp1 
                        JOIN joueur AS p2 ON p2.idp = idp2 
                        WHERE p2.pseudo = %s 
                        AND demande = 0;""", (session["login"],))
            for result in cur:
                amis.append(result.demande)
    conn.close()
    if amis == []:
        amis.append(0)
    return render_template("lstdemandes.html", action = 1, head = "Demandes d'amis reçus", joueurs = amis)

@app.route("/demande/<ami>")
def amirecu(ami):
    lstjeux = []
    lstsucces = []
    lstnotes = []
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT titre, datea FROM jeux 
                        NATURAL JOIN achete NATURAL JOIN joueur 
                        WHERE pseudo = %s;""", (ami,))
            for result in cur:
                lstjeux.append(result.titre + " - Depuis le " + str(result.datea))
            cur.execute("""SELECT titre FROM jeux NATURAL JOIN partage 
                        JOIN joueur ON idp = idp2 WHERE pseudo = %s""", (ami,))
            for result2 in cur:
                lstjeux.append(result2.titre)
            cur.execute("""SELECT titre, intitule, dater 
                        FROM jeux NATURAL JOIN succes 
                        NATURAL JOIN reussi NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for resutl3 in cur:
                lstsucces.append(resutl3.titre + " - " + resutl3.intitule + " - Reussi le " + str(resutl3.dater))
            cur.execute("""SELECT note, commentaire, titre 
                        FROM jeux NATURAL JOIN note NATURAL JOIN joueur 
                        WHERE pseudo = %s""", (ami,))
            for result4 in cur:
                lstnotes.append(result4.titre + " - " + str(result4.note) + "/10  " + result4.commentaire)
    conn.close()
    if lstjeux == []:
        lstjeux.append("Aucun jeu possédé")
    if lstsucces == []:
        lstsucces.append("Aucun succès reussi")
    if lstnotes == []:
        lstnotes.append("Aucune note laissé")
    return render_template("pageparami.html", jeu = ami, action = 3, liste_jeux = lstjeux, liste_succes = lstsucces, liste_notes = lstnotes)

@app.route("/demande/<ami>/reponse", methods = ['POST'])
def reponse(ami):
    if "login" not in session:
        return redirect(url_for("connexion"))
    oui = request.form.get("oui")
    non = request.form.get("non")
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (session["login"],))
            for result in cur:
                idjoueur = result.idp
            cur.execute("SELECT idp FROM joueur WHERE pseudo = %s", (ami,))
            for result in cur:
                idami = result.idp
            if oui is not None:
                cur.execute("UPDATE amis SET demande = 1 WHERE idp1 = %s AND idp2 = %s;", (idami, idjoueur))
            if non is not None:
                cur.execute("DELETE FROM amis WHERE idp1 = %s AND idp2 = %s;", (idami, idjoueur))
    conn.commit()
    conn.close()
    return redirect(url_for("demanderecu"))


if __name__=='__main__':
    app.run()
