from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from eExamApp.models import *
import simplejson as json
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.

def index(request):
     return render(request,'cover.html')

def login(request):
        
#---------------------------- Ensure that data is sent in the student or teacher form-----------------
        if request.method =='POST':
                user_ID=request.POST['ID']
                password=request.POST['password']
                check_ID=False
                check_password=False
                error_messages=[]
                route_page=''

                if user_ID == '' or password == '':
                    return render(request,'login.html',{'teacher_error':'رجاءً قم بملء جميع الحقول'})
                
#---------------------------- Ensure that the transmission was from the teacher form-----------------                
                if request.GET['l'] == '0':  
                    error_messages.append('teacher_error')   
                    error_messages.append('كلمة المرور والرقم الوظيفي ليسا صحيحين')   
                    error_messages.append('الرقم الوظيفي ليس صحيحاً')   
                    error_messages.append('كلمة المرور  ليست صحيحة')
                    route_page='teacher_home'
                    
                    for teacher in Teacher.objects.all():
                        if str(user_ID)==str(teacher.functional_ID):
                            check_ID=True
                        if str(password)==str(teacher.password):
                            check_password=True

#---------------------------- Ensure that the transmission was from the student form-----------------
                elif request.GET['l'] == "1":
                    error_messages.append('student_error')   
                    error_messages.append('كلمة المرور والرقم الأكاديمي ليسا صحيحين')   
                    error_messages.append('الرقم الأكاديمي ليس صحيحاً')   
                    error_messages.append('كلمة المرور  ليست صحيحة') 
                    route_page='student_home'
                    for student in Student.objects.all():
                        if str(user_ID)==str(student.academic_ID):
                            check_ID=True
                        if str(password)==str(student.password):
                            check_password=True
                     
                if check_ID and check_password:
                        re=Approach.objects.all()
                        # return HttpResponse(re)
                        return redirect(route_page)
                
                elif not check_ID and not check_password:
                    return render(request,'login.html',{error_messages[0]:error_messages[1],
                                                                })
                elif not check_ID:
                    return render(request,'login.html',{error_messages[0]:error_messages[2]})
                elif not check_password:
                    return render(request,'login.html',{error_messages[0]:error_messages[3]})
        else:
            return render(request,'login.html',{'check':False})




