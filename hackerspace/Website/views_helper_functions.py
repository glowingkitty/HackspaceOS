# by Marco Bartsch


def JSON_RESPONSE_more_results(request, template_path, queryset):
    print('LOG: JSON_RESPONSE_more_results(request,queryset)')
    from django.http import JsonResponse
    from django.template.loader import get_template

    start_from = int(request.GET.get('from', None))
    upt_to = int(start_from+10)

    return JsonResponse({
        'html': get_template('components/body/'+template_path).render({
            'all_results': queryset[start_from:upt_to]
        }),
        'continue_from': upt_to,
        'more_results': True if queryset.count() > upt_to else False
    })
