from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    url(r'^facebook/', include('facebookconnect.urls')),

    url(r'^$', 'views.index', name='index'),
    url(r'^sitemap.xml$', 'views.sitemap', name='sitemap'),

    ### Search ###
    url(r'^search/(.*)', 'html.ursula.search.views.results', name='search_results'),

   ### User Profile Functions ###
    url(r'^member/user-signed-in/$', 'ursula.member.views.usersignedin', name='user-signed-in'),
    url(r'^member/login/$', 'ursula.member.views.login', name='login'),
    url(r'^member/signout/$', 'ursula.member.views.signout', name='signout'),  
    (r'^member/', include('registration.backends.default.urls')),
    url(r'^mystuff/$', 'html.ursula.mystuff.views.index', name='mystuff'),

    ### Collectibles - Mystuff ###
    url(r'^mystuff/collectibles/add/$', 'html.ursula.mystuff.views.addmystuff', name='add-my-stuff'),
    url(r'^mystuff/collectibles/edit/(?P<mystuff_id>[0-9]+)/$', 'html.ursula.mystuff.views.editcollectible', name='edit-mystuff-id'),
    url(r'^mystuff/collectibles/remove/(?P<mystuff_id>[0-9]+)/$', 'html.ursula.mystuff.views.removecollectible', name='remove-mystuff-id'),
    url(r'^mystuff/collectibles/$', 'html.ursula.mystuff.views.mycollectibles', name='mycollectibles'),


    ### Collectibles - Wish List ###
    url(r'^mystuff/wishlist/add/$', 'html.ursula.mystuff.views.addwishlist', name='add-wishlist'),
    url(r'^mystuff/wishlist/edit/(?P<wishlist_id>[0-9]+)/$', 'html.ursula.mystuff.views.editwishlist', name='edit-wishlist-id'),
    url(r'^mystuff/wishlist/remove/(?P<wishlist_id>[0-9]+)/$', 'html.ursula.mystuff.views.removewishlist', name='remove-wishlist-id'),
    url(r'^mystuff/wishlist/$', 'html.ursula.mystuff.views.mywishlist', name='mywishlist'),

    url(r'^mystuff/books/$', 'html.ursula.mystuff.views.mybooks', name='mybooks'),


    #url(r'^mystuff/remove-wishlist(?P<mystuff_id>[0-9]+)/$', 'html.ursula.wishlist.views.remove', name='remove-mystuff-id'),
 
    url(r'^contribute/$', 'html.ursula.contribute.views.index', name='contribute-index'),
    url(r'^contribute/image/(?P<item_id>[0-9]+)/$', 'html.ursula.contribute.views.contributeimage', name='contribute-image'),

    ### ITEMS ###
    url(r'^collectibles/$', 'html.ursula.collectibles.views.index', name='collectible-index'),
    #url(r'^collectibles/(?P<type_slug>[-\w]+)/add-my-stuff/$', 'html.ursula.collectibles.views.addmystuff', name='collectible-item-addmystuff'),
    #url(r'^collectibles/(?P<type_slug>[-\w]+)/tag/(?P<tag_slug>[-\w]+)$', 'html.ursula.collectibles.views.taglist', name='collectible-list-tag'),
    url(r'^collectibles/(?P<type_slug>[-\w]+)/$', 'html.ursula.collectibles.views.list', name='collectible-list-type'),  
    url(r'^collectibles/(?P<type_slug>[-\w]+)/(?P<item_slug>[-\w]+)/$', 'html.ursula.collectibles.views.detail', name='collectible-item-detail'),

    ### Books ###
    url(r'^books/$', 'html.ursula.books.views.index', name='books-index'),
    url(r'^books/(?P<item_slug>[-\w]+)/$', 'html.ursula.books.views.detail', name='book-detail'),

    ### Podcasts ###
    url(r'^podcasts/$', 'html.ursula.podcasts.views.index', name='podcast-index'),
    url(r'^podcasts/(?P<item_slug>[-\w]+)/$', 'html.ursula.podcasts.views.detail', name='podcast-detail'),

    ### Blogs ###
    url(r'^blogs/$', 'html.ursula.blogs.views.index', name='blog-index'),
    url(r'^blogs/(?P<item_slug>[-\w]+)/$', 'html.ursula.blogs.views.detail', name='blog-detail'),    

    ### LOCATIONS ###
    url(r'^locations/$', 'ursula.locations.views.index', name='location-index'),
    url(r'^locations/(?P<location_slug>[-\w]+)$', 'ursula.locations.views.detail', name='location-detail'),
    ### TAGS ###
    url(r'^tags/$', 'ursula.tags.views.index', name='tag-index'),
    url(r'^tags/(?P<tag_slug>[-\w]+)$', 'ursula.tags.views.detail', name='tag-detail'),
    ### PEOPLE ###
    url(r'^people/$', 'ursula.people.views.index', name='people-index'),
    url(r'^people/(?P<person_slug>[-\w]+)$', 'ursula.people.views.detail', name='people-detail'),


    ### BLOG ###
    url(r'^news/$', 'html.ursula.news.views.index', name='news-index'),
    url(r'^news/feed/$', view='html.ursula.news.views.feed', name='news-feed'),
    url(r'^news/category/(?P<slug>[-\w]+)$', view='html.ursula.news.views.archive_category', name='news-category'),
    url(r'^news/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', view='html.ursula.news.views.detail', name='news-detail'),
    url(r'^news/(?P<year>\d{4})/(?P<month>\d{2})/$', view='html.ursula.news.views.archive_month', name='news-archive-month'),

	url(r'^about/$', view='html.ursula.pages.views.about', name='show-about'),
	url(r'^contact/$', view='html.ursula.pages.views.contact', name='show-contact'),
    	#(r'^_lib/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/www/vhosts/html.com/html/_lib'}),


)


