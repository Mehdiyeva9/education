from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.api.serializer import UserCreateSerializer,UserSerializer, LoginSerializer, ResourceSerializer, HelpFormSerializer, SiteSettingsSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.core.mail import send_mail
from core.models import PasswordResetToken, Resource, HelpForm, SiteSettings

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAccountRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    lookup_field = "id"

class PasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        token = PasswordResetToken.objects.create(user=user, token=token)

        reset_url = request.build_absolute_uri(
            reverse("password-reset-confirm", kwargs={"token": token})
        )

        send_mail(
            subject="Password Reset",
            message=f"Hi {user.username},\nReset your password using this link: {reset_url}",
            from_email="noreply@yourapp.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)
    
class ResourceListAPIView(ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceRetrieveAPIView(RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    lookup_field = "id"

class HelpFormCreateAPIView(CreateAPIView):
    queryset = HelpForm.objects.all()
    serializer_class = HelpFormSerializer

class SiteSettingsListAPIView(ListAPIView):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer