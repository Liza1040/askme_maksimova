from django.db import models
from django.db.models import Count

class QuestionManager(models.Manager):
    def get_new(self):
        return self.all().order_by('date').reverse()

    def get_hot(self):
        return self.all().order_by('rating').reverse()

    def get_by_id(self, question_id):
        return self.all().filter(id=question_id)

class AnswerManager(models.Manager):
    def get_answer(self, question_id):
        return self.filter(question=question_id).all().order_by('rating').reverse()

    def get_count_answer(self, question_id):
        return self.filter(question=question_id).count

class TagManager(models.Manager):
    def get_by_tag(self, tag_str):
        tag = self.filter(text=tag_str).first().questions.all().order_by('date').reverse()
        if not tag:
            return None
        return tag

    def get_tag(self, tag_str):
        tag = self.filter(text=tag_str).first()
        if not tag:
            return None
        return tag

    def get_top_9(self):
        return self.annotate(tags=Count('questions')).order_by('tags').reverse()[0:9]

class ProfileManager(models.Manager):
    def get_top_10(self):
        return self.all().order_by('rating').reverse()[:10]

class LikeManager(models.Manager):
    def get_like_by_content(self, content, content_id, user):
        return self.filter(object_id=content_id, content_type=content, user=user).first()