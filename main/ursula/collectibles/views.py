from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags, escape
from datetime import datetime
from ursula.models import Item, ItemForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.models import Location, Location_List
from ursula.models import Type
from ursula.models import MyStuff, WishList
from ursula.models import Ebay_Item

# meta functions
from ursula.items.meta import do_image_ordinals
from ursula.items.meta import do_tags
from ursula.items.meta import do_people
from ursula.items.meta import do_locations

# -----------------------------------
# Collectibles Landing Page
# -----------------------------------
def index(request):
    pins = Item.objects.all().filter(type=1).order_by('-release_date', '-id')[:7]
    dd = Item.objects.all().filter(type=4).order_by('-year')[:7]
    v = Item.objects.all().filter(type=5).order_by('-year')[:7]
    hb = Item.objects.all().filter(type=6).order_by('?')[:7]
    gof = Item.objects.all().filter(type=7).order_by('?')[:7]
    dm = Item.objects.all().filter(type=8).order_by('?')[:7]
    
    return render_to_response('ursula/collectibles/index.html',
        {
         'pins': pins,
         'disneydollars': dd,
         'vinylmations': v,
         'gof':gof,
         'hb':hb,
         'dm':dm,
         'nav': 'collectibles',
        }, context_instance=RequestContext(request)
    )   
    

# -----------------------------------
# Listings Landing Page
# -----------------------------------
def list(request, type_slug):
    #get relevant incoming Query Parameters
    sort_tag = request.REQUEST.get("tag", "")
    sort = request.REQUEST.get("sort", "")
        
    type = Type.objects.get(slug__exact = type_slug)
        
    # get list of items for type_name
    items = Item.objects.all().filter(type__slug__exact = type_slug, is_active = 1)
    
    # get list of tags for the items so we only show what is relevant
    # in the tag dropdown
    
    
    
    if sort_tag:
        items = items.filter(tag_list__tag = sort_tag, tag_list__is_active = 1)
        sort_tag = int(sort_tag)
    
    
    if sort == "high":
        items = items.order_by("-retail_price")
    elif sort == "low":
        items = items.order_by("retail_price")
    elif sort == "new":
        items = items.order_by("-release_date")
    elif sort == "old":
        items = items.order_by("release_date")
    else:
        items = items.order_by("-release_date")

  
    return render_to_response('ursula/collectibles/list.html',
        {'items': items,
         'sort_tag': sort_tag,
         'sort': sort,
         'type': type,
         'nav': 'collectibles',
        }, context_instance=RequestContext(request)
    )
    
# -----------------------------------
# Tag Landing Page
# -----------------------------------
def taglist(request, type_slug, tag_slug):
    #get relevant incoming Query Parameters
    sort_tag = request.REQUEST.get("tag", "")
    sort = request.REQUEST.get("sort", "")
        
    type = Type.objects.get(slug__exact = type_slug)
        
    # get list of items for type_name
    items = Item.objects.all().filter(type__slug__exact = type_slug, is_active = 1)
    
    # get list of tags for the items so we only show what is relevant
    # in the tag dropdown
    
    if sort_tag:
        items = items.filter(tag_list__tag = sort_tag, tag_list__is_active = 1)
        sort_tag = int(sort_tag)
    
    if sort == "high":
        items = items.order_by("-retail_price")
    elif sort == "low":
        items = items.order_by("retail_price")
    elif sort == "new":
        items = items.order_by("-release_date")
    elif sort == "old":
        items = items.order_by("release_date")
    else:
        items = items.order_by("-release_date")

  
    return render_to_response('ursula/collectibles/tag-list.html',
        {'items': items,
         'sort_tag': tag_slug,
         'sort': sort,
         'type': type,
         'nav': 'collectibles',
        }, context_instance=RequestContext(request)
    )    
    

# -----------------------------------
# Item Detail
# -----------------------------------
def detail(request, type_slug, item_slug):
    user_mystuff = False
    user_wishlist = False
    ebay_list = None
    item = get_object_or_404(Item, slug=item_slug, type__slug=type_slug, is_active=1)
    if item.view_count:
        item.view_count = item.view_count + 1
    else:
        item.view_count = 1
    #item.save()
    type = Type.objects.get(slug__exact = type_slug)
    # let's create a bit of randomness and pull some pins in
    tag_ids = []
    for tag in item.tag_list_set.all():
        tag_ids.append(tag.tag.id)
    
    # see if this user has this item, for view
    if request.user.is_authenticated():
        mystuff_item = MyStuff.objects.all().filter(item = item.id, user = request.user.id)
        wishlist_item = WishList.objects.all().filter(item = item.id, user = request.user.id)
        if mystuff_item:
            user_mystuff = True
        if wishlist_item:
            user_wishlist = True
    
    # get images
    image_list = Image_List.objects.all().filter(item = item).order_by("ordinal")
    
    # this is a hack to get around my legacy issue of empty pin image
    # showing as img/pins/main/
    if len(image_list) == 1:
        if image_list[0].image.src == "img/pins/main/":
            image_list = None
        
    # get randoms
    random_pins = Item.objects.all().filter(tag_list__tag__in = tag_ids, type__slug__exact = "pins", is_active = 1).order_by("?")[:12]
        
    # get ebay listings
    ebay_list = Ebay_Item.objects.all().filter(item = item, needs_admin = 0, is_active = 1, end_time__gte = datetime.now()).order_by("end_time")

    return render_to_response(item.type.template,
       {'item': item,
        'image_list': image_list,
        'random_pins':random_pins,
        'type': type,
        'has_mystuff': user_mystuff,
        'has_wishlist': user_wishlist,
        'ebay_list': ebay_list,
        'stripped_content': escape(strip_tags(item.content)),
        'nav': 'collectibles',
       }, context_instance=RequestContext(request)
    )
    
  







    
