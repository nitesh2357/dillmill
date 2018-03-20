from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from main.form import LoginForm, ProfileForm, ActionForm
from main.models import UserProfile, Action

# Create your views here.

## sigup api
class SignUp(View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse('Success', safe=False)
        return JsonResponse(form.errors, safe=False)

## login api
class Login(View):
    def post(self, request):
        # check if user is already signed in
        if request.user.is_authenticated():
            print request.user
            return JsonResponse('Already Signed in', safe=False)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                return JsonResponse('Username or Password is incorrect', safe=False)
            login(request, user)
            ## On successful login in we can get thier current location using geo location api
            ## to find a nearby people
            return JsonResponse('Login Successfull', safe=False)
        return JsonResponse(form.errors, safe=False)

# logged user can update thier profile
class UpdateProfile(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse('Login to Update your profile', safe=False)
        form = ProfileForm(request.POST, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return JsonResponse('profile updated for %s' % (request.user), safe=False)
        return JsonResponse(form.errors, safe=False)

# logged user can view thier profile
class Profile(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse('Login to View your profile', safe=False)
        queryset = get_object_or_404(UserProfile, user=request.user)
        response = {
            'first_name': queryset.first_name,
            'last_name': queryset.last_name,
            'email': queryset.email,
            'date_of_birth': queryset.date_of_birth,
            'bio': queryset.bio,
            'age': queryset.age,
            'gender': queryset.gender
        }

        return JsonResponse(response, safe=False)


class Logout(View):
    def get(self, request):
        logout(request)
        return JsonResponse('Logout Sucessful', safe=False)


class Search(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse('Login to View Search Result', safe=False)
        ## search algorithm
        ## return list of profile found using search algorithm excluding the one's already liked or disliked

        ## for the purpose of demo returing list of all profile except the userprofile

        queryset = UserProfile.objects.all().exclude(user=request.user)
        result = [{
            'first_name': item.first_name,
            'last_name': item.last_name,
            'bio': item.bio,
            'age': item.age,
        } for item in queryset]

        return JsonResponse(result, safe=False)

# lisk or dislike api
class Swipe(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse('Login to View Search Result', safe=False)
        form = ActionForm(request.POST)
        if form.is_valid():
            other_person_user_id = form.cleaned_data.get('other_person_user_id')
            # this check is not required but for demo I am manualy entering id so i kept this
            if other_person_user_id == request.user.id:
                return JsonResponse('Please enter other person id', safe=False)
            try:
                action = form.save(commit=False)
                action.user = request.user
                try:
                    # check if other person has also like this person then it's a match
                    queryset = Action.objects.get(user_id=other_person_user_id, other_person_user_id=request.user.id,
                                                      like=True)
                    queryset.matched = True
                    action.matched = True
                    queryset.save()
                    action.save()
                    return JsonResponse('Congrates you have been matched', safe=False)
                except Action.DoesNotExist:
                    action.save()
                if action.like:
                    return JsonResponse('You liked the person', safe=False)
                else:
                    return JsonResponse('You are not interested in person', safe=False)
            except IntegrityError:
                return JsonResponse('Already Swiped', safe=False)
        return JsonResponse(form.errors, safe=False)

# see the person you are matched with
class MatchedList(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse('Login to View Matched Result', safe=False)
        queryset = UserProfile.objects.filter(user__action__user=request.user, user__action__matched=True)
        result = [{
            'id': item.user_id,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'bio': item.bio,
            'age': item.age,
        } for item in queryset]

        return JsonResponse(result, safe=False)


class UpdatePreference(View):
    def post(self, request):
        ## api to update the user preference for a better search
        pass


class Unmatch(View):
    def post(self, request):
        ## api to unmatch a person
        pass

