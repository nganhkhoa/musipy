import os
import getopt
import sys


class Parser():
    def __init__(self):
        argv = sys.argv[1:]
        self.source = None
        self.output = None
        self.attr = None
        self.mode = None

        self.playlistname = None

        try:
            opts, args = getopt.getopt(
                argv, 'hs:o:a:m:pln:',
                ['source=', 'output=', 'attribute=', 'mode=', 'playlistname='])

        except getopt.GetoptError:
            print('')
            exit(0)

        for opt, arg in opts:
            if opt == '-h':
                print("Help")
                exit(0)
            elif opt in ('-s', '--source'):
                self.source = arg
            elif opt in ('-o', '--output'):
                self.output = arg
            elif opt in ('-a', '--attribute'):
                self.attr = arg
            elif opt in ('-m', '--mode'):
                self.mode = arg
            elif opt in ('-pl', '--playlistname'):
                self.playlistname = arg
            else:
                print("Unknown flag {} {}".format(opt, arg))

        if self.source is None:
            self.source = os.getcwd()
        if self.output is None:
            self.output = self.source + '/output'
        if self.attr is None:
            self.attr = 'album'
        if self.mode is None:
            self.mode = 'sort'

        if self.mode == 'playlist' and self.playlistname is None:
            print("No play list name")
            exit()


if __name__ == '__main__':
    p = Parser()
    print(p.source)
    print(p.output)
    print(p.attr)
    print(p.mode)
