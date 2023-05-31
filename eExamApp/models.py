from django.db import models
from datetime import datetime
# Create your models here.

'''
----------------------------------------------------------------------
---------------------------الجداول الأساسية---------------------------
----------------------------------------------------------------------
'''


#-------------------------------المستوى-----------------------------

class Level(models.Model):
    level_name=models.CharField(null=True,unique=True,max_length=30)

    def __str__(self) :
        return self.level_name

#-------------------------------الكلية-----------------------------


class College(models.Model):
    college_name=models.CharField(null=True,unique=True,max_length=100)

    def __str__(self) :
        return self.college_name

#-------------------------------التخصص-----------------------------

class Specialization(models.Model):
    specialization_name=models.CharField(null=True,unique=True,max_length=100)
    college_ID=models.ForeignKey(College,on_delete=models.PROTECT)



    def __str__(self) :
        return self.specialization_name

#-------------------------------الطالب-----------------------------


class Student(models.Model):
    student_name=models.CharField(null=True,unique=True,max_length=100)
    academic_ID=models.BigAutoField(primary_key=True,auto_created=True,serialize=False, verbose_name='ID')
    password=models.CharField(null=True,max_length=100)
    # photo=models.ImageField()
    entry_date=models.DateTimeField(default=datetime.now,null=True)
    college=models.ForeignKey(College,on_delete=models.PROTECT)
    specialization=models.ForeignKey(Specialization,on_delete=models.PROTECT)
    level=models.ForeignKey(Level,on_delete=models.PROTECT)
    
    def __str__(self) :
        return self.student_name

#-------------------------------المدرس-----------------------------

    
class Teacher(models.Model):
    functional_ID=models.BigAutoField(primary_key=True,auto_created=True,serialize=False, verbose_name='ID')
    teacher_name=models.CharField(null=True,unique=True,max_length=100)
    password=models.CharField(null=True,max_length=100)
    phone=models.IntegerField(unique=True)
    email=models.EmailField(null=True,unique=True,max_length=100)
    qualified=models.CharField(null=True,max_length=200)

    
    def __str__(self) :
        return self.teacher_name


#-------------------------------المقرر-----------------------------

class Decision(models.Model):
    decision_name=models.CharField(null=True,unique=True,max_length=100)

    def __str__(self) :
        return self.decision_name

#-------------------------------نماذج الإمتحان-----------------------------


class Exam_Models(models.Model):
    name=models.CharField(null=True,max_length=100,unique=True)
    exam_duration=models.CharField(null=True,max_length=100)
    def __str__(self) :
        return self.name
    
#------------------------------- أسئلة نماذج الامتحان-----------------------------

class Exam_Models_Questions(models.Model):
    question_text=models.CharField(null=True,max_length=500)
    answer_number=models.IntegerField()
    options=models.CharField(null=True,max_length=2000)
    model_name=models.ForeignKey(Exam_Models,on_delete=models.PROTECT)

    def __str__(self) :
        return self.question_text

'''
---------------------------------------------------------------------------
-----------------------------الجداول الوسيطة------------------------------ 
---------------------------------------------------------------------------
'''

#-------------------------------المنهج-----------------------------

class Approach(models.Model):
    teatcher_ID=models.ForeignKey(Teacher,on_delete=models.PROTECT)
    decision_ID=models.ForeignKey(Decision,on_delete=models.PROTECT)
    decision_type=models.CharField(null=True,max_length=10)

    def __int__(self) :
        return self.id

#-------------------------------النتيجة-----------------------------

class Result(models.Model):
    student_ID=models.ForeignKey(Student,on_delete=models.PROTECT)
    decision_ID=models.ForeignKey(Decision,on_delete=models.PROTECT)
    exam_result=models.IntegerField(null=True)

class Decision_And_Level(models.Model):
    decision_ID=models.ForeignKey(Decision,on_delete=models.PROTECT)
    level_ID=models.ForeignKey(Level,on_delete=models.PROTECT)
    

class Decision_And_College(models.Model):
    decision_ID=models.ForeignKey(Decision,on_delete=models.PROTECT)
    college_ID=models.ForeignKey(College,on_delete=models.PROTECT)

class Decision_And_Specialization(models.Model):
    decision_ID=models.ForeignKey(Decision,on_delete=models.PROTECT)
    specialization_ID=models.ForeignKey(Specialization,on_delete=models.PROTECT)






    