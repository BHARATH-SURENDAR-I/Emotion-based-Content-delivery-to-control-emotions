from django.urls import path
from . import views 
urlpatterns = [

    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('base/',views.base,name='base'),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('common/',views.common,name='common'),
    path('takeimg/',views.takeimg,name='takeimg'),
    path('index1/',views.index1,name='index1'),
    path('error/',views.index1,name='error'),
    path('manageemotions/',views.manageemotions,name='manageemotions'),
    #path('monitoremotions/',views.monitoremotions,name='montioremotions'),
    path('drugscheck/',views.drugscheck,name='drugscheck'),

]



