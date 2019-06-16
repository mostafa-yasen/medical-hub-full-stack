from django.shortcuts import render, redirect
from .models import Community, Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

@login_required
def communities(request):
    if request.user.is_authenticated:
        print(request.user)
        communities = Community.objects.all()

        context = {
            'communities': communities.reverse()
        }
        return render(request, 'communities.html', context=context)
    else:
        # User Not Authenticated
        print('0' * 50)
        print('User Not Authenticated')
        return redirect('/')

@login_required
def community(request, pk):
    community = Community.objects.get(pk=pk)
    posts = Post.objects.filter(community=community)

    for post in posts:
        post.calcComments()
        post.save()


    if community is None:
        print('Community Not Found.')
        return redirect('/communities/')

    context = {
        'community': community,
        'posts': posts
    }

    return render(request, 'community.html', context=context)


@login_required
def create_post(request, community_id):
    if request.method == 'POST':
        
        content = request.POST['post_content']
        community = Community.objects.get(pk=community_id)

        post = Post(
            creator=request.user,
            community=community,
            content=content
            )
        post.save()

        return redirect('/communities/%s' % community_id)

    return redirect('/communities/%s' % community_id)


@login_required
def getComments(request, community_id, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    creator = post.creator

    data = {
        'post': serializers.serialize('json', [post]),
        'creator': serializers.serialize('json', [creator]),
        'comments': serializers.serialize('json', comments)
    }

    return JsonResponse(data)

@login_required
def addComment(request, community_id, post_id):

    comment_content = request.POST['comment_text']
    user = request.user
    post = Post.objects.get(id=request.POST['post_id'])
    
    comment = Comment(creator=user, post=post, content=comment_content)
    comment.save()
    
    post.calcComments()
    post.save()

    print('=' * 50)
    print(comment)

    return redirect('/communities/' + str(community_id))

@login_required
def like(request, community_id, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        if request.POST['operation'] == 'like':
            post.likes += 1
        else:
            post.likes -= 1
        
        post.save()

        return JsonResponse({'success':'True'})

