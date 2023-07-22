from django.urls import path
from eExamApp import views,teacher_views,admin_views,student_views

urlpatterns = [
    #--------------------------Teacher URLs-----------------------------------------
    path('', views.index,name='cover'),

    path('teacher_login/', teacher_views.teacher_login,name='teacher_login'),
    path('teacher_home/', teacher_views.teacher_home,name='teacher_home'),
    path('model/', teacher_views.model_question,name='model'),
    path('new_model/', teacher_views.new_model,name='new_model'),
    path('add_model_questions/', teacher_views.add_model_questions,name='add_model_questions'),
    path('edit_model_questions/', teacher_views.edit_model_questions,name='edit_model_questions'),
    path('edit_model_questions/upload_model/', teacher_views.upload_model,name='upload_model'),
    path('edit_model_questions/cancel_model/', teacher_views.cancel_model,name='cancel_model'),
    path('delete_model/', teacher_views.delete_model,name='delete_model'),



    #--------------------------Students URLs-----------------------------------------
    path('student_home/', student_views.student_home,name='student_home'),
    path('student_home/exam/', student_views.exam,name='exam'),
    path('lecture/', student_views.lecture,name='lecture'),
    path('student_home/result/', student_views.result,name='result'),
    path('student_login/', student_views.student_login,name='student_login'),




    #--------------------------Admin URLs-----------------------------------------
    path('admin_home/',admin_views.admin_home,name='admin_home'),
    path('teacher_decisions/',admin_views.teacher_decisions,name='teacher_decisions'),
    path('decision_models/',admin_views.decision_models,name='decision_models'),
    path('result_students/',admin_views.result_students,name='result_students'),
    path('model_success/',admin_views.model_success,name='model_success'),
    path('admin_login/', admin_views.admin_login,name='admin_login'),



]
