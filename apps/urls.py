from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import HomeCategoryViewSet, HomeViewSet, HomeImageViewSet, HomeNeedViewSet, AdvertisementViewSet, \
    UserProfileUpdateView, DistrictListView, RegionListView, RegisterView, HomeListAPIView, \
    LoginRegisterListCreateAPIView, VerifySMSAPIView, LoginRegisterRetrieveUpdateDestroyAPIView

router = DefaultRouter()
router.register('categories', HomeCategoryViewSet, basename='categories')
router.register('homes', HomeViewSet, basename='homes')
router.register('images', HomeImageViewSet, basename='images')
router.register('needs', HomeNeedViewSet, basename='needs')
router.register('reklama', AdvertisementViewSet, basename='reklama')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('users/<int:pk>/profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),

    path('district', DistrictListView.as_view(), name='district-list'),
    path('regions', RegionListView.as_view(), name='region-list'),
]

urlpatterns += [
    path('login/register/', LoginRegisterListCreateAPIView.as_view(), name='login-register'),
    path('login/verify/', VerifySMSAPIView.as_view(), name='verify-sms'),
    path('LoginRegister/<int:pk>', LoginRegisterRetrieveUpdateDestroyAPIView.as_view()),

    # path('api/register/', RegisterView.as_view(), name='register'),

    path('filter/', HomeListAPIView.as_view(), name='filter'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
