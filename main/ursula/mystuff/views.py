from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime
from ursula.models import Item, ItemForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.models import Location, Location_List
from ursula.models import Type
from ursula.models import MyStuff
from ursula.models import WishList
from ursula.classes.book import AmazonBook as AmazonBook
from ursula.classes.book import AmazonBookCreator as AmazonBookCreator


# -----------------------------------
# Landing page
# -----------------------------------
def index(request):
    #user must be logged in with a valid account
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/member/login?next=/mystuff/')
    
    return HttpResponseRedirect("/mystuff/collectibles/");

    
    
    # get most recent items added
    #recent_items = MyStuff.objects.all().filter(user = request.user.id).order_by('-added_on')[:49]
    
    #return render_to_response('ursula/mystuff/index.html',
    #    {'recent_items': recent_items,
    #    }, context_instance=RequestContext(request)
    #)
    
# -----------------------------------
# View My Collectibles
# -----------------------------------
def mycollectibles(request):
    #user must be logged in with a valid account
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/member/login?next=/mystuff/')
    
    msg = request.REQUEST.get("m", "")
    
    if msg == "error":
        msg = "There was an error in processing your request."
        
    if msg == "removed":
        msg = "Your item was removed successfully."
        
    # get "collectible" items
    #items = MyStuff.objects.all().filter(user = request.user.id).exclude(item__type__id = 2,
    #                                                                     item__type__id = 3).order_by("added_on")
    
    items = MyStuff.objects.all().filter(user = request.user.id).order_by("added_on")
    items = items.exclude(item__type__id=2)    
    
    return render_to_response('ursula/mystuff/mycollectibles.html',
        {'items': items,
         'type': 'collectibles',
         'message': msg,
        }, context_instance=RequestContext(request)
    )
    
# -----------------------------------
# View My Books
# -----------------------------------
def mybooks(request):
    #user must be logged in with a valid account
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/member/login?next=/mystuff/')

    msg = request.REQUEST.get("m", "")
    
    if msg == "error":
        msg = "There was an error in processing your request."
        
    if msg == "removed":
        msg = "Your item was removed successfully."    
        
    # get "collectible" items
    #items = MyStuff.objects.all().filter(user = request.user.id).exclude(item__type__id = 2,
    #                                                                     item__type__id = 3).order_by("added_on")
    
    items = MyStuff.objects.all().filter(user = request.user.id).order_by("added_on")
    items = items.exclude(item__type__id=1)
    items = items.exclude(item__type__id=3)
    items = items.exclude(item__type__id=4)
    
    
    return render_to_response('ursula/mystuff/mybooks.html',
        {'items': items,
         'type': 'books',
         'message': msg,
        }, context_instance=RequestContext(request)
    )    
     
# -----------------------------------
# View My Wish
# -----------------------------------
def mywishlist(request):
    #user must be logged in with a valid account
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/member/login?next=/mystuff/wishlist')
    
    msg = request.REQUEST.get("m", "")
    
    if msg == "error":
        msg = "There was an error in processing your request."
        
    if msg == "removed":
        msg = "Your item was removed successfully."    
    
    items = WishList.objects.all().filter(user = request.user.id).order_by("added_on")
    #items = items.exclude(item__type__id=2)    
    
    return render_to_response('ursula/mystuff/mywishlist.html',
        {'items': items,
         'type': 'wishlist',
         'message': msg,
        }, context_instance=RequestContext(request)
    )


# -----------------------------------
# Edit Portfolio Item - Collectible
# -----------------------------------
def editcollectible(request, mystuff_id):
    #user must be logged in with a valid account
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/member/login?next=/mystuff/')
        
    was_edited = False
    if request.method == 'GET':
        #user must be logged in with a valid account
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/member/login?next=/mystuff/edit/'+mystuff_id)
        
        #get item and make sure it's associated with this user
        item = MyStuff.objects.all().filter(id = mystuff_id, user = request.user.id)
        
        #make sure the item exists
        if not item:
            return HttpResponse("There was an error locating this item.")
        
        
        #make sure this user has access to this item
        #if item.user != request.user.id:
        #    return HttpResponse("You do not have access to this item.")
        
        return render_to_response('ursula/mystuff/edit-collectible.html',
            {'item':item[0],
             'saved':False,
             
            }, context_instance=RequestContext(request)
        )
        
    if request.method == 'POST':
        date_got = request.REQUEST.get("date-got", "")
        price_paid = request.REQUEST.get("price-paid", "")
        where_got = request.REQUEST.get("where-got", "")
        notes = request.REQUEST.get("notes", "")
        
        item = MyStuff.objects.all().filter(id = mystuff_id, user = request.user.id)
        item = item[0]
        if item:
            if date_got:
                item.date_got = datetime.strptime(date_got, '%m/%d/%Y')
            item.price_paid = price_paid
            item.where_got = where_got
            item.notes = notes
            
        else:
            return HttpResponse("This is not your item.")
            
        item.save()
        was_edited = True;

        return render_to_response('ursula/mystuff/edit-collectible.html',
            {'item':item,
             'saved':True,
             'was_edited': was_edited,
            }, context_instance=RequestContext(request)
        )
        
        
# -----------------------------------
# Edit Wishlist Item 
# -----------------------------------
def editwishlist(request, wishlist_id):
    #user must be logged in with a valid account
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/member/login?next=/mystuff/')
        
    was_edited = False
    if request.method == 'GET':
        #user must be logged in with a valid account
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/member/login?next=/mystuff/edit/'+wishlist_id)
        
        #get item and make sure it's associated with this user
        item = WishList.objects.all().filter(id = wishlist_id, user = request.user.id)
        
        #make sure the item exists
        if not item:
            return HttpResponse("There was an error locating this item.")
        
        
        #make sure this user has access to this item
        #if item.user != request.user.id:
        #    return HttpResponse("You do not have access to this item.")
        
        return render_to_response('ursula/mystuff/edit-wishlist.html',
            {'item':item[0],
             'saved':False,
            }, context_instance=RequestContext(request)
        )
        
    if request.method == 'POST':
        notes = request.REQUEST.get("notes", "")
        
        item = WishList.objects.all().filter(id = wishlist_id, user = request.user.id)
        item = item[0]
        if item:
            item.notes = notes            
        else:
            return HttpResponse("This is not your item.")
            
        item.save()
        was_edited = True;

        return render_to_response('ursula/mystuff/edit-wishlist.html',
            {'item':item,
             'saved':True,
             'was_edited': was_edited,
            }, context_instance=RequestContext(request)
        )        
     
     
# -----------------------------------
# Add To My Stuff
# -----------------------------------
def addmystuff(request):
   if request.method == 'GET':
        return HttpResponse("-1");
    
    # check login status
   if not request.user.is_authenticated():
        return HttpResponse("0")

    # lets see if the item already exists
   item_id = request.REQUEST.get("item_id", "")
   mystuff_item = MyStuff.objects.all().filter(item = item_id, user = request.user.id)
   if not mystuff_item:
       mystuff_item = MyStuff()
       mystuff_item.user_id = request.user.id
       mystuff_item.item_id = item_id
       mystuff_item.save()
       return HttpResponse("1")
   
   return HttpResponse("2");


# -----------------------------------
# Remove Item From My Stuff
# -----------------------------------
def removecollectible(request, mystuff_id):
    mystuff_item = MyStuff.objects.all().filter(id = mystuff_id, user = request.user.id)
    
    if not mystuff_item:
        return HttpResponseRedirect("/mystuff/collectibles/?m=error")
    
    type = mystuff_item[0].item.type.id
    mystuff_item.delete()
    
    if type == 2:
        return HttpResponseRedirect("/mystuff/books/?m=removed")

    return HttpResponseRedirect("/mystuff/collectibles/?m=removed")


# -----------------------------------
# Add To My Wish List
# -----------------------------------
def addwishlist(request):
   if request.method == 'GET':
        return HttpResponse("-1");
    
    # check login status
   if not request.user.is_authenticated():
        return HttpResponse("0")

    # lets see if the item already exists
   item_id = request.REQUEST.get("item_id", "")
   wishlist_item = WishList.objects.all().filter(item = item_id, user = request.user.id)
   if not wishlist_item:
       wishlist_item = WishList()
       wishlist_item.user_id = request.user.id
       wishlist_item.item_id = item_id
       wishlist_item.save()
       return HttpResponse("1")
   
   return HttpResponse("2");


# -----------------------------------
# Remove Item From My Wish List
# -----------------------------------
def removewishlist(request, wishlist_id):
    wishlist_item = WishList.objects.all().filter(id = wishlist_id, user = request.user.id)
    
    if not wishlist_item:
        return HttpResponseRedirect("/mystuff/wishlist/?m=error")
    
    wishlist_item.delete()
    
    return HttpResponseRedirect("/mystuff/wishlist/?m=removed")






