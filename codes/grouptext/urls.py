from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'TextGroups', views.TextGroupViewSet)
router.register(r'TextGroupMember', views.TextGroupMemberViewSet)
router.register(r'TextQuestion', views.TextQuestionViewSet)
router.register(r'TextMessage', views.TextMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'add_group_member/<int:group_id>/', views.add_group_member),
    path(r'view_groups_members/', views.get_groups_and_members),
    path(r'ask_group_question/<int:group_id>/', views.ask_group_question),
    path(r'send_sms', views.send_sms),
    # path(r'sms_final_status', views.sms_final_status),
    path('api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]
