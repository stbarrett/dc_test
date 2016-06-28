from django.template import Library, Node, TemplateSyntaxError  
from django import template  
from django.template import resolve_variable 
from BeautifulSoup import BeautifulSoup, Comment
from django.forms import ChoiceField, FileField
import re
import math

from django import template
register = template.Library()

size_pat = re.compile(r'(\d+)x(\d+)$')

filesize_formats = ['k', 'm', 'G', 'T', 'P', 'E', 'Z', 'Y']
filesize_long_formats = {
    'k': 'kilo', 'M': 'mega', 'G': 'giga', 'T': 'tera', 'P': 'peta',
    'E': 'exa', 'Z': 'zetta', 'Y': 'yotta',
}

@register.filter(name='file_size')
## THIS WAS RIPPED FROM THE SNORL APPLICATION
def file_size(bytes): 
    format='auto1000'
    """
    Returns the number of bytes in either the nearest unit or a specific unit
    (depending on the chosen format method).

    Acceptable formats are:

    auto1024, auto1000
      convert to the nearest unit, appending the abbreviated unit name to the
      string (e.g. '2 KiB' or '2 kB').
      auto1024 is the default format.
    auto1024long, auto1000long
      convert to the nearest multiple of 1024 or 1000, appending the correctly
      pluralized unit name to the string (e.g. '2 kibibytes' or '2 kilobytes').
    kB, MB, GB, TB, PB, EB, ZB or YB
      convert to the exact unit (using multiples of 1000).
    KiB, MiB, GiB, TiB, PiB, EiB, ZiB or YiB
      convert to the exact unit (using multiples of 1024).

    The auto1024 and auto1000 formats return a string, appending the correct
    unit to the value. All other formats return the floating point value.

    If an invalid format is specified, the bytes are returned unchanged.
    """
    format_len = len(format)
    # Check for valid format
    if format_len in (2, 3):
        if format_len == 3 and format[0] == 'K':
            format = 'k%s' % format[1:]
        if not format[-1] == 'b' or format[0] not in filesize_formats:
            return bytes
        if format_len == 3 and format[1] != 'i':
            return bytes
    elif format not in ('auto1024', 'auto1000',
                        'auto1024long', 'auto1000long'):
        return bytes
    # Check for valid bytes
    try:
        bytes = long(bytes)
    except (ValueError, TypeError):
        return bytes

    # Auto multiple of 1000 or 1024
    if format.startswith('auto'):
        if format[4:8] == '1000':
            base = 1000
        else:
            base = 1024
        logarithm = bytes and math.log(bytes, base) or 0
        index = min(int(logarithm) - 1, len(filesize_formats) - 1)
        if index >= 0:
            if base == 1000:
                bytes = bytes and bytes / math.pow(1000, index + 1)
            else:
                bytes = bytes >> (10 * (index))
                bytes = bytes and bytes / 1024.0
            unit = filesize_formats[index]
        else:
            # Change the base to 1000 so the unit will just output 'B' not 'iB'
            base = 1000
            unit = ''
        if bytes >= 10 or ('%.1f' % bytes).endswith('.0'):
            bytes = '%.0f' % bytes
        else:
            bytes = '%.1f' % bytes
        if format.endswith('long'):
            unit = filesize_long_formats.get(unit, '')
            if base == 1024 and unit:
                unit = '%sbi' % unit[:2]
            unit = '%sbyte%s' % (unit, bytes != '1' and 's' or '')
        else:
            unit = '%s%s' % (base == 1024 and unit.upper() or unit,
                             base == 1024 and 'iB' or 'b')

        return '%s %s' % (bytes, unit)

    if bytes == 0:
        return bytes
    base = filesize_formats.index(format[0]) + 1
    # Exact multiple of 1000
    if format_len == 2:
        return bytes / (1000.0 ** base)
    # Exact multiple of 1024
    elif format_len == 3:
        bytes = bytes >> (10 * (base - 1))
        return bytes / 1024.0
    


class TruncateNode(Node):  
  def __init__(self, value, cutoff):  
    self.value, self.cutoff = value, cutoff  
  
  def render(self, context):  
    truncated = template.resolve_variable(self.value, context)  
    size = int(template.resolve_variable(self.cutoff, context))  
    if len(truncated) > size and size > 3:  
      truncated = truncated[0:(size - 3)] + '...'  
  
    return truncated  
  
def truncate(parser, token):  
  bits = token.contents.split()  
  if len(bits) != 3:  
    raise TemplateSyntaxError, "truncate takes exactly two arguments, string, size"  
  return TruncateNode(bits[1], bits[2])  
  
register.tag('truncate', truncate)  


#http://www.djangosnippets.org/snippets/205/
#modified to handle input tags to ignore
#def sanitize_html(value):
#    valid_tags = 'p i strong b u a h1 h2 h3 pre br img'.split()
#    valid_attrs = 'href src'.split()
#    soup = BeautifulSoup(value)
#    for comment in soup.findAll(
#        text=lambda text: isinstance(text, Comment)):
#        comment.extract()
#    for tag in soup.findAll(True):
#        if tag.name not in valid_tags:
#            tag.hidden = True
#        tag.attrs = [(attr, val) for attr, val in tag.attrs
#                     if attr in valid_attrs]
#    return soup.renderContents().decode('utf8').replace('javascript:', '')

#register.filter('sanitize', sanitize_html)


## Create Node
class SanitizeHtmlNode(template.Node):
    def __init__(self, data):
        self.data = data
        #self.tags = tags
        
    def render(self, context):
        #br
        valid_tags = 'p i strong b u a h1 h2 h3 pre img'.split()
        valid_attrs = 'href src'.split()
        soup = BeautifulSoup(template.resolve_variable(self.data, context)  )
        for comment in soup.findAll(
            text=lambda text: isinstance(text, Comment)):
            comment.extract()
        for tag in soup.findAll(True):
            if tag.name not in valid_tags:
                tag.hidden = True
            tag.attrs = [(attr, val) for attr, val in tag.attrs
                         if attr in valid_attrs]
        return soup.renderContents().decode('utf8').replace('javascript:', '')

#parser
def sanitize_html(parser, token):
  try:
      tag_name, data = token.split_contents();
  except ValueError:
    raise template.TemplateSyntaxError, "%r tag requires exactly 1 arguments" % token.contents.split()[0]

  return SanitizeHtmlNode(data)  


register.tag('sanitize_html', sanitize_html)
















