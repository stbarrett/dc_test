from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db.models import permalink

import datetime

from djangosphinx.models import SphinxSearch


# -----------------------------------
# Type
# -----------------------------------
class Type(models.Model):
    name = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=True)
    template = models.CharField(max_length=255, null=True)
    parent_url = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=False)
    title_single = models.CharField(max_length=255, null=False)
    img_slug = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=64, null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class TypeForm(ModelForm):
    class Meta:
        model = Type
        

# -----------------------------------
# People
# -----------------------------------
class Person(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)
    
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
    
    def gen_slug_internal(self):
        new_slug = slugify(self.first_name + " " + self.last_name)
        orig_slug = new_slug
        #check for slug already existing
        counter = 1
        while (Person.objects.all().filter(slug=new_slug).count() > 0):
            new_slug = orig_slug + "-" + str(counter)
            counter += 1
            
        self.slug =  new_slug
     

class PersonForm(ModelForm):
    class Meta:
        model = Person
        
# -----------------------------------
# Publisher
# ----------------------------------- 
class Publisher(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.name
    
    def gen_slug_internal(self):
        new_slug = slugify(self.name)
        orig_slug = new_slug
        #check for slug already existing
        counter = 1
        while (Publisher.objects.all().filter(slug=new_slug).count() > 0):
            new_slug = orig_slug + "-" + str(counter)
            counter += 1
            
        self.slug =  new_slug
        
        
class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        
        
# -----------------------------------
# Podcasts
# ----------------------------------- 
class Podcast(models.Model):
    title = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    author = models.TextField(null=True,blank=True)
    feed_url = models.CharField(max_length=255, null=True)
    itunes_url = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    type = models.ForeignKey(Type)
    image = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.title
    
    def gen_slug_internal(self):
        new_slug = slugify(self.title)
        orig_slug = new_slug
        #check for slug already existing
        counter = 1
        while (Podcast.objects.all().filter(slug=new_slug).count() > 0):
            new_slug = orig_slug + "-" + str(counter)
            counter += 1
            
        self.slug =  new_slug
        
    def podcast_image(self):
        return self.image
        
        
class PodcastForm(ModelForm):
    class Meta:
        model = Podcast   
        
        
# -----------------------------------
# Podcasts Feed Items
# ----------------------------------- 
class PodcastItem(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    publication_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    media_url = models.CharField(max_length=255, null=True, blank=True)
    media_size = models.CharField(max_length=32, null=True, blank=True)
    media_type = models.CharField(max_length=50, null=False, blank=True)
    guid = models.CharField(max_length=255, null=False)
    podcast = models.ForeignKey(Podcast)
    is_new = models.BooleanField()
    
class PodcastItemForm(ModelForm):
    class Meta:
        model = PodcastItem  
    
        
# -----------------------------------
# Items
# -----------------------------------
class Item(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=False)
    official_link = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    retail_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=64, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    edition_size = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField()    
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    type = models.ForeignKey(Type)
    isbn = models.CharField(max_length=15, null=True, blank=True)
    asin = models.CharField(max_length=10, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, null=True, blank=True)
    binding = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    #denomination = models.IntegerField()
    denomination = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    year = models.SmallIntegerField(null=True, blank=True)
    view_count = models.SmallIntegerField(null=True, blank=True)
    scrape_status = models.SmallIntegerField(null=True, blank=True)
    disable_ebay = models.BooleanField()
    ebay_search_phrase = models.CharField(max_length=255, null=False, blank=True)
    
    search = SphinxSearch(
        index ='items', 
        weights = { # individual field weighting
            'title': 100,
            'content': 90,
        }
    )    
    
    
    def __unicode__(self):
        return self.title 
    
    def get_average_rating(self):
        ratings = Ratings.objects.all().filter(id = self.id)
        # get average
        return len(ratings)
    
    def first_image(self):
        image = Image_List.objects.all().filter(item = self.id, is_active=1).order_by('ordinal')
        if not image:
            return ""
        return image[0].image.src

    def first_image_copyright(self):
        image = Image_List.objects.all().filter(item = self.id, is_active=1).order_by('ordinal')
        return image[0].image.copyright
    
class ItemForm(ModelForm):
    class Meta:
        model = Item   
 
     
# -----------------------------------
# Images
# -----------------------------------
class Image(models.Model):
    user = models.ForeignKey(User, unique=False, blank=True, null=True)
    src = models.CharField(max_length=255, null=True)
    copyright = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)

    def __unicode__(self):
        return self.src


class ImageForm(ModelForm):
    class Meta:
        model = Image
        
# -----------------------------------
# ImagesList
#  Lookup table for images and items
# -----------------------------------
class Image_List(models.Model):
    image = models.ForeignKey(Image)
    item = models.ForeignKey(Item, null=True)
    caption = models.CharField(max_length=255, null=True, blank=True)
    ordinal = models.IntegerField(null=False)
    is_active = models.BooleanField()
    needs_admin= models.BooleanField()
         
    def __unicode__(self):
        return str(id)
    

class ImageListForm(ModelForm):
    class Meta:
        model = Image_List
    
    
# -----------------------------------
# Locations
# -----------------------------------
class Location(models.Model):
    name = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)
   
    def __unicode__(self):
        return self.name
        
class LocationForm(ModelForm):
    class Meta:
        model = Location

 
# -----------------------------------
# LocationsList
# Lookup table for locations
# -----------------------------------
class Location_List(models.Model):
    location = models.ForeignKey(Location)
    item = models.ForeignKey(Item, null=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return str(self.id)
        
# -----------------------------------
# Person List
# Lookup table for people
# -----------------------------------
class Person_List(models.Model):
    person = models.ForeignKey(Person)
    item = models.ForeignKey(Item, null=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.person.last_name

# -----------------------------------
# Tag
# -----------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    updated_on = models.DateTimeField(auto_now=True, null=False)

    def __unicode__(self):
        return self.name
    
class TagForm(ModelForm):
    class Meta:
        model = Tag
        
# -----------------------------------
# Tag_List
# Lookup table for tags
# -----------------------------------
class Tag_List(models.Model):
    tag = models.ForeignKey(Tag)
    item = models.ForeignKey(Item, null=True, blank=True)
    podcast = models.ForeignKey(Podcast, null=True, blank=True)
    podcastitem = models.ForeignKey(PodcastItem, null=True, blank=True)
    is_active = models.BooleanField()

    def __unicode__(self):
        return str(self.id)
    
    
# -----------------------------------
# User Item Lookup Table
# -----------------------------------
class User_Item_List(models.Model):
    user = models.ForeignKey(User, unique=True)
    item_id = models.ForeignKey(Item, null=True)
    
    def __unicode__(self):
        return str(self.id)
    
    

# -----------------------------------
# Ratings
# -----------------------------------
class Ratings(models.Model):
    item = models.ForeignKey(Item, null=False)
    user = models.ForeignKey(User, null=False)
    rating = models.SmallIntegerField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)



# -----------------------------------
# Post -- Blog type content
# -----------------------------------
class Post(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=False)
    content = models.TextField(null=True, blank=True)
    excerpt = models.TextField(null=True, blank=True)
    home_image = models.CharField(max_length=255, null=True, blank=True)
    publish_date = models.DateTimeField(null=False, blank=True)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    
    @permalink
    def get_absolute_url(self):
        return ('news-detail', None, {
            'year': self.publish_date.year,
            'month': self.publish_date.strftime('%m'),
            'slug': self.slug
        })    
    
class PostForm(ModelForm):
    class Meta:
        model = Post


# -----------------------------------
# PostCategory -- Blog Categories
# -----------------------------------
class PostCategory(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField()
    
class PostCategoryForm(ModelForm):
    class Meta:
        model = PostCategory
  
# -----------------------------------
# PostCategoryList -- Blog Categories
#                     Lookup Table
# -----------------------------------
class PostCategoryList(models.Model):
    post = models.ForeignKey(Post, null=False)
    post_category = models.ForeignKey(PostCategory, null=False)
    is_active = models.BooleanField()


# -----------------------------------
# Pages -- Static, non Post type content
# ie. TOS, contact, etc.
# -----------------------------------
class Page(models.Model):
    title = models.CharField(max_length=255, null=False)
    slug = models.CharField(max_length=255, null=False)
    content = models.TextField(null=True, blank=True)
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)


class PageForm(ModelForm):
    class Meta:
        model = Page


# -----------------------------------
# MyStuff -- My Stuff tracking
# -----------------------------------
class MyStuff(models.Model):
    item = models.ForeignKey(Item, null=False)
    user = models.ForeignKey(User, null=False)
    added_on = models.DateTimeField(auto_now_add=True, null=False)
    date_got = models.DateTimeField(null=True, blank=True)
    price_paid = models.CharField(max_length=32, null=True, blank=True)
    where_got = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    

# -----------------------------------
# WishList -- Wishlist items
# -----------------------------------
class WishList(models.Model):
    item = models.ForeignKey(Item, null=False)
    user = models.ForeignKey(User, null=False)
    added_on = models.DateTimeField(auto_now_add=True, null=False)
    notes = models.TextField(null=True, blank=True)

# -----------------------------------
# Log -- Log items for various funcs.
# -----------------------------------
class Log(models.Model):
    log_text = models.TextField(null=True, blank=True)
    log_type = models.CharField(max_length=32, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)


# -----------------------------------
# Ebay
# -----------------------------------
class Ebay_Item(models.Model):
	ebay_item_id = models.CharField(max_length=32, null=False)
	title = models.CharField(max_length=255, null=False)
	url = models.CharField(max_length=255, null=False)
	item = models.ForeignKey(Item, null=False)
	current_price = models.DecimalField(max_digits=12, decimal_places=2, null=False)
	buyit_now_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	gallery_url = models.CharField(max_length=255, null=True, blank=True)
	selling_state = models.CharField(max_length=255, null=False)
	end_time = models.DateTimeField(auto_now_add=False, null=True)
	created_on = models.DateTimeField(auto_now_add=True, null=False)
	is_active = models.BooleanField()
	needs_admin = models.BooleanField()
