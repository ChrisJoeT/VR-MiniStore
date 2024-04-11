from django.contrib import admin
from myapp.models import *
# Register your models here.
class useradmin(admin.ModelAdmin):
    list_display = ('fname','mobile','email','password','rights')

admin.site.register(userreg, useradmin)
admin.site.register(product)
#username : ChrisJoe
#password : chris9383424792
