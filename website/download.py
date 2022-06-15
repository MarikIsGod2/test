from flask import Blueprint, render_template, request, flash, redirect, send_file, current_app

download = Blueprint('download', __name__)

@download.route('/download/<path:path>')
def download_file(path):
    print(path)
    directory = current_app.config['DOWNLOAD_DIRECTORY'] + path
    return send_file(directory, as_attachment=True)