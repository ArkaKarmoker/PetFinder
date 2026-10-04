from django.contrib import admin
from .models import Pet, AdoptionRequest, Favorite

# Register your models here.

admin.site.site_header = "PetFinder Administration"
admin.site.site_title = "PetFinder Admin Portal"
admin.site.index_title = "Pet Adoption & Rescue Management"


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'age', 'gender', 'location', 'status', 'created_at')
    list_filter = ('status', 'animal_type', 'gender', 'location', 'created_at')
    search_fields = ('name', 'breed', 'location', 'description')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        ("Basic Information", {
            'fields': ('name', 'animal_type', 'breed', 'age', 'gender')
        }),
        ("Location & Status", {
            'fields': ('location', 'status')
        }),
        ("Media & Details", {
            'fields': ('image', 'description')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_available', 'mark_as_adopted']

    @admin.action(description="Mark selected pets as Available")
    def mark_as_available(self, request, queryset):
        queryset.update(status='Available')

    @admin.action(description="Mark selected pets as Adopted")
    def mark_as_adopted(self, request, queryset):
        queryset.update(status='Adopted')


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pet', 'phone', 'short_reason', 'previous_pet_experience', 'status', 'created_at')
    list_filter = ('status', 'previous_pet_experience', 'created_at')
    search_fields = ('user__username', 'user__email', 'pet__name', 'phone', 'address', 'reason')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    @admin.display(description="Reason")
    def short_reason(self, obj):
        return (obj.reason[:40] + '...') if len(obj.reason) > 40 else obj.reason
    fieldsets = (
        ("Application Overview", {
            'fields': ('user', 'pet', 'status')
        }),
        ("Applicant Contact Details", {
            'fields': ('phone', 'address')
        }),
        ("Adoption Questionnaire", {
            'fields': ('reason', 'previous_pet_experience', 'message')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_requests', 'reject_requests']

    @admin.action(description="Approve selected adoption requests (Mark pet as Adopted)")
    def approve_requests(self, request, queryset):
        count = 0
        for adoption in queryset:
            adoption.status = 'Approved'
            adoption.save()  # Triggers business logic in model save()
            count += 1
        self.message_user(request, f"{count} adoption request(s) approved successfully.")

    @admin.action(description="Reject selected adoption requests")
    def reject_requests(self, request, queryset):
        count = 0
        for adoption in queryset:
            adoption.status = 'Rejected'
            adoption.save()
            count += 1
        self.message_user(request, f"{count} adoption request(s) rejected successfully.")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'pet__name')
    readonly_fields = ('created_at',)
