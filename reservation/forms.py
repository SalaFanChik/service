from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ClientProfile, Service, StaffProfile, Order, Staff

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['phone_number']

class UserWithProfileCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone_number']

    def save(self, commit=True):
        user = super(UserWithProfileCreationForm, self).save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user

    def save_profile(self, user):
        profile = ClientProfile(user=user, phone_number=self.cleaned_data["phone_number"])
        profile.save()


class ChooseService(forms.Form):
    service = forms.ChoiceField(choices=[(x.id, x.name) for x in Service.objects.all()], label="Service")

class ChooseMaster(forms.Form):
    master = forms.ChoiceField(choices=[], label="Master")

    def __init__(self, *args, **kwargs):
        service_id = kwargs.pop('service_id', None)
        super(ChooseMaster, self).__init__(*args, **kwargs)

        if service_id:
            self.fields['master'].choices = [(x.id, x.user.username) for x in StaffProfile.objects.filter(services__id=int(service_id))]

class ChooseDate(forms.Form):
    def __init__(self, *args, **kwargs):
        master_id = kwargs.pop('master_id', None)
        super(ChooseDate, self).__init__(*args, **kwargs)

        if master_id:
            available_dates = StaffProfile.objects.get(id=master_id).holiday
            self.fields['date'].widget.attrs['data-available-dates'] = available_dates


    date= forms.CharField(
        max_length=100,  # Set the maximum length of the text
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'date'}),
        required=False,   # Set to False if the field is optional
    )

class ChooseTime(forms.Form):
    time = forms.ChoiceField(choices=[], label="Time")

    def __init__(self, *args, **kwargs):
        master_id = kwargs.pop('master_id', None)
        date = kwargs.pop('date', None)
        super(ChooseTime, self).__init__(*args, **kwargs)

        if master_id and date:
            working_hours = StaffProfile.objects.get(id=master_id).WorkingHours 
            self.fields['time'].choices = [(x, x) for x in working_hours.all()]