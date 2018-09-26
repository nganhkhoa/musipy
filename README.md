# musipy

A tool to organize your music files.

## Why I create this

I have a very big folder of music files, and searching through files is hard for me, also, the placement was hard to navigate. I want to create a script to move files using tag and organize them.

Then comes a few more use case.

## Usage

```sh
python run.py --help

Usage: run.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  format
  playlist
  sort
```

### Sort

Take all files in `src` arrange them by `attr` and move the files to `dst/attr`. I currently use this to re-arrange my files by album.

### Playlist

Take all files in `src` by `attr` and output a `m3u` playlist file. I use VLC to open `m3u`, a request for another format is always helpful, just ping me a request.

### Format

/// Not implement yet

Rename the files in `src` and follow the format `fmt`.

## Development

### The command line - core

Using 2 foreign library `click` to handle CLI commands; `TinyTag` to parse info from music files. Then the arguments are passed to `CommandHandler` to validate the argument. After that, arguments are taken to `CommandExecutioner` specific class to handle the job.

### The GUI

Hopefully in the future updates. Provide basic GUI to select task, set arguments and make a call to core.

### Testing

Right now just plain testing is being done.

### Coding guidelines

I work on python3 with flake8 and mypy for linting.

### Bug and feature request

Just open a new issue.

## License

I have not yet decide.
