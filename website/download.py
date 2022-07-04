from flask import Blueprint, send_file, current_app, flash, redirect, url_for
import os

download = Blueprint('download', __name__)

@download.route('/download/<path:path>')
def download_file(path):
    directory = current_app.config['DOWNLOAD_DIRECTORY'] + path
    if os.path.isfile(directory):
        flash("File download successful")
        return send_file(directory, as_attachment=True)
    else:
        flash("Download Link not found. ", category="error")
        return redirect(url_for("views.home", displayed_directory="%%%%"))


@download.route('/download/')
def redirect_download():
    return redirect(url_for("views.home", displayed_directory="%%%%"))

@download.route('/download')
def redirect_download_():
    return redirect(url_for("views.home", displayed_directory="%%%%"))
