from django.contrib import admin

from user.models import CustomUser

admin.site.register(CustomUser)

from django.contrib import messages

def has_delete_permission(self, request, obj=None):
    if request.POST and request.POST.get('action') == 'delete_selected':
        if '1' in request.POST.getlist('_selected_action'):
            messages.add_message(request, messages.ERROR, (
                "Widget #1 is protected, please remove it from your selection "
                "and try again."
            ))
            return False
        return True
    return obj is None or obj.pk != 1
