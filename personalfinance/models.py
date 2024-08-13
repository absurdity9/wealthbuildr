from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
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
    allocation_pct = models.DecimalField(max_digits=5, decimal_places=2)

class PublishedPage(models.Model):
    id = models.AutoField(primary_key=True)
    fmodel = models.OneToOneField(FModel, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    is_public = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.page_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PublishedPage: {self.page_name} (Public: {self.is_public})"