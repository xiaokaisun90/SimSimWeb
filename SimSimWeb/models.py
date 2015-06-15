from django.db import models
from django.contrib.auth.models import User

class UserState(models.Model):
    user_state_id = models.IntegerField(primary_key=True)
    user_state_type = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user_state_type


class UserRoleTypes(models.Model):
    user_role_type_id = models.IntegerField(primary_key = True)
    user_role_type = models.CharField(max_length=64)
    def __unicode__(self):
        return self.user_role_type


class UserInfo(models.Model):
    #user_num is the user_id to avoid the clash with built-in user
    user_id = models.OneToOneField(User, primary_key = True)
    primary_mobile_number = models.CharField(max_length=50)
    is_mobile_verified = models.CharField(max_length=1, null=True)
    country = models.CharField(max_length=50, null=True)
    account_created = models.DateTimeField(null=True)
    account_verified = models.DateTimeField(null=True)
    last_sign_in = models.DateTimeField(null=True)
    is_web_registered = models.CharField(max_length=1, null=True)
    # possible foreign key
    user_state_id = models.ForeignKey(UserState)
    def __unicode__(self):
        print(type(self.user_id))
        return self.user_id.username


class UserProfile(models.Model):
    user_id = models.ForeignKey(UserInfo, primary_key=True)
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


class SubscriptionPlans(models.Model):
    subscription_plan_id = models.IntegerField(primary_key = True)
    subscription_plan = models.CharField(max_length=50)


class Properties(models.Model):
    property_id = models.IntegerField(primary_key=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=24)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    is_visible_to_guests = models.CharField(max_length=1)
    def __unicode__(self):
        return self.address + ", " + self.city + ", " + self.state + " " +self.zipcode + ", " + self.country


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
    subscription_plan_id = models.ForeignKey(SubscriptionPlans)
    family_count = models.IntegerField()
    guest_count = models.IntegerField()
    lock_power = models.FloatField()
    lock_start_angle = models.FloatField()
    lock_end_angle = models.FloatField()
    def __unicode__(self):
        return self.lock_purpose


class PropertyLocks(models.Model):
    property_lock_id = models.IntegerField(primary_key=True)
    property_id = models.ForeignKey(Properties)
    lock_id = models.ForeignKey(Locks)
    def __unicode__(self):
        # print(type(self.lock_id))
        return str(self.lock_id)


class UserPropertyLocks(models.Model):
    user_id = models.ForeignKey(UserInfo)
    property_lock_id = models.ForeignKey(PropertyLocks)
    user_role_type_id = models.ForeignKey(UserRoleTypes)


class UserIntermediateData(models.Model):
    user_id = models.ForeignKey(UserInfo, primary_key=True)
    intermediate_mobile_number = models.CharField(max_length=50)
    intermediate_email_address = models.CharField(max_length=100)


class UserNotificationPreferences(models.Model):
    user_id = models.ForeignKey(UserInfo, primary_key=True)
    lock_unlock_notification_choice = models.BooleanField(default=False)
    unlocked_5mins_notification_choice = models.BooleanField(default=False)
    guest_request_access_notification_choice = models.BooleanField(default=False)
    wifi_disconnected_notification_choice = models.BooleanField(default=False)


class LockActivityType(models.Model):
    lock_activity_type_id = models.IntegerField(primary_key = True)
    lock_activity_type = models.CharField(max_length=64)
    def __unicode__(self):
        return self.lock_activity_type.lower()


class LockActivity(models.Model):
    lock_activity_id = models.IntegerField(primary_key = True)
    lock_id = models.ForeignKey(Locks)
    lock_activity_type_id = models.ForeignKey(LockActivityType)
    lock_activity_time_stamp = models.DateTimeField()
    user_id = models.ForeignKey(UserInfo)
    def __unicode__(self):
        return str(self.user_id.user_id.username) + " " + str(self.lock_activity_type_id) + " " + str(self.lock_id)

    def activityTime(self):
        return self.lock_activity_time_stamp.strftime("%m/%d/%Y %H:%M")


class GuestAccessRequestQueue(models.Model):
    request_id = models.IntegerField(primary_key=True)
    property_id = models.ForeignKey(Properties)
    requested_access_start_time = models.DateTimeField()
    requested_access_end_time = models.DateTimeField()
    request_access_time_stamp = models.IntegerField()
    mobile_phone_number = models.IntegerField()
    repeat = models.BooleanField()
    access_times = models.IntegerField()


class UserAccessRequest(models.Model):
    user_id = models.ForeignKey(UserInfo)
    request_id = models.ForeignKey(GuestAccessRequestQueue)


class ApprovedAccessRequest(models.Model):
    request_id = models.IntegerField(primary_key=True)
    property_lock_id = models.ForeignKey(PropertyLocks)
    access_given_by_user_id = models.ForeignKey(UserInfo)
    allocated_access_start_time = models.DateTimeField()
    allocated_access_end_time = models.DateTimeField()
    access_request_state_id = models.IntegerField()
    response_access_time_stamp = models.DateTimeField()
