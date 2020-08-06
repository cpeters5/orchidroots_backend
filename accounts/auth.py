
from myproject import settings
import requests
import jwt
from datetime import timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
import urllib.request


class Auth(object):

    @staticmethod
    def facebook_auth(social_token, social_id):
        appLink = 'https://graph.facebook.com/oauth/access_token?client_id=' + settings.FACEBOOK_CLIENT_ID + \
            '&client_secret=' + settings.FACEBOOK_CLIENT_SECRET + \
            '&grant_type=client_credentials'
        appToken = requests.get(appLink).json()['access_token']
        link = 'https://graph.facebook.com/debug_token?input_token=' + \
            social_token + '&access_token=' + social_token
        context = dict()
        try:
            userId = requests.get(link).json()['data']['user_id']
            data = requests.get('https://graph.facebook.com/v4.0/' +
                                userId + '?access_token=' + social_token).json()
            context['Valid'] = True
            try:
                email = data['email']
            except Exception:
                data['email'] = data['id']+'@orchidroots.com'
            try:
                image_url = 'https://graph.facebook.com/' + \
                    social_id+'/picture?height=250&width=250'
                image = ContentFile(urllib.request.urlopen(image_url).read())
                data['image'] = image
            except Exception as error:
                data['image'] = None
                pass
            context['userdata'] = data
        except (ValueError, KeyError, TypeError) as error:
            context['Valid'] = False
        return context
