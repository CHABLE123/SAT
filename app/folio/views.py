from django.shortcuts import render
from folio.forms import Registro_form2, Registro_form, Solicitud_form, fResetPassword, Creargrupo
from folio.models import solicitud, Usuario
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from utils.folio_generator import GetFolio
from django.contrib.auth import update_session_auth_hash


@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def Cpassword(request):
    if request.method == 'POST':
        fpassword = fResetPassword(request.POST, label_suffix = '')
        if fpassword.is_valid():
            current_pass = fpassword.cleaned_data['current_password']
            if request.user.check_password(current_pass):
                new_pass = fpassword.cleaned_data['new_password']
                request.user.set_password(new_pass)
                request.user.save(update_fields=['password'])
                update_session_auth_hash(request, request.user)
                messages.success(request, 'La contraseña ha sido cambiada exitosamente')
                return redirect('login')
            else:
                messages.warning(request, 'No se guardó ningún cambio. Intente de nuevo')
        else:
            messages.warning(request, 'No se guardó ningún cambio. Intente de nuevo')
    else:
        fpassword = fResetPassword(label_suffix = '')
    context = {'fpassword': fpassword}
    return render(request, 'cambiar_contraseña.html', context)

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def home(request):
    return render(request, 'home.html')

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def reg_folio(request):
    if request.method=='POST':
        form = Solicitud_form(request.POST)
        if form.is_valid():
            folio = GetFolio(solicitud)
            f=form.save(commit=False)
            f.folio = folio.generate()
            f.usuario = request.user
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

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
@permission_required(['folio.create_users'], raise_exception = True)
def reg_usuario(request):
    if request.method=='POST':
        form = Registro_form(request.POST)
        if form.is_valid():
            r=form.save(commit=False)
            r.is_active = True
            r.set_password(form.cleaned_data['password'])
            r.save()
            form.save_m2m()
            print('Registro guardado')
            messages.success(request,'El usuario ha sido registrado')
            return redirect('reg_usuario')
        else:
            print(form.errors)
            print('Registro no guardado')
    else:
        form = Registro_form()
    return render(request, 'solicitud_usuario.html', {
        'form': form
    })

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
@permission_required(['folio.list_users'], raise_exception = True)
def cons_usuario(request):
    data = {
        'usuarios': Usuario.objects.exclude(dni = request.user.dni)
    }
    return render(request, 'consulta_usuario.html', data)

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def cons_folio(request):
    solis = []
    if request.user.has_perm('folio.option'):
        solis = solicitud.objects.all()
    else:
        solis = request.user.solicitudes.all()
    data = {
        'solicitudes': solis
    }
    return render(request, 'consulta_solicitud.html', data)

@login_required(login_url=settings.LOGOUT_REDIRECT_URL) 
def mod_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    data = {
        'form': Registro_form2(instance=usuario)
    }
    if request.method == 'POST':
        form = Registro_form2(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            print('Registro guardado')
            messages.success(request,'El Registro ha sido modificado')
            return redirect('cons_usuario')
        else:
            print(form.errors)
            print('Registro no guardado')
    return render(request, 'modificar_usuario.html', data)

@login_required(login_url=settings.LOGOUT_REDIRECT_URL)
def eli_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request,'Se elimino el registro correctamente')
    return redirect('cons_usuario')

@login_required(login_url=settings.LOGOUT_REDIRECT_URL) 
def mod_folio(request, id):
    solicitudes = get_object_or_404(solicitud, id=id)
    data2 = {
        'form': Solicitud_form(instance=solicitudes)
    }
    if request.method=='POST':
        form = Solicitud_form(request.POST, instance=solicitudes)
        if form.is_valid():
            f=form.save(commit=False)
            f.save()
            print('Registro guardado')
            messages.success(request,'El Registro ha sido modificado')
            return redirect('cons_folio')
        else:
            print('Registro no guardado')
    return render(request, 'modificar_folio.html', data2)

def grupo(request):
    if request.method=='POST':
        form = Creargrupo(request.POST)
        if form.is_valid():
            form.save()
            print('Registro guardado')
            messages.success(request,'El grupo ha sido registrado')
            return redirect('grupo')
        else:
            print(form.errors)
            print('Registro no guardado')
    else:
        form = Creargrupo()
    return render(request, 'grupo.html', {
        'form': form
    })