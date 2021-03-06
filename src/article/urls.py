from django.urls import path

from .views import views_login
from .views import views_user

app_name = "article"
urlpatterns = [
    path("index/", views_user.IndexView.as_view(), name="index"),
    path("<int:article_id>/detail/", views_user.DetailView.as_view(), name="detail"),
    path(
        "index/categories/<str:category>/",
        views_user.CategoryView.as_view(),
        name="category",
    ),
    path("index/tags/<str:tag>/", views_user.TagView.as_view(), name="tag",),
    path("prepare/", views_login.PrepareArticleView.as_view(), name="prepare_post"),
    path("post/", views_login.PostArticleView.as_view(), name="post"),
    path("login/", views_login.LoginView.as_view(), name="login"),
    path("logout/", views_login.LogoutView.as_view(), name="logout"),
    path("login/index/", views_login.IndexView.as_view(), name="login_index"),
    path(
        "login/<int:article_id>/detail/",
        views_login.DetailView.as_view(),
        name="login_detail",
    ),
    path(
        "login/<int:article_id>/edit/",
        views_login.EditView.as_view(),
        name="login_edit",
    ),
    path(
        "login/<int:pk>/delete/",
        views_login.DeleteArticleView.as_view(),
        name="login_delete",
    ),
    path(
        "login/add-category/",
        views_login.AddCategoryView.as_view(),
        name="add_category",
    ),
    path("login/add-tag/", views_login.AddTagView.as_view(), name="add_tag"),
    path(
        "login/index/categories/<str:category>/",
        views_login.CategoryView.as_view(),
        name="login_category",
    ),
    path(
        "login/index/tag/<str:tag>/", views_login.TagView.as_view(), name="login_tag",
    ),
    path("login/setting/", views_login.SettingView.as_view(), name="setting",),
    path(
        "login/change-username",
        views_login.ChangeUsernameView.as_view(),
        name="change_username",
    ),
    path(
        "login/change-email",
        views_login.ChangeEmailView.as_view(),
        name="change_email",
    ),
    path(
        "login/change-password",
        views_login.ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("login/sign-up", views_login.SignUpView.as_view(), name="sign_up"),
]
