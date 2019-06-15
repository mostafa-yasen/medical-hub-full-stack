from django.shortcuts import render, redirect
from .models import Community
from django.contrib.auth.decorators import login_required


@login_required
def communities(request):
    if request.user.is_authenticated:
        print(request.user)
        communities = Community.objects.all()

        context = {
            'communities': communities
        }
        return render(request, 'communities.html', context=context)
    else:
        # User Not Authenticated
        print('0' * 50)
        print('User Not Authenticated')
        return redirect('/')