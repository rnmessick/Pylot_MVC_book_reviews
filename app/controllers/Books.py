from system.core.controller import *
from flask import redirect, request, flash

class Books(Controller):
    def __init__(self,action):
        super(Books, self).__init__(action)
        self.load_model('Book')

    def new(self):
        return self.load_view('/book_new.html')

    def create(self):
        book_info = request.form
        user_id = session['id']
        book_id = session['id']
        result = self.models['Book'].create_book(user_id,book_info)
        return redirect('/user')

    def show(self, id):
        #showing info of book and its reviews
        book_id = id
        book_info = self.models['Book'].book_info(book_id)
        reviews = self.models['Book'].get_reviews(book_id)
        return self.load_view('/book_show.html', book_info = book_info, reviews = reviews, id=id)

    def update(self, id):
        user_id = session['id']
        book_id = id
        info = request.form
        reviews = self.models['Book'].add_reviews(user_id, book_id, info)
        return redirect('/books/'+str(reviews))

    def destroy(self, id):
        review_id = id
        delete_review = self.models['Book'].destroy(review_id)
        return redirect('/books/'+str(delete_review))

    