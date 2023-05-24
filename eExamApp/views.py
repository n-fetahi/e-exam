from django.shortcuts import render
from django.http import HttpResponse
from eExamApp.models import *
import simplejson as json
from django.shortcuts import redirect

# Create your views here.

def index(request):
     return render(request,'eExamApp\cover.html')

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
                    return render(request,'eExamApp\login.html',{'teacher_error':'رجاءً قم بملء جميع الحقول'})
                
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
                        return redirect(route_page)
                
                elif not check_ID and not check_password:
                    return render(request,'eExamApp\login.html',{error_messages[0]:error_messages[1],
                                                                })
                elif not check_ID:
                    return render(request,'eExamApp\login.html',{error_messages[0]:error_messages[2]})
                elif not check_password:
                    return render(request,'eExamApp\login.html',{error_messages[0]:error_messages[3]})
        else:
            return render(request,'eExamApp\login.html',{'check':False})

class Teacher_Views:     
    
    def teacher_home(request):
        if 'm' in request.GET:
            if request.GET['m'] == '2':
                 return render(request,'eExamApp\\teacher\index.html',{'students':Student.objects.all(),
                                                                    'view':'students'})

        return render(request,'eExamApp\\teacher\index.html',{'view':'dashboard',
                                                                'models':Exam_Models.objects.all()
                                                                })

    def model(request):

#------------------------------------- Processes within the model--------------------------------------
        if 'q' in request.GET:
        
#---------------------------------------- Add question --------------------------------------------
            if request.GET['q'] =='add':
                options=[]
                request_items=request.POST
                if request_items['question_text']!=Exam_Models_Questions.objects.last().question_text:
                    for i in range(1,len(request_items)-2):
                        options.append(request_items['op%d' %i])
                    question=Exam_Models_Questions()
                    question.question_text=request_items['question_text']
                    question.answer_number=request_items['inlineRadioOptions']
                    question.options=json.dumps(options)
                    question.model_name=Exam_Models.objects.last()
                    question.save()

#--------------------------------- View confirmation message delete question -----------------------
            elif request.GET['q'] =='m_delete':
                    return render(request,'eExamApp\\teacher\questions.html',
                                {'model':'#deletModal',
                                'id':request.GET['id'],
                                'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())})
            
 #----------------------------------------- Delete question ---------------------------------------------
            elif request.GET['q'] =='delete':
                Exam_Models_Questions.objects.filter(id=request.GET['id']).delete()

 #----------------------------------------- View the form for editing a question ---------------------------------------------
            elif request.GET['q'] =='s_edit':
                options=[]
                editting_field=Exam_Models_Questions.objects.filter(id=request.GET['id'])
                jsonDec = json.decoder.JSONDecoder()
                for i in Exam_Models_Questions.objects.filter(id=request.GET['id']):
                    options.append(jsonDec.decode(i.options))
                # return HttpResponse(options[0])
                return render(request,'eExamApp\\teacher\questions.html',
                            {'model':'#editModal',
                            'id':request.GET['id'],
                            'editting_field':editting_field,
                            'options':options[0],
                            'answer':range(len(options[0])),
                            'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())
                            })
            elif request.GET['q'] =='edit':
                options=[]
                request_items=request.POST
                for i in range(1,len(request_items)-2):
                        options.append(request_items['op%d' %i])
                
                specific_question=Exam_Models_Questions.objects.get(id=str(request.GET['id']))
                
                specific_question.question_text=request_items['question_text']
                specific_question.answer_number=request_items['inlineRadioOptions']

                specific_question.options=json.dumps(options)
                specific_question.model_name=Exam_Models.objects.last()
                specific_question.save()
                return render(request,'eExamApp\\teacher\questions.html',
                                        {
                                        'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())
                                        })                 
                            
            
                

#--------------------------------- Add new Model --------------------------------------------------------
        else:    
            name=request.POST['name']
            min=request.POST['min']
            hour=request.POST['hour']

            if name!=Exam_Models.objects.last().name:
                model_name=Exam_Models()
                model_name.name=name
                model_name.exam_duration=str(hour)+':'+str(min)
                model_name.save()
        return render(request,'eExamApp\\teacher\questions.html',{'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())})



class Student_Views:

    
    def student_home(request):
        
        if 'm' in request.GET:
            if request.GET['m'] == '2':
                    return render(request,'eExamApp\student\index.html',
                                            {
                                                 'view':'coming_examinations',

                                            })

            if request.GET['m'] == '3':
                    return render(request,'eExamApp\student\index.html',
                                            {
                                                 'view':'previous_examinations',

                                            })
        return render(request,'eExamApp\student\index.html',
                                {
                                    'view':'current_examinations',

                                 })


    def exam(request):
         return render(request,'eExamApp\student\exam.html')