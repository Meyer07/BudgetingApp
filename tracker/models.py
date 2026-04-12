from django.db import models
from django.utils import timezone

class Category(models.Model):
    name=models.CharField(max_length=100)


    def __str__(self):
        return self.name


class transactions(models.Model):
    TRANSACTION_TYPES=[
        ('income','Income'),
        ('expense','Expense')
    ]

    title=models.CharField(max_length=200)
    amount=models.DecimalField(max_digits=10,max_places=2)
    transaction_type=models.CharField(max_length=10,choices=TRANSACTION_TYPES)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(default=timezone.now)
    notes=models.TextField(blank=True)
    
