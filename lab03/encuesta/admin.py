from django.contrib import admin
from .models import Pregunta, Opcion

# Register your models here.
class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['pregunta_texto']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [OpcionInline]
    list_display = ('pregunta_texto', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['pregunta_texto']

admin.site.register(Pregunta, PreguntaAdmin)
