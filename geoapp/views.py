import json

import jwt
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from .models import UserDetails
from .serializers import UserProfileSerializer, UserDetailsSerializer
from django.core.serializers import serialize
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from drf_yasg import openapi



from django.shortcuts import render
from django.http import JsonResponse
# import numpy as np
# import cv2
# import face_recognition


class TokenObtainView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('access_token', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        access_token = request.query_params.get('access_token')
        try:
            decoded_token = jwt.decode(access_token, options={"verify_signature": False})
            expiry_timestamp = decoded_token['exp']
            expiry_datetime = datetime.utcfromtimestamp(expiry_timestamp)
            current_datetime = datetime.utcnow()
            # Extract user ID, roles, permissions, etc. from the token payload
            user_id = decoded_token.get('user_id')
            roles = decoded_token.get('roles', [])
            permissions = decoded_token.get('permissions', [])

            if current_datetime < expiry_datetime:
                return Response({
                    'time': expiry_datetime - current_datetime,
                    'status': "Access token is not expired.",
                    'user_id': user_id,
                    'roles': roles,
                    'permissions': permissions
                })
            else:
                return Response({
                    'time': expiry_datetime - current_datetime,
                    'status': "Access token has expired.",
                })
        except jwt.ExpiredSignatureError:
            print("Access token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid access token.")


class TokenRefreshView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
            },
        )
    )
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        # Validate refresh token
        try:
            token = RefreshToken(refresh_token)
            user_id = token.payload['user_id']
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate new access token
        access_token = str(token.access_token)
        return Response({'access_token': access_token})





class AdminDataView(ListAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer
    # pagination_class = PageNumberPagination
    # def get():
    #     queryset = UserDetails.objects.all()
    #     paginator = self.pagination_class()
    #     result_page = paginator.paginate_queryset(queryset, request)
    #     serializer = UserDetailsSerializer(result_page, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=UserDetailsSerializer)
    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         required=['refresh_token'],
    #         properties={
    #             'f_name': openapi.Schema(type=openapi.TYPE_STRING),
    #             'email': openapi.Schema(type=openapi.TYPE_STRING),
    #             'phone': openapi.Schema(type=openapi.TYPE_STRING),
    #             'address': openapi.Schema(type=openapi.TYPE_STRING)
    #         },
    #     )
    # )
    def post(self, request):
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self):
        return Response({}, status=status.HTTP_200_OK)



def verify_selfie(request):
    if request.method == 'POST' and request.FILES['image']:
        return render(request, 'geoapp/verify_selfie.html')
#         # Load the uploaded image
#         if 1: #try:
#             uploaded_image = request.FILES['image'].read()
#             # Convert the image bytes to numpy array
#             nparr = np.frombuffer(uploaded_image, np.uint8)
#             img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#             # Perform face detection
#             face_locations = face_recognition.face_locations(img)
#
#             # Assuming there's only one face in the image
#             if len(face_locations) == 1:
#                 # Perform face recognition
#                 # Load the known image (stored in UserProfile model for example)
#                 known_image = face_recognition.load_image_file("/Users/rajeev.ranjan/PycharmProjects/GeoLocation/download.jpeg")
#                 # Encode the known face
#                 known_face_encoding = face_recognition.face_encodings(known_image)[0]
#
#                 # Encode the uploaded image
#                 unknown_face_encoding = face_recognition.face_encodings(img)[0]
#
#                 # Compare faces
#                 results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
#
#                 if results[0]:
#
#
#                     return JsonResponse({'verified': True})
#                 else:
#                     return JsonResponse({'verified': False, 'message': 'Face not recognized'})
#             else:
#                 return JsonResponse({'verified': False, 'message': 'Multiple faces detected or no face detected'})
#         # except:
#         #     return JsonResponse({'verified': False, 'message': 'Face not recognized'})
#
#     return render(request, 'geoapp/verify_selfie.html')
