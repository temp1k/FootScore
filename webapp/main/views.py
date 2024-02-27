from django.shortcuts import render


# Create your views here.
def index(request):
    data = {
        'title': 'Главная страница',
        'description': 'Наш сайт предоставляет информацию о различных футбольных лигах со всего мира. Посетители могут найти расписание матчей, результаты игр, информацию о командах и игроках, текущие таблицы лиг, а также новости и статистику. Сайт также может предоставлять возможность регистрации пользователей, подписки на уведомления о матчах и многое еще будет.'
    }
    return render(request, 'main/index.html', data)


def about(request):
    return render(request, 'main/about.html')
