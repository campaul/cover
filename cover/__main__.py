import sys
import webbrowser

from cover.cover import get_album_art

artist = sys.argv[1]
album = sys.argv[2]

webbrowser.open_new_tab(get_album_art(artist, album).url)
