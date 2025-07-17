from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """
    Returns a QuerySet of all Book instances whose author’s name matches `author_name`.
    """
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return Book.objects.none()
    return author.books.all()


def get_books_in_library(library_name):
    """
    Returns a QuerySet of all Book instances in the Library with the given name.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return Book.objects.none()
    return library.books.all()


def get_librarian_for_library(library_name):
    """
    Returns the Librarian instance for the Library with the given name,
    or None if no such library or no librarian is assigned.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None

    # thanks to related_name='librarian', we can do:
    return getattr(library, 'librarian', None)


# ——— Example usage ———
if __name__ == "__main__":
    print("Books by Tolkien:", list(get_books_by_author("J. R. R. Tolkien")))
    print("Books at Central Library:", list(get_books_in_library("Central Library")))
    print("Librarian at Central Library:", get_librarian_for_library("Central Library"))
