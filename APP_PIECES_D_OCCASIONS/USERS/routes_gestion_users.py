# routes_gestion_users.py
# OM 2020.04.06 Gestions des "routes" FLASK pour les users.
import re
import pymysql
from flask import render_template, flash, request, redirect, url_for
from APP_PIECES_D_OCCASIONS import obj_mon_application
from APP_PIECES_D_OCCASIONS.DATABASE.erreurs import msg_erreurs, MaBdErreurDoublon, MonErreur, MaBdErreurConnexion
from APP_PIECES_D_OCCASIONS.GENDERS.data_gestion_genders import GestionGenders
from APP_PIECES_D_OCCASIONS.USERS.data_gestion_users import GestionUsers
from APP_PIECES_D_OCCASIONS.DATABASE.connect_db_context_manager import MaBaseDeDonnee


# OM 2020.04.16 Afficher un avertissement sympa...mais contraignant
# Pour la tester http://127.0.0.1:1234/avertissement_sympa_pour_geeks
# @obj_mon_application.route("/avertissement_sympa_pour_geeks")
def avertissement_sympa_pour_geeks():
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("users/AVERTISSEMENT_SYMPA_POUR_LES_GEEKS_users.html")


# OM 2020.04.16 Afficher les users
# Pour la tester http://127.0.0.1:1234/users_afficher
@obj_mon_application.route("/users_afficher")
def users_afficher():
    # OM 2020.04.09 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs du formulaire HTML.
    if request.method == "GET":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_users = GestionUsers()
            # Récupére les données grâce à une requête MySql définie dans la classe GestionUsers()
            # Fichier data_gestion_users.py
            data_users = obj_actions_users.users_afficher_data()
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(" data users", data_users, "type ", type(data_users))

            # OM 2020.04.09 La ligns ci-après permet de donner un sentiment rassurant aux utilisateurs.
            flash("Données users affichées !!", "Success")
        except Exception as erreur:
            print(f"RGF Erreur générale.")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)" fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            # flash(f"RGG Exception {erreur}")
            raise Exception(f"RGF Erreur générale. {erreur}")

    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("users/users_afficher.html", data=data_users)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /users_add ,
# cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template"
# En cas d'erreur on affiche à nouveau la page "users_add.html"
# Pour la tester http://127.0.0.1:1234/users_add
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route("/users_add", methods=['GET', 'POST'])
def users_add():
    # OM 2019.03.25 Pour savoir si les données d'un formulaire sont un affichage
    # ou un envoi de donnée par des champs utilisateurs.
    obj_actions_user = GestionUsers()
    data_user = obj_actions_user.user_afficher_data()
    if request.method == "POST":
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_users = GestionUsers()
            # OM 2020.04.09 Récupère le contenu du champ dans le formulaire HTML "users_add.html"
            firstname_user = request.form['firstname_user_html']
            lastname_user = request.form['lastname_user_html']
            mail = request.form['mail_html']
            phone = request.form['phone_html']
            address = request.form['address_html']
            city = request.form['city_html']
            npa = request.form['npa_html']
            gender = request.form['gender_select']
            date_user = request.form['date_user_html']

            # OM 2019.04.04 On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-z\u00C0-\u00FF])[A-Za-z\u00C0-\u00FF]*['\\- ]?[A-Za-z\u00C0-\u00FF]+$",
                            firstname_user):
                # OM 2019.03.28 Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")
                # On doit afficher à nouveau le formulaire "users_add.html" à cause des erreurs de "claviotage"
                return render_template("users/users_add.html")
            else:

                # Constitution d'un dictionnaire et insertion dans la BD
                valeurs_insertion_dictionnaire = {"value_firstname_user": firstname_user,
                                                  "value_lastname_user": lastname_user,
                                                  "value_mail": mail,
                                                  "value_phone": phone,
                                                  "value_address": address,
                                                  "value_city": city,
                                                  "value_npa": npa,
                                                  "value_gender": gender,
                                                  "value_date_user": date_user}

                obj_actions_users.add_user_data(valeurs_insertion_dictionnaire)

                # OM 2019.03.25 Les 2 lignes ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Données insérées !!", "Sucess")
                print(f"Données insérées !!")
                # On va interpréter la "route" 'users_afficher', car l'utilisateur
                # doit voir le nouveau firstname_user qu'il vient d'insérer.
                return redirect(url_for('users_afficher'))

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        # except pymysql.err.IntegrityError as erreur:
            # OM 2020.04.09 On dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            #raise MaBdErreurDoublon(
                # f"RGG pei {msg_erreurs['ErreurDoublonValue']['message']} et son status {msg_erreurs['ErreurDoublonValue']['status']}")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        #except (pymysql.err.OperationalError,
            #     pymysql.ProgrammingError,
            #     pymysql.InternalError,
            #     TypeError) as erreur:
            # flash(f"Autre erreur {erreur}")
            #raise MonErreur(f"Autre erreur")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts très important de respecter l'ordre.
        except Exception as erreur:
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(
                f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']} et son status {msg_erreurs['ErreurConnexionBD']['status']}")
    # OM 2020.04.07 Envoie la page "HTML" au serveur.
    return render_template("users/users_add.html", data_user=data_user)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /users_edit , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un firstname_user de users par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/users_edit', methods=['POST', 'GET'])
def users_edit():
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "users_afficher.html"
    obj_actions_genders = GestionGenders()
    data_genders = obj_actions_genders.gender_afficher_data()
    if request.method == 'GET':
        try:
            # Récupérer la valeur de "id_user" du formulaire html "users_afficher.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_user"
            # grâce à la variable "id_user_edit_html"
            # <a href="{{ url_for('users_edit', id_user_edit_html=row.id_user) }}">Edit</a>
            id_user_edit = request.values['id_user_edit_html']

            # Pour afficher dans la console la valeur de "id_user_edit", une façon simple de se rassurer,
            # sans utiliser le DEBUGGER
            print(id_user_edit)

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_select_dictionnaire = {"value_id_user": id_user_edit}

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_users = GestionUsers()

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_user = obj_actions_users.edit_user_data(valeur_select_dictionnaire)
            print("dataIdUser ", data_id_user, "type ", type(data_id_user))
            # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
            flash(f"Editer le firstname_user d'un film !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            # On indique un problème, mais on ne dit rien en ce qui concerne la résolution.
            print("Problème avec la BD ! : %s", erreur)
            # OM 2020.04.09 On dérive "Exception" dans "MaBdErreurConnexion" fichier "erreurs.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            raise MaBdErreurConnexion(f"RGG Exception {msg_erreurs['ErreurConnexionBD']['message']}"
                                      f"et son status {msg_erreurs['ErreurConnexionBD']['status']}")

    return render_template("users/users_edit.html",
                           data_genders=data_genders,
                           data=data_id_user)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /users_update , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un firstname_user de users par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/users_update', methods=['POST', 'GET'])
def users_update():
    # DEBUG bon marché : Pour afficher les méthodes et autres de la classe "flask.request"
    print(dir(request))
    # OM 2020.04.07 Les données sont affichées dans un formulaire, l'affichage de la sélection
    # d'une seule ligne choisie par le bouton "edit" dans le formulaire "users_afficher.html"
    # Une fois que l'utilisateur à modifié la valeur du firstname_user alors il va appuyer sur le bouton "UPDATE"
    # donc en "POST"
    obj_actions_genders = GestionGenders()
    data_genders = obj_actions_genders.gender_afficher_data()

    if request.method == 'POST':
        try:
            # DEBUG bon marché : Pour afficher les valeurs contenues dans le formulaire
            print("request.values ", request.values)

            # Récupérer la valeur de "id_user" du formulaire html "users_edit.html"
            # l'utilisateur clique sur le lien "edit" et on récupére la valeur de "id_user"
            # grâce à la variable "id_user_edit_html"
            # <a href="{{ url_for('users_edit', id_user_edit_html=row.id_user) }}">Edit</a>
            id_user_edit = request.values['id_user_edit_html']

            # Récupère le contenu du champ "firstname_user" dans le formulaire HTML "UsersEdit.html"
            firstname_user = request.values['edit_firstname_user_html']
            lastname_user = request.form['edit_lastname_user_html']
            mail = request.form['edit_mail_html']
            phone = request.form['edit_phone_html']
            address = request.form['edit_address_html']
            city = request.form['edit_city_html']
            npa = request.form['edit_npa_html']
            gender = request.form['edit_gender_select']
            date_user = request.form['edit_date_user_html']
            valeur_edit_list = [{'id_user': id_user_edit, 'firstname_user': firstname_user,
                                 'lastname_user': lastname_user, 'mail': mail, 'phone': phone,
                                 'address': address, 'city': city, 'npa': npa, 'fk_gender': gender,
                                 'date_user': date_user}]
            # On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
            # des valeurs avec des caractères qui ne sont pas des lettres.
            # Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
            if not re.match("^([A-Z]|[a-z\u00C0-\u00FF])[A-Za-z\u00C0-\u00FF]*['\\- ]?[A-Za-z\u00C0-\u00FF]+$",
                            firstname_user):
                # En cas d'erreur, conserve la saisie fausse, afin que l'utilisateur constate sa misérable faute
                # Récupère le contenu du champ "firstname_user" dans le formulaire HTML "UsersEdit.html"
                # firstname_user = request.values['name_edit_user_html']
                # Message humiliant à l'attention de l'utilisateur.
                flash(f"Une entrée...incorrecte !! Pas de chiffres, de caractères spéciaux, d'espace à double, "
                      f"de double apostrophe, de double trait union et ne doit pas être vide.", "Danger")

                # On doit afficher à nouveau le formulaire "users_edit.html" à cause des erreurs de "claviotage"
                # Constitution d'une liste pour que le formulaire d'édition "users_edit.html" affiche à nouveau
                # la possibilité de modifier l'entrée
                # Exemple d'une liste : [{'id_user': 13, 'firstname_user': 'philosophique'}]
                valeur_edit_list = [{'id_user': id_user_edit, 'firstname_user': firstname_user,
                                     'lastname_user': lastname_user, 'mail': mail, 'phone': phone,
                                     'address': address, 'city': city, 'npa': npa, 'fk_gender': gender,
                                     'date_user': date_user}]
                # DEBUG bon marché :
                # Pour afficher le contenu et le type de valeurs passées au formulaire "users_edit.html"
                print(valeur_edit_list, "type ..", type(valeur_edit_list))
                return render_template('users/users_edit.html', data=valeur_edit_list)
            else:
                # Constitution d'un dictionnaire et insertion dans la BD
                valeur_update_dictionnaire = {"value_id_user": id_user_edit,
                                              "value_firstname_user": firstname_user,
                                              "value_lastname_user": lastname_user,
                                              "value_mail": mail,
                                              "value_phone": phone,
                                              "value_address": address,
                                              "value_city": city,
                                              "value_npa": npa,
                                              "value_gender": gender,
                                              "value_date_user": date_user}

                # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
                obj_actions_users = GestionUsers()

                # La commande MySql est envoyée à la BD
                data_id_user = obj_actions_users.update_user_data(valeur_update_dictionnaire)
                # DEBUG bon marché :
                print("dataIdUser ", data_id_user, "type ", type(data_id_user))
                # Message ci-après permettent de donner un sentiment rassurant aux utilisateurs.
                flash(f"Editer le firstname_user d'un film !!!")
                # On affiche les users
                return redirect(url_for('users_afficher'))

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:

            print(erreur.args)
            flash(f"problème users update{erreur.args[0]}")
            # En cas de problème, mais surtout en cas de non respect
            # des régles "REGEX" dans le champ "name_edit_user_html" alors on renvoie le formulaire "EDIT"
            return render_template('users/users_edit.html', data=valeur_edit_list)

    return render_template("users/users_update.html", data_genders=data_genders)


# ---------------------------------------------------------------------------------------------------
# OM 2020.04.07 Définition d'une "route" /users_select_delete , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# On change la valeur d'un firstname_user de users par la commande MySql "UPDATE"
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/users_select_delete', methods=['POST', 'GET'])
def users_select_delete():
    if request.method == 'GET':
        try:

            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_users = GestionUsers()
            # OM 2019.04.04 Récupérer la valeur de "idUserDeleteHTML" du formulaire html "UsersDelete.html"
            id_user_delete = request.args.get('id_user_delete_html')

            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_user": id_user_delete}

            # OM 2019.04.02 La commande MySql est envoyée à la BD
            data_id_user = obj_actions_users.delete_select_user_data(valeur_delete_dictionnaire)
            flash(f"EFFACER et c'est terminé pour cette \"POV\" valeur !!!")

        except (Exception,
                pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                pymysql.IntegrityError,
                TypeError) as erreur:
            # Communiquer qu'une erreur est survenue.
            # DEBUG bon marché : Pour afficher un message dans la console.
            print(f"Erreur users_delete {erreur.args[0], erreur.args[1]}")
            # C'est une erreur à signaler à l'utilisateur de cette application WEB.
            flash(f"Erreur users_delete {erreur.args[0], erreur.args[1]}")

    # Envoie la page "HTML" au serveur.
    return render_template('users/users_delete.html', data=data_id_user)


# ---------------------------------------------------------------------------------------------------
# OM 2019.04.02 Définition d'une "route" /usersUpdate , cela va permettre de programmer quelles actions sont réalisées avant de l'envoyer
# au navigateur par la méthode "render_template".
# Permettre à l'utilisateur de modifier un firstname_user, et de filtrer son entrée grâce à des expressions régulières REGEXP
# ---------------------------------------------------------------------------------------------------
@obj_mon_application.route('/users_delete', methods=['POST', 'GET'])
def users_delete():
    # OM 2019.04.02 Pour savoir si les données d'un formulaire sont un affichage ou un envoi de donnée par des champs utilisateurs.
    if request.method == 'POST':
        try:
            # OM 2020.04.09 Objet contenant toutes les méthodes pour gérer (CRUD) les données.
            obj_actions_users = GestionUsers()
            # OM 2019.04.02 Récupérer la valeur de "id_user" du formulaire html "UsersAfficher.html"
            id_user_delete = request.form['id_user_delete_html']
            # Constitution d'un dictionnaire et insertion dans la BD
            valeur_delete_dictionnaire = {"value_id_user": id_user_delete}

            data_users = obj_actions_users.delete_user_data(valeur_delete_dictionnaire)
            # OM 2019.04.02 On va afficher la liste des users des users
            # OM 2019.04.02 Envoie la page "HTML" au serveur. On passe un message d'information dans "message_html"

            # On affiche les users
            return redirect(url_for('users_afficher'))



        except (pymysql.err.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, pymysql.IntegrityError,
                TypeError) as erreur:
            # OM 2020.04.09 Traiter spécifiquement l'erreur MySql 1451
            # Cette erreur 1451, signifie qu'on veut effacer un "firstname_user" de users qui est associé dans "t_users_films".
            if erreur.args[0] == 1451:
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash('IMPOSSIBLE d\'effacer !!! Cette valeur est associée à des users !')
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(
                    f"IMPOSSIBLE d'effacer !! Ce firstname_user est associé à des users dans la t_users_films !!! : {erreur}")
                # Afficher la liste des users des users
                return redirect(url_for('users_afficher'))
            else:
                # Communiquer qu'une autre erreur que la 1062 est survenue.
                # DEBUG bon marché : Pour afficher un message dans la console.
                print(f"Erreur users_delete {erreur.args[0], erreur.args[1]}")
                # C'est une erreur à signaler à l'utilisateur de cette application WEB.
                flash(f"Erreur users_delete {erreur.args[0], erreur.args[1]}")

            # OM 2019.04.02 Envoie la page "HTML" au serveur.
    return render_template('users/users_afficher.html', data=data_users)
