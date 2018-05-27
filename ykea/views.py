from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Item
from .models import Shoppingcart, Quantity, ShoppingCounter, Wallet, Bill, ItemBill
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from .serializers import ItemSerializer

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from .serializers import UserSerializer

from ykea.permissions import IsCommercial


# Create your views here.
def index(request):
    #Quantity.objects.all().delete()
    return HttpResponse("Hello, world. You're at the YKEA home page.")

def queryMoney(request):
    if(request.user.is_authenticated() and Wallet.objects.filter(user = request.user).exists()):
        money = request.user.wallet.money
    else:
        money = 0
    return money
def home(request):
    categories = Item.CATEGORIES
    context = {
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }
    return render(request, 'ykea/home.html', context)



def items(request,category=""):
    items_by_category = Item.objects.filter(category=category)
    categories = Item.CATEGORIES
    context = {
        'items': items_by_category,
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'category': category,
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }
    return render(request, 'ykea/items.html', context)

def description(request,category="",item_number=""):
    item = Item.objects.filter(item_number=item_number)
    categories = Item.CATEGORIES
    context = {
        'item': item,
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }
    return render(request, 'ykea/description.html', context)


#def shoppingcart(request):
#    if "selectedItem" in request.session:
#    	  selectedItems = request.session["selectedItem"]
#    else:
#        selectedItems = []
#    for key in request.POST:
#        if key.startswith("checkbox"):
#            selectedItems.append(request.POST[key])
#
#    request.session["selectedItem"] = selectedItems
#    return HttpResponseRedirect(reverse('buy'))

@login_required
def shoppingcart(request):
    try:
        if "cart" in request.session:
            cart = Shoppingcart.objects.get(id_cart = request.session["cart"])

        else:
            #cart, created = Shoppingcart.objects.get_or_create(id_cart = ShoppingCounter.counter)
            cart = Shoppingcart.objects.create()
            #ShoppingCounter.counter+=1;
            cart.save()
            request.session["cart"] = cart.id_cart
    except:
        #cart, created = Shoppingcart.objects.get_or_create(id_cart = ShoppingCounter.counter)
        cart = Shoppingcart.objects.create()
        #ShoppingCounter.counter+=1;
        cart.save()
        request.session["cart"] = cart.id_cart
    #Quantity.objects.all().delete()
    for key in request.POST:
        if key.startswith("checkbox"):
            #selectedItems.append(request.POST[key])
            #cart.item_list.add(Quantity.objects.get(item=Item.objects.get(item_number = request.POST[key])))
            if Quantity.objects.filter(shopping_cart = cart, item = Item.objects.get(item_number = request.POST[key])).exists():
                quantitat = int(Quantity.objects.get(shopping_cart = cart, item = Item.objects.get(item_number = request.POST[key])).quantitat) + 1
                Quantity.objects.filter(item = Item.objects.get(item_number = request.POST[key])).update(quantitat = quantitat)
                #quant.quantitat = quant.quantitat + 1
            else:
                Quantity.objects.create(shopping_cart = cart, item=Item.objects.get(item_number = request.POST[key]), quantitat=1)
            cart.save()


    #request.session["selectedItem"] = selectedItems


    return HttpResponseRedirect(reverse('buy'))

def buy(request):
    #userItem = request.session["selectedItem"]
    cart = request.session["cart"]
    quant = Shoppingcart.objects.get(id_cart = cart).item_list.all()
    items = []
    preuTotal = 0
    for i in quant:
        quantitat = Quantity.objects.get(item = i).quantitat
        totalItem = float(quantitat) * float(i.price)
        preuTotal += totalItem
        items.append([i, quantitat, totalItem])
    categories = Item.CATEGORIES
    context = {
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'cart' : cart,
        'items' : items,
        'total' : preuTotal,
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }
    return render(request, 'ykea/shoppingcart.html', context)

def delete(request):
    for id in request.session["delete"]:
            Quantity.objects.get(item=Item.objects.get(item_number = id)).delete()
    return HttpResponseRedirect(reverse('buy'))

def checkout(request):
    cart = request.session["cart"]
    quant = Shoppingcart.objects.get(id_cart = cart).item_list.all()
    items = []
    bill = Bill.objects.create(user = Wallet.objects.get(user = request.user), total = 0)

    for item_id in request.session["sum"]:
        Quantity.objects.filter(item = Item.objects.get(item_number = item_id[0][6:])).update(quantitat = item_id[1])

    preuTotal = 0
    for i in quant:
        quantitat = Quantity.objects.get(item = i).quantitat
        totalItem = float(quantitat) * float(i.price)
        preuTotal += totalItem
        items.append([i, quantitat, totalItem])
        ItemBill.objects.create(bill = bill, item = i, quantitat = quantitat, subtotal = totalItem)
    Bill.objects.filter(id_bill = bill.id_bill).update(total = totalItem)

    categories = Item.CATEGORIES
    context = {
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'cart' : cart,
        'items' : items,
        'total' : preuTotal,
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }

    if(request.user.wallet.money - preuTotal < 0.00):
        return render(request, 'ykea/checkout_error.html', context)
    else:
        Wallet.objects.filter(user = request.user).update(money = request.user.wallet.money - preuTotal)
        request.user.wallet.money -= preuTotal
        context['money'] = request.user.wallet.money

    Quantity.objects.all().delete()
    Shoppingcart.objects.get(id_cart = cart).delete()
    request.session["cart"]=[]
    return render(request, 'ykea/checkout.html', context)

def process(request):
    request.session["delete"] = []
    request.session["sum"] = []
    for key in request.POST:
        if key.startswith("C"):
            for num in request.POST:
                if num.startswith("number"):
                    request.session["sum"].append((num,request.POST[num]))
            return HttpResponseRedirect(reverse('checkout'))
        if key.startswith("D"):
            for deleted in request.POST:
                if deleted.startswith("checkbox"):
                    request.session["delete"].append(request.POST[deleted])
            return HttpResponseRedirect(reverse('delete'))

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            wallet, created = Wallet.objects.get_or_create(user = new_user, money = 1000)
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    })

def checkout_error(request):
    context = {
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }
    return render(request, 'ykea/checkout_error.html', context)

def isAdmin(user):
    return user.is_authenticated() and user.is_superuser
@user_passes_test(isAdmin, login_url="/ykea/accounts/login/")
def admin_money(request):
    usernames = User.objects.all()
    users=[]
    for user in usernames:
        users.append([user ,user.wallet.money])
    categories = Item.CATEGORIES
    context = {
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
        'users' : users,
    }
    return render(request, 'ykea/admin_money.html', context)

def modify_money(request):
    for key in request.POST:
        if key.startswith("S"):
            for money in request.POST:
                if money.startswith("money"):
                    user = User.objects.get(username = money[5:])
                    Wallet.objects.filter(user = user).update(money = request.POST[money])
    return HttpResponseRedirect(reverse('home'))

@user_passes_test(isAdmin, login_url="/ykea/accounts/login/")
def admin_item(request):
    categories = Item.CATEGORIES

    context = {
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
    }
    return render(request, 'ykea/admin_item.html',context)


def process_item(request):
    for key in request.POST:
        if key.startswith("G"):
            item_number = None
            name = None
            description = None
            price = None
            is_new = None
            size = None
            categories = None

            for informacio in request.POST:
                if informacio == "item_number":
                    item_number = float(request.POST[informacio])
                elif informacio == "name":
                    name = request.POST[informacio]
                elif informacio == "description":
                    description = request.POST[informacio]
                elif informacio == "price":
                    price = float(request.POST[informacio])
                #elif informacio == "true":
                #    is_new = request.POST[informacio]
                #elif informacio == "false":
                #    is_new = request.POST[informacio]
                elif informacio == "size":
                    size = request.POST[informacio]
                elif informacio == "categories":
                    categories = request.POST[informacio]

            Item.objects.create(item_number = item_number, name = name, description = description, price = price,
            is_new = True, size = size, category = categories)
            categories = Item.CATEGORIES
            context = {
                'category': zip([i[0] for i in categories],[i[1] for i in categories]),
                'auth' : request.user.is_authenticated(),
                'user' : request.user.username,
                'money' : queryMoney(request),
            }

            return render(request, 'ykea/admin_item.html',context)


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Items to be viewed or edited.
    """
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Item.objects.all().order_by('item_number')
        category = self.request.query_params.get('category', None)
        price = self.request.query_params.get('price', None)
        new = self.request.query_params.get('new', None)

        if category is not None:
            queryset = queryset.filter(category=category)
        if price is not None:
            queryset = queryset.filter(price__lte=price)
        if new is not None:
            if(new.lower() == "yes"):
                queryset = queryset.filter(is_new='true')
            elif(new.lower() =="no"):
                queryset = queryset.filter(is_new='false')


        return queryset

    queryset = Item.objects.all().order_by('item_number')
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommercial)



def save(self, *args, **kwargs):
    """
    Use the `pygments` library to create a highlighted HTML
    representation of the code snippet.
    """
    lexer = get_lexer_by_name(self.language)
    linenos = 'table' if self.linenos else False
    options = {'title': self.title} if self.title else {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super(Snippet, self).save(*args, **kwargs)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommercial,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommercial,)

def comparator(request,ips):
    categories = Item.CATEGORIES
    context = {
        'categories': zip([i[0] for i in categories],[i[1] for i in categories]),
        'categories2' : zip([i[0] for i in categories],[i[1] for i in categories]),
        'auth' : request.user.is_authenticated(),
        'user' : request.user.username,
        'money' : queryMoney(request),
        'ips' : ips,
    }

    return render(request, 'ykea/comparator.html',context)
