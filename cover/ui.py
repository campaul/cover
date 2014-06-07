import io
from urllib import request

from gi.repository import Gtk, GdkPixbuf

def render(artist, album, url):
    # Load Image
    loader = GdkPixbuf.PixbufLoader.new()
    loader.write(request.urlopen(url).read())
    loader.close()

    # Create Pixbuf
    pixbuf = loader.get_pixbuf().scale_simple(640, 640, GdkPixbuf.InterpType.BILINEAR)

    # Setup Window
    window = Gtk.Window()
    window.set_title(' - '.join([artist, album]))
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect('delete-event', Gtk.main_quit)
    window.add(Gtk.Image.new_from_pixbuf(pixbuf))
    window.show_all()

    # Start the GTK loop
    Gtk.main()
