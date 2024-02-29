from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import Camp, Week
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from datetime import date

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class CampViewSet(viewsets.ModelViewSet):
    queryset = Camp.objects.all().order_by('-start_date')
    serializer_class = CampSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def upcoming_camps(self, request):
        today = date.today()
        upcoming_camps = Camp.objects.filter(end_date__gt=today)
        serializer = self.get_serializer(upcoming_camps, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            new_camp = Camp.objects.create(
                name=data.get("name"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
            )
            return Response(status=status.HTTP_201_CREATED, data=self.get_serializer(new_camp).data)
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class WeekViewSet(viewsets.ModelViewSet):
    serializer_class = WeekSerializer
    permission_classes = [IsAuthenticated]
    queryset = Week.objects.all()

    @action(detail=False, methods=['put'])
    def register_kid(self, request):
        data = request.data
        kid_id = data.get("kid_id")
        week_id = data.get("week_id")
        Week.objects.get(id=week_id).kids.add(kid_id)
        return Response(status=status.HTTP_200_OK)

class KidViewSet(viewsets.ModelViewSet):
    serializer_class = KidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Kid.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def list_all(self, request):
        queryset = Kid.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def list_one(self, request, pk=None):
        try:
            kid = Kid.objects.get(id=pk)
            serializer = self.get_serializer(kid)
            return Response(serializer.data)
        except Kid.DoesNotExist:
            return Response({"error": "Kid not found"}, status=status.HTTP_404_NOT_FOUND)

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

class LogoutView(APIView):
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
    
