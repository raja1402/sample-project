from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from django.http import HttpResponse
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
# from django.forms import modelformset_factory,inlineformset_factory
from .forms import personform,locationform

from django.views.decorators.cache import cache_page

# Create your views here.

# def index(request):
#     # locations = location.objects.get(pk=location_id)
#     # personformset = modelformset_factory(person,fields=('name',))
#     Location = location()
#     Location_form = locationModelForm(instance=Location)
#     personformset = inlineformset_factory(location,person,fields=('name','job'),can_delete=False,extra=1)
    
#     if request.method == "POST":
#         Location_form = locationModelForm(request.POST)
#         formset = personformset(request.POST,request.FILES)

#         if Location_form.is_valid():
#             created_location = Location_form.save(commit=False)
#             # formset = personformset(request.POST,queryset=person.objects.filter(location__id=locations.id))
#             # formset = personformset(request.POST,instance=locations)
#             formset = personformset(request.POST,request.FILES,instance=created_location)


#             if formset.is_valid():
#                 created_location.save()
#                 formset.save()
#                 # instances = formset.save(commit=False)
#                 # for instance in instances:
#                 #     instance.location_id = locations.id
#                 #     instance.save()
#                 return redirect('index')



#     # formset = personformset(queryset=person.objects.filter(location__id=locations.id))
#     Location_form = locationModelForm(instance=Location)
#     formset = personformset()
#     return render(request,'index.html',{'formset':formset,'Location_form':Location_form})

@cache_page(300)
def index(request):
    
    if request.method=="POST":
        template = loader.get_template("thanks.html")
        form = personform(request.POST)
        if form.is_valid():
            form.save()
            #THIS PROCESS FOR USING COOKIES
            # response = redirect('thanks')
            # response.set_cookie('p&l','this is my cookie with redirect',max_age=None)
            # return response
            #THIS IS FOR SESSION COOKIES:
            name = form.cleaned_data['name']
            job = form.cleaned_data['job']
            request.session['name'] = name
            request.session['job'] = job
            response =  redirect('thanks')
            return response
            

    form = personform()
    return render(request,'index.html',{'form':form})      

@cache_page(200)
def loc(request):
    if request.method == "POST":
        form = locationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = locationform()
    return render(request,'loc.html',{'form':form})      

def thanks(request):
    return render(request,'thanks.html')      


def listperson(request):
    l_person = person.objects.all()
    # cookie_show = request.COOKIES['person_name']
    #THIS IS FOR SHOWING COOKIES
    # cookie_show = "commeted the cookie for now"
    # return render(request,'list.html',{'l_person':l_person,'cookie_show':cookie_show})
    #THIS IS FOR SHOWING SESSION COOKIES:
    responce = "<h1>welcome to sessions data</h1>"
    if request.session.get('name'):
        responce += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('job'):
        responce += "Job : {0} <br>".format(request.session.get('job'))    
        return render(request,'list.html',{'responce':responce,'l_person':l_person})
    else:
        return render(request,'list.html',{'l_person':l_person,'msg':"the session_cookie is deleted"})

@cache_page(300)
def updateperson(request,id):
    obj = get_object_or_404(person,id=id)
    form = personform(request.POST or None,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('list')
    return render(request,'update.html',{'form':form})

def deleteperson(request,id):
    obj = get_object_or_404(person,id=id)
    if request.method == "POST":
        
        obj.delete()
        #THIS IS FOR DELETING THE COOKIES
        # if request.COOKIES.get('person_name'):
        #     responce =  redirect('list')
        #     responce.delete_cookie('person_name')
        #     return  responce
        # else:
        #     responce=HttpResponse("no cookie is present")
        #     return responce    
        
        #THIS IS FOR DELETING SESSIONS
        try:
            del request.session['name']
            del request.session['job']
        except:
            pass
        finally:
            return redirect('index') 

    return render(request,'delete.html')        


from .forms import Profile_Form
from .models import User_Profile

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_profile(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.display_picture = request.FILES['display_picture']
            file_type = user_pr.display_picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'error.html')
            user_pr.save()
            return render(request, 'details.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'create.html', context)