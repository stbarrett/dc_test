from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from ursula.classes.podcastfeed import PodcastFeed as PodcastFeed
import feedparser


#http://feeds2.feedburner.com/Wedwayradio5
    
def index(request):
    feed = request.REQUEST.get("feed", "")
    podcast = PodcastFeed()
    podcast.parse_feed(feed)
    
    # comment above and uncomment below for debug
    #return HttpResponse(podcast.parse_feed(feed))
    

    #return HttpResponse(book.raw_xml)
    return render_to_response('pod/index.html',
        {'item': podcast,
        }, context_instance=RequestContext(request)
    )
    
    
    
    
    