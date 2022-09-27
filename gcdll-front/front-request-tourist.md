# 前端接口需求

## 游客端

### 一、游客主页

#### 1 获取当前所有展览

/api/home

method：GET

返回：json字符串

```javascript
code: "200"
data: {
    {
        id: "展览id",
        name: "展览名字",
	    introduction: "这是一个关于风景的展览",
        timestamp: "13位上传时间戳",
	    img_src: '封面图片',
        comments: "评论数",
        likes: "点赞数",
    },
    ...
}
```

### 二、展览页

#### 1 获取展览信息

/api/exhibit

method: GET

request: 参数

```javascript
{
    id: "2353425"
}
```

返回：json字符串

```javascript
code: "200"
data: {
    img_list: {
        {
            id: "照片id",
            name: "照片名字",
	        introduction: "照片介绍",
            timestamp: "13位上传时间戳",
	        img_src: '图片',
            comments: "评论数",
            likes: "点赞数",
        },
        ...
    },
    exhibit_info: {
        id: "展览id",
        name: "展览名字",
	    introduction: "这是一个关于风景的展览",
        timestamp: "13位上传时间戳",
	    img_src: '封面图片',
        comments: "评论数",
        likes: "点赞数",
    },
}
```

#### 2 给展览点赞、评论

/api/exhibit

method: POST

cookie: 用户id

```javascript
{
    id: "",
}
```

request: body中json字符串

```javascript
{
    id: "展览id",
    type: "", //1是点赞，2是评论。。。（可能要加收藏
    content: "",
}
```

返回：json字符串



### 三、照片详情页

#### 1 获取照片信息

/api/photo

method: GET

request: 参数

```javascript
{
    id: "照片id",
}
```

返回：json字符串

```javascript
code: "200",
data: {
    id: "照片id",
    name: "照片名字",
	introduction: "照片介绍",
    timestamp: "13位上传时间戳",
	img_src: '图片',
    comments: "评论数",
    likes: "点赞数",
},
```

#### 

#### 2 给照片点赞、评论

/api/photo

method: POST

cookie: 用户id

```javascript
{
    id: "",
}
```

request: body中json字符串

```javascript
{
    id: "照片id",
    type: "", //1是点赞，2是评论。。。（可能要加收藏
    content: "",
}
```

返回：json字符串



### 四、评论、点赞

#### 1 获取评论详情

/api/comment

method: GET

request: 参数

```javascript
{
    type: "0", //0-展览，1-照片
    id: "照片/展览id",
    order: "0", //排序方式，0-按热度，1-按时间最新
    start: "0", //需要评论范围，[start*10, (start+1)*10)
}
```

返回：json字符串

```javascript
{
    code: "200",
    data: {
        {
            id: "comment id",
            user: "comment user",
            avatar: "user avatar",
            content: "内容",
            likes: "",
        },
        ...
    }
}
```

#### 2 给评论点赞

/api/comment

method: POST

request: body

```javascript
{
    id: "comment id",
}
```

返回：

```javascript
{
    code: "200",
}
```



### 五、照片修复页

#### 1 获取照片修复详情

/api/repair

method:GET

request: 参数

```javascript
{
    //更新 3.21 3：56
    type: "0" //0-照片，1-展览
    id: "image id"
}
```

返回：

```javascript
{
    code: "200",
    data: {
        image_history_list:{
            {
                id: "照片id/修复图片id",
	            operation: "照片修复操作名称",
                timestamp: "13位上传时间戳",
	            img_src: '图片',
            },
            ...
        }
        name: "照片名字",
	    introduction: "修复详情介绍",
	    img_src: '图片',
        now_time: "已经进行时间",
        expect_time: "预计完成总时间",
        operation: "正在修复操作名称",
        flag: "是否已经修复完成"
    }
}
```


