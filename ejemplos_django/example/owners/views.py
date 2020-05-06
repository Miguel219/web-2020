import math
from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from owners.models import Owner
from owners.serializers import OwnerSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='PetPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated,
                    'list': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': lambda user, req: user.is_authenticated,
                    'destroy': lambda user, req: user.is_authenticated,
                    'update': True,
                    'partial_update': 'owner.change_owner',


                }
            }
        ),
    )

    def perform_create(self, serializer):
        pet = serializer.save()
        user = self.request.user
        assign_perm('owner.change_owner', user, pet)
        return Response(serializer.data)