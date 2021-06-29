from rest_framework import generics, permissions

from .models import Wallet
from .serializers import WalletSerializer


class WalletListCreate(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Wallet.objects.all()


class WalletRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Wallet.objects.all()
    http_method_names = ('get', 'patch', 'delete', 'head', 'options',)
