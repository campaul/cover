from urllib import request
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET
import json

from cover.image import Image

def build_query(artist, album):
    '''Constructs valid query for the MusicBrainz GET request'''
    query_part = 'artist:' + quote_plus(artist) + '+recording:' + quote_plus(album)
    earl = 'http://www.musicbrainz.org/ws/2/recording/?query='
    return earl + query_part


def fetch_results(artist, album):
    '''Retrieves results from MusicBrainz query.'''
    return request.urlopen(build_query(artist, album))

def with_ns(tag):
    '''Converts the plain tag to the namespace-having equivalent.'''
    xmlns = 'http://musicbrainz.org/ns/mmd-2.0#'
    return '{'+ xmlns + '}' + tag

def get_mbids_from_response(response):
    '''Extracts MusicBrainz IDs from response.'''
    tree = ET.parse(response)
    root = tree.getroot()

    mbids = []
    for release in root.iter(with_ns('release')):
        mbids.append(release.attrib['id'])

    return mbids

def extract_caa_urls(response):
    '''Extracts image information from JSON CAA response'''

    # Just return one for now
    result = json.loads(response.read().decode(encoding='UTF-8'))
    images = result['images'][0]
    return images['image']


def load(artist, album):
    '''Retrieve album art image for given Artist and Album'''
    mb_search_results = fetch_results(artist, album)
    mbids = get_mbids_from_response(mb_search_results)

    # We take the first MusicBrainz ID search result and cross our fingers
    art_query = mbids[0]
    
    # Get the response from the album art archive
    response = request.urlopen('http://coverartarchive.org/release/'+art_query)

    # Extract image URLs from result and return
    # Workaround for the required image size (none provided by MB/CAA)
    return Image(500, 500, extract_caa_urls(response))

