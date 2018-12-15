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
    "is_closed": False,
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


