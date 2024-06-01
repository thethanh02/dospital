from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import Account
from .serializers import AccountSerializer
from .filters import AccountFilter

@api_view(['POST'])
def batch_user_info(request):
    user_ids = request.data.get('user_ids', [])
    users = Account.objects.filter(id__in=user_ids)
    serializer = AccountSerializer(users, many=True)
    user_info = {user['id']: user for user in serializer.data}
    return Response(user_info)

@api_view(['GET'])
def get_me(request):
    users = Account.objects.get(id=request.user.pk)
    serializer = AccountSerializer(users)
    return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filterset_class = AccountFilter