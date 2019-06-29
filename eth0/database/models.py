from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    # Post contents
    title = models.CharField(default="", max_length=50)
    postedBy = models.CharField(default="", max_length=50)
    body = models.CharField(null=True, max_length=500)
    url = models.CharField(null=True, max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    # Post type for template renders
    type = models.CharField(default="txt", max_length=10)

    # Post interactions
    upvotes = models.ManyToManyField(User, related_name='postUpvotes')
    downvotes = models.ManyToManyField(User, related_name='postDownvotes')
    
    def voteNum(self):
        return self.upvotes.count() - self.downvotes.count()

class Comment(models.Model):
    # Foreign key for post
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    # Comment contents
    postedBy = models.CharField(max_length=200)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    # Comment interactions
    upvotes = models.ManyToManyField(User, related_name='commentUpvotes')
    downvotes = models.ManyToManyField(User, related_name='commentDownvotes')

    def voteNum(self):
        return self.upvotes.count() - self.downvotes.count()
