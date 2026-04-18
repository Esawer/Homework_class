from django.db import models
from django.contrib.auth.models import User


class UserClass(models.Model):
    USER_TYPES = {
        "Student": "Student",
        "Teacher": "Teacher",
    }

    username = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    surname = models.CharField(max_length=150, null=True, blank=True)
    class_member = models.ManyToManyField("SchoolClass", null=True, blank=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=True)
    user_type = models.CharField(max_length=7, choices=USER_TYPES, default="Student")  # type: ignore

    def __str__(self):
        return self.username


class SchoolClass(models.Model):  # particular class of many homeworks
    name = models.CharField(max_length=100, blank=True)
    class_code = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(UserClass, on_delete=models.CASCADE, null=True)
    locked = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.name


class SchoolHomework(models.Model):
    name = models.CharField(max_length=100, blank=True)
    grade_importance = models.IntegerField(null=True)
    description = models.TextField(default="", blank=True)
    teacher = models.ForeignKey(UserClass, on_delete=models.SET_NULL, null=True)
    time_to_end = models.DateField(null=True)
    upload_after_time = models.BooleanField(null=True, default=True, blank=True)
    class_number = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade_number = models.IntegerField(blank=True, null=True)
    homework_href = models.FileField(blank=True)
    homework_number = models.ForeignKey(
        SchoolHomework, on_delete=models.CASCADE, null=True
    )
    student = models.ForeignKey(
        UserClass, on_delete=models.CASCADE, null=True, related_name="student"
    )

    def __str__(self):
        return f"{self.homework_number}_{self.student}"
