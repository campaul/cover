from cover.providers import google

def get_album_art(artist, album):
    query = ' '.join([artist, album, 'cover art']).replace(' ', '%20')
    return sorted(google.load(artist, album), key=score_album_art).pop()

def score_album_art(image):
    return image.width if image.width == image.height else 0
