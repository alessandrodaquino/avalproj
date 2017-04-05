import json
import sendgrid
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from aval.models import Candidates
from aval.models import Answers
from sendgrid.helpers.mail import *

def start(request):
    """start funcion, for main/welcome page"""
    return render(request, 'base.html', {})

def is_valid_string(s):
    if isinstance(s, str):
        s = s.strip()
        if len(s) > 0:
            return True

    return False

def check_questions_answered(db, idcandidate):
    done = True

    db.execute("SELECT 1 FROM AVAL_ANSWERS WHERE CANDIDATE_ID = %s", [idcandidate])
    row = db.fetchone()

    if row is None:
        done = False

    return done

def create_candidate(db, post_data):
    cand = Candidates(name=post_data['name'], email=post_data['email'])
    cand.save()
    return cand.pk

def login_page_post(request, post_data):
    db = connection.cursor()
    db.execute("SELECT id FROM AVAL_CANDIDATES WHERE EMAIL = %s", [post_data['email']])
    row = db.fetchone()

    if row is None:
        id = create_candidate(db, post_data)
        return JsonResponse({
            'status': 'ok',
            'idcandidate': id
        })
    else:
        done = check_questions_answered(db, row[0])
        if done:
            return JsonResponse({
                'status': 'cand_exists',
                'msg': 'Candidato já cadastrado. Obrigado pelo interesse.'
            })
        else:
            return JsonResponse({
                'status': 'ok',
                'idcandidate': row[0]
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

def load_question_list(db, get_data):
    db.execute("SELECT id, description FROM aval_questions")
    fieldnames = [name[0] for name in db.description]
    result = []
    for row in db.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

def check_existing_candidate(db, idcandidate):
    exists = True

    db.execute("SELECT 1 FROM AVAL_CANDIDATES WHERE ID = %s", [idcandidate])
    row = db.fetchone()

    if row is None:
        exists = False

    return exists


def load_quest_page(request, get_data):
    db = connection.cursor()

    exists = check_existing_candidate(db, get_data['idcandidate'])
    if exists:
        has_completed = check_questions_answered(db, get_data['idcandidate'])
    else:
        msg = 'Candidato não encontrado.'
        return JsonResponse({'status': 'not_found', 'msg': msg})

    if has_completed:
        msg = 'Você já realizou esta avaliação. Obrigado pelo interesse.'
        return JsonResponse({'status':'completed', 'msg': msg})

    questions = load_question_list(db, get_data)
    return JsonResponse({'status': 'ok', 'questions': json.dumps(questions)})

def isok_skill(val):
    if val >= 7:
        return True
    return False

def send(dest, subj, msg):
    #TODO - Gerar nova chave e colocar em variavel de ambiente 
    sg = sendgrid.SendGridAPIClient(apikey='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')
    data = {
    "personalizations": [
        {
        "to": [
            {
            "email": dest
            }
        ],
        "subject": subj
        }
    ],
    "from": {
        "email": "aldaquino@outlook.com"
    },
    "content": [
        {
        "type": "text/plain",
        "value": msg
        }
    ]
    }
    sg.client.mail.send.post(request_body=data)


def send_mail(where, idcandidate):
    subj = 'Obrigado por se candidatar'
    msg = 'Error'

    db = connection.cursor()
    db.execute('select email from aval_candidates where id = %s', [idcandidate])
    mail = db.fetchone()[0]

    if where == 'frontend':
        msg = 'Obrigado por se candidatar, assim que tivermos uma vaga disponível para programador Front-End entraremos em contato.'
    elif where == 'backend':
        msg = 'Obrigado por se candidatar, assim que tivermos uma vaga disponível para programador Back-End entraremos em contato.'
    elif where == 'mobile':
        msg = 'Obrigado por se candidatar, assim que tivermos uma vaga disponível para programador Mobile entraremos em contato.'
    else: #generic
        msg = 'Obrigado por se candidatar, assim que tivermos uma vaga disponível para programador entraremos em contato.'

    send(mail, subj, msg)

def sort_and_send_mail(frontend, backend, mobile, idcadidate):
    if frontend and backend and mobile: #all
        send_mail('frontend', idcadidate)
        send_mail('backend', idcadidate)
        send_mail('mobile', idcadidate)
    elif frontend and not backend and not mobile: #frontend
        send_mail('frontend', idcadidate)
    elif not frontend and backend and not mobile: #backend
        send_mail('backend', idcadidate)
    elif not frontend and not backend and mobile: #mobile
        send_mail('mobile', idcadidate)
    else: #generic
        send_mail('generic', idcadidate)

def save_answers(request, post_data):
    answers = post_data['answers']
    idcandidate = post_data['idcandidate']
    html = False
    javascript = False
    css = False
    pyth = False
    djan = False
    android = False
    ios = False
    backend = False
    frontend = False
    mobile = False

    for answ in answers:
        ans = Answers(answer=answ['op'], candidate_id=int(idcandidate), question_id=answ['id'])
        ans.save()
        if answ['id'] == 1:
            html = isok_skill(answ['op'])
        elif answ['id'] == 2:
            css = isok_skill(answ['op'])
        elif answ['id'] == 3:
            javascript = isok_skill(answ['op'])
        elif answ['id'] == 4:
            pyth = isok_skill(answ['op'])
        elif answ['id'] == 5:
            djan = isok_skill(answ['op'])
        elif answ['id'] == 6:
            android = isok_skill(answ['op'])
        elif answ['id'] == 7:
            ios = isok_skill(answ['op'])

    if html and javascript and css:
        frontend = True
    elif djan and pyth:
        backend = True
    elif android and ios:
        mobile = True

    sort_and_send_mail(frontend, backend, mobile, idcandidate)

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
