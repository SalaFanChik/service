from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from .forms import UserWithProfileCreationForm, ChooseDate, ChooseTime, ChooseService, ChooseMaster
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from .models import User, ClientProfile, StaffProfile, Order, Service, WorkingHours
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Это нужно, если вы планируете принимать запросы извне без CSRF-токена
def handle_post_request(request):
    if request.method == 'POST':
        received_data = request.POST
        print(received_data)
        return JsonResponse({'received_data': received_data})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)

def index(request):
    print(request.user.username)
    return render(request, 'reservation/index.html')



def pay(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name, email, message)
        return HttpResponse('Form submitted successfully!')
    
    return render(request, 'reservation/payment.html')
    

class UserWithProfileCreationView(View):
    template_name = 'reservation/signup.html'
    form_class = UserWithProfileCreationForm

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index')) 
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index')) 
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            form.save_profile(user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})
    


class CustomLoginView(LoginView):
    template_name = 'reservation/login.html'
    success_url = reverse_lazy('/')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().form_valid(form)
    

FORMS = [
    ("service", ChooseService),
    ("master", ChooseMaster), 
    ("date", ChooseDate),
    ("message", ChooseTime),
]



TEMPLATES = {
    "service": "reservation/choose_service.html",
    "master": "reservation/choose_master.html",
    "date": "reservation/choose_date.html",
    "message": "reservation/message.html",
    }


class ContactWizard(SessionWizardView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactWizard, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['extra_data'] = {'key': 'value'}
        return context

    def get_form_kwargs(self, step):
        kwargs = super().get_form_kwargs(step)
        if step == 'master':
            service_data = self.get_cleaned_data_for_step('service') or {}
            service_id = service_data.get('service')
            kwargs['service_id'] = service_id
        if step == 'date':
            service_data = self.get_cleaned_data_for_step('service') or {}
            service_id = service_data.get('service')
            master_data = self.get_cleaned_data_for_step('master') or {}
            master_id = master_data.get('master')
            kwargs['master_id'] = master_id
        if step == 'message':
            master_data = self.get_cleaned_data_for_step('master') or {}
            master_id = master_data.get('master')
            date_data = self.get_cleaned_data_for_step('date') or {}
            date = date_data.get('date')
            kwargs['master_id'] = master_id
            kwargs['date'] = date
        return kwargs

    def done(self, form_list, **kwargs):
        print([form.cleaned_data for form in form_list])
        return render(self.request, 'reservation/order.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
    
    