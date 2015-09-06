__author__ = 'ansun'

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from requests import HTTPError

from social import __version__ as version
from social.apps.django_app.default.models import UserSocialAuth
from test_app.utils import load_signed_request

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('home.html', {'version': version},
                                  RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    user = request.user
    social = user.social_auth.get(provider='facebook')
    userid = social.uid
    ctx = {
        'facebook_id' : userid,
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('done.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))



def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def deauth(request):
    data = request.POST
    if 'signed_request' in data:
        parsed_data = load_signed_request(data['signed_request'])
        facebook_user = UserSocialAuth.objects.get(uid=parsed_data['user_id'])
        facebook_user.user.is_active = False
        facebook_user.user.save()
    return HttpResponseRedirect('/')
