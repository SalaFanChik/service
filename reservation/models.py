from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver




class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey("ClientProfile", on_delete=models.CASCADE)
    staff = models.ForeignKey("StaffProfile", on_delete=models.CASCADE)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.client.user.username} - {self.service.name} - {self.date} - {self.time}"


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"
        STAFF = "STAFF", "Staff"

    base_role = Role.STAFF
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            super().save(*args, **kwargs)



class ClientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CLIENT)

class Client(User):
    base_role = User.Role.CLIENT

    client = ClientManager()

    class Meta:
        proxy = True

@receiver(post_save, sender=Client)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "CLIENT":
        ClientProfile.objects.create(user=instance)


class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    #orders = models.ManyToManyField(Order, blank=True)
 

    def __str__(self):
        return self.user.username



    
class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STAFF)

class Staff(User):
    base_role = User.Role.STAFF

    staff = StaffManager()

    class Meta:
        proxy = True

class WorkingHours(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    phone_number = models.CharField(max_length=20, unique=True)
    #orders = models.ManyToManyField(Order, blank=True)
    services = models.ManyToManyField("Service", blank=True)
    class Weekday(models.TextChoices):
        MONDAY = "1", "Monday"
        TUESDAY = "2", "Tuesday"
        WEDNESDAY = "3", "Wednesday"
        THURSDAY = "4", "Thursday"
        FRIDAY = "5", "Friday"
        SATURDAY = "6", "Saturday"
        SUNDAY = "7", "Sunday"

    holiday = models.CharField(max_length=50, choices=Weekday.choices, default=Weekday.MONDAY)
    WorkingHours = models.ManyToManyField(WorkingHours, blank=True)
    def __str__(self):
        return self.user.username



@receiver(post_save, sender=Staff)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STAFF":
        StaffProfile.objects.create(user=instance)