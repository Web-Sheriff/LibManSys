# all the classes there (but not copy) is about documents, not about library system. Copy connects library and documents
from django.db import models

import datetime

from library.models import Library
from users.models import User, Faculty


class Author(models.Model):
    name = models.CharField(max_length=250)


class Keyword(models.Model):
    word = models.CharField(max_length=255)


# there are 3 types of documents: books, journal articles and audio/video files
class Document(models.Model):
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='documents')
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField(Author, related_name='documents')
    price_value = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='documents')

    def booking_period(self, user):
        return datetime.timedelta(weeks=2)


class Book(Document):
    is_best_seller = models.BooleanField(default=False)
    edition = models.IntegerField()
    publisher = models.CharField(max_length=100)
    publish_time = models.DateField()

    def booking_period(self, user):
        if isinstance(user, Faculty):
            return datetime.timedelta(weeks=4)
        elif self.is_best_seller:
            return datetime.timedelta(weeks=2)
        return datetime.timedelta(weeks=3)


class ReferenceBook (Book):
    pass


class AudioVideo(Document):
    pass


class Editor(models.Model):
    first_name = models.CharField(max_length=250)
    second_name = models.CharField(max_length=250)


class Journal(models.Model):
    title = models.CharField(max_length=250)


class Issue(models.Model):
    publication_date = models.DateField()
    editors = models.ManyToManyField(Editor, related_name='issues')
    journal = models.ForeignKey(Journal, on_delete=models.DO_NOTHING, related_name='issues')


class JournalArticles(Document):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING, related_name='journal_articles')


class Copy(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, related_name='copies')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='copies')
    number = models.IntegerField()
    is_checked_out = models.BooleanField(default=False)
    booking_date = models.DateField(null=True)
    overdue_date = models.DateField(null=True)

    def check_out(self, user):
        if isinstance(self.document, ReferenceBook):
            return False
        if self.document.copies.filter(user=user).exists():
            return False
        self.is_checked_out = True
        self.user = user
        self.booking_date = datetime.date.today()
        self.overdue_date = self.booking_date + self.document.booking_period(user)
        self.save()
        return True
