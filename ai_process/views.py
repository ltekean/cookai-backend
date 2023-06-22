from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageUploadSerializer

from roboflow import Roboflow

import os

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_serializer = ImageUploadSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            
            rf = Roboflow(api_key=os.environ.get("RF_API_KEY"))
            project = rf.workspace().project("cookai")
            model = project.version("3").model
            
            image_file = image_serializer.validated_data["image"]
            
            prediction = model.predict(image_file.path, confidence=40, overlap=30).json()
        
            return Response({"result":prediction}, status=201)
        else:
            return Response(image_serializer.errors, status=400)