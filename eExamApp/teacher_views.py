from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from eExamApp.models import *
import simplejson as json
from django.shortcuts import redirect
from django.contrib import messages

def teacher_login(request):
        #---------------------------- Ensure that data is sent in the student or teacher form-----------------
        if request.method =='POST':
                user_ID=request.POST['ID']
                password=request.POST['password']
                check_ID=False
                check_password=False
                error_messages=[]
                route_page=''

                if user_ID == '' or password == '':
                    return render(request,'teacher_login.html',{'teacher_error':'رجاءً قم بملء جميع الحقول'})
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
                
                if check_ID and check_password:
                        re=Approach.objects.all()
                        # return HttpResponse(re)
                        request.session['teacher_ID'] = user_ID
                        request.session['password'] = password
                        return redirect(route_page)
                
                elif not check_ID and not check_password:
                    return render(request,'teacher_login.html',{error_messages[0]:error_messages[1],
                                                                })
                elif not check_ID:
                    return render(request,'teacher_login.html',{error_messages[0]:error_messages[2]})
                elif not check_password:
                    return render(request,'teacher_login.html',{error_messages[0]:error_messages[3]})
        
        else:
                     
            return render(request,'teacher_login.html',{'check':False})

def teacher_home(request):
        if "teacher_ID" not in request.session:
              return HttpResponse('<div class="alert alert-danger d-flex align-items-center" role="alert">'+
                     '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>'+
                     '<div>قم بتسجيل الدخول أولاً</div></div>')

        if 'm' in request.GET:
            if request.GET['m'] == '2':
                 return render(request,'teacher/index.html',{'students':Student.objects.all(),
                                                                    'view':'students'})
        decisions=Approach.objects.filter(teatcher_ID=Teacher.objects.get(functional_ID=request.session['teacher_ID']))
        levels=[]
        specializations=[]
        for decision in decisions:      
            for level in Decision_And_Level.objects.filter(decision_ID=decision.decision_ID):
                levels.append(level.level_ID)
            for specialization in Decision_And_Specialization.objects.filter(decision_ID=decision.decision_ID):
                specializations.append(specialization.specialization_ID)
        levels=list(set(levels))  
        specializations=list(set(specializations))  
        if  request.method == 'POST':
            decision_id=Decision.objects.get(decision_name=request.POST['decision']).id
            for level in Decision_And_Level.objects.filter(decision_ID=decision_id):
                 if str(level.level_ID) == request.POST['level']:
                    for specialization in Decision_And_Specialization.objects.filter(decision_ID=decision_id):
                         if str(specialization.specialization_ID) == request.POST['specialization']:
                            if Exam_Models.objects.filter(decision_ID=Decision.objects.get(decision_name=request.POST['decision']),teacher_ID=Teacher.objects.get(functional_ID='1')).count() == 0:
                            
                                return render(request,'teacher/index.html',{'view':'dashboard',
                                                                'decision':request.POST['decision'],
                                                                'level' : request.POST['level'],
                                                                'specialization':request.POST['specialization'],
                                                                 'decisions':decisions,
                                                                 'levels':levels,
                                                                 'specializations':specializations,
                                                                 'error':'لم يتم تضمين أي نموذج لهذا المقرر، قم بإنشاء نموذج جديد'
                                                                 
                                                                }) 
                            else:
                                 return render(request,'teacher/index.html',{'view':'dashboard',
                                                                                         'models':Exam_Models.objects.filter(
                                                                                decision_ID=Decision.objects.get(decision_name=request.POST['decision']),
                                                                                level_ID=Level.objects.get(level_name=request.POST['level']),
                                                                                specialization_ID=Specialization.objects.get(specialization_name=request.POST['specialization'])  ,
                                                                                teacher_ID=Teacher.objects.get(functional_ID='1')
                                                                              
                                                                                ),
                                                                'decision':request.POST['decision'],
                                                                'level' : request.POST['level'],
                                                                'specialization':request.POST['specialization'],
                                                                 'decisions':decisions,
                                                                 'levels':levels,
                                                                 'specializations':specializations,
                                                                
                                                                 
                                                                }) 
                                           
                      

            return render(request,'teacher/index.html',{'view':'dashboard',
                                                                 'decisions':decisions,
                                                                 'levels':levels,
                                                                 'specializations':specializations,
                                                                 'error':'رجاءً قم بإختيار "المستوى" و "التخصص" و "المقرر" بشكل صحيح'
                                                                })
            



        return render(request,'teacher/index.html',{'view':'dashboard',
                                                                 'decisions':decisions,
                                                                 'levels':levels,
                                                                 'specializations':specializations,
                                                                 'error':'لإنشاء نموذج أو إستعراضه قم باختيار التخصص والمستوى والمقرر الذي تدرسة ثم اضغط على "إستعراض النماذج"'
                                                                 
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
        if request.method =='POST':
            if 'name' in request.POST:
                name=request.POST['name']
                duration=request.POST['duration']

                if name== '' :
                    return render(request,'teacher/new_model.html',{'model_error':'رجاءً قم بإدخال اسم النموذج'})
        
            # elif 'level' in request.POST and 'specialization' in request.POST and 'decision' in request.POST:   
            
                else:
                  if not Exam_Models.objects.filter(name=name).exists():
                    model_name=Exam_Models()
                    model_name.name=name
                    model_name.exam_duration=duration
                    model_name.teacher_ID=Teacher.objects.get(functional_ID=request.session['teacher_ID'])
                    model_name.level_ID=Level.objects.get(level_name=request.POST['level'])
                    model_name.decision_ID=Decision.objects.get(decision_name=request.POST['decision'])
                    model_name.specialization_ID=Specialization.objects.get(specialization_name=request.POST['specialization'])   
                    model_name.save()
                    return redirect('model')
                
                  else:
                      return render(request,'teacher/new_model.html',{'model_error':'إسم النموذج موجود من قبل'})

        return render(request,'teacher/new_model.html', {
             'level': request.POST['level'],
             'decision': request.POST['decision'],
             'specialization': request.POST['specialization'],
         }
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
    
def delete_model(request):
    Exam_Models_Questions.objects.filter(model_name=Exam_Models.objects.last()).delete()
    Exam_Models.objects.last().delete()
    return redirect('teacher_home')


def upload_model(request):
        model=Exam_Models.objects.get(id=request.GET['id'])
        model.model_state=1
        model.save()
        return redirect('teacher_home')
    
def cancel_model(request):
        model=Exam_Models.objects.get(id=request.GET['id'])
        model.model_state=0
        model.save()
        return redirect('teacher_home')
        # return HttpResponse(model.)
  