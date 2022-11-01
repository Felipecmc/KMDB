from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from users.models import User
from users.serializers import  LoginSerializer, UserSerializer
import ipdb 
class UserRegistration(APIView):
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    
class UserListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        user_token_id = Token.objects.get(key= request.auth).user_id
        user_request = User.objects.get(id = user_token_id)
        users_list = User.objects.all() 
        serializer = UserSerializer(users_list, many=True)
        
        if not users_list:
            return Response({"detail": "No users found"}, status.HTTP_404_NOT_FOUND)
        
        if not user_request.is_superuser:
            return Response({"detail" : "User not authorized"}, status=403)
        
        return Response(serializer.data, status.HTTP_200_OK)
    
    
class LoginUserView(ObtainAuthToken):
    def post (self, request: Request):
        login = self.serializer_class(data=request.data, context= {"request": request})
        #ipdb.set_trace()
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #ipdb.set_trace()
        if not login.is_valid():
            return Response({"detail": "invalid data"}, status=400)
        
        user = login.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({"token": token.key})
    
class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request:Request, user_id):
        user_token_id = Token.objects.get(key= request.auth).user_id
        user_request = User.objects.get(id = user_token_id)
        user =get_object_or_404(User, id= user_id)
        serializer = UserSerializer(user)
        
        if user_id != user_token_id and user_request.is_superuser == False:
            return Response({"detail" : "User not authorized"}, status=403)
        
        elif user_id == user_token_id:
            return Response(serializer.data, status=200)
        
        else:
            return Response(serializer.data, status=200)