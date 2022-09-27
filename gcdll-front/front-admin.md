# 前端接口需求

## 管理员端

### 一、登陆页

#### 1 游客/管理员 登陆

/login

method: POST

request: body

```javascript
{
    login: true,    //if 'login' in ...
    //应该不需要type: "admin"/"user",
    user: "username",
    password: "password",
}
```

response: json

```javascript
{
code: '200',
data: {
    id: "user id"
    name: "user name"
    avatar: "user avatar"    //可暂时先省略
}
}
```

#### 2 游客注册

/login

method: POST

request: body

```javascript
{
    register: true,
    //type: "admin"/"user",
    user: "username",
    password: "password",
}
```

response: json

```javascript
{
code: '200',
data: {
    id: "user id"
    name: "user name"
    avatar: "user avatar"    //可暂时先省略
}
}
```

### 二、管理

#### 1  正在处理的照片和已处理完成的照片

/admin/photo

method: GET

request: 无

response: json

```javascript
{
code: '200',
data: {
    fixing:{
        id: '图片id',
        name: '图片名字',
        operation: "正在进行的操作",
        timestamp: "上传时间",
        expected_time: "预计需要总时间",
        now_time: "已经处理的时间",
		img_src: "当前处理的图片程度图片",
    },
    fixed:{
        id: '图片id',
        name: '图片名字',
        timestamp: "完成时间",
		img_src: "当前处理的图片程度图片",
    },
}
}
```
