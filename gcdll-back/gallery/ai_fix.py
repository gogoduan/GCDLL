import requests
from gallery.io import *
import base64
import io
import re
from gallery.models import *

# import datetime
from django.utils import timezone
import time
import os
from PIL import Image
from copy import copy
from gallery.exceptions import logger


url_pre = "^data:image/.+;base64,"
base_url = "https://aip.baidubce.com/rest/2.0/"
access_token = "24.519d483937ab634db771b0a60edc6b10.2592000.1654695257.282335-26192511"

global_timeout = 12.2


def image_defog(photo_id, img_b64, title, info, tag1, user_id):
    """
        图片除雾函数
        传入图片img
        在向百度智能云发送请求后传回处理后图�??
    """
    img_base64 = copy(img_b64)
    try:
        img_b64 = re.sub(url_pre, "", img_b64)
        imgdata = base64.b64decode(img_b64)
        im = Image.open(io.BytesIO(imgdata))
        width, height = im.size
        if max(width, height) > 1600:
            if width > height:
                im = im.resize((1600, int(height * 1600 / width)), Image.ANTIALIAS)
            else:
                im = im.resize((int(width * 1600 / height), 1600), Image.ANTIALIAS)
            buffered = io.BytesIO()
            im.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue())
    except Exception:
        pass
    # tag = Tag.objects.filter(tag=tag1, fixed=True)
    # if tag.count() == 0:
    #     tag = Tag.objects.create(tag=tag1, fixed=True)
    # else:
    #     tag = tag[0]
    request_url = base_url + "image-process/v1/dehaze"
    params = {"image": img_base64}
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    try:
        logger.info("{} send".format(photo_id))
        time.sleep(1)
        response = requests.post(
            request_url, data=params, headers=headers, timeout=global_timeout
        )
    except Exception as e:
        logger.error("{} timeout".format(photo_id))
        return None
    if response:
        try:
            img_base64 = response.json()["image"]
        except Exception:
            logger.error(response.json())
            return None
        img_data = base64.b64decode(img_base64)
        # user = User.objects.filter(id=user_id).first()
        # photo = Photo.objects.get(id=photo_id)
        # photo.title = title
        # photo.info = info
        # photo.user = user
        # photo.tag.add(tag)
        try:
            os.remove("./static/photo/raw/{}.jpeg".format(photo_id))
        except FileNotFoundError:
            pass
        with open("./static/photo/processed/{}.jpeg".format(photo_id), "wb") as f:
            f.write(img_data)
        # photo.photo="photo/processed/{}.jpeg".format(photo_id)
        # photo.operation = "图片除雾"
        # photo.pub_date = timezone.now()
        # photo.save()
        photo_dict = {
            "user": user_id,
            "title": title,
            "info": info,
            "pub_date": timezone.now(),
            "operation": "图片除雾",
            "photo": "photo/processed/{}.jpeg".format(photo_id),
        }
        if not photo_set_all(photo_id, photo_dict):
            logger.error("{} photo set error".format(photo_id))
            return None
        photo_remove_tags(photo_id, ["修复中"])
        photo_add_tags(photo_id, [tag1], True)
        return img_base64, get_photo(photo_id)
    else:
        logger.error("{} no response".format(photo_id))
        return None


def image_enhance_contrast(photo_id, img_b64, title, info, tag1, user_id):
    """
        图片对比度增�?
        传入图片img
        在向百度智能云发送请求后传回处理后图�??
    """
    # time.sleep(5)
    img_base64 = copy(img_b64)
    try:
        img_b64 = re.sub(url_pre, "", img_b64)
        imgdata = base64.b64decode(img_b64)
        im = Image.open(io.BytesIO(imgdata))
        width, height = im.size
        if max(width, height) > 1600:
            if width > height:
                im = im.resize((1600, int(height * 1600 / width)), Image.ANTIALIAS)
            else:
                im = im.resize((int(width * 1600 / height), 1600), Image.ANTIALIAS)
            buffered = io.BytesIO()
            im.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue())
    except Exception:
        pass
    # tag = Tag.objects.filter(tag=tag1, fixed=True)
    # if tag.count() == 0:
    #     tag = Tag.objects.create(tag=tag1, fixed=True)
    # else:
    #     tag = tag[0]

    request_url = base_url + "image-process/v1/contrast_enhance"
    params = {"image": img_base64}
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    try:
        logger.info("{} send".format(photo_id))
        time.sleep(1)
        response = requests.post(
            request_url, data=params, headers=headers, timeout=global_timeout
        )
    except Exception as e:
        logger.error("{} timeout".format(photo_id))
        return None
    if response:
        try:
            img_base64 = response.json()["image"]
        except Exception:
            logger.error(response.json())
            return None
        img_data = base64.b64decode(img_base64)
        # user = User.objects.filter(id=user_id).first()
        # photo = Photo.objects.get(id=photo_id)
        # photo.title = title
        # photo.info = info
        # photo.user = user
        # photo.tag.add(tag)
        try:
            os.remove("./static/photo/raw/{}.jpeg".format(photo_id))
        except FileNotFoundError:
            pass
        with open("./static/photo/processed/{}.jpeg".format(photo_id), "wb") as f:
            f.write(img_data)
        # photo.photo="photo/processed/{}.jpeg".format(photo_id)
        # photo.operation = "对比度增强"
        # photo.pub_date = timezone.now()
        # photo.save()
        photo_dict = {
            "user": user_id,
            "title": title,
            "info": info,
            "pub_date": timezone.now(),
            "operation": "对比度增强",
            "photo": "photo/processed/{}.jpeg".format(photo_id),
        }
        if not photo_set_all(photo_id, photo_dict):
            logger.error("{} photo set error".format(photo_id))
            return None
        photo_remove_tags(photo_id, ["修复中"])
        photo_add_tags(photo_id, [tag1], True)
        return img_base64, get_photo(photo_id)
    else:
        logger.error("{} no response".format(photo_id))
        return None


def image_colourize(photo_id, img_b64, title, info, tag1, user_id):
    img_base64 = copy(img_b64)
    try:
        img_b64 = re.sub(url_pre, "", img_b64)
        imgdata = base64.b64decode(img_b64)
        im = Image.open(io.BytesIO(imgdata))
        width, height = im.size
        if max(width, height) > 1600:
            if width > height:
                im = im.resize((1600, int(height * 1600 / width)), Image.ANTIALIAS)
            else:
                im = im.resize((int(width * 1600 / height), 1600), Image.ANTIALIAS)
            buffered = io.BytesIO()
            im.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue())
    except Exception:
        pass
    # tag = Tag.objects.filter(tag=tag1, fixed=True)
    # if tag.count() == 0:
    #     tag = Tag.objects.create(tag=tag1, fixed=True)
    # else:
    #     tag = tag[0]

    request_url = base_url + "image-process/v1/colourize"
    params = {"image": img_base64}
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    try:
        logger.info("{} send".format(photo_id))
        time.sleep(1)
        response = requests.post(
            request_url, data=params, headers=headers, timeout=global_timeout
        )
    except Exception:
        logger.error("{} timeout".format(photo_id))
        return None
    if response:
        try:
            img_base64 = response.json()["image"]
        except Exception:
            logger.error(response.json())
            return None
        img_data = base64.b64decode(img_base64)
        # user = User.objects.filter(id=user_id).first()
        # photo = Photo.objects.get(id=photo_id)
        # photo.title = title
        # photo.info = info
        # photo.user = user
        # photo.tag.add(tag)
        try:
            os.remove("./static/photo/raw/{}.jpeg".format(photo_id))
        except FileNotFoundError:
            pass
        with open("./static/photo/processed/{}.jpeg".format(photo_id), "wb") as f:
            f.write(img_data)
        # photo.photo="photo/processed/{}.jpeg".format(photo_id)
        # photo.operation = "黑白上色"
        # photo.pub_date = timezone.now()
        # photo.save()
        photo_dict = {
            "user": user_id,
            "title": title,
            "info": info,
            "pub_date": timezone.now(),
            "operation": "黑白上色",
            "photo": "photo/processed/{}.jpeg".format(photo_id),
        }
        if not photo_set_all(photo_id, photo_dict):
            logger.error("{} photo set error".format(photo_id))
            return None
        photo_remove_tags(photo_id, ["修复中"])
        photo_add_tags(photo_id, [tag1], True)
        return img_base64, get_photo(photo_id)
    else:
        logger.error("{} no response".format(photo_id))
        return None


def img_sharpness_enhancement(photo_id, img_b64, title, info, tag1, user_id):
    img_base64 = copy(img_b64)
    try:
        img_b64 = re.sub("^data:image/.+;base64,", "", img_b64)
        imgdata = base64.b64decode(img_b64)
        im = Image.open(io.BytesIO(imgdata))
        width, height = im.size
        if max(width, height) > 1600:
            if width > height:
                im = im.resize((1600, int(height * 1600 / width)), Image.ANTIALIAS)
            else:
                im = im.resize((int(width * 1600 / height), 1600), Image.ANTIALIAS)
            buffered = io.BytesIO()
            im.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue())
    except Exception:
        pass
    # tag = Tag.objects.filter(tag=tag1, fixed=True)
    # if tag.count() == 0:
    #     tag = Tag.objects.create(tag=tag1, fixed=True)
    # else:
    #     tag = tag[0]

    request_url = base_url + "image-process/v1/image_definition_enhance"
    params = {"image": img_base64}
    request_url = request_url + "?access_token=" + access_token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    try:
        logger.info("{} send".format(photo_id))
        time.sleep(1)
        response = requests.post(
            request_url, data=params, headers=headers, timeout=global_timeout
        )
    except Exception as e:
        logger.error("{} timeout".format(photo_id))
        return None
    if response:
        try:
            img_base64 = response.json()["image"]
        except Exception:
            logger.error(response.json())
            return None
        img_data = base64.b64decode(img_base64)
        # user = User.objects.filter(id=user_id).first()
        # photo = Photo.objects.get(id=photo_id)
        # photo.title = title
        # photo.info = info
        # photo.user = user
        # photo.tag.add(tag)
        try:
            os.remove("./static/photo/raw/{}.jpeg".format(photo_id))
        except FileNotFoundError:
            pass
        with open("./static/photo/processed/{}.jpeg".format(photo_id), "wb") as f:
            f.write(img_data)
        # photo.photo="photo/processed/{}.jpeg".format(photo_id)
        # photo.operation = "清晰度增强"
        # photo.pub_date = timezone.now()
        # photo.save()
        photo_dict = {
            "user": user_id,
            "title": title,
            "info": info,
            "pub_date": timezone.now(),
            "operation": "清晰度增强",
            "photo": "photo/processed/{}.jpeg".format(photo_id),
        }
        if not photo_set_all(photo_id, photo_dict):
            logger.error("{} photo set error".format(photo_id))
            return None
        photo_remove_tags(photo_id, ["修复中"])
        photo_add_tags(photo_id, [tag1], True)
        return img_base64, get_photo(photo_id)
    else:
        logger.error("{} no response".format(photo_id))
        return None
