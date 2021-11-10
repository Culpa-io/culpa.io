from cureview.models import Course, ReviewableObject, ReviewableCategory, Professor, Review

# courses = ReviewableCategory.objects.get(name='courses')

# for course in Course.objects.all():
#     rvo = ReviewableObject(name=f"[{course.course_identifier}] {course.course_name}", category=courses,
#     relatedCourse=course, image='reviewimages/lecturehall.jpg')
#     rvo.save()


professors = ReviewablepCategory.objects.get(name='professors')
for p in Professor.objects.all():
    rvo = ReviewableObject(name=f"{p.name} ({p.uni})", category=professors,
    relatedProfessor=p, image='reviewimages/man.png')
    rvo.save()