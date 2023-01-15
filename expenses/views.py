from django.views.generic import ListView, UpdateView
from django.db.models import Sum
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            datefrom = form.cleaned_data.get('date1')
            dateto = form.cleaned_data.get('date2')
            multiplecategories = form.cleaned_data.get('multiplecategories')
            sorting_order = form.cleaned_data.get('sorting_order')
            sorting_by = form.cleaned_data.get('sorting_category')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if datefrom or dateto:
                queryset = queryset.filter(date__range=[datefrom, dateto])
            if multiplecategories:
                queryset = queryset.filter(category__in=multiplecategories)

            if sorting_by == '':
                sorting_by = 'category'

            if sorting_order == 'ascending':
                queryset = queryset.order_by(sorting_by)
            else:
                sorting_by = '-' + sorting_by
                queryset = queryset.order_by(sorting_by)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount=queryset.aggregate(Sum('amount')),
            summary_per_year=queryset.all().values_list('date__year').annotate(Sum('amount')).order_by('date__year'),
            summary_per_month=queryset.all().values_list('date__month').annotate(Sum('amount')).order_by('date__month'),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self):
        expenses_per_category = Expense.objects.values_list('category__name', 'category__id').annotate(Sum('amount'))

        return super().get_context_data(expenses_per_category=expenses_per_category)


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

