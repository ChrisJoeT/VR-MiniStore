from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('h/',views.index),
    path('ur/', views.registeration),
    path('pr/', views.addproduct),

    path('sap/', views.showadminpage),
    path('adp/', views.addproduct),
    path('ap/', views.listproduct),
    path('del/<int:id>/', views.delprogram),
    path('ed/<int:id>/', views.editproduct),

    path('bb/', views.login),
    path('sup/', views.showuserpage),
    path('atoc/<int:id>/', views.order),
    path('vc/', views.viewcart),
    path('delp/<int:id>/', views.removeitem),
    path('pay/', views.payment),
    path('upay/', views.userpayment),

    path('passs/', views.changepassword),
    path('myp/', views.viewsales),
    path('ms/<int:salesno>/', views.viewsalessub),
    path('nfeed/', views.addfeedback),
    path('vfd/', views.viewfeedback),

    path('inv/', views.adminviewsales),
    path('ams/<int:salesno>/', views.adminviewsalessub),
    path('ams1/<int:salesno>/', views.invoice),

    path('adms/', views.adminsaleshistory),

]