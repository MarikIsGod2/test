import os
from humanize import naturalsize
import datetime
from flask import current_app


def get_file_data(directory):
    data = []
    # Looping thru the current directory.
    for a in os.listdir(directory):
        # temporally saving file / directory information.
        modification_date = os.path.getmtime(directory + a)
        file_size = naturalsize(os.stat(directory + a).st_size)
        # Changing UNIX timestamp to readable time.
        value = datetime.datetime.fromtimestamp(modification_date)
        modification_date = value.strftime('%d.%m.%Y %H:%M')

        if os.path.isfile(directory + a) == False:
            # storing filedata in array
            file_size = 0
            row = {"type": "dir", "name": a, "modification_date": modification_date, "file_size": file_size}
            data.append(row)
        #           data = data + [[dir_link_directory, dir_link_name, modification_date, file_size]]

        if os.path.isfile(directory + a) == True:
            # storing directory data in array. File_size gets set to 0 due to the calculation taking too long.
            row = {"type": "file", "name": a, "modification_date": modification_date, "file_size": file_size}
            data.append(row)
    # splitting the directory & removing the not needed part of it.
    tmp_directory = directory.split("/")
    display_directory = ""
    i = 0
    while i < len(tmp_directory) - 2:
        i = i + 1
        if i > current_app.config['LEN_DOWNLOAD_DIRECTORY'] - 1 :
            display_directory = display_directory + "/" + tmp_directory[i]
    display_directory = display_directory + "/"

    return data, display_directory
