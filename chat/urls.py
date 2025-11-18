from django.urls import path
from .views import (
     GroupUpdateAPIView,
     GroupDestroyAPIView,
     GroupChatCreateAPIView,
     GroupAddMemberAPIView,
     GroupAddAdminAPIView,
     PrivateChat,
     BlockUserAPIView,
     UnblockUserAPIView,
)


app_name = 'chat'

urlpatterns = [
    # Groups
    path('groups/', GroupChatCreateAPIView.as_view(), name='group-create'),
    path('groups/<int:group_id>/', GroupUpdateAPIView.as_view(), name='group-update'),
    path('groups/<int:group_id>/delete/', GroupDestroyAPIView.as_view(), name='group-delete'),
    path('groups/<int:group_id>/members/', GroupAddMemberAPIView.as_view(), name='group-add-member'),
    path('groups/<int:group_id>/admins/', GroupAddAdminAPIView.as_view(), name='group-add-admin'),

    # Private Chats
    path('private/<int:user_id>/', PrivateChat.as_view(), name='private-chat'),
    path('block/<int:user_id>/', BlockUserAPIView.as_view(), name='block'),
    path('unblock/<int:user_id>/', UnblockUserAPIView.as_view(), name='unblock'),
]
