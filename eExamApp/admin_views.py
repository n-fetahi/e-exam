from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from eExamApp.models import *
import simplejson as json
from django.shortcuts import redirect
from django.contrib import messages


def admin_login(request):
        #---------------------------- Ensure that data is sent in the student or teacher form-----------------
        if request.method =='POST':
                user_ID=request.POST['ID']
                password=request.POST['password']
                check_ID=False
                check_password=False
                error_messages=[]
                route_page=''

                if user_ID == '' or password == '':
                    return render(request,'admin_login.html',{'teacher_error':'رجاءً قم بملء جميع الحقول'})
                error_messages.append('teacher_error')   
                error_messages.append('كلمة المرور والرقم الوظيفي ليسا صحيحين')   
                error_messages.append('الرقم الوظيفي ليس صحيحاً')   
                error_messages.append('كلمة المرور  ليست صحيحة')
                route_page='admin_home'
                    
                for admin in Admin.objects.all():
                        if str(user_ID)==str(admin.functional_ID):
                            check_ID=True
                        if str(password)==str(admin.password):
                            check_password=True
                
                if check_ID and check_password:
                        re=Approach.objects.all()
                        # return HttpResponse(re)
                        request.session['admin_ID'] = user_ID
                        request.session['password'] = password
                        return redirect(route_page)
                
                elif not check_ID and not check_password:
                    return render(request,'admin_login.html',{error_messages[0]:error_messages[1],
                                                                })
                elif not check_ID:
                    return render(request,'admin_login.html',{error_messages[0]:error_messages[2]})
                elif not check_password:
                    return render(request,'admin_login.html',{error_messages[0]:error_messages[3]})
        
        else:
                     
            return render(request,'admin_login.html',{'check':False})



def teacher_decisions(request):
    return render(request,'system_admin/teachers/teacher_decisions.html')

def decision_models(request):
    return render(request,'system_admin/teachers/decision_models.html') 

def result_students(request):
    return render(request,'system_admin/teachers/students.html',{
             'students':Student.objects.all()
        }) 

def admin_home(request):
    if "admin_ID" not in request.session:
        return HttpResponse('<div class="alert alert-danger d-flex align-items-center" role="alert">' +
                            '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>' +
                            '<div>قم بتسجيل الدخول أولاً</div></div>')

    if 'm' in request.GET:
            if request.GET['m'] == '2':
                    return render(request,'system_admin/index.html',
                                            {
                                                 'view':'teachers_names',
                                            })


    return render(request,'system_admin/index.html',{
         'models':Exam_Models.objects.filter(model_state=1)
    }) 

def model_success(request):
    time =str(request.POST['time'])+':00'
    # return HttpResponse()
    model=Exam_Models.objects.get(id=request.GET['id'])
    exam_dateTime=request.POST['date']+' '+time
    model.exam_dateTime=exam_dateTime
    model.model_state=2
    model.save()

    return  redirect('admin_home')