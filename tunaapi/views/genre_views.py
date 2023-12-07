"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre

class GenreView(ViewSet):
  """Tuna Piano Genre View"""
  
  def retrieve(self, request, pk):
    """Handle GET requests for single genre
    
    Returns -> Response -- JSON serialized genre"""
    
    try:
      genre = Genre.objects.get(pk=pk)
      serializer = GenreSerializer(genre)
      return Response(serializer.data)
    except Genre.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests for all genres
    
    Returns -> Response -- JSON serialized list of genres"""
    
    try:
      genres = Genre.objects.all()
      serializer = GenreSerializer(genres, many=True)
      return Response(serializer.data)
    except Genre.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def create(self, request):
    """Handle POST operations for genres
    
    Returns -> JSON serialized genre instance"""
    
    genre = Genre.objects.create(
      description=request.data["description"],
    )
    
    serializer = GenreSerializer(genre)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Handle PUT request for a genre
    
    Returns -> Empty body with 204 status code"""
    
    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    genre.save()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
    
      

class GenreSerializer(serializers.ModelSerializer):
  """JSON serializer for genres"""
  class Meta:
    model= Genre
    fields= ('id', 'description')
