# musipy

## Usage

python musipy.py -s source/dir/ -o output/dir/ -attr attribute -m sort

### -s, --source=

The source directory to scan for files, default to current directory when you run this script

### -o, --output=

The output directory, default to source/dir/output

### -attr, --attribute=

The attribute to use when sort, this could either be 'genre' or 'album'

### -m, --mode=

The mode to use, currently only 'sort' and 'playlist' is able to use. In future update: 

+ [X] 'sort' for sorting files in source/dir by attribute
+ [ ] 'backup' for backing up files structure in a source/dir
+ [ ] 'restore' for restoring files in source/dir to a backup flash
+ [ ] 'rename' for rename multiple files names (Track1.mp3, Track2.mp3... or similar) using a file input of Titles, Artist, Genre, Album, Disk
+ [X] 'playlist' for creating playlist file by any config in source/dir

#### PLay list configuration

When the playlist mode is chosen, you will need to provide the name of the output file through `--playlistname`. The place of the playlist will be at sourcedir, which is 'current working directory' by default.

## Why I create this

I have a very big folder of files, and searching through files is hard for me, also, the structure when I first place them in is hard to navigate. I want to create a script to move files using tag and organize them. And create a playlist with the options I prefer.

## When will I deploy?

I do not know, I just create for myself. Hosting on Git is to keep my project organized, and hope to get some collaborators.

## License

I have not yet decide.
