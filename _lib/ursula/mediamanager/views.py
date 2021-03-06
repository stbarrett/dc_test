import os
import fnmatch
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

# helper class to pass to template so a file
# can be display properly
class MediaFile:
    def __init__(self, name, size, file_path):
        self.name = name
        self.size = size
        self.file_path = file_path

def index(request):
    file_pattern = request.REQUEST.get('folderSearch', '')
    prefix = request.REQUEST.get("prefix", "")
    prefix = prefix.lstrip('/')
    up_prefix = ""
    media_url = settings.MEDIA_URL + prefix
    path = settings.MEDIA_ROOT + prefix
    listing = os.listdir(path)
    files = []
    directories = []
    
    # build 'up' value
    prefix_split = prefix.split('/')
    if len(prefix_split) >= 1:
        prefix_split.pop()

    up_prefix = "/".join(prefix_split)        
 
    # create list of directories and files
    for item in listing:
        if item != "_adjusted": # these are our autogenerated images, we don't care about them
            if os.path.isdir(os.path.join(path, item)):
                directories.append(item)
            else: 
                if file_pattern:
                    if fnmatch.fnmatch(item, "*"+file_pattern+"*"):
                        file_path = prefix.lstrip('/') + '/' + item
                        f = MediaFile(item, 1, file_path)
                        files.append(f)
                else:
                    file_path = prefix.lstrip('/') + '/' + item
                    f = MediaFile(item, 1, file_path)
                    files.append(f)
    
    return render_to_response('ursula/mediamanager/view.html',
        { 'path': path,
          'files': files,
          'directories': directories,
          'up_prefix': up_prefix,
          'prefix': prefix,
          'media_url': media_url,
          'file_pattern': file_pattern,
        }, context_instance=RequestContext(request)
    )


def upload(request):
    
    if request.method == 'POST':
        file = request.FILES['Filedata']
        prefix = request.POST['prefix']
        path = settings.MEDIA_ROOT + prefix + "/" + file.name
        f = open(path, 'wb+')
        for chunk in file.chunks():
            f.write(chunk)
        return HttpResponse("ok")
    
    
    
    if request.method == 'GET':
        return render_to_response('ursula/mediamanager/upload.html',
        {}, context_instance=RequestContext(request))



def add_dir(request):
    path = request.POST.get('path', '')
    path = settings.MEDIA_ROOT + path
    os.makedirs(path)
    return HttpResponse("")
    
    
    
    


