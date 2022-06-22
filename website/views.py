from flask import Blueprint, render_template, request, flash, redirect, current_app
from werkzeug.utils import secure_filename
from .list_dir import get_file_data

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
            #directory = (request.form.get('directory')+ request.form.get('dir')+ "/")
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']
#    data, directory_anzeige = get_file_data(directory)
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


# Files löschen mit bestätigung

# file freigeben



# Verzeichniss wechseln ( Link im namen / Directory) done 50%
#Vrzeichniss oben Anzeigen

#var.startwith("start path")
#var.split(/) für entfernen des letzten ordners für zurück
# env Variable für path

#Upload auf extra Seite
#Umstellen auf Linux ( Pfade ändern etc) done

# Darkmode
# Dateien löschen button
# Dateien löschen mit checkbox
# Ordner löschen
#home button farbe ändern
