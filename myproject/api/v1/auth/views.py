import requests
import json


from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from blogApp.models import UserProfile


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    response_data = {"status": 6003, "message": "An unexpected error occurred."}  # Initialize with a default error response
    email = request.data.get('email')
    name = request.data.get('name')
    profile = request.data.get('profile_picture')
    bio = request.data.get('bio')
    info = request.data.get('information')
    password = request.data.get('password')
    if not email or not password or not name:
        return Response({"status": 6002, "message": "Email, password, and name are required."}, status=400)
    
    if not User.objects.filter(username=email).exists():
        user = User.objects.create_user(username=email, password=password, first_name=name)
        UserProfile.objects.create(user=user, profile_picture=profile, bio=bio, information=info, name=name)
       
        headers = {"Content-Type": "Application/json"}
        data = {'username': email, 'password': password}
        protocol = 'https://' if request.is_secure() else 'http://'
        host = request.get_host()
        url = protocol + host + '/api/v1/auth/token/'
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(request.data) 
        
        if response.status_code == 200:

            response_data = {
                'status': 6000,
                "data": response.json(),
                'message': 'Account created successfully.'
            }
        else:
            response_data = {
                'status': response.status_code,
                'message': 'Failed to authenticate newly created user.'
            }
    else:
        response_data = {"status": 6001, "message": "User already exists."}
    
    return Response(response_data)








