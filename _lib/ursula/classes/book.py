from django.conf import settings
from xml.etree import ElementTree
from boto.connection import AWSQueryConnection

import time
import datetime
import urllib


#http://jjinux.blogspot.com/2009/06/python-amazon-product-advertising-api.html


class AmazonBookCreator:
    name = ""
    role = ""
    
    
class AmazonEditorial:
    source = ""
    content = ""
    
class AmazonBook:
    raw_xml = ""
    title = ""
    description = ""
    editorial_reviews = []
    ASIN = ""
    ISBN = ""
    authors = []
    binding = ""
    tiny_image = ""
    med_image = ""
    lrg_image = ""
    list_price = ""
    sale_price = ""
    percentage_saved = ""
    amount_saved = ""    
    creators = []
    publisher = ""
    publication_date = ""
    pages = ""
    detail_url = ""
    edition = ""
    
    def __init__(self):
        self.editorial_reviews = []
        self.authors = []
        self.creators = []
    
    
    # url - http://www.amazon.com/exec/obidos/ASIN/1423116534/<affiliate id>
    def create_amazon_book_by_asin(self, asin):

        AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
        AWS_ASSOCIATE_TAG = settings.AWS_ASSOCIATE_TAG
        AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
                
        search_index = 'Book'
        aws_conn = AWSQueryConnection(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, is_secure=False,
            host='ecs.amazonaws.com')
        aws_conn.SignatureVersion = '2'
        params = dict(
            Service='AWSECommerceService',
            Version='2008-08-19',
            SignatureVersion=aws_conn.SignatureVersion,
            AWSAccessKeyId=AWS_ACCESS_KEY_ID,
            AssociateTag=AWS_ASSOCIATE_TAG,
            Operation='ItemLookup',
            ItemId=asin,
            ResponseGroup='ItemAttributes,Large, Images,Reviews',
            Timestamp=time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()))
        verb = 'GET'
        path = '/onca/xml'
        qs, signature = aws_conn.get_signature(params, verb, path)
        qs = path + '?' + qs + '&Signature=' + urllib.quote(signature)
        #print "verb:", verb, "qs:", qs
        response = aws_conn._mexe(verb, qs, None, headers={})
        returned_xml = self.raw_xml = myxml = str(response.read())
        
        returned_xml = returned_xml.replace(" xmlns=\"http://webservices.amazon.com/AWSECommerceService/2008-08-19\"", '')
        
        doc = ElementTree.fromstring(returned_xml)
        

        try:
            self.title = doc.find('Items/Item/ItemAttributes/Title').text
        except:
            self.title = ""
            
        #self.author = doc.find('Items/Item/ItemAttributes/Author').text
        author_list = doc.findall('Items/Item/ItemAttributes/Author')
        for a in author_list:
            self.authors.append(a.text)
        try:
            self.edition = doc.find('Items/Item/ItemAttributes/Edition').text
        except:
            self.edition = ""
        try:
            self.list_price = doc.find('Items/Item/ItemAttributes/ListPrice/FormattedPrice').text
        except AttributeError:
            self.list_price = ""
        try:
            self.sale_price = doc.find('Items/Item/Offers/Offer/OfferListing/Price/FormattedPrice').text
        except AttributeError:
            self.sale_price = ""
        try:
            self.amount_saved = doc.find('Items/Item/Offers/Offer/OfferListing/AmountSaved/FormattedPrice').text
        except AttributeError:
            self.amount_saved = ""
        try:
            self.percentage_saved = doc.find('Items/Item/Offers/Offer/OfferListing/PercentageSaved').text
        except AttributeError:
            self.percentage_saved = ""
        try:
            self.ISBN = doc.find('Items/Item/ItemAttributes/ISBN').text
        except AttributeError:
            self.ISBN = ""
        try:
            self.ASIN = doc.find('Items/Item/ASIN').text
        except:
            self.ASIN = ""
        try:
            self.binding = doc.find('Items/Item/ItemAttributes/Binding').text
        except:
            self.binding = ""
            
        try:
            self.detail_url = doc.find('Items/Item/DetailPageURL').text
        except:
            self.detail_url = ""
            
        try:
            temp_date = doc.find('Items/Item/ItemAttributes/PublicationDate').text
        except:
            self.date = ""
        try:
            # convert to struct_time, then to datetime obj
            c = time.strptime(temp_date,"%Y-%m-%d")
            d = datetime.datetime(*c[:6])
            self.publication_date = d
        except:
            self.publication_date = ""

        try:
            self.publisher = doc.find('Items/Item/ItemAttributes/Publisher').text   # this should be a tag so it becomes a link to view more books by publisher
        except:
            self.publisher = ""
        try:
            self.pages = doc.find('Items/Item/ItemAttributes/NumberOfPages').text
        except AttributeError:
            self.page= ""
        try:
            self.lrg_image = doc.find('Items/Item/LargeImage/URL').text
        except AttributeError:
            self.lrg_img = ""
            
        try:
            self.med_image = doc.find('Items/Item/MediumImage/URL').text
        except AttributeError:
            self.med_image= ""
            
        try: 
            self.tiny_image = doc.find('Items/Item/ImageSets/ImageSet/TinyImage/URL').text
        except AttributeError:
            self.tiny_image = ""
        editorials = doc.findall('Items/Item/EditorialReviews/EditorialReview')
        for reviews in editorials:
            if reviews.find('Source').text == "Product Description":
                self.description = reviews.find('Content').text
            else:
                ed = AmazonEditorial()
                ed.source = reviews.find('Source').text
                ed.content = reviews.find('Content').text
                self.editorial_reviews.append(ed)
                
            
        creators = doc.findall('Items/Item/ItemAttributes/Creator')
        
        for creator in creators:
            cr = AmazonBookCreator()
            cr.name = creator.text
            cr.role = creator.attrib['Role']
            self.creators.append(cr)
            
            