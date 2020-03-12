class ImageUpload():
    def __init__(self, request=None):
        from django.http import JsonResponse
        from django.template.loader import get_template

        if request.FILES['images[0]'].content_type != 'image/jpeg' and request.FILES['images[0]'].content_type != 'image/png':
            response = JsonResponse({
                'notification': get_template('components/notification.html').render({
                    'text_message': 'Please upload a JPG or PNG image.',
                    'str_icon': 'error'
                })})
            response.status_code = 500

        else:
            from _apis.models import Aws

            image_s3_url = Aws().upload(request.FILES['images[0]'])

            if image_s3_url:
                response = JsonResponse({'url_image': image_s3_url})
            else:
                response = JsonResponse(
                    {'url_image': None, 'error': '--> AWS secrets are missing. Couldnt upload image.'})

        self.value = response
