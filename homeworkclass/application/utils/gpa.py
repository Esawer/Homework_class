def gpa_count(gpa_list) -> float:
    r = 0.0
    weighted_grades_num = 0

    if gpa_list:
        for i in gpa_list:
            weighted_grades_num += i.homework_number.grade_importance
            print(i.grade_number * i.homework_number.grade_importance)
            r += i.grade_number * i.homework_number.grade_importance

        return r / weighted_grades_num

    return 0.0
