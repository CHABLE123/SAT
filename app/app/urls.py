"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from folio import views
from django.contrib.auth.views import LogoutView, LoginView
from folio.forms import LoginForm
from utils.reportes import generate_report, generate_report_red

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='login.html', form_class=LoginForm), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.home, name="home"),
    path('registro/solicitud/', views.reg_folio, name="reg_folio"),
    path('registro/usuario/', views.reg_usuario, name="reg_usuario"),
    path('registro/reduccion/', views.reg_reduccion, name="reg_reduccion"),
    path('consulta/usuario/', views.cons_usuario, name="cons_usuario"),
    path('consulta/solicitud', views.Solicitudes.as_view(), name='cons_folio'),
    path('consulta/reduccion/', views.ReduccionesList.as_view(), name="cons_reduccion"),
    path('consulta/indicadores/', views.IndicadoresList.as_view(), name="cons_indicadores"),
    path('registro/indicadores/', views.IndicadorCrear.as_view(), name='reg_indicadores'),
    path('reporte/solicitudes/', generate_report, name='reporte_solicitudes'),
    path('reporte/reducciones/', generate_report_red, name='reporte_red'),
    path('solicitudes/estatus/', views.CambiarEstatus.as_view(), name='cambiar_estatus'),
    path('modificar/usuario/<id>/', views.mod_usuario, name='mod_usuario'),
    path('eliminar/usuario/<id>/', views.eli_usuario, name='eli_usuario'),
    path('modificar/folio/<id>/', views.mod_folio, name='mod_folio'),
    path('modificar/indicador/<id>/', views.mod_indicadores, name='mod_indicadores'),
    path('cambiar/contraseña/', views.Cpassword, name='Cpassword'),
    path('grupo/', views.grupo, name='grupo'),
]
