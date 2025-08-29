from django.contrib import admin
from .models import Institution, DomainVerificationToken, LegalRepresentative


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'acronym', 'status', 'domain', 'domain_verified', 'domain_verification_date')
    list_filter = ('status', 'domain_verified', 'country', 'state')
    search_fields = ('name', 'acronym', 'domain', 'user__username')
    readonly_fields = ('creation_date', 'update_date', 'domain_verification_date')

    fieldsets = (
        ('Dados Básicos', {
            'fields': ('user', 'name', 'acronym', 'phone', 'status')
        }),
        ('Localização', {
            'fields': ('city', 'state', 'country', 'full_address')
        }),
        ('Representante Legal', {
            'fields': ('representative',)
        }),
        ('Domínio', {
            'fields': ('domain', 'domain_verified', 'domain_verification_date')
        }),
        ('Timestamps', {
            'fields': ('creation_date', 'update_date'),
        }),
    )


@admin.register(DomainVerificationToken)
class DomainVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('institution', 'temporary_domain', 'token', 'creation_date', 'expiration_date', 'is_expired_display')
    search_fields = ('institution__user__username', 'temporary_domain', 'token')
    readonly_fields = ('token', 'creation_date', 'expiration_date')

    def is_expired_display(self, obj):
        return obj.is_expired
    is_expired_display.boolean = True
    is_expired_display.short_description = 'Expirado?'


@admin.register(LegalRepresentative)
class LegalRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'phone', 'creation_date', 'update_date')
    search_fields = ('name', 'role', 'email')
    readonly_fields = ('creation_date', 'update_date')
