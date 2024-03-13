"""
Core views for app
"""
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


@extend_schema(tags=["health-check"])
@api_view(["GET"])
def health_check(request):
    """Returns succesful response."""
    return Response({"healthy": True})
