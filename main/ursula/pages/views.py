from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags, escape
from datetime import datetime
from django.contrib.sites.models import Site
from akismet import Akismet

from django.core.mail import send_mail

from ursula.models import Page

# -----------------------------------
# About Page
# -----------------------------------
def about(request):
    page = get_object_or_404(Page, slug='about', is_active=True)
    
    return render_to_response('ursula/pages/show.html',
        {
         'page': page,
         'stripped_content': escape(strip_tags(page.content)),
        }, context_instance=RequestContext(request)
    )    


# -----------------------------------
# Contact Page
# -----------------------------------
def contact(request):
    page = get_object_or_404(Page, slug='contact', is_active=True)
    msg = ""
    if request.method == 'POST':
        msg = "<p>Thank you for submitting our contact form.</p>"
        name = request.REQUEST.get("name", "")
        email = request.REQUEST.get("email", "")
        subject = request.REQUEST.get("subject", "")
        comment = request.REQUEST.get("comment", "")

        send_mail('Contact: '+subject, "From: " + name + "\r\n\r\n" + comment, email,
                  [settings.CONTACT_EMAIL], fail_silently=False)


    
    return render_to_response('ursula/pages/show.html',
        {
         'page': page,
         'msg': msg,
         'stripped_content': 'Contact Us with any questions or comments you have.',
        }, context_instance=RequestContext(request)
    )    
