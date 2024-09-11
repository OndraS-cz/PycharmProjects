from datetime import date

from django.core.exceptions import ValidationError
from django.db.models.expressions import result
from django.forms import Form, CharField, DateField, ModelChoiceField, Textarea, ModelForm, NumberInput

from viewer.models import Country, Creator


class CreatorForm(Form):
    name = CharField(max_length=32, required=False)
    surname = CharField(max_length=32, required=False)
    date_of_birth = DateField(required=False)
    date_of_death = DateField(required=False)
    country_of_birth = ModelChoiceField(queryset=Country.objects, required=False)
    country_of_death = ModelChoiceField(queryset=Country.objects, required=False)
    biography = CharField(widget=Textarea, required=False)


    def clean_name(self):
        initial = self.cleaned_data['name']
        print(f"initial name: '{initial}'")
        result = initial.strip()
        print(f"result: '{result}'")
        if len(result):
            result = result.capitalize()
        print(f"result: '{result}'")
        return result


    def clean_date_of_birth(self, value):
        super().clean()
        if value and value >= date.today():
            raise ValidationError('Datum narození musí být v minulosti!')


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        surname = cleaned_data['surname']
        if len(name.strip()) == 0 and len(surname.strip()) == 0:
            raise ValidationError('Je nutno zadat jméno nebo příjmení!')

class CreatorModelForm(ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'  # případně můžeme definovat, které položky se mají zobrazit; např. ['name', 'surname']
        # exclude = ['date_of_death'] - vyjmutí některého pole

    date_of_birth = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}))
    date_of_death = DateField(required=False, widget=NumberInput(attrs={'type': 'date'}))

    def clean_name(self):
        initial = self.cleaned_data['name']
        print(f"initial name: '{initial}'")
        result = initial.strip()
        print(f"result: '{result}'")
        if len(result):
            result = result.capitalize()
        print(f"result: '{result}'")
        return result


    def clean_date_of_birth(self, value):
        super().clean()
        if value and value >= date.today():
            raise ValidationError('Datum narození musí být v minulosti!')


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        surname = cleaned_data['surname']
        if len(name.strip()) == 0 and len(surname.strip()) == 0:
            raise ValidationError('Je nutno zadat jméno nebo příjmení!')
