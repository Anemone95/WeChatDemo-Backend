from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib import auth
import requests
import json
import datetime,time

from .models import *

def get_wechat_secret_key():
    if not settings.WECHAT_SECRET_KEY:
        with open('./secretkey.txt', 'r') as f:
            settings.WECHAT_SECRET_KEY=f.readline().replace('\r','').replace('\n','')
    return settings.WECHAT_SECRET_KEY

def get_object(request):
    entity=request.GET['entity']
    _id=request.GET['id']
    entity2model={
        "user": User,
        "question": Question,
        "answer": Answer,
        "review": Review,
    }
    _object=entity2model[entity].objects.get(id=_id)
    return JsonResponse(dict(status=200, body=_object.to_dict()))

# Create your views here.
def user_action(request):
    request_json=json.loads(request.body)
    action2func={
        "login": wechat_login,
        "follow_user": follow_user,
        "disfollow_user": disfollow_user,
        "edit_user": edit_user,
        "block_user": block_user,
        "unblock_user": unblock_user,
        "report_user": report_user,
    }
    body, status=action2func[request_json["action"]](request, request_json["body"])
    if status==200:
        return JsonResponse(dict(status=status, response=body))
    else:
        return JsonResponse(dict(status=status, error=body))

def question_action(request):
    request_json = json.loads(request.body)
    action2func = {
        "ask_question": ask_question,
        "update_question": update_question,
        "follow_question": follow_question,
        "disfollow_question": disfollow_question,
    }
    body, status=action2func[request_json["action"]](request, request_json["body"])
    if status==200:
        return JsonResponse(dict(status=status, response=body))
    else:
        return JsonResponse(dict(status=status, error=body))

def answer_action(request):
    request_json = json.loads(request.body)
    action2func = {
        "add_answer": add_answer,
        "update_answer": update_answer,
        "follow_answer": follow_answer,
        "disfollow_answer": disfollow_answer,
    }
    body, status = action2func[request_json["action"]](request, request_json["body"])
    if status == 200:
        return JsonResponse(dict(status=status, response=body))
    else:
        return JsonResponse(dict(status=status, error=body))

def review_action(request):
    request_json = json.loads(request.body)
    action2func = {
        "add_review": add_review,
    }
    body, status = action2func[request_json["action"]](request, request_json["body"])
    if status == 200:
        return JsonResponse(dict(status=status, response=body))
    else:
        return JsonResponse(dict(status=status, error=body))

def wechat_login(request, body):
    payload = {'appid': 'wx8c53cbd60fbb55bc',
               'secret': get_wechat_secret_key(), # 4da***57
               'js_code': body["code"],
               'grant_type': 'authorization_code',
              }
    r = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=payload)
    # r.text={"session_key":"xWm0r4af3WN79vz00d0Ipg==","openid":"oxGBW4-Q6UXupqZJbL8HTbgPEYmY"}
    res = json.loads(r.text)
    if "errmsg" not in res:
        user = User.objects.filter(openid=res["openid"])

        if not User.objects.filter(openid=res["openid"]).exists():
            user = User.objects.create_user(username=res["openid"],password=res["openid"],email="{}@wechat.com".format(res["openid"]), openid=res["openid"])
            user.save()
        # auth只能用用户密码登陆，因此如果既有用户密码又有小程序的话，就需要重新设计密码，
        # 使用普通密码/微信id/oathid获取真实密码，再用auth(用户名，真实密码)登陆
        user = auth.authenticate(username=res["openid"], password=res["openid"])
        if user is not None:
            auth.login(request,user)
            print(user.id)
            return {"uid": user.id}, 200
        else:
            return "Wrong username or password", 400
    else:
        return res["errmsg"],400


def follow_user(request, body):
    followed_user=User.objects.get(id=body["uid"])
    request.user.followed_users.add(followed_user)
    request.user.save()
    return "",200

def disfollow_user(request, body):
    disfollowed_user=User.objects.get(id=body["uid"])
    request.user.followed_users.remove(disfollowed_user)
    request.user.save()
    return "",200

def edit_user(request, body):
    request.user.nickname=body["nickname"]
    request.user.describe=body["describe"]
    request.user.save()
    return "",200

def block_user(request, body):
    blocked_user=User.objects.get(id=body["uid"])
    request.user.blocked_users.add(blocked_user)
    request.user.save()
    return "",200

def unblock_user(request, body):
    blocked_user=User.objects.get(id=body["uid"])
    request.user.blocked_users.remove(blocked_user)
    request.user.save()
    return "",200

def report_user(request, body):
    bad_user=User.objects.get(id=body["uid"])
    bl=BlockList(report_user=request.user,
              bad_user=bad_user,
              reason=body["reason"])
    bl.save()
    return "",200

def ask_question(request, body):
    title=body["title"]
    content=body["content"]
    is_anonynous=body["is_anonynous"]
    question=Question(title=title,
                      content=content,
                      is_anonynous=is_anonynous,
                      asker=request.user,
                      )
    question.save()
    return question.id,200

def update_question(request, body):
    question=Question.objects.get(id=body["qid"])
    question.title=body["title"]
    question.content=body["content"]
    question.is_anonynous=body["is_anonynous"]
    question.is_closed=body["is_closed"]
    question.save()
    return question.id,200

def follow_question(request, body):
    followed_question = Question.objects.get(id=body["qid"])
    request.user.followed_questions.add(followed_question)
    request.user.save()
    return "", 200

def disfollow_question(request, body):
    disfollowed_user = Question.objects.get(id=body["qid"])
    request.user.followed_questions.remove(disfollowed_user)
    request.user.save()
    return "", 200

def add_answer(request, body):
    qid=body["qid"]
    question=Question.objects.get(id=qid)
    answer = Answer(question=question,
                    answerer=request.user,
                    content=body["content"],
                    is_anonynous=body["is_anonynous"],
                    is_allow_review=body["is_allow_review"]
                    )
    answer.save()
    return answer.id,200


def update_answer(request, body):
    answer = Answer.objects.get(id=body["aid"])
    answer.content=body["content"]
    answer.is_anonynous = body["is_anonynous"]
    answer.is_allow_review = body["is_allow_review"]
    answer.save()
    return answer.id, 200


def follow_answer(request, body):
    follow_answer = Answer.objects.get(id=body["aid"])
    request.user.followed_answers.add(follow_answer)
    request.user.save()
    return "",200

def disfollow_answer(request, body):
    disfollow_answer = Answer.objects.get(id=body["aid"])
    request.user.followed_answers.remove(disfollow_answer)
    request.user.save()
    return "", 200

def add_review(request, body):
    aid=body["aid"]
    answer=Answer.objects.get(id=aid)
    review = Review(content=body["content"],
                    answer=answer,
                    reviewer=request.user
                    )
    review.save()
    return review.id,200

def getAnswerOutlineList(request):
    '''Success'''
    answer=Answer.objects.filter(recent_time__lte=datetime.datetime.now()+datetime.timedelta(days=-30))
    res = []

    for i in reversed(answer):
        print (type(i.question.id))
        component={}
        component["nickName"] = User.objects.get(id=i.answerer.id).nickname
        component["questionId"] = (str)(i.question.id)
        component["answerId"] = (str)(i.id)
        component["questionTitle"] = (str)(Question.objects.get(id=i.question.id).title)
        component["answerContent"] = i.content[:100]
        component["reviewNum"] = (str)(len(Review.objects.filter(answer=i)))
        res.append(component)

    return JsonResponse(res, safe=False)

def getMyAnswer(request):
    '''success'''
    answer=Answer.objects.filter(answerer=request.user)
    res = []
    for i in reversed(answer):
        print (type(i.question.id))
        component={}
        component["nickName"] = User.objects.get(id=i.answerer.id).nickname
        component["questionId"] = (str)(i.question.id)
        component["answerId"] = (str)(i.id)
        component["questionTitle"] = (str)(Question.objects.get(id=i.question.id).title)
        component["answerContent"] = i.content[:100]
        component["reviewNum"] = (str)(len(Review.objects.filter(answer=i)))
        res.append(component)

    return JsonResponse(res, safe=False)

def getMyQuestion(request):
    '''success'''
    question = Question.objects.filter(asker=request.user)
    res = []
    for i in reversed(question):
        print(type(i.id))
        component = {}
        component["nickName"] = User.objects.get(id=i.asker.id).nickname
        component["questionId"] = (str)(i.id)
        component["questionTitle"] = (str)(i.title)
        component["questionContent"] = i.content[:100]
        component["answerNum"] = (str)(len(Answer.objects.filter(question=i)))
        res.append(component)

    return JsonResponse(res, safe=False)

def getFollowedUser(request):
    user = request.user.followed_users.all()
    print(type(user))
    res = []
    for i in reversed(user):
        component = {}
        component["uid"] = (str)(i.id)
        component["nickname"] = i.nickname
        #component["followTime"] = (str)(i.title)
        res.append(component)
    return JsonResponse(res, safe=False)

def getFollowedQuestion(request):
    questions = request.user.followed_questions.all()
    res = []
    for i in reversed(questions):
        component = {}
        component["nickName"] = User.objects.get(id=i.asker.id).nickname
        component["questionId"] = (str)(i.id)
        component["questionTitle"] = (str)(i.title)
        component["questionContent"] = i.content[:100]
        component["answerNum"] = (str)(len(Answer.objects.filter(question=i)))
        # component["followTime"] = (str)(i.title)
        res.append(component)
    return JsonResponse(res, safe=False)

def getFollowedAnswer(request):
    answers = request.user.followed_answers.all()
    res = []
    for i in reversed(answers):
        component = {}
        component["nickName"] = (str)(i.id)
        component["questionId"] = i.nickname
        component["answerId"] = (str)(i.id)
        component["questionTitle"] = i.nickname
        component["answerContent"] = (str)(i.id)
        component["reviewNum"] = i.nickname
        # component["followTime"] = (str)(i.title)
        res.append(component)
    return JsonResponse(res, safe=False)
