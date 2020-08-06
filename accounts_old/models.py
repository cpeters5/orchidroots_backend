from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Tier(models.Model):
    tier        = models.IntegerField(primary_key=True)
    max_upload  = models.IntegerField(default=0)
    description = models.CharField(max_length=150, null=True, blank=True)
    def __str__(self):
        return self.max_upload


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, fullname=None, credited_name=None, is_staff=False, is_admin=False, is_active=True):
        if not username:
            raise ValueError("User must have user name")
        if not email:
            raise ValueError("User must have email address")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(
            username = username,
            email = self.normalize_email(email),
            fullname = fullname,
            credited_name = credited_name,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, password=None):
        user_obj = self.create_user(
            username,
            email,
            password=password,
            is_staff=True
        )
        return user_obj

    def create_superuser(self, username, email, password=None):
        user_obj = self.create_user(
            username,
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user_obj


class User(AbstractBaseUser):
    username  = models.CharField(max_length=255, unique=True)
    fullname =  models.CharField(max_length=255, null=True)
    email = models.EmailField(verbose_name='email address', max_length=255) #,  unique=True,)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    created_date = models.DateTimeField(auto_now_add=True)
    tier = models.ForeignKey(Tier, null=True, default=1, db_column='tier',on_delete=models.DO_NOTHING)
    credited_name =  models.CharField(max_length=255, null=True)
    specialty =  models.CharField(max_length=255, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # Username, Email & Password are required by default.

    def get_email(self):
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    def get_author(self):
        author = Profile.objects.get(user_id=self.id)
        return author.current_credit_name

class Country(models.Model):
    # class Meta:
    #     unique_together = (("dist_code", "dist_num", "region"),)
    #     ordering = ['country','region']
    dist_code = models.CharField(max_length=3,primary_key=True)
    dist_num  = models.IntegerField(null=True, blank=True)
    country   = models.CharField(max_length=100,null=True, blank=True)
    region    = models.CharField(max_length=100,null=True, blank=True)
    orig_code = models.CharField(max_length=100,null=True, blank=True)
    uncertainty = models.CharField(max_length=10,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.country


class Photographer(models.Model):
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
    user_id   =  models.OneToOneField(
        User,
        db_column='user_id',
        null = True,
        on_delete=models.DO_NOTHING)
        # models.ForeignKey(User, null=True, blank=True, db_column='user_id', related_name='userid', on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.displayname != self.fullname:
            return '%s (%s)' % (self.displayname, self.fullname)
        return self.fullname

    # def mypriphoto (self):
    #     myimg = SpcImages.objects.filter(rank__gt=0).filter(user_id=self.user_id).count() + \
    #             SpcImages.objects.filter(rank__gt=0).filter(user_id=self.user_id).count() + \
    #             UploadFile.objects.filter(user_id=self.user_id).count()
    #     return '%' % str(myimg)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fullname = models.CharField(max_length=255,blank=True,null=True)
    confirm_email = models.CharField(max_length=100, blank=True)
    photo_credit_name = models.CharField(max_length=100, blank=True)
    current_credit_name = models.OneToOneField(Photographer, blank=True, null=True, on_delete=models.DO_NOTHING)
    specialty = models.CharField(max_length=500, null=True,blank=True)
    portfolio_site = models.URLField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',null=True,blank=True)
    # country = models.CharField(max_length=10, null=True, blank=True)
    country = models.ForeignKey(Country,db_column='country',on_delete=models.DO_NOTHING,null=True, blank=True)
    approved = models.BooleanField( blank=True, default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        if self.user.fullname:
            return self.user.fullname
        else:
            return self.user.username


class Donation(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, blank=True,null=True,on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    payment_type = models.CharField(max_length=20,blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Partner(models.Model):
    partner_id = models.CharField(max_length=50, primary_key=True)
    author = models.ForeignKey(Photographer,db_column='author',on_delete=models.DO_NOTHING,null=True, blank=True)
    displayname = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    logo = models.CharField(max_length=50, blank=True)
    banner = models.CharField(max_length=50, blank=True)
    banner_color = models.CharField(max_length=50, blank=True)
    affiliation = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    web = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, default='TBD')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    information = models.TextField(null=True)
    user_id   =  models.OneToOneField(
        User,
        db_column='user_id',
        null = True,
        on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.displayname != self.fullname:
            return '%s' % (self.displayname)
        return self.fullname


