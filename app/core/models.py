from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from model_utils import Choices


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Client(models.Model):
    company_name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    company_url = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    logo = models.ImageField(
        upload_to="client_logo",
        null=True,
        blank=True,
        default=None
    )
    address_1 = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    mobile_number = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    create_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name='client_created_by',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Suspended'),
            (3, 'Deleted'),
            (4, 'Incomplete Profile'),
            (5, 'For Activation'),
        ],
        default=1
    )

    def __str__(self):
        return self.company_name


class ClientCompensation(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    type = models.IntegerField(
        choices=Choices(
            (1, 'Leave and absence'),
            (2, 'Overtime'),
        ),
        default=1
    )

    def __str__(self):
        client_name = ''
        name = ''
        if self.name:
            name = self.name

        if self.client:
            client_name = self.client.company_name

        return "%s %s" % (
            client_name,
            name
        )


class ClientBenefits(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self):
        client_name = ''
        name = ''
        if self.name:
            name = self.name

        if self.client:
            client_name = self.client.company_name

        return "%s %s" % (
            client_name,
            name
        )


class Department(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    representative = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    info = models.TextField(
        null=True,
        blank=True
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Department"

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Employees"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_user',
        db_index=True,
        blank=True,
        null=True
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        related_name='employees',
        db_index=True,
        null=True,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to="profile",
        null=True,
        blank=True,
        default=None
    )
    employee_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    gender = models.IntegerField(
        choices=Choices(
            (1, 'male'),
            (2, 'female'),
            (3, 'other')
        ),
        default=3
    )
    date_hired = models.DateField(null=True, blank=True)
    job_title = models.ForeignKey(
        'JobTitle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    address_1 = models.TextField(null=True, blank=True)
    address_2 = models.TextField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    mobile_number = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    martial_status = models.IntegerField(
        choices=Choices(
            (1, 'Single'),
            (2, 'Married')
        ),
        default=1
    )
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(default=0)
    employee_status = models.IntegerField(
        choices=Choices(
            (1, 'Probationary'),
            (2, 'Project'),
            (3, 'Regular'),
        ),
        default=1
    )
    user_type = models.IntegerField(
        choices=[
            (1, 'Super Admin'),
            (2, 'Admin'),
            (3, 'Standard'),
        ],
        default=3
    )
    office_location = models.ForeignKey(
        'OfficeLocation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    level = models.ForeignKey(
        'Level',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    work_arrangement = models.IntegerField(
        choices=Choices(
            (1, 'WFH'),
            (2, 'ON_SITE'),
            (3, 'WFH/ON_SITE'),
        ),
        default=2
    )
    course_to_do = models.IntegerField(default=0)
    overdue_course = models.IntegerField(default=0)
    completed_course = models.IntegerField(default=0)
    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    cpioe = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    cpioe_contact_no = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Suspended'),
            (3, 'Deleted'),
            (4, 'Incomplete Profile'),
            (5, 'For Activation'),
        ],
        default=1
    )
    creation_step = models.IntegerField(
        choices=[
            (1, 'Step one'),
            (2, 'Step two'),
            (3, 'Step three'),
            (4, 'Step Four'),
            (5, 'Step Five'),
        ],
        default=1
    )
    sss_no = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    phil_no = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    tin_no = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    pagibig_no = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        first_name = ''
        last_name = ''

        if self.user:
            first_name = self.user.first_name
        if self.user:
            last_name = self.user.last_name

        return "%s %s" % (first_name, last_name)


class Attendance(models.Model):
    SITE_LOCATION = Choices(
        (1, 'WFH', ('WFH')),
        (2, 'ON_SITE', ('ON_SITE')),
    )

    TYPE = Choices(
        (1, 'TIMEIN', ('TIMEIN')),
        (2, 'TIMEOUT', ('TIMEOUT')),
        (3, 'LEAVE', ('LEAVE')),
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    approve = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(
        upload_to="attendance",
        null=True,
        blank=True,
        default=None
    )
    task_image = models.ImageField(
        upload_to="attendance",
        null=True,
        blank=True,
        default=None
    )
    remarks = models.TextField(
        null=True,
        blank=True
    )
    site_location = models.IntegerField(
        choices=SITE_LOCATION,
        null=True,
        blank=True
    )
    type = models.IntegerField(
        choices=TYPE,
        null=True,
        blank=True
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        related_name='client_admin',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"


class News(models.Model):

    memo_number = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        related_name='memo_client',
        db_index=True,
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    ftp = models.FileField(upload_to='memo', null=True, blank=True)
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        related_name="memo_department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    text = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Inactive'),
            (3, 'Incomplete'),
            (4, 'Deleted'),
        ],
        default=1
    )

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class Document(models.Model):

    control_number = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        related_name='form_client',
        db_index=True,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        related_name="form_department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date = models.DateTimeField(
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.TextField(null=True, blank=True)
    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Inactive'),
            (3, 'Incomplete'),
            (4, 'Deleted'),
        ],
        default=1
    )
    date_uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title


class DocumentFiles(models.Model):
    document = models.ForeignKey(
        'Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ftp = models.FileField(
        upload_to='form',
        null=True,
        blank=True
    )
    link = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    date_uploaded = models.DateTimeField(auto_now_add=True)
    version = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Document Files"
        verbose_name_plural = "Document Files"


class Notification(models.Model):

    sender = models.ForeignKey(
        User,
        related_name='notif_sender',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True
    )
    receiver = models.ForeignKey(
        User,
        related_name='notif_receiver',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True
    )
    from_client = models.ForeignKey(
        Client,
        related_name='notif_from_client',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True
    )
    to_client = models.ForeignKey(
        Client,
        related_name='notif_to_client',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True
    )

    subject = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    file = models.FileField(
        upload_to='notification',
        null=True, blank=True
    )
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    notif_type = models.IntegerField(
        choices=[
            (1, 'Feedback'),
            (2, 'Upload Logo Feature'),
            (3, 'Notify Client'),
        ],
        default=1
    )

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return "%s" % self.subject


class NewsFile(models.Model):
    news = models.ForeignKey(
        'News',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to='news',
        null=True,
        blank=True
    )
    link = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    date_uploaded = models.DateTimeField(
        auto_now_add=True
    )


class JobTitle(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Inactive'),
            (3, 'Deleted'),
        ],
        default=1
    )

    def __str__(self):
        client_name = ''
        name = ''
        if self.name:
            name = self.name

        if self.client:
            client_name = self.client.company_name

        return "%s %s" % (
            client_name,
            name
        )


class Level(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Inactive'),
            (3, 'Deleted'),
        ],
        default=1
    )

    def __str__(self):
        client_name = ''
        name = ''
        if self.name:
            name = self.name

        if self.client:
            client_name = self.client.company_name

        return "%s %s" % (
            client_name,
            name
        )


class OfficeLocation(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.IntegerField(
        choices=[
            (1, 'Active'),
            (2, 'Inactive'),
            (3, 'Deleted'),
        ],
        default=1
    )

    def __str__(self):
        client_name = ''
        name = ''
        if self.name:
            name = self.name

        if self.client:
            client_name = self.client.company_name

        return "%s %s" % (
            client_name,
            name
        )


class EducBackGround(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    school_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    date_graduated = models.DateTimeField(
        auto_now=False,
        null=True,
        blank=True,
        default=None,
    )
    degree = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    address = models.TextField(
        null=True, blank=True
    )

    educ_type = models.IntegerField(
        choices=[
            (1, 'Primary Education'),
            (2, 'Secondary Education'),
            (3, 'Tertiary Education'),
        ],
        default=1
    )

    def __str__(self):
        user_name = ''
        if self.employee:
            if self.employee.user:
                user_name = '%s %s' % (
                   self.employee.user.first_name,
                   self.employee.user.last_name
                )
        return user_name


class EmployeeCompensation(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    compensation = models.ForeignKey(
        'ClientCompensation',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    count = models.IntegerField(
        null=True,
        blank=True
    )
    type = models.IntegerField(
        choices=[
            (1, 'Leave And Absence'),
            (2, 'Overtime'),
        ],
        default=1
    )
    term = models.IntegerField(
        choices=[
            (1, 'Month'),
            (2, 'Year'),
        ],
        default=1
    )
    availability = models.IntegerField(
        choices=[
            (1, 'Upon Regularization'),
        ],
        default=1
    )

    def __str__(self):
        user_name = ''
        if self.employee:
            if self.employee.user:
                user_name = '%s %s' % (
                   self.employee.user.first_name,
                   self.employee.user.last_name
                )
        return user_name


class EmployeeBenefits(models.Model):
    benefits = models.ForeignKey(
        'ClientBenefits',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        default=0
    )
    term = models.IntegerField(
        choices=[
            (1, 'Month'),
            (2, 'Year'),
        ],
        default=1
    )
    start_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        user_name = ''
        if self.employee:
            if self.employee.user:
                user_name = '%s %s' % (
                   self.employee.user.first_name,
                   self.employee.user.last_name
                )
        return user_name


class Region(models.Model):
    name = models.CharField(max_length=200, null=True,)

    def __str__(self):
        return "%s" % (self.name)


class Province(models.Model):
    name = models.CharField(max_length=200, null=True,)
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        db_index=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s" % (self.name)


class City(models.Model):
    name = models.CharField(max_length=200, null=True,)
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        db_index=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s" % (self.name)


class Barangay(models.Model):
    name = models.CharField(max_length=200, null=True,)
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        db_index=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s" % (self.name)


# class Assessment(models.Model):
#     name = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     description = models.TextField(null=True, blank=True)
#     total_page = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     total_section = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     total_time = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     time_limit = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     logo = models.ImageField(
#         upload_to="assessment_logo",
#         null=True,
#         blank=True,
#         default=None
#     )
#     active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name = "Assessment"
#         verbose_name_plural = "Assessment"

#     def __str__(self):
#         return self.name


# class ClientAssessment(models.Model):
#     client = models.ForeignKey(
#         Client,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     assessment = models.ForeignKey(
#         Assessment,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     create_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     class Meta:
#         verbose_name = "Client Assessment"
#         verbose_name_plural = "Client Assessment"

#     def __str__(self):
#         return self.client.company_name


# class Section(models.Model):
#     assessment = models.ForeignKey(
#         Assessment,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     name = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     description = models.TextField(null=True, blank=True)
#     total_page = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     total_time = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     sequence = models.IntegerField(
#         null=True,
#         blank=True
#     )
#     is_certificate = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = "Section"
#         verbose_name_plural = "Sections"

#     def __str__(self):
#         return "%s %s" % (self.assessment.name, self.name)


# class Page(models.Model):
#     TEXT = 1
#     MULTIPLE_CHOICES = 2
#     VIDEO = 3
#     IMAGE_SLIDES = 4
#     TEXT_WITH_IMAGE = 5
#     DOCUMENT_VIEWER = 6
#     ALL_IN = 7
#     TRUE_OR_FALSE = 8
#     MULTIPLE_ANSWERS = 9
#     ENUMERATION = 10
#     CERTIFICATE = 11
#     TEXT_AND_AUDIO = 12

#     PAGE_TYPE = [
#         (TEXT, 'Text'),
#         (MULTIPLE_CHOICES, 'Multiple choices'),
#         (TRUE_OR_FALSE, 'True or False'),
#         (MULTIPLE_ANSWERS, 'Multiple Answers'),
#         (ENUMERATION, 'Enumeration'),
#         (VIDEO, 'Video'),
#         (IMAGE_SLIDES, 'Image slides'),
#         (TEXT_WITH_IMAGE, 'Text with image'),
#         (DOCUMENT_VIEWER, 'Document viewer'),
#         (CERTIFICATE, 'Certificate'),
#         (ALL_IN, 'All in'),
#         (TEXT_AND_AUDIO, 'Text and audio'),
#     ]
#     section = models.ForeignKey(
#         Section,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     name = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     title = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     embed = models.BooleanField(default=False)
#     description = models.TextField(null=True, blank=True)
#     description1 = RichTextField(null=True, blank=True)
#     page_no = models.IntegerField(
#         null=True,
#         blank=True
#     )
#     page_type = models.IntegerField(choices=PAGE_TYPE, default=TEXT)
#     text = RichTextField(null=True, blank=True)
#     text2 = models.TextField(null=True, blank=True)
#     file = models.FileField(upload_to='page', null=True, blank=True)
#     timed = models.BooleanField(default=True)
#     link = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     file_type = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     file_name = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     time_limit = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     sequence = models.IntegerField(
#         null=True,
#         blank=True
#     )
#     video = models.FileField(upload_to='page', null=True, blank=True)

#     class Meta:
#         verbose_name = "Page"
#         verbose_name_plural = "Pages"

#     def __str__(self):
#         return "%s %s %s" % (
#             self.section.assessment.name,
#             self.section.name,
#             self.name
#         )


# class EmployeeAssessment(models.Model):
#     employee = models.ForeignKey(
#         Employee,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     assessment = models.ForeignKey(
#         Assessment,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     invited_at = models.DateTimeField(
#         auto_now_add=True,
#         db_index=True
#     )
#     invited_by = models.ForeignKey(
#         User,
#         related_name='exam_created_by',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     started = models.DateTimeField(
#         auto_now=False,
#         null=True,
#         blank=True,
#         default=None,
#         db_index=True
#     )
#     expired_at = models.DateTimeField(
#         null=True,
#         blank=True,
#         db_index=True
#     )
#     current_progress = models.IntegerField(
#         default=0
#     )
#     book_mark = models.ForeignKey(
#         'EmployeePage',
#         related_name='book_mark',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     reference_number = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     certificate_number = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     deleted = models.BooleanField(default=True)
#     completed = models.DateTimeField(
#         auto_now=False,
#         null=True,
#         blank=True,
#         default=None,
#         db_index=True
#     )

#     class Meta:
#         verbose_name = "Employee Assessment"
#         verbose_name_plural = "Employee Assessment"

#     def __str__(self):
#         return "%s %s %s" % (
#             self.employee.user.id,
#             self.employee.user.first_name,
#             self.assessment.name
#         )


# class EmployeeSection(models.Model):
#     employee_assessment = models.ForeignKey(
#         EmployeeAssessment,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     section = models.ForeignKey(
#         Section,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     current_progress = models.IntegerField(
#         default=0
#     )

#     completed = models.DateTimeField(
#         auto_now=False,
#         null=True,
#         blank=True,
#         default=None,
#         db_index=True
#     )

#     class Meta:
#         verbose_name = "Employee Section"
#         verbose_name_plural = "Employee Section"

#     def __str__(self):
#         return "%s %s %s %s" % (
#             self.employee_assessment,
#             self.section.name,
#             self.employee_assessment.employee.user.first_name,
#             self.employee_assessment.employee.user.last_name,
#         )


# class EmployeePage(models.Model):
#     employee_section = models.ForeignKey(
#         EmployeeSection,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     page = models.ForeignKey(
#         Page,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     current_progress = models.IntegerField(
#         default=0
#     )

#     completed = models.DateTimeField(
#         auto_now=False,
#         null=True,
#         blank=True,
#         default=None,
#         db_index=True
#     )
#     score = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )

#     class Meta:
#         verbose_name = "Employee Page"
#         verbose_name_plural = "Employee page"

#     def __str__(self):
#         return "%s %s %s" % (
#             self.page.name,
#             self.employee_section.employee_assessment.employee.user.first_name,
#             self.employee_section.employee_assessment.employee.user.last_name
#         )


# class Score(models.Model):
#     employee_page = models.ForeignKey(
#         EmployeePage,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     score = models.IntegerField(
#         null=True,
#         blank=True,
#         default=0
#     )
#     average_time = models.FloatField(
#         null=False,
#         blank=False,
#         default=0
#     )
#
#     class Meta:
#         verbose_name = "Score"
#         verbose_name_plural = "Scores"


# class Question(models.Model):
#     page = models.ForeignKey(
#         Page,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     text = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     image = models.ImageField(
#         upload_to="profile",
#         null=True,
#         blank=True,
#         default=None
#     )
#     sequence = models.IntegerField(
#         null=True,
#         blank=True
#     )

#     class Meta:
#         verbose_name = "Question"
#         verbose_name_plural = "Questions"

#     def __str__(self):
#         return "%s" % self.text


# class Choice(models.Model):
#     text = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     image = models.ImageField(
#         upload_to="profile",
#         null=True,
#         blank=True,
#         default=None
#     )

#     class Meta:
#         verbose_name = "Choice"
#         verbose_name_plural = "Choices"

#     def __str__(self):
#         return "%s" % self.text


# class QuestionChoice(models.Model):
#     question = models.ForeignKey(
#         Question,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     choice = models.ForeignKey(
#         Choice,
#         on_delete=models.SET_NULL,
#         db_index=True,
#         null=True,
#         blank=True
#     )
#     value = models.IntegerField(
#         null=True,
#         blank=True,
#         default=None
#     )
#     correct_answer = models.BooleanField(default=False)
#     sequence = models.IntegerField(
#         null=True,
#         blank=True
#     )

#     class Meta:
#         verbose_name = "Question choice"
#         verbose_name_plural = "Question choices"


# # class Answer(models.Model):
# #     employee = models.ForeignKey(
# #         Employee,
# #         on_delete=models.SET_NULL,
# #         db_index=True,
# #         null=True,
# #         blank=True
# #     )
# #     question_choice = models.ForeignKey(
# #         QuestionChoice,
# #         on_delete=models.SET_NULL,
# #         db_index=True,
# #         null=True,
# #         blank=True
# #     )
# #     time_consume = models.FloatField(
# #         null=False,
# #         blank=False,
# #         default=0
# #     )
# #
# #     class Meta:
# #         verbose_name = "Answer"
# #         verbose_name_plural = "Answers"

# class Badge(models.Model):
#     title = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True
#     )
#     description = models.TextField(
#         null=True,
#         blank=True
#     )
#     image1 = models.ImageField(
#         upload_to="badge_logo",
#         null=True,
#         blank=True,
#         default=None
#     )
#     image2 = models.ImageField(
#         upload_to="badge_logo",
#         null=True,
#         blank=True,
#         default=None
#     )

#     class Meta:
#         verbose_name = 'Badge'
#         verbose_name_plural = 'Badges'

#     def __str__(self):
#         return "%s" % self.title


# class AssessmentBadge(models.Model):
#     assessment = models.ForeignKey(
#         Assessment,
#         on_delete=models.CASCADE
#     )
#     badge = models.ForeignKey(
#         Badge,
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         verbose_name = 'Assessment Badge'
#         verbose_name_plural = 'Assessment Badges'

#     def __str__(self):
#         return "%s %s" % (
#             self.badge.title,
#             self.assessment.name
#         )


# class EmployeeBadge(models.Model):
#     employee = models.ForeignKey(
#         Employee,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     badge = models.ForeignKey(
#         Badge,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     completed = models.DateTimeField(
#         auto_now=False,
#         null=True,
#         blank=True,
#         default=None,
#         db_index=True
#     )

#     class Meta:
#         verbose_name = 'Employee Badge'
#         verbose_name_plural = 'Employee Badges'

#     def __str__(self):
#         return "%s %s %s" % (
#             self.badge.title,
#             self.employee.user.first_name,
#             self.employee.user.last_name
#         )
