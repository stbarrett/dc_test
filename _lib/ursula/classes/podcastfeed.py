from django.conf import settings
from xml.etree import ElementTree
import time
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

import urllib

"""
    BMS Vidcast:
        http://feeds.feedburner.com/BMSVidcast
    All About the Mouse:
        http://allaboutthemouse.com/themouse.xml
    The Big D Podcast
        http://chreestopher.libsyn.com/rss
    Oakfan:
        http://www.oakfan.com/BDHVodcast.xml
    Inside the Magic
        http://www.distantcreations.com/insidethemagic/inside.xml
    The Magical Definition:
        http://www.magicaldefinition.com/md-disney-podcast.xml
    The Mouselounge:
        http://mouselounge.libsyn.com/rss
    WDWRadio:
        http://www.wdwradio.com/xml/wdwradio.xml?option=com_podcast&feed=RSS2.0&no_html=1
     
"""



NS_MAP = {
          'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
          'media': 'http://search.yahoo.com/mrss/'
}
    
    
class PodcastFeedItem:
    title = ""
    subtitle = ""
    link = ""
    description = ""
    publication_date = ""
    guid = ""
    duration = ""
    media_url = ""
    media_length = ""
    media_type = ""
    
    
class PodcastFeed:
    feed_url = ""
    itunes_url = ""
    title = ""
    subtitle = ""
    description = ""
    author = ""
    email = ""
    thumbnail = ""
    link = ""
    feed_items = []
    
    
    def __init__(self):
        self.feed_items = []


    def parse_feed(self, feed):
        f = urllib.urlopen(feed)
        returned_xml = f.read()
        doc = ElementTree.fromstring(returned_xml)
        
        # uncomment for debugging
        #return returned_xml
        
        # main feed data
        self.feed_url = feed
        self.itunes_url = self.feed_url.replace("http://", "itpc://");
        self.title = doc.find('channel/title').text
        #self.subtitle = doc.find('channel/{'+NS_MAP['itunes']+'}subtitle').text
        self.description = doc.find('channel/description').text
        self.link = doc.find('channel/link').text

        self.email = doc.find('channel/{'+NS_MAP['itunes']+'}owner/{'+NS_MAP['itunes']+'}email').text

        try:
            self.thumbnail = doc.find('channel/image/url').text
        except:
            self.thumbnail = ""
        
        # feed items
        items = doc.findall('channel/item')
        for item in items:
            feed_item = PodcastFeedItem()
            feed_item.title = item.find('title').text
            feed_item.guid = item.find('guid').text
            feed_item.publication_date = parse(item.find('pubDate').text)
            
            try:
                feed_item.author = item.find('{'+NS_MAP['itunes']+'}author').text
            except:
                feed_item.author = ""
                        
            try:
                feed_item.link = item.find('link').text
            except:
                feed_item.link = ""
            try:
                feed_item.description = item.find('description').text
            except:
                feed_item.description = item.find('{'+NS_MAP['itunes']+'}summary').text
            
            try:
                feed_item.media_url = item.find('enclosure').attrib.get('url')
                feed_item.media_size = item.find('enclosure').attrib.get('length')
                feed_item.media_type = item.find('enclosure').attrib.get('type')
            except:
                try:
                    feed_item.media_url = item.find('media').attrib.get('url')
                    feed_item.media_size = item.find('media').attrib.get('fileSize')
                    feed_item.media_type = item.find('media').attrib.get('type')
                except:
                    feed_item.media_url = ""
                    feed_item.media_size = ""
                    feed_item.media_type = ""
            
            self.feed_items.append(feed_item)
            
            
            
            
            
            
            
            
            
            
            
        