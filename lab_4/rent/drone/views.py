from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from .models import drone, Gallery, Model
from .serializers import droneSerializer, GallerySerializer, modelSerializer


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class DroneViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = droneSerializer
    queryset = drone.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('^name', '^model__name')

    def get_queryset(self):
        if 'year_from' in self.request.query_params:
            year_from = self.request.query_params.get('year_from')
            year_to = self.request.query_params.get('year_to')
            return self.queryset.filter(available__exact=True) \
                .filter(model_year__gte=year_from) \
                .filter(model_year__lte=year_to)

        elif 'price_from' in self.request.query_params:
            price_from = self.request.query_params.get('price_from')
            price_to = self.request.query_params.get('price_to')
            return self.queryset.filter(available__exact=True) \
                .filter(price_hourly__gte=price_from) \
                .filter(price_hourly__lte=price_to)

        elif self.request.query_params.get('top_rated'):
            return self.queryset.filter(available__exact=True) \
                .filter(rate__exact=5)

        elif 'fuel_type' in self.request.query_params:
            fuel_type = self.request.query_params.get('fuel_type')
            return self.queryset.filter(available__exact=True) \
                .filter(engine__fuel_type__name__exact=fuel_type)
        return self.queryset.filter(available=True)

    @action(methods=['get'], detail=True)
    def gallery(self, request, pk):
        drone = self.get_object()
        if drone is not None:
            queryset = Gallery.objects.filter(drone=drone)
            serializer = GallerySerializer(instance=queryset, many=True)
            drone_list = serializer.data
            return Response(drone_list)
        if 'drone_list' in cache and drone is None:
            drone_list = cache.get('drone_list')
        else:
            queryset = Gallery.objects.filter(drone=drone)
            queryset = Gallery.objects.all()
            serializer = GallerySerializer(instance=queryset, many=True)
            drone_list = serializer.data
            cache.set('drone_list', drone_list, timeout=CACHE_TTL)
        # return Response([])
        return Response(data=drone_list)


class GetDronesView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'drone/view_drones.html'

    def get(self, request):
        brands = Model.objects.all()
        # return TemplateHTMLRenderer()
        # return Response()
        return Response(data={'brands': brands})
        # return Response(modelSerializer(instance=brands).data)


class GetdroneInfoView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'drone/get_drone_info.html'

    def get(self, request, pk=None):
        return Response()





