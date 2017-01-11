
from django import forms

from .models import Company


class CompanyAdminForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyAdminForm, self).__init__(*args, **kwargs)
        # set email to required
        self.fields['email'].required = True
