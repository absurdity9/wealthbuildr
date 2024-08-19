from django.contrib import admin
from .models import Userprofile, FModel, Income, Expense, Asset, PublishedPage

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
    list_display = ('id', 'fmodel', 'asset_name', 'yield_rate', 'principle_amount', 'allocation_pct')
    search_fields = ('asset_name',)
    list_filter = ('fmodel', 'yield_rate')
    ordering = ('id',)
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('id', 'fmodel', 'asset_name', 'yield_rate', 'principle_amount', 'allocation_pct')
        }),
    )

class PublishedPageAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'fmodel', 'is_public', 'published_date')
    search_fields = ('page_name', 'fmodel__fmodel_name')
    list_filter = ('is_public', 'published_date')
    ordering = ('-published_date',)
    readonly_fields = ('published_date',)
    fieldsets = (
        (None, {
            'fields': ('fmodel', 'page_name', 'slug', 'is_public', 'published_date')
        }),
    )

admin.site.register(Userprofile, UserprofileAdmin)
admin.site.register(FModel, FModelAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(PublishedPage, PublishedPageAdmin)