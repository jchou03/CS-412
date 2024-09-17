# hw/views.py
# description: logic to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request): # use same name for function as used in url path
    '''a function to respond to the /hw URL.''' # docstring (required for every function)
    
    # create text
    response_text ='''
    <html>
    <body>
    <h1>Hello world!</h1>
    <p>This is our first Django web page!</p>
    </body>
    </html>
    '''
    
    # return response to client
    return HttpResponse(response_text)
    