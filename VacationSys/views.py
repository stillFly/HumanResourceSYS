from django.shortcuts import render, redirect

from django.views.generic.list import ListView

from VacationSys.models import Passengersinfo
from VacationSys.models import TableOfInfo
from VacationSys.models import NoteForLeave

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
#class NoteListView(ListView):


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', context={'form':form})

@login_required
def dashboard(request):
    person_in_list  = TableOfInfo.objects.filter(status=True)
    person_out_list = TableOfInfo.objects.filter(status=False)
    notes = []
    for person in person_out_list:
        notes.append(NoteForLeave.objects.filter(person__PassengerID=person.person.PassengerID).latest('ID'))
    context = {'person_in':person_in_list, 'person_out':zip(person_out_list, notes)}
    return render(request, 'VacationSys/dashboard.html', context=context)

@login_required
def tables(request):
    person_in_list  = TableOfInfo.objects.filter(status=True)
    person_out_list = TableOfInfo.objects.filter(status=False)
    notes = []
    for person in person_out_list:
        notes.append(NoteForLeave.objects.filter(person__PassengerID=person.person.PassengerID).latest('ID'))
    context = {'person_in':person_in_list, 'person_out':zip(person_out_list, notes)}
    return render(request, 'VacationSys/tables.html', context=context)

def bad_request(request):
    return render(request, 'page_400.html')

def page_error(request):
    return render(request, 'page_500.html')

def page_not_found(request):
    return render(request, 'page_404.html')

def permission_denied(request):
    return render(request, 'page_403.html')
