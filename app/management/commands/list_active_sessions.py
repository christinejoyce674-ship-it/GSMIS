from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils import timezone


class Command(BaseCommand):
    help = 'List all active user sessions'

    def handle(self, *args, **options):
        User = get_user_model()
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        
        self.stdout.write(self.style.SUCCESS(f'\nFound {active_sessions.count()} active sessions:\n'))
        
        for session in active_sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    user_type_display = dict(User.USER_TYPES).get(user.user_type, 'Unknown')
                    self.stdout.write(
                        f'  • {user.email} ({user_type_display}) - '
                        f'Expires: {session.expire_date.strftime("%Y-%m-%d %H:%M:%S")}'
                    )
                except User.DoesNotExist:
                    self.stdout.write(f'  • Unknown user (ID: {user_id})')
            else:
                self.stdout.write('  • Anonymous session')
        
        self.stdout.write('')
