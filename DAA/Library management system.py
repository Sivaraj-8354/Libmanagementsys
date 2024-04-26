import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class Book:
    def __init__(self, title, author, category, ISBN):
        self.title = title
        self.author = author
        self.category = category
        self.ISBN = ISBN

def quicksort(arr, key='title'):
    if len(arr) <= 1:
        return arr
    else:
        pivot = getattr(arr[0], key)
        less = [book for book in arr[1:] if getattr(book, key) < pivot]
        greater = [book for book in arr[1:] if getattr(book, key) >= pivot]
        return quicksort(less, key) + [arr[0]] + quicksort(greater, key)

def partial_match(title, search_title):
    return title.lower().find(search_title.lower()) != -1

def binary_search(arr, search_title, key='title'):
    low, high = 0, len(arr) - 1
    matching_indices = []

    while low <= high:
        mid = (low + high) // 2
        mid_value = getattr(arr[mid], key)

        if partial_match(mid_value, search_title):
            matching_indices.append(mid)
            # Continue searching on both sides for more matches
            left = mid - 1
            right = mid + 1

            while left >= 0 and partial_match(getattr(arr[left], key), search_title):
                matching_indices.append(left)
                left -= 1

            while right < len(arr) and partial_match(getattr(arr[right], key), search_title):
                matching_indices.append(right)
                right += 1

            return matching_indices

        elif mid_value < search_title:
            low = mid + 1
        else:
            high = mid - 1

    return matching_indices

class LibraryManagementSystem:
    def __init__(self, root):
        self.library = []
        self.root = root
        self.root.title("Library Management System")

        # Initialize GUI components
        self.create_gui()

        # Add default books to the library
        self.add_default_books()

    def create_gui(self):
        # Entry variables
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # Labels
        ttk.Label(self.root, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.root, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.root, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.root, text="ISBN:").grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Entry widgets
        ttk.Entry(self.root, textvariable=self.title_var).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.author_var).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.category_var).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.isbn_var).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Buttons
        ttk.Button(self.root, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Label(self.root, text="Search:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.search_var).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self.root, text="Search", command=self.search_books).grid(row=6, column=0, columnspan=2, pady=10)

        # Listbox with Scrollbars
        self.book_listbox = tk.Listbox(self.root, width=50, height=10)
        self.book_listbox.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        y_scrollbar = ttk.Scrollbar(self.root, command=self.book_listbox.yview, orient='vertical')
        y_scrollbar.grid(row=7, column=2, sticky="nsw")
        self.book_listbox.config(yscrollcommand=y_scrollbar.set)
        
        x_scrollbar = ttk.Scrollbar(self.root, command=self.book_listbox.xview, orient='horizontal')
        x_scrollbar.grid(row=8, column=0, columnspan=2, sticky="ew")
        self.book_listbox.config(xscrollcommand=x_scrollbar.set)

    def add_book(self):
        title = self.title_var.get()
        author = self.author_var.get()
        category = self.category_var.get()
        isbn = self.isbn_var.get()

        # Check if any of the fields is empty
        if not (title and author and category and isbn):
            tk.messagebox.showerror("Error", "Please fill in all fields.")
            return

        new_book = Book(title, author, category, isbn)
        self.library.append(new_book)

        # Display the books in the listbox
        self.display_books()

    def search_books(self):
        search_term = self.search_var.get().lower()
        matching_books = [book for book in self.library if
                          search_term in book.title.lower() or search_term in book.category.lower()]

        # Display the matching books in the listbox
        self.display_books(matching_books)

    def display_books(self, books=None):
        # Clear the listbox
        self.book_listbox.delete(0, tk.END)

        if books is None:
            books = self.library

        # Sort the books before displaying
        sorted_books = quicksort(books, key='title')

        # Display books in the listbox
        for i, book in enumerate(sorted_books):
            display_text = f"{i + 1}. Title: {book.title}, Author: {book.author}, Category: {book.category}, ISBN: {book.ISBN}"
            self.book_listbox.insert(tk.END, display_text)

    def add_default_books(self):
        # Add 5 default books to the library
        default_books = [
            Book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "9780142437016"),
            Book("To Kill a Mockingbird", "Harper Lee", "Fiction", "0061120081"),
            Book("1984", "George Orwell", "Dystopian", "0451524934"),
            Book("Pride and Prejudice", "Jane Austen", "Classic", "9780141439518"),
            Book("The Catcher in the Rye", "J.D. Salinger", "Fiction", "9780241950432")
        ]

        self.library.extend(default_books)
        self.display_books()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

