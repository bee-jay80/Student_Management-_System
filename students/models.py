from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import StudentsManager
# cloudinary
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage, uploader




class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, unique=True)
    course_image = models.ImageField(upload_to="courses/images/",default="courses/images/default.jpg")
    course_duration = models.CharField(max_length=100)
    course_fees = models.CharField(max_length=100)
    course_description = models.TextField()
    number_of_months = models.IntegerField()

    def __str__(self):
        return self.course_name


class Student(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255,unique=True,verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Middle Name"))
    current_month = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Current Month"))
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    primary_phone = models.CharField(max_length=20, blank=True, null=True)
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Joined"))
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    courses = models.ManyToManyField(Courses, related_name="students")
    learning_duration = models.IntegerField(blank=True, null=True)
    learning_center = models.CharField(max_length=100)



    objects = StudentsManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["-date_joined"]

   

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()


class ProfileImage(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="profile_image")
    image = CloudinaryField("image", default="default_profile.png")
    image_url = models.URLField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        if self.pk:
            # Retrieve the existing instance to check for changes
            existing_instance = ProfileImage.objects.get(pk=self.pk)
            # If the image has been updated, delete the old image from Cloudinary
            if existing_instance.image != self.image and existing_instance.image.public_id != "default_profile.png":
                uploader.destroy(existing_instance.image.public_id)

        # Save the model instance to ensure the image is uploaded to Cloudinary
        super().save(*args, **kwargs)

        # If an image is uploaded, retrieve its URL from Cloudinary
        if self.image:
            # Use Cloudinary's API to get the secure URL of the uploaded image
            cloudinary_image = CloudinaryImage(self.image.public_id)
            self.image_url = cloudinary_image.build_url(secure=True)

            # Save the updated model instance with the image URL
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary if it is not the default image
        if self.image and self.image.public_id != "default_profile.png":
            uploader.destroy(self.image.public_id)

        # Call the parent delete method to remove the instance from the database
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} Profile Image"