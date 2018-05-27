from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

listOfAddresses = ["sd2018-ykeaa4.herokuapp.com", 'sd2018-ykea-a9.herokuapp.com']

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^items/$', views.items, name='items2'),
    url(r'^items/(?P<item_number>.\d+)/$', views.description, name='description'),
    url(r'^items/(?P<category>.*)/$', views.items, name='items'),
    url(r'^shoppingcart/$', views.shoppingcart, name='shoppingcart'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^checkout/error$', views.checkout_error, name='checkout_error'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^process/$', views.process, name='process'),
    url(r'^register/$', views.register, name='register'),
    url(r'^admin_money/$', views.admin_money, name='admin_money'),
    url(r'^modify_money/$', views.modify_money, name='modify_money'),
    url(r'^admin_item/$', views.admin_item, name='admin_item'),
    url(r'^process_item/$', views.process_item, name='process_item'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^comparator$', views.comparator, {'ips': listOfAddresses}),
    url(r'^.*$', RedirectView.as_view(url='</ykea/home>', permanent=False), name='index'),



]
