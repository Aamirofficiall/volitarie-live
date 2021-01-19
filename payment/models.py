from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
import jsonfield


class Order(models.Model):
    ORDER_CHOICE = (
        ('Starter', 'Starter'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'), 
    )  
    order_option = models.CharField(max_length=30, choices=ORDER_CHOICE,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return '{})- {} {}'.format(
            self.id,self.user.username,self.order_option
            )

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    recipt_url= models.URLField(max_length = 200) 
    payment_info=jsonfield.JSONField()

    def __str__(self):
        return '{})- {} {}'.format(
            self.id,self.user.username,self.order.order_option
            )    

class Balance(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    amount = models.IntegerField() 
    remaining_balance = models.FloatField(default=0.0)  
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return '{})- {} {}'.format(
            self.id,self.user.username,self.amount,self.remaining_balance,
            )  