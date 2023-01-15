from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    datefrom = forms.DateTimeField(required=False, label="Date from")
    dateto = forms.DateTimeField(required=False, label="Date to")
    multiplecategories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                        label="Category", widget=forms.CheckboxSelectMultiple,
                                                        required=False)
    SORTING = [('ascending', 'Ascending'), ('descending', 'Descending')]
    sorting_order = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=SORTING)
    SORTING_BY = [('category', 'Category'), ('date', 'Date')]
    sorting_category = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=SORTING_BY)

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

