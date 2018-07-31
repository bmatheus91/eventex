from django.contrib import admin
from django.utils.html import format_html
from eventex.core.models import Speaker, Contact, Talk, Course


# Register your models here.
class ContactInline(admin.TabularInline):

    model = Contact
    extra = 1


class SpeakerModelAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'photo_img', 'website_link', 'email', 'phone']
    inlines = [ContactInline]

    def website_link(self, obj):
        return format_html('<a href="{0}">{0}</a>', obj.website)

    website_link.short_description = 'website'

    def photo_img(self, obj):
        return format_html('<img width="32px" src="{0}" />', obj.photo)

    photo_img.short_description = 'foto'

    def email(self, obj):
        return obj.contact_set.emails().first()

    email.short_description = 'email'

    def phone(self, obj):
        return obj.contact_set.phones().first()

    phone.short_description = 'telefone'


admin.site.register(Speaker, SpeakerModelAdmin)

admin.site.register(Talk)
admin.site.register(Course)
