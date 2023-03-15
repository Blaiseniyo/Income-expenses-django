from django.shortcuts import render

from rest_framework import generics,status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
# from .util import Util
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        user = request.data
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email = user_data["email"])
        token = RefreshToken.for_user(user).access_token
        
        current_site = get_current_site(request).domain
        
        relative_link = reverse("email-verify")
        abs_url = f"http://{current_site}/{relative_link}?token={token}"
        email_body = f"Hi, {user.username} use linl below to verify your email \n {abs_url}"
        data = {"to_email":user.username,'subject':"Verify your email","body":email_body}
        # Util.send_email(data)
        return Response(user_data,status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    
    def get(self):
        pass