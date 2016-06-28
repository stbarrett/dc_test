from django import template
from django.template import Library, Node, TemplateSyntaxError
from ursula.models import Post, PostCategory, PostCategoryList
register = template.Library()
                            
@register.filter(name='show_summary')
def show_summary(obj):
    split_content = obj.content.split("<p><!-- pb --></p>")
    return split_content[0]


# -----------------------------------
# Get Archive Dates for sidebar
# -----------------------------------
class ArchiveNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        dates = Post.objects.dates('publish_date', 'month', order='DESC').filter(is_active = 1)
        if dates:
            context[self.varname] = dates
        return ''

#parser
def do_sidebar_archive(parser, token):
    tokens = token.contents.split()
    return ArchiveNode(tokens[2])

register.tag('sidebar_archive', do_sidebar_archive)

# -----------------------------------
# Get Categories for sidebar
# -----------------------------------
class CategoriesNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        cats = PostCategory.objects.all().order_by('title').filter(is_active = 1)
        final_cats = []
        for cat in cats:
            cat_test = PostCategoryList.objects.all().filter(post_category = cat, is_active = 1)
            if cat_test:
                final_cats.append(cat)
                
        if cats:
            context[self.varname] = final_cats
        return ''

#parser
def do_sidebar_categories(parser, token):
    tokens = token.contents.split()
    return CategoriesNode(tokens[2])

register.tag('sidebar_categories', do_sidebar_categories)

# -----------------------------------
# Get Categories for a post
# sorted by title
# -----------------------------------
class CategoriesForPostNode(template.Node):
    def __init__(self, varname, post_id):
        self.varname = varname
        self.post_id = post_id
        
    def render(self, context):
        post_id = template.resolve_variable(self.post_id, context)
        cats = PostCategoryList.objects.all().filter(is_active = 1, post = post_id).order_by('post_category__title')
        if cats:
            context[self.varname] = cats
        return ''

#parser
def do_post_categories(parser, token):
    tokens = token.contents.split()
    return CategoriesForPostNode(tokens[2], tokens[3])

register.tag('post_categories', do_post_categories)



# -----------------------------------
# Admin, don't show cats a post
# already has
# -----------------------------------
class PostCategoryNode(template.Node):
    def __init__(self, varname, current_cats):
        self.varname = varname
        self.current_cats = current_cats
        
    def render(self, context):
        cats = []
        show_cats = []
        current_cats = template.resolve_variable(self.current_cats, context)
        #for cat in self.current_cats:
        #    cats.append(self.current_cats.postcategory.id)
            
        new_cats = PostCategory.objects.all().filter(is_active = 1).order_by('-title')
        for new_cat in new_cats:
            remove = False
            for c in current_cats:
                if new_cat.id == c.post_category.id:
                    if c.is_active == True:
                        remove = True
            if not remove:
                show_cats.append(new_cat)
        context[self.varname] = show_cats
        #context[self.varname] = show_cats
        return ''

#parser
def do_list_PostCategory(parser, token):
    tokens = token.contents.split()
    return PostCategoryNode(tokens[2], tokens[3])


register.tag('list_post_categories', do_list_PostCategory)
