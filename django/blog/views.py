# blog/views.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import *
import random

# Create your views here.
class ShowAllView(ListView):
    '''a view to show all articles'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"
    
    
class RandomArticleView(DetailView):
    '''a view to show one article at random'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" 
        # singular name
        
    # AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one solution: implement get_object method
    def get_object(self):
        '''return the instancec of the Article object to show'''
        # get all articles
        all_articles = Article.objects.all()
            # SELECT *
        # pick one at random
        return random.choice(all_articles)

    
class ArticleView(DetailView):
    '''a view to show one specific article'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" 
        # singular name