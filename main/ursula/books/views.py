from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags, escape
from datetime import datetime, date
from ursula.models import Item, ItemForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.models import Location, Location_List
from ursula.models import Type
from ursula.models import MyStuff
from ursula.models import WishList
from ursula.models import Publisher
from ursula.classes.book import AmazonBook as AmazonBook
from ursula.classes.book import AmazonBookCreator as AmazonBookCreator

class BookPerson:
    slug = ""
    name = ""
    role = ""
   

# -----------------------------------
# Books Landing Page
# -----------------------------------
def index(request):
    
    items = Item.objects.all().filter(type__slug__exact = "books", is_active = 1).order_by('-release_date')
  
    return render_to_response('ursula/books/index.html',
        {'items': items,
         'nav': 'books',
        }, context_instance=RequestContext(request)
    )
 
        
# -----------------------------------
# Item Detail
# -----------------------------------
def detail(request, item_slug):
    user_mystuff = False;
    user_wishlist = False;
    item = get_object_or_404(Item, slug=item_slug, is_active=1)
    book = AmazonBook()
    book.create_amazon_book_by_asin(item.asin)
        
    # see if this user has this item, for view
    if request.user.is_authenticated():
        mystuff_item = MyStuff.objects.all().filter(item = item.id, user = request.user.id)
        wishlist_item = WishList.objects.all().filter(item = item.id, user = request.user.id)
        if mystuff_item:
            user_mystuff = True
        if wishlist_item:
            user_wishlist = True
            
    # matchup author to person
    # matchup creator to person
    person_list = Person_List.objects.all().filter(item = item, is_active = 1)
    authors_list = []
    creators_list = []
    for person in person_list:
        fname = person.person.first_name
        lname = person.person.last_name
        name = fname + " " + lname
        for author in book.authors:
            if author == name:
                book_person = BookPerson()
                book_person.slug = person.person.slug
                book_person.name = author
                authors_list.append(book_person)
        for creator in book.creators:
            if creator.name == name:
                book_creator = BookPerson()
                book_creator.slug = person.person.slug
                book_creator.name = creator.name
                book_creator.role = creator.role
                creators_list.append(book_creator)
    
    publisher = ""
    #publisher = Publisher.objects.all().filter(name = book.publisher)
    #if publisher != None:
    #    publisher = publisher[0]
    preorder = False
    
    if item.release_date:
        if datetime.today() < item.release_date:
            preorder = True
          
    return render_to_response(item.type.template,
       {'item': item,
        'book': book,
        'type': 'books',
        'authors': authors_list,
        'creators': creators_list,
        'publisher': publisher,
        'has_mystuff': user_mystuff,
        'has_wishlist': user_wishlist,
        'preorder': preorder,
        'stripped_content': escape(strip_tags(book.description)),
         'nav': 'books',
       }, context_instance=RequestContext(request)
    )





    