# coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import Template,RequestContext, loader, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required
from photologue.models import Photo
from django.http import HttpResponse
# Create your views here.
from datetime import tzinfo, timedelta, datetime
from django.views.decorators.cache import never_cache
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import ugettext_noop
from django.utils.translation import get_language
from ncatalogue import models as ncatalogue_models
from django.db.models import Q,F
from shops import models as shop_models

PPP = settings.NCATALOGUE_PRODUCTS_PER_PAGE
index_page_html = settings.INDEX_PAGE_HTML
product_page_html = settings.PRODUCT_PAGE_HTML

def index(request):
#  print request.session.session_key
#  print request.shop
#  try:
#    print request.session['has_commented']
#  except:
#    print "no"
#  request.session['has_commented'] = 'fffff'
  #print request.session['has_commented']
  categories_all = ncatalogue_models.Category.objects.filter(is_operating = True, shop=request.shop)
  products = ncatalogue_models.Product.objects.filter(
  	  Q(categories = categories_all[0]) | Q(categories__parent=categories_all[0])
  	).distinct()
  params = {  
  	'products' : products,
  	'show_breadcrumb' : True,
  }
  return render_to_response(index_page_html, params, context_instance = RequestContext(request))

def category_list(request,category_slug):
  category = ncatalogue_models.Category.objects.get(slug = category_slug)
  products = ncatalogue_models.Product.objects.filter(
  	  Q(categories = category) | Q(categories__parent=category)
  	).distinct()
  params = {  
  	'products' : products,
  	'show_breadcrumb' : True,
  	'category' : category
  }
  return render_to_response(index_page_html, params, context_instance = RequestContext(request))


def productpage(request,product_id):
  categories = ncatalogue_models.Category.objects.filter(is_operating = True)
  product = ncatalogue_models.Product.objects.get(id = product_id)
  try:
    child_category = product.categories.filter(is_operating = True).exclude(parent=None)[0]
  except:
    child_category = product.categories.filter(is_operating = True)[0]
  might_like_products = ncatalogue_models.Product.objects.filter(
  	  Q(categories = categories[0]) | Q(categories__parent=categories[0])
  	).exclude(id=product_id).distinct()
  params = {  
  	'product' : product,
  	'child_category' : child_category,
  	'might_like_products' : might_like_products,
  	'show_breadcrumb' : True
  }
  return render_to_response(product_page_html, params, context_instance = RequestContext(request))