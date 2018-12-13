from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib import auth
import requests
import json

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


def wechat_login(request, body):
    payload = {'appid': 'wx1c530cec0bfa60c7',
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


