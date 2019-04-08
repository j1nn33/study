from django.urls import include, path
from . import views

"""
STUCTURE OF SITE

'object' - index.html # home.page + login.page 
'object/list/'        # список объектов всех (в зависимости от того кто вошел)
'object/create/'      # созадть новый объект
'object/izdelye/<id>' # детальная информация по изделию
'object/edit/<id>'    # отредактировать информацию по изделию
'object/contact'      # информация по контактам
'object/report'       # отчеты технический
'object/logout'       # отчеты (в зависимости от того кто вошел)
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('contact/', views.contact, name='contact'),
    path('report/', views.report, name='report'),
    path('create/', views.create, name='create'),


]


urlpatterns += [
    path('izdelye/<int:pk>/', views.izdelye, name='izdelye'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    #path('izdelye/<int:pk>/', views.create, name='izdelye')
    #path('izdelye/<int:pk>/edit/', views.IzdelyeDetailView.as_view(), name='izdelye'),
]

# path('list/', views.ObjectListView.as_view(), name='list'),
#path('izdelye/<int:pk>', views.IzdelyeDetailView.as_view(), name='izdelye'),
