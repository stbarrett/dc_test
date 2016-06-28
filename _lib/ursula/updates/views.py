from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from decimal import *
from ursula.models import Item, ItemForm
import urllib



@login_required
def dailyupdate(request):
    update_date = request.REQUEST.get("update_date", "")
    items = ""
    if request.method == 'POST':
        d = update_date.split("/")
        items = Item.objects.all().filter(created_on__month = d[0], created_on__day = d[1], created_on__year = d[2], is_active = 1).order_by('type')
    
    
    return render_to_response('ursula/daily-updates/daily-update.html',
        {'items': items,
        }, context_instance=RequestContext(request)
    )

    
    
    
    
    
    
    
    
    
    
    

        