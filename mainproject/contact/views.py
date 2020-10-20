from django.shortcuts import render, HttpResponse, HttpResponseRedirect,redirect
from .models import Person
from .forms import PersonForm
# Create your views here.
def contact_list(request):
    persons = Person.objects.all().order_by('first_name')
    return render(request,'contact/contact_list.html',{'persons':persons})

def detail(request,contact_id):
    person = Person.objects.get(id = contact_id)
    return render(request,'contact/contact_detail.html',{'persons':person})

def delete(request, contact_id):
    person = Person.objects.get(id = contact_id)
    print(person)
    person.delete()
    persons = Person.objects.all().order_by('first_name')
    return HttpResponseRedirect("/contact") 

def contact_create_view(request):
    form = PersonForm(request.POST)

    if form.is_valid():
        form.save()    
    
    return render(request,'contact/contact_create.html',{'form':form})

def contact_edit(request, contact_id):
    person = Person.objects.get(id= contact_id)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('/contact/'+str(person.id))
    else:
        form = PersonForm(instance=person)
    return render(request, 'contact/contact_create.html', {'form': form})


