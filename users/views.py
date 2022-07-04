from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        userData = UserSerializer(user).data
        token, created = Token.objects.get_or_create(user=user)
        userData["token"] = token.key
        return Response(userData)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)

        data = serializer.data
        token, created = Token.objects.get_or_create(user=user)
        data["token"] = token.key
        data["diagnostics"] = []
        
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
