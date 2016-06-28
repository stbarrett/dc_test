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
from ursula.models import Page, PageForm

import urllib


# meta functions


@login_required
def index(request):
    item_list = Page.objects.all().order_by('id')
    return render_to_response('ursula/pages/page-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )

        
@login_required
def edit(request, id=""):
    submit_action = ''
    form = PageForm()
    item = ""

    if id != "":
        item = Page.objects.get(pk=id)        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = PageForm(request.POST)
            if form.is_valid():
                item = form.save()
                return HttpResponseRedirect('/pages/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PageForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                return HttpResponseRedirect('/pages/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(Page, pk=id)
            form = PageForm(instance=item)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/pages/page-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
        },
        context_instance=RequestContext(request))
    
    
    
    
def gen_slug(request):
    new_slug = slugify(request.GET.get('slug', ''))
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Page.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)    
        
        
