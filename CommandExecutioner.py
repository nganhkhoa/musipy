from tinytag import TinyTag
import os
# from functools import reduce
import pprint
from binascii import b2a_hex


class CommandExecutioner:
    def __init__(self, kwargs):
        self.options = kwargs

    def work(self):
        pass

    def scan(self):
        """
        set self.files to be a list of files
        element in list are in full path
        """
        self.files = []

        for root, dirs, files in os.walk(self.source):
            print("[+] Scan {}".format(root))
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for folder in dirs:
                folder = os.path.join(root, folder)
            for f in files:
                self.files.append(os.path.join(root, f))

    def _scan(self):
        """
        deprecated
        """
        # files to work on
        # scan all files and store whole path on here
        self.files = []

        folder_queue = [self.source]
        home_path_len = len(folder_queue[0])

        while (len(folder_queue) > 0):
            current_folder = folder_queue[0]
            folder_queue = folder_queue[1:]

            if len(current_folder[home_path_len:]) == 0:
                print("[+] Scan /")
            else:
                print("[+] Scan {}".format(current_folder[home_path_len:]))

            self.files += list(
                filter(
                    lambda x: os.path.isfile(x),
                    os.listdir(current_folder))
            )
            for f in self.files:
                f = current_folder + '/' + f

            folders = list(
                filter(
                    lambda x:
                        os.path.isdir(x) and x[0] != '.',
                    os.listdir(current_folder)))

            for folder in folders:
                folder_queue.append(current_folder + '/' + folder)

    def makedict(self):
        """
        from list of files
        to dictionary of file by attribute specified
        """
        self.data = {}
        for f in self.files:
            try:
                tag = TinyTag.get(f)
            except LookupError:
                # not a music file
                continue
            except BaseException:
                print("Cannot get tag from file --> Skip\n\t{}".format(f))
                continue
            tag = getattr(tag, self.attribute)
            if tag in self.data:
                self.data[tag].append(f)
            else:
                self.data[tag] = []
                self.data[tag].append(f)


class CommandSort(CommandExecutioner):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.source = kwargs['source']
        self.destination = kwargs['destination']
        self.attribute = kwargs['attribute']

    def work(self):
        self.scan()
        self.makedict()
        pprint.pprint(self.data)
        self.sort()

    def sort(self):
        # key is now the name of the folder
        for folder_name, tracks in self.data.items():
            # print(folder_name)
            # continue

            if folder_name is None:
                # file attribute is None
                folder = "Undefined"
            elif folder_name == '':
                # file attribute is empty string
                folder = "Undefined"
            else:
                folder = folder_name

            # because folder is taken from file tags
            # some tags could have '/' in it
            # which is not acceptable as a file name in linux
            # folder = folder.replace('/', '-')

            # print(self.destination)
            folder = self.destination + '/' + folder
            if not os.path.exists(folder):
                os.makedirs(folder)

            print("========================================")
            print("Album: {}".format(folder_name))
            print("Folder: {}".format(folder))
            # continue
            for track in tracks:
                new_file = folder + '/' + os.path.basename(track)
                if track == new_file:
                    # after sort, stay the same
                    continue
                if os.path.exists(new_file):
                    pass
                else:
                    print("[+] Replace\n\t{}\n\t{}".format(track, new_file))
                    # uncomment when you are ready
                    # os.rename(track, new_file)
                    pass
        return


class CommandPlaylist(CommandExecutioner):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.source = kwargs['source']
        self.destination = kwargs['destination']
        self.attribute = kwargs['attribute']
        self.playlist = kwargs['playlist']

    def work(self):
        self.scan()
        self.makedict()
        print("Create playlist {}".format(self.playlist))

        playlist = open(self.playlist, 'w')
        playlist.write('#EXTM3U\n')

        for key, musics in self.data.items():
            for music in musics:
                tag = TinyTag.get(music)
                if tag.artist is None:
                    tag.artist = ''
                if tag.title is None:
                    tag.title = ''
                tag.duration = int(tag.duration)

                # write comment
                playlist.write('#EXTINF:{},{} - {}\n'
                               .format(
                                   tag.duration,
                                   tag.artist,
                                   tag.title))

                # write file direction
                music = encode_to_hex(music)
                playlist.write('file://{}\n'.format(music))

        print("{} created".format(self.playlist))


def encode_to_hex(string):
    """
    change special char to hex
    """
    chars = list(string)
    for i in range(len(string)):
        hex_c = ord(chars[i])
        if hex_c >= ord('!') and hex_c <= ord('~'):
            # skip ascii characters
            # be aware of special ascii!!!
            continue
        elif hex_c == ord(' '):
            chars[i] = '%20'
        else:
            # not ascii change to hex
            u = b2a_hex(chars[i].encode('utf-8')).decode('utf-8')
            u = list(u)
            for j in range(len(u)):
                u[j] = u[j].upper()
                if j % 2 != 0:
                    continue
                u[j] = '%' + u[j]
            chars[i] = "".join(u)

    string = "".join(chars)
    return string
