# blog/views.py
# views to show the blog application
from django.shortcuts import render

from . models import *
from django.views.generic import *
import random
from . forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.
class ShowAllView(ListView):
    '''a view to show all articles'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"
    
    def dispatch(self, *args, **kwargs):
        '''every time this class is called this method is called'''
        print(f'self.request.user={self.request.user}')
        return super().dispatch(*args, **kwargs)
        
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
        
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''a view to show/process the create Article form:
    on GET: sends back the form
    on POST: read form data, create an instance of comment'''
    
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
    login_url="login"
    # or could also define the 'get_login_url' function
    
    def form_valid(self, form):
        '''add debugging statements'''
        print(f'CreateArticleView.form_valid: form.cleaned_data={form.cleaned_data}')
        
        # find the user logged in
        user = self.request.user
        print(f'CreateArticleView:form_valid() user={user}')
        form.instance.user = user
        
        # delegate work to superclass
        return super().form_valid(form)
    
class RegistrationView(CreateView):
    '''display and process the user creation form for account registration'''
    
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    
    def dispatch(self, *args, **kwargs):
        '''function that is called first on any generic view to deal with a request'''
        '''handle the user creation process'''
        
        # we handle the POST request
        if self.request.POST:
            # testuser: inclassexample
            # banana: isafruit
            # reconstruct UserCreationForm from HTTP POST
            print(f"self.request.POST={self.request.POST}")
            # save the new user object
            form = UserCreationForm(self.request.POST)
            if not form.is_valid():
                print(f"form.errors={form.errors}")
                # if there is an error, just let the CreateView superclass handle this
                return super().dispatch(*args, **kwargs)
                
            user = form.save() # creates a new instance of the User object in the database
            print(f'RegistrationView.dispatch: created user {user}')

            # log in the user
            login(self.request, user)
            print(f'user is logged in')
            
            # mini_fb note:
            # need to attach the newly created user to the new Profile being created
            
            # return result
            return redirect((reverse('show_all')))
        
        # let superclass handle GET request
        return super().dispatch(*args, **kwargs)