import os


def same_name_alert(oldfile, newfile):
    print("Old: {}".format(oldfile))
    print("New: {}".format(newfile))
    print("File existed, overwrite?")
    print("'y' for yes")
    print("'m' to view more data")
    print("'l' to listen to two song")
    while True:
        ans = input("Answer: ")
        if ans == 'y':
            os.rename(oldfile, newfile)
            break
        elif ans == 'm':
            print("Old file data:")
            print("New file data:")
        elif ans == 'l':
            print("Listen to song 1")
            print("Listen to song 2")
        else:
            break
    return
