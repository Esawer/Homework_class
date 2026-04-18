from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home_view, name="home"),
    path("logout/", views.user_logout, name="logout"),
    path("authorization/", views.auth_view, name="auth"),
    path("class/", views.classes_view, name="classes"),
    path("class/<int:class_id>/", views.homeworks_view, name="homeworks"),
    path("options/<int:class_id>/", views.owner_options_view, name="owner_options"),
    path(
        "options/<int:class_id>/<int:homework_id>/<int:student_id>/",
        views.teacher_grading_view,
        name="teacher_grading",
    ),
    path(
        "homework/<int:class_id>/<int:homework_id>/",
        views.homeworkpage_view,
        name="homework",
    ),
    path(
        "homework/<int:class_id>/<int:homework_id>/grade/",
        views.homeworkgrade_view,
        name="grade_homework",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
