from re import I
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import Sum
from django.contrib.auth.models import User

class Department(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Faculty', 'Faculty'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DEPARTMENT_CHOICES = [
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Faculty', 'Faculty'),
    ]
    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES,
        default='Student',
    )
    
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    location = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location

class Bus(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE, blank= True, null = True)
    bus_number = models.CharField(max_length=250)
    seats = models.FloatField(max_length=5, default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_number

class Schedule(models.Model):
    code = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    depart = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='depart_location')
    destination = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='destination')
    schedule= models.DateTimeField()
    seats_available = models.IntegerField(null=True)  # replaced fare with seats_available
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Cancelled')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    ABLE_TO_BOOK_CHOICES = [
        ('None', 'None'),
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Faculty', 'Faculty'),
    ]
    able_to_book = models.CharField(
        max_length=10,
        choices=ABLE_TO_BOOK_CHOICES,
        default='None',
    )

    def __str__(self):
        return str(self.code + ' - ' + self.bus.bus_number)

    def count_available(self):
        booked = Booking.objects.filter(schedule=self, status='2').aggregate(Sum('seats'))['seats__sum']
        if booked is not None:
            return self.seats_available - booked
        else:
            # Handle the case where no seats are booked for this schedule
            return self.seats_available

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # allow NULL values temporarily
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    schedule = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    seats = models.IntegerField()
    status = models.CharField(max_length=2, choices=(('1','Pending'),('2','Approved'),('3','Rejected')), default=1)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code + ' - ' + self.name)

    # def total_payable(self):
    #     return self.seats * self.schedule.fare

class TripRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    depart = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='request_depart_location')
    destination = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='request_destination')
    schedule= models.DateField()
    seats= models.IntegerField(null=True)
    status = models.CharField(max_length=10, choices=(('active', 'Active'), ('cancelled', 'Cancelled'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='active')
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user.username + ' - ' + self.bus.bus_number)

# @receiver(models.signals.post_save, sender=Invoice_Item)
# def stock_update(sender, instance, **kwargs):
#     stock = Stock(product = instance.product, quantity = instance.quantity, type = 2)
#     stock.save()
#     # stockID = Stock.objects.last().id
#     Invoice_Item.objects.filter(id= instance.id).update(stock=stock)

# @receiver(models.signals.post_delete, sender=Invoice_Item)
# def delete_stock(sender, instance, **kwargs):
#     try:
#         stock = Stock.objects.get(id=instance.stock.id).delete()
#     except:
#         return instance.stock.id



    
    