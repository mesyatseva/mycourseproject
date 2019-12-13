from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.db.models import Count

from django.contrib.auth.decorators import login_required

"""Вызов наших собственных моделей которых мы создали"""
from .models import Recipe, CBUser, Kitchen, Dish, BookLikedRecipesAndUser

"""Высокоуровневный класс"""
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordChangeView, PasswordChangeDoneView

"""Выоскоуровневый параметр для класса регистрации/изменений пользовательских данных"""
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView

"""Вызов форм"""
from .forms import RegisterUserForm, RecipeForm, ChangeUserInfoForm, CommentForm, SmallSearchForm
from CookBook.сhoices import difficulty_choices, cooktime_choices


# Create your views here
# Вывод на главную страницу
def index(request):
    last_recipes = Recipe.objects.all()[:6]
    context = {
        'last_recipes': last_recipes,
        'difficulty_choices': difficulty_choices,
        'cooktime_choices': cooktime_choices
    }
    return render(request, 'CookBook/index.html', context)


def other_page(request, page):
    try:
        template = get_template('CookBook/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


# Вход - написан для высокоуровневого класса
class CBLoginView(LoginView):
    template_name = 'CookBook/login.html'
    login_url = 'login'


@login_required(login_url='')
def loginSuccessfull(request):
    return render(request, 'CookBook/index.html')


class CBLogoutView(LogoutView):
    template_name = 'CookBook/logout.html'


class CBPasswordResetView(PasswordResetView):
    template_name = 'CookBook/registration/uhjkl/password_reset_form.html'


class CBPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'CookBook/registration/uhjkl/password_reset_done.html'
    # success_url = reverse_lazy('accounts/password-reset/done/')


# Регистрация
class RegisterUserView(CreateView):
    model = CBUser
    template_name = 'CookBook/registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('CookBook:register_done')


# Успешная регистрация
class RegisterDoneView(TemplateView):
    template_name = 'CookBook/registration/register_done.html'


# Веб-страница правки основных сведений - контроллер выполняет правку => логический ход
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """"Включаем, какая модель требуется - CBUser - для изменения данных. Также добавим форму обработки данных"""
    model = CBUser  # Какие данные применяются
    template_name = 'CookBook/change_user_info.html'  # В каком шаблоне будет работать данный контроллер
    form_class = ChangeUserInfoForm  # Форма обработки данных на основе модели
    success_url = reverse_lazy('CookBook:profile')  # Если успешно, то попадем на страницу профиля
    success_message = 'Личные данные пользователя успешно изменены'  # Выводится сообщении об успешном выполнении операции

    def dispatch(self, request, *args, **kwargs):
        """ Контроллер должен извлечь из модели CBUser запись, представляющую текущего пользователя =>
         получим ключ пользователя. Ключ хранится в атрибуте user объекта запроса => используем метод dispatch().
         Метод наследуется всеми контроллерами-классами от их общего суперкласса View(). Метод выполняет в самом начале исполнении
         контроллера. Извлечем ключ пользователя и сохраним в атрибуте user_id"""
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Извлечение исправляемой записи проводится в методе get_object(). В методе учитываем тот момент, что набор
        записей, из которого следует извлечь искомую запись, может быть, передан методу с параметром queryset. В противном случае
        набор записей следует получить get_queryset(). После чего ищем запись, представляющего пользователя"""
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class CBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'CookBook/password_change.html'
    success_message = 'Пароль успешно изменен'
    success_url = reverse_lazy('CookBook:password_change_done')


class CBPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'CookBook/password_change_done.html'


# Функция контроллера для смены пароля
class CookBookPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """Высокоуровневый класс-контроллер, поэтому нам ничего не надо особенно писать. За нас программа выполняет
    свою работу по изменению пароля. С нашей стороны следует верно указать место на сайте, место в шаблоне. """
    template_name = 'CookBook/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя успешно изменен'


def profile(request):
    myRecipes = Recipe.objects.filter(author=request.user.pk)

    count = myRecipes.count()

    context = {
        'myRecipes': myRecipes,
        'count': count
    }
    return render(request, 'CookBook/profile.html', context)


"""Логический контроллер фильтрует рецепты в зависимости от тех или иных условий"""


def all_kitchen(request):
    all = Recipe.objects.all()

    paginator = Paginator(all, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'page': page, 'all': page.object_list}
    return render(request, 'CookBook/kitchens/allkitchens.html', context)


def kitchen_slug(request, slug):
    kitchen = get_object_or_404(Kitchen, slug=slug)
    recipes = Recipe.objects.filter(kitchen__slug=slug)

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(name__icontains=keyword) | Q(description__iexact=keyword) | Q(steps__iexact=keyword)
        recipes = recipes.filter(q)
    else:
        keyword = ''
    small_search_form = SmallSearchForm(initial={'keyword': keyword})

    paginator = Paginator(recipes, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {
        'kitchen': kitchen,
        'page': page,
        'recipes': page.object_list,
        'small_search_form': small_search_form
    }
    return render(request, 'CookBook/kitchens/any_kitchen.html', context)


def dish_slug(request, slug):
    dish = get_object_or_404(Dish, slug=slug)
    recipes = Recipe.objects.filter(dish__slug=slug)

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(name__icontains=keyword) | Q(description__iexact=keyword) | Q(steps__iexact=keyword)
        recipes = recipes.filter(q)
    else:
        keyword = ''
    small_search_form = SmallSearchForm(initial={'keyword': keyword})

    paginator = Paginator(recipes, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {
        'dish': dish,
        'page': page,
        'recipes': page.object_list,
        'small_search_form': small_search_form
    }
    return render(request, 'CookBook/dishes/dishes.html', context)


def detail(request, pk):  # убрала SLUG
    recipe = get_object_or_404(Recipe, pk=pk)
    # addimages = recipe.additionalimage_set.all()
    pk = recipe.pk
    author = request.user.pk

    comments = recipe.comments.filter(active=True)

    new_comment = None

    # if request.method == 'POST':
    comment_form = CommentForm(request.POST, request.user.pk)
    if comment_form.is_valid():
        # Создаём объект Комментарий, но пока без сохранения в БД
        new_comment = comment_form.save(commit=False)
        # Привязываем коммент к посту(рецепту)
        new_comment.recipe = recipe
        #  Сохраняем комментарий в БД
        new_comment.save()
    else:
        comment_form = CommentForm(initial={'user': request.user.pk})

    context = {
        'recipe': recipe,
        'author': author,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, 'CookBook/recipes/detail.html', context)  # ТУТ ИЗМЕНИЛА!!! RECIPE = DETAIL 21:05


"""Контроллер создания формы рецепта"""


def addRecipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save()
            return redirect('CookBook:profile')
    else:
        form = RecipeForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'CookBook/recipes/create_recipe.html', context)


'''Изменение рецепта его автором в профиле'''


def changeRecipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            return redirect('CookBook:profile')
    else:
        form = RecipeForm(instance=recipe)
    context = {'form': form}
    return render(request, 'CookBook/recipes/change_recipe.html', context)


'''Удаление рецепта его автором в профиле'''


def deleteRecipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('CookBook:profile')
    else:
        return render(request, 'CookBook/recipes/delete_recipe.html')


'''Добавление рецепта к себе в Избранное'''
'''Принцип M2M: один юзер может добавлять несколько рецептов в Избранное'''
'''А один рецепт может быть в Избранном у нескольких пользователей'''


# @login_required
# def user_likes(request):
#     count = Recipe.objects.filter(status='done').count()
#     user = request.user
#     likes = True
#     active = user.is_active
#     recipes = Recipe.objects.all()
#     title = "Избранное"
#     if not user.is_authenticated:
#         raise Http404("Авторизуйтесь, чтобы добавить")
#     recipes=[]
#     for num in Recipe.objects.all():
#         if num in user.profile.likes.all():
#             recipes.append(num)
#     return render(request, 'profile_liked.html',locals())
# def favorite_recipes(request, fav_rec):
#     recipe = get_object_or_404(Recipe, id=fav_rec)
#     if request.method == 'POST':
#         recipe.favorite.add(request.user)
#     return render(request, 'CookBook/registration/profile_liked.html')

def search(request):
    query_set_recipes = Recipe.objects.order_by('-created_at')

    # Поиск, где name="recept" см. в index.html или search.html
    if 'recept' in request.GET:
        recept = request.GET['recept']
        if ['recept']:
            query_set_recipes = query_set_recipes.filter(name__icontains=recept)

    # food_keyword - Ингредиент. Рассчитываем, что пока слово содержится в текстовом поле модели (steps)
    if 'food_keyword' in request.GET:
        food_keyword = request.GET['food_keyword']
        if ['food_keyword']:
            query_set_recipes = query_set_recipes.filter(steps__contains=food_keyword)

    # Cooktime - время приготовления
    if 'cooktime' in request.GET:
        cooktime = request.GET['cooktime']
        if ['cooktime']:
            query_set_recipes = query_set_recipes.filter(cooktime__iexact=cooktime)

    # Сложность приготовления
    if 'difficulty' in request.GET:
        difficulty = request.GET['difficulty']
        if ['difficulty']:
            query_set_recipes = query_set_recipes.filter(difficulty__iexact=difficulty)

    context = {
        'difficulty_choices': difficulty_choices,
        'cooktime_choices': cooktime_choices,
        'recipes': query_set_recipes,
        'values': request.GET,
    }
    return render(request, 'CookBook/search.html', context)


@login_required()
def profile_liked(request):
    liked_recipes = BookLikedRecipesAndUser.objects.filter(user=request.user.pk)

    list_liked_recipes = []
    for rec in liked_recipes:
        qRec = get_object_or_404(Recipe, id=rec.recipe_id)
        list_liked_recipes.append(qRec)

    numberLiked = len(list_liked_recipes)

    paginator = Paginator(list_liked_recipes, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {
        'list_liked_recipes': page.object_list,
        'numberLiked': numberLiked,
        'page': page
    }
    return render(request, 'CookBook/profile_liked.html', context)


@login_required()
def add_liked_recipe_to_profile(request, pk):
    recipe_chosen = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        #     print("Проверка-----")
        new_liked_recipe = BookLikedRecipesAndUser(
            recipe_id=recipe_chosen.id,
            user_id=request.user.pk
        )
        new_liked_recipe.like = True
        new_liked_recipe.save()
    return redirect('CookBook:profile_liked')


@login_required()
def delete_liked_recipe_from_profile(request, pk):
    recipe_to_delete = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        BookLikedRecipesAndUser.objects.get(recipe_id=recipe_to_delete.id, user_id=request.user.pk).delete()
        return redirect('CookBook:profile_liked')
