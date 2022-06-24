import os
from shutil import rmtree

from flask import Blueprint, render_template, request, flash, redirect, current_app, url_for
from werkzeug.utils import secure_filename

from .list_dir import get_file_data

views = Blueprint('views', __name__)


@views.route('/')
def redirect_slash():
    return redirect(url_for('views.home', displayed_directory="%%%%"))


@views.route('/home')
def redirect_home():
    return redirect(url_for('views.home', displayed_directory="%%%%"))


@views.route('/logged_in')
def redirect_logged_in():
    return redirect(url_for('views.logged_in', displayed_directory="%%%%"))


@views.route('/logged_in/')
def redirect_logged_in_slash():
    return redirect(url_for('views.logged_in', displayed_directory="%%%%"))


@views.route('/home/<path:displayed_directory>', methods=['POST', 'GET'])
def home(displayed_directory):
    if displayed_directory != '%%%%':
        directory = current_app.config['DOWNLOAD_DIRECTORY'] + displayed_directory
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']
        if not os.path.exists(directory):
            flash("Unknown path. Changing to default download path.", category="error")
            directory = current_app.config['DOWNLOAD_DIRECTORY']

    if request.method == 'POST':
        if request.form.get('back'):
            directory = current_app.config['DOWNLOAD_DIRECTORY'] + displayed_directory
    print(directory)
    data, displayed_directory = get_file_data(directory)
    tmp_directory = displayed_directory.split("/")
    i = 0
    old_directory = ""
    while i < len(tmp_directory) - 3:
        i = i + 1
        old_directory = old_directory + "/" + tmp_directory[i]
    old_directory = old_directory + "/"
    if old_directory == "/":
        old_directory = "%%%%"
    return render_template("home.html", data=data, directory=directory, displayed_directory=displayed_directory,
                           old_directory=old_directory)


@views.route('/logged_in/<path:displayed_directory>', methods=['POST', 'GET'])
def logged_in(displayed_directory):
    # Überprüfung ob es der erste Aufruf ist (Ob ein POST übergeben wurde)
    if displayed_directory != '%%%%' and displayed_directory != '%%%%/':
        directory = current_app.config['DOWNLOAD_DIRECTORY'] + displayed_directory
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']
        if not os.path.exists(directory):
            flash("Unknown path. Changing to default download path.", category="error")
            directory = current_app.config['DOWNLOAD_DIRECTORY']

    if request.method == 'POST':
        if request.form.get('back'):
            directory = current_app.config['DOWNLOAD_DIRECTORY'] + displayed_directory

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
                file.save(directory + filename)
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
    print(request.form.get('displayed_directory'))
    directory = request.form.get('directory')
    if request.method == 'POST':
        if request.form.get('del_file'):
            directory_anzeige = request.form.get('displayed_directory') + request.form.get('del_file')
            file_name = request.form.get('del_file')
        elif request.form.get('del_dir'):
            directory_anzeige = request.form.get('displayed_directory') + request.form.get('del_dir')
            file_name = request.form.get('del_dir')
        elif request.form.get('delete_confirmed') == "confirmed":
            print("Directory", directory, "old_directory_anzeige", request.form.get('displayed_directory'))
            if os.path.isfile(directory):
                os.remove(directory)
                flash("File successfully deleted. " + directory, category="sucess")

            else:
                rmtree(directory)
                flash("Directory successfully deleted. " + directory, category="sucess")
            if request.form.get('old_directory_anzeige') == "/":
                old_directory_anzeige = "%%%%"
            else:
                old_directory_anzeige = request.form.get("old_directory_anzeige")
            print(url_for('views.logged_in', displayed_directory=old_directory_anzeige), "AUSGABE URL ")
            return redirect(url_for('views.logged_in', displayed_directory=old_directory_anzeige))

        else:
            flash("Deletion canceled.", category="error")
            return redirect(url_for('views.logged_in', displayed_directory=request.form.get('old_directory_anzeige')))
    else:
        flash("Error: (No POST request received.)", category="error")
        return redirect(url_for('views.redirect_home'))
    return render_template("confirm_delete.html", directory_anzeige=directory_anzeige, file_name=file_name,
                           directory=directory, old_directory_anzeige=request.form.get('displayed_directory'))
