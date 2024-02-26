from django.db import models
from django.contrib.auth.models import User

class Camp(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Week(models.Model):
    week_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)

    def __str__(self):
        return f'Week {self.week_number} of {self.camp.name}'
    
class Kid(models.Model):
    name = models.CharField(max_length=50)
    dob = models.DateField()
    school = models.CharField(max_length=50)
    allergies = models.TextField(max_length=300)
    emergency_contact = models.CharField(max_length=25)
    leaving_permissions = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'