from django.urls import path
from eExamApp import views

urlpatterns = [
    #--------------------------Teacher URLs-----------------------------------------
    path('', views.index,name='cover'),

    path('login/', views.login,name='login'),
    path('teacher_home/', views.Teacher_Views.teacher_home,name='teacher_home'),
    path('model/', views.Teacher_Views.model_question,name='model'),
    path('new_model/', views.Teacher_Views.new_model,name='new_model'),
    path('add_model_questions/', views.Teacher_Views.add_model_questions,name='add_model_questions'),
    path('edit_model_questions/', views.Teacher_Views.edit_model_questions,name='edit_model_questions'),
   
    #--------------------------Students URLs-----------------------------------------
    path('student_home/', views.Student_Views.student_home,name='student_home'),
    path('exam/', views.Student_Views.exam,name='exam'),

]
