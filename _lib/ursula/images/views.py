from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Q
from django import forms
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from ursula.models import Image, ImageListForm, Image_List


def edituserupload(request, id=""):
    edit_id = id
    current_site = Site.objects.get(id=settings.SITE_ID)


    if request.method == 'POST':
        copyright = request.POST['copyright']
        caption = request.POST['caption']
        message = request.POST['message']
        approve = request.POST['approve']

        image_list_obj = Image_List.objects.get(pk=id)
        image_obj = Image.objects.get(pk=image_list_obj.image_id)
        
        image_list_obj.caption = caption
        image_list_obj.needs_admin = False
        if approve == "1":
            image_list_obj.is_active = True
            image_list_for_id = Image_List.objects.all().filter(item = image_list_obj.item).order_by('ordinal')
            ord = image_list_for_id[len(image_list_for_id)-2].ordinal
            image_list_obj.ordinal = ord + 1
            if copyright == "":
                copyright = "Uploaded by "+ image_obj.user.username
            image_obj.copyright = copyright
            
            image_list_obj.save()
            image_obj.save()
            url = "http://"+current_site.domain+image_list_obj.item.type.parent_url+"/"+image_list_obj.item.slug
            msg = "Thank you for submitting an image to Dizcollect.com. \r\n\r\nYour image has been approved and added to the site and can be viewed at:\r\n"+url+"\r\n\r\n"+message+"\r\n\r\n -- Dizcollect.com"
            send_mail('Dizcollect Image Upload ', msg, settings.CONTACT_EMAIL,
            [image_obj.user.email] , fail_silently=False)            
        else:
            image_list_obj.save()
            msg = "Thank you for submitting an image to Dizcollect.com. \r\n\r\nWe are sorry, but your image was not approved.\r\n\r\n"+message+"\r\n\r\n -- Dizcollect.com"
            send_mail('Dizcollect Image Upload ', msg, settings.CONTACT_EMAIL,
            [image_obj.user.email] , fail_silently=False)
            
        
       
        return HttpResponseRedirect('/') # Redirect after POST
 
    if request.method == 'GET':
        image = get_object_or_404(Image_List, pk=id)

    return render_to_response(
        'ursula/images/image-edit-user-upload.html',
        { 'request': request,
          'edit_id': edit_id,
          'image': image
        },
        context_instance=RequestContext(request))

def edit(request, id=""):
    edit_id = id

    if request.method == 'POST':
        image_list_id = request.POST['id']
        copyright = request.POST['copyright']
        caption = request.POST['caption']

        image_list_obj = Image_List.objects.get(pk=image_list_id)
        image_obj = Image.objects.get(pk=image_list_obj.image_id)
        
        image_list_obj.caption = caption
        image_list_obj.save()
        
        image_obj.copyright = copyright
        image_obj.save()
        
       
        return HttpResponse("")
 
    if request.method == 'GET':
        image = get_object_or_404(Image_List, pk=id)

    return render_to_response(
        'ursula/images/image-edit.html',
        { 'request': request,
          'edit_id': edit_id,
          'image': image
        },
        context_instance=RequestContext(request))


def remove(request, id=""):
    image = Image_List.objects.get(pk=id)
    image.is_active = 0
    image.save()
    return HttpResponse("true")


def create(request):
    img_src = request.POST.get('img', '')
    type = request.POST.get('type', '')
    item_id = request.POST.get('item_id', '')
    full_path = settings.MEDIA_URL + img_src;
    
    # see if the image currently exists
    #in our image table
    img = ""
    try:
        img = Image.objects.get(src = img_src)
    except Image.DoesNotExist:
        #create image
        img = Image()
        img.src = img_src 
        img.is_active = 1
        img.save()
        
        
    # see if the image exists
    # in the images_list
    image_list_item = ""
    try:
        image_list_item = Image_List.objects.get(
                                    Q(item = item_id),
                                    Q(image = img.id)
                          )
        image_list_item.is_active = 1
        image_list_item.save()
    except Image_List.DoesNotExist:
        image_list_item = Image_List()
        image_list_item.item_id = item_id;
        image_list_item.image_id = img.id
        image_list_item.is_active = 1
        image_list_item.ordinal = 1
        image_list_item.save()
        
    return HttpResponse(str(image_list_item.id) + ", " + full_path)
















