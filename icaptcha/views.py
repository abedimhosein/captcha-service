from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from icaptcha.models import Captcha
from icaptcha.serializers import CaptchaSerializer


@api_view()
def captcha_load(request):
    new_captcha = Captcha.objects.create()
    serializer = CaptchaSerializer(new_captcha, context={'request': request})
    return Response(serializer.data)


@api_view()
def captcha_download(request, pub_id: str):
    target_captcha = Captcha.objects.get_by_pub_id(pub_id=pub_id)
    if target_captcha:
        opened_file = open(target_captcha.image.path, mode='rb')
        return FileResponse(opened_file, as_attachment=True)


@api_view(['POST'])
def captcha_solve(request):
    pub_id = str(request.POST['pub_id'])
    user_input = str(request.POST['user_input'])

    target_captcha = Captcha.objects.get_by_pub_id(pub_id=pub_id)
    if target_captcha:
        private_id = target_captcha.pri_id
        target_captcha.delete()

        if private_id == user_input:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_404_NOT_FOUND)
