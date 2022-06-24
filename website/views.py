from flask import Blueprint, render_template, request, flash, redirect, current_app, url_for
from werkzeug.utils import secure_filename
from .list_dir import get_file_data
import os
from shutil import rmtree

views = Blueprint('views', __name__)


@views.route('/')
def redirect_slash():
    return redirect(url_for('views.home', anzeige_directory="%%%%"))


@views.route('/home')
def redirect_home():
    return redirect(url_for('views.home', anzeige_directory="%%%%"))


@views.route('/logged_in')
def redirect_logged_in():
    return redirect(url_for('views.logged_in', anzeige_directory="%%%%"))


@views.route('/home/<path:anzeige_directory>', methods=['POST', 'GET'])
def home(anzeige_directory):
    if anzeige_directory != '%%%%':
        directory = current_app.config['DOWNLOAD_DIRECTORY'] + anzeige_directory
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']
        if not os.path.exists(directory):
            flash("Unknown path. Changing to default download path.", category="error")
            directory = current_app.config['DOWNLOAD_DIRECTORY']

    if request.method == 'POST':
        if request.form.get('back'):
            directory = current_app.config['DOWNLOAD_DIRECTORY'] + anzeige_directory
    print(directory)
    data, directory_anzeige = get_file_data(directory)
    tmp_directory = directory_anzeige.split("/")
    i = 0
    old_directory = ""
    while i < len(tmp_directory) - 3:
        i = i + 1
        old_directory = old_directory + "/" + tmp_directory[i]
    old_directory = old_directory + "/"
    if old_directory == "/":
        old_directory = "%%%%"
    return render_template("home.html", data=data, directory=directory, directory_anzeige=directory_anzeige,
                           old_directory=old_directory)


@views.route('/logged_in/<path:anzeige_directory>', methods=['POST', 'GET'])
def logged_in(anzeige_directory):
    # Überprüfung ob es der erste Aufruf ist (Ob ein POST übergeben wurde)
    if anzeige_directory != '%%%%' and anzeige_directory != '%%%%/':
        directory = current_app.config['DOWNLOAD_DIRECTORY'] + anzeige_directory
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']
        if not os.path.exists(directory):
            flash("Unknown path. Changing to default download path.", category="error")
            directory = current_app.config['DOWNLOAD_DIRECTORY']

    if request.method == 'POST':
        if request.form.get('back'):
            directory = current_app.config['DOWNLOAD_DIRECTORY'] + anzeige_directory

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                print(directory + filename, "[DEBUG] AUSGABE PATH FILE")
                file.save(directory + filename)
                flash("Upload sucessfull", category="sucess")
    data, directory_anzeige = get_file_data(directory)
    tmp_directory = directory_anzeige.split("/")
    i = 0
    old_directory = ""
    while i < len(tmp_directory) - 3:
        i = i + 1
        old_directory = old_directory + "/" + tmp_directory[i]
    if old_directory == "":
        old_directory = "%%%%"
    return render_template("logged_in.html", data=data, directory=directory, directory_anzeige=directory_anzeige,
                           old_directory=old_directory)


@views.route('/confirm_delete', methods=['POST', 'GET'])
def confirm_delete():
    print(request.form.get('directory_anzeige'))
    directory = request.form.get('directory')
    if request.method == 'POST':
        if request.form.get('del_file'):
            directory_anzeige = request.form.get('directory_anzeige') + request.form.get('del_file')
            file_name = request.form.get('del_file')
        elif request.form.get('del_dir'):
            directory_anzeige = request.form.get('directory_anzeige') + request.form.get('del_dir')
            file_name = request.form.get('del_dir')
        elif request.form.get('delete_confirmed') == "confirmed":
            print("Directory", directory, "old_directory_anzeige", request.form.get('directory_anzeige'))
            if os.path.isfile(directory):
                os.remove(directory)
                flash("Datei wurde erfolgreich gelöscht. " + directory, category="sucess")

            else:
                rmtree(directory)
                flash("Ordner wurde erfolgreich gelöscht. " + directory, category="sucess")
            if request.form.get('old_directory_anzeige') == "/":
                old_directory_anzeige = "%%%%"
            else:
                old_directory_anzeige = request.form.get("old_directory_anzeige")
            print(url_for('views.logged_in', anzeige_directory=old_directory_anzeige), "AUSGABE URL ")
            print(request.form.get('old_directory_anzeige'), "----------------------------")
            return redirect(url_for('views.logged_in', anzeige_directory=old_directory_anzeige))

        else:
            flash("Der löschvorgang wurde abgebrochen.", category="error")
            return redirect(url_for('views.logged_in', anzeige_directory=request.form.get('old_directory_anzeige')))
    else:
        flash("Error: (Keine POST request erhalten.)", category="error")
        return redirect(url_for('views.redirect_home'))
    return render_template("confirm_delete.html", directory_anzeige=directory_anzeige, file_name=file_name,
                           directory=directory, old_directory_anzeige=request.form.get('directory_anzeige'))

# Dateinahme auf Sonderzeichen & äüö überprüfen
# Englisch
# directory root flash Meldung
