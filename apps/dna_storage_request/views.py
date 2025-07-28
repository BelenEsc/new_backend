from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Requester, Request, DnaAliquot
from .serializers import RequesterSerializer, DnaAliquotSerializer


class HomeView(APIView):
    def get(self, request):
        return Response({'mensaje': 'Bienvenido a la API'})

class MensajeView(APIView):
    def get(self, request):
        return Response({'mensaje': 'Hola desde Django'})

    def post(self, request):
        return Response({'mensaje': 'Datos recibidos'}, status=status.HTTP_200_OK)

class StorageRequestView(APIView):
    def post(self, request):
        requester_serializer = RequesterSerializer(data=request.data)
        if requester_serializer.is_valid():
            requester_serializer.save()
            return Response(requester_serializer.data, status=status.HTTP_201_CREATED)
        return Response(requester_serializer.errors, status=status.HTTP_400_BAD_REQUEST)