import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.db.models import Q


class Professor(models.Model):
    name = models.CharField(max_length=100)
    uni = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_identifier = models.CharField(max_length=40)  # ECONBC3061
    subject_long_name = models.CharField(max_length=200)  # Economics
    course_number = models.CharField(max_length=50)  # 3061
    department_name = models.CharField(
        max_length=200)  # Economics (barnard) (ECOB)
    term = models.CharField(max_length=50)  # 20213 -> Fall 2021
    course_name = models.CharField(max_length=500)  # SENIOR THESIS I
    professors = models.ManyToManyField(Professor)

    def __str__(self):
        return self.course_identifier


class ReviewableCategory(models.Model):
    name = models.CharField(max_length=500)
    # Everything except professors is directly reviewable
    directly_reviewable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ReviewableObject(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='reviewimages')  # base64, temp

    # What category does this belong to? Courses? Dorms?
    category = models.ForeignKey(ReviewableCategory, on_delete=models.CASCADE)

    relatedCourse = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True)
    relatedProfessor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True)

    numReviews = models.PositiveIntegerField(default=0)

    @property
    def title_name(self):
        if self.relatedCourse:
            return self.name.title()
        else:
            return self.name

    def __str__(self):
        return self.name


class Review(models.Model):
    # Review data
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    contents = models.TextField()
    overall_rating = models.PositiveIntegerField(
        default=None, null=True, validators=[
            MinValueValidator(1), MaxValueValidator(5)])

    # What is this review about?
    target = models.ForeignKey(
        ReviewableObject,
        on_delete=models.CASCADE,
        null=True)

    # Is it approved yet?
    approved = models.BooleanField(default=False)

    # Optional Professor link
    relatedProfessor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Review)
def update_num_reviews(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        if instance.approved:
            instance.target.numReviews += 1
            instance.target.save()

            if instance.relatedProfessor:
                ro_prof = ReviewableObject.objects.get(
                    relatedProfessor=instance.relatedProfessor)
                ro_prof.numReviews += 1
                ro_prof.save()

    else:
        if not obj.approved == instance.approved:  # Field has changed
            if instance.approved:
                instance.target.numReviews += 1
                instance.target.save()

                if instance.relatedProfessor:
                    ro_prof = ReviewableObject.objects.get(
                        relatedProfessor=instance.relatedProfessor)
                    ro_prof.numReviews += 1
                    ro_prof.save()

                if instance.target.category.name == 'courses':
                    instance.target.relatedCourse.professors.add(
                        instance.relatedProfessor)

            elif not instance.approved:
                instance.target.numReviews -= 1
                instance.target.save()

                if instance.relatedProfessor:
                    ro_prof = ReviewableObject.objects.get(
                        relatedProfessor=instance.relatedProfessor)
                    ro_prof.numReviews -= 1
                    ro_prof.save()

                if instance.target.category.name == 'courses' and not Review.objects.filter(target=instance.target).filter(relatedProfessor=instance.relatedProfessor).filter(~Q(id=instance.pk)):
                    instance.target.relatedCourse.professors.remove(
                        instance.relatedProfessor)


@receiver(pre_delete, sender=Review)
def update_num_reviews_on_delete(sender, instance, **kwags):
    if instance.approved:
        instance.target.numReviews -= 1
        instance.target.save()

        if instance.relatedProfessor:
            ro_prof = ReviewableObject.objects.get(
                relatedProfessor=instance.relatedProfessor)
            ro_prof.numReviews -= 1
            ro_prof.save()
