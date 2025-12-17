from django.shortcuts import render , redirect
from django.urls import reverse_lazy
# Create your views here.

from .models import *
from .forms import *

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
#used when using class based functions

from django.contrib.auth.decorators import login_required

from django.contrib.auth import login
from .forms import RegisterForm

class CustomLoginView(LoginView):
    tempelate_name = 'tasks/login.html' 
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list')
    
def register(request):
    if request.user.is_authenticated:
        return redirect('list')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto login after register
            return redirect('list')

    context = {'form': form}
    return render(request, 'tasks/register.html', context)

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
        return redirect('/')

    context = { 'tasks' : tasks , 'form': form}
    return render(request , 'tasks/list.html', context)

@login_required
def updateTask(request , pk):
    task = Task.objects.get(id=pk, user=request.user)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}

    return render(request, 'tasks/update_task.html' , context)

@login_required
def deleteTask(request , pk):
    item = Task.objects.get(id=pk, user=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {'item' : item}
    return render(request, 'tasks/delete.html' , context) 