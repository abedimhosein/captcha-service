from rest_framework import serializers
from icaptcha.models import Captcha
from django.urls import reverse

class CaptchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captcha
        fields = ['pub_id', 'captcha_url']

    captcha_url = serializers.SerializerMethodField(method_name='get_captcha_url')

    def get_captcha_url(self, obj: Captcha):
        request = self.context.get('request')

        return request.build_absolute_uri(f"{reverse('icaptcha:download', kwargs={'pub_id': obj.pub_id})}")
