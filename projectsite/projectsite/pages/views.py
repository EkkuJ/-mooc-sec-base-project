from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Todo


@login_required
@csrf_exempt
def indexView(request):
    todos = Todo.objects.filter(owner=request.user)
    return render(request, 'pages/index.html', {"todos": todos})


@login_required
@csrf_exempt
def addView(request):
    content = request.POST.get('content')
    if len(content) > 0:
        todo = Todo(owner=request.user, content=content)
        todo.save()
    return redirect('/')


@login_required
@csrf_exempt
def deleteView(request):
    todo = Todo.objects.get(id=request.POST.get('id'))
    todo.delete()
    return redirect('/')


@login_required
@csrf_exempt
def downloadView(request):
    # user = request.user
    user = request.GET.get('user')
    todos = []
    set = Todo.objects.filter(owner__username=user)
    for todo in set:
        todos.append(todo.content)
    return JsonResponse({'todos': todos})
