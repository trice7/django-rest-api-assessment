"""View module for handling requests for artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist

class ArtistView(ViewSet):
  """Tuna Piano Artist View"""
  
  def retrieve(self, request, pk):
    """Handle GET request for single artist
    
    Returns -> Response -- JSON serialized artist"""
    
    try:
      artist = Artist.objects.get(pk=pk)
      serializer = ArtistSerializer(artist)
      return Response(serializer.data)
    except Artist.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests for all artists
    
    Returns -> Response -- JSON serialized list of artists"""

class ArtistSerializer(serializers.ModelSerializer):
  """JSON serializer for artists"""
  class Meta:
    model = Artist
    fields = ('id', 'name', 'age', 'bio')
