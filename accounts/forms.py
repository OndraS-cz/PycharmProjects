from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import NumberInput, DateField, CharField, Textarea

from accounts.models import Profile

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password1']

    date_of_birth = DateField(widget=NumberInput(attrs={'type': 'date'}), label='Datum narození')
    biography = CharField(widget=Textarea, label='Něco o mě..', required=False)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)  # Vytváříme uživatele (v databázi - auth_user)
        date_of_birth = self.cleaned_data['date_of_birth']
        biography = self.cleaned_data['biography']
        profile = Profile(user=user, date_of_birth=date_of_birth, biography=biography)
        if commit:
            profile.save()  # Vytváříme profil uživatele (v databázi - accounts_profile)
        return user
