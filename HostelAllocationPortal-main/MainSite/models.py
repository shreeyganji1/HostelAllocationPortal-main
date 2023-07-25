from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    is_warden = models.BooleanField(default=False)

hostel_choices = [('I','I-block'),('H','H-block'),('F','F-block')]
occupancy_choices = [('4', 'four'), ('5', 'five')]

class Student(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    gender_choices = [('N','None'),('M', 'Male'), ('F', 'Female')]
    course_choices = [('CSE','Computer Engineering'),('ExTC', 'Electronics and Telecommunication Engineering'), ('Mech', 'Mechanical Engineering')]
    student_name = models.CharField(max_length=200, null=True)
    father_name = models.CharField(max_length=200, null=True)
    enrollment_no = models.CharField(max_length=10, unique=True, null=True)
    course = models.CharField(
        choices=course_choices,
        null=True,
        max_length=4,
        default=None)
    dob = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default='N',null=True)
    room = models.OneToOneField(
        'Room',
        blank=True,
        on_delete= models.SET_NULL,
        null=True)
    room_allotted = models.BooleanField(default=False)
    documnets_uploaded = models.BooleanField(default=False)
    documnets_aproved = models.BooleanField(default=False)
    no_dues = models.BooleanField(default=True)
    current_cgpa = models.FloatField(default=0)
    aadharCard = models.CharField(max_length = 2000,default=None, null=True)
    photoId = models.CharField(max_length = 2000, default=None, null=True)
    feeReciept = models.CharField(max_length = 2000, default=None, null=True)
    pref1 = models.CharField(max_length=200, null=True, default=None)
    pref2 = models.CharField(max_length=200, null=True, default=None)
    pref3 = models.CharField(max_length=200, null=True, default=None)
    pref4 = models.CharField(max_length=200, null=True, default=None)
    pref5 = models.CharField(max_length=200, null=True, default=None)
    prefRec = models.BooleanField(default=False)

    def __str__(self):
        return str(self.enrollment_no)

    def delete(self, *args, **kwargs):
        room_del = Room.objects.filter(student__room=self.room)
        for s in room_del:
            s.vacant = True
            s.save()
        super(Student, self).delete(*args, **kwargs)


class Room(models.Model):
    Number = models.CharField(max_length=5)
    room_type = models.CharField(choices=occupancy_choices, max_length=1, default=None)
    vacant = models.BooleanField(default=False)
    hostel =models.ForeignKey('Hostel',default=None,null=True, on_delete=models.CASCADE)
    repair = models.CharField(max_length=100, blank=True)
    preferences = models.TextField(null=True)

    def __str__(self):
        return '%s %s' %(self.Number, self.hostel)

    def delete(self, *args, **kwargs):
        stud = Student.objects.filter(room=self)
        for s in stud:
            s.room_allotted = False
            s.save()
        super(Room, self).delete(*args, **kwargs)


class Hostel(models.Model):
    name = models.CharField(choices=hostel_choices, max_length=1, default=None)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    occupancy = models.CharField(choices=occupancy_choices, max_length=1, default=None)
    caretaker = models.CharField(max_length=100, blank=True)
    alloted = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Warden(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    hostel = models.ForeignKey('Hostel',default=None,null=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user.is_warden is False:  # Set default reference
            self.user.is_warden = True
            self.user.save()
        super(Warden, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.is_warden = False
        self.user.save()

        super(Warden, self).delete(*args, **kwargs)


class Leave(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100,blank = False)
    accept = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    confirm_time = models.DateTimeField(auto_now_add=True)
