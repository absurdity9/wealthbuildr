from django.shortcuts import render
from django.contrib.auth.models import User
from personalfinance.models import Userprofile, FModel, Income, Expense, Asset
# Create your views here.

def create_user_profile(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        age = request.POST.get('age')
        job = request.POST.get('job')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

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
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)