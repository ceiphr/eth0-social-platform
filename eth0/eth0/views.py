from django.shortcuts import render
from django.views.generic.base import View
from database.models import Post, Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import json

############################################
# Template Views
############################################

def sortBy(posts, type):
    toBeSorted = []
    res = []
    if type == "new":
        for post in posts:
            toBeSorted.append(post.created_date)
        sortedPosts = sorted(toBeSorted)
        sortedPosts.reverse()
        for date in sortedPosts:
            for post in posts:
                if post.created_date == date and post not in res:
                    res.append(post)

    elif type == "con":
        toBeSorted = []
        for post in posts:
            conVal = abs(post.upvotes.count() - post.downvotes.count())
            toBeSorted.append(conVal)
        sortedPosts = sorted(toBeSorted)
        for votes in sortedPosts:
            for post in posts:
                conVal = abs(post.upvotes.count() - post.downvotes.count())
                if conVal == votes and post not in res:
                    res.append(post)

    elif type == "pop":
        toBeSorted = []
        for post in posts:
            toBeSorted.append(post.voteNum())
        sortedPosts = sorted(toBeSorted)
        sortedPosts.reverse()
        for votes in sortedPosts:
            for post in posts:
                if post.voteNum() == votes and post not in res:
                    res.append(post)
    return res
    
class FrontPage(View):
    def get(self, request, sortType="pop"):
        context = dict()
        posts = Post.objects.all()
        context["posts"] = sortBy(posts, sortType)
        return render(request, 'index.html', context)        

class PostPage(View):
    def get(self, request, postID):
        context = dict()
        post = Post.objects.get(id=postID)
        context["post"] = post
        return render(request, 'post.html', context)

############################################
# Account Views
############################################

class SignUp(View):
    def post(self, request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

############################################
# Post Views
############################################

class CreateTP(View):
    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get("title")
            body = request.POST.get("body")
            name = request.user.username
            post = Post(title=title, body=body, postedBy=name, type="txt")
            post.save()
            return HttpResponseRedirect("/")
        return HttpResponseRedirect("/accounts/login")

class CreateIVP(View):
    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get("title")
            url = request.POST.get("url")
            name = request.user.username
            post = Post(title=title, url=url, postedBy=name, type="ivc")
            post.save()
            return HttpResponseRedirect("/")
        return HttpResponseRedirect("/accounts/login")

class CreateLP(View):
    def post(self, request):
        if request.user.is_authenticated:
            title = request.POST.get("title")
            url = request.POST.get("url")
            name = request.user.username
            post = Post(title=title, url=url, postedBy=name, type="lnk")
            post.save()
            return HttpResponseRedirect("/")
        return HttpResponseRedirect("/accounts/login")

class UpvotePost(View):
    def post(self, request, postID):
        if request.user.is_authenticated:
            user = request.user
            post = Post.objects.get(id=postID)
            if user in post.upvotes.all(): 
                post.upvotes.remove(user)
            elif user in post.downvotes.all():
                post.upvotes.add(user)
                post.downvotes.remove(user)
            else: 
                post.upvotes.add(user)
            post.save()
            # https://stackoverflow.com/questions/14007453/my-own-like-button-django-ajax-how
            dvote = {'voteNum': post.voteNum()} 
            return HttpResponse(json.dumps(dvote), content_type='application/json')
        return HttpResponseRedirect("/accounts/login")

class DownvotePost(View):
    def post(self, request, postID):
        if request.user.is_authenticated:
            user = request.user
            post = Post.objects.get(id=postID)
            if user in post.downvotes.all(): 
                post.downvotes.remove(user)
            elif user in post.upvotes.all():
                post.downvotes.add(user)
                post.upvotes.remove(user)
            else: 
                post.downvotes.add(user)
            post.save()
            # https://stackoverflow.com/questions/14007453/my-own-like-button-django-ajax-how
            dvote = {'voteNum': post.voteNum()} 
            return HttpResponse(json.dumps(dvote), content_type='application/json')
        return HttpResponseRedirect("/accounts/login")

class GetCurrentPostVotes(View):
    def post(self, request):
        posts = Post.objects.all()
        voteValues, userVoted = dict(), dict()
        user = request.user
        for post in posts:
            voteValues[post.id] = post.voteNum()
            if user in post.upvotes.all():
                userVoted[post.id] = (True, "upvote")
            elif user in post.downvotes.all():
                userVoted[post.id] = (True, "downvote")
            else: 
                userVoted[post.id] = (False, None)
        return HttpResponse(json.dumps([voteValues, userVoted]), content_type='application/json')
        
class DeletePost(View):
    def get(self, request, postID):
        post = Post.objects.get(id=postID)
        if request.user.username == post.postedBy:
            post.delete()
        return HttpResponseRedirect("/")

############################################
# Comment Views
############################################

class CreateComment(View):
    def post(self, request, postID):
        if request.user.is_authenticated:
            name = request.user.username
            body = request.POST.get("body")
            post = Post.objects.get(id=postID)
            comment = Comment(postedBy=name, body=body)
            comment.post = post
            comment.save()
            return HttpResponseRedirect("/post/%s" % postID)
        return HttpResponseRedirect("/accounts/login")

class UpvoteComment(View):
    def post(self, request, postID, commentID):
        if request.user.is_authenticated:
            print("HELLO")
            user = request.user
            post = Post.objects.get(id=postID)
            comment = post.comments.get(id=commentID)
            if user in comment.upvotes.all(): 
                comment.upvotes.remove(user)
            elif user in comment.downvotes.all():
                comment.upvotes.add(user)
                comment.downvotes.remove(user)
            else: 
                comment.upvotes.add(user)
            comment.post = post
            comment.save()
            # https://stackoverflow.com/questions/14007453/my-own-like-button-django-ajax-how
            dvote = {'voteNum': comment.voteNum()} 
            return HttpResponse(json.dumps(dvote), content_type='application/json')
        return HttpResponseRedirect("/accounts/login")

class DownvoteComment(View):
    def post(self, request, postID, commentID):
        if request.user.is_authenticated:
            user = request.user
            post = Post.objects.get(id=postID)
            comment = post.comments.get(id=commentID)
            if user in comment.downvotes.all(): 
                comment.downvotes.remove(user)
            elif user in comment.upvotes.all():
                comment.downvotes.add(user)
                comment.upvotes.remove(user)
            else: 
                comment.downvotes.add(user)
            comment.post = post
            comment.save()
            # https://stackoverflow.com/questions/14007453/my-own-like-button-django-ajax-how
            dvote = {'voteNum': comment.voteNum()} 
            return HttpResponse(json.dumps(dvote), content_type='application/json')
        return HttpResponseRedirect("/accounts/login")

class GetCurrentCommentVotes(View):
    def post(self, request, postID):
        post = Post.objects.get(id=postID)
        comments = post.comments.all()
        voteValues, userVoted = dict(), dict()
        user = request.user
        for comment in comments:
            voteValues[comment.id] = comment.voteNum()
            if user in comment.upvotes.all():
                userVoted[comment.id] = (True, "upvote")
            elif user in comment.downvotes.all():
                userVoted[comment.id] = (True, "downvote")
            else: 
                userVoted[comment.id] = (False, None)
        return HttpResponse(json.dumps([voteValues, userVoted]), content_type='application/json')

class DeleteComment(View):
    def get(self, request, postID, commentID):
        post = Post.objects.get(id=postID)
        comment = post.comments.get(id=commentID)
        if request.user.username == comment.postedBy:
            comment.delete()
        return HttpResponseRedirect("/post/%s" % postID)
