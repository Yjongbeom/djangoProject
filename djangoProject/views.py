import jwt
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .settings import SECRET_KEY


class AuthAPIView(APIView):
    def post(self, request):
        # 유저 인증
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )

        if user is not None:
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            user.access = access_token
            user.save()

            res = Response(
                {
                        "access": access_token,
                        "refresh": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            try:
                # access token decode
                access = request.data.get("access")
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                username = payload.get('username')
                user = get_object_or_404(User, username=username)

                user.access = access
                user.save()

                serializer = UserSerializer(instance=user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except(jwt.exceptions.ExpiredSignatureError):
                # 토큰 만료 시 토큰 갱신
                refresh_value = request.data.get("refresh")
                serializer = TokenRefreshSerializer(data={'refresh': refresh_value})
                try:
                    if serializer.is_valid(raise_exception=True):
                        access_token = serializer.validated_data.get('access', None)
                        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
                        username = payload.get('username')
                        user = get_object_or_404(User, username=username)
                        if access_token is not None:
                            user.access = access_token
                            user.save()

                            res = Response(
                                {
                                    "access": access_token,
                                },
                                status=status.HTTP_200_OK
                            )
                            return res
                        else:
                            return Response({"error": "리프레시 중에 액세스 토큰이 None입니다."}, status=status.HTTP_400_BAD_REQUEST)

                except(TokenBackendError, TokenError):
                    return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
            except(jwt.exceptions.InvalidTokenError):
                # 사용 불가능 토큰
                return Response(status=status.HTTP_400_BAD_REQUEST)

