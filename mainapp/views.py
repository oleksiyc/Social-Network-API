from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from mainapp.models import Member, Profile, Message
from rest_framework import viewsets
from mainapp.serializers import MemberSerializer
from mainapp.serializers import MessageSerializer
from mainapp.serializers import ProfileSerializer

appname = 'Social Network'

class MemberViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# decorator that tests whether user is logged in
def loggedin(f):
    def test(request):
        if 'username' in request.session:
            return f(request)
        else:
            return render(request, 'mainapp/not-logged-in.html', {})
    return test

def index(request):
    context = {
        'appname': appname,
    }
    return render(request, 'mainapp/index.html', context)

def signup(request):
    context = { 'appname': appname }
    return render(request, 'mainapp/signup.html', context)

def register(request):
    u = request.POST['username']
    p = request.POST['password']
    user = Member(username=u, password=p)
    user.save()
    context = {
        'appname': appname,
        'username' : u
    }
    return render(request, 'mainapp/user-registered.html', context)

def login(request):
    if 'username' not in request.POST:
        context = { 'appname': appname }
        return render(request, 'mainapp/login.html', context)
    else:
        u = request.POST['username']
        p = request.POST['password']
        try:
            member = Member.objects.get(pk=u)
        except Member.DoesNotExist:
            return HttpResponse("User does not exist")
        if p == member.password:
            request.session['username'] = u;
            request.session['password'] = p;
            return render(request, 'mainapp/login.html', {
                'appname': appname,
                'username': u,
                'loggedin': True}
            )
        else:
            return HttpResponse("Wrong password") 

@loggedin
def friends(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    # list of people I'm following
    following = member_obj.following.all()
    # list of people that are following me
    followers = Member.objects.filter(following__username=username)
    # render reponse
    context = {
        'appname': appname,
        'username': username,
        'members': members,
        'following': following,
        'followers': followers,
        'loggedin': True
    }
    return render(request, 'mainapp/friends.html', context)

@loggedin
def logout(request):
    if 'username' in request.session:
        u = request.session['username']
        request.session.flush()        
        context = {
            'appname': appname,
            'username': u
        }
        return render(request, 'mainapp/logout.html', context)
    else:
        raise Http404("Can't logout, you are not logged in")

def member(request, view_user):
    username = request.session['username']
    member = Member.objects.get(pk=view_user)

    if view_user == username:
        greeting = "Your"
    else:
        greeting = view_user + "'s"

    if member.profile:
        text = member.profile.text
    else:
        text = ""
    return render(request, 'mainapp/member.html', {
        'appname': appname,
        'username': username,
        'view_user': view_user,
        'greeting': greeting,
        'profile': text,
        'loggedin': True}
        )

@loggedin
def members(request):
    username = request.session['username']
    member_obj = Member.objects.get(pk=username)
    # follow new friend
    if 'add' in request.GET:
        friend = request.GET['add']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.add(friend_obj)
        member_obj.save()
    # unfollow a friend
    if 'remove' in request.GET:
        friend = request.GET['remove']
        friend_obj = Member.objects.get(pk=friend)
        member_obj.following.remove(friend_obj)
        member_obj.save()
    # view user profile
    if 'view' in request.GET:
        return member(request, request.GET['view'])
    else:
        # list of all other members
        members = Member.objects.exclude(pk=username)
        # list of people I'm following
        following = member_obj.following.all()
        # list of people that are following me
        followers = Member.objects.filter(following__username=username)
        # render reponse
        return render(request, 'mainapp/members.html', {
            'appname': appname,
            'username': username,
            'members': members,
            'following': following,
            'followers': followers,
            'loggedin': True}
            )

@loggedin
def profile(request):
    u = request.session['username']
    member = Member.objects.get(pk=u)
    if 'text' in request.POST:
        text = request.POST['text']
        if member.profile:
            member.profile.text = text
            member.profile.save()
        else:
            profile = Profile(text=text)
            profile.save()
            member.profile = profile
        member.save()
    else:
        if member.profile:
            text = member.profile.text
        else:
            text = ""
    return render(request, 'mainapp/profile.html', {
        'appname': appname,
        'username': u,
        'text' : text,
        'loggedin': True}
        )

@loggedin
def messages(request):
    username = request.session['username']
    user = Member.objects.get(pk=username)
    # Whose message's are we viewing?
    if 'view' in request.GET:
        view = request.GET['view']
    else:
        view = username
    recip = Member.objects.get(pk=view)
    # If message was deleted
    if 'erase' in request.GET:
        msg_id = request.GET['erase']
        Message.objects.get(id=msg_id).delete()
    # If text was posted then save on DB
    if 'text' in request.POST:
        text = request.POST['text']
        pm = request.POST['pm'] == "0"
        message = Message(user=user,recip=recip,pm=pm,time=timezone.now(),text=text)
        message.save()
    messages = Message.objects.filter(recip=recip)
    profile_obj = Member.objects.get(pk=view).profile
    profile = profile_obj.text if profile_obj else ""
    return render(request, 'mainapp/messages.html', {
        'appname': appname,
        'username': username,
        'profile': profile,
        'view': view,
        'messages': messages,
        'loggedin': True}
        )

def regCheckUser(request):
    if 'username' in request.POST:
        u = request.POST['username']
        try:
            member = Member.objects.get(pk=u)
            return HttpResponse("<span class='taken'>&nbsp;&#x2718; This username is taken</span>")
        except Member.DoesNotExist:
            return HttpResponse("<span class='available'>&nbsp;&#x2714; This username is available</span>")
    else:
        return HttpResponse("Expected 'username' in request")

def logCheckUser(request):
    if 'username' in request.POST:
        u = request.POST['username']
        try:
            member = Member.objects.get(pk=u)
            return HttpResponse("<span class='available'>&nbsp;&#x2714; Valid username</span>")
        except Member.DoesNotExist:
            return HttpResponse("<span class='taken'>&nbsp;&#x2718; Unknown username</span>")
    else:
        return HttpResponse("")
