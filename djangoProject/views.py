import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .settings import SECRET_KEY

class AuthAPIView(APIView):
    # 유저 정보 확인
    def post(self, request):
            # 유저 인증
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
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
                # access token을 decode 해서 유저 id 추출 => 유저 식별
                access = request.data.get("access")
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                username = payload.get('username')
                user = get_object_or_404(User, username=username)
                serializer = UserSerializer(instance=user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except(jwt.exceptions.ExpiredSignatureError):
                # 토큰 만료 시 토큰 갱신
                try:
                    refresh_value = request.data.get("refresh")
                    serializer = TokenRefreshSerializer(data={'refresh': refresh_value})
                    if serializer.is_valid(raise_exception=True):
                        access_token = serializer.validated_data.get('access', None)
                        res = Response(
                            {
                                "access": access_token,
                            },
                            status=status.HTTP_200_OK
                        )
                        return res
                except(jwt.exceptions.InvalidTokenError):
                    # 사용 불가능한 토큰일 때
                    return Response(status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "access": access_token,
                    "refresh": refresh_token,
                },
                status=status.HTTP_200_OK,
            )

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)