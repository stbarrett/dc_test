from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from decimal import *
from ursula.models import Item, ItemForm
from ursula.models import Publisher, PublisherForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.classes.book import AmazonBook as AmazonBook
from ursula.classes.book import AmazonBookCreator as AmazonBookCreator
import urllib


# meta functions
from ursula.items.meta import do_image_ordinals
from ursula.items.meta import do_tags
from ursula.items.meta import do_people

@login_required
def index(request):
    item_list = Item.objects.all().filter(type=2).order_by('-id')
    return render_to_response('ursula/books/books-list.html',
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
    people_ids = request.POST.getlist('people_active_list')
    if id != "":
        item = Item.objects.get(pk=id)
        images = Image_List.objects.all().filter(item = id, is_active = 1).order_by('ordinal')
        
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save()
                
                # do images
                do_image_ordinals(str(request.post['image_ordinals']), item.id)
                
                # do tags
                do_tags(tag_ids, item.id)
                
                # do people
                do_people(people_ids, item.id)

                return HttpResponseRedirect('/books/') # Redirect after POST
            else:
                submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save()
                
                # do images
                do_image_ordinals(str(request.REQUEST.get("image_ordinals", "")), item.id)
                
                # do tags
                do_tags(tag_ids, item.id)
                
                # do people
                do_people(people_ids, item.id)
                         
                return HttpResponseRedirect('/books/')
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
        'ursula/books/book-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': id,
          'item': item,
          'images': images,
        },
        context_instance=RequestContext(request))
    
    
# Create Amazon Book 
def add_by_asin(request):
    asin = request.REQUEST.get("asin", "")
    if asin:
        # lookup asin and see if it already exists
        item = Item.objects.filter(asin=asin)
        if item:
            return HttpResponse(-2)
        else :
            book = AmazonBook()
            book.create_amazon_book_by_asin(asin)
            
            # do publisher
            try:
                publisher = Publisher.objects.get(name=book.publisher)
            except Publisher.DoesNotExist: 
                publisher = Publisher()
                publisher.name = book.publisher
                publisher.gen_slug_internal()
                publisher.is_active = 1
                publisher.save()
            
            item = Item()
            item.publisher_id = publisher.id
            item.title = book.title
            if book.publication_date:
                item.release_date = book.publication_date
                
            
            # clean up for storage
            if book.sale_price:
                book.sale_price = book.sale_price.replace("$", "")
                item.retail_price = Decimal(book.sale_price, 2)
            item.asin = book.ASIN
            item.isbn = book.ISBN
            item.binding = book.binding
            item.image = book.tiny_image    # used as thumbnail
            item.slug = gen_slug_internal(book.title)
            item.official_link = urllib.unquote(book.detail_url)
            item.content = book.description
            item.is_active = 1
            item.type_id = 2
            item.save()
            
            # do author - Person Table
            for ars in book.authors:
                a_split = ars.split(" ")
                try:
                    person = Person.objects.get(first_name=a_split[0], last_name=a_split[1])
                    create_person_list(person, item)
                except Person.DoesNotExist:
                    person = Person()
                    person.first_name = a_split[0]
                    a_split.pop(0)  # remove first element, everything else is pushed into last_name
                    person.last_name = ' '.join(a_split)
                    person.is_active = 1
                    person.gen_slug_internal()
                    person.save()
                    create_person_list(person, item)
            
            # do creators - Person Table
            for creator in book.creators:
                c_split = creator.name.split(" ")
                try:
                    person = Person.objects.get(first_name=c_split[0], last_name=c_split[1])
                    create_person_list(person, item)
                except Person.DoesNotExist:
                    person = Person()
                    person.first_name = c_split[0]
                    person.last_name = c_split[1]
                    person.is_active = 1
                    person.gen_slug_internal()
                    person.save()
                    create_person_list(person, item)
            

            return HttpResponse(item.id)

    else:
        return HttpResponse(-1)

# create person list item
def create_person_list(person, item):
    person_list = Person_List()
    person_list.person_id = person.id
    person_list.item_id = item.id
    person_list.is_active = 1
    person_list.save()


def gen_slug_internal(slug_str):
    new_slug = slugify(slug_str)
    orig_slug = new_slug
    #check for slug already existing
    counter = 1
    while (Item.objects.all().filter(slug=new_slug).count() > 0):
        new_slug = orig_slug + "-" + str(counter)
        counter += 1
        
    return new_slug
    
    
def search_slug(request):
    search_slug = request.GET['slug']
    item_list = Item.objects.all().filter(slug = search_slug, type = 2)
    return render_to_response('ursula/books/books-list.html',
        {'item_list': item_list
        }, context_instance=RequestContext(request)
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        