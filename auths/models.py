from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import Q


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, False, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email
    
    def get_tournament_Count(self):
        from manager import models
 
        return models.Tournament.objects.filter( 
                    Q(match__teamA__lead__email=self.email) | Q(match__teamA__player2__email=self.email) | Q(match__teamA__player3__email=self.email) | Q(match__teamA__player4__email=self.email)|Q(match__teamA__player5__email=self.email) 
                    |Q(match__teamB__lead__email=self.email) | Q(match__teamB__player2__email=self.email) | Q(match__teamB__player3__email=self.email) | Q(match__teamB__player4__email=self.email)|Q(match__teamB__player5__email=self.email) 
            ).distinct().count() 

    
