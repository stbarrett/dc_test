from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django import forms
from django.template.defaultfilters import slugify
from ursula.models import Location, LocationForm

@login_required
def index(request):
    location_list = Location.objects.all().order_by('-id')
    return render_to_response('ursula/locations/locations-list.html',
        {'location_list': location_list
        }, context_instance=RequestContext(request)
    )

@login_required
def detail(request, location_slug):
    #Get Item
    location = get_object_or_404(Location, slug=location_slug, is_active=True)
    return render_to_response('ursula/locations/locations-detail.html',
        { 'location': location
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    edit_id = id
    form = LocationForm()
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
          form = LocationForm(request.POST)
          if form.is_valid():
            form.save()
            return HttpResponseRedirect('/locations/') # Redirect after POST
          else:
            submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = LocationForm(request.POST, instance=Location.objects.get(pk=id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/locations/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            location = get_object_or_404(Location, pk=id)
            form = LocationForm(instance=location)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/locations/locations-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': edit_id
        }
      ) 
    
    
def gen_slug(request):
    new_slug = slugify(request.GET.get('slug', ''))
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Location.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)
