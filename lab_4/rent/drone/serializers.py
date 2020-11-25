from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Drone, Gallery, Model


class modelSerializer(Serializer):
    # drones = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Model
        fields = '__all__'
        depth = 2


class droneSerializer(ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
        depth = 2


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


