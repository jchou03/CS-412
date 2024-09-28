from django.shortcuts import redirect, render
import time
import random

menu_items=[
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
    },
    {
        "name": "Cheese Pizza",
        "price": 10,
    },
    {
        "name": "Pepperoni (topping)",
        "price": 2
    },
    {
        "name": "Mushroom (topping)",
        "price": 2
    },
    {
        "name": "Olives (topping)",
        "price": 2
    },
    {
        "name": "Maple Syrup (topping)",
        "price": 3
    }
]

daily_specials = [
    {
        "name": "Moose Melk",
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

# Create your views here.
def main(request):
    '''The main page for Papa Petryk's Pizza Palace'''
    template_name = "restaurant/main.html"
    context ={
        "current_time": time.ctime(),
    }
    
    return render(request, template_name, context)

def order(request):
    '''The ordering page to create an online order'''
    template_name = "restaurant/order.html"
    
    context ={
        "current_time": time.ctime(),
        "menu_items": menu_items,
        "daily_special": random.choice(daily_specials),
    }
    return render(request, template_name, context)

def confirm(request): 
    template_name="restaurant/confirmation.html"
    
    print("request info:")
    print(request)
    # read form data
    if request.POST:
        print(request.POST)
        name=request.POST["name"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        comments=request.POST["comments"]
        
        ordered_items = [item for item in request.POST if not (item in ["name", "phone", "email", "csrfmiddlewaretoken", "comments"])]
        total_cost = 0
        
        for item in menu_items:
            if item["name"] in ordered_items:
                total_cost += item["price"]

        for item in daily_specials:
            if item["name"] in ordered_items:
                total_cost += item["price"]
        
        current_time = time.ctime()
        ready_time = time.ctime(time.time() + (random.randint(30,60) * 60))
        context={
            "name": name,
            "phone": phone,
            "email": email,
            "ordered_items":ordered_items,
            "total_cost": total_cost,
            "ready_time": ready_time,
            "current_time": current_time,
            "comments": comments,
        }
        
        return render(request, template_name, context)
    else:
        return redirect("/restaurant")