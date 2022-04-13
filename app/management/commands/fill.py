from random import randint

from django.core.management.base import BaseCommand
from faker import Faker

from app.models import *

COUNT_THOUSAND_TAG = 11
COUNT_USER = 11000
COUNT_QUESTION = 101000
COUNT_TAG_IN_QUESTION = 5
COUNT_ANSWER = 1001000
COUNT_LIKE_QUESTION = 1000000
COUNT_LIKE_ANSWER = 1000000


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(COUNT_THOUSAND_TAG):
            tag_text = set()
            while len(tag_text) != 999:
                tag_text.add(Faker().word() + str(randint(1000, 2000)) + str(i))
                print(11 - i, ' ', len(tag_text))
            tags = []
            for k in tag_text:
                tags.append(Tag(text=k))
            Tag.objects.bulk_create(tags)

        user = [
            User(
                username=Faker().simple_profile()['username'] + Faker().pystr()[:10],
                email=Faker().email(),
                password=Faker().name()
            )
            for i in range(COUNT_USER)
        ]
        User.objects.bulk_create(user)
        # for i in range(COUNT_USER):
        #     user = User.objects.create(username=Faker().simple_profile()['username'] + Faker().pystr()[:10],
        #                                email=Faker().email(),
        #                                password=Faker().name())
        #     user.profile.nickname = Faker().simple_profile()['username'] + Faker().pystr()[:10]
        #     user.save()
        #     print(i)

        profile = [
            Profile(
                user=User.objects.get(pk=i),
                nickname=Faker().simple_profile()['username'] + Faker().pystr()[:10]
            )
            for i in range(COUNT_USER)
        ]
        Profile.objects.bulk_create(profile)

        tags = [] * COUNT_QUESTION
        for i in range(COUNT_QUESTION):
            for j in range(COUNT_TAG_IN_QUESTION):
                tags[i].append(Tag.objects.get(pk=randint(Tag.objects.first().id, Tag.objects.last().id)))

        question = [
            Question(
                author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                title=Faker().paragraph(nb_sentences=1),
                text=Faker().text,
                date=Faker().date,
                rating=randint(-100, 100),
                tag=tags[i]
            )
            for i in range(COUNT_QUESTION)
        ]
        Question.objects.bulk_create(question)
        # for i in range(COUNT_QUESTION):
        #     question = Question.objects.create(
        #         author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
        #         title=Faker().paragraph(nb_sentences=1),
        #         text=Faker().text,
        #         date=Faker().date,
        #         rating=randint(-100, 100)
        #     )
        #     tags = []
        #     for j in range(COUNT_TAG_IN_QUESTION):
        #         tags.append(Tag.objects.get(pk=randint(Tag.objects.first().id, Tag.objects.last().id)))
        #     question.tag.set(tags)
        #     print(i)

        answer = [
            Answer(
                body=Faker().text,
                author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                date=Faker().date,
                question=Question.objects.get(pk=randint(Question.objects.first().id, Question.objects.last().id)),
                rating=randint(-100, 100),
            )
            for i in range(COUNT_ANSWER)
        ]
        Answer.objects.bulk_create(answer)
        # for i in range(COUNT_ANSWER):
        #     Answer.objects.create(body=Faker().text,
        #                           author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
        #                           date=Faker().date,
        #                           question=Question.objects.get(
        #                               pk=randint(Question.objects.first().id, Question.objects.last().id)),
        #                           rating=randint(-100, 100),
        #                           )
        #     print(i)

        obj_q = [] * COUNT_LIKE_QUESTION
        for i in range(COUNT_LIKE_QUESTION):
            obj_q[i]=Question.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))

        like = [
            Like.objects.create(
                user=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                content_type=ContentType.objects.get_for_model(obj_q),
                rating=1,
                object_id=obj_q[i].id
            )
            for i in range(COUNT_LIKE_QUESTION)
        ]
        Like.objects.bulk_create(like)
        # for i in range(COUNT_LIKE_QUESTION):
        #     obj = Question.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))
        #     Like.objects.create(
        #         user=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
        #         content_type=ContentType.objects.get_for_model(obj),
        #         rating=1,
        #         object_id=obj.id
        #     )
        #     print(i)

        obj_a = [] * COUNT_LIKE_ANSWER
        for i in range(COUNT_LIKE_ANSWER):
            obj_a[i] = Answer.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))

        like = [
            Like.objects.create(
                user=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                content_type=ContentType.objects.get_for_model(obj_a),
                rating=1,
                object_id=obj_a[i].id
            )
            for i in range(COUNT_LIKE_ANSWER)
        ]
        Like.objects.bulk_create(like)
        # for i in range(COUNT_LIKE_ANSWER):
        #     obj = Answer.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))
        #     Like.objects.create(
        #         user=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
        #         content_type=ContentType.objects.get_for_model(obj),
        #         rating=1,
        #         object_id=obj.id
        #     )
        #     print(i)