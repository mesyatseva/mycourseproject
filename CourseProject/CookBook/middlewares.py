from .models import Kitchen, Dish

"""Посредник (middleware) Django - это программный модуль, выполняющий предварительную обработку клиентского запроса 
перед передачей его контроллеру, а также окончательную обработку ответа, сгенерированного контроллером. Список
посредников, зарегистрированных в проекте, указывается в параметре MIDDLEWARE (Дронов В.А., Джанго 2.1)"""


def cookbook_context_proccesor(request):
    """Обработчик контекста, в котором формируется список кухней"""
    context = {}
    context['kitchens'] = Kitchen.objects.all()
    context['dishes'] = Dish.objects.all()
    context['keyword'] = ''
    context['all'] = ''

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']

    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
