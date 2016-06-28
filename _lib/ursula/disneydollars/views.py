from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from ursula.models import Item, ItemForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Location, Location_List

# meta functions
from ursula.items.meta import do_image_ordinals
from ursula.items.meta import do_tags
from ursula.items.meta import do_locations

@login_required
def index(request):
    item_list = Item.objects.all().filter(type=4).order_by('-year', 'denomination')
    return render_to_response('ursula/disneydollars/disneydollars-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    test = ''
    submit_action = ''
    form = ItemForm()
    item = ""
    images = ""
    tag_ids = request.POST.getlist('tag_active_list')
    location_ids = request.POST.getlist('location_active_list')
    if id != "":
        item = Item.objects.get(pk=id)
        images = Image_List.objects.all().filter(item = id, is_active = 1).order_by('ordinal')
        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save()
                
                # do images
                do_image_ordinals(str(request.POST['image_ordinals']), item.id)
                                
                # do tags
                do_tags(tag_ids, item.id)
               
                # do locations
                do_locations(location_ids, item.id)        

                return HttpResponseRedirect('/disneydollars/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                
                # do images
                do_image_ordinals(str(request.POST['image_ordinals']), item.id)
                
                # do tags
                do_tags(tag_ids, item.id)
                
             
                # do locations
                do_locations(location_ids, item.id)                
                
                
                return HttpResponseRedirect('/disneydollars/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(Item, pk=id)
            form = ItemForm(instance=item)
        else:
            submit_action = 'Add'
        
    return render_to_response(
        'ursula/disneydollars/disneydollars-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
          'images': images,
        },
        context_instance=RequestContext(request))
	

def gen_slug(request):
    new_slug = slugify(request.GET.get('slug', ''))
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Item.objects.all().filter(slug=new_slug, type=4).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)

    
    
    
    
    