import unittest

from ReservationsWithPrinting import Reservation


class Library(object):
    def __init__(self):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from

    def add_user(self, name):
        if name in self._users:
            return None
        self._users.add(name)
        return name

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1
        return self._books[name]

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return False
        if date_from > date_to:
            return False
        if book_count == 0:
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return False
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        return desired_reservation

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        return res

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            return False
        if new_user not in self._users:
            return new_user
        relevant_reservations[0].change_for(new_user)

    def book_get_copy(self, book):
        return self._books.get(book, 0)

    def get_user(self, user):
        return user in self._users


class LibraryWithPrints(Library):

    def __init__(self):
        super(LibraryWithPrints, self).__init__()
        print(F'Library created.')

    def add_user(self, name):
        user = super(LibraryWithPrints, self).add_user(name)
        if name == user:
            print(F'User {name} created.')
        else:
            print(F'User not created, user with name {name} already exists.')

    def add_book(self, name):
        copies = super(LibraryWithPrints, self).add_book(name)
        print(F'Book {name} added. We have {copies} coppies of the book.')

    def reserve_book(self, user, book, date_from, date_to):
        book_count = super(LibraryWithPrints, self).book_get_copy(book)
        if user not in self._users:
            print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                  F'User does not exist.')
        elif date_from > date_to:
            print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                  F'Incorrect dates.')
        elif book_count == 0:
            print(F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. ' +
                  F'We do not have that book.')
        else:
            desired_reservation = super(LibraryWithPrints, self).reserve_book(user, book, date_from, date_to)
            if desired_reservation:
                print(F'Reservation {desired_reservation._id} included.')
            else:
                print(F'We cannot reserve book {book} for {user} from {date_from} ' +
                      F'to {date_to}. We do not have enough books.')

    def check_reservation(self, user, book, date):
        res = super(LibraryWithPrints, self).check_reservation(user, book, date)
        string = 'exists'
        if not res:
            string = 'does not exist'
        print(F'Reservation for {user} of {book} on {date} {string}.')

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = super(LibraryWithPrints, self).change_reservation(user, book, date, new_user)
        if not relevant_reservations:
            print(F'Reservation for {user} of {book} on {date} does not exist.')
        elif new_user in relevant_reservations:
            print(F'Cannot change the reservation as {new_user} does not exist.')
        else:
            print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')


class TestLibrary(unittest.TestCase):
    def test_add_user_isnt_user(self):
        library = Library()
        user = 'Carl'

        result = library.add_user(user)

        self.assertIsNotNone(result)

    def test_add_user_is_user(self):
        library = Library()
        user = 'Carl'
        library.add_user(user)

        result = library.add_user(user)

        self.assertIsNone(result)

    def test_reserve_book_user_not_in_users(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date_from = 1
        date_to = 2

        result = library.reserve_book(user, book, date_from, date_to)

        self.assertFalse(result)

    def test_reserve_book_user_not_valid_date(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date_from = 2
        date_to = 1
        library.add_user(user)

        result = library.reserve_book(user, book, date_from, date_to)

        self.assertFalse(result)

    def test_reserve_book_count_0(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date_from = 1
        date_to = 2
        library.add_user(user)

        result = library.reserve_book(user, book, date_from, date_to)

        self.assertFalse(result)

    def test_reserve_more_than_book_count(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date_from = 1
        date_to = 2
        library.add_user(user)
        library.add_book(book)
        library.reserve_book(user, book, date_from, date_to)

        result = library.reserve_book(user, book, date_from, date_to)

        self.assertFalse(result)

    def test_reserve_book(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date_from = 1
        date_to = 2
        library.add_user(user)
        library.add_book(book)

        result = library.reserve_book(user, book, date_from, date_to)

        self.assertIsNotNone(result)

    def test_check_reservation(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date = 1
        library.add_user(user)
        library.add_book(book)
        library.reserve_book(user, book, 1, 2)

        result = library.check_reservation(user, book, date)

        self.assertTrue(result)

    def test_check_reservation_no_reservation(self):
        library = Library()
        user = 'Carl'
        book = 'Gatsby'
        date = 1
        library.add_user(user)
        library.add_book(book)

        result = library.check_reservation(user, book, date)

        self.assertFalse(result)

    def test_change_reservation_no_reservation(self):
        library = Library()
        user = 'Carl'
        new_user = 'Richard'
        book = 'Gatsby'
        date = 1
        library.add_user(user)
        library.add_book(book)

        result = library.change_reservation(user, book, date, new_user)

        self.assertFalse(result)

    def test_change_reservation_no_new_user(self):
        library = Library()
        user = 'Carl'
        new_user = 'Richard'
        book = 'Gatsby'
        date = 1
        library.add_user(user)
        library.add_book(book)
        library.reserve_book(user, book, 1, 2)

        result = library.change_reservation(user, book, date, new_user)

        self.assertIsNotNone(result)

    def test_book_get_copy_no_book(self):
        library = Library()
        book = 'Gatsby'

        result = library.book_get_copy(book)

        self.assertEqual(result, 0)

    def test_book_get_copy_with_book(self):
        library = Library()
        book = 'Gatsby'
        library.add_book(book)

        result = library.book_get_copy(book)

        self.assertNotEqual(result, 0)

    def test_get_user_no_user(self):
        library = Library()
        user = 'Carl'

        result = library.get_user(user)

        self.assertFalse(result)

    def test_get_user_with_user(self):
        library = Library()
        user = 'Carl'
        library.add_user(user)

        result = library.get_user(user)

        self.assertTrue(result)
