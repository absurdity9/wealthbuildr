from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from personalfinance.models import Userprofile, FModel, Income, Expense, Asset
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