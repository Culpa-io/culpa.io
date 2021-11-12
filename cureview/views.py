from nltk.corpus import stopwords
from nltk import word_tokenize
import re
import nltk
from django.shortcuts import render
from .models import Review, ReviewableObject, ReviewableCategory, Professor, Course
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
import json
import inflect
p = inflect.engine()

# Word cloud
stop_words = stopwords.words('english')

# @login_required


def index(request):
    context = {}
    review_categories = ReviewableCategory.objects.all()
    review_cats_list = []
    reviewable_objects_preview = {}
    for rvc in review_categories:
        relevantROs = ReviewableObject.objects.filter(
            category=rvc).order_by('-numReviews')[:4]
        if len(relevantROs) >= 4:
            review_cats_list.append(rvc.name)
            ro_data = []
            for relevant_ro in relevantROs:
                relevantReviews = Review.objects.filter(
                    target=relevant_ro).filter(approved=True)
                if rvc.name == 'professors':
                    relevantReviews = Review.objects.filter(
                        relatedProfessor=relevant_ro.relatedProfessor).filter(
                        approved=True)
                ro_data_instance = {
                    "name": relevant_ro.title_name,
                    "image_path": relevant_ro.image.url,
                    "id": relevant_ro.id}
                ro_data_instance["total_reviews"] = len(relevantReviews)
                ro_data_instance["total_score"] = 0
                if len(relevantReviews) >= 1:
                    ro_data_instance["total_score"] = round(sum(
                        [*map(lambda x: x.overall_rating, relevantReviews)]) / len(relevantReviews), 3)
                ro_data_instance["rounded_total_score"] = int(
                    round(ro_data_instance["total_score"], 5))

                ro_data_instance["overall_on_stars"] = range(
                    ro_data_instance["rounded_total_score"])
                ro_data_instance["overall_off_stars"] = range(
                    5 - ro_data_instance["rounded_total_score"])

                if len(relevantReviews) == 0:
                    ro_data_instance["total_score"] = "--"
                    ro_data_instance["rounded_total_score"] = "--"

                ro_data.append(ro_data_instance)
            reviewable_objects_preview["-".join(rvc.name.split(' '))] = ro_data

    context["reviewable_categories"] = json.dumps(review_cats_list)
    context["reviewable_objects_preview_max4"] = reviewable_objects_preview

    return render(request, "cureview/index.html", context)

# @login_required


def search(request):
    context = {"categories": [
        *map(lambda x: x.name, ReviewableCategory.objects.all())]}
    return render(request, "cureview/search.html", context)

# @login_required


def reviews(request, category, id):
    context = {}
    categorySearch = ' '.join(category.lower().split('-'))
    categoryQuery = ReviewableCategory.objects.filter(name=categorySearch)
    if len(categoryQuery) == 0:
        return HttpResponseRedirect('/search')

    targetQuery = ReviewableObject.objects.filter(
        category=categoryQuery[0]).filter(pk=id)
    if not targetQuery:
        return HttpResponseRedirect('/search')

    target = targetQuery[0]

    context["metadata"] = {
        "name": target.title_name,
        "category": categorySearch.title(),
        "image_url": target.image.url,
        "targetid": target.id,
        "has_meta": categorySearch in [
            'professors',
            'courses'],
        "meta_category": 'professors' if categorySearch == 'courses' else 'courses',
        "all_words": []}

    if not context['metadata']['has_meta']:
        context['metadata']['meta_category'] = context['metadata']['category']

    relevantReviews = Review.objects.filter(
        target=target).filter(approved=True)
    if categorySearch == 'professors':
        relevantReviews = Review.objects.filter(
            relatedProfessor=target.relatedProfessor).filter(
            approved=True)

    reviewData = []
    for review in relevantReviews.order_by('-date'):
        meta = None
        meta_url = None

        if categorySearch in ['professors', 'courses']:
            meta = review.relatedProfessor.name if categorySearch == 'courses' else review.target.relatedCourse.course_name
            if categorySearch == 'courses':
                meta_url = '/reviews/professors/' + \
                    str(ReviewableObject.objects.get(relatedProfessor=review.relatedProfessor).id)
            else:
                meta_url = '/reviews/courses/' + str(review.target.id)
        if categorySearch in ['professors', 'courses']:
            for word in nltk.pos_tag(word_tokenize(review.contents)):
                if not word[0].lower() in stop_words and word[1] in [
                        'JJ'] and re.match('^\\w+$', word[0]):
                    context['metadata']['all_words'].append(word[0])
        else:
            context['metadata']['all_words'].append(review.title)
        reviewData.append({"title": review.title,
                           "contents": review.contents,
                           "on_stars": range(review.overall_rating),
                           "off_stars": range(5 - review.overall_rating),
                           "date": review.date,
                           "meta": meta,
                           "meta_url": meta_url})
    context["reviewdata"] = reviewData

    context["top_reviews"] = False
    context["top_review_data"] = []
    if len(reviewData) >= 2:
        context["top_reviews"] = True
        scoreStratified = relevantReviews.order_by('-overall_rating')

        posReview = scoreStratified[0]
        meta_url = None
        meta = None

        if categorySearch in ['professors', 'courses']:
            meta = posReview.relatedProfessor.name.split(
                ' ')[-1] if categorySearch == 'courses' else posReview.target.relatedCourse.course_identifier
            if categorySearch == 'courses':
                meta_url = '/reviews/professors/' + \
                    str(ReviewableObject.objects.get(relatedProfessor=posReview.relatedProfessor).id)
            else:
                meta_url = '/reviews/courses/' + str(posReview.target.id)
        context["top_review_data"].append({"title": posReview.title,
                                           "contents": posReview.contents[:150],
                                           "on_stars": range(posReview.overall_rating),
                                           "off_stars": range(5 - posReview.overall_rating),
                                           "date": posReview.date,
                                           "meta": meta,
                                           "meta_url": meta_url})

        negReview = scoreStratified.reverse().filter(~Q(pk=posReview.id))[0]
        meta_url = None
        meta = None
        if categorySearch in ['professors', 'courses']:
            meta = negReview.relatedProfessor.name.split(
                ' ')[-1] if categorySearch == 'courses' else negReview.target.relatedCourse.course_identifier
            if categorySearch == 'courses':
                meta_url = '/reviews/professors/' + \
                    str(ReviewableObject.objects.get(relatedProfessor=negReview.relatedProfessor).id)
            else:
                meta_url = '/reviews/courses/' + str(negReview.target.id)

        context["top_review_data"].append({"title": negReview.title,
                                           "contents": negReview.contents[:150],
                                           "on_stars": range(negReview.overall_rating),
                                           "off_stars": range(5 - negReview.overall_rating),
                                           "date": negReview.date,
                                           "meta": meta,
                                           "meta_url": meta_url})

    context["total_reviews"] = len(relevantReviews)
    context["total_score"] = 0
    if len(relevantReviews) >= 1:
        context["total_score"] = round(sum(
            [*map(lambda x: x.overall_rating, relevantReviews)]) / len(relevantReviews), 3)
    context["rounded_total_score"] = int(round(context["total_score"], 5))

    context["overall_on_stars"] = range(context["rounded_total_score"])
    context["overall_off_stars"] = range(5 - context["rounded_total_score"])

    if len(relevantReviews) == 0:
        context["total_score"] = "--"
        context["rounded_total_score"] = "--"

    suggestedROs = None
    if not context['metadata']['has_meta']:
        suggestedROs = ReviewableObject.objects.filter(
            category__name=categorySearch).order_by('-numReviews')[:5]
    else:
        if categorySearch == 'professors':
            suggestedROs = ReviewableObject.objects.filter(
                relatedCourse__professors=target.relatedProfessor).order_by('-numReviews')[:20]
        elif categorySearch == 'courses':
            suggestedROs = []
            for p in target.relatedCourse.professors.all()[:20]:
                suggestedROs.append(
                    ReviewableObject.objects.get(
                        relatedProfessor=p))

    context['suggestedROs'] = []
    for relevant_ro in suggestedROs:
        relevantReviews = Review.objects.filter(
            target=relevant_ro).filter(
            approved=True)
        if categorySearch == 'courses':
            relevantReviews = Review.objects.filter(
                relatedProfessor=relevant_ro.relatedProfessor).filter(
                approved=True)
        ro_data_instance = {
            "name": relevant_ro.title_name,
            "image_url": relevant_ro.image.url,
            "id": relevant_ro.id}
        ro_data_instance["total_reviews"] = len(relevantReviews)
        ro_data_instance["total_score"] = 0
        if len(relevantReviews) >= 1:
            ro_data_instance["total_score"] = round(sum(
                [*map(lambda x: x.overall_rating, relevantReviews)]) / len(relevantReviews), 1)

        ro_data_instance["rounded_total_score"] = int(
            round(ro_data_instance["total_score"], 5))

        ro_data_instance["overall_on_stars"] = list(
            range(ro_data_instance["rounded_total_score"]))
        ro_data_instance["overall_off_stars"] = list(
            range(5 - ro_data_instance["rounded_total_score"]))
        context['suggestedROs'].append(ro_data_instance)

    return render(request, "cureview/reviews.html", context)

# @login_required


def compose(request):
    context = {}
    return render(request, "cureview/compose.html", context)

# @login_required


def searchOpt(request):
    query = request.GET.get('query')
    searchResult = []
    allROS = list(ReviewableObject.objects.filter(
        name__icontains=query).order_by('-numReviews')[:5])
    for ipn in ReviewableObject.objects.filter(
            name__trigram_similar=query).order_by('-numReviews')[:5]:
        if ipn not in allROS:
            allROS.append(ipn)
    for item in allROS:
        itemData = {
            "name": item.title_name,
            "id": item.id,
            "category": item.category.name}
        searchResult.append(itemData)
    return JsonResponse(searchResult, safe=False)

# @login_required


def compare(request):
    return render(request, "cureview/compare.html", {})

# @login_required


def getrodata(request):
    obj_id = request.GET.get("id")
    ro = ReviewableObject.objects.get(pk=obj_id)
    reviewCount = len(Review.objects.filter(target=ro))

    category_name = ro.category.name
    singular = p.singular_noun(category_name)
    if singular:
        category_name = singular

    itemProfessors = []
    if ro.relatedCourse is not None:
        for professor in ro.relatedCourse.professors.all():
            itemProfessors.append(
                {'name': professor.name, 'uni': professor.uni})

    itemCourses = []
    if ro.relatedProfessor is not None:
        for course in Course.objects.filter(professors=ro.relatedProfessor):
            itemCourses.append(
                {
                    'name': f"[{course.course_identifier}] {course.course_name.title()}",
                    'roid': ReviewableObject.objects.get(
                        relatedCourse=course).id})

    return JsonResponse({"name": ro.title_name,
                         "image_url": ro.image.url,
                         "num_reviews": reviewCount,
                         "category_name": category_name,
                         "professors": itemProfessors,
                         "courses": itemCourses})

# @login_required


def submitreview(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        ro = ReviewableObject.objects.get(pk=body['target_id'])
        relatedProfessor = None
        if body['category'] == 'course':
            relatedProfessor = Professor.objects.get(uni=body['metadata'])
        elif body['category'] == 'professor':
            relatedProfessor = ro.relatedProfessor
            # you can't directly review a professor, so we convert this to a
            # review about the class with the professor
            ro = ReviewableObject.objects.get(pk=body['metadata'])
        rv = Review(
            title=body['title'],
            contents=body['review'],
            overall_rating=body['rating'],
            target=ro,
            date=datetime.now(),
            relatedProfessor=relatedProfessor)
        rv.save()
        return JsonResponse({"success": True})
    except Exception as e:
        print(str(e))
        return JsonResponse({"success": False})

# @login_required


def coreDataQuery(request):
    query = request.GET.get('query')
    core_data = {}
    for category in ReviewableCategory.objects.all():
        reviewableObjectsData = {}
        shouldPush = False

        workingSet = ReviewableObject.objects.filter(category=category)
        if query:
            workingSet = list(ReviewableObject.objects.filter(category=category).filter(
                name__icontains=query).order_by('-numReviews')[:10])
            for item in ReviewableObject.objects.filter(category=category).filter(
                    name__trigram_similar=query).order_by('-numReviews')[:10]:
                if item not in workingSet:
                    workingSet.append(item)

        # workingSet = workingSet.order_by('-numReviews')

        for relevant_ro in workingSet[:10]:
            shouldPush = True
            relevantReviews = Review.objects.filter(
                target=relevant_ro).filter(approved=True)
            if category.name == 'professors':
                relevantReviews = Review.objects.filter(
                    relatedProfessor=relevant_ro.relatedProfessor).filter(
                    approved=True)
            ro_data_instance = {
                "name": relevant_ro.title_name,
                "image_url": relevant_ro.image.url,
                "id": relevant_ro.id}
            ro_data_instance["total_reviews"] = len(relevantReviews)
            ro_data_instance["total_score"] = 0
            if len(relevantReviews) >= 1:
                ro_data_instance["total_score"] = round(sum(
                    [*map(lambda x: x.overall_rating, relevantReviews)]) / len(relevantReviews), 1)

            ro_data_instance["rounded_total_score"] = int(
                round(ro_data_instance["total_score"], 5))

            ro_data_instance["overall_on_stars"] = list(
                range(ro_data_instance["rounded_total_score"]))
            ro_data_instance["overall_off_stars"] = list(
                range(5 - ro_data_instance["rounded_total_score"]))

            if len(relevantReviews) == 0:
                ro_data_instance["total_score"] = "—"
                ro_data_instance["rounded_total_score"] = "—"
            reviewableObjectsData[relevant_ro.title_name] = ro_data_instance
        if shouldPush:
            core_data[category.name.title()] = reviewableObjectsData

    return JsonResponse({"core_data": core_data, "query": query}, safe=False)
