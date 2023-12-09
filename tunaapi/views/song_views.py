"""View module for handling request for songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre, SongGenre

class SongView(ViewSet):
  """Tuna Piano Song View"""
  
  def retrieve(self, request, pk):
    """Handle GET request for single song
    
    Returns -> Response -- JSON serialized song, status 200"""
    
    try:
      song = Song.objects.get(pk=pk)
      genre_list = SongGenre.objects.filter(song_id = song.pk)
      
      genres = []
      for e in genre_list:
        genres.append(e.genre_id_id)
      
      song.genres = Genre.objects.filter(pk__in = genres)
      serializer = SingleSongSerializer(song)
      return Response(serializer.data)
    except Song.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests for all songs
    
    Returns -> JSON serialized list of songs. Status 200"""
    
    try:
      songs = Song.objects.all()
      serializer = SongSerializer(songs, many=True)
      return Response(serializer.data)
    except Song.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def create(self, request):
    """Handle POST operations for songs
    
    Returns -> JSON serialized song instance with a status of 201"""
    
    artist_id = Artist.objects.get(pk=request.data['artist_id'])
    
    song = Song.objects.create(
      title = request.data['title'],
      artist_id = artist_id,
      album = request.data['album'],
      length = request.data['length'],
    )
    
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    """Handles PUT request for a song
    
    Returns -> JSON serialized son with 200 status code"""
    
    song = Song.objects.get(pk=pk)
    
    artist_id = Artist.objects.get(pk=request.data['artist_id'])
    
    song.title = request.data['title']
    song.artist_id = artist_id
    song.album = request.data['album']
    song.length = request.data['length']
    
    song.save()
    serializer = SongSerializer(song)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    """Handles Delete request for a song
    
    Returns -> Empty body with a 204 status"""
    
    song = Song.objects.get(pk=pk)
    song.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class GenreSerializer(serializers.ModelSerializer):
  """JSON serializer for genres"""
  class Meta:
    model= Genre
    fields= ('id', 'description')
  
# class SongGenreSerializer(serializers.ModelSerializer):
#   genre = GenreSerializer()
#   class Meta:
#     model= SongGenre
#     fields=('genre',)
#     depth = 1

class SongSerializer(serializers.ModelSerializer):
  """JSON serializer for songs"""
  class Meta:
    model = Song
    fields = ('id', 'title', 'artist_id', 'album', 'length')

class SingleSongSerializer(serializers.ModelSerializer):
  """JSON serializer for songs"""
  genres = GenreSerializer(many=True)
  class Meta:
    model = Song
    fields = ('id', 'title', 'artist_id', 'album', 'length', 'genres')
    depth = 1
