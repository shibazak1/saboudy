import csv

from many.models import person, course , membership


def run():

    fhand = open()
    reader = csv.reader(fhand)

    person.objects.all().delete()
    course.objects.all().delete()


    for line in reader:

        print(line)

        p ,create  = person.get_or_create(email=line[0])
        c , create = course.get_or_create(title=line[2])

        r = membership.LEARNER

        if line[1] = 'I': r = membership.INSTRUCTER
        m = membership(person=p,course=c,role=r)
        m.save()

        
