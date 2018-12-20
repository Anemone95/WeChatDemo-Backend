from django.db import models

# Create your models here.
from django.contrib.auth.models import  AbstractUser,UserManager

class User(AbstractUser):
    '''
    Users within the Django authentication system are represented by this model. Username, password and email are required. Other fields are optional.
    '''
    class Meta:
        app_label = 'question_answer'

    def __str__(self):
        return self.nickname if self.nickname else self.username

    def to_dict(self):
        followed_users=list(map(lambda e: {"id": e.id, "nickname": e.nickname}, self.followed_users.all()))
        followed_questions=list(map(lambda e: e.id, self.followed_questions.all()))
        followed_answers=list(map(lambda e: e.id, self.followed_answers.all()))
        blocked_users=list(map(lambda e: {"id": e.id, "nickname": e.nickname}, self.blocked_users.all()))
        return dict(
                uid=self.id,
                nickname=self.nickname,
                describe=self.describe if self.describe else "",
                followed_users=followed_users,
                followed_questions=followed_questions,
                followed_answers=followed_answers,
                blocked_users=blocked_users,
        )

    openid=models.CharField(max_length=32)
    wechat_session=models.CharField(max_length=32)
    nickname=models.CharField(max_length=64)
    describe=models.TextField(null=True)
    followed_users=models.ManyToManyField("self", related_name="followed_users")
    followed_questions=models.ManyToManyField("Question", related_name="followed_questions")
    followed_answers=models.ManyToManyField("Answer", related_name="followed_answers")
    blocked_users=models.ManyToManyField("self", related_name="blocked_users")

class Question(models.Model):
    class Meta:
        app_label = 'question_answer'

    def __str__(self):
        return self.title

    def to_dict(self):
        return dict(
                title=self.title,
                content=self.content,
                asker=self.asker.id,
                is_anonynous=self.is_anonynous,
                is_closed=self.is_closed,
                create_time = self.create_time,
                recent_time = self.recent_time,
        )
    title=models.CharField(max_length=255)
    content=models.TextField()
    asker=models.ForeignKey("User", on_delete=models.CASCADE)
    is_anonynous=models.BooleanField(default=False)
    is_closed=models.BooleanField(default=False)
    create_time=models.TimeField(auto_now_add=True)
    recent_time=models.TimeField(auto_now=True)

class Answer(models.Model):
    class Meta:
        app_label = 'question_answer'

    def __str__(self):
        return self.answerer.nickname+": "+self.content[:30]

    def to_dict(self):
        return dict(
                content=self.content,
                answerer=self.answerer.id,
                question=self.question.id,
                is_anonynous=self.is_anonynous,
                is_allow_review=self.is_allow_review,
                create_time = self.create_time,
                recent_time = self.recent_time,
        )
    content=models.TextField()
    answerer=models.ForeignKey("User", on_delete=models.CASCADE)
    question=models.ForeignKey("Question", on_delete=models.CASCADE)
    is_anonynous=models.BooleanField(default=False)
    is_allow_review=models.BooleanField(default=True)
    create_time=models.TimeField(auto_now_add=True)
    recent_time=models.TimeField(auto_now=True)

class Review(models.Model):
    class Meta:
        app_label = 'question_answer'

    def __str__(self):
        return self.reviewer.nickname+": "+self.content[:30]

    def to_dict(self):
        return dict(
                content=self.content,
                reviewer=self.reviewer.id,
                answer=self.answer.id,
                create_time = self.create_time,
                recent_time = self.recent_time,
        )
    content=models.TextField()
    reviewer=models.ForeignKey("User", on_delete=models.CASCADE)
    answer=models.ForeignKey("Answer", on_delete=models.CASCADE)
    create_time=models.TimeField(auto_now_add=True)
    recent_time=models.TimeField(auto_now=True)

class BlockList(models.Model):
    class Meta:
        app_label = 'question_answer'

    def to_dict(self):
        return dict(
                report_user=self.report_user.id,
                bad_user=self.bad_user.id,
                reason=self.reason,
                is_anonynous=self.is_anonynous,
                is_closed=self.is_closed,
                create_time = self.create_time,
                recent_time = self.recent_time,
        )

    report_user=models.ForeignKey("User", on_delete=models.CASCADE, related_name="report_user")
    bad_user=models.ForeignKey("User", on_delete=models.CASCADE, related_name="bad_user")
    reason=models.TextField(default="")
    create_time=models.TimeField(auto_now_add=True)
