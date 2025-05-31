# app/api/views.py
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.api.serializers import ProjekPushSerializer

@api_view(['POST'])
def receive_project_data(request):
    """
    Endpoint for external systems to PUSH a single project payload.
    Accepts JSON body matching ProjekPushSerializer.
    """
    serializer = ProjekPushSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the upsert happens atomically (esp. if you’ll receive concurrent pushes)
    with transaction.atomic():
        obj, created = serializer.create_or_update()

    return Response(
        {
            'status' : 'success',
            'action' : 'created' if created else 'updated',
            'id'     : obj.id_projek,
        },
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )
