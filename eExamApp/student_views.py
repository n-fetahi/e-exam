from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from eExamApp.models import *
import simplejson as json
from django.shortcuts import redirect
from django.contrib import messages
import random
from django.core.serializers import serialize

def student_login(request):
        list=[]
        s=serialize('json',Student.objects.all())
        jsonDec = json.decoder.JSONDecoder()
        d=jsonDec.decode(s)

        
        return JsonResponse({'json':d})
        #---------------------------- Ensure that data is sent in the student or teacher form-----------------
        if request.method =='POST':
              user_ID=request.POST['ID']
              password=request.POST['password']

              check_ID=False
              check_password=False
              error_messages=[]
              route_page=''

              if user_ID == '' or password == '':
                    return render(request,'student_login.html',{'teacher_error':'رجاءً قم بملء جميع الحقول'})
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
                        request.session['student_ID'] = user_ID
                        request.session['password'] = password
                        # return HttpResponse(re)
                        return redirect(route_page)

              elif not check_ID and not check_password:
                    return render(request,'student_login.html',{error_messages[0]:error_messages[1],
                                                                })
              elif not check_ID:
                    return render(request,'student_login.html',{error_messages[0]:error_messages[2]})
              elif not check_password:
                    return render(request,'student_login.html',{error_messages[0]:error_messages[3]})

        else:

            return render(request,'student_login.html',{'check':False})



def student_home(request):
        if "student_ID" not in request.session:
              return HttpResponse('<div class="alert alert-danger d-flex align-items-center" role="alert">'+
                     '<svg class="bi flex-shrink-0 me-2" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>'+
                     '<div>قم بتسجيل الدخول اولا</div></div>')

        if 'm' in request.GET:
            if request.GET['m'] == '2':
                    return render(request,'student/index.html',
                                            {
                                                 'view':'coming_examinations',

                                            })

            elif request.GET['m'] == '3':
                    return render(request,'student/index.html',
                                            {
                                                 'view':'previous_examinations',

                                            })
            elif request.GET['m'] == '4':
                    return render(request,'student/index.html',
                                            {
                                                 'view':'study_decision',

                                            })
        models=Exam_Models.objects.filter(model_state=2,)
        if models.count() == 0:
               return render(request,'student/index.html',{'message':'لا يوجد أي إختبارات جارية',
                                                    })
        else:
          model_random=random.choice(models)

          time_now=datetime.strptime(datetime.now().strftime('%d/%m/%Y %I:%M:%S'),'%d/%m/%Y %I:%M:%S')
          exam_time=datetime.strptime(model_random.exam_dateTime.strftime('%d/%m/%Y %I:%M:%S'),'%d/%m/%Y %I:%M:%S')
          if exam_time < time_now:
               #   return HttpResponse(model_random)
                 return render(request,'student/index.html',{'current_model':model_random,
                                                    })
          return render(request,'student/index.html',{'message':'لا يوجد أي إختبارات جارية',
                                                    })


def exam(request):
         questions_list=[]
         jsonDec = json.decoder.JSONDecoder()
         model=Exam_Models.objects.filter(name=request.POST['model']) 
         questions=Exam_Models_Questions.objects.filter(model_name=model[0])
         for i in questions:
                questions_list.append({
                       'id':i.id,
                       'option':jsonDec.decode(i.options),
                       'question_text':i.question_text,
                       'duration':model[0].exam_duration
                       })
                i.answer=0
                i.save()

         return render(request,'student/exam.html',{'questions':questions_list,
                                                    'model':request.POST['model']
                                                    })

def lecture(request):
         return render(request,'student/lecture.html')

def result(request):  
         answers_count=0
         result=0
         exam=request.POST
         questions_list=[]

     #     return HttpResponse(exam)
         qu=Exam_Models_Questions.objects.filter(question_text=request.POST['question1'])
         questions=Exam_Models_Questions.objects.filter(model_name=qu[0].model_name)
         jsonDec = json.decoder.JSONDecoder()

         for i in range(len(questions)):
                questions_list.append({
                       'id':questions[i].id,
                       'option':jsonDec.decode(questions[i].options),
                       'question_text':questions[i].question_text,
                       'duration':qu[0].model_name.exam_duration,
                       'answer':questions[i].answer,
                       'answer_num':questions[i].answer_number
                       })
               #  question=Exam_Models_Questions.objects.filter(question_text=exam['question%d' %(i+1)])
               #  return HttpResponse(question[0].id)
             
                if 'option%d' %(questions[i].id) in exam:
                       if str(questions[i].answer_number) == str(exam['option%d' %(questions[i].id)]):
                              questions[i].answer=1
                              # return HttpResponse(questions[i].answer)

                              questions[i].save()
                              answers_count+=1
                else:
                       continue
                       
         result=(60 / int(questions.count()))*answers_count
         if Student.objects.filter(academic_ID=request.session['student_ID'])[0] in Result.objects.all():
                         return render(request,'student/result.html',{
                'questions':questions_list,
                'model':qu[0].model_name,
                
                
         })
                
         student_result=Result()
         student_result.student_ID=Student.objects.filter(academic_ID='1')[0]
         student_result.decision_ID=Exam_Models.objects.filter(name=qu[0].model_name)[0].decision_ID
         student_result.exam_result=result
         student_result.save()
     #     return HttpResponse('done')      

                                


         return render(request,'student/result.html',{
                'questions':questions_list,
                'model':qu[0].model_name
                
         })

def examDone(request):         
          return render(request,'student/examDone.html')



       
     