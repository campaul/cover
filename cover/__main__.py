import sys

from cover.cover import get_album_art
from cover.ui import render

artist = sys.argv[1]
album = sys.argv[2]

render(artist, album, get_album_art(artist, album).url)
