from django.db import models
from django.contrib.auth.models import User as User_django
from django.core.paginator import *


# Create your models here.
class User(models.Model):
    name = models.CharField(unique=True, max_length=20)
    register_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        upload_to="static/photos/avatar",
        blank=True,
        default="./static/test_photos/test_avatar.jpeg",
    )
    admin = models.BooleanField(default=False)  # Admin = True
    django_user = models.OneToOneField(User_django, on_delete=models.CASCADE)
    cmt_cnt = models.IntegerField(default=0)
    report_cmt_cnt = models.IntegerField(default=0)

    class Meta:
        permissions = [
            ("is_admin", "This user is an admin"),
            ("post_comments", "This user can post comments"),
            ("is_alive", "This user is not killed"),
        ]


class Tag(models.Model):
    tag = models.CharField(max_length=20)
    fixed = models.BooleanField(default=False)


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="undefined")
    intro = models.CharField(max_length=500)
    cover = models.ImageField(
        upload_to="static/photos/cover",
        blank=True,
        default="./static/test_photos/cover",
    )
    like_user = models.ManyToManyField(User, related_name="like_user_gallery")
    like = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    like = models.IntegerField(default=0)
    layout = models.CharField(max_length=20, default="board")
    cmt_cnt = models.IntegerField(default=0)


class Photo(models.Model):
    group_id = models.IntegerField(
        default=95434
    )  # Different phases of a photo have the same group_id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=20, default="Untitled")
    info = models.CharField(max_length=100, default="Uninfoed")
    pub_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to="static/photos/photo", default="./static/test_photos/8513087.jpg"
    )
    gallery = models.ManyToManyField(Gallery)
    like_user = models.ManyToManyField(User, related_name="like_user_photo")
    like = models.IntegerField(default=0)
    operation = models.CharField(max_length=100, default="origin")
    year = models.IntegerField(default=2022)
    cmt_cnt = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    # started_repair_time = models.DateTimeField()


class Photo_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    like_user = models.ManyToManyField(User, related_name="like_user_photo_comment")
    like = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)
    is_banned = models.BooleanField(default=False)
    report_cnt = models.IntegerField(default=0)
    report_user = models.ManyToManyField(User, related_name="report_user_photo_comment")


class Gallery_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    like_user = models.ManyToManyField(User, related_name="like_user_gallery_comment")
    like = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)
    is_banned = models.BooleanField(default=False)
    report_cnt = models.IntegerField(default=0)
    report_user = models.ManyToManyField(
        User, related_name="report_user_gallery_comment"
    )


class FixQueue(models.Model):
    queue_length = models.IntegerField(default=0)


class CheckQueue(models.Model):
    queue_length = models.IntegerField(default=0)
