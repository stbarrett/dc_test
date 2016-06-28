from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from datetime import datetime
from decimal import *
from ursula.models import Podcast, PodcastItemForm, PodcastItem
from ursula.classes.podcastfeed import PodcastFeed as PodcastFeed
from ursula.classes.podcastfeed import PodcastFeedItem as PodcastFeedItem
from ursula.models import Tag, Tag_List
import urllib


@login_required
def index(request):
    f = request.GET.get('f', '')
    if f:
        item_list = PodcastItem.objects.all().filter(podcast__id__exact = f).order_by('-is_new', 'id')
    else:
        item_list = PodcastItem.objects.all().order_by('-is_new', 'id')
    return render_to_response('ursula/podcastfeeds/podcastfeeds-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    form = PodcastItemForm()
    item = ""
    tag_ids = request.POST.getlist('tag_active_list')
    if id != "":
        item = PodcastItem.objects.get(pk=id)
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = PodcastItemForm(request.POST)
            if form.is_valid():
                item = form.save()
           
                return HttpResponseRedirect('/podcasts/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PodcastItemForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                
                # do tags
                do_tags(tag_ids, item.id)
                         
                return HttpResponseRedirect('/podcastfeeds/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(PodcastItem, pk=id)
            form = PodcastItemForm(instance=item)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/podcastfeeds/podcastfeed-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
        },
        context_instance=RequestContext(request))
    
    
    
# -----------------------------------
# Process tags for a podcast item
# -----------------------------------
def do_tags(tag_ids, item_id):
   # mark each tag for item_id as inactive first
    tag_list = Tag_List.objects.filter(podcastitem = item_id)
    for tag_list_item in tag_list:
        tag_list_item.is_active = 0
        tag_list_item.save()
        

    # mark each incoming tag as active
    # first check to see if it exists.
    for id in tag_ids:
        id_set = 0
        for tag_list_item in tag_list:
            if str(tag_list_item.tag_id) == id:
                tag_list_item.is_active = 1
                tag_list_item.save()
                id_set = 1
                break
            
        if id_set == 0:
            new_item = Tag_List()
            new_item.tag_id = id
            new_item.podcastitem_id = item_id
            new_item.is_active = 1
            new_item.save()
                
    return 1
    
        