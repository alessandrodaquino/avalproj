import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from aval.models import Candidates

def start(request):
    """start funcion, for main/welcome page"""
    return render(request, 'base.html', {})

def is_valid_string(s):
    if isinstance(s, str):
        s = s.strip()
        if len(s) > 0:
            return True

    return False

def create_candidate(db, post_data):
    cand = Candidates(name=post_data['name'], email=post_data['email'])
    cand.save()
    return cand.pk

def login_page_post(request, post_data):
    db = connection.cursor()
    db.execute("SELECT 1 FROM AVAL_CANDIDATES WHERE EMAIL = %s", [post_data['email']])
    row = db.fetchone()

    if row == None:
        id = create_candidate(db, post_data)
        return JsonResponse({
            'status': 'ok',
            'idcandidate': id
        })
    else:
        return JsonResponse({
            'status': 'cand_exists',
            'msg': 'Candidato já cadastrado. Obrigado pelo interesse.'
        })

    return JsonResponse({'status': 'err', 'msg': 'Erro desconhecido'})

def checklogin(request, post_data):
    err = False
    fieldname_valid = False
    fieldemail_valid = False

    if 'name' in post_data:
        is_valid_name = is_valid_string(post_data['name'])
        if not is_valid_name:
            err = True
        else:
            fieldname_valid = True
    else:
        err = True

    if 'email' in post_data:
        is_valid_mail = is_valid_string(post_data['email'])
        if not is_valid_mail:
            err = True
        else:
            fieldemail_valid = True
    else:
        err = True

    if err:
        msg = ''
        if (not fieldemail_valid) and (not fieldname_valid):
            msg = 'Nome e e-mail inválidos'
        elif not fieldemail_valid:
            msg = 'E-mail inválido'
        elif not fieldname_valid:
            msg = 'Nome inválido'

        return JsonResponse({
            'status': 'err',
            'msg': msg,
            'fname': fieldname_valid,
            'femail': fieldemail_valid
        })
    else: #se nenhum erro for encontrado, prossegue para a base de dados
        return login_page_post(request, post_data)

    return JsonResponse({'status': 'ok'})

def load_quest_page(request, get_data):
    db = connection.cursor()
    db.execute("SELECT id, description FROM aval_questions")
    fieldnames = [name[0] for name in db.description]
    result = []
    for row in db.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return JsonResponse({'status': 'ok', 'questions': json.dumps(result)})

def save_answers(request, post_data):
    answers = post_data['answers']
    print(answers)
    for answer in answers:
        for k, v in answer.items():
            print(k, v)

    #     print(answers[item])
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
        get_data = fix_get_data(request)

        if get_data['page'] == 'quest':
            return load_quest_page(request, get_data)

    elif request.method == 'POST':
        post_data = fix_post_data(request)

        if post_data['page'] == 'login':
            return checklogin(request, post_data)
        elif post_data['page'] == 'quest':
            return save_answers(request, post_data)

    return render(request, 'base.html', {})
