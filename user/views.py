from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            data = request.data
            name = data['name']
            email = data['email'].lower()
            password = data['password']
            re_password = data['re_password']
            is_realtor = data['is_realtor'] == 'True' 

            # Password validation
            if password != re_password:
                return Response({'Error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            if len(password) < 8:
                return Response({'Error': 'Password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user already exists
            if User.objects.filter(email=email).exists():
                return Response({'Error': 'User already exists with provided email'}, status=status.HTTP_400_BAD_REQUEST)

            # Create user or realtor account
            if is_realtor:
                User.objects.create_realtor(name=name, email=email, password=password)
                return Response({'Success': 'Realtor account created successfully.'}, status=status.HTTP_201_CREATED)
            else:
                User.objects.create_user(name=name, email=email, password=password)
                return Response({'Success': 'User created successfully.'}, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({'Error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'Error': f'Something went wrong when registering user: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class RetrieveUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)
            return Response(
                {'User': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'Error': 'Something Went Wrong When Registering User.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )