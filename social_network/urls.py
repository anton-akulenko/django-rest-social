from django.urls import path
from social_network.views import PostList, LikeCreate, DislikeCreate, RegisterView, \
    ProfileUserView, LikesAnalyticsAPIView, UserActivityDetailView, LoginView

urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>/like', LikeCreate.as_view()),
    path('posts/<int:pk>/dislike', DislikeCreate.as_view()),
    path('signup/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileUserView.as_view()),
    path('analytics/', LikesAnalyticsAPIView.as_view()),
    path('user-activity/<str:user__username>/', UserActivityDetailView.as_view()),
]
