# blog/views.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import *
import random
from . forms import *

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
        
class CreateArticleView(CreateView):
    '''a view to show/process the create Article form:
    on GET: sends back the form
    on POST: read form data, create an instance of comment'''
    
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
    
    def form_valid(self, form):
        '''add debugging statements'''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')
        # delegate work to superclass
        return super().form_valid(form)
    