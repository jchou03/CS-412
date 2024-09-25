from django.shortcuts import render
import time
import random

# Create your views here.
def main(request):
    '''The main page for Papa Petryk's Pizza Palace'''
    template_name = "restaurant/home.html"
    context ={
        "current_time": time.ctime(),
    }
    
    return render(request, template_name, context)

def order(request):
    '''The ordering page to create an online order'''
    template_name = "restaurant/order.html"
    
    menu_items=[
        {
            "name": "Cheese Pizza",
            "price": 10,
        },
        {
            "name": "BBQ Chicken Pizza",
            "price": 15,
        },
        {
            "name": "Garlic Knots",
            "price": 8,
        },
        {
            "name": "Calzone",
            "price": 11
        }
    ]
    
    daily_specials = [
        {
            "name": "Moose Milk",
            "price": 25,
        },
        {
            "name": "Poutine",
            "price": 17
        },
        {
            "name": "Beaver Tail",
            "price": 22
        },
        {
            "name": "Ketchup Chips",
            "price": 5
        }
    ]
    
    context ={
        "current_time": time.ctime(),
        "menu_items": menu_items,
        "daily_special": random.choice(daily_specials),
    }
    return render(request, template_name, context)