from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings

from ursula.models import Image


    
def clean_image_path(request):
   images = Image.objects.all()
   
   for img in images:
       if img.src != "":
           if img.src[0] == '/':
               img.src = img.src.lstrip('/')
               img.save()

        
   return HttpResponse('done')
    
    

    
    
    