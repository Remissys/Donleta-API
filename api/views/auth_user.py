from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from ..serializers import LoginSerializer, RefreshTokenSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = LoginSerializer(request.data)

            user = authenticate(request, username=data.username, password=data.password)

            if user is None:
                return JsonResponse({"status": False, "message": "Credenciais inválidas"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not user.is_active:
                return JsonResponse({"status": False, "message": "Usuário inativo"}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)

            response = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "is_admin": user.is_staff,
                }
            }

            return JsonResponse({"status": True, "message": "Login realizado com sucesso", "data": {response}}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = RefreshTokenSerializer(request.data)

            if not data.refresh_token:
                return JsonResponse({"status": False, "message": "Refresh token não enviado"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                refresh = RefreshToken(data.refresh_token)
                access_token = refresh.access_token

                response = {
                    "access": str(access_token)
                }

                return JsonResponse({"status": True, "message": "Token atualizado com sucesso", data: {response}}, status=status.HTTP_200_OK)
            
            except TokenError:
                return JsonResponse({"status": False, "message": "Refresh token inválido ou expirado"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)