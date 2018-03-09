import os
from parser import Parser
from common import same_name_alert, get_content
from tinytag import TinyTag
from binascii import b2a_hex


class musipy:
    def __init__(self):
        # prepare data
        self.data = {}
        self.parser = Parser()

        # run
        self.run()

    def run(self):
        if self.parser.mode == 'sort':
            self.collect()
            self.move_files()
        elif self.parser.mode == 'playlist':
            self.collect()
            self.playlist()
        else:
            pass
        return

    # sort files bases on attribute
    def sort(self, f, tag):
        # get attribute from tag
        # using self.attr
        tag = getattr(tag, self.parser.attr)
        if tag in self.data:
            self.data[tag].append(f)
        else:
            self.data[tag] = []
            self.data[tag].append(f)
        return

    # move files to new destination based on attribute
    def move_files(self):
        for folder, tracks in self.data.items():

            if folder is None:
                folder = "Undefined"
            if not folder:
                folder = "Undefined"

            new_folder = self.parser.output + '/' + folder
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

            print("Folder: {}".format(folder))
            moved_files = 0
            total_files = len(tracks)
            for track in tracks:
                moved_files += 1
                percent = int(moved_files / total_files * 100)
                print("Processing ... {:3d}%".format(percent), end='\r')

                new_file = new_folder + '/' + os.path.basename(track)
                if track == new_file:
                    # after sort, stay the same
                    continue
                if os.path.exists(new_file):
                    same_name_alert(track, new_file)
                else:
                    os.rename(track, new_file)
            print("")
        return

    def playlist(self):
        print("Create playlist name {}".format(self.parser.playlistname))
        pl_file = self.parser.source + '/' + self.parser.playlistname + '.m3u'
        mode = 'w'

        while os.path.exists(pl_file):
            rewrite = input('Playlist existed, rewrite?(y/n) ')
            if rewrite == 'y':
                break
            newname = input("New file name: ")
            pl_file = self.parser.source + '/' + newname + '.m3u'
            # return

        playlist = open(pl_file, mode)
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
                               .format(tag.duration, tag.artist, tag.title))
                # change special char to hex
                chars = list(music)
                for i in range(len(music)):
                    hex_c = ord(chars[i])
                    if hex_c >= ord('!') and hex_c <= ord('~'):
                        # if in range of ascii characters
                        continue
                    elif hex_c == ord(' '):
                        chars[i] = '%20'
                    else:
                        u = b2a_hex(chars[i].encode('utf-8')).decode('utf-8')
                        u = list(u)
                        for j in range(len(u)):
                            u[j] = u[j].upper()
                            if j % 2 != 0:
                                continue
                            u[j] = '%' + u[j]
                        chars[i] = "".join(u)
                        # print("Cannot find this character: 0x{}"
                        #       .format(hex(hex_c)))
                        # exit(-1)

                music = "".join(chars)
                # write file direction
                playlist.write('file://{}\n'.format(music))

        print("{} created".format(pl_file))
        return

    # collect all files and store in self.data
    def collect(self):
        folder_queue = [self.parser.source]
        home_path_len = len(folder_queue[0])

        while (len(folder_queue) > 0):

            current_folder = folder_queue[0]
            folder_queue = folder_queue[1:]

            if len(current_folder[home_path_len:]) == 0:
                print("[+] Scan /")
            else:
                print("[+] Scan {}".format(current_folder[home_path_len:]))

            files, folders = get_content(current_folder)

            # skip folder named '.folder'
            # generate full path
            for folder in folders:
                if folder[0] != '.':
                    full_path = current_folder + '/' + folder
                    folder_queue.append(full_path)

            # work with files
            for f in files:
                try:
                    fp = current_folder + '/' + f  # full path to file
                    tag = TinyTag.get(fp)
                except LookupError:
                    continue
                except:
                    print("Cannot get tag from file --> Skip\n\t{}".format(fp))
                    continue

                self.sort(fp, tag)


if __name__ == "__main__":
    muse = musipy()
