from django.db import models

class Candidates(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Questions(models.Model):
    description = models.CharField(max_length=500)
    # question_type = models.CharField(max_length=10)

    def __str__(self):
        return self.description

class Answers(models.Model):
    candidate = models.ForeignKey(Candidates)
    question = models.ForeignKey(Questions)
    answer = models.IntegerField()

    def __str__(self):
        return u'%s R: %s' % (self.question, self.answer)
