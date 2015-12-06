#!/usr/bin/python
import urllib2
import sys
from urlparse import parse_qs, urlparse

class VideoInfo(object):
    """
    VideoInfo Class hold all information retrieved from www.youtube.com/get_video_info?video_id=
    [VIDEO_ID]
    """
    def __init__(self, video_url):
	
        request_url = 'http://www.youtube.com/get_video_info?video_id='
	video_id = extract_video_id(video_url)
        if video_id != None:
            request_url += video_id
        else :
            sys.exit('Error : Invalid Youtube URL Passing %s' % video_url)
        request = urllib2.Request(request_url)
        try:
            self.video_info = parse_qs(urllib2.urlopen(request).read())
        except urllib2.URLError :
	    print "urllib error"
            sys.exit('Error : Invalid Youtube URL Passing %s' % video_url)

def extract_video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def video_file_urls(videoinfo):
    """
    extract video file's url from VideoInfo object and return them
    """
    if not isinstance(videoinfo, VideoInfo):
        sys.exit('Error : method(video_file_urls) invalid argument passing')
    url_encoded_fmt_stream_map = videoinfo.video_info['url_encoded_fmt_stream_map'][0].split(',')
    entrys = [parse_qs(entry) for entry in url_encoded_fmt_stream_map]
    url_maps = [dict(url=entry['url'][0], type=entry['type']) for entry in entrys]
    return url_maps
  
def get_flux_url(url_str):
    type = 'video/mp4'

    video_info = VideoInfo(url_str)
    video_url_map = video_file_urls(video_info)
    url = ''

    for entry in video_url_map:
        entry_type = entry['type'][0]
        entry_type = entry_type.split(';')[0]
        if entry_type.lower() == type.lower():
            url = entry['url']
            break

    if url == '' :
        sys.exit('Error : Can not find video file\'s url')
    
    return url
