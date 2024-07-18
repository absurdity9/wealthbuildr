from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from personalfinance.models import Userprofile, FModel, Income, Expense, Asset, ProfilePage
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
import simplejson as json


logger = logging.getLogger(__name__)

@login_required
def index(request):
    user = request.user
    fmodels = FModel.objects.filter(user=user).prefetch_related('income_set', 'expense_set', 'asset_set')
    fmodel_count = fmodels.count()

    data = {}
    for fmodel in fmodels:
        incomes = fmodel.income_set.all()
        expenses = fmodel.expense_set.all()
        assets = fmodel.asset_set.all()

        model_data = {
            'model_info': {
                'model_id': fmodel.id,
                'model_name': fmodel.fmodel_name,
                'date_created': fmodel.created.strftime('%Y-%m-%d %H:%M:%S')
            },
            'incomes': list(incomes.values()),
            'expenses': list(expenses.values()),
            'assets': list(assets.values())
        }

        data[fmodel.id] = model_data

    json_data = json.dumps(data)

    context = {
        'user': user,
        'fmodel_count': fmodel_count,
        'fmodels_data': json_data
    }

    return render(request, 'personalfinance/index.html', context)

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
        
        except IntegrityError:
            return JsonResponse({'error': 'FModel with this name already exists for this user'}, status=400)

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
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            fmodel_name = data.get('fmodel_name')
            expenses = data.get('expenses')

            if not (user_id and fmodel_name and expenses):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            user = User.objects.filter(id=user_id).first()
            fmodel = FModel.objects.filter(user=user, fmodel_name=fmodel_name).first()

            if not (user and fmodel):
                return JsonResponse({'error': 'User or FModel not found'}, status=400)

            created_expenses = []

            for expense_data in expenses:
                expense_name = expense_data.get('expense_name')
                value = expense_data.get('value')

                if not (expense_name and value):
                    return JsonResponse({'error': 'Missing required fields in expenses array'}, status=400)

                expense = Expense.objects.create(
                    fmodel=fmodel,
                    expense_name=expense_name,
                    value=value
                )

                created_expenses.append({
                    'id': expense.id,
                    'fmodel_id': expense.fmodel.id,
                    'expense_name': expense.expense_name,
                    'value': str(expense.value)
                })

            return JsonResponse({'expenses': created_expenses}, status=201)

        except Exception as e:
            logger.error(f"Error creating Expense: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_assets(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            fmodel_name = data.get('fmodel_name')
            assets = data.get('assets')

            if not (user_id and fmodel_name and assets):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            user = User.objects.filter(id=user_id).first()
            fmodel = FModel.objects.filter(user=user, fmodel_name=fmodel_name).first()

            if not (user and fmodel):
                return JsonResponse({'error': 'User or FModel not found'}, status=400)

            created_assets = []

            for asset_data in assets:
                asset_name = asset_data.get('asset_name')
                yield_rate = asset_data.get('yield_rate')
                principle_amount = asset_data.get('principle_amount')

                if not (asset_name and yield_rate and principle_amount):
                    return JsonResponse({'error': 'Missing required fields in assets array'}, status=400)

                asset = Asset.objects.create(
                    fmodel=fmodel,
                    asset_name=asset_name,
                    yield_rate=yield_rate,
                    principle_amount=principle_amount
                )

                created_assets.append({
                    'id': asset.id,
                    'fmodel_id': asset.fmodel.id,
                    'asset_name': asset.asset_name,
                    'yield_rate': str(asset.yield_rate),
                    'principle_amount': str(asset.principle_amount)
                })

            return JsonResponse({'assets': created_assets}, status=201)

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

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'personalfinance/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)

def edit_fmodel_name(request, fmodel_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_name = data.get('new_name')
            if not new_name:
                return JsonResponse({'error': 'New name is required'}, status=400)

            fmodel = get_object_or_404(FModel, id=fmodel_id)
            fmodel.fmodel_name = new_name
            fmodel.save()

            return JsonResponse({'message': 'FModel name updated successfully'}, status=200)
        except Exception as e:
            logger.error(f"Error updating FModel: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)