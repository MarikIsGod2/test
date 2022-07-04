import os
from shutil import rmtree

from flask import Blueprint, render_template, request, flash, redirect, current_app, url_for
from werkzeug.utils import secure_filename

from .list_dir import get_file_data

views = Blueprint('views', __name__)

#   Redirects to pages /logged_in/<path> & /home/<path>
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

    #   setting Directory to Link in URL
    if displayed_directory != '%%%%':
        directory = current_app.config['DOWNLOAD_DIRECTORY'] + displayed_directory
        # Checking if the path exists or not
        if not os.path.exists(directory):
            flash("Unknown path. Changing to default download path.", category="error")
            directory = current_app.config['DOWNLOAD_DIRECTORY']
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']
    #    executing get-file_data() from list_dir.py it returns the data for the table & the directory to display on top
    data, displayed_directory = get_file_data(directory)

    #    creates variable from the directory before.
    #    Information gets submitted to the HTML page for the "go back" button.
    tmp_directory = displayed_directory.split("/")
    i = 0
    old_directory = ""
    while i < len(tmp_directory) - 3:
        i = i + 1
        old_directory = old_directory + "/" + tmp_directory[i]
    old_directory = old_directory + "/"
    #   if the directory is the default directory change link to "%25%25%25%25 "
    if old_directory == "/":
        old_directory = "%25%25%25%25"

    #   rendering the HTML file & submitting information to it.
    return render_template("home.html", data=data, directory=directory, displayed_directory=displayed_directory,
                           old_directory=old_directory)


@views.route('/logged_in/<path:displayed_directory>', methods=['POST', 'GET'])
def logged_in(displayed_directory):
    # setting Directory to Link in URL
    if displayed_directory != '%%%%' and displayed_directory != '%%%%/':
        directory = current_app.config['DOWNLOAD_DIRECTORY'] + displayed_directory
        # Checking if the path exists or not
        if not os.path.exists(directory):
            flash("Unknown path. Changing to default download path.", category="error")
            directory = current_app.config['DOWNLOAD_DIRECTORY']
    else:
        directory = current_app.config['DOWNLOAD_DIRECTORY']


    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:
            file = request.files['file']

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                if filename != "%25%25%25%25" and filename != "%25%25%25%25/":
                    file.save(directory + filename)
                    flash("Upload sucessfull", category="success")
                else:
                    flash("Download canceled filename not allowed.", category="error")

    #    executing get-file_data() from list_dir.py it returns the data for the table & the directory to display on top
    data, displayed_directory = get_file_data(directory)

    #    creates variable from the directory before.
    tmp_directory = displayed_directory.split("/")
    i = 0
    old_directory = ""
    while i < len(tmp_directory) - 3:
        i = i + 1
        old_directory = old_directory + "/" + tmp_directory[i]

        #   if the directory is the default directory change link to "%25%25%25%25 "
    if old_directory == "":
        old_directory = "%25%25%25%25"

    #   rendering the HTML file & submitting information to it.
    return render_template("logged_in.html", data=data, directory=directory, displayed_directory=displayed_directory,
                           old_directory=old_directory)


@views.route('/confirm_delete', methods=['POST', 'GET'])
def confirm_delete():
    # setting variables for the file to delete.
    directory = request.form.get('directory')
    if request.method == 'POST':
        if request.form.get('del_file'):
            # del_file beeing set means that the user is trying to delete a file.
            displayed_directory = request.form.get('displayed_directory') + request.form.get('del_file')
            file_name = request.form.get('del_file')
        elif request.form.get('del_dir'):
            # del_dir beeing set means that the user is trying to delete a directory.
            displayed_directory = request.form.get('displayed_directory') + request.form.get('del_dir')
            file_name = request.form.get('del_dir')
        elif request.form.get('delete_confirmed') == "confirmed":
            # This gets executed after pressing a button on confirm_delete.html
            if os.path.isfile(directory):
                # Deleting the given file
                os.remove(directory)
                flash("File successfully deleted. " + directory, category="sucess")
            else:
                # Deleting the submitted directory.
                rmtree(directory)
                flash("Directory successfully deleted. ", category="sucess")
            if request.form.get('old_displayed_directory') == "/":
                old_displayed_directory = "%%%%"
            else:
                old_displayed_directory = request.form.get("old_displayed_directory")
            # Sending the user back to the logged_in page.
            # It sends them to the directory they where in before they deleted the file.
            return redirect(url_for('views.logged_in', displayed_directory=old_displayed_directory))

        else:
            # gets executed when pressing the "No" button n confirm_delete.html
            flash("Deletion canceled.", category="error")
            return redirect(url_for('views.logged_in', displayed_directory=request.form.get('old_displayed_directory')))
    else:
        # This should never happen. The confirm_delete page can only be accessed with a POST input.
        flash("Error: (No POST request received.)", category="error")
        return redirect(url_for('views.redirect_home'))
    return render_template("confirm_delete.html", displayed_directory=displayed_directory, file_name=file_name,
                           directory=directory, old_displayed_directory=request.form.get('displayed_directory'))


# Unbekannter Pfad beim download behandeln
# delete url ändern bei sucess