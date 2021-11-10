# Run this file with: 
# python3 manage.py shell
# exec(open('cureview/syncdata.py').read())


import requests
import re 
import json, sys, copy

from cureview.models import Professor, Course, ReviewableCategory, ReviewableObject


courses = ReviewableCategory.objects.get(name='courses')
professors = ReviewableCategory.objects.get(name='professors')

departments = json.loads(requests.get("https://vergil.registrar.columbia.edu/feeds/filters.js").text)['filters']['departments']

def processCourse(course):
    data = {
        'course_identifier': course["course_identifier"],
        'subject_long_name': course["subject"]["long_name"],
        'course_number': course["number"],
        'department_name': course["department"]["name"],
        'term': course["term"],
        'course_name': course["course_name"]
    }

    # Make sure course doesnt exist already
    course_exists = Course.objects.filter(course_identifier=data['course_identifier']).filter(course_number=data['course_number']).filter(course_name=data['course_name']).first()

    if not course_exists:
        print(f"Course {data['course_identifier']} does not exist. Creating...")
        course_exists = Course(**data)
        course_exists.save()

        rvo = ReviewableObject(name=f"[{course_exists.course_identifier}] {course_exists.course_name}", category=courses,
        relatedCourse=course_exists, image='reviewimages/lecturehall.jpg')
        rvo.save()
        print(f"Created Reviewable Interface for {rvo.name}")
    else:
        print(f"Course {data['course_identifier']} already exists.")


    for cu_class in course["classes"]['class']:
        instructors = cu_class["instructors"]
        for instr in instructors:
            instructor_data = {
                "name": instr["name"],
                "uni": instr["uni"],
            }

            # Make sure they don't exist already
            professor_exists = Professor.objects.filter(uni=instructor_data["uni"]).first()
            if not professor_exists:
                print(f"Professor {instructor_data['uni']} does not exist. Creating...")
                professor_exists = Professor(**instructor_data)
                professor_exists.save()

                rvo = ReviewableObject(name=f"{professor_exists.name} ({professor_exists.uni})", category=professors,
                relatedProfessor=professor_exists, image='reviewimages/man.png')
                rvo.save()
                print(f"Created Reviewable Interface for {rvo.name}")
            else: 
                print(f"Professor {instructor_data['uni']} already exists.")
        
            course_exists.professors.add(professor_exists)

def landInDB(all_data):
    for data in all_data: # all_data is an array of all the courses
        course = data["course"]
        
        course_name = None 
        if 'course_name' in course:
            course_name = course['course_name']

        # we need to determine the naming scheme
        all_section_names = []
        for section in course["classes"]["class"]:
            all_section_names.append(re.sub('(TPC|tpc|topic|TOPIC|Topic)\s*:\s*', '', section['subtitle']))


        if course_name and ('topics' in course_name.lower() or 'physical education activities' in course_name.lower()) and not (all_section_names[0].lower() in course_name.lower() and len(all_section_names) == 0):
            print(all_section_names)
            print("Processing Complex Section Class")
            for section in course["classes"]["class"]:
                section_course_name = f"{course_name+': ' if course_name else ''}{section['subtitle']}"
                section_course_instructors = section['instructors']

                courseCopy = copy.deepcopy(course)

                courseCopy['course_name'] = section_course_name
                courseCopy['classes'] = {
                    'class': [{
                        "instructors": section_course_instructors
                    }]
                }
                
                processCourse(courseCopy)

        elif not course_name: # Case 2, no course name but all sections are the same
            course['course_name'] = all_section_names[0]
            processCourse(course)

        else: # Basic class
            processCourse(course)




# USAGE

# Departments 2021 fall 

# for dept in departments:
#     DEPT_KEY = dept['value']
#     r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?dept={DEPT_KEY}&key=*&moreresults=2&term=20213")
#     data = json.loads(r.text[6:])
#     landInDB(data)

# Departments 2020 fall

# for dept in departments:
#     DEPT_KEY = dept['value']
    # r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?dept={DEPT_KEY}&key=*&moreresults=2&term=20203")
    # data = json.loads(r.text[6:])
    # landInDB(data)
 
# Departments 2021 spring

# for dept in departments:
#     DEPT_KEY = dept['value']
#     r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?dept={DEPT_KEY}&key=*&moreresults=2&term=20211")
#     data = json.loads(r.text[6:])
#     landInDB(data)

# Departments 2020 spring

# for dept in departments:
#     DEPT_KEY = dept['value']
#     r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?dept={DEPT_KEY}&key=*&moreresults=2&term=20201")
#     data = json.loads(r.text[6:])
#     landInDB(data)

# Humanities 2021 fall 

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20213&subject=HUMA")
# data = json.loads(r.text[6:])
# landInDB(data)


# Humanities 2021 spring 

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20211&subject=HUMA")
# data = json.loads(r.text[6:])
# landInDB(data)

# Humanities 2020 fall

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20203&subject=HUMA")
# data = json.loads(r.text[6:])
# landInDB(data)

# English 2021 fall

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20213&subject=ENGL")
# data = json.loads(r.text[6:])
# landInDB(data),

# English 2021 spring

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20211&subject=ENGL")
# data = json.loads(r.text[6:])
# landInDB(data)

# English 2020 fall 

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20203&subject=ENGL")
# data = json.loads(r.text[6:])
# landInDB(data)

# English 2020 spring 

# r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=*&moreresults=2&term=20201&subject=ENGL")
# data = json.loads(r.text[6:])
# landInDB(data)

r = requests.get(f"https://vergil.registrar.columbia.edu/doc-adv-queries.php?key=CONTEMP+WESTERN+CIVILIZATION+I&moreresults=2&term=20203")
data = json.loads(r.text[6:])
landInDB(data)
