from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from rango.models import Category
from rango.models import Page

from rango.forms import CategoryForm

def index(request):
	context = RequestContext(request)
	category_list = Category.objects.order_by('-likes')
	top_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'top_pages': top_list}

	for category in category_list:
		category.url = create_url(category.name)

	return render_to_response('rango/index.html', context_dict, context)

def category(request, category_name_url):
	context = RequestContext(request)
	category_name = create_name(category_name_url)
	context_dict = {'category_name': category_name}

	try:
		category = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass

	return render_to_response('rango/category.html', context_dict, context)

def about(request):
	return HttpResponse("Rango Says: Here is the about page. <a href='/rango/'>Index</a>")

def add_category(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return HttpResponseRedirect('/rango/')
		else:
			print form.errors
	else:
		form = CategoryForm()

	return render_to_response('rango/add_category.html', {'form': form}, context)


def create_url(name):
	url = name.replace(' ', '_')
	return url

def create_name(url):
	name = url.replace('_', ' ')
	return name