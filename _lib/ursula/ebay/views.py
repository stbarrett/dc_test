from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from ursula.models import Ebay_Item

def delete(request, id=None):
    ebay_items = Ebay_Item.objects.all().filter(ebay_item_id = id)
    try:
        for item in ebay_items:
            item.is_active = 0
            item.needs_admin = 0
            item.save()
    except:
        return HttpResponse(0)
    
    return HttpResponse(1)
    
def approve(request, id=None):
    ebay_items = Ebay_Item.objects.all().filter(ebay_item_id = id)
    try:
        for item in ebay_items:
            item.needs_admin = 0
            item.is_active = 1
            item.save()
    except:
        return HttpResponse(0)

    return HttpResponse(1)    
