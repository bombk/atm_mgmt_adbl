from django.contrib import admin
from .models import Brand, ATM , DownReason


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ATM)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('terminal_code', 'terminal_branch', 'atm_brand', 'atm_ip', 'atm_acc_no', 'branch_code', 'atm_user', 'atm_password', 'atm_ram', 'atm_storage', 'atm_os', 'atm_bit', 'atm_p')
    search_fields = ('terminal_code', 'atm_acc_no', 'atm_ip', 'atm_brand','atm_ip','atm_acc_no','branch_code')
    list_filter = ('terminal_branch', 'atm_brand')
@admin.register(DownReason)
class DownReasonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
# Alternatively, you can use admin.site.register() method
# admin.site.register(Branch, BranchAdmin)
# admin.site.register(Brand, BrandAdmin)
# admin.site.register(Terminal, TerminalAdmin)
