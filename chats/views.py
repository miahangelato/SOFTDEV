from django.shortcuts import render
from .models import Mychats
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
# Create your views here.

@login_required
def chats(request):
    frnd_name = request.GET.get('user',None)
    mychats_data = None
    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and Mychats.objects.filter(me=request.user,frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = Mychats.objects.get(me=request.user,frnd=frnd_).chats
    frnds = User.objects.exclude(pk=request.user.id)
    return render(request,'chat/chats.html',{'my':mychats_data,'chats': mychats_data,'frnds':frnds})