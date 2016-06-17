from system.core.model import Model
import re

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()

    def create_book(self, user_id,book_info):
        author_query="SELECT * FROM authors WHERE name='{}'".format(book_info['author'])
        author = self.db.query_db(author_query)
        if not author:
            insert_author_query = "INSERT INTO authors (name, created_at, updated_at) VALUES ('{}',NOW(), NOW())".format(book_info['author'])
            self.db.query_db(insert_author_query)
        else:
            insert_author_query = "INSERT INTO authors (name, created_at, updated_at) VALUES ('{}',NOW(), NOW())".format(book_info['author'])
            self.db.query_db(insert_author_query)

        get_author_query = "SELECT * FROM authors ORDER BY id DESC LIMIT 1"
        author = self.db.query_db(get_author_query)
        # print author
        insert_book_query = "INSERT INTO books (title, author_id, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(book_info['title'], author[0]['id'])
        self.db.query_db(insert_book_query)

        get_book_query = "SELECT * FROM books ORDER BY id DESC LIMIT 1"
        book = self.db.query_db(get_book_query)
        # print book
        insert_review_query = "INSERT INTO reviews (review, rating, created_at, updated_at, user_id, book_id) VALUES ('{}','{}',NOW(),NOW(),'{}','{}')".format(book_info['review'], book_info['rating'],user[0]['id'], book[0]['id'])
        self.db.query_db(insert_review_query)
        print book[0]['id']
        return book[0]['id']

    def book_info(self, id):
        book_info_query = "SELECT books.title, authors.name, books.id FROM books JOIN authors ON authors.id = books.author_id WHERE books.id = '{}'".format(id)
        book_info = self.db.query_db(book_info_query)
        print book_info[0]
        return book_info[0]

    def get_reviews(self, id):
        get_reviews_query = "SELECT reviews.rating, reviews.review, users.name, reviews.created_at, users.id, reviews.id AS review_id FROM reviews JOIN books ON reviews.book_id = books.id LEFT JOIN users ON users.id = reviews.user_id WHERE books.id = {}".format(id)
        reviews = self.db.query_db(get_reviews_query)
        # print reviews
        return reviews

    def add_reviews(self, user_id, book_id, info):
        add_reviews_query = "INSERT INTO reviews (review, rating, created_at, updated_at, user_id, book_id) VALUES ('{}','{}',NOW(), NOW(), '{}','{}')".format(info['add_review'],info['rating'],user_id,book_id)
        self.db.query_db(add_reviews_query)

        book_id_query = "SELECT id from books WHERE id = {}".format(book_id)
        book_id = self.db.query_db(book_id_query)
        return book_id[0]['id']

    def recent_reviews(self):
        recent_reviews = "SELECT reviews.rating, reviews.review, users.name, users.id as user_id, reviews.created_at, books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id LEFT JOIN users ON users.id = reviews.user_id ORDER BY reviews.created_at DESC LIMIT 3"
        reviews = self.db.query_db(recent_reviews)
        return reviews

    def other_reviews(self):
        other_reviews_query = "SELECT books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id GROUP BY books.title ORDER BY reviews.created_at ASC"
        other_reviews = self.db.query_db(other_reviews_query)
        return other_reviews

    def total_reviews(self, user_id):
        total_reviews_query = "SELECT COUNT(*) AS total_reviews FROM reviews WHERE user_id = {}".format(user_id)
        total_reviews = self.db.query_db(total_reviews_query)
        return total_reviews[0]

    def review_titles(self, user_id):
        review_titles_query = "SELECT books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id WHERE user_id = {} GROUP BY books.title".format(user_id)
        review_titles = self.db.query_db(review_titles_query)
        return review_titles
        
    def destroy(self, review_id):
        book_id_query = "SELECT books.id FROM books  JOIN reviews ON reviews.book_id = books.id WHERE reviews.id = {}".format(review_id)
        book_id = self.db.query_db(book_id_query)
        print book_id
        delete_query = "DELETE FROM reviews WHERE id='{}'".format(review_id)
        delete = self.db.query_db(delete_query)
        return book_id[0]['id']