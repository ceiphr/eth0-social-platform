"""eth0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from eth0.views import *

urlpatterns = [
    # Admin paths
    path('admin/', admin.site.urls),

    # User Account paths
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Template paths
    path('', FrontPage.as_view()),
    path(r'filter=<sortType>', FrontPage.as_view()),
    path(r'post/<postID>', PostPage.as_view()),

    # Post interaction paths
    path(r'post/<postID>/upvote', UpvotePost.as_view()),
    path(r'post/<postID>/downvote', DownvotePost.as_view()),
    path(r'post/<postID>/del', DeletePost.as_view()),
    path(r'votes', GetCurrentPostVotes.as_view()),

    # Post - Comment interaction paths
    path(r'post/<postID>/<commentID>/upvote', UpvoteComment.as_view()),
    path(r'post/<postID>/<commentID>/downvote', DownvoteComment.as_view()),
    path(r'post/<postID>/<commentID>/del', DeleteComment.as_view()),
    path(r'post/<postID>/votes', GetCurrentCommentVotes.as_view()),


    # Post Creation paths
    path(r'post/<postID>/cc', CreateComment.as_view()),

    # Creation paths
    path(r'ctp', CreateTP.as_view()),
    path(r'civp', CreateIVP.as_view()),
    path(r'clp', CreateLP.as_view())
]
