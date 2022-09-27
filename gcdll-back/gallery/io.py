from functools import wraps
import django
from django.db import OperationalError, transaction
from gallery.comment_check import is_legal
from .models import *
import time
import base64
import os
from django.contrib.auth.models import User as User_django
from django.contrib.auth.models import Permission
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q, F

# import datetime
from django.utils import timezone
from copy import copy
from .exceptions import logger

base_url = "http://gcdll-back-gcdll.app.secoder.net"
# base_url = ''

# 最大数据库队列时间
Tmax = 600
MAX_QUEUE_LENGTH = 2


# 数据库访问装饰器，请在每个访问数据库的函数前修饰
# 访问前加锁，如果访问失败（代表其他线程在访问）则循环等待直到最大时长
def db_oper_deco(f):
    @wraps(f)
    def ret_f(*args, **kwargs):
        s = time.time()
        while True:
            try:
                with transaction.atomic():
                    return f(*args, **kwargs)
            except OperationalError as e:
                if time.time() - s > Tmax:
                    logger.error("attemp time out")
                    return None
                if str(e) != "database is locked":
                    logger.error(e)
                    raise e

    return ret_f


def from_objects_to_list(a):
    return [copy(x.__dict__) for x in a]


def from_tag_to_dict(tag):
    return {"tag": tag.tag}


def from_comment_to_dict(comment):
    comment_dict = copy(comment.__dict__)
    user_dict = copy(comment.user.__dict__)
    user_dict["avatar"] = base_url + "/static" + comment.user.avatar.url
    comment_dict["user"] = user_dict
    comment_dict["user"].pop("_state")
    comment_dict.pop("_state")
    comment_dict["like_user"] = list(map(lambda x: x.id, comment.like_user.all()))
    comment_dict["pub_date"] = int(comment_dict["pub_date"].timestamp())
    return comment_dict


@db_oper_deco
def from_photo_to_dict(photo):
    if photo.group_id == 95434:
        photo.group_id = photo.id
        photo.save()
    old_photo = Photo.objects.filter(group_id=photo.group_id)
    if old_photo.count() == 0:
        old_photo = photo
        photo.group_id = photo.id
        photo.save()
    else:
        old_photo = old_photo[old_photo.count() - 1]
    photo_dict = copy(photo.__dict__)
    # if "static" in old_photo.photo.url:
    #     photo_dict["old_photo"] = base_url + old_photo.photo.url
    # else:
    photo_dict["old_photo"] = base_url + "/static" + old_photo.photo.url
    user = photo.user
    photo_dict["user"] = copy(user.__dict__)
    photo_dict["user"].pop("_state")
    photo_comment = photo.photo_comment_set.all()
    photo_dict["photo_comment"] = list(
        map(lambda x: from_comment_to_dict(x), photo_comment)
    )
    # if "static" in photo.photo.url:
    #     photo_dict["photo"] = base_url + photo.photo.url
    # else:
    photo_dict["photo"] = base_url + "/static" + photo.photo.url
    photo_dict.pop("_state")
    photo_dict["pub_date"] = int(photo.pub_date.timestamp())
    photo_dict["like_user"] = list(map(lambda x: x.id, photo.like_user.all()))
    photo_dict["tag"] = list(map(lambda x: from_tag_to_dict(x), photo.tag.all()))
    return photo_dict


def from_gallery_to_dict(gallery):
    gallery_dict = copy(gallery.__dict__)
    gallery_comment = gallery.gallery_comment_set.all()
    gallery_dict["gallery_comment"] = list(
        map(lambda x: from_comment_to_dict(x), gallery_comment)
    )
    photos = gallery.photo_set.all().order_by("order")
    gallery_dict["photo"] = [from_photo_to_dict(x) for x in photos]
    gallery_dict["cover"] = base_url + "/static" + gallery.cover.url
    gallery_dict["pub_date"] = int(gallery.pub_date.timestamp())
    gallery_dict.pop("_state")
    gallery_dict["like_user"] = list(map(lambda x: x.id, gallery.like_user.all()))
    gallery_dict["tag"] = list(map(lambda x: from_tag_to_dict(x), gallery.tag.all()))
    user = gallery.user
    gallery_dict["user"] = copy(user.__dict__)
    gallery_dict["user"].pop("_state")
    return gallery_dict


def from_user_to_dict(user):
    user_dict = copy(user.__dict__)
    # user_dict["avatar"] = base_url + "/static" + user.avatar.url
    user_dict["photo"] = list(
        map(lambda x: from_photo_to_dict(x), user.photo_set.all())
    )
    user_dict["password"] = user.django_user.password
    user_dict["avatar"] = base_url + "/static" + user.avatar.url
    user_dict["register_date"] = int(user_dict["register_date"].timestamp())
    user_dict.pop("_state")
    return user_dict


@db_oper_deco
def get_all_galleries():
    """
        获取全部展览
        返回一个list的dictionary
    """
    return [from_gallery_to_dict(x) for x in Gallery.objects.all()]


@db_oper_deco
def get_all_photos():
    """
        获取全部图片
        返回一个list的dictionary
    """
    return [from_photo_to_dict(x) for x in Photo.objects.all()]


@db_oper_deco
def get_user(id):
    """
        获取用户
        返回一个dictionary的user
        返回一个list的dictionary的photo
    """
    try:
        user = User.objects.filter(id=id)[0]
        return from_user_to_dict(user)

    except Exception:
        return {}


@db_oper_deco
def get_user_by_name(name):
    """
        获取用户
        返回一个dictionary的user
        返回一个list的dictionary的photo
    """
    user = User.objects.filter(name=name)[0]
    return from_user_to_dict(user)


@db_oper_deco
def get_gallery(id):
    """
        获取id = id的展览
        返回一个dictionary的gallery
    """
    try:
        gallery = Gallery.objects.filter(id=id)[0]
        return from_gallery_to_dict(gallery)

    except Exception:
        return {}


@db_oper_deco
def like_gallery(user_id, gallery_id, type):
    """
        user_id = user_id的用户点赞gallery_id = gallery_id的展览
        其中type=0为点赞，type=1为取消点赞
    """
    try:
        user = User.objects.filter(id=user_id)[0]
        gallery = Gallery.objects.filter(id=gallery_id)[0]
        if type == 0:
            assert not gallery.like_user.contains(user)
            gallery.like_user.add(user)
            gallery.like += 1
            gallery.save()
        elif type == 1:
            assert gallery.like_user.contains(user)
            gallery.like_user.remove(user)
            gallery.like -= 1
            gallery.save()
        else:
            raise

    except Exception:
        raise


@db_oper_deco
def comment_gallery(user_id, gallery_id, content=""):
    """
        user_id = user_id的用户评论gallery_id = gallery_id的展览
    """
    try:
        user = User.objects.filter(id=user_id)[0]
        gallery = Gallery.objects.filter(id=gallery_id)[0]
        while True:
            if push_queue("check"):
                is_banned, banned_reason = is_legal(content)
                time.sleep(1 / MAX_QUEUE_LENGTH)
                pop_queue("check")
                break
        is_banned = not is_banned
        Gallery_Comment.objects.create(
            user=user, gallery=gallery, content=content, is_banned=is_banned
        )
        user.cmt_cnt = user.gallery_comment_set.count() + user.photo_comment_set.count()
        gallery.cmt_cnt = gallery.gallery_comment_set.count()
        gallery.save()
        user.save()
        return is_banned, banned_reason

    except Exception:
        return True, "Error"


@db_oper_deco
def get_photo(id):
    """
        获取id = id的图片
        返回一个dictionary的photo
        返回一个list的dictionary的photo_comment

    """
    try:
        photo = Photo.objects.filter(id=id)[0]
        return from_photo_to_dict(photo)

    except Exception:
        return {}


@db_oper_deco
def like_photo(user_id, photo_id, type):
    """
        user_id = user_id的用户点赞/取消点赞photo_id = photo_id的图片
        其中type=0为点赞，type=1为取消点赞
    """
    try:
        photo = Photo.objects.filter(id=photo_id)[0]
        user = User.objects.filter(id=user_id)[0]
        if type == 0:
            assert not photo.like_user.contains(user)
            photo.like_user.add(user)
            photo.like += 1
            photo.save()
        elif type == 1:
            assert photo.like_user.contains(user)
            photo.like_user.remove(user)
            photo.like -= 1
            photo.save()
        else:
            raise

    except Exception:
        raise


@db_oper_deco
def comment_photo(user_id, photo_id, content=""):
    """
        user_id = user_id的用户评论photo_id = photo_id的图片
    """
    try:
        photo = Photo.objects.filter(id=photo_id)[0]
        user = User.objects.filter(id=user_id)[0]
        is_banned, banned_reason = is_legal(content)
        is_banned = not is_banned
        comment = Photo_Comment.objects.create(
            user=user, photo=photo, content=content, is_banned=is_banned,
        )
        user.cmt_cnt = user.photo_comment_set.count() + user.gallery_comment_set.count()
        photo.cmt_cnt = photo.photo_comment_set.count()
        photo.save()
        user.save()
        return is_banned, banned_reason, from_comment_to_dict(comment)

    except Exception:
        return True, "Error"


@db_oper_deco
def get_comment(id, type, order, start):
    """
        获取评论
        type == 1为图片评�? type == 0为展览评�?
        order == 1为按照时间降�? order == 0为按照热度（点赞）降�?
        获取区间范围为[start*10,(start + 1)*10)
        返回一个list的dictionary的comment
    """
    try:
        if type == 1:
            photo = Photo.objects.filter(id=id)[0]
            photo_comment = photo.photo_comment_set.all()
            if order == 1:
                photo_comment = photo_comment.order_by("-pub_date")
            else:
                photo_comment = photo_comment.order_by("-like")
            return list(
                map(
                    lambda x: from_comment_to_dict(x),
                    photo_comment[start * 10: (start + 1) * 10],
                )
            )
        elif type == 0:
            gallery = Gallery.objects.filter(id=id)[0]
            gallery_comment = gallery.gallery_comment_set.all()
            if order == 1:
                gallery_comment = gallery_comment.order_by("-pub_date")
            else:
                gallery_comment = gallery_comment.order_by("-like")
            return list(
                map(
                    lambda x: from_comment_to_dict(x),
                    gallery_comment[start * 10: (start + 1) * 10],
                )
            )
        else:
            return []

    except Exception:
        return []


@db_oper_deco
def create_gallery(title, intro, photolist, user_id, cover="./test_gallery.jpeg"):
    """
        用所给参数创建一个新的展览
        返回一个dictionary的gallery
    """
    try:
        user = User.objects.get(id=user_id)

    except Exception:
        return {}
    gallery = Gallery.objects.create(user=user, title=title, intro=intro, cover=cover)
    try:
        photo = Photo.objects.get(id=photolist[0])

    except Exception:
        return {}
    try:
        if photo.id == photo.group_id:
            with open("./static/photo/raw/{}.jpeg".format(photo.id), "rb") as f:
                img = f.read()
                with open(
                    "./static/cover/gallery_{}.jpeg".format(gallery.id), "wb"
                ) as ff:
                    ff.write(img)
            gallery.cover = "cover/gallery_{}.jpeg".format(gallery.id)
        else:
            with open("./static/photo/processed/{}.jpeg".format(photo.id), "rb") as f:
                img = f.read()
                with open(
                    "./static/cover/gallery_{}.jpeg".format(gallery.id), "wb"
                ) as ff:
                    ff.write(img)
            gallery.cover = "cover/gallery_{}.jpeg".format(gallery.id)

    except Exception:
        gallery.cover = "cover/test_cover.jpeg"
    gallery.save()
    for i, id in enumerate(photolist):
        try:
            photo = Photo.objects.get(id=id)

        except Exception:
            return {}
        photo.order = i
        photo.gallery.add(gallery)
        gallery.photo_set.add(photo)
        photo.save()
    return from_gallery_to_dict(gallery)


@db_oper_deco
def create_user(
    name, register_date, admin, password, avatar="./static/avatar/test_avatar.jpeg"
):
    """
        用所给参数创建一个新的用�?
        返回一个dictionary的user
    """
    django_user = User_django.objects.create_user(
        username=name, password=password, is_superuser=False, is_active=True,
    )
    user = User.objects.create(
        name=name,
        register_date=register_date,
        avatar=avatar,
        admin=admin,
        django_user=django_user,
    )
    permission1 = Permission.objects.get(codename="is_admin")
    permission2 = Permission.objects.get(codename="post_comments")
    permission3 = Permission.objects.get(codename="is_alive")
    if user.admin:
        user.django_user.user_permissions.add(permission1)
        user.django_user.user_permissions.add(permission3)
        user.save()
    else:
        user.django_user.user_permissions.add(permission2)
        user.django_user.user_permissions.add(permission3)
        user.save()
    return from_user_to_dict(user)


@db_oper_deco
def user_logout(id):
    """
        查找id=id的用户并将其设置为下线
    """
    try:
        user = User.objects.filter(id=id).first()
        user.django_user.is_active = False

    except Exception:
        raise


@db_oper_deco
def request_user_authenticated(request):
    user = request.user
    return user.is_authenticated


@db_oper_deco
def request_user_id(request):
    user = request.user
    return user.user.id


@db_oper_deco
def change_password(id, old_password, new_password):
    """
        更改id=id用户的密码
    """
    try:
        user = User.objects.get(id=id)

    except Exception:
        return {}
    # if old_password == user.django_user.password:
    #     user.django_user.password = new_password
    # else:
    #     return AssertionError
    if check_password(old_password, user.django_user.password):
        user.django_user.password = make_password(new_password)
        user.django_user.save()
        user.save()
        return from_user_to_dict(user)
    else:
        raise AssertionError


@db_oper_deco
def create_photo_base64(img_base64, user_id, pub_date, year=2022):
    slice = 0
    for s in img_base64:
        slice += 1
        if s == ",":
            break
    if slice > 50:
        slice = 0
    img = base64.b64decode(img_base64[slice:])
    try:
        user = User.objects.get(id=user_id)

    except Exception:
        return {}
    photo = Photo.objects.create(user=user, pub_date=pub_date, year=year)
    try:
        f = open("./static/photo/raw/{}.jpeg".format(photo.id), "wb")
        f.write(img)
        f.close()
        photo.photo = "photo/raw/{}.jpeg".format(photo.id)

    except Exception:
        photo.photo = "photo/raw/test_photo.jpeg"
    # print('created photo', photo.id)
    logger.info("created photo{}".format(photo.id))
    photo.group_id = photo.id
    photo.save()
    return from_photo_to_dict(photo)


@db_oper_deco
def search_gallery(title):
    """
        通过名字搜索展览
        返回一个dictionary的gallery
    """
    galleries = Gallery.objects.filter(title__contains=title)
    return [from_gallery_to_dict(x) for x in galleries]


@db_oper_deco
def change_photo_title(id, title):
    """
        通过id改变图片标题
        返回一个dictionary的gallery
    """
    try:
        photo = Photo.objects.filter(id=id).first()
        photo.title = title
        photo.save()

    except Exception:
        raise


@db_oper_deco
def change_photo_pubdate_now(id):
    """
        通过id改变图片发布日期(设为现在)
    """
    photo = Photo.objects.filter(id=id).first()
    photo.pub_date = timezone.now()
    photo.save()


@db_oper_deco
def change_photo_info(id, info):
    """
        通过id改变图片简�?
    """
    try:
        photo = Photo.objects.filter(id=id).first()
        photo.info = info
        photo.save()

    except Exception:
        raise


@db_oper_deco
def get_photo_by_group_id(group_id):
    photo = Photo.objects.filter(group_id=group_id)
    return [from_photo_to_dict(x) for x in photo]


@db_oper_deco
def get_all_users(order=None):
    if order is None:
        return map(lambda x: from_user_to_dict(x), User.objects.all())
    elif order == "report_cnt":
        users = User.objects.all()
        users = users.order_by("-report_cmt_cnt")
        return map(lambda x: from_user_to_dict(x), users)
    elif order == "cmt_cnt":
        users = User.objects.all()
        users = users.order_by("-cmt_cnt")
        return map(lambda x: from_user_to_dict(x), users)


@db_oper_deco
def user_login(request, username, password):
    user = User.objects.get(name=username)
    django_user = user.django_user
    if check_password(password, django_user.password):
        # if password == django_user.password:
        auth.login(request, django_user)
        return True
    else:
        return False


@db_oper_deco
def user_logout(request):
    auth.logout(request)


@db_oper_deco
def order_set(order_name, order_method, query_set):
    if order_name == "time":
        order = "pub_date"
        if order_method is False:
            order = "-" + order
        return query_set.order_by(order)
    if order_name == "comment":
        order = "cmt_cnt"
        if order_method is False:
            order = "-" + order
        return query_set.order_by(order)
    if order_name == "like":
        order = "like"
        if order_method is False:
            order = "-" + order
        return query_set.order_by(order)
    if order_name == "comment_report":
        order = "report_cnt"
        if order_method is False:
            order = "-" + order
        return query_set.order_by(order)
    if order_name == "user_report":
        order = "user__report_cmt_cnt"
        if order_method is False:
            order = "-" + order
        return query_set.order_by(order)


@db_oper_deco
def gallery_advanced_search(
    filters, page_num, amount, order_name=None, order_method=None
):
    try:
        galleries = Gallery.objects.all()
        for filter in filters:
            if filter.get("min_id") is not None:
                min_id = int(filter.get("min_id"))
                max_id = int(filter.get("max_id"))
                galleries = galleries.filter(Q(id__gte=min_id) & Q(id__lte=max_id))
            elif filter.get("min_timestamp") is not None:
                min_time = filter.get("min_timestamp")
                max_time = filter.get("max_timestamp")
                min_time /= 1000
                max_time /= 1000
                min_time = time.localtime(min_time)
                max_time = time.localtime(max_time)
                min_time = time.strftime("%Y-%m-%d %H:%M:%S", min_time)
                max_time = time.strftime("%Y-%m-%d %H:%M:%S", max_time)
                galleries = galleries.filter(
                    Q(pub_date__gte=min_time) & Q(pub_date__lte=max_time)
                )
            elif filter.get("tag") is not None or \
                filter.get("title") is not None or \
                    filter.get("introduction") is not None:
                galleries_tag = (
                    galleries_title
                ) = galleries_intro = Gallery.objects.filter(id=-1)
                if filter.get("tag") is not None:
                    galleries_tag = galleries
                    for tag in filter.get("tag"):
                        galleries_tag = galleries_tag.filter(tag__tag__contains=tag)
                if filter.get("title") is not None:
                    galleries_title = galleries
                    for title in filter.get("title"):
                        galleries_title = galleries_title.filter(title__contains=title)
                if filter.get("introduction") is not None:
                    for intro in filter.get("introduction"):
                        galleries_intro = galleries_intro.filter(intro__contains=intro)
                gallery = galleries_tag | galleries_title | galleries_intro
                if filter.get("negative") is True:
                    galleries = galleries.exclude(pk__in=gallery)
                else:
                    galleries = galleries & gallery
        galleries = galleries.distinct()
        total_num = galleries.count()
        try:
            galleries = order_set(order_name, order_method, galleries)
            galleries = Paginator(galleries, amount)
            return (
                total_num,
                list(map(from_gallery_to_dict, galleries.page(page_num).object_list)),
            )

        except Exception:
            return 0, []

    except Exception:
        return 0, []


@db_oper_deco
def photo_advanced_search(
    filters, amount, page_num, order_name=None, order_method=None, unique=True
):
    try:
        photos = (
            Photo.objects.filter(id=F("group_id")) if unique else Photo.objects.all()
        )
        gallery_id = None
        for filter in filters:
            if filter.get("exhibit_id"):
                gallery_id = int(filter.get("exhibit_id"))
        if gallery_id is not None:
            try:
                gallery = Gallery.objects.get(id=gallery_id)

            except Exception:
                return 0, []
            photos = gallery.photo_set.all()
        for filter in filters:
            if filter.get("min_id") is not None:
                min_id = int(filter.get("min_id"))
                max_id = int(filter.get("max_id"))
                photos = photos.filter(Q(id__gte=min_id) & Q(id__lte=max_id))
            elif filter.get("min_timestamp") is not None:
                min_time = filter.get("min_timestamp")
                max_time = filter.get("max_timestamp")
                min_time /= 1000
                max_time /= 1000
                min_time = time.localtime(min_time)
                max_time = time.localtime(max_time)
                min_time = time.strftime("%Y-%m-%d %H:%M:%S", min_time)
                max_time = time.strftime("%Y-%m-%d %H:%M:%S", max_time)
                photos = photos.filter(
                    Q(pub_date__gte=min_time) & Q(pub_date__lte=max_time)
                )
            elif filter.get("tag") or filter.get("title") or filter.get("introduction"):
                photos_tag = photos_title = photos_info = Photo.objects.filter(id=-1)
                if filter.get("tag") is not None:
                    photos_tag = photos
                    for tag in filter.get("tag"):
                        photos_tag = photos_tag.filter(tag__tag__contains=tag)
                if filter.get("title") is not None:
                    photos_title = photos
                    for title in filter.get("title"):
                        photos_title = photos_title.filter(title__contains=title)
                if filter.get("introduction") is not None:
                    photos_info = photos
                    for info in filter.get("introduction"):
                        photos_info = photos_info.filter(info__contains=info)
                photo = photos_tag | photos_title | photos_info
                if filter.get("negative") is True:
                    photos = photos.exclude(pk__in=photo)
                else:
                    photos = photos & photo
        photos = photos.distinct()
        total_num = photos.count()
        try:
            photos = order_set(order_name, order_method, photos)
            photos = Paginator(photos, amount)
            return (
                total_num,
                list(map(from_photo_to_dict, photos.page(page_num).object_list)),
            )

        except Exception:
            return 0, []

    except Exception:
        return 0, []


@db_oper_deco
def photo_comment_advanced_search(
    filters, amount, page_num, order_name=None, order_method=None
):
    try:
        pho_cmts = Photo_Comment.objects.all()
        for filter in filters:
            if filter.get("min_id") is not None:
                min_id = int(filter.get("min_id"))
                max_id = int(filter.get("max_id"))
                pho_cmts = pho_cmts.filter(Q(id__gte=min_id) & Q(id__lte=max_id))
            elif filter.get("min_timestamp") is not None:
                min_time = filter.get("min_timestamp")
                max_time = filter.get("max_timestamp")
                min_time /= 1000
                max_time /= 1000
                min_time = time.localtime(min_time)
                max_time = time.localtime(max_time)
                min_time = time.strftime("%Y-%m-%d %H:%M:%S", min_time)
                max_time = time.strftime("%Y-%m-%d %H:%M:%S", max_time)
                pho_cmts = pho_cmts.filter(
                    Q(pub_date__gte=min_time) & Q(pub_date__lte=max_time)
                )
            elif filter.get("username") is not None or\
                filter.get("content") is not None or\
                filter.get("info") is not None or\
                    filter.get("banned") is not None:
                pho_cmts_user = (
                    pho_cmts_content
                ) = pho_cmts_info = pho_cmts_banned = Photo_Comment.objects.filter(
                    id=-1
                )
                if filter.get("username") is not None:
                    pho_cmts_user = pho_cmts
                    for username in filter.get("username"):
                        pho_cmts_user = pho_cmts_user.filter(
                            user__name__contains=username
                        )
                if filter.get("content") is not None:
                    pho_cmts_content = pho_cmts
                    for content in filter.get("content"):
                        pho_cmts_content = pho_cmts_content.filter(
                            content__contains=content
                        )
                if filter.get("info") is not None:
                    pho_cmts_info = pho_cmts
                    for info in filter.get("info"):
                        pho_cmts_info = pho_cmts_info.filter(
                            photo__title__contains=info
                        )
                if filter.get("banned") is not None:
                    pho_cmts_banned = pho_cmts
                    banned = filter.get("banned")
                    if banned == "unbanned":
                        pho_cmts_banned = pho_cmts_banned.filter(is_banned=False)
                    elif banned == "banned":
                        pho_cmts_banned = pho_cmts_banned.filter(is_banned=True)
                pho_cmt = (
                    pho_cmts_user | pho_cmts_content | pho_cmts_info | pho_cmts_banned
                )
                pho_cmts = pho_cmts & pho_cmt
        total_num = pho_cmts.count()
        pho_cmts.distinct()
        try:
            pho_cmts = order_set(order_name, order_method, pho_cmts)
            pho_cmts = Paginator(pho_cmts, amount)
            return (
                total_num,
                list(map(from_comment_to_dict, pho_cmts.page(page_num).object_list)),
            )

        except Exception:
            return 0, []

    except Exception:
        return 0, []


@db_oper_deco
def gallery_comment_advanced_search(
    filters, amount, page_num, order_name=None, order_method=None
):
    try:
        gal_cmts = Gallery_Comment.objects.all()
        for filter in filters:
            if filter.get("min_id") is not None:
                min_id = int(filter.get("min_id"))
                max_id = int(filter.get("max_id"))
                gal_cmts = gal_cmts.filter(Q(id__gte=min_id) & Q(id__lte=max_id))
            elif filter.get("min_timestamp") is not None:
                min_time = filter.get("min_timestamp")
                max_time = filter.get("max_timestamp")
                min_time /= 1000
                max_time /= 1000
                min_time = time.localtime(min_time)
                max_time = time.localtime(max_time)
                min_time = time.strftime("%Y-%m-%d %H:%M:%S", min_time)
                max_time = time.strftime("%Y-%m-%d %H:%M:%S", max_time)
                gal_cmts = gal_cmts.filter(
                    Q(pub_date__gte=min_time) & Q(pub_date__lte=max_time)
                )
            elif filter.get("username") is not None or\
                filter.get("content") is not None or\
                filter.get("info") is not None or\
                    filter.get("banned") is not None:
                gal_cmts_user = (
                    gal_cmts_content
                ) = gal_cmts_info = gal_cmts_banned = Gallery_Comment.objects.filter(
                    id=-1
                )
                if filter.get("username") is not None:
                    gal_cmts_user = gal_cmts
                    for name in filter.get("username"):
                        gal_cmts_user = gal_cmts_user.filter(user__name__contains=name)
                if filter.get("content") is not None:
                    gal_cmts_content = gal_cmts
                    for content in filter.get("content"):
                        gal_cmts_content = gal_cmts_content.filter(
                            content__contains=content
                        )
                if filter.get("info") is not None:
                    gal_cmts_info = gal_cmts
                    for info in filter.get("info"):
                        gal_cmts_info = gal_cmts_info.filter(
                            gallery__title__contains=info
                        )

                if filter.get("banned") is not None:
                    gal_cmts_banned = gal_cmts
                    banned = filter.get("banned")
                    if banned == "unbanned":
                        gal_cmts_banned = gal_cmts_banned.filter(is_banned=False)
                    elif banned == "banned":
                        gal_cmts_banned = gal_cmts_banned.filter(is_banned=True)

                gal_cmt = (
                    gal_cmts_user | gal_cmts_content | gal_cmts_info | gal_cmts_banned
                )
                gal_cmts = gal_cmts & gal_cmt
        total_num = gal_cmts.count()
        gal_cmts.distinct()
        try:
            gal_cmts = order_set(order_name, order_method, gal_cmts)
            gal_cmts = Paginator(gal_cmts, amount)
            return (
                total_num,
                list(map(from_comment_to_dict, gal_cmts.page(page_num).object_list)),
            )

        except Exception:
            return 0, []

    except Exception:
        return 0, []


@db_oper_deco
def user_advanced_search(
    group, filters, page_num, amount, order_name=None, order_method=None
):
    try:
        users = User.objects.filter(admin=False)
        if group == "visited":
            users = users.filter(
                Q(django_user__user_permissions__codename="post_comments")
            )
        elif group == "banned":
            user = users.filter(
                Q(django_user__user_permissions__codename="post_comments")
            )
            users = users.exclude(pk__in=user)
            users = users.filter(Q(django_user__user_permissions__codename="is_alive"))
        elif group == "deleted":
            user = users.filter(Q(django_user__user_permissions__codename="is_alive"))
            users = users.exclude(pk__in=user)
        for filter in filters:
            if filter.get("min_id") is not None:
                min_id = int(filter.get("min_id"))
                max_id = int(filter.get("max_id"))
                users = users.filter(Q(id__gte=min_id) & Q(id__lte=max_id))
            elif filter.get("min_timestamp") is not None:
                min_time = filter.get("min_timestamp")
                max_time = filter.get("max_timestamp")
                min_time /= 1000
                max_time /= 1000
                min_time = time.localtime(min_time)
                max_time = time.localtime(max_time)
                min_time = time.strftime("%Y-%m-%d %H:%M:%S", min_time)
                max_time = time.strftime("%Y-%m-%d %H:%M:%S", max_time)
                users = users.filter(
                    Q(register_date__gte=min_time) & Q(register_date__lte=max_time)
                )
            elif filter.get("name") is not None:
                users_name = User.objects.filter(id=-1)
                if filter.get("name") is not None:
                    users_name = users
                    for name in filter.get("name"):
                        users_name = users_name.filter(name__contains=name)
                if filter.get("negative") is True:
                    users = users.exclude(pk__in=users_name)
                else:
                    users = users & users_name
        users = users.distinct()
        total_num = users.count()
        try:
            if order_name == "time":
                order = "register_date"
                if not order_method:
                    order = "-" + order
                users = users.order_by(order)
            elif order_name == "comment_cnt":
                order = "cmt_cnt"
                if not order_method:
                    order = "-" + order
                users = users.order_by(order)
            elif order_name == "reported_cnt":
                order = "report_cmt_cnt"
                if not order_method:
                    order = "-" + order
                users = users.order_by(order)
            users = Paginator(users, amount)
            return (
                total_num,
                list(map(from_user_to_dict, users.page(page_num).object_list)),
            )

        except Exception:
            return 0, []

    except Exception:
        return 0, []


@db_oper_deco
def delete_comment(type, comment_id):
    """
        type = 0 photo
        type = 1 gallery
    """
    if type == 0:
        try:
            comment = Photo_Comment.objects.get(id=comment_id)

        except Exception:
            raise
        comment.delete()
    else:
        if type == 1:
            try:
                comment = Gallery_Comment.objects.get(id=comment_id)

            except Exception:
                raise
            comment.delete()
        else:
            raise


@db_oper_deco
def revive_comment(type, comment_id):
    """
        type = 0 photo
        type = 1 gallery
    """
    if type == 0:
        try:
            comment = Photo_Comment.objects.get(id=comment_id)

        except Exception:
            raise
        comment.is_banned = False
        comment.save()
    else:
        if type == 1:
            try:
                comment = Gallery_Comment.objects.get(id=comment_id)

            except Exception:
                raise
            comment.is_banned = False
            comment.save()
        else:
            raise


@db_oper_deco
def forbid_comment(type, comment_id):
    """
        type = 0 photo
        type = 1 gallery
    """
    if type == 0:
        try:
            comment = Photo_Comment.objects.get(id=comment_id)

        except Exception:
            raise
        comment.is_banned = True
        comment.save()
    else:
        if type == 1:
            try:
                comment = Gallery_Comment.objects.get(id=comment_id)

            except Exception:
                raise
            comment.is_banned = True
            comment.save()
        else:
            raise


@db_oper_deco
def like_comment(type, comment_id, user_id):
    """
        type = 0 photo + 1
        type = 1 gallery + 1
        type = 2 photo - 1
        type = 3 photo - 1
    """
    try:
        user = User.objects.get(id=user_id)
        if type == 0:
            comment = Photo_Comment.objects.get(id=comment_id)
            assert not comment.like_user.contains(user)
            comment.like_user.add(user)
            comment.like += 1
            comment.save()
        elif type == 1:
            comment = Gallery_Comment.objects.get(id=comment_id)
            assert not comment.like_user.contains(user)
            comment.like_user.add(user)
            comment.like += 1
            comment.save()
        elif type == 2:
            comment = Photo_Comment.objects.get(id=comment_id)
            assert comment.like_user.contains(user)
            comment.like_user.remove(user)
            comment.like -= 1
            comment.save()
        elif type == 3:
            comment = Gallery_Comment.objects.get(id=comment_id)
            assert comment.like_user.contains(user)
            comment.like_user.remove(user)
            comment.like -= 1
            comment.save()

    except Exception:
        raise


@db_oper_deco
def report_comment(type, comment_id, user_id):
    """
        type = 0 photo + 1
        type = 1 gallery + 1
        type = 2 photo - 1
        type = 3 photo - 1
    """
    try:
        user = User.objects.get(id=user_id)
        if type == 0:
            comment = Photo_Comment.objects.get(id=comment_id)
            comment.report_user.add(user)
            comment.report_cnt += 1
            comment.save()
        elif type == 1:
            comment = Gallery_Comment.objects.get(id=comment_id)
            comment.report_user.add(user)
            comment.report_cnt += 1
            comment.save()
        elif type == 2:
            comment = Photo_Comment.objects.get(id=comment_id)
            assert comment.report_user.contains(user)
            comment.report_user.remove(user)
            comment.report_cnt -= 1
            comment.save()
        elif type == 3:
            comment = Gallery_Comment.objects.get(id=comment_id)
            assert comment.report_user.contains(user)
            comment.report_user.remove(user)
            comment.report_cnt -= 1
            comment.save()

    except Exception:
        raise


@db_oper_deco
def ban_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        permission = Permission.objects.get(codename="post_comments")
        if user.django_user.has_perm("gallery.post_comments"):
            user.django_user.user_permissions.remove(permission)
            user.save()

    except Exception:
        raise


@db_oper_deco
def is_admin(id):
    try:
        user = User.objects.get(id=id)
        return user.django_user.has_perm("gallery.is_admin")

    except Exception:
        return False


@db_oper_deco
def user_is_banned(id):
    try:
        user = User.objects.get(id=id)
        return (not user.django_user.has_perm("gallery.post_comments")) and (
            user.django_user.has_perm("gallery.is_alive")
        )

    except Exception:
        raise


@db_oper_deco
def photo_remove_tags(photo_id, tags_list):
    try:
        photo = Photo.objects.get(id=photo_id)
        for tag in tags_list:
            tag_list = Tag.objects.filter(tag=tag)
            if tag_list.count() != 0:
                photo.tag.remove(tag_list[0])
        photo.save()

    except Exception:
        raise


@db_oper_deco
def photo_add_tags(photo_id, tags_list, fixed=False):
    try:
        photo = Photo.objects.get(id=photo_id)
        for tag1 in tags_list:
            tag_list = Tag.objects.filter(tag=tag1)
            if tag_list.count() > 0:
                tag = tag_list[0]
            else:
                tag = Tag.objects.create(tag=tag1, fixed=fixed)
            photo.tag.add(tag)
        photo.save()

    except Exception:
        raise


@db_oper_deco
def photo_change_tags(photo_id, tags_list):
    try:
        photo = Photo.objects.get(id=photo_id)
        for tag in photo.tag.filter(fixed=False):
            photo.tag.remove(tag)
        for tag in tags_list:
            tag_list = Tag.objects.filter(tag=tag)
            if tag_list.count() > 0:
                tag_list = tag_list[0]
            else:
                tag_list = Tag.objects.create(tag=tag)
            photo.tag.add(tag_list)
        photo.save()

    except Exception:
        raise


@db_oper_deco
def photo_set_all(photo_id, photo_dict):
    try:
        photo = Photo.objects.get(id=photo_id)
    except Photo.DoesNotExist:
        return False
    if "user" in photo_dict:
        user = User.objects.get(id=photo_dict["user"])
        photo.user = user
    if "pub_date" in photo_dict:
        photo.pub_date = photo_dict["pub_date"]
    if "title" in photo_dict:
        photo.title = photo_dict["title"]
    if "info" in photo_dict:
        photo.info = photo_dict["info"]
    if "photo" in photo_dict:
        photo.photo = photo_dict["photo"]
    if "operation" in photo_dict:
        photo.operation = photo_dict["operation"]
    photo.save()
    return True


@db_oper_deco
def gallery_change_tags(gallery_id, tags_list):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        for tag in gallery.tag.all():
            gallery.tag.remove(tag)
        for tag in tags_list:
            tag_list = Tag.objects.filter(tag=tag)
            if tag_list.count() > 0:
                tag_list = tag_list[0]
            else:
                tag_list = Tag.objects.create(tag=tag)
            gallery.tag.add(tag_list)
        gallery.save()

    except Exception:
        raise


@db_oper_deco
def delete_photo(photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)
        if photo.group_id == photo.id:
            photo_group = get_photo_by_group_id(photo.group_id)
            for photo1 in photo_group:
                group_photo = Photo.objects.get(id=photo1["id"])
                try:
                    if "raw" in photo1["photo"]:
                        os.remove("./static/photo/raw/{}.jpeg".format(photo1["id"]))
                    else:
                        os.remove(
                            "./static/photo/processed/{}.jpeg".format(photo1["id"])
                        )
                except FileNotFoundError:
                    pass
                group_photo.delete()
        else:
            photo_dict = get_photo(photo.id)
            try:
                if "raw" in photo_dict["photo"]:
                    os.remove("./static/photo/raw/{}.jpeg".format(photo_dict["id"]))
                else:
                    os.remove(
                        "./static/photo/processed/{}.jpeg".format(photo_dict["id"])
                    )
            except Exception:
                pass
            photo.delete()

    except Exception:
        raise


@db_oper_deco
def delete_gallery(gallery_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        gallery.delete()

    except Exception:
        raise


@db_oper_deco
def set_group_id(photo_id, group_id):
    try:
        photo = Photo.objects.get(id=photo_id)
        photo.group_id = group_id
        photo.save()

    except Exception:
        raise


@db_oper_deco
def remove_photo_from_gallery(gallery_id, photo_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        photo = Photo.objects.get(id=photo_id)
        photo.gallery.remove(gallery)
        photo.save()
        gallery.photo_set.remove(photo)
        gallery.save()

    except Exception:
        raise


@db_oper_deco
def gallery_remove_tags(gallery_id, tags_list):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        for tag in tags_list:
            tag_list = Tag.objects.filter(tag=tag)[0]
            gallery.tag.remove(tag_list)
        gallery.save()

    except Exception:
        raise


@db_oper_deco
def gallery_add_tags(gallery_id, tags_list):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        for tag1 in tags_list:
            tag_list = Tag.objects.filter(tag=tag1)
            if tag_list.count() > 0:
                tag_list = tag_list[0]
            else:
                tag_list = Tag.objects.create(tag=tag1)
            gallery.tag.add(tag_list)
        gallery.save()

    except Exception:
        raise


@db_oper_deco
def gallery_add_photo(gallery_id, photo_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        photo = Photo.objects.get(id=photo_id)
        gallery.photo_set.add(photo)
        photo.gallery.add(gallery)
        gallery.save()
        photo.save()

    except Exception:
        raise


@db_oper_deco
def gallery_remove_photo(gallery_id, photo_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        photo = Photo.objects.get(id=photo_id)
        gallery.photo_set.remove(photo)
        photo.gallery.remove(gallery)
        gallery.save()
        photo.save()

    except Exception:
        raise


@db_oper_deco
def change_gallery_title(gallery_id, title):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        gallery.title = title
        gallery.save()

    except Exception:
        raise


@db_oper_deco
def change_gallery_intro(gallery_id, intro):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        gallery.intro = intro
        gallery.save()

    except Exception:
        raise


@db_oper_deco
def kill_user(id):
    try:
        user = User.objects.get(id=id)
        permission = Permission.objects.get(codename="is_alive")
        permission1 = Permission.objects.get(codename="post_comments")
        if user.django_user.has_perm("gallery.is_alive"):
            user.django_user.user_permissions.remove(permission)
            user.django_user.user_permissions.remove(permission1)
            user.save()

    except Exception:
        raise


@db_oper_deco
def is_killed(id):
    try:
        user = User.objects.get(id=id)
        return not user.django_user.has_perm("gallery.is_alive")

    except Exception:
        return True


@db_oper_deco
def unban_user(id):
    try:
        user = User.objects.get(id=id)
        permission = Permission.objects.get(codename="post_comments")
        if not user.django_user.has_perm("gallery.post_comments"):
            user.django_user.user_permissions.add(permission)
            user.save()

    except Exception:
        raise


@db_oper_deco
def revive_user(id):
    try:
        user = User.objects.get(id=id)
        permission = Permission.objects.get(codename="is_alive")
        if not user.django_user.has_perm("gallery.is_alive"):
            user.django_user.user_permissions.add(permission)
            user.save()

    except Exception:
        raise


@db_oper_deco
def photo_liked(user_id, photo_id):
    try:
        photo = Photo.objects.get(id=photo_id)

    except Exception:
        return False
    try:
        user = photo.like_user.get(id=user_id)
        return True
    except Exception:
        return False


@db_oper_deco
def gallery_liked(user_id, gallery_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)

    except Exception:
        return False
    try:
        user = gallery.like_user.get(id=user_id)
        return True
    except Exception:
        return False


@db_oper_deco
def photo_comment_liked(user_id, comment_id):
    try:
        photo_comment = Photo_Comment.objects.get(id=comment_id)

    except Exception:
        return False
    try:
        user = photo_comment.like_user.get(id=user_id)
        return True
    except Exception:
        return False


@db_oper_deco
def photo_comment_reported(user_id, comment_id):
    try:
        photo_comment = Photo_Comment.objects.get(id=comment_id)

    except Exception:
        return False
    try:
        user = photo_comment.report_user.get(id=user_id)
        return True

    except Exception:
        return False


@db_oper_deco
def gallery_comment_liked(user_id, comment_id):
    try:
        gallery_comment = Gallery_Comment.objects.get(id=comment_id)

    except Exception:
        return False
    try:
        user = gallery_comment.like_user.get(id=user_id)
        return True
    except Exception:
        return False


@db_oper_deco
def gallery_comment_reported(user_id, comment_id):
    try:
        gallery_comment = Gallery_Comment.objects.get(id=comment_id)

    except Exception:
        return False
    try:
        user = gallery_comment.report_user.get(id=user_id)
        return True

    except Exception:
        return False


@db_oper_deco
def change_gallery_cover(gallery_id, img_base64, user_id, pub_date=None):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        slice = 0
        for s in img_base64:
            slice += 1
            if s == ",":
                break
        if slice > 50:
            slice = 0
        img = base64.b64decode(img_base64[slice:])
        try:
            with open("./static/cover/gallery_{}.jpeg".format(gallery.id), "wb") as f:
                f.write(img)

        except Exception:
            raise
        gallery.cover = "cover/gallery_{}.jpeg".format(gallery.id)
        gallery.save()
        return from_gallery_to_dict(gallery)

    except Exception:
        return {}


@db_oper_deco
def report_photo_comment(photo_comment_id):
    try:
        photo_comment = Photo_Comment.objects.get(id=photo_comment_id)
        photo_comment.report_cnt += 1
        photo_comment.save()
        user = photo_comment.user
        user.report_cmt_cnt += 1
        user.save()

    except Exception:
        raise


@db_oper_deco
def report_gallery_comment(gallery_comment_id):
    try:
        gallery_comment = Gallery_Comment.objects.get(id=gallery_comment_id)
        gallery_comment.report_cnt += 1
        gallery_comment.save()
        user = gallery_comment.user
        user.report_cmt_cnt += 1
        user.save()

    except Exception:
        raise


@db_oper_deco
def change_user_avatar(id, img_base64):
    try:
        user = User.objects.get(id=id)
        old_avatar = user.avatar.url
        slice = 0
        for s in img_base64:
            slice += 1
            if s == ",":
                break
        if slice > 50:
            slice = 0
        img = base64.b64decode(img_base64[slice:])
        try:
            if "test_avatar" not in old_avatar:
                os.remove("./static/avatar/{}.jpeg".format("avatar_" + str(user.id)))

        except Exception:
            raise
        try:
            with open(
                "./static/avatar/{}.jpeg".format("avatar_" + str(user.id)), "wb"
            ) as f:
                f.write(img)

        except Exception:
            raise
        user.avatar = "avatar/{}.jpeg".format("avatar_" + str(user.id))
        user.save()
        return from_user_to_dict(user)

    except Exception:
        return {}


@db_oper_deco
def change_gallery_layout(gallery_id, layout):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        gallery.layout = layout
        gallery.save()
        return from_gallery_to_dict(gallery)

    except Exception:
        return {}


@db_oper_deco
def change_gallery_order(gallery_id, order):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        photos = gallery.photo_set.all()
        for i, id in enumerate(order):
            photo = photos.get(id=id)
            photo.order = i
            photo.save()

    except Exception:
        raise


@db_oper_deco
def get_all_gallery_comments():
    com_list = Gallery_Comment.objects.all()
    return [from_comment_to_dict(x) for x in com_list]


@db_oper_deco
def get_all_photo_comments():
    com_list = Photo_Comment.objects.all()
    return [from_comment_to_dict(x) for x in com_list]


@db_oper_deco
def more_info_on_comment(id, type):
    """
        type = 0 gallery_comment,
        type = 1 photo_comment
    """
    try:
        if type == 0:
            comment = Gallery_Comment.objects.get(id=id)
            return from_gallery_to_dict(comment.gallery)
        elif type == 1:
            comment = Photo_Comment.objects.get(id=id)
            return from_photo_to_dict(comment.photo)

    except Exception:
        return {}


@db_oper_deco
def ban_comment(id, type):
    """
        type = 0 gallery_comment
        type = 1 photo_comment
    """
    try:
        if type == 0:
            comment = Gallery_Comment.objects.get(id=id)
            comment.is_banned = True
            comment.save()
            return from_comment_to_dict(comment)
        elif type == 1:
            comment = Photo_Comment.objects.get(id=id)
            comment.is_banned = True
            comment.save()
            return from_comment_to_dict(comment)

    except Exception:
        return {}


@db_oper_deco
def comment_is_banned(id, type):
    """
        type = 0 gallery_comment
        type = 1 photo_comment
    """
    try:
        if type == 0:
            comment = Gallery_Comment.objects.get(id=id)
            return comment.is_banned
        elif type == 1:
            comment = Photo_Comment.objects.get(id=id)
            return comment.is_banned

    except Exception:
        return False


@db_oper_deco
def unban_comment(id, type):
    """
        type = 0 gallery_comment
        type = 1 photo_comment
    """
    try:
        if type == 0:
            comment = Gallery_Comment.objects.get(id=id)
            comment.is_banned = False
            comment.save()
            return from_comment_to_dict(comment)
        elif type == 1:
            comment = Photo_Comment.objects.get(id=id)
            comment.is_banned = False
            comment.save()
            return from_comment_to_dict(comment)

    except Exception:
        return {}


@db_oper_deco
def relive_user(id):
    try:
        user = User.objects.get(id=id)
        if is_killed(user.id):
            permission = Permission.objects.get(codename="is_alive")
            user.django_user.user_permissions.add(permission)
        return from_user_to_dict(user)

    except Exception:
        return {}


@db_oper_deco
def get_queue(name):
    if name == "fix":
        Model = FixQueue
    elif name == "check":
        Model = CheckQueue
    if Model.objects.count() == 0:
        Model.objects.create()
    return Model.objects.first().queue_length


@db_oper_deco
def push_queue(name):
    if name == "fix":
        Model = FixQueue
    elif name == "check":
        Model = CheckQueue
    if Model.objects.count() == 0:
        Model.objects.create()
    queue = Model.objects.first()
    if queue.queue_length < MAX_QUEUE_LENGTH:
        queue.queue_length += 1
        queue.save()
        return queue.queue_length
    return None


@db_oper_deco
def pop_queue(name):
    if name == "fix":
        Model = FixQueue
    elif name == "check":
        Model = CheckQueue
    if Model.objects.count() == 0:
        Model.objects.create()
    queue = Model.objects.first()
    queue.queue_length -= 1
    queue.save()
    return queue.queue_length >= 0


@db_oper_deco
def from_id_to_base64(type, id):
    """
        type = 0 raw
        type = 1 processed
    """
    if type == 0:
        try:
            with open("./static/photo/raw/{}.jpeg".format(id), "rb") as f:
                img = f.read()
                b64 = base64.b64encode(img).decode()
                return b64
        except FileNotFoundError:
            return None
    elif type == 1:
        try:
            with open("./static/photo/processed/{}.jpeg".format(id), "rb") as f:
                img = f.read()
                b64 = base64.b64encode(img).decode()
                return b64
        except FileNotFoundError:
            return None
