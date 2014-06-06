import json
from urllib import request

from cover.image import Image

def load(artist, album):
    query = ' '.join([artist, album, 'cover art']).replace(' ', '%20')
    response = request.urlopen('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + query)
    result = json.loads(response.read().decode(encoding='UTF-8'))

    return [Image(image['width'], image['height'], image['unescapedUrl'])
        for image in result['responseData']['results']]
