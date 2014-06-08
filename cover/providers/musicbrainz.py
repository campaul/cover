from urllib import request
from urllib.parse import quote_plus
from urllib.error import HTTPError
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

def get_mbids_from_response(response, artist, album):
    '''Extracts MusicBrainz IDs from response.'''
    tree = ET.parse(response)
    root = tree.getroot()

    # Construct list of recordings
    recordings = []
    for recording in root[0]:
        recordings.append(recording)

    # Extract release ID from list of recordings
    mbids = []
    for recording in recordings:
        if recording.find(with_ns('title')).text == album:
            for each in recording.iter(with_ns('release')):
                mbids.append(each.attrib['id'])
    return mbids

def extract_caa_urls(response):
    '''Extracts image information from JSON CAA response'''
    #TODO: Set up a chain of precedence for type e.g. front --> large --> image
    result = json.loads(response.read().decode(encoding='UTF-8'))
    images = result['images'][0]
    return images['image']

def load(artist, album):
    '''Retrieve album art image for given Artist and Album'''
    mb_search_results = fetch_results(artist, album)
    mbids = get_mbids_from_response(mb_search_results, artist, album)

    # See which of the MusicBrainz IDs have album art
    results = []
    for each in mbids:
        art_query = each

        # Get the response from the album art archive
        try:
            results.append(request.urlopen('http://coverartarchive.org/release/'+art_query))

        except HTTPError:
            # Sometimes there isn't album art for a given release. That's okay.
            continue

    # Extract image URLs from result and return them
    # Workaround for the required image size (none provided by MB/CAA)
    return [Image(500, 500, extract_caa_urls(result))
        for result in results]
