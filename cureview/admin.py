from django.contrib import admin
from cureview.models import Review, ReviewableObject, ReviewableCategory, Professor, Course

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    pass


class ReviewableCategoryAdmin(admin.ModelAdmin):
    pass


class ReviewableObjectAdmin(admin.ModelAdmin):
    pass


class ProfessorAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewableCategory, ReviewableCategoryAdmin)
admin.site.register(ReviewableObject, ReviewableObjectAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Course, CourseAdmin)
