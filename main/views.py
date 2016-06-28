from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ursula.models import Item, ItemForm
from ursula.models import Tag, TagForm, Tag_List
from ursula.models import Post
from ursula.models import Type
from ursula.models import Ebay_Item
from django.views.decorators.cache import cache_page
import time

from djangosphinx.models import SphinxSearch

def index(request):
    
    # get latest posts
    #news = Post.objects.all().filter(is_active = 1).order_by('-publish_date')[:5]
    
    #qs = Item.search.query("Pixar")
    
     
    #pins = Item.objects.all().filter(type=1).order_by('-release_date', '-id')[:15]
    pins = Item.objects.all().filter(is_active = 1, type=1).order_by("-release_date")[:10]
    #pins = qs.filter(is_active = 1, type_id = 1).order_by('-release_date', '@weight')[0:15]
    books = Item.objects.all().filter(type=2, is_active = 1).order_by("?")[:8]
    #books = qs.filter(is_active = 1, type_id = 2).order_by('-release_date')[0:8]
    vinylmations = Item.objects.all().filter(is_active = 1, type=5, tag_list__is_active=1).order_by("?")[:10]
    ebay_list = Ebay_Item.objects.all().filter(is_active = 1, needs_admin = 0, end_time__gte = datetime.now()).order_by("?")[:5]
    return render_to_response('index.html',
        {
         'pins': list(pins),
         'pins_title': 'The Latest',
         'pins_more_url': '/collectibles/pins/',
         'books': books,
         'vinylmations': vinylmations,
         'books_title': "",
         'ebay_list': ebay_list,
         'nav': 'home',
        }, context_instance=RequestContext(request)
    )


## Generate our own sitemap
def sitemap(request):
    # get types
    types = Type.objects.all().filter(type = 'collectible')
    items = Item.objects.all().filter(is_active = 1)
    
    return render_to_response('sitemap.html',
        {
         'types': types,
         'items': items
        }, context_instance=RequestContext(request)
    )    
    
    
