from django.db import models


class FestPass(models.Model):
    """Model for GITAM Students Festpass"""

    name = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    roll_number = models.CharField(max_length=300, blank=True, null=True)
    participation_category = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    participation_type = models.CharField(max_length=300, blank=True, null=True)
    faculty_or_other = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    confirm_id = models.CharField(max_length=300, blank=True, null=True)
    txn_id = models.CharField(max_length=300, blank=True, null=True)
    transaction_status = models.CharField(max_length=300, blank=True, null=True)
    order_id = models.CharField(max_length=300, blank=True, null=True)
    bankref_number = models.CharField(max_length=300, blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)


class Registrations(models.Model):
    """Model for Non-GITAM Students festpass"""

    name = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    roll_number = models.CharField(max_length=300, blank=True, null=True)
    participation_category = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    participation_type = models.CharField(max_length=300, blank=True, null=True)
    faculty_or_other = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    confirm_id = models.CharField(max_length=300, blank=True, null=True)
    txn_id = models.CharField(max_length=300, blank=True, null=True)
    transaction_status = models.CharField(max_length=300, blank=True, null=True)
    order_id = models.CharField(max_length=300, blank=True, null=True)
    bankref_number = models.CharField(max_length=300, blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)


class Accomdation(models.Model):
    """Model for accomdation"""

    name = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    roll_number = models.CharField(max_length=300, blank=True, null=True)
    participation_category = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    participation_type = models.CharField(max_length=300, blank=True, null=True)
    faculty_or_other = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    confirm_id = models.CharField(max_length=300, blank=True, null=True)
    txn_id = models.CharField(max_length=300, blank=True, null=True)
    transaction_status = models.CharField(max_length=300, blank=True, null=True)
    order_id = models.CharField(max_length=300, blank=True, null=True)
    bankref_number = models.CharField(max_length=300, blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    """Model for Non-GITAM Competition"""

    name = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    roll_number = models.CharField(max_length=300, blank=True, null=True)
    participation_category = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    participation_type = models.CharField(max_length=300, blank=True, null=True)
    faculty_or_other = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True, null=True)
    confirm_id = models.CharField(max_length=300, blank=True, null=True)
    txn_id = models.CharField(max_length=300, blank=True, null=True)
    transaction_status = models.CharField(max_length=300, blank=True, null=True)
    order_id = models.CharField(max_length=300, blank=True, null=True)
    bankref_number = models.CharField(max_length=300, blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name