from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from ursula.models import Item
 
from djangosphinx.models import SphinxSearch

# -----------------------------------
# Search Results
# -----------------------------------
def results(request, query):
    type = request.REQUEST.get("t", "")
    exclude = request.REQUEST.get("ex", "")
    show = request.REQUEST.get("show", "")
    show_list = []
    page = request.REQUEST.get("page", "")
    item_results = ""
    book_results = ""
    no_results = False
    template = "ursula/search/results.html"
    
    collectible_list = "4|7|6|1|5|8"
    qs_collectible_list = [4,7,6,1,5,8]
    
    if show:
        show_list = show.split('|')
    
    #return HttpResponse(show);
    
    if(query == ''):
        query = request.REQUEST.get("query", "")
    qs = Item.search.query(query)
    #results = qs.filter(is_active = 1, type_id = 1)[0:1000]
    
    if type == "collectibles":
        template = "ursula/search/collectibles.html"
        if show_list:
            item_results = qs.filter(is_active = 1, type_id =show_list).order_by('-release_date', '@weight')[0:1000]
        else:
            item_results = qs.filter(is_active = 1, type_id =qs_collectible_list).order_by('-release_date', '@weight')[0:1000]
            show_list = collectible_list.split('|')
            
    elif type == "books":
        book_results = qs.filter(is_active = 1, type_id = 2).order_by('@weight')[0:1000]
        template = "ursula/search/books.html"
    else:
        item_results = qs.filter(is_active = 1, type_id =qs_collectible_list).order_by('-release_date', '-@weight')[0:14]
        book_results = qs.filter(is_active = 1, type_id = 2).order_by('-release_date', '-@weight')[0:12]
    
    
    over_limit = False
    if qs._sphinx['total_found'] > 1000:
       over_limit = True
    
    
    if qs._sphinx['total_found'] == 0:
        no_results = True 
    
    return render_to_response(template,
        {'item_results': list(item_results),
         'book_results': list(book_results),
         'query': query,
         'search_meta': qs._sphinx,
         'over_limit': over_limit,
         'type': type,
         'page': page,
         'show_list': show_list,
         'no_results': no_results,
        }, context_instance=RequestContext(request)
    )



