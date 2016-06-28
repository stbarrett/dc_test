from shutil import copy
import string
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import datetime, time
from django.core.mail import send_mail
from settings import MEDIA_ROOT
from ursula.models import Item, ItemForm, Image, Image_List
import ursula


import Image

# -----------------------------------
# Contribute Landing Page
# -----------------------------------
def index(request):

    return render_to_response('ursula/contribute/index.html',
        {

        }, context_instance=RequestContext(request)
    )   
    

# -----------------------------------
# Contribute Image to Item
# -----------------------------------
def contributeimage(request, item_id):
    if not request.user.is_authenticated():
        return render_to_response('ursula/contribute/contribute-image.html',
            {
             'step': -1
            }, context_instance=RequestContext(request)
        )


    item = Item.objects.get(pk=item_id)
    step = 1
    img = ""
    
    if request.method == 'POST':
        step = int(request.POST['step'])
        if step == 1:
            step = 2
            image = request.FILES['image']
            file_name = str(request.user.id) + "_" + str(item_id) + "_" + str(datetime.now().microsecond) + "_" + image.name
            file_path = MEDIA_ROOT + "img/user_upload/" + file_name
            file_path_raw = MEDIA_ROOT + "img/user_upload/_raw/" + file_name
            handle_uploaded_file(image, file_path)
            handle_uploaded_file(image, file_path_raw)
            # resize image to manageable image
            img = Image.open(file_path)
            size = 800, 800
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(file_path, "JPEG")
            img = "img/user_upload/" + file_name
        elif step == 2:
            step = 3
            image = request.POST['image']
            image_path = MEDIA_ROOT + image
            x1 = request.POST['x1']
            y1 = request.POST['y1']
            x2 = request.POST['x2']
            y2 = request.POST['y2']
            crop_box = (int(x1), int(y1), int(x2), int(y2))
            im = Image.open(image_path)
            new_img = im.crop(crop_box)
            new_img.save(image_path, "JPEG")
            img = image
        elif step == 3:
            step = 4
            image = request.POST['image']
            caption = request.POST['caption']
            copyright = request.POST['copyright']
            f_path = string.split(image,"/")
            file_name = f_path[len(f_path)-1]
            new_path =  MEDIA_ROOT + "img/" + item.type.img_slug + "/" + file_name
            copy(MEDIA_ROOT + image, new_path)
            #handle_uploaded_file(MEDIA_ROOT + image, new_path)
            ursula_image = ursula.models.Image()
            ursula_image_list = ursula.models.Image_List()
            ursula_image.user_id = request.user.id
            ursula_image.src = "img/" + item.type.img_slug + "/" + file_name
            ursula_image.copyright = copyright
            ursula_image.is_active = True
            ursula_image.save();
            ursula_image_list.image_id = ursula_image.id
            ursula_image_list.item_id = item.id
            ursula_image_list.caption = caption
            ursula_image_list.ordinal = 1000
            ursula_image_list.is_active = False
            ursula_image_list.needs_admin = True
            ursula_image_list.save()
    
    return render_to_response('ursula/contribute/contribute-image.html',
        {
         'item': item,
         'step': step,
         'img': img
        }, context_instance=RequestContext(request)
    )


def handle_uploaded_file(f, file_path):
    destination = open(file_path, 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()





    