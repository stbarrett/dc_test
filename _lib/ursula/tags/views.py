from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django import forms
from django.template.defaultfilters import slugify
from ursula.models import Tag, TagForm


@login_required
def index(request):
    tag_list = Tag.objects.all().order_by('name')
    return render_to_response('ursula/tags/tags-list.html',
        {'tag_list': tag_list
        }, context_instance=RequestContext(request)
    )

@login_required
def detail(request, tag_slug):
    #Get Item
    tag = get_object_or_404(Tag, slug=tag_slug, is_active=True)
    return render_to_response('ursula/tags/tags-detail.html',
        { 'tag': tag
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    edit_id = id
    form = TagForm()
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
          form = TagForm(request.POST)
          if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tags/') # Redirect after POST
          else:
            submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = TagForm(request.POST, instance=Tag.objects.get(pk=id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/tags/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            tag = get_object_or_404(Tag, pk=id)
            form = TagForm(instance=tag)
            
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/tags/tags-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': edit_id
        }
      ) 
    
def create_ajax(request):
    tag_name = request.POST.get('tag_name', '')
    tag_slug = create_slug(tag_name)

    tag = Tag()
    tag.name = tag_name
    tag.slug = tag_slug
    tag.is_active = 1
    tag.save()
    
    return HttpResponse(tag.id)
    
    
def gen_slug(request):
    return HttpResponse(create_slug(request.GET.get('slug', '')))

def create_slug(slug):
    new_slug = slugify(slug)
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Tag.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return new_slug