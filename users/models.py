import datetime
import re

from django.db import models

from library.models import Library


# there are 2 types of users: patrons and librarians
class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    library_card_number = models.CharField(max_length=100)
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, related_name='users')


# there are 2 types of patrons: students and faculties
class Patron(User):

    # # search for the documents using string
    # def search_doc(self, string):
    #     d1 = self.search_doc_author(string)
    #     d2 = self.search_doc_title(string)
    #     d3 = self.search_doc_keywords(string)
    #     d4 = d1 | d2 | d3
    #     return d4.distinct()

    # # search for the documents using string, which is the name of the author
    # def search_doc_author(self, name):
    #     documents = self.user_card.library.documents.filter(authors__name__contains=name).distinct()
    #     return documents

    # # search for the documents using string, which is the title
    # def search_doc_title(self, name):
    #     documents = self.user_card.library.documents.filter(title__contains=name).distinct()
    #     return documents

    # # search for the documents using string, which contains keywords
    # def search_doc_keywords(self, string):
    #     words = re.split('[ ,.+;:]+', string)
    #     documents = self.user_card.library.documents.filter(keywords__word__in=words).distinct()
    #     return documents

    def booking_period(self, document):
        return document.booking_period(self)

    def find_copy(self, document):
        if not document.copies.filter(is_checked_out=False).exists():
            return None
        return document.copies.filter(is_checked_out=False)[0]

    # check out some copy of the document. If it is not possible returns False
    def check_out_doc(self, document):
        copy = self.find_copy(document)
        if copy is None:
            return False
        return copy.check_out(self)

    # return copy of the document to the library. If it is not possible returns False
    def return_doc(self, document):
        if not self.copies.filter(document=document).exists():
            return False
        copy = self.copies.get(document=document)
        copy.is_checked_out = False
        copy.user = None
        copy.save()
        return True

    def has_overdue(self):  # bool
        pass


class Student(Patron):
    pass


class Faculty(Patron):
    pass


class Librarian(User):

    def patrons_docs(self, user, doc):
        for copy in user.copies.all():
            if copy.document == doc:
                print ("{} {}: {}: {}".format(user.first_name, user.second_name, doc.title, copy.number))

    def unchecked_copies(self, doc):
        print("There are {} unchrcked copies of document {} in library.".format(self.library.count_unchecked_copies(doc), doc.title))

    def manage_patron(self):
        pass

    def check_overdue_copy(self):
        pass

    def add_doc(self):
        pass

    def delete_doc(self):
        pass

    def modify_doc(self):
        pass
