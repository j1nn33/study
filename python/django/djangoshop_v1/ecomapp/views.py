from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from ecomapp.models import Category, Product, CartItem, Cart, Order
from decimal import Decimal
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User



def base_view(request):
    try:
        cart_id = request.session['cart_id']  # присваеиваем значение которое есть в сессиях по ключу  cart_id т.е когда корзина уже создана
        cart = Cart.objects.get(id=cart_id)   # для бейджика на меню корзины  (берем корзину которая существует по этому cart_id)
        request.session['total'] = cart.items.count() # в сессии создаем значение соответсвующее количеству товаров 
    except:                 
        cart = Cart()                         # создание новой корзины
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id  # записываем в сессию cart_id нашей вновь созданой корзины
        cart = Cart.objects.get(id=cart_id)   # для бейджика на меню корзины  (берем корзину которая существует по этому cart_id)
    
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'cart' : cart,
        'categories': categories,
        'products': products,
    }
    return render(request, 'base.html',context)

def product_view(request, product_slug):
    """ для работы ссылок на каждый  продукт """
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)   # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)    # для бейджика на меню корзины
    
    categories = Category.objects.all()    # для отображения в меню dropdowm base.html
    product = Product.objects.get(slug=product_slug)
    context = {
        'cart' : cart,
        'product': product,
        'categories': categories,
    }
    return render(request, 'product.html', context)

def category_view(request, category_slug):
    """ для работы ссылок на категрии """
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)    # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)    # для бейджика на меню корзины

    categories = Category.objects.all()    # для отображения в меню dropdowm base.html
    category = Category.objects.get(slug=category_slug)
    # так как мы переопределили в models.py class ProductManager(models.Manager): 
    # то по выражению внизу выводятся все товары, а не только те которые принадлежат категории 
    # product_of_category = category.product_set.all()
    # для этого надо написать строку
    product_of_category = Product.objects.filter(category=category)
    context = {
        'cart' : cart,
        'category': category,
        'product_of_category': product_of_category,
        'categories': categories,
    }
    return render(request, 'category.html', context)

def cart_view(request):

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)    # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)     # для бейджика на меню корзины
    
    categories = Category.objects.all()
    context = {
        'cart' : cart,
        'categories': categories,
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request):
    """ добавление товара в корзину """
    
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины

    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)               # вызов функции которую добавили в класс
    new_cart_total = 0.00
    for item in cart.items.all():
	    new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # все это перенесено в класс корзины models.py
    #product_slug = request.GET.get('product_slug')
    #product = Product.objects.get(slug=product_slug)
    #new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    # new_item, _ так как метод отдает кортеж типа двойное присваивание
    #if new_item not in cart.items.all():
    #    cart.items.add(new_item)
    #    cart.save()
    #    return JsonResponse({'cart_total': cart.items.count()})
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  
def remove_from_cart_view(request):
    """ удаление товара в корзину """
    
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины

    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)          # вызов функции которую добавили в класс
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(), 'cart_total_price': cart.cart_total})
    
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # все это перенесено в класс корзины models.py
    # логика: проверяем наличие продукта в козине и если он есть то удаляем его
    #for cart_item in cart.items.all():
    #    if cart_item.product == product:
    #        cart.items.remove(cart_item)
    #        cart.save()
    #        return JsonResponse({'cart_total': cart.items.count()})
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
    
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    # print(qty, item_id)
    cart.change_qty(qty, item_id)               # вызов функции которую добавили в класс
    cart_item = CartItem.objects.get(id=int(item_id))
  
	    
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # все это перенесено в класс корзины models.py
    #cart_item.qty = int(qty)
    #cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    #cart_item.save()
    # расчет общей стоимости заказа
    #new_cart_total = 0.00
    #for item in cart.items.all():
    #    new_cart_total += Decimal(item.item_total)
    #cart.cart_total = new_cart_total
    #cart.save()
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    return JsonResponse(
        {'cart_total': cart.items.count(),
         'item_total': cart_item.item_total,
         'cart_total_price': cart.cart_total, 
         })


def checkout_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
    
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'checkout.html', context)
  


def order_create_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
    
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()  
    context = {             # для передачи информации в html ( кол-во товаров в заказе - цифра у корзины и т.д. )
        'form': form,
        'cart': cart,
        'categories': categories,
    }
    return render(request, 'order.html', context)

def make_order_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id=cart.id 
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)      # для бейджика на меню корзины
    
    form = OrderForm(request.POST or None)
    categories = Category.objects.all()

    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        # поля беруться из models.py
        new_order = Order.objects.create(
            user=request.user,
            items=cart,
            total=cart.cart_total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            comments=comments
            )
        
        del request.session['cart_id']
        del request.session['total']

        print ('ФОРМА ВАЛИДНА')

        return HttpResponseRedirect(reverse('thank_you'))
        #return HttpResponseRedirect(reverse('make_order_view'))
    return render(request, 'order.html', {'categories': categories})
   

def account_view(request):
    # берутьс все заказы данного пользователя filter(user=request.user)  отбражение в обратном порядке - order_by('-id')
    order = Order.objects.filter(user=request.user).order_by('-id')
    categories = Category.objects.all()
   
    for item in order:
        for new_item in item.items.items.all():
            #print(new_item.item_total)
            pass
    

    context = {
        'order': order,
        'categories': categories
    }
    return render(request, 'account.html', context)

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
	# проверка формы на валидность 
    if form.is_valid():
        new_user = form.save(commit=False)        # эта строчка необходима когда форма создается на основе модели
        # все что внутри до new_user.save()    Относится к данным из формы
        
        # получение данных из формы
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        # создание пользователя на основе полученных данных
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()                           # эта строчка необходима когда форма создается на основе модели
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form,
        'categories': categories
        }
    return render(request, 'registration.html', context)

def login_view(request):
    form = LoginForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('base'))
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'login.html', context)

def thank_you_view(request):
    pass
