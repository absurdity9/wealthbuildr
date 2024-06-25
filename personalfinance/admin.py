from django.contrib import admin
from .models import Userprofile, FModel, Income, Expense, Asset, ProfilePage

class UserprofileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'job')
    search_fields = ('user__username', 'job')

class FModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fmodel_name', 'created')
    search_fields = ('fmodel_name', 'user__username')
    list_filter = ('created', 'user')

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'fmodel', 'income_name', 'value')
    search_fields = ('income_name', 'fmodel__fmodel_name')
    list_filter = ('fmodel',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'fmodel', 'expense_name', 'value')
    search_fields = ('expense_name', 'fmodel__fmodel_name')
    list_filter = ('fmodel',)

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'fmodel', 'asset_name', 'yield_rate', 'principle_amount')
    search_fields = ('asset_name', 'fmodel__fmodel_name')
    list_filter = ('fmodel',)

class ProfilePageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fmodel', 'page_name')
    search_fields = ('page_name', 'user__username', 'fmodel__fmodel_name')
    list_filter = ('user', 'fmodel')

admin.site.register(Userprofile, UserprofileAdmin)
admin.site.register(FModel, FModelAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(ProfilePage, ProfilePageAdmin)
