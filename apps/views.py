import random

from django.core.mail import send_mail
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.generics import UpdateAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import HomeCategory, Home, HomeImages, HomeNeed, Advertisement, User, District, Region, LoginRegister
from apps.serializers import HomeCategorySerializer, HomeSerializer, HomeImagesSerializer, HomeNeedSerializer, \
    AdvertisementSerializer, UserSerializer, DistrictSerializer, RegionSerializer, RegisterSerializer, \
    LoginRegisterModelSerializer


@extend_schema(tags=["Category"])
class HomeCategoryViewSet(viewsets.ModelViewSet):
    queryset = HomeCategory.objects.all()
    serializer_class = HomeCategorySerializer


@extend_schema(tags=["Home"])
class HomeViewSet(viewsets.ModelViewSet):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

    def get_queryset(self):
        queryset = Home.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


@extend_schema(tags=["Images"])
class HomeImageViewSet(viewsets.ModelViewSet):
    queryset = HomeImages.objects.all()
    serializer_class = HomeImagesSerializer


@extend_schema(tags=["Needs"])
class HomeNeedViewSet(viewsets.ModelViewSet):
    queryset = HomeNeed.objects.all()
    serializer_class = HomeNeedSerializer


@extend_schema(tags=["Reklama"])
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer


@extend_schema(tags=["Profil"])
class UserProfileUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=['Region'])
class DistrictListView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


@extend_schema(tags=['regions'])
class RegionListView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


@extend_schema(tags=['Register'])
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeFilter(FilterSet):
    district = ModelChoiceFilter(queryset=District.objects.all())
    location = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Home
        fields = ['district', 'location']


@extend_schema(tags=['Filter'])
class HomeListAPIView(ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeFilter


@extend_schema(tags=["RegisterLogin"])
class LoginRegisterListCreateAPIView(ListCreateAPIView):
    queryset = LoginRegister.objects.all()
    serializer_class = LoginRegisterModelSerializer

    def post(self, request, *args, **kwargs):
        sms_verify_code = str(random.randint(1000, 9999))

        data = request.data.copy()
        data['sms_verify'] = sms_verify_code

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)

            email = serializer.validated_data['email']
            send_mail(
                'SMS Verification Code',
                f'Your verification code is: {sms_verify_code}',
                'Uy_Bor@example.com',
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["RegisterLogin"])
class LoginRegisterRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = LoginRegister.objects.all()
    serializer_class = LoginRegisterModelSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VerifySMSAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        sms_verify_code = request.data.get('sms_verify')

        try:
            user = LoginRegister.objects.get(user_id=user_id)
            if user.sms_verify == sms_verify_code:
                user.is_verified = True
                user.save()
                return Response({"message": "User successfully verified."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except LoginRegister.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
