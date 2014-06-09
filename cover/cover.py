from cover.providers import google
from cover.providers import musicbrainz

def get_album_art(artist, album):
    musicbrainz_results = get_album_art_from_provider(artist, album, musicbrainz)
    google_results = get_album_art_from_provider(artist, album, google)

    return (musicbrainz_results + google_results).pop()

def get_album_art_from_provider(artist, album, provider):
    return sorted(provider.load(artist, album)[:3], key=score_album_art)

def score_album_art(image):
    return image.width if image.width == image.height else 0
