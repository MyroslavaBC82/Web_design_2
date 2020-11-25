from django.urls import path, include
from rest_framework import routers
from .views import DroneViewSet, GetDronesView, GetdroneInfoView

app_name = 'drone'

urlpatterns = [
    path('', GetDronesView.as_view(), name='view_drones'),
    path('<int:pk>/info/', GetdroneInfoView.as_view(), name='get_drone_info'),

]

router = routers.DefaultRouter()
router.register('list', DroneViewSet)

urlpatterns += router.urls

