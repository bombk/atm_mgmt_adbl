from django.db import models


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ATM(models.Model):
    terminal_code = models.CharField(max_length=100, unique=True)
    terminal_branch = models.CharField(max_length=255)
    atm_ip = models.CharField(max_length=100)
    atm_brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    atm_acc_no = models.CharField(max_length=50, unique=True)
    branch_code = models.CharField(max_length=50)
    atm_user = models.CharField(null=True, blank=True,max_length=100)
    atm_password = models.CharField(null=True, blank=True,max_length=100)
    atm_ram = models.CharField(null=True, blank=True,max_length=50)
    atm_storage = models.CharField(null=True, blank=True,max_length=50)
    atm_os = models.CharField(null=True, blank=True,max_length=50)
    atm_bit = models.CharField(null=True, blank=True,max_length=10)

    def __str__(self):
        return f"{self.terminal_code} - {self.atm_brand}"

    
class DownReason(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name


class ATMDown(models.Model):
    terminal_code = models.CharField(max_length=100)
    terminal_branch = models.CharField(max_length=255)
    atm_brand = models.CharField(max_length=100)
    down_date= models.DateField()
    down_reason = models.ForeignKey(DownReason, on_delete=models.CASCADE)
    remarks= models.CharField(max_length=255)

    def __str__(self):  
        return self.terminal_code

