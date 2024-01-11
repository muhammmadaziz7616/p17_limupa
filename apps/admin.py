import csv

from django.contrib import admin
from django.forms import forms
from django.http import HttpResponse

from apps.models import Category, Blog, Comment, Tag


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Blog)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class ProductAdmin(admin.ModelAdmin):
    pass
