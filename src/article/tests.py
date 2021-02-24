from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db import utils
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import PostArticleForm
from .models import Article
from .models import ArticleCategory


class ArticleCategoryTest(TestCase):
    def test_create_category(self):
        category = ArticleCategory.objects.create(category="python")
        self.assertEqual(category.category, "python")
        self.assertNotEqual(category.category, "Python")
        self.assertNotEqual(category.category, " python")
        with self.assertRaises(utils.IntegrityError):
            with transaction.atomic():
                ArticleCategory.objects.create(category="python")
            with transaction.atomic():
                ArticleCategory.objects.create(category="python")
        with self.assertRaises(utils.DataError):
            with transaction.atomic():
                ArticleCategory.objects.create(
                    category="aiueoaiueoaiueoaiueoa",
                )


class ArticleTest(TestCase):
    def test_create_article(self):
        c = ArticleCategory.objects.create(category="python")
        user = get_user_model()
        u = user.objects.create_user(email="test@test.com", password="test")
        article = Article.objects.create(
            author=u,
            title="python tour",
            summary="python is good",
            content="python is good lang",
            publish_date=timezone.now(),
            category=c,
        )
        self.assertEqual(article.author.email, u.email)
        self.assertEqual(article.title, "python tour")
        self.assertEqual(article.summary, "python is good")
        self.assertEqual(article.content, "python is good lang")
        self.assertEqual(article.category.category, c.category)
        with self.assertRaises(utils.DataError):
            with transaction.atomic():
                Article.objects.create(
                    author=u,
                    title="p" * 256,
                    summary="python is good",
                    content="python is good lang",
                    publish_date=timezone.now(),
                    category=c,
                )
        with self.assertRaises(utils.DataError):
            with transaction.atomic():
                Article.objects.create(
                    author=u,
                    title="p",
                    summary="p" * 256,
                    content="python is good lang",
                    publish_date=timezone.now(),
                    category=c,
                )


class UserManagersTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@test.com", password="test")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="test")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="test@test.com", password="test"
        )
        self.assertEqual(admin_user.email, "test@test.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class PostArticleFormTest(TestCase):
    def setUp(self) -> None:
        self.category = ArticleCategory.objects.create(category="python")

    def test_valid_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
        }

        form = PostArticleForm(data)
        self.assertTrue(form.is_valid())

    def test_not_valid_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
        }

        error_datas = {
            "title": "",
            "summary": "",
            "content": "",
            "publish_date": "1999/09/09",
            "category": "python",
        }
        for key, value in error_datas.items():
            error_data = data.copy()
            error_data[key] = value
            form = PostArticleForm(error_data)
            self.assertFalse(form.is_valid())

        past_data = data.copy()
        past_data["publish_date"] = timezone.now() + timezone.timedelta(days=-1)
        form = PostArticleForm(past_data)
        self.assertFalse(form.is_valid())


class LoginViewTests(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )

    def test_login_sucsess(self):
        response = self.client.post(
            "/article/login/", data={"email": "test@test.com", "password": "aiueoaiueo"}
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:index"))

    def test_login_error(self):
        response = self.client.post(
            "/article/login/",
            data={"email": "test@test.com", "password": "pythonpython"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Eメールアドレス または パスワードに誤りがあります.")

        response = self.client.post(
            "/article/login/",
            data={"email": "tete@tete.com", "password": "aiueoaiueo"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Eメールアドレス または パスワードに誤りがあります.")
