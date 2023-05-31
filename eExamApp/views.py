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
                    route_page='teacher_home/?id='+str(user_ID)
                    
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

class Teacher_Views:     
    
    def teacher_home(request):
        # return HttpResponse(Approach.objects.filter(teatcher_ID=Teacher.objects.get(functional_ID='1'))[3].decision_ID)
        if 'm' in request.GET:
            if request.GET['m'] == '2':
                 return render(request,'teacher/index.html',{'students':Student.objects.all(),
                                                                    'view':'students'})
        

        level=[]
        # for i in Approach.objects.filter(teatcher_ID=Teacher.objects.get(functional_ID='1')[0].decision_ID):
        #                  
        # # return HttpResponse(Decision_And_Level.objects.filter(decision_ID='1'))
        # return HttpResponse()
        return render(request,'teacher/index.html',{'view':'dashboard',
                                                                'models':Exam_Models.objects.all(),
                                                                 'decisions':Approach.objects.filter(teatcher_ID=Teacher.objects.get(functional_ID='1')),
                                                                 'levels':Decision_And_Level.objects.filter(decision_ID=Approach.objects.filter(teatcher_ID=Teacher.objects.get(functional_ID='1'))[2].decision_ID),
                                                                 'specializations':Decision_And_Specialization.objects.filter(decision_ID='1')
                                                                 
                                                                })

    def model_question(request):

        if 'done' in request.GET:
             return HttpResponse('done')

#------------------------------------- Processes within the model--------------------------------------
        if 'q' in request.GET:
        

#--------------------------------- View confirmation message delete question -----------------------
            if request.GET['q'] =='m_delete':
                    return render(request,'teacher/questions.html',
                                {'model':'#deletModal',
                                'id':request.GET['id'],
                                'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())})
            
 #----------------------------------------- Delete question ---------------------------------------------
            elif request.GET['q'] =='delete':
                Exam_Models_Questions.objects.filter(id=request.GET['id']).delete()


              
                        
                
        return render(request,'teacher/questions.html',{'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())})

    def new_model(request):
        if(request.method =='POST'):
            name=request.POST['name']
            duration=request.POST['duration']

            if name== '' :
                return render(request,'teacher/new_model.html',{'model_error':'رجاءً قم بإدخال اسم النموذج'})
        
                 
            
            else:
                if not Exam_Models.objects.filter(name=name).exists():
                    model_name=Exam_Models()
                    model_name.name=name
                    model_name.exam_duration=duration
                    model_name.save()
                    return redirect('model')
                
                else:
                    return render(request,'teacher/new_model.html',{'model_error':'إسم النموذج موجود من قبل'})

                 
        return render(request,'teacher/new_model.html', { }
                      )

    def edit_model_questions(request):
        options=[]
        question=Exam_Models_Questions.objects.get(id=request.GET['id'])
        if request.method == 'POST':
            request_items=request.POST
            for i in range(1,len(request_items)-2):
                options.append(request_items['op%d' %i])
            question.question_text=request_items['question_text']
            question.answer_number=request_items['inlineRadioOptions']

            question.options=json.dumps(options)
            question.model_name=Exam_Models.objects.last()
            question.save()
            return render(request,'teacher/questions.html',
                                        {
                                        'questions':Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last())
                                        })  
            
              
 #--------------------------- View the form for editing a question ---------------------------------------------

        else:               
            jsonDec = json.decoder.JSONDecoder()
            for i in Exam_Models_Questions.objects.filter(id=request.GET['id']):
                options.append(jsonDec.decode(i.options))
            
            # return HttpResponse(len(options[0]))
            return render(request,'teacher/edit_model_questions.html',
                          {
                            'options':options[0],
                            'question_text':question.question_text,
                            'answer_number':question.answer_number,
                            'id':request.GET['id']
                          })
    
    def add_model_questions(request):
        if request.method== 'POST':
                    request_items=request.POST
                    question_text=request_items['question_text']
                    answer_number=request_items['inlineRadioOptions']
                    options=[]
                    if not Exam_Models_Questions.objects.filter(question_text=request_items['question_text']).exists():
                        for i in range(1,len(request_items)-2):
                            if request_items['op%d' %i] != '':
                                options.append(request_items['op%d' %i])
                        if question_text == '' or len(options) ==0 :
                            return render(request,'teacher/add_model_questions.html',{'error':'رجاءً قم بملء جميع الحقول'})
                        elif len(options) <2:
                            return render(request,'teacher/add_model_questions.html',{'error':'يجب ألا يقل عدد الخيارات عن 2',
                                                                                      'options':options,
                                                                                      'question_text':question_text
                                                                                      })
                        else:
                            question=Exam_Models_Questions()
                            question.question_text=question_text
                            question.answer_number=answer_number
                            question.options=json.dumps(options)
                            question.model_name=Exam_Models.objects.last()
                            question.save()
                            return redirect('model')
                             
                    else:
                        return render(request,'teacher/add_model_questions.html',{'error':'هذا السؤال موجود مسبقاً'})

                        

        return render(request,'teacher/add_model_questions.html')
         

class Student_Views:

    
    def student_home(request):
        
        if 'm' in request.GET:
            if request.GET['m'] == '2':
                    return render(request,'student/index.html',
                                            {
                                                 'view':'coming_examinations',

                                            })

            if request.GET['m'] == '3':
                    return render(request,'student/index.html',
                                            {
                                                 'view':'previous_examinations',

                                            })
        return render(request,'student/index.html',
                                {
                                    'view':'current_examinations',

                                 })


    def exam(request):
         return render(request,'student/exam.html')