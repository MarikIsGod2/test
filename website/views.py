from flask import Blueprint, render_template, request, flash, redirect, current_app, url_for
from werkzeug.utils import secure_filename
from .list_dir import get_file_data
import os
from shutil import rmtree

views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
def home():
    # Überprüfung ob es der erste Aufruf ist (Ob ein POST übergeben wurde)

    if request.method == 'POST':

        if request.form.get('back'):
            directory = request.form.get('back')

            tmp_directory = directory.split("/")
            i = 0
            directory = ""
            while i < len(tmp_directory) - 3:
                i = i + 1
                directory = directory + "/" + tmp_directory[i]
            directory = directory + "/"
            if directory.startswith(current_app.config['DOWNLOAD_DIRECTORY']):
                pass
            else:
                flash("Sie sind am ersten Directory angekommen.", category="error")
                directory = current_app.config['DOWNLOAD_DIRECTORY']
        else:
            print(request.form.get('dir'), "dir", request.form.get('directory'), "directory")

            if request.form.get('dir'):
                directory = (request.form.get('directory') + request.form.get('dir') + "/")
            else:
                directory = (request.form.get('directory'))
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']

    data, directory_anzeige = get_file_data(directory)
    return render_template("home.html", data=data, directory=directory, directory_anzeige=directory_anzeige)

@views.route('/logged_in', methods=['POST', 'GET'])
def logged_in():
    # Überprüfung ob es der erste Aufruf ist (Ob ein POST übergeben wurde)
  #  flash(path)
    if request.method == 'POST':
        if request.form.get('back'):
            directory = request.form.get('back')

            tmp_directory = directory.split("/")
            i = 0
            directory = ""
            while i < len(tmp_directory) - 3:
                i = i + 1
                directory = directory + "/" + tmp_directory[i]
            directory = directory + "/"
            if directory.startswith(current_app.config['DOWNLOAD_DIRECTORY']):
                pass
            else:
                flash("Sie sind am ersten Directory angekommen.", category="error")
                directory = current_app.config['DOWNLOAD_DIRECTORY']
        else:
            print(request.form.get('dir'), "dir", request.form.get('directory'), "directory")

            if request.form.get('dir'):
                directory = (request.form.get('directory') + request.form.get('dir') + "/")
            else:
                directory = (request.form.get('directory'))
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']

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
    print(directory_anzeige)

    return render_template("logged_in.html", data=data, directory=directory, directory_anzeige=directory_anzeige)

@views.route('/confirm_delete', methods=['POST', 'GET'])
def confirm_delete():
    directory = request.form.get('directory')
    if request.method == 'POST':
        if request.form.get('del_file'):
            directory_anzeige = request.form.get('directory_anzeige') + request.form.get('del_file')
            file_name = request.form.get('del_file')
        elif request.form.get('del_dir'):
            directory_anzeige = request.form.get('directory_anzeige') + request.form.get('del_dir')
            file_name = request.form.get('del_dir')
        elif request.form.get('delete_confirmed') == "confirmed":
            if os.path.isfile(directory) == True:
                os.remove(directory)
                flash("Datei wurde erfolgreich gelöscht. " + directory, category="sucess")

            else:
                rmtree(directory)
                flash("Ordner wurde erfolgreich gelöscht. " + directory, category="sucess")

            return redirect(url_for('views.logged_in'))
        else:
            flash("Der löschvorgang wurde abgebrochen.", category="error")
            return redirect(url_for('views.logged_in'))
    else:
        flash("Error: (Keine POST request erhalten.)", category="error")
        return redirect(url_for('views.logged_in'))
    return render_template("confirm_delete.html", directory_anzeige=directory_anzeige, file_name=file_name,  directory=directory)

