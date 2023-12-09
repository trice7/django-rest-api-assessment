"""View module for handling requests for artists"""
from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Song

class ArtistView(ViewSet):
  """Tuna Piano Artist View"""
  
  def retrieve(self, request, pk):
    """Handle GET request for single artist
    
    Returns -> Response -- JSON serialized artist"""
    
    try:
      artist = Artist.objects.annotate(song_count = Count('song_list')).get(pk=pk)
      artist.songs = Song.objects.filter(artist_id = artist.pk)
      serializer = SingleArtistSerializer(artist)
      return Response(serializer.data)
    except Artist.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests for all artists
    
    Returns -> Response -- JSON serialized list of artists"""
    
    try:
      artists = Artist.objects.all()
      serializer = ArtistSerializer(artists, many=True)
      return Response(serializer.data)
    except Artist.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def create(self, request):
    """Handle POST operations for artists
    
    Returns -> JSON serialized artist instance with a status of 201"""
    
    artist = Artist.objects.create(
      name = request.data['name'],
      age = request.data['age'],
      bio = request.data['bio'],
    )
    
    serializer = ArtistSerializer(artist)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    """Handles PUT request for an artist
    
    Returns -> JSON serialized artist with 200 status code"""
    
    artist = Artist.objects.get(pk=pk)
    artist.name = request.data['name']
    artist.age = request.data['age']
    artist.bio = request.data['bio']
    
    artist.save()
    
    serializer = ArtistSerializer(artist)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    """Handles Delete request for an artist
    
    Returns -> Empty body with 204 status code"""
    artist = Artist.objects.get(pk=pk)
    artist.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  

class SongSerializer(serializers.ModelSerializer):
  """JSON serializer for songs"""
  class Meta:
    model = Song
    fields = ('id', 'title', 'album', 'length')
class ArtistSerializer(serializers.ModelSerializer):
  """JSON serializer for artists"""
  class Meta:
    model = Artist
    fields = ('id', 'name', 'age', 'bio')
    

class SingleArtistSerializer(serializers.ModelSerializer):
  """JSON serializer for artists"""
  song_count = serializers.IntegerField(default=None)
  songs = SongSerializer(many=True)
  class Meta:
    model = Artist
    fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
