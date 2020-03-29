import unittest
from itertools import count


class Reservation(object):
    _ids = count(0)

    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0

    def overlapping(self, other):
        ret = (self._book == other._book and self._to >= other._from
               and self._to >= other._from)
        return ret

    def includes(self, date):
        ret = (self._from <= date <= self._to)
        return ret

    def identify(self, date, book, for_):
        if book != self._book:
            return book
        if for_ != self._for:
            return for_
        if not self.includes(date):
            return False
        return True

    def change_for(self, for_):
        self._for = for_
    
    def get_reservation_id(self):
        return self._id

    def get_book(self):
        return self._book

    def get_for(self):
        return self._for

    def get_from(self):
        return self._from

    def get_to(self):
        return self._to


class ReservationWithPrints(Reservation):
    def __init__(self, from_, to, book, for_):
        super(ReservationWithPrints, self).__init__(from_, to, book, for_)
        print(F'Created a reservation with id {super(ReservationWithPrints, self).get_reservation_id()}' +
              F' of {book} from {from_} to {to} for {for_}.')

    def overlapping(self, other):
        ret = super(ReservationWithPrints, self).overlapping(other)
        string = 'do'
        if not ret:
            string = 'do not'
        print(F'Reservations {super(ReservationWithPrints, self).get_reservation_id()}' +
              F' and {other._id} {string} overlap')

    def includes(self, date):
        ret = super(ReservationWithPrints, self).includes(date)
        str = 'includes'
        if not ret:
            str = 'does not include'
        print(F'Reservation {super(ReservationWithPrints, self).get_reservation_id()} {str} {date}')

    def identify(self, date, book, for_):
        ret = super(ReservationWithPrints, self).identify(date, book, for_)
        if book == ret:
            print(F'Reservation {super(ReservationWithPrints, self).get_reservation_id()}' +
                  F' reserves {super(ReservationWithPrints, self).get_book()} not {book}.')
        elif for_ == ret:
            print(F'Reservation {super(ReservationWithPrints, self).get_reservation_id()}' +
                  F' is for {super(ReservationWithPrints, self).get_for()} not {for_}.')
        elif not ret:
            print(F'Reservation {super(ReservationWithPrints, self).get_reservation_id()}' +
                  F' is from {super(ReservationWithPrints, self).get_from()}' +
                  F' to {super(ReservationWithPrints, self).get_to()} which ' +
                  F'does not include {date}.')
        else:
            print(F'Reservation {super(ReservationWithPrints, self).get_reservation_id()}' +
                  F' is valid {for_} of {book} on {date}.')

    def change_for(self, for_):
        print(F'Reservation {super(ReservationWithPrints, self).get_reservation_id()}' +
              F' moved from {super(ReservationWithPrints, self).get_for()} to {for_}')
        super(ReservationWithPrints, self).change_for(for_)


class TestReservation(unittest.TestCase):
    def test_overlapping_same_book(self):
        from_ = 1
        to = 3
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        from_0 = 3
        to_0 = 4
        book_0 = 'Gatsbyy'
        for_0 = 'Richard'
        other = Reservation(from_0, to_0, book_0, for_0)

        result = reservation.overlapping(other)

        self.assertFalse(result)

    def test_overlapping_date_on_first_user(self):
        from_ = 1
        to = 2
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        from_0 = 3
        to_0 = 4
        book_0 = 'Gatsby'
        for_0 = 'Richard'
        other = Reservation(from_0, to_0, book_0, for_0)

        result = reservation.overlapping(other)

        self.assertFalse(result)

    def test_includes_to_is_lower(self):
        from_ = 1
        to = 2
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        date = 3

        result = reservation.includes(date)

        self.assertFalse(result)

    def test_includes_from_is_higher(self):
        from_ = 2
        to = 3
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        date = 1

        result = reservation.includes(date)

        self.assertFalse(result)

    def test_identify_no_book(self):
        from_ = 1
        to = 2
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        date = 1
        book_test = 'Cosmos'

        result = reservation.identify(date, book_test, for_)

        self.assertIs(result, book_test)

    def test_identify_no_for_(self):
        from_ = 1
        to = 2
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        date = 1
        for_test = 'Richard'

        result = reservation.identify(date, book, for_test)

        self.assertIs(result, for_test)

    def test_identify_date(self):
        from_ = 1
        to = 2
        book = 'Gatsby'
        for_ = 'Carl'
        reservation = Reservation(from_, to, book, for_)
        date = 3

        result = reservation.identify(date, book, for_)

        self.assertFalse(result)
