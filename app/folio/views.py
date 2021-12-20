from django.shortcuts import render
from folio.forms import Registro_form
from folio.models import solicitud
from folio.models import Usuario
from folio.forms import Solicitud_form
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def home(request):
    return render(request, 'home.html')

def reg_folio(request):
    if request.method=='POST':
        form = Solicitud_form(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.folio=str(solicitud.objects.all().count()+1)
            f.save()
            print('Registro guardado')
            messages.success(request,'Tu numero de folio es '+f.folio)
            return redirect('reg_folio')
        else:
            print('Registro no guardado')
    else:
        form = Solicitud_form()
    return render(request, 'solicitud_folio.html', {
        'form': form  
    })

def reg_usuario(request):
    if request.method=='POST':
        form = Registro_form(request.POST)
        if form.is_valid():
            r=form.save(commit=False)
            r.is_active = True
            r.set_password(form.cleaned_data['password'])
            r.save()
            print('Registro guardado')
            messages.success(request,'Registro guardado')
            return redirect('reg_usuario')
        else:
            print(form.errors)
            print('Registro no guardado')
    else:
        form = Registro_form()
    return render(request, 'solicitud_usuario.html', {
        'form': form
    })

def cons_usuario(request):
    data = {
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'consulta_usuario.html', data)

def cons_folio(request):
    data = {
        'solicitudes': solicitud.objects.all()
    }
    return render(request, 'consulta_solicitud.html', data)
 
def mod_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    data = {
        'form': Registro_form(instance=usuario)
    }
    if request.method == 'POST':
        form = Registro_form(request.POST, instance=usuario)
        if form.is_valid():
            r=form.save(commit=False)
            r.save()
            print('Registro guardado')
            messages.success(request,'El Registro ha sido modificado')
            return redirect('cons_usuario')
        else:
            print(form.errors)
            print('Registro no guardado')
    return render(request, 'modificar_usuario.html', data)

def eli_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('cons_usuario')