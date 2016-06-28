from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from datetime import datetime
from decimal import *
from ursula.models import Podcast, PodcastForm, PodcastItem
from ursula.classes.podcastfeed import PodcastFeed as PodcastFeed
from ursula.classes.podcastfeed import PodcastFeedItem as PodcastFeedItem
import urllib


# meta functions
from ursula.items.meta import do_image_ordinals
from ursula.items.meta import do_tags
from ursula.items.meta import do_people

@login_required
def index(request):
    item_list = Podcast.objects.all().order_by('title')
    return render_to_response('ursula/podcasts/podcasts-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    form = PodcastForm()
    item = ""

    if id != "":
        item = Podcast.objects.get(pk=id)        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = PodcastForm(request.POST)
            if form.is_valid():
                item = form.save()
           
                return HttpResponseRedirect('/podcasts/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PodcastForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                
                return HttpResponseRedirect('/podcasts/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(Podcast, pk=id)
            form = PodcastForm(instance=item)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/podcasts/podcasts-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
        },
        context_instance=RequestContext(request))
    
    




# Create Podcast 
def add_by_feed(request):
    feed = request.REQUEST.get("feed", "")
    if feed:
        # lookup feed and see if it already exists
        item = Podcast.objects.filter(feed_url=feed)
        if item:
            return HttpResponse(-2)
        else :
            podcast = Podcast()
            podcast_feed = PodcastFeed()
            podcast_feed.parse_feed(feed)
            
            podcast.title = podcast_feed.title
            podcast.gen_slug_internal()
            podcast.feed_url = podcast_feed.feed_url
            podcast.itunes_url = podcast_feed.itunes_url
            podcast.url = podcast_feed.link
            podcast.email = podcast_feed.email
            podcast.author = podcast_feed.author
            podcast.is_active = 1
            
            ## do image
            if podcast_feed.thumbnail: 
                try:
                    image_path = podcast.slug + podcast_feed.thumbnail[-4:]
                    podcast.image = settings.PODCAST_MEDIA_IMG + image_path
                    image_path = settings.MEDIA_ROOT + settings.PODCAST_MEDIA_IMG + image_path
                    #podcast.image = settings.PODCAST_MEDIA_IMG + image_path
                
                    f_in = urllib.urlopen(podcast_feed.thumbnail)
                    img = f_in.read()
                    f_out = open(image_path, "w")
                    f_out.write(img)
                    f_out.close()
                except IOError:
                    image_path = podcast.slug + podcast_feed.thumbnail[-4:]
                    podcast.image = settings.PODCAST_MEDIA_IMG + image_path
                    
            podcast.save()
            
            ## do feeds
            for item in podcast_feed.feed_items:
                feed_item = PodcastItem()
                feed_item.guid = item.guid
                feed_item.title = item.title
                feed_item.description = item.description
                feed_item.media_url = item.media_url
                feed_item.media_size = item.media_size
                feed_item.media_type = item.media_type
                feed_item.publication_date = item.publication_date.replace(tzinfo=None) #datetime.strptime(item.publication_date, '%Y-%m-%d %H:%M:%S')
                
                #d = datetime.datetime(*(item.publication_date[0:6]))    
                #feed_item.publication_date = d.strftime('%Y-%m-%d %H:%M:%S')
                
                feed_item.podcast = podcast
                feed_item.is_new = 1
                feed_item.save()
            
            return HttpResponse(podcast.id)
        
    

        