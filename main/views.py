from django.shortcuts import render, redirect
from .models import Task
from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


def home(request):
    # Get all tasks from database
    tasks = Task.objects.all()
    now = timezone.now().date()

    # Tasks which have same date as today will be stored in this list
    today = []
    # Tasks which have a date that is not later then next seven days will be stored in this list
    week = []

    # Later then one week is gonna store in this list
    moreThenSeven = []

    for task in tasks:
        # Check if tasks date is same as today if it is then it will be append to today list
        if now == task.date_of_task.date():
            today.append(task)

        # Check if tasks date is in the next seven days plus it is not same as today's date
        if timedelta(days=7) >= task.date_of_task.date() - now >= timedelta(days=1):
            week.append(task)

        if task.date_of_task.date() - now > timedelta(days=7):
            moreThenSeven.append(task)

    context = {
        'today': today, 'week': week, 'tasks': moreThenSeven
    }
    return render(request, 'main/index.html', context=context)


def today(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        tasks = Task.objects.all()
        now = timezone.now().date()
        today = []

        # Checking if task's data is same as today
        for task in tasks:
            if now == task.date_of_task.date():
                today.append(task)

        context = {
            'today': today
        }
        return render(request, 'main/today.html', context=context)
    else:
        # if user is not logged in he/she will be redirect to index page
        return render(request,"main/index.html")


def week(request):
    if request.user.is_authenticated:
        tasks = Task.objects.all()
        now = timezone.now().date()
        week = []

        for task in tasks:
            if timedelta(days=7) >= task.date_of_task.date() - now >= timedelta(days=1):
                week.append(task)

        context = {
            'week': week
        }
        return render(request, 'main/nextSevenDays.html', context=context)
    else:
        return render(request,"main/index.html")


@login_required
def addNewTask(request):
    format_str = '%Y-%m-%d %H:%M'
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        dateAndTime = request.POST["date"] + " " + request.POST["time"]
        dateOfTask = datetime.strptime(dateAndTime, format_str)
        if title and dateOfTask:
            task = Task()
            task.user = request.user
            task.title = title
            task.text = text
            task.date_of_task = dateOfTask
            task.date_task_created = timezone.now()
            task.is_done = False
            task.save()
            return redirect("main_home")
        else:
            return render(request, 'main/new.html', {"fieldIsNotFilled": "Please fill the field with star"})
    return render(request, 'main/new.html')


@login_required
def update(request, pk):
    format_str = '%Y-%m-%d %H:%M'
    taskFilterd = Task.objects.filter(id=pk)[0]
    if request.user == taskFilterd.user:
        task = {
            'task': taskFilterd,
            'date': taskFilterd.date_of_task.strftime("%Y-%m-%d"),
            'time': taskFilterd.date_of_task.strftime("%H:%M")
        }
    else:
        raise PermissionDenied

    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        dateAndTime = request.POST["date"] + " " + request.POST["time"]
        dateOfTask = datetime.strptime(dateAndTime, format_str)
        if title and dateOfTask:
            task = Task.objects.filter(pk=pk)[0]
            task.user = request.user
            task.title = title
            task.text = text
            task.date_of_task = dateOfTask
            task.date_task_created = timezone.now()
            task.is_done = False
            task.save()
            return redirect("main_home")
        else:
            return render(request, 'main/update.html', {"fieldIsNotFilled": "Please fill the field with star"})
    else:
        return render(request, 'main/update.html', context=task)


@login_required
def taskIsDone(request, pk):
    taskFilterd = Task.objects.filter(pk=pk)[0]
    if request.user == taskFilterd.user:
        if taskFilterd.is_done:
            taskFilterd.is_done = False
            taskFilterd.save()
            return redirect("doneList")
        else:
            taskFilterd.is_done = True
            taskFilterd.save()
    else:
        raise PermissionDenied
    return redirect("main_home")


def showDoneTasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        context = {
            'tasks': tasks
        }
        return render(request, 'main/showDone.html', context=context)
    else:
        return render(request, 'main/index.html')


@login_required
def deleteTask(request, pk):
    taskFilterd = Task.objects.filter(pk=pk)[0]
    if request.method == "POST":
        if request.user == taskFilterd.user:
            taskFilterd.delete()
            return redirect("main_home")
        else:
            raise PermissionDenied
    else:
        return render(request, "main/delete.html", context={'task': taskFilterd})


def setImportant(request, pk):
    taskFilterd = Task.objects.filter(pk=pk, user=request.user)[0]
    if request.user == taskFilterd.user:
        if taskFilterd.is_important:
            taskFilterd.is_important = False
            taskFilterd.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            taskFilterd.is_important = True
            taskFilterd.save()
    else:
        raise PermissionDenied
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def showImportanTasks(request):
    if request.user.is_authenticated:
        # Filter task by user
        tasks = Task.objects.filter(user=request.user)
        context = {
            'tasks': tasks
        }
        return render(request, 'main/importants.html', context=context)
    else:
        return render(request, 'main/index.html')
