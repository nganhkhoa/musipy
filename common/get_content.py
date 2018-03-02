import os


def get_content(source):
    files = []
    folders = []

    for f in os.listdir(source):
        if os.path.isfile(os.path.join(source, f)):
            files.append(f)
        else:
            folders.append(f)
    return files, folders
