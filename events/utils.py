from datetime import datetime
from django.utils.crypto import get_random_string

def path_and_rename(user_id, filename):
        # ext = filename.split('.')[-1]
        ext = 'webp'
        now = datetime.now()
        if user_id:
            filename = '{}{}.{}'.format(now.strftime('%d%H%M%S'), str(user_id), ext)
        else:
            allowed_chars=u'abcdefghijklmnopqrstuvwxyz0123456789'
            filename = '{}{}.{}'.format(now.strftime('%d%H%M%S'), get_random_string(length=5, allowed_chars=allowed_chars), ext)
        return filename