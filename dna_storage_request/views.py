from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
        try:
            return Response({'mensaje': 'Formulario recibido'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )