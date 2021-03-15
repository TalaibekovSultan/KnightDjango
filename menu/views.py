from .models import Menu, CartContent, Cart
from .forms import MenuForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, RegisterForm, MenuForm, SearchForm
from django.views.generic import DetailView, UpdateView
from django.contrib.postgres.search import SearchVector
from django.views import View
from django.core.exceptions import ObjectDoesNotExist


class MasterView(View):

    def get_cart_records(self, cart=None, response=None):
        cart = self.get_cart() if cart is None else cart
        if cart is not None:
            cart_records = CartContent.objects.filter(cart_id=cart.id)
        else:
            cart_records = []

        if response:
            response.set_cookie('cart_count', len(cart_records))
            return response

        return cart_records

    def get_cart(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
            except ObjectDoesNotExist:
                cart = Cart(user_id=user_id,
                            total_cost=0)
                cart.save()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            try:
                cart = Cart.objects.get(session_key=session_key)
            except ObjectDoesNotExist:
                cart = Cart(session_key=session_key,
                            total_cost=0)
                cart.save()

        return cart



class NewDeteilView(DetailView):
    model = Menu
    template_name = 'menu/details_view.html'
    context_object_name = "article"


class NewUpdateView(UpdateView):
    model = Menu
    template_name = 'menu/adda.html'

    form_class = MenuForm


def menu(request):
    menu = Menu.objects.all()

    # all_dishes = ''


    if request.method == 'POST':
        form = SearchForm(request.POST)
        search = request.POST.get('search')

        if form.is_valid() and search:
            search_vector = SearchVector('name',
                                         'about',
                                         'price',
                                         'companys__name',)
            menu = Menu.objects.annotate(search=search_vector).filter(search=search)
    else:
        form = SearchForm

    return render(request, 'menu/menu_home.html', {'menu': menu, 'name': menu, 'form': form, 'user': request.user})





def adda(request):
    error = ''
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            error = 'Форма неверна'

    form = MenuForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'menu/adda.html', data)


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # if request.GET and 'next' in request.GET:
                #     return redirect(request.GET['next'])
                return redirect('/')
            else:
                form.add_error('login', 'Bad login or password')
                form.add_error('password', 'Bad login or password')
    else:
        form = LoginForm()

    return render(request, 'menu/user.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'menu/user.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('/')


def aboutuser(request):
    return render(request, 'menu/aboutuser.html')


class CartView(MasterView):
    def get(self, request):
        cart = self.get_cart()
        cart_records = self.get_cart_records(cart)
        cart_total = cart.get_total() if cart else 0

        context = {
            'cart_records': cart_records,
            'cart_total': cart_total,
        }
        return render(request, 'menu/cart.html', context)

    def post(self, request):
        dish = Menu.objects.get(id=request.POST.get('dish_id'))
        cart = self.get_cart()
        quantity = request.POST.get('qty')
        # get_or_create - найдет обьект, если его нет в базе, то создаст
        # первый параметр - обьект, второй - булевое значение которое сообщает создан ли обьект
        # если обьект создан, то True, если он уже имеется в базе, то False
        cart_content, _ = CartContent.objects.get_or_create(cart=cart, product=dish)
        cart_content.qty = quantity
        if cart != 0:
            cart_content.save()
        response = self.get_cart_records(cart, redirect('/menu/#dish-{}'.format(dish.id)))
        return response
        # перенаправляем на главную страницу, с учетом якоря

