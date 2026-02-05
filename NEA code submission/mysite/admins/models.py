from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields.ranges import IntegerRangeField,DecimalRangeField


from django.db import models
from django.contrib.auth.models import User  # This is the built-in User model

# forms.py

category_choices = [
    ('accessories', 'Accessories'),
    ('art', 'Art'),
    ('beauty_and_fragrance', 'Beauty and Fragrance'),
    ('food_and_drink', 'Food and Drink'),
    ('gifts', 'Gifts'),
    ('homewares', 'Homewares'),
    ('jewellery', 'Jewellery'),
    ('kids', 'Kids'),
    ('ladies_clothing', 'Ladies Clothing'),
    ('mens', 'Mens'),
    ('stationary', 'Stationary'),
    ('other', 'Other'),
]


# Custom User model extending Django's built-in User
class Auth_User(User):
    class Meta:
        managed = False
        db_table = 'auth_user'


# Names Model
class Names(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    stallholdername = models.CharField(blank=True, null=True)
    buisname = models.CharField(max_length=255, primary_key=True,)
    comments = models.CharField(max_length=255, null=True,) 
    
    class Meta:
        managed = False
        db_table = 'namers'
    
    def __str__(self):
        return self.buisname

# General Info Model
class GeneralInfo(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    email = models.EmailField(max_length=255, primary_key=True)
    adress = models.CharField(max_length=255, blank=True, null=True)
    phonenumber = models.CharField(max_length=11, blank=True, null=True)
    tsandcs = models.BooleanField(blank=True, null=True, db_column='tsandcs')
    referral_source = models.CharField(max_length=255, blank=True, null=True, db_column='referral source')
    aob = models.CharField(blank=True, null=True, db_column='AOB')
    
    class Meta:
        managed = False
        db_table = 'generalinfo'
    
    def __str__(self):
        return self.email

# Stall Type Model
class StallType(models.Model):
    rail = models.BooleanField(blank=True, null=True, db_column='rail')
    numtables = models.IntegerField(blank=True, null=True)
    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    class Meta:
        managed = False
        db_table = 'stalltype'
    
    def __str__(self):
        return f"Rail: {self.rail}"

# Trading Model
class Trading(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    buisname = models.ForeignKey(
        'Names',
        on_delete=models.CASCADE,
        to_field='buisname',
        blank=True,
        null=True
    )
    MRDfair = models.DateField(blank=True, null=True)
    productdesc = models.CharField(blank=True, null=True)
    category = models.CharField(max_length=25, choices = category_choices)
    wherelsesold = models.CharField(blank=True, null=True)
    recordnum = models.AutoField(primary_key = True )
    
    class Meta:
        managed = False
        db_table = 'trading'
    
    def __str__(self):
        return f"Trading on {self.MRDfair}"

# Fairs Attended Model
class FairsAttended(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    buisname = models.ForeignKey(
        'Names',
        on_delete=models.CASCADE,
        to_field='buisname',
        blank=True,
        null=True
    )
    yearstrading = models.IntegerField(blank=True, null=True)
    prevfairs = models.CharField(max_length=255, blank=True, null=True)
    no_prevfairs = models.IntegerField(blank=True, null=True)
    recordnum = models.AutoField(primary_key=True, null = False)
    
    class Meta:
        managed = False
        db_table = 'fairsattended'
    
    def __str__(self):
        return f"Fairs {self.yearstrading}"

# Finances Model
class Finances(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    buisname = models.ForeignKey(
        'Names',
        on_delete=models.CASCADE,
        to_field='buisname',
        blank=True,
        null=True
    )
    yearstrading = models.IntegerField(blank=True, null=True)
    SimEarnings = models.IntegerField(blank=True, null=True)
    pricerange = DecimalRangeField(blank=True, null=True)
    recordnum = models.AutoField(primary_key=True, null = False)
    MRDfair = models.DateField(blank=True,null=True)
    MRDfairEarnings = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'finances'
    
    def __str__(self):
        return f"Finances {self.simearnings}"

# Social Media Model
class SocialMedia(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    buisname = models.ForeignKey(
        'Names',
        on_delete=models.CASCADE,
        to_field='buisname',
        blank=True,
        null=True
    )
    weblink = models.URLField(max_length=255, blank=True, null=True)
    somedialinks = models.CharField(max_length=255, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    marketingplan = models.CharField(max_length=255, blank = True, null=True)
    record_id = models.AutoField(primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'socialmedia'
    
    def __str__(self):
        return f"Social Media {self.user}"

# Status Model
class Status(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    buisname = models.ForeignKey(
        'Names',
        on_delete=models.CASCADE,
        to_field='buisname',
        blank=True,
        null=True
    )
    reviewed = models.BooleanField(blank=True, null = True)
    starred = models.BooleanField(blank=True, null=True)
    accepted = models.BooleanField(blank=True, null=True)
    denied = models.BooleanField(blank=True, null=True)
    recordnum = models.AutoField(primary_key=True, null = False)
    emailed = models.BooleanField(blank=True, null = True)
    fsub = models.BooleanField(blank = True, null = True)
    
    class Meta:
        managed = False
        db_table = 'status'
    
    def __str__(self):
        return f"Status {self.reviewed}"

# Django Built-in Models (for reference and compatibility)

class AuthGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    
    class Meta:
        managed = False
        db_table = 'auth_group'
    
    def __str__(self):
        return self.name

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE, db_column='group_id')
    permission = models.ForeignKey('AuthPermission', on_delete=models.CASCADE, db_column='permission_id')
    
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
    
    def __str__(self):
        return f"Group {self.group} - Permission {self.permission}"

class AuthPermission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE, db_column='content_type_id')
    codename = models.CharField(max_length=100)
    
    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)
    
    def __str__(self):
        return f"{self.content_type} - {self.codename}"

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Auth_User, on_delete=models.CASCADE, db_column='user_id')
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE, db_column='group_id')
    
    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)
    
    def __str__(self):
        return f"User {self.user} - Group {self.group}"

class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Auth_User, on_delete=models.CASCADE, db_column='user_id')
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE, db_column='permission_id')
    
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
    
    def __str__(self):
        return f"User {self.user} - Permission {self.permission}"

class DjangoAdminLog(models.Model):
    id = models.AutoField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE, blank=True, null=True, db_column='content_type_id')
    user = models.ForeignKey(Auth_User, on_delete=models.CASCADE, db_column='user_id')
    
    class Meta:
        managed = False
        db_table = 'django_admin_log'
    
    def __str__(self):
        return f"Admin Log {self.id}"

class DjangoContentType(models.Model):
    id = models.AutoField(primary_key=True)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    
    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)
    
    def __str__(self):
        return f"{self.app_label}.{self.model}"

class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'django_migrations'
    
    def __str__(self):
        return f"{self.app}.{self.name}"

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'django_session'
    
    def __str__(self):
        return self.session_key

class Updatestable(models.Model):
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    infoup = models.CharField(max_length=255, blank = True, null=True)
    recordnum = models.AutoField(primary_key=True, null = False)

    class Meta:
        managed = False
        db_table = 'updatestable'
    def __str__(self):
        return self.recordnum



# Admin Accounts Model
class AdminAccount(models.Model):
    email = ArrayField(
        models.CharField(max_length=255),
        size=None,
        blank=True,
        null=True
    )
    password = ArrayField(
        models.CharField(max_length=255),
        size=None,
        blank=True,
        null=True
    )
    groupcode = models.IntegerField(blank=True, null=True)
    adminid = models.AutoField(primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'adminaccounts'
    
    def __str__(self):
        return f"Admin {self.adminid}"

# Applicant Accounts Model
class ApplicantAccount(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    appid = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'Auth_User',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    class Meta:
        managed = False
        db_table = 'applicantaccounts'
    
    def __str__(self):
        return f"Applicant {self.appid}"