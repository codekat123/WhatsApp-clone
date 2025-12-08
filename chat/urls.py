from django.urls import path
from .views import (
     GroupUpdateAPIView,
     GroupDestroyAPIView,
     GroupChatCreateAPIView,
     GroupAddMemberAPIView,
     GroupAddAdminAPIView,
     PrivateChat,
     ChatListPerUser,
     ToggleBlockAPIView,

)


app_name = 'chat'

urlpatterns = [
    # Groups
    path('groups/', GroupChatCreateAPIView.as_view(), name='group-create'),
    path('groups/<int:group_id>/', GroupUpdateAPIView.as_view(), name='group-update'),
    path('groups/<int:group_id>/delete/', GroupDestroyAPIView.as_view(), name='group-delete'),
    path('groups/members/', GroupAddMemberAPIView.as_view(), name='group-add-member'),
    path('groups/admins/', GroupAddAdminAPIView.as_view(), name='group-add-admin'),

    # Private Chats
    path('private/<int:user_id>/', PrivateChat.as_view(), name='private-chat'),
    path('block/<int:user_id>/', ToggleBlockAPIView.as_view(), name='block'),
    path('list/',ChatListPerUser.as_view(),name='chat-list'),
]
