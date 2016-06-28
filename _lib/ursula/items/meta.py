from django.template.defaultfilters import slugify
from ursula.models import Item, ItemForm
from ursula.models import Image, Image_List
from ursula.models import Tag, Tag_List
from ursula.models import Person, Person_List
from ursula.models import Location, Location_List

# -----------------------------------
# Process image ordinals for an item
# -----------------------------------
def do_image_ordinals(ordinal_ids, item_id):
    ordinal_split = ordinal_ids.split(',')
    if len(ordinal_split) > 1:
        p_id = ordinal_split.pop()
        counter = 1
        for id in ordinal_split:
            try:
                image_list = Image_List.objects.get(pk=id)
                image_list.ordinal = counter
                image_list.item_id = item_id
                image_list.save()
                counter += 1
            except Image_List.DoesNotExist:
                #do nothing
                return 2
    else:
        if ordinal_ids:
            try:
                image_list = Image_List.objects.get(pk=ordinal_ids)
                image_list.ordinal = 1
                image_list.item_id = item_id
                image_list.save()
            except Image_List.DoesNotExist:
                #do nothing
                return 3  
        
    return 1


# -----------------------------------
# Process tags for an item
# -----------------------------------
def do_tags(tag_ids, item_id):
   # mark each tag for item_id as inactive first
    tag_list = Tag_List.objects.filter(item = item_id)
    for tag_list_item in tag_list:
        tag_list_item.is_active = 0
        tag_list_item.save()
        

    # mark each incoming tag as active
    # first check to see if it exists.
    for id in tag_ids:
        id_set = 0
        for tag_list_item in tag_list:
            if str(tag_list_item.tag_id) == id:
                tag_list_item.is_active = 1
                tag_list_item.save()
                id_set = 1
                break
            
        if id_set == 0:
            new_item = Tag_List()
            new_item.tag_id = id
            new_item.item_id = item_id
            new_item.is_active = 1
            new_item.save()
                
    return 1


# -----------------------------------
# Process people for an item
# -----------------------------------
def do_people(people_ids, item_id):
   # mark each people for item_id as inactive first
    people_list = Person_List.objects.filter(item = item_id)
    for people_list_item in people_list:
        people_list_item.is_active = 0
        people_list_item.save()

    # mark each incoming tag as active
    # first check to see if it exists.
    for id in people_ids:
        id_set = 0
        for people_list_item in people_list:
            if str(people_list_item.person_id) == id:
                people_list_item.is_active = 1
                people_list_item.save()
                id_set = 1
                break
            
        if id_set == 0:
            new_item = Person_List()
            new_item.person_id = id
            new_item.item_id = item_id
            new_item.is_active = 1
            new_item.save()
                
    return 1


# -----------------------------------
# Process locations for an item
# -----------------------------------
def do_locations(location_ids, item_id):
   # mark each location for item_id as inactive first
    location_list = Location_List.objects.filter(item = item_id)
    for location_list_item in location_list:
        location_list_item.is_active = 0
        location_list_item.save()
        

    # mark each incoming tag as active
    # first check to see if it exists.
    for id in location_ids:
        id_set = 0
        for location_list_item in location_list:
            if str(location_list_item.location_id) == id:
                location_list_item.is_active = 1
                location_list_item.save()
                id_set = 1
                break
            
        if id_set == 0:
            new_item = Location_List()
            new_item.location_id = id
            new_item.item_id = item_id
            new_item.is_active = 1
            new_item.save()
                
    return 1


