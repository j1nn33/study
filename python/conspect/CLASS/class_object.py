class Book():
    def __init__(self, author, name, year, item):
        self.author = author
        self.name = name
        self.year = year
        self.item = item

    def __repr__(self):
        return (self.name)


def main():
    book1 = Book('red', 'final', 1982, 'fictono')
    print(repr(book1))
    print(book1.author, book1.year)
    print(str(book1))


if __name__ == '__main__':
    main()