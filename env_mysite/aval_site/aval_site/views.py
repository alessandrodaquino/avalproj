import json
from django.shortcuts import render
from django.http import JsonResponse

def start(request):
    """start funcion, for main/welcome page"""
    return render(request, 'base.html', {})

def is_valid_string(s):
    if isinstance(s, str):
        s = s.strip()
        if len(s) > 0:
            return True
    return False

def checklogin(request, post_data):
    err = False
    if 'name' in post_data:
        is_valid_name = is_valid_string(post_data['name'])
        if not is_valid_name:
            err = True
    else:
        err = True

    if 'email' in post_data:
        is_valid_mail = is_valid_string(post_data['email'])
        if not is_valid_mail:
            err = True
    else:
        err = True

    if err:
        msg = 'Nome ou e-mail inválido'
        return JsonResponse({'status': 'err', 'msg': msg})

    return JsonResponse({'status': 'ok'})

def fix_post_data(request):
    post_data = {}

    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))

    return post_data

def fix_get_data(request):
    get_data = {}
    if request.method == 'GET':
        get_data = dict(request.GET.dict())
    
    return get_data

def route(request):
    if request.method == 'GET':
        pass
        # get_data = fix_get_data(request)
        # if get_data['page'] == 'questionario':
        #     return render(request, 'quest.html', {})
    elif request.method == 'POST':
        post_data = fix_post_data(request)
        if post_data['page'] == 'login':
            return checklogin(request, post_data)
    return render(request, 'base.html', {})
