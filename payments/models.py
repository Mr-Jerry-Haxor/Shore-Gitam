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
    

class nongitamite(models.Model):
    """Model for Non-GITAM festpass"""

    name = models.CharField(max_length=300, blank=True, null=True)
    mobile = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    college = models.CharField(max_length=300, blank=True, null=True)
    college_roll_number = models.CharField(max_length=300, blank=True, null=True)
    branch = models.CharField(max_length=300, blank=True, null=True)
    year_of_study = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    event_type = models.CharField(max_length=300, blank=True, null=True)
    event_name = models.CharField(max_length=300, blank=True, null=True)
    accommodation = models.BooleanField(default=False)
    payment = models.CharField(max_length=300, blank=True, null=True)
    paid = models.BooleanField(default=False)
    shoreid = models.CharField(max_length=200, unique=True, editable=False)
    campus = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created (not updated)
            last_id = nongitamite.objects.order_by("-id").first()
            if last_id:
                last_shore_id = int(last_id.shoreid[6:-3])  # Extracting numeric part
                new_shore_id = last_shore_id + 1
            else:
                new_shore_id = 1

            self.shoreid = f"shore{new_shore_id:05d}024"

        super().save(*args, **kwargs)