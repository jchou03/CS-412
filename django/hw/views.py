# hw/views.py
# description: logic to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse
import time
import random

# Create your views here.

# def home(request): # use same name for function as used in url path
#     '''a function to respond to the /hw URL.''' # docstring (required for every function)
    
#     # create text
#     response_text = f'''
#     <html>
#     <body>
#     <h1>Hello world!</h1>
#     <p>This is our first Django web page!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </body>
#     </html>
#     '''
    
#     # return response to client
#     return HttpResponse(response_text)
    
def home(request): 
    '''
    A function to respond to the /hw URL.
    This function will delegate work to an HTML template
    '''
    
    # template will present response
    template_name = "hw/home.html"
    
    # create dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65,90)), # letter in range A to Z
        'letter2': chr(random.randint(65,90)), 
        'number': random.randint(1,10),
    }
    
    # delegate response to template
    return render(request, template_name=template_name, context=context)
    