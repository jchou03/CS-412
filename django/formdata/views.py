from django.shortcuts import render, redirect

# Create your views here.
def show_form(request): 
    template_name = "formdata/form.html"
    context={}
    
    return render(request, template_name, context)

def submit(request):
    
    template_name="formdata/confirmation.html"
    context={}
    
    print(request)
    # read form data
    if request.POST:
        name = request.POST["name"]
        favorite_color = request.POST["favorite_color"]
        context["name"] = name
        context["favorite_color"] = favorite_color
        # generate response
        return render(request, template_name, context)
    else:
        # if client got here by making get request, send them back to the form
        # return show_form(request)
        
        # use redirect
        return redirect("/formdata")