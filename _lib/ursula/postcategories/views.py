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
from ursula.models import PostCategory, PostCategoryForm, PostCategoryList

import urllib


# meta functions


@login_required
def index(request):
    item_list = PostCategory.objects.all().order_by('-title')
    return render_to_response('ursula/postcategories/postcategories-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )

        
@login_required
def edit(request, id=""):
    submit_action = ''
    form = PostCategoryForm()
    item = ""
    
    if id != "":
        item = PostCategory.objects.get(pk=id)        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = PostCategoryForm(request.POST)
            if form.is_valid():
                item = form.save()
                
                return HttpResponseRedirect('/postcategories/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PostCategoryForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                
                return HttpResponseRedirect('/postcategories/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(PostCategory, pk=id)
            form = PostCategoryForm(instance=item)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/postcategories/postcategories-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
        },  
        context_instance=RequestContext(request))
    
    
def create_ajax(request):
    cat_name = request.POST.get('category_name', '')
    cat_slug = create_slug(cat_name)

    cat = PostCategory()
    cat.title = cat_name
    cat.slug = cat_slug
    cat.is_active = 1
    cat.save()
    
    return HttpResponse(cat.id)
    
    
    
def gen_slug(request):
    return HttpResponse(create_slug(request.GET.get('slug', '')))

def create_slug(slug):
    new_slug = slugify(slug)
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (PostCategory.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return new_slug



        