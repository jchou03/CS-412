# blog/models.py
# define data models (objects) for use in blog application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    '''encapsulate data for an Article by some author'''
    
    # each Article will be associated with a django User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # data attributes:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True) ## new field
    
    
    def __str__(self):
        '''create string representation'''
        return f"{self.title} by {self.author}"

    def get_comments(self):
        '''retrieve all comments for this article'''
        # use ORM to filter Comments where this object is the foreign key
        # instance of Article is the Foreign Key
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        '''return the url to view one article'''
        return reverse("article", kwargs={'pk': self.pk})

class Comment(models.Model):
    '''encapsulate comment on an article'''
    # create 1 to many relationship between Articles and COmments
    article = models.ForeignKey("Article", on_delete=models.CASCADE) ### IMPORTANT
        # on_delete = what to do when the foreign key gets deleted
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''return string representation of this object'''
        return f'{self.text}'

