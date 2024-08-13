from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from personalfinance.models import Userprofile, FModel, Income, Expense, Asset, PublishedPage
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
import simplejson
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from personalfinance.models import PublishedPage
from django.http import HttpResponseForbidden

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
    
    print(data)  # For debugging purposes
    
    json_data = simplejson.dumps(data, use_decimal=True)
    
    context = {
        'user': user,
        'fmodel_count': fmodel_count,
        'fmodels_data': json_data
    }
    return render(request, 'personalfinance/index.html', context)

def add(request):
    return render(request, 'personalfinance/add.html')

def add_copy(request):
    return render(request, 'personalfinance/add_copy.html')

def get_fmodel_data(request, fmodel_id):
    fmodel = get_object_or_404(FModel, id=fmodel_id)
    
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
    
    return JsonResponse(model_data)

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
                allocation_pct = asset_data.get('allocation_pct')  # Get allocation_pct from the request

                if not (asset_name and yield_rate and principle_amount and allocation_pct is not None):
                    return JsonResponse({'error': 'Missing required fields in assets array'}, status=400)

                asset = Asset.objects.create(
                    fmodel=fmodel,
                    asset_name=asset_name,
                    yield_rate=yield_rate,
                    principle_amount=principle_amount,
                    allocation_pct=allocation_pct  # Include allocation_pct when creating the asset
                )

                created_assets.append({
                    'id': asset.id,
                    'fmodel_id': asset.fmodel.id,
                    'asset_name': asset.asset_name,
                    'yield_rate': str(asset.yield_rate),
                    'principle_amount': str(asset.principle_amount),
                    'allocation_pct': str(asset.allocation_pct)  # Return allocation_pct in the response
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
            profile_page = PublishedPage.objects.create(
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
            logger.error(f"Error creating PublishedPage: {e}")
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import FModel, Income, Expense, Asset

@csrf_exempt
def edit_fmodel(request, fmodel_id):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        print(data)
        # Get the financial model object
        fmodel = FModel.objects.get(id=fmodel_id)

        # Update the model name if it has been changed
        if 'model_name' in data:
            fmodel.fmodel_name = data['model_name']
            fmodel.save()

        # Update the income data if it has been changed
        if 'incomes' in data:
            for i, income_data in enumerate(data['incomes']):
                income = fmodel.income_set.all()[i]
                if 'income_name' in income_data:
                    income.income_name = income_data['income_name']
                if 'value' in income_data:
                    income.value = income_data['value']
                income.save()

        # Update the expense data if it has been changed
        if 'expenses' in data:
            for i, expense_data in enumerate(data['expenses']):
                expense = fmodel.expense_set.all()[i]
                if 'expense_name' in expense_data:
                    expense.expense_name = expense_data['expense_name']
                if 'value' in expense_data:
                    expense.value = expense_data['value']
                expense.save()

        # Update the asset data if it has been changed
        if 'assets' in data:
            for i, asset_data in enumerate(data['assets']):
                asset = fmodel.asset_set.all()[i]
                if 'asset_name' in asset_data:
                    asset.asset_name = asset_data['asset_name']
                if 'yield_rate' in asset_data:
                    asset.yield_rate = asset_data['yield_rate']
                if 'principle_amount' in asset_data:
                    asset.principle_amount = asset_data['principle_amount']
                asset.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Return a JSON response indicating error
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def published_page_view(request, slug):
    published_page = get_object_or_404(PublishedPage, slug=slug)
    
    if not published_page.is_public:
        if not request.user.is_authenticated or published_page.fmodel.user != request.user:
            return HttpResponseForbidden("You do not have permission to view this page.")
    
    context = {
        'published_page': published_page,
        'fmodel': published_page.fmodel,
        'incomes': published_page.fmodel.income_set.all(),
    }
    
    return render(request, 'published_page.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def create_or_update_published_page(request):
    try:
        data = simplejson.loads(request.body)
        page_name = data.get('page_name')
        slug = data.get('slug')
        is_public = data.get('is_public')
        fmodel_id = data.get('fmodel')

        if not page_name or not slug or not fmodel_id:
            return HttpResponseBadRequest("Missing required fields.")
        
        existing_page = PublishedPage.objects.filter(fmodel_id=fmodel_id).exclude(slug=slug).first()
        if existing_page:
            return HttpResponseBadRequest(
                simplejson.dumps({"error": f"A PublishedPage with fmodel_id {fmodel_id} already exists."}),
                content_type='application/json'
            )
        
        print(f"Existing page: {existing_page}")         # Create or update PublishedPage
        
        published_page, created = PublishedPage.objects.update_or_create(
            slug=slug,
            defaults={
                'page_name': page_name,
                'is_public': is_public,
                'fmodel_id': fmodel_id
            }
        )

        response_data = {
            'id': published_page.id,
            'page_name': published_page.page_name,
            'slug': published_page.slug,
            'is_public': published_page.is_public,
            'published_date': published_page.published_date.isoformat(),
            'fmodel': published_page.fmodel.id
        }

        return JsonResponse(response_data, status=200)

    except simplejson.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data.")
    except Exception as e:
        return HttpResponseBadRequest(str(e))

@csrf_exempt
def check_published_page(request, fmodel_id):
    try:
        # Try to get the PublishedPage object for the given fmodel_id
        published_page = PublishedPage.objects.get(fmodel_id=fmodel_id)
        response = {
            'exists': True,
            'page_name': published_page.page_name,
            'is_public': published_page.is_public,
            'slug': published_page.slug,
            'published_date': published_page.published_date.isoformat(),
        }
    except PublishedPage.DoesNotExist:
        # If no PublishedPage exists, return a response indicating that
        response = {
            'exists': False,
            'message': f"No PublishedPage found for fmodel_id {fmodel_id}."
        }

    return JsonResponse(response)

@csrf_exempt
def toggle_public(request):
    try:
        data = simplejson.loads(request.body)
        slug = data.get('slug')
        is_public = data.get('is_public')

        if slug is None or is_public is None:
            return HttpResponseBadRequest("Missing required fields.")

        published_page = PublishedPage.objects.filter(slug=slug).first()
        if not published_page:
            return HttpResponseNotFound("Page not found.")

        published_page.is_public = is_public
        published_page.save()

        response_data = {
            'id': published_page.id,
            'page_name': published_page.page_name,
            'slug': published_page.slug,
            'is_public': published_page.is_public,
            'published_date': published_page.published_date.isoformat(),
            'fmodel': published_page.fmodel.id
        }

        return JsonResponse(response_data, status=200)

    except simplejson.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON data.")
    except Exception as e:
        return HttpResponseBadRequest(str(e))