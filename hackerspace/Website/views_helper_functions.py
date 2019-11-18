# by Marco Bartsch


def JSON_RESPONSE_more_results(request, template_path, queryset):
    print('LOG: JSON_RESPONSE_more_results(request,queryset)')
    from django.http import JsonResponse
    from django.template.loader import get_template

    # see if request comes from a guilde/space page, then show guilde/space events, not all events
    if request.GET.get('origin', None):
        if 'guilde/' in request.GET.get('origin', None):
            queryset = queryset.filter(
                one_guilde__str_slug=request.GET.get('origin', None)[1:])
        elif 'space/' in request.GET.get('origin', None):
            queryset = queryset.filter(
                one_space__str_slug=request.GET.get('origin', None)[1:])

    start_from = int(request.GET.get('from', None))
    upt_to = int(start_from+10)

    return JsonResponse({
        'html': get_template('components/body/'+template_path).render({
            'all_results': queryset[start_from:upt_to],
            'specific_selector': request.GET.get('specific_selector', None)
        }),
        'continue_from': upt_to,
        'more_results': True if queryset.count() > upt_to else False
    })
