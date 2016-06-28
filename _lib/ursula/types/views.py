from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django import forms
from django.template.defaultfilters import slugify
from ursula.models import Type, TypeForm


@login_required
def index(request):
    type_list = Type.objects.all().order_by('id')
    return render_to_response('ursula/types/type-list.html',
        {'type_list': type_list
        }, context_instance=RequestContext(request)
    )

@login_required
def edit(request, id=""):
    submit_action = ''
    edit_id = id
    form = TypeForm()
    if request.method == 'POST':
        if request.POST['submit_action'] == 'Add':
          form = TypeForm(request.POST)
          if form.is_valid():
            form.save()
            return HttpResponseRedirect('/types/') # Redirect after POST
          else:
            submit_action = 'Add'
        if request.POST['submit_action'] == 'Update':
            form = TypeForm(request.POST, instance=Type.objects.get(pk=id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/types/')
            else:
                submit_action = 'Update'
    if request.method == 'GET':
        if id:
            submit_action = 'Update'
            type = get_object_or_404(Type, pk=id)
            form = TypeForm(instance=type)
           
        else:
            submit_action = 'Add'

    return render_to_response(
        'ursula/types/type-edit.html',
        { 'request': request,
          'form': form,
          'submit_action': submit_action,
          'edit_id': edit_id
        }
      ) 
    