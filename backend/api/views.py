from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def test_api(request):
    return Response({"message": "Django REST Framework is working!"})
