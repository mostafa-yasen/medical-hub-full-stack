from django.shortcuts import render, redirect
from .models import Community, Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
        # user = User.objects.get(request.POST['user_id'])
        community = Community.objects.get(pk=community_id)

        post = Post(
            creator=request.user,
            community=community,
            content=content
            )
        post.save()

        print('=' * 50)
        print(post)

        return redirect('/communities/%s' % community_id)

    print('=' * 50)
    print('Get Request')
    print('=' * 50)

    return redirect('/home/')