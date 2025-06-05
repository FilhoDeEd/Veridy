from common.models import UserTypeChoices
from django import template
from django.urls import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def url_for_user_type(context, url_type):
    """
    Returns the correct URL for the current user based on their user type.

    Usage in templates:
        {% url_for_user_type 'profile' %}

    This will resolve to 'subject_profile' or 'institution_profile'
    depending on whether the user is a Subject or Institution.

    If the user is not authenticated or the URL name cannot be reversed,
    it returns '#' as a fallback.
    """
    user = context.get('user')

    if not user or not user.is_authenticated:
        return '#'

    user_type = getattr(user, 'user_type', None)

    try:
        if user_type == UserTypeChoices.SUBJECT:
            return reverse(f'subject_{url_type}')
        elif user_type == UserTypeChoices.INSTITUTION:
            return reverse(f'institution_{url_type}')
        else:
            return '#'
    except Exception:
        return '#'
