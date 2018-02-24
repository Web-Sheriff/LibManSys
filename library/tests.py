import datetime

from django.test import TestCase

from library.models import *
from users.models import *
from documents.models import *


def create_library():
	return Library.objects.create()

def create_user(class_model, library, num):
	return class_model.objects.create(login='test',
		password='test', first_name='test',
		second_name='test', address='test',
		phone_number='test', library_card_number=num,
		library=library)

def create_book(library, is_best_seller=False, reference=False, title='"Good_book"'):
	class_model = ReferenceBook if reference else Book
	return class_model.objects.create(library=library,
		title=title, price_value=0, is_best_seller=is_best_seller,
		edition=0, publisher='test', publish_time=datetime.date.today())

def create_copy(document,  number):
	Copy.objects.create(document=document, number=number)

def create_author():
	return Author.objects.create(name='Beautifull_author')


class FirstTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Patron, lib, 0)
		create_user(Librarian, lib, 1)
		book = create_book(lib)
		create_copy(book, 0)
		create_copy(book, 1)

	def test_case(self):
		print ("TEST 1")
		patron = Patron.objects.get()
		book = Book.objects.get()
		lib = Library.objects.get()
		if patron.check_out_doc(book):
			print("patron checked out the book "+ book.title)
		else:
			print("patron can't check out the book "+book.title)
		print("patron has "+ str(len(Copy.objects.filter(document=book, is_checked_out=True, user=patron)))+' copies of the book "'+book.title +'"')
		print("library has " + str(lib.count_unchecked_copies(book))+' unchecked copies of the book "'+book.title )




class SecondTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Patron, lib, 0)
		create_user(Librarian, lib, 1)
		create_author()

	def test_case(self):
		print ("TEST 2")
		patron = Patron.objects.get()
		author = Author.objects.get()
		if Document.objects.filter(authors=author).exists():
			print ("library has books of author "+author.name)
		else:
			print ("library has no books of author "+author.name)


class ThirdTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Faculty, lib, 0)
		create_user(Student, lib, 1)
		create_user(Librarian, lib, 2)
		book = create_book(lib)
		create_copy(book, 0)

	def test_case(self):
		print ("TEST 3")
		faculty = Faculty.objects.get()
		book = Book.objects.get()
		if faculty.check_out_doc(book):
			print("faculty checked out the book successfully")
		else:
			print("faculty didn't check out the book")
		copy = Copy.objects.get()
		print ("returning time is: "+str((copy.overdue_date - copy.booking_date).days)+" days")


class FourthTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Faculty, lib, 0)
		create_user(Student, lib, 1)
		create_user(Librarian, lib, 2)
		book = create_book(lib, is_best_seller=True)
		create_copy(book, 0)

	def test_case(self):
		print ("TEST 4")
		faculty = Faculty.objects.get()
		book = Book.objects.get()
		if faculty.check_out_doc(book):
			print("faculty checks out the book successfully")
		else:
			print("faculty didn't check out the book")
		copy = Copy.objects.get()
		print ("returning time is: "+str((copy.overdue_date - copy.booking_date).days)+" days")


class FifthTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Patron, lib, 0)
		create_user(Patron, lib, 1)
		create_user(Patron, lib, 2)
		create_user(Librarian, lib, 3)
		book = create_book(lib)
		create_copy(book, 0)
		create_copy(book, 1)

	def test_case(self):
		print ("TEST 5")
		patron1, patron2, patron3 = Patron.objects.all()
		book = Book.objects.get()
		if patron1.check_out_doc(book):
			print ("patron #" + str(patron1.library_card_number) + " checks out the book " + book.title )
		else:
			print ("patron #" + str(patron1.library_card_number) + " can't check out the book " + book.title )

		if patron2.check_out_doc(book):
			print ("patron #" + str(patron2.library_card_number) + " checks out the book " + book.title )
		else:
			print ("patron #" + str(patron2.library_card_number) + " can't check out the book " + book.title )

		if patron3.check_out_doc(book):
			print ("patron #" + str(patron3.library_card_number) + " checks out the book " + book.title )
		else:
			print ("patron #" + str(patron3.library_card_number) + " can't check out the book " + book.title )


class SixthTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Patron, lib, 0)
		create_user(Librarian, lib, 1)
		book = create_book(lib)
		create_copy(book, 0)
		create_copy(book, 1)

	def test_case(self):
		print("TEST 6")
		patron = Patron.objects.get()
		book = Book.objects.get()
		print ("patron tries to check out the book "+ book.title)
		if patron.check_out_doc(book):
			print ("patron checks out the book " + book.title )
		else:
			print ("patron can't check out the book " + book.title )

		print ("patron tries to check out the book "+ book.title)
		if patron.check_out_doc(book):
			print ("patron checks out the book " + book.title )
		else:
			print ("patron can't check out the book " + book.title )


class SeventhTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Patron, lib, 0)
		create_user(Patron, lib, 1)
		create_user(Librarian, lib, 2)
		book = create_book(lib)
		create_copy(book, 0)
		create_copy(book, 1)

	def test_case(self):
		print ("TEST 7")
		patron1, patron2 = Patron.objects.all()
		book = Book.objects.get()
		patron1.check_out_doc(book)
		patron2.check_out_doc(book)

		if Copy.objects.filter(document=book, is_checked_out=True, user=patron1).exists():
			print ("Patron # "+ str(patron1.library_card_number)+" has copy of the book "+book.title)
		else:		
			print ("Patron # "+ str(patron1.library_card_number)+" hasn't copy of the book "+book.title)

		if Copy.objects.filter(document=book, is_checked_out=True, user=patron2).exists():
			print ("Patron # "+ str(patron2.library_card_number)+" has copy of the book "+book.title)
		else:		
			print ("Patron # "+ str(patron2.library_card_number)+" hasn't copy of the book "+book.title)


class EighthTestCase(TestCase):
	def setUp(self):

		lib = create_library()
		create_user(Faculty, lib, 0)
		create_user(Student, lib, 1)
		create_user(Librarian, lib, 2)
		book = create_book(lib)
		create_copy(book, 0)

	def test_case(self):
		print("TEST 8")
		student = Student.objects.get()
		book = Book.objects.get()
		print ("student tries to check out the book "+ book.title)
		student.check_out_doc(book)
		if Copy.objects.filter(document=book, is_checked_out=True, user=student).exists():
			print ("Patron has copy of the book "+book.title)
		else:		
			print ("Student hasn't copy of the book "+book.title)
		copy = Copy.objects.get()
		print ("returning time is: "+str((copy.overdue_date - copy.booking_date).days)+" days")


class NinthTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Faculty, lib, 0)
		create_user(Student, lib, 1)
		create_user(Librarian, lib, 2)
		book = create_book(lib, is_best_seller=True)
		create_copy(book, 0)

	def test_case(self):
		print("TEST 9")
		student = Student.objects.get()
		book = Book.objects.get()
		print ("student tries to check out the book "+ book.title)
		student.check_out_doc(book)
		if Copy.objects.filter(document=book, is_checked_out=True, user=student).exists():
			print ("Patron has copy of the book "+book.title)
		else:		
			print ("Student hasn't copy of the book "+book.title)
		copy = Copy.objects.get()
		print ("returning time is: "+str((copy.overdue_date - copy.booking_date).days)+" days")


class TenthTestCase(TestCase):
	def setUp(self):
		lib = create_library()
		create_user(Patron, lib, 0)
		create_user(Librarian, lib, 1)
		book_a = create_book(lib, title='A')
		create_copy(book_a, 0)
		book_b = create_book(lib, reference=True, title="B")
		create_copy(book_b, 0)

	def test_case(self):
		print ("TEST 10")
		patron = Patron.objects.get()
		book_a = Book.objects.get(title='A')
		book_b = ReferenceBook.objects.get()

		print ("patron tries to check out the book "+ book_a.title)
		if patron.check_out_doc(book_a):
			print ("patron checks out the book " + book_a.title )
		else:
			print ("patron can't check out the book " + book_a.title )

		print ("patron tries to check out the book "+ book_b.title)
		if patron.check_out_doc(book_b):
			print ("patron checks out the book " + book_b.title )
		else:
			print ("patron can't check out the book " + book_b.title )	
