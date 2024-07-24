from django.contrib import admin
from django import forms

from post_machine.models import PostMachine
from .models import Parcel


class ParcelAdminForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ParcelAdminForm, self).__init__(*args, **kwargs)
        self.fields['post_machine_locker'].required = False
        self.fields['open_date_time'].required = False


class ParcelAdmin(admin.ModelAdmin):
    form = ParcelAdminForm


class PostMachineFilter(admin.SimpleListFilter):
    title = 'Post Machine'
    parameter_name = 'post_machine'

    def lookups(self, request, model_admin):
        post_machines = PostMachine.objects.all()
        return [(post_machine.id, post_machine.address) for post_machine in post_machines]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(post_machine__id=self.value())
        return queryset


admin.site.register(Parcel, ParcelAdmin)

