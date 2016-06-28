from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django import forms
from django.template.defaultfilters import slugify
from ursula.models import Publisher, PublisherForm

@login_required
def index(request):
    publisher_list = Publisher.objects.all().order_by('name')
    return render_to_response('ursula/publishers/publishers-list.html',
        {'publisher_list': publisher_list
        }, context_instance=RequestContext(request)
    )

@login_required
def detail(request, person_slug):
    #Get Item
    person = get_object_or_404(Publisher, slug=person_slug, is_active=True)
    return render_to_response('ursula/publishers/publishers-detail.html',
        { 'person': person
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    edit_id = id
    form = PublisherForm()
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
          form = PublisherForm(request.POST)
          if form.is_valid():
            form.save()
            return HttpResponseRedirect('/publishers/') # Redirect after POST
          else:
            submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PublisherForm(request.POST, instance=Publisher.objects.get(pk=id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/publishers/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            person = get_object_or_404(Publisher, pk=id)
            form = PublisherForm(instance=person)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/publishers/publishers-edit.html',
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
    while (Publisher.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)




