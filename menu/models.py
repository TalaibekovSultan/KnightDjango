from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField('Название', max_length=40)
    about = models.CharField('О компании', max_length=1000)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    work = models.CharField('Место работы', max_length=200)
    age = models.IntegerField('Возраст', null=True)
    images = models.ImageField('Аватарка', default='null')

    # avatar
    def __str__(self):
        return self.user.username


class Menu(models.Model):
    images = models.ImageField(upload_to='media/', verbose_name='Вид', blank=True, null=True)
    name = models.CharField('Название', max_length=30)
    cotegory = models.CharField('Тип', max_length=30, default='Dish')
    companys = models.ManyToManyField(Company, verbose_name='Изготовитель')
    about = models.TextField('О блюде')
    price = models.PositiveIntegerField(null=True, verbose_name="Цена")

    def get_absolute_url(self):
        return f'/menu/{self.id}'

    def get_companys(self):
        return ', '.join([cat.name for cat in self.companys.all()])

    class Meta:
        verbose_name = 'Еду'
        verbose_name_plural = 'Еда'

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    session_key = models.CharField(max_length=999, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_cost = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        items = CartContent.objects.filter(cart=self.id)
        total = 0
        for item in items:
            total += item.product.price * item.qty
        return total

    @property
    def get_cart_content(self):
        return CartContent.objects.filter(cart=self.id)


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=True)
