from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django import forms
from django.template.defaultfilters import slugify
from ursula.models import Person, PersonForm

@login_required
def index(request):
    person_list = Person.objects.all().order_by('last_name')
    return render_to_response('ursula/people/people-list.html',
        {'person_list': person_list
        }, context_instance=RequestContext(request)
    )

@login_required
def detail(request, person_slug):
    #Get Item
    person = get_object_or_404(Person, slug=person_slug, is_active=True)
    return render_to_response('ursula/people/people-detail.html',
        { 'person': person
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    edit_id = id
    form = PersonForm()
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
          form = PersonForm(request.POST)
          if form.is_valid():
            form.save()
            return HttpResponseRedirect('/people/') # Redirect after POST
          else:
            submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = PersonForm(request.POST, instance=Person.objects.get(pk=id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/people/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            person = get_object_or_404(Person, pk=id)
            form = PersonForm(instance=person)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/people/people-edit.html',
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
    while (Person.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)




