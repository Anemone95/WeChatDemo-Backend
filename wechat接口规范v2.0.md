# Default

POST /url:

```json
{
    "action":xxx,
    "body":xxx
}

```

Success Response:

```json
{
    "response":{"response body"},
	"status":200
}
```

Failed Response：

```json
{
    "error":"error reason",
	"status":400
}
```

## User Object

```json
{
    "uid":1,
    "nickname":"xxx",
    "describ":"describe",
    "followed_users": "User IDs",
    "followed_questions":"Question IDs",
    "followed_answers":"answer IDs",
    "blocked_users":"User IDs"
}
```

## Question Object
```json
{
    "qid": 1,
    "title": "title",
    "content": "content",
    "asker": "User Id",
    "answers": "Answer Id",
    "is_anonynous": True,
    "is_closed": False,
    "create_time":1111,
    "recent_time": 1111
}
```
## Answer Object
```json
{
    "aid": 1,
    "content": "content",
    "answerer": "User Id",
    "question": "Question Id",
    "is_anonynous": True,
    "is_allow_review": False,
    "create_time":1111,
    "recent_time": 1111
}
```

## Review Object
```json
{
    "rid":1,
    "content": "content",
    "reviewer": "User Id",
    "answer": "Answer id",
    "create_time":1111,
    "recent_time": 1111
}

```

## Get User/Question/Answer/Review
GET /object?entity={user|question|answer|review}&id={id}  (session require) 

RESPONSE: json(User/Question/Answer/Review Object)


# /User

POST /user

## Login

```json
{
    "action":"login",
    "body":
    {
        "code":1
    }
}
```

Response

set-cookie: session=3rd

```json
{
	"status":200,
    "body": {
    	"uid":1
	}
}
```



## FollowUser

```json
{
    "action":"follow_user",
    "body":
    {
        "uid":1
    }
}
```

RESPONSE:

```json
{
	"status":200
}
```

## EditUser

```json
{
    "action":"edit_user",
    "body":
    {
        "nickname": "name",
        "describe":"ddd"
    }
}
```

RESPONSE:

```json
{
	"status":200
}
```

## BlockUser

```json
{
    "action":"block_user",
    "body":
    {
        "uid":1
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```

## UnBlockUser

```json
{
    "action":"unblock_user",
    "body":
    {
        "uid":1
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```

## ReportUser(举报)

```json
{
    "action":"report_user",
    "body":
    {
        "uid":1,
        "reason":"string"
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```

## DisFollowUser

```json
{
    "action":"disfollow_user",
    "body":
    {
        "uid":1,
        "reason":"string"
    }
}
```

RESPONSE:

```json
{
	"status":200
}
```


# /Question
POST /question


## AskQuestion

```json
{
    "action":"ask_question",
    "body":
    {
        "title":"title",
        "content":"content",
        "is_anonynous":False
    }
}
```

RESPONSE:

```json
{
    "response": "Question Id",
	"status":200/xxx
}
```

## UpdateQuestion

```json
{
    "action":"update_question",
    "body":
    {
        "qid":1,
        "title":"title",
        "content":"content",
        "is_anonynous":False,
        "is_closed":False
    }
}
```

RESPONSE:

```json
{
    "response": "Question Id",
	"status":200/xxx
}
```
## FollowQuestion

```json
{
    "action":"follow_question",
    "body":
    {
        "qid":1
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```

## DisFollowQuestion

```json
{
    "action":"disfollow_question",
    "body":
    {
        "qid":1
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```

# /Answer

POST /answer

## AddAnswer
```json
{
    "action":"add_answer",
    "body":
    {
        "qid":1,
        "content":"content",
        "is_anonynous":false,
        "is_allow_review":true
    }
}
```

RESPONSE:

```json
{
    "response": "Answer Id",
	"status":200
}
```

## UpdateAnswer

```json
{
    "action":"update_answer",
    "body":
    {
        "aid":1,
        "content":"content",
        "is_anonynous":false,
        "is_allow_review":true
    }
}
```

RESPONSE:

```json
{
    "response": "Answer Id",
	"status":200/xxx
}
```

## FollowAnswer

```json
{
    "action":"follow_answer",
    "body":
    {
        "aid":1
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```


## DisFollowAnswer

```json
{
    "action":"disfollow_answer",
    "body":
    {
        "aid":1
    }
}
```

RESPONSE:

```json
{
	"status":200/xxx
}
```

# /Review
POST /review

## AddReview

```json
{
    "action":"add_review",
    "body":
    {
        "aid":1,
        "content":"content"
    }
}
```

RESPONSE:

```json
{
    "response": "Review Id",
	"status":200/xxx
}
```

# 我的关注

1、获取我关注的用户列表，根据关注时间由近到远排序
url:"/followedUser"

method: GET

```json
[{
    "uid":"被关注用户的id",
    "nickname","被关注用户的昵称",
    "followTime","开始关注的时间"
}]
```

2、获取我关注的问题列表，根据关注时间由近到远排序
url:"/followedQuestion"

method: GET

```json
[{
    "nickName":"提问用户的用户名",
    "questionId":"问题id",
    "questionTitile": "问题标题",
    "questionContent":"该问题100字以内的描述概要",
    "answerNum":"回答数",
    "followTime","开始关注的时间"
}]
```

3、获取我关注的回答列表，根据关注时间由近到远排序
url:"/followAnswer"

method: GET

```json
[{
    "nickName":"答主的用户名",
    "questionId":"问题id",
    "answerId":"回答id",
    "questionTitile": "该回答针对的问题的题目",
    "answerContent":"该回答的100字以内的内容概要",
    "reviewNum":"评论数",
    "followTime","开始关注的时间"
}]
```

# 我的提问

该接口会返回我的回答的概要信息，按时间由近到远顺序排序
url:"/myAnswer"

method: GET

```json
{
    "nickName":"答主的用户名,即自己的用户名",
    "questionId":"问题id",
    "answerId":"回答id",
    "questionTitile": "该回答针对的问题的题目",
    "answerContent":"该回答的100字以内的内容概要",
    "reviewNum":"评论数"
}
```

一个相似的接口，用于实现返回“我的提问”的概要信息
url:"/myQuestion"

method: GET

```json
{
    "nickName":"答主的用户名,即自己的用户名",
    "questionId":"问题id",
    "questionTitile": "问题标题",
    "questionContent":"该问题100字以内的描述概要",
    "answerNum":"回答数"
}
```

# mainStage页面关于回答概要的接口

url:"/answerOutlineList"
method: get

```json
{
    "nickName":"答主的用户名",
    "questionId":"问题id"，
    "answerId":"回答id",
    "questionTitile": "该回答针对的问题的题目",
    "answerContent":"该回答的100字以内的内容概要",
    "reviewNum":"评论数"
}
```

