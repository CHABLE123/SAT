import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from folio.forms import Registro_form2, Registro_form, Solicitud_form, fResetPassword, Creargrupo, ReduccionForm, IndicadorForm
from folio.models import solicitud, Usuario, Indicadores, Reducciones
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from utils.folio_generator import GetFolio
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, RedirectView
from django.db.models import Q
from django.utils.timezone import make_aware


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
            folio = GetFolio(solicitud.objects.all())
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
def reg_reduccion(request):
    if request.method=='POST':
        form = ReduccionForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            if f.tipo == 't1':
                folio = GetFolio(Reducciones.objects.filter(tipo='t1'))
                folio = folio.generate()
                f.folio = 'RED74{}/{}'.format(folio, datetime.date.today().year)
            else:
                folio = GetFolio(Reducciones.objects.filter(tipo='t2'))
                folio = folio.generate()
                f.folio = 'RED/VA/ART41Y74/{}/{}'.format(folio, datetime.date.today().strftime('%y'))
            f.ejecutivo = request.user
            f.save()
            messages.success(request,'Tu numero de folio es '+f.folio)
            return redirect('reg_reduccion')
        else:
            pass
    else:
        form = ReduccionForm()
    return render(request, 'solicitud_red.html', {
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

class ReduccionesList(LoginRequiredMixin, ListView):
    model = Reducciones
    paginate_by = 50
    template_name = 'consulta_red.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        d = self.request.GET.get('d', '')
        type_ = self.request.GET.get('t', '')
        lookup = (Q(folio__icontains = q))
        if self.request.user.has_perm('folio.option_red'):
            solicitudes = self.model._default_manager.filter(lookup)
        else:
            solicitudes = self.request.user.reducciones.filter(lookup)

        solicitudes = self.model._default_manager.filter(lookup)
        if type_ in ['t1', 't2']:
            solicitudes = solicitudes.filter(tipo=type_)
        try:
            d = make_aware(datetime.datetime.fromisoformat(d)).date()
            solicitudes = solicitudes.filter(fecha_reg__date=d)
        except:
            pass
        self.queryset = solicitudes
        return solicitudes
    
    def get_context_data(self):
        context = {'q': self.request.GET.get('q', ''), 'd': self.request.GET.get('d', ''), 't': self.request.GET.get('t', 'todos'), 'total': self.queryset.count()}
        return super().get_context_data(**context)

class Solicitudes(LoginRequiredMixin, ListView):
    model = solicitud
    paginate_by = 50
    template_name = 'consulta_solicitud.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        d = self.request.GET.get('d', '')
        type_ = self.request.GET.get('t', '')
        lookup = (Q(folio__icontains = q))
        if self.request.user.has_perm('folio.option'):
            solicitudes = self.model._default_manager.filter(lookup)
        else:
            solicitudes = self.request.user.solicitudes.filter(lookup)
        if type_ in ['pendiente', 'despachado', 'cancelado']:
            solicitudes = solicitudes.filter(estatus=type_)
        try:
            d = make_aware(datetime.datetime.fromisoformat(d)).date()
            solicitudes = solicitudes.filter(fecha_reg__date=d)
        except:
            pass
        self.queryset = solicitudes
        return solicitudes
    
    def get_context_data(self):
        context = {'q': self.request.GET.get('q', ''), 'd': self.request.GET.get('d', ''), 't': self.request.GET.get('t', 'todos'), 'total': self.queryset.count()}
        return super().get_context_data(**context)

class CambiarEstatus(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    url = reverse_lazy('cons_folio')

    def post(self, request, *args, **kwargs):
        folios = request.POST.getlist('folio', [])
        estatus = 'pendiente'
        if request.POST.get('done', None) is not None:
            estatus = 'despachado'
        if request.POST.get('cancel', None) is not None:
            estatus = 'cancelado'
        counter = 0
        for f in folios:
            try:
                folio = solicitud.objects.get(folio=f)
                folio.estatus = estatus
                folio.save()
                counter = counter+1 
            except solicitud.DoesNotExist:
                pass
        messages.success(request, '{} solicitud(es) modificada(s)'.format(counter))
        return self.get(request, *args, **kwargs)

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

class IndicadoresList(LoginRequiredMixin, ListView):
    model = Indicadores
    paginate_by = 50
    template_name = 'consulta_indicadores.html'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        mes = self.request.GET.get('mes', datetime.datetime.now().month)
        anio = self.request.GET.get('anio', datetime.datetime.now().year)
        lookup = (Q(nombre__icontains = q) & (Q(mes__exact = mes) & Q(anio__exact = anio)))
        solicitudes = self.model._default_manager.filter(lookup)
        self.queryset = solicitudes
        return solicitudes
    
    def get_context_data(self):
        mes = self.request.GET.get('mes', datetime.datetime.now().month)
        anio = self.request.GET.get('anio', datetime.datetime.now().year)
        context = {
            'q': self.request.GET.get('q', ''),
            'total': self.queryset.count(),
            'form': IndicadorForm(label_suffix='', initial={'mes': datetime.datetime.now().month, 'anio': datetime.datetime.now().year}),
            'form2': IndicadorForm(label_suffix='', initial={'mes': mes, 'anio': anio})
        }
        return super().get_context_data(**context)

class IndicadorCrear(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    url = reverse_lazy('cons_indicadores')

    def post(self, request, *args, **kwargs):
        form = IndicadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se agregó un indicador exitosamente')
        else:
            messages.error(request, 'Error al guardar')
        return self.get(request, *args, **kwargs)


@login_required(login_url=settings.LOGOUT_REDIRECT_URL) 
def mod_indicadores(request, id):
    solicitudes = get_object_or_404(Indicadores, id=id)
    data2 = {
        'form': IndicadorForm (instance=solicitudes)
    }
    if request.method=='POST':
        form = IndicadorForm(request.POST, instance=solicitudes)
        if form.is_valid():
            f=form.save(commit=False)
            if 'cantidad' in form.changed_data:
                f.porcentaje = None
            elif 'porcentaje' in form.changed_data:
                f.cantidad = None
            f.save()
            print(f.porcentaje, f.cantidad)
            print('Registro guardado')
            messages.success(request,'El Registro ha sido modificado')
            return redirect('cons_indicadores')
        else:
            print(form.errors)
            print('Registro no guardado')
    return render(request, 'modificar_indicador.html', data2)
