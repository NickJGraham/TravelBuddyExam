from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('registration/processing', views.register_User),
    path('home', views.Home),
    path('logout', views.logout),
    path('login/processing', views.login),
    path('addTrip', views.addTrip),
    path('trip/processing', views.processTrip),
    path('destination/<int:destinationId>', views.showDestination),
    path('join/<int:destinationId>', views.joinTrip),
]