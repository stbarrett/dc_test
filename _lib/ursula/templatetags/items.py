from django import template
from django.template import Library, Node, TemplateSyntaxError 
register = template.Library()
                            
@register.filter(name='first_image')
def first_image(obj):
    return obj.first_image()

@register.filter(name='first_image_copyright')
def first_image_copyright(obj):
    return obj.first_image_copyright()


# resize amazon images via their nameing scheme
#._SL100_AA100_.jpg -- SLheight_AAWIDTH -- these are maximum height/widths
   
## Create Node
class AmazonImgResizeNode(template.Node):
    def __init__(self, img, max_side):
        self.img = template.Variable(img)
        self.max_side = max_side
        
    def render(self, context):
        img_str = self.img.resolve(context).split(".")
        img_path = img_str[0] + "." + img_str[1] + "." +  img_str[2] + "._SL"+self.max_side+"_.jpg"
        
        return img_path

#parser
def amazon_img_resize(parser, token):
  try:
      tag_name, img, max_side = token.split_contents();
  except ValueError:
    raise template.TemplateSyntaxError, "%r tag requires exactly 2 arguments" % token.contents.split()[0]

  return AmazonImgResizeNode(img, max_side)  


register.tag('amazon_img_resize', amazon_img_resize)
