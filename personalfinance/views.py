from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from personalfinance.models import Userprofile, FModel, Income, Expense, Asset, ProfilePage
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def create_user_profile(request):

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        age = request.POST.get('age')
        job = request.POST.get('job')

        if not (user_id and age and job):
            return JsonResponse({'error': 'Missing profile data'}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)
        
        try:
            userprofile = Userprofile.objects.create(
                user=user,
                age=age,
                job=job
            )

            return JsonResponse({
                'id': userprofile.id,
                'user_id': userprofile.user.id,
                'age': userprofile.age,
                'job': userprofile.job
            }, status=200)
    
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_fmodel(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        fmodel_name = request.POST.get('fmodel_name')

        if not (user_id and fmodel_name):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)

        try:
            fmodel = FModel.objects.create(
                user=user,
                fmodel_name=fmodel_name
            )

            return JsonResponse({
                'id': fmodel.id,
                'user': fmodel.user.id,
                'fmodel_name': fmodel.fmodel_name,
                'created': fmodel.created.strftime('%Y-%m-%d')
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating FModel: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def create_income(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        fmodel_name = request.POST.get('fmodel_name')
        income_name = request.POST.get('income_name')
        value = request.POST.get('value')

        if not (user_id and fmodel_name and income_name and value):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            fmodel = FModel.objects.get(user=user, fmodel_name=fmodel_name)

        except (User.DoesNotExist, FModel.DoesNotExist):
            return JsonResponse({'error': 'User or FModel not found'}, status=400)

        try:
            income = Income.objects.create(
                fmodel=fmodel,
                income_name=income_name,
                value=value
            )

            return JsonResponse({
                'id': income.id,
                'fmodel_id': income.fmodel.id,
                'income_name': income.income_name,
                'value': str(income.value)
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating Income: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_expense(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        fmodel_name = request.POST.get('fmodel_name')
        expense_name = request.POST.get('expense_name')
        value = request.POST.get('value')

        if not (user_id and fmodel_name and expense_name and value):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            fmodel = FModel.objects.get(user=user, fmodel_name=fmodel_name)
        except (User.DoesNotExist, FModel.DoesNotExist):
            return JsonResponse({'error': 'User or FModel not found'}, status=400)

        try:
            expense = Expense.objects.create(
                fmodel=fmodel,
                expense_name=expense_name,
                value=value
            )

            return JsonResponse({
                'id': expense.id,
                'fmodel_id': expense.fmodel.id,
                'expense_name': expense.expense_name,
                'value': str(expense.value)
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating Expense: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_asset(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        fmodel_name = request.POST.get('fmodel_name')
        asset_name = request.POST.get('asset_name')
        yield_rate = request.POST.get('yield_rate')
        principle_amount = request.POST.get('principle_amount')

        if not (user_id and fmodel_name and asset_name and yield_rate and principle_amount):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            fmodel = FModel.objects.get(user=user, fmodel_name=fmodel_name)
        except (User.DoesNotExist, FModel.DoesNotExist):
            return JsonResponse({'error': 'User or FModel not found'}, status=400)

        try:
            asset = Asset.objects.create(
                fmodel=fmodel,
                asset_name=asset_name,
                yield_rate=yield_rate,
                principle_amount=principle_amount
            )

            return JsonResponse({
                'id': asset.id,
                'fmodel_id': asset.fmodel.id,
                'asset_name': asset.asset_name,
                'yield_rate': str(asset.yield_rate),
                'principle_amount': str(asset.principle_amount)
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating Asset: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_profile_page(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        fmodel_name = request.POST.get('fmodel_name')
        page_name = request.POST.get('page_name')

        if not (user_id and fmodel_name and page_name):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            fmodel = FModel.objects.get(user=user, fmodel_name=fmodel_name)
        except (User.DoesNotExist, FModel.DoesNotExist):
            return JsonResponse({'error': 'User or FModel not found'}, status=400)

        try:
            profile_page = ProfilePage.objects.create(
                user=user,
                fmodel=fmodel,
                page_name=page_name
            )

            return JsonResponse({
                'id': profile_page.id,
                'user_id': profile_page.user.id,
                'fmodel_id': profile_page.fmodel.id,
                'page_name': profile_page.page_name
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating ProfilePage: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        fmodel_id = request.POST.get('fmodel_id')
        page_name = request.POST.get('page_name')

        if not (user_id and fmodel_id and page_name):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            fmodel = FModel.objects.get(id=fmodel_id, user=user)
        except (User.DoesNotExist, FModel.DoesNotExist):
            return JsonResponse({'error': 'User or FModel not found'}, status=400)

        try:
            profile_page = ProfilePage.objects.create(
                user=user,
                fmodel=fmodel,
                page_name=page_name
            )

            return JsonResponse({
                'id': profile_page.id,
                'user_id': profile_page.user.id,
                'fmodel_id': profile_page.fmodel.id,
                'page_name': profile_page.page_name
            }, status=201)

        except Exception as e:
            logger.error(f"Error creating ProfilePage: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)