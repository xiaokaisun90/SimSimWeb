from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    # user_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User)
    # user_id = models.IntegerField(max_length=10, null=True)
    primary_mobile_number = models.CharField(max_length=50)
    is_mobile_verified = models.CharField(max_length=1, null=True)
    country = models.CharField(max_length=50, null=True)
    account_created = models.DateTimeField(null=True)
    account_verified = models.DateTimeField(null=True)
    last_sign_in = models.DateTimeField(null=True)
    is_web_registered = models.CharField(max_length=1, null=True)
    # possible foreign key
    user_state_id = models.IntegerField(null=True)

class Properties(models.Model):
    property_id = models.IntegerField(primary_key=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=24)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    is_visible_to_guests = models.CharField(max_length=1)

class Locks(models.Model):
    lock_id = models.IntegerField(primary_key=True)
    lock_purpose = models.CharField(max_length=64)
    is_lock_configured = models.BooleanField(default=False)
    description = models.TextField()
    is_lock_active = models.BooleanField(default=False)
    lock_secret = models.CharField(max_length=255)
    is_locked = models.BooleanField(default=False)
    subscription_expiry_date = models.DateTimeField()
    subscription_last_paid_date = models.DateTimeField()
    subscription_expiry_amount = models.IntegerField()
    subscription_plan_id = models.IntegerField()
    family_count = models.IntegerField()
    guest_count = models.IntegerField()
    lock_power = models.FloatField()
    lock_start_angle = models.FloatField()
    lock_end_angle = models.FloatField()

class UserPropertyLocks(models.Model):
    user_id = models.IntegerField()
    property_lock_id = models.IntegerField()
    user_role_type_id = models.IntegerField()

class PropertyLocks(models.Model):
    property_lock_id = models.IntegerField()
    property_id = models.IntegerField()
    lock_id = models.IntegerField()

class UserProfile(models.Model):
    user_id = models.ForeignKey(User, primary_key=True)
    avatar_url = models.CharField(max_length=300)
    data_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=1)
    email_address = models.CharField(max_length=100)
    is_email_verified = models.CharField(max_length=1)
    alternate_mobile_number = models.CharField(max_length=50)
    is_alternate_mobile_verified = models.CharField(max_length=1)
    primary_address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=50)
    search_engine_visibility = models.CharField(max_length=1)

class UserIntermediateData(models.Model):
    user_id = models.IntegerField()
    intermediate_mobile_number = models.CharField(max_length=50)
    intermediate_email_address = models.CharField(max_length=100)

class UserNotificationPreferences(models.Model):
    user_id = models.IntegerField()
    lock_unlock_notification_choice = models.BooleanField(default=False)
    unlocked_5mins_notification_choice = models.BooleanField(default=False)
    guest_request_access_notification_choice = models.BooleanField(default=False)
    wifi_disconnected_notification_choice = models.BooleanField(default=False)

class UserState(models.Model):
    user_state_id = models.IntegerField(primary_key=True)
    user_state_type = models.CharField(max_length=50)

class UserRoleTypes(models.Model):
    user_role_type_id = models.IntegerField()
    user_role_type = models.CharField(max_length=64)

class SubscriptionPlans(models.Model):
    subscription_plan_id = models.IntegerField()
    subscription_plan = models.CharField(max_length=50)

class LockActivity(models.Model):
    lock_id = models.IntegerField()
    lock_activity_type_id = models.IntegerField()
    lock_activity_time_stamp = models.DateTimeField()
    user_id = models.IntegerField()

class LockActivityType(models.Model):
    lock_activity_id = models.IntegerField()
    lock_activity_type = models.CharField(max_length=64)

class UserAccessRequest(models.Model):
    user_id = models.IntegerField()
    request_id = models.IntegerField()

class GuestAccessRequestQueue(models.Model):
    request_id = models.IntegerField(primary_key=True)
    property_id = models.ForeignKey(Properties)
    requested_access_start_time = models.DateTimeField()
    requested_access_end_time = models.DateTimeField()
    request_access_time_stamp = models.IntegerField()

class ApprovedAccessRequest(models.Model):
    request_id = models.IntegerField(primary_key=True)
    property_lock_id = models.ForeignKey(PropertyLocks)
    access_given_by_user_id = models.IntegerField()
    allocated_access_start_time = models.DateTimeField()
    allocated_access_end_time = models.DateTimeField()
    access_request_state_id = models.IntegerField()
    response_access_time_stamp = models.DateTimeField()



