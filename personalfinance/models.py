from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    job = models.CharField(max_length=100)

class FModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fmodel_name = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'fmodel_name'], name='unique_fmodel_per_user')
        ]


class Income(models.Model):
    id = models.IntegerField(primary_key=True)
    fmodel = models.ForeignKey(FModel, on_delete=models.CASCADE)
    income_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)

class Expense(models.Model):
    id = models.IntegerField(primary_key=True)
    fmodel = models.ForeignKey(FModel, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)

class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    fmodel = models.ForeignKey(FModel, on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=100)
    yield_rate = models.DecimalField(max_digits=5, decimal_places=2)
    principle_amount = models.DecimalField(max_digits=10, decimal_places=2)

class ProfilePage(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fmodel = models.ForeignKey(FModel, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
