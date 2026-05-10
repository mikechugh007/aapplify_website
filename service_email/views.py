import django.db
from django.http import JsonResponse
from django.shortcuts import render
import json
from authentication.models import User
from mainapp.models import CreditTransaction
from .services import gpt_generate_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_mail(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        prompt = data.get('prompt','')
        print(request.user.id)
        
        if not prompt:
            return JsonResponse({'error': 'Question is required.'},status=400)

        # if not request.user.service_bookings.filter(service_id=1).exists():
        #     return JsonResponse({'error': 'You do not have access to this service.'},status=403)

        # return JsonResponse({'response': 'service email!'},status=200)
        
        user =request.user

        if user.credits<=0:
            return JsonResponse({'error': 'You do not have enough credits to use this service.'},status=403
            )
        
        try:
            # Deduct the credits within a transaction
            with transaction.atomic():
                response = gpt_generate_mail(prompt, stream=False)

                # Deduct one credit from the user
                user.credits -= 1
                user.save()

                CreditTransaction.objects.create(
                    user=user,
                    credits_spent=1,
                    log='Used 1 credit for a mail generation request.'
                )

        except Exception as e:
            return JsonResponse({'error': 'Failed to process request.'}, status=500)
        
        return JsonResponse({'response': response,'remaining_credits': user.credits}, status=200)

