"""WeChatDemo_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from question_answer import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', app_views.user_action),
    path('object/', app_views.get_object),
    path('question/', app_views.question_action),
    path('answer/',app_views.answer_action),
    path('review/',app_views.review_action),
    path('answerOutlineList/',app_views.getAnswerOutlineList),
    path('myAnswer/',app_views.getMyAnswer),
    path('myQuestion/',app_views.getMyQuestion),
    path('followedUser/', app_views.getFollowedUser),
    path('followedQuestion/', app_views.getFollowedQuestion),
    path('followedAnswer/', app_views.getFollowedAnswer),

]
