
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Brand, ATM , DownReason,ATMContact
from django import forms
import csv
import io

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DownReason)
class DownReasonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class ATMAdmin(admin.ModelAdmin):
    list_display = ('terminal_code', 'terminal_branch', 'atm_brand', 'atm_ip', 'atm_acc_no', 'branch_code', 'atm_user', 'atm_password', 'atm_ram', 'atm_storage', 'atm_os', 'atm_bit')
    change_list_template = "admin/contact_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.admin_site.admin_view(self.upload_csv), name='upload_csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        
        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)  # Skip the header row
                for row in csv.reader(io_string, delimiter=',', quotechar='"'):
                    try:
                        brand = Brand.objects.get(name=row[3])
                    except Brand.DoesNotExist:
                        brand = Brand.objects.create(name=row[3])
                    ATM.objects.update_or_create(
                        terminal_code=row[0],
                        defaults={
                            'terminal_branch': row[1],
                            'atm_ip': row[2],
                            'atm_brand': brand,
                            'atm_acc_no': row[4],
                            'branch_code': row[5],
                            'atm_user': row[6],
                            'atm_password': row[7],
                            'atm_ram': row[8],
                            'atm_storage': row[9],
                            'atm_os': row[10],
                            'atm_bit': row[11],
                        }
                    )
                self.message_user(request, "CSV file has been uploaded successfully.")
                return HttpResponseRedirect("../")

        form = CSVUploadForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['upload_form'] = CSVUploadForm()
        return super(ATMAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(ATM, ATMAdmin)
@admin.register(ATMContact)
class ATMContactAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Customize the label for the atm_branch dropdown
        form.base_fields['atm_branch'].label_from_instance = lambda obj: obj.terminal_branch
        return form
