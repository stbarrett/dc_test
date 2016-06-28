from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime, date
from django.core.mail import send_mail
from ursula.models import Tag, Tag_List
from ursula.models import Podcast, PodcastItem
from ursula.models import Type

# -----------------------------------
# Books Landing Page
# -----------------------------------
def index(request):
    #items = Podcast.objects.all().filter(is_active = 1).order_by('title')
    msg = ""
    if request.method == 'POST':
        msg = "<p>Thank you for submitting the Podcast. We will add it to our processing queue and will begin tagging and categorizing it.</p>"
        name = request.REQUEST.get("name", "")
        email = request.REQUEST.get("email", "webmaster@dizcollect.com")
        link = request.REQUEST.get("link", "")
        comment = request.REQUEST.get("comment", "")

        send_mail('Podcast Rec: '+name, name + "\r\n\r\n" + comment, email,
                  [settings.CONTACT_EMAIL], fail_silently=False)


      
    return render_to_response('ursula/podcasts/index.html',
        {#'items': items,
         'nav': 'podcasts',
         'msg': msg,
        }, context_instance=RequestContext(request)
    )
 



# -----------------------------------
# Item Detail
# -----------------------------------
def detail(request, item_slug):
    return HttpResponseRedirect("/podcasts/")
    
    
    user_mystuff = False;
    item = get_object_or_404(Podcast, slug=item_slug, is_active=1)
    
    # get feeds for podcast
    feed_items = PodcastItem.objects.all().filter(podcast = item).order_by('-publication_date')
    
    
    # see if this user has this item, for view
    #if request.user.is_authenticated():
    #    mystuff_item = MyStuff.objects.all().filter(item = item.id, user = request.user.id)
    #    if mystuff_item:
    #        user_mystuff = True
            
         
    return render_to_response(item.type.template,
       {'item': item,
        'feed_items': feed_items,
        'type': 'podcasts',
        'has_mystuff': user_mystuff,
        'nav': 'podcasts',
       }, context_instance=RequestContext(request)
    )