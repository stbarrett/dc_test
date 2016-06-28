from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

# -----------------------------------
# Sign in Member
# -----------------------------------
def login(request):
    if request.method == 'GET':
        next = request.REQUEST.get("next", "")
        return render_to_response('ursula/member/signin.html',
            {'next': next,
            }, context_instance=RequestContext(request)
        )

    if request.method == 'POST':
        username = request.REQUEST.get("username", "")
        password = request.REQUEST.get("password", "")
        next = request.REQUEST.get("next", "/")
        

            
        # django built in auth call
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                #return HttpResponse(user.username)
                return HttpResponseRedirect(next)
            #else:
                # Return a 'disabled account' error message
        else:
            return render_to_response('ursula/member/signin.html',
            {'error': "true",
            }, context_instance=RequestContext(request)
        )
            
            
# -----------------------------------
# Sign out Member
# -----------------------------------
def signout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


# -----------------------------------
# Check if user is signed in
# return true || false
# -----------------------------------
def usersignedin(request):
    if not request.user.is_authenticated():
        return HttpResponse("0")
    else:
        return HttpResponse("1")