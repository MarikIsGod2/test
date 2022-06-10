import datetime
import os
from flask import Blueprint, render_template, request, flash
from humanize import naturalsize

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
            if directory.startswith("/mnt/c/Users/Support/Desktop/"):
                pass
            else:
                flash("Sie sind am ersten Directory angekommen.", category="error")
                directory = "/mnt/c/Users/Support/Desktop/"
        else:
            directory = (request.form.get('directory')+ request.form.get('dir')+ "/")
    else:
        directory = "/mnt/c/Users/Support/Desktop/"
    data = []
#    directory = r"C:\Users\Support\Desktop\\"

    for a in os.listdir(directory):
        modification_date = os.path.getmtime(directory + a)
        file_size = naturalsize(os.stat(directory + a).st_size)

        value = datetime.datetime.fromtimestamp(modification_date)
        modification_date = value.strftime('%d.%m.%Y %H:%M')

        if os.path.isfile(directory + a) == False:
            size = 0
            file_size = 0
            row = {"type": "dir", "name": a, "modification_date": modification_date, "file_size": file_size}
            data.append(row)
#           data = data + [[dir_link_directory, dir_link_name, modification_date, file_size]]

        if os.path.isfile(directory + a) == True:
            row = {"type": "file", "name": a, "modification_date": modification_date, "file_size": file_size}
            data.append(row)
    tmp_directory = directory.split("/")
    directory_anzeige = ""
    i = 0
    while i  < len(tmp_directory) - 2:
        i = i + 1
        if i > 5:
            directory_anzeige = directory_anzeige + "/" + tmp_directory[i]
    directory_anzeige = directory_anzeige + "/"
    return render_template("home.html", data=data, directory=directory, directory_anzeige=directory_anzeige)

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