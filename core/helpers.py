from core import models as core_models
from django.db.models import Q
import datetime

def get_active_key():
    key_queryset = core_models.Key.objects.all().values('id')

    keys = [key['id'] for key in key_queryset]

    today = datetime.datetime.now().date()
    
    query = Q(key_id__in = keys) & Q(expired=True) & Q(date = today)
    
    key_usages = core_models.KeyUsage.objects.filter(query).values('key_id')

    expired_keys = [key['key_id'] for key in key_usages]

    key_ids_which_can_be_used = list( set(keys) - set(expired_keys))

    if len(key_ids_which_can_be_used) > 0:
        # Return the first key to be used
        key_usage, _ = core_models.KeyUsage.objects.get_or_create(key_id=key_ids_which_can_be_used[0], date = today)
        key_usage.expired = False
        key_usage.save()
        return key_ids_which_can_be_used[0]
    else:
        return None