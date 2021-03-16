from django.test import TestCase
from django.utils import timezone

from article.forms import AddCategoryForm
from article.forms import AddTagForm
from article.forms import PrepareArticleForm
from article.forms import PrePostArticleForm
from article.models import Article
from article.models import ArticleCategory
from article.models import Tag


class PrepareArticleFormTest(TestCase):
    def setUp(self) -> None:
        self.category = ArticleCategory.objects.create(name="python")

    def test_valid_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
        }

        self.assertEqual(Article.objects.count(), 0)
        form = PrepareArticleForm(data)
        self.assertTrue(form.is_valid())

    def test_not_valid_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
        }

        error_datas = {
            "title": "",
            "summary": "",
            "publish_date": "1999/09/09",
            "category": "python",
        }
        for key, value in error_datas.items():
            error_data = data.copy()
            error_data[key] = value
            form = PrepareArticleForm(error_data)
            self.assertFalse(form.is_valid())

        past_data = data.copy()
        past_data["publish_date"] = timezone.now() + timezone.timedelta(days=-1)
        form = PrepareArticleForm(past_data)
        self.assertFalse(form.is_valid())


class AddCategoryFormTest(TestCase):
    def setUp(self) -> None:
        data = {"name": "python"}
        ArticleCategory.objects.create(**data)

    def test_add_category_form_success(self):
        data = {"name": "django"}
        form = AddCategoryForm(data)
        self.assertTrue(form.is_valid())

    def test_add_category_form_error(self):
        data = {"name": ""}
        form = AddCategoryForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"][0], "このフィールドは必須です。")

        data = {"name": "python"}
        form = AddCategoryForm(data)
        self.assertFalse(form.is_valid())


class AddTagFormTest(TestCase):
    def setUp(self) -> None:
        data = {"name": "python"}
        self.tag = Tag.objects.create(**data)

    def test_valid_form(self):
        data = {"name": "php"}
        form = AddTagForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_not_unique_name(self):
        data = {"name": "python"}
        form = AddTagForm(data)
        self.assertFalse(form.is_valid())


class PrePostArticleFormTest(TestCase):
    def setUp(self) -> None:
        self.category = ArticleCategory.objects.create(name="python")
        self.tag = Tag.objects.create(name="php")

    def test_valid_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
            "tag": [self.tag.id],
        }

        form = PrePostArticleForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_past_article_error(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "category": self.category,
        }

        form = PrePostArticleForm(data)
        self.assertFalse(form.is_valid())

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
            form = PrePostArticleForm(error_data)
            self.assertFalse(form.is_valid())

        past_data = data.copy()
        past_data["publish_date"] = timezone.now() + timezone.timedelta(days=-1)
        form = PrePostArticleForm(past_data)
        self.assertFalse(form.is_valid())
