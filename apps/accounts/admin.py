from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from .tasks import send_fake_mail

from .models import User


class GuestNotifyForm(forms.Form):
    """
    To notify the group of guests, message will be emailed to all selected users
    """
    message = forms.CharField(widget=forms.Textarea)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    actions = ('notify_selected_guests',)

    def notify_selected_guests(self, request, queryset):
        qs = queryset.filter(role=User.ROLE_GUEST).exclude(email='')

        if 'send_notify' in request.POST:
            message = request.POST.get('message')
            for guest in qs:
                send_fake_mail.delay(guest.email, message)
                # print(guest.email, message)
            messages.info(request, _('Notification messages has been sent'))
            return HttpResponseRedirect(request.get_full_path())

        return render(
            request, 'admin/accounts/guest_notify.html',
            context=dict(form=GuestNotifyForm, title=_('Input notify message'), guests=qs)
        )
    notify_selected_guests.short_description = _("Notify selected guests")
