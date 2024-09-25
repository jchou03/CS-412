from django.shortcuts import render
import time

# Create your views here.
def main(request):
    template_name = "restaurant/home.html"
    context ={
        "current_time": time.ctime(),
    }
    
    return render(request, template_name, context)