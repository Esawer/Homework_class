from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import *
from .utils import code_generator, gpa
import datetime as dt
from django.db.models import Q


@unauthenticated_user
def home_view(request):
    return render(request, "application/index.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


@unauthenticated_user
@never_cache
def auth_view(request):

    form = CreateUser()
    if request.method == "POST":
        if request.POST.get("login"):
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                response = HttpResponse(status=204)
                response["HX-Redirect"] = ""
                return response
            else:
                response = HttpResponse(status=204)
                response["HX-Redirect"] = ""
                return response

        elif request.POST.get("register"):
            form = CreateUser(request.POST)

            if form.is_valid():

                user_class = form.save()
                UserClass.objects.create(
                    username=user_class.username,
                    name=form.cleaned_data.get("first_name"),
                    surname=form.cleaned_data.get("last_name"),
                    user=user_class,
                )
                response = HttpResponse(status=204)
                response["HX-Redirect"] = ""
                return response
            else:
                response = HttpResponse(status=204)
                response["HX-Redirect"] = ""
                return response

    context = {"form": form}
    return render(request, "application/auth.html", context)


@login_required
def classes_view(request):
    classes = request.user.userclass.class_member.all()
    user_type = request.user.userclass.user_type
    student_gpa = 0
    num_of_students = UserClass.objects.filter(
        class_member__in=SchoolClass.objects.filter(owner=request.user.userclass),
        user_type="Student",
    ).count()

    grade_assignments = Grade.objects.filter(
        Q(
            homework_number__upload_after_time=True,
        )
        | Q(
            homework_number__time_to_end__gte=dt.date.today(),
            homework_number__upload_after_time=False,
        ),
        grade_number=None,
        homework_number__class_number__in=request.user.userclass.class_member.all(),
    ).count()

    pending_assignments = Grade.objects.filter(
        Q(homework_number__upload_after_time=True)
        | Q(
            homework_number__time_to_end__gte=dt.date.today(),
            homework_number__upload_after_time=False,
        ),
        grade_number=None,
        student=request.user.userclass,
    ).count()

    if request.user.userclass.user_type == "Student":
        student_gpa = gpa.gpa_count(
            Grade.objects.filter(
                student=request.user.userclass,
                grade_number__isnull=False,
            )
        )

    if request.method == "POST":
        if request.POST.get("class_name"):
            class_code = code_generator.generate_code()

            new_class = SchoolClass.objects.create(
                name=request.POST.get("class_name"),
                owner=UserClass.objects.get(user=request.user),
                class_code=class_code,
            )

            request.user.userclass.class_member.add(new_class)
            return redirect("classes")

        elif request.POST.get("class_code"):
            c_code = request.POST.get("class_code")

            try:
                hw_class = SchoolClass.objects.get(
                    class_code=request.POST.get("class_code")
                )
                if not hw_class.locked:
                    request.user.userclass.class_member.add(hw_class)
                    if request.user.userclass.user_type == "Student":
                        homeworks = SchoolHomework.objects.filter(class_number=hw_class)
                        hw_check = Grade.objects.filter(
                            student=request.user.userclass,
                            homework_number__in=homeworks,
                        )

                        if not hw_check.exists():
                            grades_to_assign = [
                                Grade(student=request.user.userclass, homework_number=i)
                                for i in homeworks
                            ]
                            Grade.objects.bulk_create(grades_to_assign)
                return redirect("classes")
            except:
                return redirect("classes")

    context = {
        "classes": classes,
        "user_type": user_type,
        "num_of_students": num_of_students,
        "grade_assignments": grade_assignments,
        "pending_assignments": pending_assignments,
        "student_gpa": student_gpa,
    }
    return render(request, "application/classes.html", context)


@login_required
def homeworks_view(request, class_id):
    user_type = request.user.userclass.user_type
    assigments = SchoolHomework.objects.filter(class_number=class_id)
    class_name = SchoolClass.objects.get(id=class_id)
    locked_value = class_name.locked
    class_owner = class_name.owner == request.user.userclass
    students_in = UserClass.objects.filter(user_type="Student", class_member=class_name)
    form = AssignmentCreation()
    student_gpa = 0

    pending_assignments = Grade.objects.filter(
        Q(
            homework_number__upload_after_time=True,
        )
        | Q(
            homework_number__time_to_end__gte=dt.date.today(),
            homework_number__upload_after_time=False,
        ),
        homework_number__in=assigments,
        student=request.user.userclass,
        grade_number=None,
    ).count()

    if request.user.userclass.user_type == "Student":
        student_gpa = gpa.gpa_count(
            Grade.objects.filter(
                student=request.user.userclass,
                grade_number__isnull=False,
                homework_number__in=assigments,
            )
        )

    if request.method == "POST":
        if request.POST.get("add_assignment") and not locked_value:

            form = AssignmentCreation(request.POST)
            if form.is_valid():
                SchoolHomework.objects.create(
                    name=form.cleaned_data["name"],
                    grade_importance=form.cleaned_data["grade_importance"],
                    description=form.cleaned_data["description"],
                    time_to_end=form.cleaned_data["time_to_end"],
                    upload_after_time=form.cleaned_data["upload_after_time"],
                    teacher=request.user.userclass,
                    class_number=class_name,
                )

            for i in students_in:

                Grade.objects.create(
                    homework_number=SchoolHomework.objects.get(
                        name=form.cleaned_data["name"],
                        grade_importance=form.cleaned_data["grade_importance"],
                        description=form.cleaned_data["description"],
                        time_to_end=form.cleaned_data["time_to_end"],
                        upload_after_time=form.cleaned_data["upload_after_time"],
                        teacher=request.user.userclass,
                        class_number=class_name,
                    ),
                    student=i,
                )

            return redirect("homeworks", class_id)

    context = {
        "assigments": assigments,
        "class_id": class_id,
        "user_type": user_type,
        "locked_value": locked_value,
        "class_owner": class_owner,
        "class_name": class_name,
        "form": form,
        "pending_assignments": pending_assignments,
        "student_gpa": student_gpa,
    }
    return render(request, "application/homeworks.html", context)


@allowed_users("Student")
@login_required
def homeworkpage_view(request, class_id, homework_id):
    form = UploadFile()
    class_name = SchoolClass.objects.get(id=class_id)
    assignment = SchoolHomework.objects.get(id=homework_id)
    user_type = request.user.userclass.user_type
    locked_value = SchoolClass.objects.get(id=class_id).locked
    student_grade = Grade.objects.get(
        student=request.user.userclass, homework_number=assignment
    )
    send_permission = True if student_grade.grade_number is None and (assignment.upload_after_time or assignment.time_to_end >= dt.date.today()) else False  # type: ignore
    change_file = True if send_permission and student_grade.homework_href else False

    if request.method == "POST":
        if request.POST.get("homework_submit"):
            form = UploadFile(request.POST, request.FILES)

            if form.is_valid():
                grade = Grade.objects.get(
                    homework_number=assignment, student=request.user.userclass
                )

                grade.homework_href = request.FILES["uploaded_file"]
                grade.save()

                response = HttpResponse(status=204)
                response["HX-Redirect"] = "/class/"
                return response

    context = {
        "assignment": assignment,
        "class_name": class_name,
        "user_type": user_type,
        "form": form,
        "send_permission": send_permission,
        "change_file": change_file,
        "locked_value": locked_value,
        "student_grade": student_grade,
    }
    return render(request, "application/homework_page.html", context)


@allowed_users("Teacher")
@login_required
def homeworkgrade_view(request, class_id, homework_id):
    assignment = SchoolHomework.objects.get(id=homework_id)
    class_name = SchoolClass.objects.get(id=class_id)
    locked_value = SchoolClass.objects.get(id=class_id).locked
    class_owner = class_name.owner == request.user.userclass
    submissions = Grade.objects.filter(homework_number=assignment)

    grade_student = False
    student_id = 0
    assignment_to_grade = 0
    assignment_send = False
    grade_assigned = 0

    form_inital_data = {
        "name": assignment.name,
        "description": assignment.description,
        "time_to_end": assignment.time_to_end,
        "grade_importance": assignment.grade_importance,
        "upload_after_time": assignment.upload_after_time,
    }

    form = AssignmentCreation(initial=form_inital_data)

    if request.method == "GET" and locked_value == False:
        student_id = request.GET.get("student_id")

        if student_id:
            student_to_grade = UserClass.objects.get(id=student_id)

            if Grade.objects.filter(
                student=student_to_grade, homework_number=assignment
            ).exists():
                assignment_to_grade = Grade.objects.get(
                    student=student_to_grade, homework_number=assignment
                )
                assignment_send = True
            else:
                Grade.objects.create(
                    student=student_to_grade,
                    homework_href=None,
                    homework_number=assignment,
                )
                assignment_to_grade = Grade.objects.get(
                    student=student_to_grade, homework_number=assignment
                )
            grade_student = True

    if request.method == "POST" and locked_value == False:
        if request.POST.get("edit_assignment"):
            form = AssignmentCreation(request.POST)
            if form.is_valid():
                SchoolHomework.objects.filter(id=homework_id).update(
                    name=form.cleaned_data["name"],
                    grade_importance=form.cleaned_data["grade_importance"],
                    description=form.cleaned_data["description"],
                    time_to_end=form.cleaned_data["time_to_end"],
                    upload_after_time=form.cleaned_data["upload_after_time"],
                )
                return redirect("grade_homework", class_id, homework_id)

        elif request.POST.get("delete_assignment"):
            Grade.objects.filter(homework_number=assignment).delete()
            SchoolHomework.objects.get(id=homework_id).delete()

            return redirect("homeworks", class_id)

        elif request.POST.get("submit_grade"):
            grade_assigned = request.POST.get("submit_grade")

            Grade.objects.filter(
                student=UserClass.objects.get(id=grade_assigned),
                homework_number=assignment,
            ).update(grade_number=request.POST.get("grade"))

    context = {
        "assignment": assignment,
        "class_name": class_name,
        "submissions": submissions,
        "grade_student": grade_student,
        "assignment_to_grade": assignment_to_grade,
        "assignment_send": assignment_send,
        "locked_value": locked_value,
        "form": form,
    }
    return render(request, "application/grade_homework.html", context)


@allowed_users("Teacher")
@login_required
def owner_options_view(reqeuest, class_id):
    class_name = SchoolClass.objects.get(id=class_id)
    locked_value = class_name.locked
    class_owner = class_name.owner

    if reqeuest.method == "POST" and class_owner:
        if reqeuest.POST.get("change_class_name") and not locked_value:
            SchoolClass.objects.filter(id=class_id).update(
                name=reqeuest.POST.get("change_class_name")
            )
        elif reqeuest.POST.get("delete_class") and not locked_value:
            class_name.delete()
            response = HttpResponse(status=204)
            response["HX-Redirect"] = "/class/"
            return response

        elif reqeuest.POST.get("lock_class"):
            SchoolClass.objects.filter(id=class_id).update(locked=not locked_value)

        response = HttpResponse(status=204)
        response["HX-Redirect"] = ""
        return response

    context = {
        "class_name": class_name,
        "locked_value": locked_value,
    }
    return render(reqeuest, "application/owner_options.html", context)


@allowed_users("Teacher")
def teacher_grading_view(request, class_id, homework_id, student_id):
    class_name = SchoolClass.objects.get(id=class_id)
    assignment = SchoolHomework.objects.get(id=homework_id)
    assignment_to_grade = Grade.objects.get(
        homework_number=assignment, student=UserClass.objects.get(id=student_id)
    )

    if request.method == "POST":
        if request.POST.get("submit_grade"):
            Grade.objects.filter(
                homework_number=assignment,
                student=UserClass.objects.get(id=student_id),
            ).update(grade_number=request.POST.get("submit_grade"))
            return redirect("grade_homework", class_id, homework_id)

    context = {
        "class_name": class_name,
        "assignment": assignment,
        "assignment_to_grade": assignment_to_grade,
    }
    return render(request, "application/teacher_grading.html", context)
