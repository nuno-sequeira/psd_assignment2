import LibraryWithPrinting

if __name__ == "__main__":
    """Test"""
    library = LibraryWithPrinting.LibraryWithPrints()
    library.add_user('ypyp')
    library.add_user('yoyo')
    library.add_book('lol')
    library.add_book('lol')
    library.reserve_book('ypyp', 'lol', 1, 2)
    library.check_reservation('ypyp', 'lol', 1)
    library.change_reservation('ypyp', 'lol', 1, 'yoyo')
    library.check_reservation('yoyo', 'lol', 1)


