from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from datetime import *
from pytz import *
from decimal import *
from ursula.models import Post, PostForm, PostCategoryList

import urllib


# meta functions


@login_required
def index(request):
    item_list = Post.objects.all().order_by('id')
    return render_to_response('ursula/blog/blog-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )

        
@login_required
def edit(request, id=""):
    submit_action = ''
    form = PostForm()
    item = ""
    cat_ids = request.POST.getlist('cat_active_list')
    pacific = timezone(settings.TZ)

    d_now = datetime.now(pacific)
    d_month = d_now.month
    d_day = d_now.day
    d_year = d_now.year
    d_hour = d_now.hour
    d_min = d_now.minute
    if d_min < 10:
        d_min = "0"+str(d_min)



    if id != "":
        item = Post.objects.get(pk=id)        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = PostForm(request.POST)
            if form.is_valid():
                item = form.save()
           
                do_cats(cat_ids, item.id)
           
                return HttpResponseRedirect('/posts/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PostForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                
                do_cats(cat_ids, item.id)
                
                return HttpResponseRedirect('/posts/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(Post, pk=id)
            form = PostForm(instance=item)
            d_month = item.publish_date.strftime("%m")
            d_day = item.publish_date.strftime("%d")
            d_year = item.publish_date.strftime("%Y")
            d_hour = item.publish_date.strftime("%H")
            d_min = item.publish_date.strftime("%M")

        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/blog/blog-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
          'month': d_month,
          'day': d_day,
          'year': d_year,
          'hour': d_hour,
          'minute': d_min,
        },
        context_instance=RequestContext(request))
    
    
    
    
def gen_slug(request):
    new_slug = slugify(request.GET.get('slug', ''))
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Post.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)    
        
        
        
# -----------------------------------
# Process categories for an item
# -----------------------------------
def do_cats(cat_ids, post_id):
   # mark each tag for post_id as inactive first
    cat_list = PostCategoryList.objects.filter(post = post_id)
    for cat_list_item in cat_list:
        cat_list_item.is_active = 0
        cat_list_item.save()
        
    # mark each incoming tag as active
    # first check to see if it exists.
    for id in cat_ids:
        id_set = 0
        for cat_list_item in cat_list:
            if str(cat_list_item.post_category_id) == id:
                cat_list_item.is_active = 1
                cat_list_item.save()
                id_set = 1
                break
            
        if id_set == 0:
            new_item = PostCategoryList()
            new_item.post_category_id = id
            new_item.post_id = post_id
            new_item.is_active = 1
            new_item.save()
                
    return 1        