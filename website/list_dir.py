import os
from humanize import naturalsize
import datetime

def get_file_data(directory):
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
    while i < len(tmp_directory) - 2:
        i = i + 1
        if i > 7:
            directory_anzeige = directory_anzeige + "/" + tmp_directory[i]
    directory_anzeige = directory_anzeige + "/"

    return data, directory_anzeige