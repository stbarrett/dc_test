from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags, escape
from datetime import datetime
from ursula.models import Post, PostCategory, PostCategoryList


# -----------------------------------
# Blog Index
# -----------------------------------
def index(request):
    items = Post.objects.all().filter(is_active = 1).order_by('-publish_date')
    
    return render_to_response('ursula/news/index.html',
        {
         'items': items,
         'type': 'summary',
         'nav': 'news',
        }, context_instance=RequestContext(request)
    )    

# -----------------------------------
# Blog Detail
# -----------------------------------  
def detail(request, year, month, slug):
    item = get_object_or_404(Post, slug=slug, is_active=True)
    
    return render_to_response('ursula/news/detail.html',
        { 'item': item,
         'type': 'detail',
         'nav': 'news',
         'stripped_content': escape(strip_tags(item.content)),
         
        }, context_instance=RequestContext(request)
    )
    
    
# -----------------------------------
# Blog Archive Month
# -----------------------------------  
def archive_month(request, year, month):
    items = Post.objects.all().filter(publish_date__year = year, publish_date__month = month, is_active = 1).order_by('-publish_date')

    return render_to_response('ursula/news/archive.html',
        { 'items': items,
         'type': 'summary',
         'archive_type': 'date',
         'nav': 'news',
         'archive_title': items[0].publish_date, # used for archive page information
        }, context_instance=RequestContext(request)
    )
    
# -----------------------------------
# Blog Archive Category
# -----------------------------------  
def archive_category(request, slug):
    category = get_object_or_404(PostCategory, slug=slug, is_active=True)
    items = Post.objects.all().filter(is_active = 1, postcategorylist__post_category = category).order_by('-publish_date')

    return render_to_response('ursula/news/archive.html',
        { 'items': items,
         'type': 'summary',
         'category': category,
         'archive_type': 'category',
         'nav': 'news',
        }, context_instance=RequestContext(request)
    )
    
# -----------------------------------
# Blog Feed
# -----------------------------------  
def feed(request):
    items = Post.objects.all().filter(is_active = 1).order_by('-publish_date')[:15]

    return render_to_response('ursula/news/feed.html',
        { 'items': items,
        }, context_instance=RequestContext(request)
    ) 
    
    
    