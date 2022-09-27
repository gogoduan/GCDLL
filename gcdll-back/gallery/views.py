# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import *
from .ai_fix import *
from .io import *
import json
import random
from django.utils import timezone

LOGIN_URL = "http: //127.0.0.1: 8000/admin/login"

# 网站：gcdll-front-gcdll.app.secoder.net


# 发表评论
def post_comment(request, type, user_id):
    """
        处理评论的函数
        type = 0为展览, 1为照片
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if user_is_banned(user_id):
        return gen_response(200, {"status": "banned_error", "detail": "您已被禁言，无法发表评论"})
    try:
        body = json.loads(request.body)
        if type == 0:  # 评论展览
            user_id = int(user_id)  # 用户id
            gal_id = int(body["id"]) if "id" in body else None  # 展览id
            content = body["content"] if "content" in body else None
            try:
                com_res = comment_gallery(user_id, gal_id, content)
                if com_res[0]:
                    reason = str(com_res[1])  # 评论被禁的原因
                    if reason == "ERROR":
                        reason = "评论上传失败"
                    return gen_response(
                        200, {"status": "illegal_comment", "detail": reason, }
                    )
                else:
                    return gen_response(200, "评论成功")
            except Exception as e:
                return gen_response(200, {"status": "like_error", "detail": "评论失败"})

        elif type == 1:  # 评论照片
            user_id = int(user_id)
            pho_id = int(body["id"]) if "id" in body else None  # 照片id
            content = body["content"] if "content" in body else None
            try:
                com_res = comment_photo(user_id, pho_id, content)
                if com_res[0]:
                    reason = str(com_res[1])
                    if reason == "ERROR":
                        reason = "评论上传失败"
                    return gen_response(
                        200, {"status": "illegal_comment", "detail": reason, }
                    )
                else:
                    return gen_response(200, "评论成功")
            except Exception as e:
                return gen_response(200, {"status": "like_error", "detail": "评论失败"})

        else:
            return gen_response(
                200,
                {
                    "status": "operation_error",
                    "detali": "Invalid comment object %d" % type,
                },
            )
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


# 点赞
def post_like(request, type, like, user_id):
    """
        处理点赞的函数
        type = 0为展览, 1为照片
        like = 0为赞, 1为取消
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    try:
        body = json.loads(request.body)
        if type == 0:  # 点赞展览
            user_id = int(user_id)  # 用户id
            gal_id = int(body["id"]) if "id" in body else None  # 展览id
            try:
                like_gallery(user_id, gal_id, like)  # 直接分开函数
                return gen_response(200, "点赞成功")
            except Exception as e:
                return gen_response(200, {"status": "like_error", "detail": "点赞失败", })

        elif type == 1:  # 点赞照片
            user_id = int(user_id)
            pho_id = int(body["id"]) if "id" in body else None  # 照片id
            try:
                like_photo(user_id, pho_id, like)
                return gen_response(200, "点赞成功")
            except Exception as e:
                return gen_response(200, {"status": "like_error", "detail": "点赞失败", })

        elif type == 2:  # 点赞评论
            user_id = int(user_id)  # 用户id
            com_id = int(body["id"]) if "id" in body else None  # 评论id
            like_type = body["type"] if "type" in body else None
            like_object = int(body["object"]) if "object" in body else None
            try:
                if like_type == "like":
                    like_comment(like_object, com_id, user_id)
                elif like_type == "unlike":
                    like_comment(like_object + 2, com_id, user_id)
                else:
                    return gen_response(
                        200, {"status": "invalid_like_type", "detail": "你是要点赞还是取消", }
                    )
                return gen_response(200, "点赞成功")
            except Exception as e:
                return gen_response(200, {"status": "like_error", "detail": "点赞失败", })
        else:
            return gen_response(
                200, {"status": "operation_error", "detail": "点赞对象错误%d" % type, }
            )
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


# 管理评论(目前只有删除评论)
def arrange_comment(request, user_id):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    try:
        body = json.loads(request.body)
        com_id = int(body["id"]) if "id" in body else None  # 评论id
        comment_object = int(body["object"]) if "object" in body else None  # 图片或者展览评论
        operation = body["type"] if "type" in body else None
        if operation == "delete":
            try:
                delete_comment(comment_object, com_id)
                return gen_response(200, "delete comment %d" % com_id)
            except Exception as e:
                return gen_response(
                    200, {"status": "delete_comment_error", "detail": "评论删除失败", }
                )
        elif operation == "report":
            try:
                report_comment(comment_object, com_id, user_id)
                return gen_response(200, "report comment %d" % com_id)
            except Exception as e:
                return gen_response(
                    200, {"status": "delete_comment_error", "detail": "评论删除失败", }
                )
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


# 搜索
def search(request):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            search_type = body["type"] if "type" in body else None
            search_filters = body["filters"] if "filters" in body else None
            amount = int(body["amount"]) if "amount" in body else None
            page = int(body["page"]) if "page" in body else 1
            order_name = body["order_name"] if "order_name" in body else None
            order_method = (
                bool(body["order_method"]) if "order_method" in body else None
            )

            if search_type == "exhibit":  # 搜索展览
                gal_all = gallery_advanced_search(
                    search_filters, page, amount, order_name, order_method
                )  # 搜索展览列表
                gal_list = gal_all[1]
                total = gal_all[0]
                try:
                    return gen_response(
                        200,
                        {
                            "mes": [
                                {
                                    "id": gal["id"],
                                    "name": gal["title"],
                                    "introduction": gal["intro"],
                                    "timestamp": gal["pub_date"],
                                    "img_src": gal["cover"],
                                    "comments": len(list(gal["gallery_comment"])),
                                    "likes": gal["like"],
                                    "tag_list": gal["tag"],
                                    "display_image_list": [
                                        {"id": pho["id"], "img_src": pho["photo"]}
                                        for pho in gal["photo"]
                                    ],
                                }
                                for gal in gal_list
                            ],
                            "total": str(total),
                        },
                    )
                except Exception as e:
                    return gen_response(
                        200, {"status": "return_error", "detail": "请求失败", }
                    )

            elif search_type == "photo":  # 搜索照片
                unique = bool(body["unique"])
                pho_all = photo_advanced_search(
                    search_filters, amount, page, order_name, order_method, unique
                )  # 搜索照片列表
                pho_list = pho_all[1]
                total = pho_all[0]
                try:
                    return gen_response(
                        200,
                        {
                            "mes": [
                                {
                                    "id": pho["id"],
                                    "name": pho["title"],
                                    "introduction": pho["info"],
                                    "timestamp": pho["pub_date"],
                                    "img_src": pho["photo"],
                                    "comments": len(list(pho["photo_comment"])),
                                    "likes": pho["like"],
                                    "tag_list": pho["tag"],
                                }
                                for pho in pho_list
                            ],
                            "total": str(total),
                        },
                    )
                except Exception as e:
                    return gen_response(
                        200, {"status": "return_error", "detail": "请求失败", }
                    )

            elif search_type == "photo_comment":  # 搜索照片评论
                com_all = photo_comment_advanced_search(
                    search_filters, amount, page, order_name, order_method
                )
                com_list = com_all[1]
                total = com_all[0]
                pho_list = []  # 每个评论对应的照片
                for com in com_list:
                    com_id = int(com["id"])
                    pho = more_info_on_comment(com_id, 1)
                    pho_list.append(pho)

                try:
                    return gen_response(
                        200,
                        {
                            "mes": [
                                {
                                    "time": com["pub_date"],
                                    "user": {
                                        "id": com["user"]["id"],
                                        "username": com["user"]["name"],
                                        "timestamp": com["user"]["register_date"],
                                        # "comment_cnt": com["user"]["cmt_cnt"],
                                        "user_report": com["user"]["report_cmt_cnt"],
                                    },
                                    "comment": com["content"],
                                    "imgsrc": pho_list[i]["photo"],
                                    "imgname": pho_list[i]["title"],
                                    "imgid": pho_list[i]["id"],
                                    "commentid": com["id"],
                                    "comment_report": com["report_cnt"],
                                    "banned": bool(com["is_banned"]),
                                }
                                for i, com in enumerate(com_list)
                            ],
                            "total": str(total),
                        },
                    )
                except Exception as e:
                    return gen_response(
                        200, {"status": "return_error", "detail": "请求失败", }
                    )

            elif search_type == "gallery_comment":  # 搜索展览评论
                com_all = gallery_comment_advanced_search(
                    search_filters, amount, page, order_name, order_method
                )
                com_list = com_all[1]
                total = com_all[0]
                gal_list = []  # 每个评论对应的照片
                for com in com_list:
                    com_id = int(com["id"])
                    gal = more_info_on_comment(com_id, 0)
                    gal_list.append(gal)
                try:
                    return gen_response(
                        200,
                        {
                            "mes": [
                                {
                                    "time": com["pub_date"],
                                    "user": {
                                        "id": com["user"]["id"],
                                        "username": com["user"]["name"],
                                        "timestamp": com["user"]["register_date"],
                                        # "comment_cnt": com["user"]["cmt_cnt"],
                                        "user_report": com["user"]["report_cmt_cnt"],
                                    },
                                    "comment": com["content"],
                                    "imgsrc": gal_list[i]["cover"],
                                    "imgname": gal_list[i]["title"],
                                    "imgid": gal_list[i]["id"],
                                    "commentid": com["id"],
                                    "comment_report": com["report_cnt"],
                                    "banned": bool(com["is_banned"]),
                                }
                                for i, com in enumerate(com_list)
                            ],
                            "total": str(total),
                        },
                    )
                except Exception as e:
                    return gen_response(
                        200, {"status": "return_error", "detail": "请求失败", }
                    )

            elif search_type == "user":  # 搜索用户
                group = body["group"]
                user_all = user_advanced_search(
                    group, search_filters, page, amount, order_name, order_method
                )
                user_list = user_all[1]
                total = user_all[0]
                try:
                    return gen_response(
                        200,
                        {
                            "mes": [
                                {
                                    "id": user["id"],
                                    "username": user["name"],
                                    "timestamp": user["register_date"],
                                    "comment_cnt": user["cmt_cnt"],
                                    "reported_cnt": user["report_cmt_cnt"],
                                    "group": group,
                                }
                                for user in user_list
                            ],
                            "total": str(total),
                        },
                    )
                except Exception as e:
                    return gen_response(
                        200, {"status": "return_error", "detail": "请求失败", }
                    )
            else:
                return gen_response(200, {"status": "search_error", "detail": "搜索类型错误"})
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法%s" % request.method, }
        )


# 游客部分
def log_in(request):
    """
        这里是登录页面
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            if "login" in body:
                # 处理登录请求
                user_name = body["user"] if "user" in body else None
                password = body["password"] if "password" in body else None
                try:
                    user = get_user_by_name(user_name)  # 这里附带返回user的权限，返回一个权限的列表
                    user_type = "user"
                    user_id = int(user["id"])
                    if is_killed(user_id):
                        return gen_response(
                            200, {"status": "killed_user", "detail": "您的账号已被注销", }
                        )
                    if user_login(request, user_name, password):
                        # 这里附带返回user的权限，返回一个权限的列表
                        user = get_user_by_name(user_name)
                        user_type = "user"
                        user_id = int(user["id"])
                        if is_admin(user_id):
                            user_type = "admin"
                        elif user_is_banned(user_id):
                            user_type = "banned_user"
                        return gen_response(
                            200,
                            {
                                "id": user["id"],
                                "name": user["name"],
                                "avatar": user["avatar"],
                                "type": user_type,
                            },
                        )
                    else:  # 密码错误
                        return gen_response(
                            200, {"status": "password_error", "detail": "密码错误！", }
                        )
                except Exception as e:  # 用户不存在
                    return gen_response(
                        200, {"status": "user_exist_error", "detail": "用户名不存在！", }
                    )
            elif "register" in body:
                # 处理注册请求
                user_name = body["user"] if "user" in body else None
                password = body["password"] if "password" in body else None
                try:
                    register_date = timezone.now()  # 注册的时间
                    user = create_user(
                        user_name,
                        register_date,
                        avatar="test_photos/test_avatar.jpeg",
                        admin=False,
                        password=password,
                    )  # 新建用户，默认不是管理员
                    user_login(request, user_name, password)  # 直接登陆
                    return gen_response(
                        200,
                        {
                            "id": user["id"],
                            "name": user["name"],
                            "avatar": user["avatar"],
                        },
                    )
                except Exception as e:
                    return gen_response(
                        200, {"status": "register_error", "detail": "该名称已被注册", }
                    )
            elif "log_out" in body:
                # 注销/登出
                user_logout(request)  # 该函数尚未实现
                return gen_response(200, "Log out!")
            elif "change_password" in body:
                # 更改密码
                user_id = int(body["id"])  # 用户id
                old_password = body["old_password"] if "old_password" in body else None
                new_password = body["new_password"] if "new_password" in body else None
                try:
                    change_password(user_id, old_password, new_password)
                    return gen_response(200, "change password!")
                except Exception as e:
                    return gen_response(
                        200, {"status": "changepassword_error", "detail": "原密码错误", }
                    )
            else:
                return gen_response(200, {"status": "error", "detail": "非法登录操作", })
            # 之后去寻找用户
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    elif request.method == "GET":
        try:
            django_user = request.user
            if hasattr(django_user, "user"):
                model_user = django_user.user
                try:
                    user = get_user(model_user.id)
                except Exception as e:
                    return gen_response(
                        200, {"status": "invalid_user", "detail": "查无此人", }
                    )
                user_type = "user"
                user_id = int(user["id"])
                if is_admin(user_id):
                    user_type = "admin"
                elif user_is_banned(user_id):
                    user_type = "banned_user"
                return gen_response(
                    200,
                    {
                        "id": user["id"],
                        "name": user["name"],
                        "avatar": user["avatar"],
                        "type": user_type,
                    },
                )
            else:
                return gen_response(
                    200, {"status": "error", "detail": "您已掉线", }
                )  # 似乎掉线了
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法%s" % request.method, }
        )


def tourist_home(request):
    """
        这里是所有展览的页面
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    # 显示所有展览
    if request.method == "GET":
        try:
            gal_list = []
            try:
                gal_list = get_all_galleries()  # 所有展览的序列，为list
            except Exception as e:
                return gen_response(
                    200, {"status": "getgallery_error", "detail": "展览出现了一些问题", }
                )

            logged_in = request_user_authenticated(request)  # 如果用户登录
            if logged_in:
                user_id = request_user_id(request)

            gal_liked_list = []
            for gal in gal_list:
                if logged_in:
                    gal_id = int(gal["id"])
                    if gallery_liked(user_id, gal_id):
                        gal_liked_list.append(True)
                    else:
                        gal_liked_list.append(False)
                else:
                    gal_liked_list.append(False)

            return gen_response(
                200,
                [
                    {
                        "id": gal["id"],  # 展览id
                        "name": gal["title"],  # 展览名称
                        "introduction": gal["intro"],  # 展览介绍
                        "timestamp": gal["pub_date"],  # 展览时间戳，但是dcq似乎没有加上这个
                        "img_src": gal["cover"],  # 展览封面图片
                        "comments": len(list(gal["gallery_comment"])),  # 展览评论数
                        "likes": gal["like"],  # 展览获赞数
                        "tag_list": gal["tag"],  # 标签列表
                        "liked": gal_liked_list[i],
                    }
                    for i, gal in enumerate(gal_list)
                ],
            )
        # 显示所有展览
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法%s" % request.method, }
        )


def exhibit_info(request):
    """
        这里是某个展览
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    # 请求某个展览所有信息
    if request.method == "GET":
        try:
            body = request.GET
            gal_id = int(body["id"]) if "id" in body else None
            gal = {}
            try:
                gal = get_gallery(gal_id)  # 展览信息dict
            except Exception as e:
                return gen_response(
                    200, {"status": "invalid_gallery", "detail": "此展览不存在！", }
                )
            pho_list = gal["photo"]  # 展览中的照片列
            gal_liked = False  # 该展览是否已被点赞
            pho_liked_list = []
            logged_in = request_user_authenticated(request)  # 如果用户登录
            if logged_in:
                user_id = request_user_id(request)
            for pho in pho_list:
                if logged_in:
                    pho_id = int(pho["id"])
                    if photo_liked(user_id, pho_id):
                        pho_liked_list.append(True)
                    else:
                        pho_liked_list.append(False)
                else:
                    pho_liked_list.append(False)

            if logged_in and gallery_liked(user_id, gal_id):  # 如果用户登录
                gal_liked = True

            return gen_response(
                200,
                {
                    "img_list": [
                        {  # 显示展览内的所有图片
                            "id": pho["id"],  # 图片id
                            "name": pho["title"],  # 图片名称
                            "introduction": pho["info"],  # 图片简介
                            "timestamp": pho["pub_date"],  # 图片上传时间
                            "img_src": pho["photo"],  # 源图片
                            "comments": len(list(pho["photo_comment"])),  # 图片评论
                            "likes": pho["like"],  # 图片获赞
                            "tag_list": pho["tag"],  # 标签列表
                            "liked": pho_liked_list[i],
                        }
                        for i, pho in enumerate(pho_list)
                    ],
                    "exhibit_info": {
                        "id": gal["id"],  # 展览id
                        "name": gal["title"],  # 展览名称
                        "introduction": gal["intro"],  # 展览简介
                        "timestamp": gal["pub_date"],
                        "img_src": gal["cover"],  # 展览封面
                        "comments": len(list(gal["gallery_comment"])),
                        "likes": gal["like"],  # 展览获赞
                        "tag_list": gal["tag"],  # 标签列表
                        "liked": gal_liked,
                        "style": gal["layout"],  # 展览样式
                        "publisher_name": gal["user"]["name"],
                        "publisher_id": gal["user"]["id"],
                    },
                },
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })

    # 点赞或评论展览
    elif request.method == "POST":
        try:
            # 这里鉴别用户是否登录，没有登陆则不能点赞或者评论
            if not request_user_authenticated(request):
                return gen_response(200, {"status": "error", "detail": "请先登录", })
            user_id = request_user_id(request)
            return gallery_commentandlike(request, user_id)
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def gallery_commentandlike(request, user):
    """
        展览点赞和评论的处理
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    try:
        user_id = user
        body = json.loads(request.body)
        op_type = int(body["type"]) if "type" in body else None  # 类型
        if op_type == 1:  # 点赞
            return post_like(request, 0, 0, user_id)
        elif op_type == 2:  # 评论
            return post_comment(request, 0, user_id)
        elif op_type == 3:  # 取消点赞
            return post_like(request, 0, 1, user_id)
        else:
            return gen_response(
                200, {"status": "error", "detail": "Invalid type %d" % op_type, }
            )
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


def photo_info(request):
    """
        获取照片信息
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    # 请求某个照片的信息
    if request.method == "GET":
        try:
            body = request.GET
            pho_id = int(body["id"]) if "id" in body else None
            pho = {}
            try:
                pho = get_photo(pho_id)  # 照片信息dict
            except Exception as e:
                return gen_response(
                    200, {"status": "invalid_photo", "ddetail": "此照片不存在!", }
                )

            pho_liked = False  # 该图片是否已被点赞
            if request_user_authenticated(request):  # 如果用户登录
                user_id = request_user_id(request)
                if photo_liked(user_id, pho_id):
                    pho_liked = True

            return gen_response(
                200,
                {
                    "id": pho["id"],
                    "name": pho["title"],
                    "introduction": pho["info"],
                    "timestamp": pho["pub_date"],
                    "img_src": pho["photo"],
                    "old_img_src": pho["old_photo"],
                    "comments": len(list(pho["photo_comment"])),
                    "likes": pho["like"],
                    "tag_list": pho["tag"],  # 标签列表
                    "liked": pho_liked,
                    "publisher_name": pho["user"]["name"],
                    "publisher_id": pho["user"]["id"],
                },
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })

    # 评论或点赞照片
    elif request.method == "POST":
        try:
            # 这里鉴别用户是否登录，没有登陆则不能点赞或者评论
            if not request_user_authenticated(request):
                return gen_response(200, {"status": "login_error", "detail": "请先登录", })
            user_id = request_user_id(request)
            return photo_commentandlike(request, user_id)
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def photo_commentandlike(request, user_id):
    """
        照片点赞和评论的处理
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    try:
        body = json.loads(request.body)
        op_type = int(body["type"]) if "type" in body else None  # 类型
        if op_type == 1:  # 点赞
            return post_like(request, 1, 0, user_id)
        elif op_type == 2:  # 评论
            return post_comment(request, 1, user_id)
        elif op_type == 3:  # 取消点赞
            return post_like(request, 1, 1, user_id)
        else:
            return gen_response(
                200, {"status": "error", "detail": "Invalid type %d" % op_type, }
            )
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


def comment_info(request):
    """
        照片评论
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    # 获取评论信息
    if request.method == "GET":
        try:
            body = request.GET
            _type = int(body["type"]) if "type" in body else None
            _id = int(body["id"]) if "id" in body else None
            _order = int(body["order"]) if "order" in body else None
            _start = int(body["start"]) if "start" in body else None
            com_list = []
            try:
                com_list = get_comment(_id, _type, _order, _start)  # 评论列表
            except Exception as e:
                return gen_response(
                    200, {"status": "invalid_comments", "detail": "无法加载评论"}
                )

            com_liked_list = []
            com_reported_list = []

            logged_in = request_user_authenticated(request)  # 如果用户登录
            if logged_in:
                user_id = request_user_id(request)

            for com in com_list:
                com_id = int(com["id"])
                if logged_in:
                    if _type == 0:  # 展览评论
                        if gallery_comment_liked(user_id, com_id):
                            com_liked_list.append(True)
                        else:
                            com_liked_list.append(False)
                        if gallery_comment_reported(user_id, com_id):
                            com_reported_list.append(True)
                        else:
                            com_reported_list.append(False)

                    else:  # 照片评论
                        if photo_comment_liked(user_id, com_id):
                            com_liked_list.append(True)
                        else:
                            com_liked_list.append(False)
                        if photo_comment_reported(user_id, com_id):
                            com_reported_list.append(True)
                        else:
                            com_reported_list.append(False)

                else:
                    com_liked_list.append(False)
                    com_reported_list.append(False)

            return gen_response(
                200,
                [
                    {
                        "id": com["id"],
                        "user": com["user"]["name"],  # 用户名称
                        "avatar": com["user"]["avatar"],  # 用户头像
                        "content": "【该评论已被删除】" if com["is_banned"] else com["content"],
                        "likes": com["like"],
                        "timestamp": com["pub_date"],
                        "liked": com_liked_list[i],
                        "reported": com_reported_list[i],
                    }
                    for i, com in enumerate(com_list)
                ],
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    # 点赞评论
    elif request.method == "POST":
        try:
            # 这里鉴别用户是否登录，没有登陆则不能点赞或者评论
            if not request_user_authenticated(request):
                return gen_response(200, {"status": "login_error", "detail": "请先登录", })
            user_id = request_user_id(request)
            return comment_likeandarrange(request, user_id)
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def comment_likeandarrange(request, user_id):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    try:
        body = json.loads(request.body)
        op_type = body["type"] if "type" in body else None
        if op_type == "like" or op_type == "unlike":  # 给照片或展览点赞或取消点赞
            post_like(request, 2, 0, user_id)
        elif op_type == "delete" or op_type == "report":  # 删除评论或举报评论
            arrange_comment(request, user_id)
        else:
            return gen_response(
                200, {"status": "error", "detail": "Invalid type %s" % op_type, }
            )
        return gen_response(200, "like!")
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


def repair_info(request):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if request.method == "GET":
        try:
            if not request_user_authenticated(request):
                return gen_response(200, {"status": "login_error", "detail": "请先登录", })
            body = request.GET
            photo_id = int(body["id"]) if "id" in body else None
            photo_dict = {}
            try:
                photo_dict = get_photo(photo_id)
            except Exception as e:
                return (200, {"status": "invalid_photo", "detail": "此照片不存在", })

            series_id = int(photo_dict["group_id"])  # 照片系列的id
            series_list = {}
            try:
                series_list = get_photo_by_group_id(series_id)  # 寻找一个系列的照片
            except Exception as e:
                return gen_response(
                    200, {"status": "invalid_photo_series", "detail": "无效的照片系列", }
                )
            origin_pho = {}

            for p in series_list:
                if p["id"] == p["group_id"]:
                    origin_pho = dict(p)  # 寻找原照片

            pub_time = float(origin_pho["pub_date"])
            now = time.time()
            wait_time = now - pub_time + 0.001
            now_time = now - pub_time

            op_nums = int(len(series_list) - 1)
            expect_time = op_nums * 6

            flag = False

            if expect_time < now_time + 4:
                expect_time = now_time + 5
            fixing_operation = "稍等片刻"
            tag_list = origin_pho["tag"]
            for t in tag_list:
                if t["tag"] == "排队等待中":
                    fixing_operation = "排队等待中"
                    now_time = 0  # 即排队等待中认为尚未开始修理
                    expect_time = 0
                else:
                    if t["tag"] == "已修复":
                        flag = True
                        wait_time = 0
                    elif t["tag"] == "上色中":
                        fixing_operation = "上色中"
                        wait_time = 0
                    elif t["tag"] == "对比度增强中":
                        fixing_operation = "对比度增强中"
                        wait_time = 0
                    elif t["tag"] == "清晰度增强中":
                        fixing_operation = "清晰度增强中"
                        wait_time = 0
                    elif t["tag"] == "图像除雾中":
                        fixing_operation = "图像除雾中"
                        wait_time = 0
                    elif t["tag"] == "修复失败":
                        flag = True
                        wait_time = 0

            return gen_response(
                200,
                {
                    "image_history_list": [
                        {
                            "id": pho["id"],
                            "name": pho["title"],
                            "introduction": pho["info"],
                            "timestamp": pho["pub_date"],
                            "img_src": pho["photo"],
                            "comments": len(list(pho["photo_comment"])),
                            "likes": pho["like"],
                            "tag_list": pho["tag"],  # 标签列表
                            "publisher_name": pho["user"]["name"],
                            "publisher_id": pho["user"]["id"],
                        }
                        for pho in series_list
                    ],
                    # 以下是原照片的信息
                    "name": origin_pho["title"],
                    "introduction": origin_pho["info"],
                    "img_src": origin_pho["photo"],
                    "now_time": now_time,
                    "expect_time": expect_time,
                    "wait_time": wait_time,
                    "operation": fixing_operation,
                    "flag": flag,  # 已完成修复
                    "publisher_name": origin_pho["user"]["name"],
                    "publisher_id": origin_pho["user"]["id"],
                },
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def user_info(request):
    """
        用户信息页
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if request.method == "GET":
        try:
            body = request.GET
            user_id = int(body["id"]) if "id" in body else None
            user = {}
            try:
                user = get_user(user_id)
            except Exception as e:
                return gen_response(200, {"status": "invalid_user", "detail": "查无此人", })
            can_postlike = True
            can_postcomment = True
            can_viewrepair = True
            user_state = "正常"
            if is_admin(user_id):
                user_state = "管理员"
                if user_is_banned(user_id):
                    can_postcomment = False
            elif user_is_banned(user_id):
                user_state = "封禁中"
                can_postcomment = False
            elif is_killed(user_id):
                user_state = "已注销"
                can_postcomment = False
                can_postlike = False
                can_viewrepair = False

            return gen_response(
                200,
                {
                    "user_info": {
                        "register_time": user["register_date"],
                        "state": user_state,
                        "permissions": [
                            {"label": "点赞", "type": can_postlike, },
                            {"label": "评论", "type": can_postcomment},
                            {"label": "访问修复详情", "type": can_viewrepair, },
                        ],
                    }
                },
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    elif request.method == "POST":
        try:
            # 更换头像必须登录
            if not request_user_authenticated(request):
                return gen_response(200, {"status": "login_error", "detail": "请先登录", })

            user_id = request_user_id(request)
            return change_avatar(request, user_id)
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def change_avatar(request, user_id):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    try:
        body = json.loads(request.body)
        if "avatar" in body:
            user_avatar = body["avatar_src"] if "avatar_src" in body else None
            change_user_avatar(user_id, user_avatar)
        else:
            return gen_response(200, {"status": "operation_error", "detail": "非法的操作", })
        return gen_response(200, "头像更改成功")
    except Exception as e:
        return gen_response(200, {"status": "request_error", "detail": "请求失败", })


# 管理员部分, 所有页面都必须登录才可以查看
def fixupload_photos(request):
    """
        鉴权块
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):  #
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )

    return fixupload_photos_body(request, user_id)


def fixupload_photos_body(request, user_id):
    """
        照片修复
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if request.method == "POST":
        body = json.loads(request.body)
        operation = body["wanted"] if "wanted" in body else "unknown"
        if operation == "please_fix" and "data" in body:
            fix_list = []
            refix_list = []
            fix_photos = []
            if "fixlist" in body["data"]:
                # 需要修复的照片列表，由base64构成
                fix_list = list(body["data"]["fixlist"])
            elif "refix" in body["data"]:
                refix_list = list(body["data"]["refix"])
            fix_step = (
                list(body["data"]["fixstep"]) if "fixstep" in body["data"] else []
            )
            pub_date = time.time()

            # 重修照片
            for photo in refix_list:
                pho_id = photo
                photo = get_photo(pho_id)
                if pho_id != photo["group_id"]:
                    continue
                photos = get_photo_by_group_id(photo["group_id"])
                for pho in photos:
                    if pho["id"] != pho["group_id"]:
                        delete_photo(pho["id"])
                photo_base64 = from_id_to_base64(0, pho_id)
                fix_photos.append(
                    {
                        "base64": photo_base64,
                        "group_id": pho_id,
                        "title": photo["title"],
                        "info": photo["info"],
                        "refix": True,
                    }
                )
            # 修复照片
            for pho_base64 in fix_list:
                # 保存照片(表示当前阶段的照片)
                current_photo = (
                    pho_base64,
                    create_photo_base64(pho_base64, user_id, pub_date),
                )
                group_id = current_photo[1]["id"]
                title = current_photo[1]["title"]
                info = current_photo[1]["info"]
                fix_photos.append(
                    {
                        "base64": pho_base64,
                        "group_id": group_id,
                        "title": title,
                        "info": info,
                        "refix": False,
                    }
                )

            for photo in fix_photos:
                pho_base64 = photo["base64"]
                group_id = photo["group_id"]
                title = photo["title"]
                info = photo["info"]
                refix = photo["refix"]
                if pho_base64 is None:
                    assert refix
                    logger.error("{} photo base64 None".format(group_id))
                    continue
                photo_remove_tags(int(group_id), ["修复失败"])
                photo_add_tags(int(group_id), ["原图"], True)
                photo_add_tags(int(group_id), ["修复中"], True)
                photo_add_tags(int(group_id), ["排队等待中"], True)
                tag = "已修复"
                temp_id = []
                fixed_list = []  # 已经进行过的修理
                for op in fix_step:
                    if op != "shangse" and\
                        op != "duibidu" and\
                        op != "qingxidu" and\
                            op != "tuxiangchuwu":
                        break
                    temp_photo = create_photo_base64(pho_base64, user_id, pub_date)
                    set_group_id(int(temp_photo["id"]), group_id)
                    photo_add_tags(int(temp_photo["id"]), ["待修复"], True)
                    temp_id.append(int(temp_photo["id"]))

                while True:
                    # f = open("gallery/queue.txt", "r", encoding="utf-8")
                    # queue_length = int(f.read())
                    # f.close()
                    queue_length = get_queue("fix")
                    if queue_length < MAX_QUEUE_LENGTH:  # 如果在修复的照片数量小于最大排队数
                        ret = push_queue("fix")
                        if ret is not None:
                            queue_length = ret
                        else:
                            continue
                        logger.info("{} start fixing".format(group_id))
                        photo_remove_tags(int(group_id), ["排队等待中"])
                        change_photo_pubdate_now(int(group_id))
                        for i, op in enumerate(fix_step):
                            if op == "shangse":  # 上色
                                fixed_list.append("黑白上色")
                                photo_add_tags(int(group_id), ["上色中"], True)
                                current_photo = image_colourize(
                                    temp_id[i], pho_base64, title, info, tag, user_id
                                )
                                if current_photo is None:
                                    logger.error("{} error".format(temp_id[i]))
                                    photo_add_tags(int(group_id), ["修复失败"], True)
                                    photo_remove_tags(int(group_id), ["修复中"])
                                    photo_add_tags(int(temp_id[i]), ["修复失败"], True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])
                                    photo_remove_tags(int(group_id), ["上色中"])
                                    photo_add_tags(int(temp_id[i]), ["上色失败"], True)
                                    assert pop_queue("fix")
                                    return gen_response(
                                        200, {"status": "fix_error", "detail": "图片上色失败"}
                                    )
                                else:
                                    photo_remove_tags(int(group_id), ["上色中"])
                                    photo_add_tags(int(temp_id[i]), fixed_list, True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])

                            elif op == "duibidu":  # 对比度增强
                                fixed_list.append("对比度增强")
                                photo_add_tags(int(group_id), ["对比度增强中"], True)
                                current_photo = image_enhance_contrast(
                                    temp_id[i], pho_base64, title, info, tag, user_id
                                )
                                if current_photo is None:
                                    logger.error("{} error".format(temp_id[i]))
                                    photo_add_tags(int(group_id), ["修复失败"], True)
                                    photo_remove_tags(int(group_id), ["修复中"])
                                    photo_add_tags(int(temp_id[i]), ["修复失败"], True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])
                                    photo_remove_tags(int(group_id), ["对比度增强中"])
                                    photo_add_tags(int(temp_id[i]), ["对比度增强失败"], True)
                                    assert pop_queue("fix")
                                    return gen_response(
                                        200,
                                        {"status": "fix_error", "detail": "图片对比度增强失败"},
                                    )
                                else:
                                    photo_remove_tags(int(group_id), ["对比度增强中"])
                                    photo_add_tags(int(temp_id[i]), fixed_list, True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])

                            elif op == "tuxiangchuwu":  # 图像除雾
                                fixed_list.append("图像除雾")
                                photo_add_tags(int(group_id), ["图像除雾中"], True)
                                current_photo = image_defog(
                                    temp_id[i], pho_base64, title, info, tag, user_id
                                )
                                if current_photo is None:
                                    logger.error("{} error".format(temp_id[i]))
                                    photo_add_tags(int(group_id), ["修复失败"], True)
                                    photo_remove_tags(int(group_id), ["修复中"])
                                    photo_add_tags(int(temp_id[i]), ["修复失败"], True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])
                                    photo_remove_tags(int(group_id), ["图像除雾中"])
                                    photo_add_tags(int(temp_id[i]), ["图像除雾失败"], True)
                                    assert pop_queue("fix")
                                    return gen_response(
                                        200, {"status": "fix_error", "detail": "图片除雾失败"}
                                    )
                                else:
                                    photo_remove_tags(int(group_id), ["图像除雾中"])
                                    photo_add_tags(int(temp_id[i]), fixed_list, True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])

                            elif op == "qingxidu":  # 清晰度增强
                                fixed_list.append("清晰度增强")
                                photo_add_tags(int(group_id), ["清晰度增强中"], True)
                                current_photo = img_sharpness_enhancement(
                                    temp_id[i], pho_base64, title, info, tag, user_id
                                )
                                if current_photo is None:
                                    logger.error("{} error".format(temp_id[i]))
                                    photo_add_tags(int(group_id), ["修复失败"], True)
                                    photo_remove_tags(int(group_id), ["修复中"])
                                    photo_add_tags(int(temp_id[i]), ["修复失败"], True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])
                                    photo_remove_tags(int(group_id), ["清晰度增强中"])
                                    photo_add_tags(int(temp_id[i]), ["清晰度增强失败"], True)
                                    assert pop_queue("fix")
                                    return gen_response(
                                        200,
                                        {"status": "fix_error", "detail": "图片清晰度增强失败"},
                                    )
                                else:
                                    photo_remove_tags(int(group_id), ["清晰度增强中"])
                                    photo_add_tags(int(temp_id[i]), fixed_list, True)
                                    photo_remove_tags(int(temp_id[i]), ["待修复"])

                            elif op == "none":  # 什么都不做
                                current_photo = current_photo
                            elif op == "":
                                break
                            else:
                                return gen_response(
                                    200,
                                    {"status": "error", "detail": "无效的图片修复方法 %s" % op, },
                                )
                            pho_base64 = current_photo[0]
                            group_id = current_photo[1]["group_id"]
                            tag = "已修复"
                        photo_remove_tags(int(group_id), ["修复中"])
                        photo_add_tags(int(group_id), ["已修复"], True)

                        sleep_time = random.uniform(0.1, 5.0)
                        time.sleep(sleep_time)
                        assert pop_queue("fix")
                        break

                    time.sleep(1)
            return gen_response(200, "start fix")  # 开始修复
        else:
            return gen_response(
                200, {"status": "operation_error", "detail": "非法的操作 %s" % operation, }
            )

    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def photo_admin(request):
    """
        鉴权块
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):  #
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )

    return photo_admin_body(request, user_id)


def photo_admin_body(request, admin):
    """
        直接展示所有照片
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    admin_id = admin
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            operation = body["wanted"] if "wanted" in body else "unknown"
            op_info = dict(body["data"])  # 操作信息，一个字典对象

            if operation == "change_name":  # 改名
                pho_id = int(op_info["id"])  # 照片id
                pho_newname = op_info["new"]
                try:
                    change_photo_title(pho_id, pho_newname)
                    return gen_response(200, "name changed")
                except Exception as e:
                    raise
                    return gen_response(
                        200, {"status": "change_photo_error", "detail": "照片名称更改失败", }
                    )

            elif operation == "change_intro":  # 修改信息
                pho_id = int(op_info["id"])  # 照片id
                pho_newintro = op_info["new"]
                try:
                    change_photo_info(pho_id, pho_newintro)
                    return gen_response(200, "intro changed")
                except Exception as e:
                    raise
                    return gen_response(
                        200, {"status": "change_photo_error", "detail": "照片信息更改失败", }
                    )

            elif operation == "change_tag":  # 修改标签
                pho_id = int(op_info["id"])  # 照片id
                pho_newtag = list(op_info["new"])
                try:
                    photo_change_tags(pho_id, pho_newtag)
                    return gen_response(200, "name changed")
                except Exception as e:
                    raise
                    return gen_response(
                        200, {"status": "change_photo_error", "detail": "照片标签更改失败", }
                    )

            elif operation == "delete":  # 删除
                pho_id = int(op_info["id"])
                try:
                    delete_photo(pho_id)
                    return gen_response(200, "delete photo %d" % pho_id)
                except Exception as e:
                    raise
                    return gen_response(
                        200, {"status": "change_photo_error", "detail": "照片删除失败", }
                    )

            else:
                return gen_response(
                    200,
                    {"status": "operation_error", "detail": "非法的操作 %s" % operation, },
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })

    elif request.method == "GET":
        try:
            all_phos = []
            try:
                all_phos = get_all_photos()  # 所有照片的列表，获取的函数尚未实现
            except Exception as e:
                return gen_response(
                    200, {"status": "getphoto_error", "detail": "照片出现了一些问题", }
                )

            return gen_response(
                200,
                [
                    {
                        "imgURL": pho["photo"],  # 图片源图像
                        "taglist": pho["tag"],  # 图片标签
                        "name": pho["title"],  # 图片名称
                        "id": pho["id"],  # 图片id
                        "timestamp": pho["pub_date"],
                        "comments": len(list(pho["comment_list"])),  # 评论
                        "tag_list": pho["tag"],  # 标签列表
                        "publisher_name": pho["user"]["name"],
                        "publisher_id": pho["user"]["id"],
                    }
                    for pho in all_phos
                ],
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def gallery_admin(request):
    """
        鉴权块
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )

    return gallery_admin_body(request, user_id)


def gallery_admin_body(request, admin):
    """
        直接展示所有展览
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    admin_id = admin  # 用户id

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            operation = body["wanted"] if "wanted" in body else "unknown"
            op_info = dict(body["data"])  # 操作信息，一个字典对象

            if operation == "change_name":  # 改名
                gal_id = int(op_info["id"])  # 展览id
                gal_newname = op_info["new"]
                try:
                    change_gallery_title(gal_id, gal_newname)
                    return gen_response(200, "name changed")
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_gallery_error", "detail": "展览名称更改失败", }
                    )

            elif operation == "change_intro":  # 修改信息
                gal_id = int(op_info["id"])  # 展览id
                gal_newintro = op_info["new"]
                try:
                    change_gallery_intro(gal_id, gal_newintro)
                    return gen_response(200, "intro changed")
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_gallery_error", "detail": "展览信息更改失败", }
                    )

            elif operation == "change_tag":  # 修改标签
                gal_id = int(op_info["id"])  # 展览id
                gal_newtag = list(op_info["new"])
                try:
                    gallery_add_tags(gal_id, gal_newtag)
                    return gen_response(200, "name changed")
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_gallery_error", "detail": "展览标签更改失败", }
                    )

            elif operation == "delete":  # 删除
                gal_id = int(op_info["id"])
                try:
                    delete_gallery(gal_id)
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_gallery_error", "detail": "展览删除失败", }
                    )
                return gen_response(200, "delete gallery %d" % gal_id)

            else:
                return gen_response(
                    200,
                    {"status": "operation_error", "detail": "非法的操作 %s" % operation, },
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })

    elif request.method == "GET":
        try:
            all_gals = []
            try:
                all_gals = get_all_galleries()
            except Exception as e:
                return gen_response(
                    200, {"status": "getgallery_error", "detail": "展览出现了一些问题", }
                )
            return gen_response(
                200,
                [
                    {
                        "urlsource": gal["cover"],  # 展览封面
                        "info": gal["intro"],  # 展览简介
                        "name": gal["title"],  # 展览名称
                        "timestamp": gal["pub_date"],  # 上传时间
                        "tag_list": gal["tag"],  # 标签列表
                        "style": gal["layout"],  # 展览样式
                    }
                    for gal in all_gals
                ],
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def edit_gallery(request):
    """
        鉴权块
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )

    return edit_gallery_body(request, user_id)


def edit_gallery_body(request, admin):
    """
        展览增减图片
    """

    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    admin_id = admin  # 用户id

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            gal_id = int(body["id"])

            if "add" in body:  # 添加照片
                pho_list = list(body["postlist"])
                for pho in pho_list:
                    pho_id = int(pho)
                    try:
                        gallery_add_photo(gal_id, pho_id)
                    except Exception as e:
                        return gen_response(
                            200, {"status": "add_photo_error", "detail": "展览添加照片失败！"}
                        )
                return gen_response(200, "add")

            elif "delete" in body:  # 删除照片
                pho_list = list(body["postlist"])
                for pho in pho_list:
                    pho_id = int(pho)
                    try:
                        remove_photo_from_gallery(gal_id, pho_id)
                    except Exception as e:
                        return gen_response(
                            200,
                            {"status": "delete_photo_error", "detail": "从展览中移除照片失败！"},
                        )
                return gen_response(200, "delete")

            elif "cover" in body:  # 更改封面
                try:
                    if "cover_src" in body:
                        new_cover = body["cover_src"]
                    elif "cover_id" in body:
                        new_cover_id = body["cover_id"]
                        new_cover = from_id_to_base64(0, new_cover_id)
                    assert new_cover is not None
                    change_gallery_cover(gal_id, new_cover, admin_id)
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_cover_error", "detail": "更换展览封面失败！"}
                    )
                return gen_response(200, "cover changed!")

            elif "style" in body:  # 更改样式
                new_style = body["style_name"]
                try:
                    change_gallery_layout(gal_id, new_style)
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_style_error", "detail": "更换展览样式失败！"}
                    )
                return gen_response(200, "style changed!")

            elif "order" in body:
                assert body["order"]
                new_order = body["new_image_list"]
                new_order = [x["id"] for x in new_order]
                try:
                    change_gallery_order(gal_id, new_order)
                except Exception as e:
                    return gen_response(
                        200, {"status": "change_order_error", "detail": "更改照片顺序失败！"}
                    )
                return gen_response(200, "order changed!")
            else:
                return gen_response(
                    200, {"status": "operation_error", "detail": "非法的操作", }
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def setnew_gallery(request):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )

    return setnew_gallery_body(request, user_id)


def setnew_gallery_body(request, admin):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    admin_id = admin

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            operation = body["wanted"] if "wanted" in body else "unknown"
            if operation == "send_new_gallery":
                new_gallery = dict(body["info"])
                gallery_name = new_gallery["name"]
                gallery_info = new_gallery["info"]
                pho_list = list(new_gallery["postlist"])
                new_gal = create_gallery(gallery_name, gallery_info, pho_list, admin_id)
                has_cover = bool(new_gallery["ifcover"])
                if has_cover:
                    gal_id = int(new_gal["id"])
                    cover = new_gallery["cover"][0]
                    pub_date = timezone.now()

                    cover_type = new_gallery["covertype"]
                    if cover_type == "src":
                        cover = from_id_to_base64(0, int(cover))
                    try:
                        change_gallery_cover(gal_id, cover, admin_id, pub_date)
                    except Exception as e:
                        return gen_response(
                            200,
                            {
                                "status": "set_cover_error",
                                "detail": "展览创建成功，但封面上传出现问题",
                            },
                        )
                return gen_response(200, "new gallery set")
            else:
                return gen_response(
                    200,
                    {"status": "operation_error", "detail": "非法的操作 %s" % operation, },
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    elif request.method == "GET":
        try:
            body = request.GET
            operation = body["wanted"] if "wanted" in body else "unknown"
            if operation == "send_all_photos":
                try:
                    all_phos = get_all_photos()  # 新建展览所有照片的列表
                except Exception as e:
                    return gen_response(
                        200, {"status": "getphoto_error", "detail": "照片出现了一些问题", }
                    )
                return gen_response(
                    200,
                    [
                        {
                            "imgURL": pho["photo"],  # 图片源图像
                            "taglist": pho["tag"],  # 图片标签
                            "name": pho["title"],  # 图片名称
                            "id": pho["id"],  # 图片id
                            "timestamp": pho["pub_date"],
                        }
                        for pho in all_phos
                    ],
                )
            else:
                return gen_response(
                    200,
                    {"status": "operation_error", "detail": "非法的操作 %s" % operation, },
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def admin_tourist(request):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )

    return admin_tourist_body(request, user_id)


def admin_tourist_body(request, admin):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    admin_id = admin

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            operation = body["wanted"] if "wanted" in body else "unknown"
            users = list(body["data"]) if "data" in body else []  # 用户id列表

            if operation == "forbiduser":  # 封禁用户
                for user_id in users:
                    try:
                        ban_user(int(user_id))
                    except Exception as e:
                        pass
                return gen_response(200, "banned users")

            elif operation == "unforbiduser":  # 解封用户
                for user_id in users:
                    try:
                        unban_user(int(user_id))
                    except Exception as e:
                        pass
                return gen_response(200, "free users")

            elif operation == "deleteuser":  # 删除用户
                for user_id in users:
                    try:
                        kill_user(int(user_id))
                    except Exception as e:
                        pass
                return gen_response(200, "delete users")

            elif operation == "undeleteuser":  # 复活用户
                for user_id in users:
                    try:
                        revive_user(int(user_id))
                        unban_user(int(user_id))
                    except Exception as e:
                        pass
                return gen_response(200, "delete users")

            elif operation == "deletetoforbid":
                for user_id in users:
                    try:
                        revive_user(int(user_id))
                    except Exception as e:
                        pass
                return gen_response(200, "delete users")

            else:
                return gen_response(
                    200,
                    {"status": "operation_error", "detail": "非法的操作 %s" % operation, },
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法 %s" % request.method, }
        )


def admin_comment(request):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    if not request_user_authenticated(request):
        return gen_response(200, {"status": "login_error", "detail": "请先登录", })
    user_id = request_user_id(request)  # 用户id

    if not is_admin(user_id):  # 判断是否是管理员
        return gen_response(
            200, {"status": "permission_error", "detail": "非管理员用户不可访问该页面", }
        )
    return admin_comment_body(request, user_id)


def admin_comment_body(request, admin_id):
    def gen_response(code: int, data: str):
        return JsonResponse({"code": code, "data": data}, status=code)

    admin = admin_id

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            operation = body["operation"] if "operation" in body else "unknown"
            com_list = body["list"] if "list" in body else []
            _type = body["type"]
            com_type = 2
            if _type == "photo_comment":
                com_type = 0
            elif _type == "gallery_comment":
                com_type = 1
            if operation == "alive":
                for com_id in com_list:
                    revive_comment(com_type, com_id)
                return gen_response(200, "revive comments")

            elif operation == "delete":
                for com_id in com_list:
                    delete_comment(com_type, com_id)
                return gen_response(200, "delete comments")

            elif operation == "forbid":
                for com_id in com_list:
                    forbid_comment(com_type, com_id)
                return gen_response(200, "forbid comments")

            else:
                return gen_response(
                    200,
                    {"status": "operation_error", "detail": "非法的操作 %s" % operation, },
                )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })

    elif request.method == "GET":
        try:
            pho_com_list = []
            gal_com_list = []
            try:
                pho_com_list = get_all_photo_comments()
            except Exception as e:
                return gen_response(
                    200, {"status": "getphotocomment_error", "detail": "照片评论出现了一些问题", }
                )

            try:
                gal_com_list = get_all_gallery_comments()
            except Exception as e:
                return gen_response(
                    200, {"status": "getgallerycomment_error", "detail": "展览评论出现了一些问题", }
                )
            return gen_response(
                200,
                {
                    "commentlist1": [
                        {
                            "id": com["id"],
                            "user": com["user"]["name"],
                            "avatar": com["user"]["avatar"],
                            "content": com["content"],
                            "likes": com["like"],
                        }
                        for com in pho_com_list
                    ],
                    "commentlist2": [
                        {
                            "id": com["id"],
                            "user": com["user"]["name"],
                            "avatar": com["user"]["avatar"],
                            "content": com["content"],
                            "likes": com["like"],
                        }
                        for com in gal_com_list
                    ],
                },
            )
        except Exception as e:
            return gen_response(200, {"status": "request_error", "detail": "请求失败", })
    else:
        return gen_response(
            200, {"status": "method_error", "detail": "非法请求方法%s" % request.method, }
        )
