import os
from CommandExecutioner import (
    CommandSort,
    CommandPlaylist
)


argument_requirement = {
    'sort':
        ['source', 'destination', 'attribute'],
    'playlist':
        ['source', 'destination', 'attribute', 'playlist_name'],
}

attributes = ('title', 'album', 'artist')


class CommandHandler:
    """
    Pre validation on arugments
    """

    def __init__(self, kwargs):
        # print(kwargs)
        self.run(kwargs)

    def run(self, kwargs):
        kwargs['source'] = os.path.abspath(kwargs['source'])
        kwargs['destination'] = os.path.abspath(kwargs['destination'])
        try:
            self.validate(kwargs)
        except Exception:
            exit(-1)

        mode = kwargs['mode']
        worker = None
        if mode == 'sort':
            worker = CommandSort(kwargs)
        elif mode == 'playlist':
            worker = CommandPlaylist(kwargs)
        else:
            # not likely
            return

        worker.work()

    def validate(self, kwargs):
        requirements = argument_requirement[kwargs['mode']]
        for requirement in requirements:
            if requirement == 'source':
                if not os.path.isdir(kwargs['source']):
                    print(
                        'source:',
                        kwargs['source'],
                        'is not a valid directory')
                    print('directory not exist or is not a directory')
                    raise Exception
            if requirement == 'destination':
                if not os.path.isdir(kwargs['destination']):
                    print(
                        'destination:',
                        kwargs['destination'],
                        'is not a valid directory')
                    print('directory not exist or is not a directory')
                    raise Exception
            elif requirement == 'attribute':
                if kwargs['attribute'] not in attributes:
                    print(
                        'attribute:',
                        kwargs['attribute'],
                        'is not a valid attribute')
                    print('valid attributes are:', attributes)
                    raise Exception
            elif requirement == 'playlist_name':
                if kwargs['playlist'] is None:
                    print("Playlist name must be given")
                    raise Exception
                pl_file = kwargs['destination'] + \
                    '/' + kwargs['playlist'] + '.m3u'
                while True:
                    if not os.path.exists(pl_file):
                        break
                    overwrite = input(
                        'File path {} is existed, overwrite?(y/n) '
                        .format(pl_file))
                    if overwrite in ('y', 'Y'):
                        break
                    newname = input("New file name: ")
                    pl_file = kwargs['destination'] + '/' + newname + '.m3u'
                kwargs['playlist'] = pl_file
