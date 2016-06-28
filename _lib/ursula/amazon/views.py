from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from ursula.models import Item, ItemForm
from ursula.models import Publisher, PublisherForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.classes.book import AmazonBook as AmazonBook
from ursula.classes.book import AmazonBookCreator as AmazonBookCreator
import urllib
from decimal import *

# meta functions
from ursula.items.meta import do_image_ordinals
from ursula.items.meta import do_tags
from ursula.items.meta import do_people

    
def index(request):
    asin = request.REQUEST.get("asin", "")
    book = AmazonBook()
    if asin:
        book.create_amazon_book_by_asin(asin)
    else:
        return HttpResponse("No Valid ASIN found")

    #return HttpResponse(book.raw_xml)
    return render_to_response('amazon/index.html',
        {'item': book,
        }, context_instance=RequestContext(request)
    )
    

# should be called via a scheduled job
# to go through amazon books and update
# our stored searchable data    
def update_books(request):
    books = Item.objects.all().filter(type__slug__exact = "books").order_by('id')
    out = ""
    for book in books:
        bookObj = AmazonBook()
        bookObj.create_amazon_book_by_asin(book.asin)
        
        #update stored objects
        book.title = bookObj.title
        #book.release_date = bookObj.publication_date
        
        # clean up for storage
        if bookObj.sale_price:
            book.sale_price = bookObj.sale_price.replace("$", "")
            book.retail_price = Decimal(book.sale_price, 2)        

        book.asin = bookObj.ASIN
        book.isbn = bookObj.ISBN
        book.binding = bookObj.binding
        
        book.content = bookObj.description.encode('utf-8')
        book.image = bookObj.tiny_image    # used as thumbnail
        book.official_link = urllib.unquote(bookObj.detail_url)
        
        ## NEED TO FIGURE OUT UTF-8 ISSUE
        try:
            book.save()
        except:
            book.content = ""
            book.save()
        
        out += book.title + "<br />\n"

    return HttpResponse(out)

    
    
    
    
    
    
    
    
    
    
    
    
    