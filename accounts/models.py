from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Tier(models.Model):
    tier = models.IntegerField(primary_key=True)
    max_upload = models.IntegerField(default=0)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return str(self.max_upload)


class Country(TimeStampedModel):
    dist_code = models.CharField(max_length=3, primary_key=True)
    dist_num = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    orig_code = models.CharField(max_length=100, null=True, blank=True)
    uncertainty = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '%s' % self.country

    class Meta:
        verbose_name_plural = "Countries"
        verbose_name = "Country"


class User(AbstractUser):
    NO_SOCIAL = 0
    FACEBOOK = 1

    SOCIAL_TYPES = ((NO_SOCIAL, "No social"),
                    (FACEBOOK, "Facebook"))
                    
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, null=True)
    # ,  unique=True,)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    created_date = models.DateTimeField(auto_now_add=True)
    tier = models.ForeignKey(Tier, related_name='users',
                             on_delete=models.DO_NOTHING, null=True, blank=True)
    credited_name = models.CharField(max_length=255, null=True)
    specialty = models.CharField(max_length=255, null=True)

    reset_pass_code = models.CharField(max_length=50, null=True, blank=True)
    reset_pass_code_attemps = models.IntegerField(default=-1)

    verify_mail_code = models.CharField(max_length=50, null=True)
    email_verified = models.BooleanField(default=False)
    
    social_type = models.IntegerField(
        choices=SOCIAL_TYPES, db_index=True, default=NO_SOCIAL)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    # Username, Email & Password are required by default.
    REQUIRED_FIELDS = ['email']

    def get_email(self):
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.username

    def get_author(self):
        return self.profile.credited_name

    # def get_author(self):
    #     author = Profile.objects.get(user_id=self.id)
    #     return author.current_credit_name


class Photographer(TimeStampedModel):
    author_id = models.CharField(max_length=50, primary_key=True)
    displayname = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    affiliation = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    web = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, default='TBD')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    expertise = models.CharField(max_length=500, null=True)
    # user_id   = models.OneToOneField(User,unique=True, null=True, blank=True, db_column='user_id', related_name='userid', on_delete=models.DO_NOTHING)
    user_id = models.OneToOneField(
        User,
        db_column='user_id',
        null=True,
        on_delete=models.DO_NOTHING)
    # models.ForeignKey(User, null=True, blank=True, db_column='user_id', related_name='userid', on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.displayname != self.fullname:
            return '%s (%s)' % (self.displayname, self.fullname)
        return self.fullname

    def __str__(self):
        if self.displayname != self.fullname:
            return '%s (%s)' % (self.displayname, self.fullname)
        return self.fullname


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    credited_name = models.CharField(max_length=255, null=True)
    current_credit_name = models.OneToOneField(
        Photographer, blank=True, null=True, on_delete=models.DO_NOTHING)
    photo_credit_name = models.CharField(max_length=100, blank=True)
    photographer = models.OneToOneField(
        Photographer, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='profile_photographer')
    specialty = models.CharField(max_length=500, null=True, blank=True)
    portfolio_site = models.URLField(max_length=500, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics', null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, null=True, blank=True)
    approved = models.BooleanField(blank=True, default=True)

    def __str__(self):
        if self.user.fullname:
            return self.user.fullname
        else:
            return self.user.username
