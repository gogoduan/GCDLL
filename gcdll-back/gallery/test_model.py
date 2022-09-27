import os
from pyexpat import model
import secrets

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PhotoGallery.settings")
import django

django.setup()
from django.test import TestCase
from django.core.files import File
from .models import *
from .io import *
from django.contrib.auth.models import User as User_django
import random


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        self.password1 = str(secrets.randbits(5))
        self.password2 = str(secrets.randbits(5))
        self.password3 = str(secrets.randbits(5))
        django_user_admin1 = User_django.objects.create(
            username="Alice", password=make_password(self.password1)
        )
        django_user_admin2 = User_django.objects.create(
            username="Bob", password=make_password(self.password2)
        )
        admin1 = User.objects.create(
            name="Alice", admin=True, django_user=django_user_admin1
        )
        admin2 = User.objects.create(
            name="Bob", admin=True, django_user=django_user_admin2
        )
        django_user_visitor1 = User_django.objects.create(
            username="Zella", password=make_password("34567")
        )
        django_user_visitor2 = User_django.objects.create(
            username="Yamo", password=make_password("45678")
        )
        visitor1 = User.objects.create(
            name="Zella",
            admin=False,
            avatar="test_photos/test_avatar.jpeg",
            django_user=django_user_visitor1,
        )
        visitor2 = User.objects.create(
            name="Yamo",
            admin=False,
            avatar="test_photos/for_test.jpeg",
            django_user=django_user_visitor2,
        )
        tag1 = Tag.objects.create(tag="awesome")
        tag2 = Tag.objects.create(tag="brilliant")
        photo1 = Photo.objects.create(
            group_id=1,
            user=admin1,
            title="photo1",
            info="This photo is for test.",
            photo="test_photos/8513279.jpg",
        )
        photo2 = Photo.objects.create(
            group_id=1,
            user=admin1,
            title="photo2",
            info="This photo is for another test",
            photo="test_photos/8463581.jpg",
        )
        photo3 = Photo.objects.create(
            group_id=2,
            user=admin2,
            title="photo3",
            info="This photo is for a third test",
            photo="test_photos/8513087.jpg",
        )
        photo4 = Photo.objects.create(
            group_id=2,
            user=admin2,
            title="photo4",
            info="Same photo, uh?",
            photo="test_photos/8513087.jpg",
        )
        tag1.photo_set.add(photo1)
        tag1.photo_set.add(photo3)
        tag2.photo_set.add(photo1)
        tag2.photo_set.add(photo2)
        tag2.photo_set.add(photo4)
        gallery1 = Gallery.objects.create(
            user=admin1,
            title="gallery1",
            intro="This gallery is for test",
            cover="test_photos/cover.jpg",
        )
        gallery1.photo_set.add(photo1)
        gallery1.photo_set.add(photo2)
        gallery1.photo_set.add(photo3)

        gallery2 = Gallery.objects.create(
            user=admin2,
            title="gallery2",
            intro="This gallery is for another test",
            cover="test_photos/cover.jpg",
        )
        gallery2.photo_set.add(photo2)
        gallery2.photo_set.add(photo3)
        gallery2.photo_set.add(photo4)

        pc1 = Photo_Comment.objects.create(
            user=visitor1, photo=photo1, content="The test photo is really awesome."
        )
        pc2 = Photo_Comment.objects.create(
            user=visitor2,
            photo=photo1,
            content="The test photo is as awesome as Zella said.",
        )
        pc3 = Photo_Comment.objects.create(
            user=visitor1, photo=photo2, content="The test photo is really brilliant."
        )
        pc4 = Photo_Comment.objects.create(
            user=visitor1, photo=photo3, content="The test photo is extremely awesome!!"
        )
        pc5 = Photo_Comment.objects.create(
            user=visitor2,
            photo=photo4,
            content="The test photo is as brilliant as photo2.",
        )

        gc1 = Gallery_Comment.objects.create(
            user=visitor1, gallery=gallery1, content="The test gallery is for Zella!"
        )
        gc2 = Gallery_Comment.objects.create(
            user=visitor2, gallery=gallery2, content="The test gallery is for Yamo!"
        )
        permission1 = Permission.objects.get(codename="is_admin")
        permission2 = Permission.objects.get(codename="post_comments")
        permission3 = Permission.objects.get(codename="is_alive")

        usera = User.objects.get(name="Alice")
        userb = User.objects.get(name="Bob")
        usera.django_user.user_permissions.add(permission1)
        usera.django_user.user_permissions.add(permission3)
        usera.save()
        userb.django_user.user_permissions.add(permission1)
        userb.django_user.user_permissions.add(permission3)
        userb.save()
        self.idr = 0
        self.idp = 0

        filesr = os.listdir("./static/photo/raw")
        for file in filesr:
            if "test" not in file and ".jpeg" in file:
                self.idr = int(file.strip(".jpeg"))
                break

        filesp = os.listdir("./static/photo/processed")
        for file in filesr:
            if "test" not in file and ".jpeg" in file:
                self.idp = int(file.strip(".jpeg"))
                break

    def test_get_photos(self):
        admin = User.objects.get(name="Alice")
        photos = admin.photo_set.all()
        photos = set(map(lambda x: x.title, photos))
        assert photos == {"photo1", "photo2"}

    def test_get_galleries(self):
        photo = Photo.objects.get(title="photo2")
        galleries = photo.gallery.all()
        galleries = set(map(lambda x: x.title, galleries))
        assert galleries == {"gallery1", "gallery2"}
        pass

    def test_get_comments(self):
        photo1 = Photo.objects.get(title="photo1")
        pcs = photo1.photo_comment_set.all()
        pcs = set(map(lambda x: (x.content, x.user.name), pcs))
        assert pcs == {
            ("The test photo is really awesome.", "Zella"),
            ("The test photo is as awesome as Zella said.", "Yamo"),
        }
        gallery1 = Gallery.objects.get(intro="This gallery is for test")
        assert gallery1.title == "gallery1"
        gcs = gallery1.gallery_comment_set.all()
        gcs = set(map(lambda x: (x.content, x.user.name), gcs))
        assert gcs == {("The test gallery is for Zella!", "Zella")}
        pass

    def test_get_photo_tag(self):
        photo3 = Photo.objects.get(title="photo3")
        assert photo3.info == "This photo is for a third test"
        tags = photo3.tag.all()
        tags = set(map(lambda x: x.tag, tags))
        assert tags == {"awesome"}
        pass

    def test_get_gallery_photos(self):
        gallery = Gallery.objects.get(title="gallery1")
        photos = gallery.photo_set.all()
        photo = photos[0]
        photos = set(map(lambda x: x.title, photos))
        assert photos == {"photo1", "photo2", "photo3"}
        gallery_remove_photo(gallery.id, photo.id)
        assert photo not in gallery.photo_set.all()
        try:
            gallery_remove_photo(-1, -1)
            assert False
        except:
            pass

    def test_get_tag_photos(self):
        tag2 = Tag.objects.get(tag="brilliant")
        photos = tag2.photo_set.all()
        admin1 = User.objects.get(name="Alice")
        admin2 = User.objects.get(name="Bob")
        photos = set(map(lambda x: (x.info, x.user.register_date), photos))
        assert photos == {
            ("This photo is for test.", admin1.register_date),
            ("This photo is for another test", admin1.register_date),
            ("Same photo, uh?", admin2.register_date),
        }
        pass

    def test_get_user_comments(self):
        visitor2 = User.objects.filter(admin=False).get(name="Yamo")
        pcs = visitor2.photo_comment_set.all()
        pcs = set(map(lambda x: (x.photo.title, x.content), pcs))
        assert pcs == {
            ("photo1", "The test photo is as awesome as Zella said."),
            ("photo4", "The test photo is as brilliant as photo2."),
        }
        pass

    def test_io(self):
        user1 = User.objects.get(name="Yamo")
        photo1 = Photo.objects.get(title="photo1")
        pc1 = Photo_Comment.objects.get(user=user1, photo=photo1)
        pc1_dict = from_comment_to_dict(pc1)
        assert pc1_dict["user"]["name"] == "Yamo"
        assert pc1_dict["user"]["register_date"] == user1.register_date
        assert pc1_dict["content"] == pc1.content

    def test_password_accuracy(self):
        admin = User.objects.get(name="Bob")
        assert check_password(self.password2, admin.django_user.password)

    def test_create_user(self):
        create_user(
            name="DCQ",
            register_date=None,
            avatar="test_photos/8513279.jpg",
            admin=True,
            password=self.password3,
        )
        user = User.objects.get(name="DCQ")
        assert user.name == "DCQ"
        assert user.django_user.has_perm("gallery.post_comments") == False
        assert user.django_user.has_perm("gallery.is_admin") == True
        # assert(user.django_user.has_perm('gallery.is_admin') == True)
        user = create_user(
            name="CDY",
            register_date=None,
            avatar="test_photos/8513279.jpg",
            admin=False,
            password=self.password3,
        )
        user = User.objects.get(name="CDY")
        # assert(user.django_user.has_perm('gallery.post_comments') == True)
        assert user.django_user.has_perm("gallery.is_admin") == False
        assert user.django_user.has_perm("gallery.post_comments") == True

    def test_ban_user(self):
        user = User.objects.all().first()
        revive_user(user.id)
        unban_user(user.id)
        user = User.objects.get(id=user.id)
        ban_user(user.id)
        assert user.django_user.has_perm("gallery.post_comments") == False
        try:
            user_is_banned(-1)
            assert False
        except:
            pass

    def test_us_admin(self):
        user = User.objects.all().first()
        is_admin(user.id)
        is_admin(-1)

    def test_create_gallery(self):
        photo = Photo.objects.all().first()
        user = User.objects.all().first()
        gallery = create_gallery(
            title="Only for test",
            intro="Guess what",
            photolist=[photo.id],
            user_id=user.id,
            cover="test_photos/8513279.jpg",
        )
        assert gallery["title"] == "Only for test"
        assert gallery["intro"] == "Guess what"
        try:
            gallery = create_gallery(
                title="Only for test",
                intro="Guess what",
                photolist=[photo.id],
                user_id=-1,
                cover="test_photos/8513279.jpg",
            )
        except:
            pass
        try:
            gallery = create_gallery(
                title="Only for test",
                intro="Guess what",
                photolist=[-1],
                user_id=user.id,
                cover="test_photos/8513279.jpg",
            )
        except:
            pass

    def test_like_comment(self):
        photo_comment = Photo_Comment.objects.all().first()
        user = User.objects.all().first()
        a = photo_comment.like
        like_comment(comment_id=photo_comment.id, user_id=user.id, type=0)
        photo_comment = Photo_Comment.objects.all().first()
        b = photo_comment.like
        assert b == a + 1

    def test_delete_comment(self):
        photo_comment = Photo_Comment.objects.all().first()
        a = photo_comment.id
        delete_comment(type=0, comment_id=photo_comment.id)
        assert Photo_Comment.objects.filter(id=a).count() == 0

        gallery_comment = Gallery_Comment.objects.all().first()
        a = gallery_comment.id
        delete_comment(type=1, comment_id=gallery_comment.id)
        assert Gallery_Comment.objects.filter(id=a).count() == 0
        try:
            delete_comment(type=2, comment_id=photo_comment.id)
            assert False
        except:
            pass
        try:
            delete_comment(type=1, comment_id=-1)
            assert False
        except:
            pass
        try:
            delete_comment(type=0, comment_id=-1)
            assert False
        except:
            pass

    def test_change_photo_info(self):
        photo = Photo.objects.all().first()
        change_photo_info(id=photo.id, info="wogaile")
        assert Photo.objects.filter(id=photo.id)[0].info == "wogaile"
        try:
            change_photo_info(id=-1, info="wogaile")
        except:
            pass

    def test_change_photo_titile(self):
        photo = Photo.objects.all().first()
        change_photo_title(id=photo.id, title="wogaile")
        assert Photo.objects.filter(id=photo.id)[0].title == "wogaile"

    def test_change_password(self):
        user = User.objects.get(name="Alice")
        user_dict = change_password(
            id=user.id, old_password=self.password1, new_password=self.password3,
        )
        assert check_password(self.password3, user_dict["password"])
        try:
            user_dict = change_password(
                id=-2, old_password=self.password3, new_password=self.password3,
            )
        except:
            pass
        try:
            user_dict = change_password(
                id=-2, old_password=self.password1, new_password=self.password3,
            )
        except:
            pass
        try:
            change_password(user.id, "1", "2")
        except:
            pass

    def test_create_photo_base64(self):
        user = User.objects.all()[0]
        f = open("./static/photo/raw/{}.jpeg".format(self.idr), "rb")
        img = f.read()
        img64 = base64.b64encode(img)
        photo_dict = create_photo_base64(
            img_base64=img64, user_id=user.id, pub_date=None,
        )
        assert photo_dict["photo"]
        try:
            photo_dict = create_photo_base64(
                img_base64="img64", user_id=user.id, pub_date=None,
            )
        except:
            pass
        photo_dict = create_photo_base64(img64, -1, None)
        assert "photo" not in photo_dict

    def test_search_gallery(self):
        gallery_dict = search_gallery("gallery1")
        assert gallery_dict[0]["title"] == "gallery1"

    def test_comment_photo(self):
        user = User.objects.all()[0]
        photo = Photo.objects.all()[1]
        is_banned, banned_reason, new_comment = comment_photo(
            user_id=user.id, photo_id=photo.id, content="Test message"
        )
        assert new_comment["photo_id"] == photo.id
        is_banned, info = comment_photo(-1, -1, "error")
        assert is_banned

    def test_is_banned(self):
        user = create_user(
            name="temp", admin=True, password="password", register_date=None
        )
        user = User.objects.get(id=user["id"])
        assert user.django_user.has_perm("gallery.is_admin") == True
        assert user.django_user.has_perm("gallery.post_comments") == False
        assert user_is_banned(user.id) == True

    def test_from_photo_to_dict(self):
        photo = Photo.objects.all().first()
        photo_dict = from_photo_to_dict(photo)
        assert photo_dict["id"] == photo.id

    def test_from_user_to_dict(self):
        user = User.objects.all().first()
        user_dict = from_user_to_dict(user)
        assert user_dict["id"] == user.id

    def test_from_comment_to_dict(self):
        comment = Photo_Comment.objects.all().first()
        comment_dict = from_comment_to_dict(comment)
        assert comment_dict["id"] == comment.id

    def test_from_gallery_to_dict(self):
        gallery = Gallery.objects.all().first()
        gallery_dict = from_gallery_to_dict(gallery)
        assert gallery_dict["id"] == gallery.id

    def test_get_all_galleries(self):
        galleries_dict = get_all_galleries()
        for i, gallery in enumerate(Gallery.objects.all()):
            assert galleries_dict[i]["id"] == gallery.id

    def test_get_all_photos(self):
        photos_dict = get_all_photos()
        for i, gallery in enumerate(Photo.objects.all()):
            assert photos_dict[i]["id"] == gallery.id

    def test_get_user(self):
        user = User.objects.all().first()
        user_dict = get_user(user.id)
        assert user_dict["id"] == user.id
        try:
            get_user(-1)
        except:
            pass

    def test_delete_gallery(self):
        gallery = Gallery.objects.all().first()
        id = gallery.id
        delete_gallery(id)
        assert Gallery.objects.filter(id=id).count() == 0
        flag = False
        try:
            delete_gallery(-1)
        except:
            flag = True
            pass

    def test_set_group_id(self):
        photo = Photo.objects.all().first()
        set_group_id(photo.id, 3)
        assert Photo.objects.all().first().group_id == 3

    def test_photo_remove_tags_and_photo_add_tags(self):
        photo = Photo.objects.all().first()
        photo_add_tags(photo.id, ["测试1"])
        tag = Tag.objects.all().get(tag="测试1")
        assert tag in photo.tag.all()
        photo_remove_tags(photo.id, ["测试1"])
        assert tag not in photo.tag.all()
        try:
            photo_remove_tags(-1, -1)
            assert False
        except:
            pass

    def test_photo_change_tags(self):
        photo = Photo.objects.all().first()
        photo_add_tags(photo.id, ["测试1"])
        tag = Tag.objects.all().get(tag="测试1")
        photo_change_tags(photo.id, ["测试2"])
        tag1 = Tag.objects.all().get(tag="测试1")
        tag2 = Tag.objects.all().get(tag="测试2")
        assert tag1 not in photo.tag.all()
        assert tag2 in photo.tag.all()

    def test_gallery_change_tags(self):
        gallery = Gallery.objects.all().first()
        gallery_add_tags(gallery.id, ["测试1"])
        tag = Tag.objects.all().get(tag="测试1")
        gallery_change_tags(gallery.id, ["测试2"])
        tag1 = Tag.objects.all().get(tag="测试1")
        tag2 = Tag.objects.all().get(tag="测试2")
        assert tag1 not in gallery.tag.all()
        assert tag2 in gallery.tag.all()
        gallery_remove_tags(gallery.id, [tag2.tag])
        assert tag2 not in gallery.tag.all()

        try:
            gallery_change_tags(-1, -1)
            assert False
        except:
            pass
        try:
            gallery_remove_tags(-1, -1)
            assert False
        except:
            pass

    def test_unban_user(self):
        user = User.objects.all().first()
        relive_user(user.id)
        ban_user(user.id)
        assert user_is_banned(user.id)
        unban_user(user.id)
        assert not user_is_banned(user.id)
        try:
            relive_user(-1)
        except:
            pass

    def test_photo_liked_and_like_photo(self):
        user = User.objects.all().first()
        photo = Photo.objects.all().first()
        like_photo(user.id, photo.id, type=0)
        assert photo_liked(user.id, photo.id)
        like_photo(user.id, photo.id, type=1)
        assert not photo_liked(user.id, photo.id)
        try:
            like_photo(-1, -1, 0)
        except:
            pass
        try:
            like_photo(user.id, photo.id, type=4)
        except:
            pass

    def test_liked_comment(self):
        user = User.objects.all().first()
        photo_comment = Photo_Comment.objects.all().first()
        gallery_comment = Gallery_Comment.objects.all().first()
        like_comment(type=0, comment_id=photo_comment.id, user_id=user.id)
        assert photo_comment_liked(user.id, photo_comment.id)
        like_comment(type=2, comment_id=photo_comment.id, user_id=user.id)
        assert not photo_comment_liked(user.id, photo_comment.id)
        like_comment(type=1, comment_id=gallery_comment.id, user_id=user.id)
        assert gallery_comment_liked(user.id, gallery_comment.id)
        like_comment(type=3, comment_id=gallery_comment.id, user_id=user.id)
        assert not gallery_comment_liked(user.id, gallery_comment.id)
        try:
            like_comment(0, -1, -1)
        except:
            pass

    def test_gallery_liked(self):
        gallery = Gallery.objects.all().first()
        user = User.objects.all().first()
        like_gallery(user.id, gallery.id, 0)
        assert gallery_liked(user.id, gallery.id)
        try:
            like_gallery(-1, -1, 0)
        except:
            pass
        try:
            like_gallery(user.id, gallery.id, 4)
        except:
            pass
        try:
            like_gallery(user.id, gallery.id, 1)
        except:
            pass

    def test_change_gallery_cover(self):
        gallery = Gallery.objects.all().first()
        user = User.objects.all().first()
        f = open("./static/photo/raw/{}.jpeg".format(self.idr), "rb")
        img = f.read()
        img64 = base64.b64encode(img)
        gallery_dict = change_gallery_cover(gallery.id, img64, user.id, pub_date=None)
        assert str(gallery.id) in gallery_dict["cover"]
        try:
            change_gallery_cover(-1, img64, user.id, pub_date=None)
        except:
            pass

    def test_kill_user_and_is_killed(self):
        user = User.objects.all().first()
        if is_killed(user.id):
            permission = Permission.objects.get(codename="is_alive")
            user.django_user.user_permissions.add(permission)
        assert not is_killed(user.id)
        kill_user(user.id)
        assert is_killed(user.id)
        try:
            kill_user(-1)
            assert False
        except:
            pass

    def test_remove_photo_from_gallery_and_add_photo_to_gallery(self):
        gallery = Gallery.objects.all().first()
        photo = Photo.objects.all().first()
        gallery_add_photo(gallery.id, photo.id)
        assert gallery.photo_set.contains(photo)
        remove_photo_from_gallery(gallery.id, photo.id)
        assert not gallery.photo_set.contains(photo)

    def test_change_gallery_info(self):
        gallery = Gallery.objects.all().first()
        change_gallery_intro(gallery.id, "修改了")
        gallery = Gallery.objects.all().first()
        assert gallery.intro == "修改了"

    def test_change_gallery_title(self):
        gallery = Gallery.objects.all().first()
        change_gallery_title(gallery.id, "修改了")
        gallery = Gallery.objects.all().first()
        assert gallery.title == "修改了"

    def test_gallery_advanced_search(self):
        gallery = Gallery.objects.all().first()
        change_gallery_title(gallery.id, "修改了")
        filters = [
            {"min_id": 0, "max_id": 1000000,},
            {"min_timestamp": 1272643200000, "max_timestamp": 1688054400000,},
            {"title": ["修改了"], "tag": [gallery.tag], "introduction": [gallery.intro],},
        ]
        num, gallery_dict_list = gallery_advanced_search(filters, 1, 1, "like", False)
        assert gallery_dict_list[0]["id"] == gallery.id
        num, gallery_dict_list = gallery_advanced_search(filters, None, None)
        assert num == 0
        filters[0]["min_id"] = "sije"
        num, gallery_dict_list = gallery_advanced_search(filters, 1, 1, "like", False)
        assert len(gallery_dict_list) == 0

    def test_photo_advanced_search(self):
        photo = Photo.objects.all().first()
        change_photo_title(photo.id, "123")
        filters = [
            {"min_id": 0, "max_id": 10000000,},
            {"min_timestamp": 1272643200000, "max_timestamp": 1688054400000,},
            {
                "title": ["123"],
                "tag": ["sajhdbhjabshdb"],
                "introduction": ["sahjhjasghdaj"],
                "negative": False,
            },
        ]
        num, photo_dict_list = photo_advanced_search(filters, 1, 1, "time", True, False)
        assert photo.id in [x["id"] for x in photo_dict_list]
        filters[0]["min_id"] = "aid"
        num, photo_dict_list = photo_advanced_search(filters, 1, 1, "time", True, False)
        assert len(photo_dict_list) == 0
        filters[0]["min_id"] = 0
        num, photo_dict_list = photo_advanced_search(
            filters, 1, None, "time", True, False
        )
        assert num == 0
        filters.append({"exhibit_id": -1})
        num, photo_dict_list = photo_advanced_search(filters, 1, 1, "time", True, False)
        assert num == 0

    def test_photo_comment_advanced_search(self):
        photo_comment = Photo_Comment.objects.all().first()
        filters = [
            {"min_id": 0, "max_id": 10000000,},
            {"min_timestamp": 1272643200000, "max_timestamp": 1688054400000,},
            {
                "username": [photo_comment.user.name],
                "content": [photo_comment.content],
                "info": [photo_comment.photo.title],
                "banned": "banned" if photo_comment.is_banned is True else "unbanned",
            },
        ]
        num, pho_cmt_dict_list = photo_comment_advanced_search(
            filters, 1, 1, "user_report", False
        )
        assert pho_cmt_dict_list[0]["id"] == photo_comment.id
        filters2 = [
            {"banned": "unbanned" if photo_comment.is_banned is True else "banned"}
        ]
        num, pho_cmt_dict_list = photo_comment_advanced_search(
            filters2, 1, 1, "user_report", False
        )
        assert photo_comment.id not in [x["id"] for x in pho_cmt_dict_list]
        filters[0]["min_id"] = "ffsdc"
        num, pho_cmt_dict_list = photo_comment_advanced_search(
            filters, 1, 1, "user_report", False
        )
        assert num == 0
        filters[0]["min_id"] = 0
        num, pho_cmt_dict_list = photo_comment_advanced_search(
            filters, 1, None, "user_report", False
        )
        assert num == 0

    def test_gallery_comment_advanced_search(self):
        gallery_comment = Gallery_Comment.objects.all().first()
        filters = [
            {"min_id": 0, "max_id": 10000000,},
            {"min_timestamp": 1272643200000, "max_timestamp": 1688054400000,},
            {
                "username": [gallery_comment.user.name],
                "content": [gallery_comment.content],
                "info": [gallery_comment.gallery.title],
                "banned": "banned" if gallery_comment.is_banned is True else "unbanned",
            },
        ]
        num, gal_cmt_dict_list = gallery_comment_advanced_search(
            filters, 1, 1, "comment_report", False
        )
        assert gal_cmt_dict_list[0]["id"] == gallery_comment.id
        filters2 = [
            {"banned": "unbanned" if gallery_comment.is_banned is True else "banned",}
        ]
        num, gal_cmt_dict_list = gallery_comment_advanced_search(
            filters2, 1, 1, "user_report", False
        )
        assert gallery_comment.id not in [x["id"] for x in gal_cmt_dict_list]
        filters[0]["min_id"] = "ffsdc"
        num, gal_cmt_dict_list = gallery_comment_advanced_search(
            filters, 1, 1, "user_report", False
        )
        assert num == 0
        filters[0]["min_id"] = 0
        num, gal_cmt_dict_list = gallery_comment_advanced_search(
            filters, 1, None, "user_report", False
        )
        assert num == 0

    def test_report_photo_comment(self):
        photo_comment = Photo_Comment.objects.all().first()
        origin_report = photo_comment.report_cnt
        report_photo_comment(photo_comment.id)
        photo_comment = Photo_Comment.objects.all().first()
        assert photo_comment.report_cnt == origin_report + 1
        try:
            report_photo_comment(-1)
        except:
            pass

    def test_report_gallery_comment(self):
        gallery_comment = Gallery_Comment.objects.all().first()
        origin_report = gallery_comment.report_cnt
        report_gallery_comment(gallery_comment.id)
        gallery_comment = Gallery_Comment.objects.all().first()
        assert gallery_comment.report_cnt == origin_report + 1
        try:
            report_gallery_comment(-1)
        except:
            pass

    def test_delete_photo(self):
        photo = Photo.objects.all().first()

    def test_change_user_avatar(self):
        user = User.objects.all().first()
        f = open("./static/photo/raw/{}.jpeg".format(self.idr), "rb")
        img = f.read()
        img64 = base64.b64encode(img)
        user_dict = change_user_avatar(user.id, img64)
        assert "avatar_{}".format(user.id) in user_dict["avatar"]
        try:
            change_user_avatar(-1, img64)
        except:
            pass

    def test_change_gallery_layout(self):
        gallery = Gallery.objects.all().first()
        gallery_dict = change_gallery_layout(gallery.id, "修改了")
        assert gallery_dict["layout"] == "修改了"

    def test_ban_comment(self):
        comment = Photo_Comment.objects.all().first()
        if comment_is_banned(comment.id, 1) is True:
            unban_comment(comment.id, 1)
            assert not comment_is_banned(comment.id, 1)
        else:
            ban_comment(comment.id, 1)
            assert comment_is_banned(comment.id, 1)
        comment = Gallery_Comment.objects.all().first()
        if comment_is_banned(comment.id, 0) is True:
            unban_comment(comment.id, 0)
            assert not comment_is_banned(comment.id, 0)
        else:
            ban_comment(comment.id, 0)
            assert comment_is_banned(comment.id, 0)
        try:
            ban_comment(-1, 0)
        except:
            pass
        try:
            comment_is_banned(-1, 0)
        except:
            pass

    def test_user_advanced_search(self):
        for user1 in User.objects.all():
            if not user1.django_user.has_perm("gallery.is_admin"):
                user = user1
                break
        filters = [
            {"min_id": 0, "max_id": 10000000,},
            {"min_timestamp": 1000000000000, "max_timestamp": 1688054400000,},
            {"name": [user.name],},
        ]
        for i in range(3):
            if i >= 1:
                revive_user(user.id)
                unban_user(user.id)
                user = User.objects.get(id=user.id)
            if i == 2:
                ban_user(user.id)
                user = User.objects.get(id=user.id)
            if user.django_user.has_perm("gallery.post_comments"):
                num, user_dict = user_advanced_search(
                    "visited", filters, 1, 1, "time", False
                )
                assert user.id == user_dict[0]["id"]
            elif not user.django_user.has_perm("gallery.is_alive"):
                num, user_dict = user_advanced_search(
                    "deleted", filters, 1, 1, "comment_cnt", False
                )
                assert user.id == user_dict[0]["id"]
            else:
                num, user_dict = user_advanced_search(
                    "banned", filters, 1, 1, "reported_cnt", False
                )
                assert user.id == user_dict[0]["id"]
                num, user_dict = user_advanced_search(
                    "banned", filters, 1, None, "reported_cnt", False
                )
                assert num == 0
                filters[0]["min_id"] = "easfe"
                num, user_dict = user_advanced_search(
                    "banned", filters, 1, 1, "reported_cnt", False
                )
                assert num == 0
                filters[0]["min_id"] = 0

    def test_forbid_comment_and_revive_comment(self):
        comment = Photo_Comment.objects.all()[0]
        if comment.is_banned is True:
            revive_comment(0, comment.id)
            assert Photo_Comment.objects.all()[0].is_banned is False
        else:
            forbid_comment(0, comment.id)
            assert Photo_Comment.objects.all()[0].is_banned is True
        comment = Gallery_Comment.objects.all()[0]
        if comment.is_banned is True:
            revive_comment(1, comment.id)
            assert Gallery_Comment.objects.all()[0].is_banned is False
        else:
            forbid_comment(1, comment.id)
            assert Gallery_Comment.objects.all()[0].is_banned is True
        comment = Photo_Comment.objects.all()[0]
        revive_comment(0, comment.id)
        comment = Gallery_Comment.objects.all()[0]
        revive_comment(1, comment.id)

        try:
            revive_comment(type=2, comment_id=comment.id)
            assert False
        except:
            pass
        try:
            revive_comment(type=1, comment_id=-1)
            assert False
        except:
            pass
        try:
            revive_comment(type=0, comment_id=-1)
            assert False
        except:
            pass
        try:
            forbid_comment(type=2, comment_id=comment.id)
            assert False
        except:
            pass
        try:
            forbid_comment(type=1, comment_id=-1)
            assert False
        except:
            pass
        try:
            forbid_comment(type=0, comment_id=-1)
            assert False
        except:
            pass

    def test_from_id_to_base64(self):
        assert from_id_to_base64(0, self.idr) is not None
        assert from_id_to_base64(0, self.idp) is not None

    def test_queue_functions(self):
        get_queue("fix")
        push_queue("fix")
        pop_queue("fix")
        get_queue("check")
        push_queue("check")
        pop_queue("check")

    def test_get_comment(self):
        pc = Photo_Comment.objects.first()
        get_comment(pc.id, type=1, order=1, start=0)
        get_comment(pc.id, type=1, order=0, start=0)
        gc = Photo_Comment.objects.first()
        get_comment(gc.id, type=0, order=1, start=0)
        get_comment(gc.id, type=0, order=0, start=0)
        try:
            get_comment(-1, 0, 1, 0)
        except:
            pass
        ret = get_comment(gc.id, type=2, order=0, start=0)
        assert len(ret) == 0

    def test_comment_gallery(self):
        user = User.objects.first()
        gallery = Gallery.objects.all().first()
        comment_gallery(user.id, gallery.id, "123")
        comment_gallery(user.id, gallery.id, "123")
        comment_gallery(user.id, gallery.id, "123")
        comment_gallery(user.id, gallery.id, "123")
        try:
            comment_gallery(-1, -1, "123")
        except:
            pass

    def test_get_all_users(self):
        get_all_users(None)
        get_all_users("report_cnt")
        get_all_users("cmt_cnt")

    def test_get_photos(self):
        photo = Photo.objects.all().first()
        get_photo(photo.id)
        try:
            get_photo(-1)
        except:
            pass

    def test_change_photo_pubdate_now(self):
        photo = Photo.objects.all().first()
        change_photo_pubdate_now(photo.id)
        try:
            change_photo_title(-1, "123")
        except:
            pass

    def test_order_set(self):
        photo = Photo.objects.all()
        order_set("comment", True, photo)
        order_set("comment", False, photo)
        order_set("time", False, photo)

    def test_get_gallery(self):
        gallery = Gallery.objects.all().first()
        get_gallery(gallery.id)
        try:
            get_gallery(-1)
        except:
            pass

    def test_user_logout(self):
        try:
            user_logout(-1)
        except:
            pass
        try:
            user_logout(User.objects.first().id)
        except:
            pass

    def test_more_info_on_comment(self):
        photo_comment = Photo_Comment.objects.all().first()
        gallery_comment = Gallery_Comment.objects.all().first()
        more_info_on_comment(0, gallery_comment.id)
        more_info_on_comment(1, photo_comment.id)
        try:
            more_info_on_comment(0, -1)
        except:
            pass

    def test_get_all_photo_comments(self):
        get_all_photo_comments()
        get_all_gallery_comments()

    def test_change_gallery_order(self):
        try:
            gallery = Gallery.objects.first()
            id = gallery.photo_set.all()[0].id
            change_gallery_order(gallery.id, [id])
        except:
            pass
        try:
            change_gallery_order(Gallery.objects.first().id, [1])
        except:
            pass

    def test_photo_and_gallery_comment_reported(self):
        photo_comment = Photo_Comment.objects.all()[0]
        user = User.objects.all()[0]
        gallery_comment = Gallery_Comment.objects.all()[0]
        try:
            photo_comment_reported(photo_comment.id, user.id)
            gallery_comment_reported(gallery_comment.id, user.id)
        except:
            pass
        try:
            photo_comment_reported(-1, -1)
        except:
            pass
        try:
            gallery_comment_reported(-1, user.id)
        except:
            pass

    def test_revive_user(self):
        user = User.objects.all()[0]
        try:
            revive_user(user.id)
        except:
            pass
        try:
            revive_user(-1)
        except:
            pass

    def test_get_group_photos(self):
        photo3 = Photo.objects.get(title="photo3")
        photo_list = get_photo_by_group_id(photo3.group_id)
        assert "photo4" in [x["title"] for x in photo_list]

    def test_report_comment(self):
        comment = Photo_Comment.objects.first()
        report_cnt = comment.report_cnt
        user = User.objects.first()
        report_comment(type=0, comment_id=comment.id, user_id=user.id)
        comment = Photo_Comment.objects.get(id=comment.id)
        assert comment.report_user.contains(user)
        assert comment.report_cnt == report_cnt + 1

        comment = Gallery_Comment.objects.first()
        report_cnt = comment.report_cnt
        user = User.objects.first()
        report_comment(type=1, comment_id=comment.id, user_id=user.id)
        comment = Gallery_Comment.objects.get(id=comment.id)
        assert comment.report_user.contains(user)
        assert comment.report_cnt == report_cnt + 1

        comment = Photo_Comment.objects.first()
        report_cnt = comment.report_cnt
        user = User.objects.first()
        report_comment(type=2, comment_id=comment.id, user_id=user.id)
        comment = Photo_Comment.objects.get(id=comment.id)
        assert not comment.report_user.contains(user)
        assert comment.report_cnt == report_cnt - 1

        comment = Gallery_Comment.objects.first()
        report_cnt = comment.report_cnt
        user = User.objects.first()
        report_comment(type=3, comment_id=comment.id, user_id=user.id)
        comment = Gallery_Comment.objects.get(id=comment.id)
        assert not comment.report_user.contains(user)
        assert comment.report_cnt == report_cnt - 1

        try:
            report_comment(type=0, comment_id=-1, user_id=-1)
            assert False
        except:
            pass

    def test_set_all(self):
        photo = Photo.objects.first()
        photo_dict = get_photo(photo.id)
        photo_dict["user"] = photo_dict["user"]["id"]
        photo_dict["pub_date"] = photo.pub_date
        assert photo_set_all(photo.id, photo_dict)

    def test_others(self):
        try:
            user_login(None, -1, -1)
        except:
            pass
        try:
            ban_user(-1)
        except:
            pass
        try:
            photo_add_tags(-1, None)
        except:
            pass
        try:
            photo_change_tags(-1, None)
        except:
            pass
        try:
            photo_set_all(-1, {})
        except:
            pass
        try:
            photo = Photo.objects.first()
            delete_photo(photo.id)
        except:
            pass
        try:
            delete_photo(2)
        except:
            pass
        try:
            set_group_id(-1)
        except:
            pass
        try:
            remove_photo_from_gallery(-1, -1)
        except:
            pass
        try:
            gallery_add_tags(-1, [])
        except:
            pass
        try:
            gallery_add_photo(-1, -1)
        except:
            pass
        try:
            change_gallery_title(-1, 'aefie')
        except:
            pass
        try:
            change_gallery_intro(-1, -1)
        except:
            pass
        try:
            kill_user(-1)
        except:
            pass
        try:
            is_killed(-1)            
        except:
            pass
        try:
            unban_user(-1)            
        except:
            pass
        try:
            photo_liked(-1, -1)            
        except:
            pass
        try:
            gallery_liked(-1, -1)            
        except:
            pass
        try:
            photo_comment_liked(-1)            
        except:
            pass
        try:
            gallery_comment_liked(-1)            
        except:
            pass
        try:
            gallery_comment_reported(-1, -1)            
        except:
            pass
       
        
        

if __name__ == "__main__":
    modelTest = ModelTest()
    modelTest.setUp()
