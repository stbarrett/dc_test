from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from ursula.models import Item, ItemForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.models import Location, Location_List
from ursula.models import Ebay_Item

# meta functions
from ursula.items.meta import do_image_ordinals
from ursula.items.meta import do_tags
from ursula.items.meta import do_people
from ursula.items.meta import do_locations

@login_required
def index(request):
    type_id = request.REQUEST.get("type", "")
    if type_id:
        item_list = Item.objects.all().filter(type=type_id).order_by('-release_date', '-id')
    else:
        item_list = Item.objects.all().order_by('-release_date', '-id')
    return render_to_response('ursula/collectibles/collectible-list.html',
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
    ebay_items = ""
    tag_ids = request.POST.getlist('tag_active_list')
    location_ids = request.POST.getlist('location_active_list')
    people_ids = request.POST.getlist('people_active_list')
    if id != "":
        item = Item.objects.get(pk=id)
        images = Image_List.objects.all().filter(item = id, is_active = 1).order_by('ordinal')
        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = ItemForm(request.POST)
            if form.is_valid():
		#check disable ebay, get correct value
                if(form.disable_ebay == 0):
                    form.disable_ebay = None;
                item = form.save()
                
                # do images
                do_image_ordinals(str(request.POST['image_ordinals']), item.id)
                                
                # do tags
                do_tags(tag_ids, item.id)
                
                # do people
                do_people(people_ids, item.id)
                
                # do locations
                do_locations(location_ids, item.id)        

                return HttpResponseRedirect('/collectibles/') # Redirect after POST
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
                
                # do people
                do_people(people_ids, item.id)
                
                # do locations
                do_locations(location_ids, item.id)                
                
                
                return HttpResponseRedirect('/collectibles/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            item = get_object_or_404(Item, pk=id)
            if(item.disable_ebay == None):
                item.disable_ebay = 0;
            form = ItemForm(instance=item)
            ebay_items = Ebay_Item.objects.all().filter(item = item, is_active = 1).order_by('-needs_admin', '-end_time')
        else:
            submit_action = 'Add'
    
    return render_to_response(
        'ursula/collectibles/collectible-edit.html',
		{	'request': request,
			'form': form,
			'submit_action': submit_action,
			'edit_id': id,
			'item': item,
			'images': images,
            'ebay_items': ebay_items
        },
        context_instance=RequestContext(request))
	

def gen_slug(request):
    new_slug = slugify(request.GET.get('slug', ''))
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Item.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return HttpResponse(new_slug)
    
    
def search_slug(request):
    search_slug = request.GET['slug']
    #item_list = Item.objects.all().filter(slug = search_slug, type = 1)
    item_list = Item.objects.all().filter(slug = search_slug)
    return render_to_response('ursula/collectibles/collectible-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )
    
    
    
    
    
    
    
