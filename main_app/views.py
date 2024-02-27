from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import Camp, Week
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class CampViewSet(viewsets.ModelViewSet):
    queryset = Camp.objects.all()
    serializer_class = CampSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

class WeekViewSet(viewsets.ModelViewSet):
    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    permission_classes = [IsAuthenticated]

class KidViewSet(viewsets.ModelViewSet):
    serializer_class = KidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Kid.objects.filter(user=self.request.user)

    # def post(self, request, *args, **kwargs):
    #     user_id = request.user.id
    #     user = User.objects.get(id=user_id)
    #     name = request.data.get("name")
    #     dob = request.data.get("dob")
    #     school = request.data.get("school")
    #     allergies = request.data.get("allergies")
    #     emergency_contact = request.data.get("emergency_contact")
    #     leaving_permissions = request.data.get("leaving_permissions")

    #     try:
    #         new_kid = Kid.objects.create(
    #             name = name,
    #             dob = dob,
    #             school = school,
    #             allergies = allergies,
    #             emergency_contact = emergency_contact,
    #             leaving_permissions = leaving_permissions,
    #             user = user
    #         )
    #         new_kid.save()

    #         return Response(status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        try:
            new_kid = Kid.objects.create(
                name=data.get("name"),
                dob=data.get("dob"),
                school=data.get("school"),
                allergies=data.get("allergies"),
                emergency_contact=data.get("emergency_contact"),
                leaving_permissions=data.get("leaving_permissions"),
                user=user
            )
            return Response(status=status.HTTP_201_CREATED, data=self.get_serializer(new_kid).data)
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def put(self, request, *args, **kwargs):
    #     kid_id = kwargs.get('pk')
    #     data = request.data  
    #     try:
    #         print(kid_id)
    #         print(data)
    #         kid = Kid.objects.get(id=kid_id, user=request.user)
    #         serializer = self.get_serializer(kid, data=data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Kid.DoesNotExist:
    #         return Response({"error": "Kid not found"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request, *args, **kwargs):
        kid_id = request.kid.id
        user = request.user
        name = request.data.get("name")
        dob = request.data.get("dob")
        school = request.data.get("school")
        allergies = request.data.get("allergies")
        emergency_contact = request.data.get("emergency_contact")
        leaving_permissions = request.data.get("leaving_permissions")

        try:
            Kid.objects.filter(id=kid_id).update(
                name=name,
                dob=dob,
                school=school,
                allergies=allergies,
                emergency_contact=emergency_contact,
                leaving_permissions=leaving_permissions,
                user=user
                )
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        kid_id = request.kid.id
        try:
            Kid.objects.get(id=kid_id).delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)

class LogoutView(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            new_user = User.objects.create(username=username, email=email)
            new_user.set_password(password)
            new_user.save()

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AddStaffView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            new_user = User.objects.create(username=username, email=email, is_staff=True)
            new_user.set_password(password)
            new_user.save()

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
