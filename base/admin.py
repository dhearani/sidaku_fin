from django.contrib import admin
from base.models import Details, ProdukHukum
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class DetailsInLine(admin.StackedInline):
    model = Details
    can_delete = False
    verbose_name_plural = 'Details'
    
class CustomizedUserAdmin (UserAdmin):
    inlines = (DetailsInLine, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Details)
admin.site.register(ProdukHukum)