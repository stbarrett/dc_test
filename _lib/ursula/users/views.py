from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# -----------------------------------
# User List
# -----------------------------------
@login_required
def users(request):
    user_list = User.objects.all().order_by('id')
    return render_to_response('ursula/users/user-list.html',
        {'user_list': user_list
        }, context_instance=RequestContext(request)
    )