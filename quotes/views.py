# quotes/views.py

from django.shortcuts import render
from django.http import HttpResponse
import time
import random

quotes = [
    "Savor the food!",
    "I'm just a girl",
    "Austin, what's another quote?",
    "Can you do my homework?",
    "That's a huge butt plug Austin!",
    "I love playing with butt plugs",
    "FIND ME A MAN!"
]
images = [
    "https://cdn.discordapp.com/attachments/1216782696303431860/1286802722669989928/IMG_1830.JPG?ex=66ef3bec&is=66edea6c&hm=415c7a3285ce660f1cf58bb932c7bb42c82b5abaf24fd3196a51fd7e4ab3827e&",
    "https://cdn.discordapp.com/attachments/1216782696303431860/1286802722896609371/IMG_1648.JPG?ex=66ef3bec&is=66edea6c&hm=2bf55c6fff68fa2b318846d9c9833d89539d1c914bf7ea9ee08effb5bf8f29cf&",
    "https://cdn.discordapp.com/attachments/1216782696303431860/1286802723173568522/IMG_9986.JPG?ex=66ef3bec&is=66edea6c&hm=d42de9aa19a4fa076256941f61a5d3b64e2cc809fcde3aade3a9dd92f7087b5f&"
]

# Create your views here.
def quote(request):
    '''function to respond to the / and /quoteurl'''
    template_name = "quotes/quote.html"
    context = {
        "current_time": time.ctime(),
        "quote": random.choice(quotes),
        "image_source": random.choice(images),
    }
    return render(request, template_name=template_name, context=context)

def show_all(request):
    template_name="quotes/show_all.html"
    context = {
        "current_time": time.ctime(),
        "all_quotes": quotes,
        "all_images": images,
    }
    return render(request, template_name=template_name, context=context)

def about(request):
    template_name="quotes/about.html"
    context = {
        "current_time": time.ctime(),
        "all_quotes": quotes,
        "all_images": images,
    }
    return render(request, template_name=template_name, context=context)