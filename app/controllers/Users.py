from system.core.controller import *
from flask import redirect, request, flash

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.load_model('Book')

    def index(self):
        return self.load_view('/user_login.html')

    def create(self):
        user_info = request.form
        user = self.models['User'].create(user_info)
        if user['status'] == False:
            for message in user['message']:
                flash(message)
                return redirect('/')
        else:
            flash("You have succesfully registered!")
            return redirect('/')

    def login(self):
        login_info = request.form
        login = self.models['User'].login(login_info)
        if login['status'] == True:
            session['id'] = login['login_status']['id']
            session['name'] = login['login_status']['name']
            return redirect('/user')
        else:
            return redirect('/')

    def logout(self):
        session.pop=['id']
        session.pop=['name']
        return redirect('/')

    def homepage(self):
        recent_reviews = self.models['Book'].recent_reviews()
        other_reviews = self.models['Book'].other_reviews()
        return self.load_view('/user_homepage.html', recent_reviews=recent_reviews, other_reviews=other_reviews)

    def show(self, id):
        user_id = id
        user_info = self.models['User'].user_info(user_id)
        total_reviews = self.models['Book'].total_reviews(user_id)
        review_titles = self.models['Book'].review_titles(user_id)
        return self.load_view('/user_show.html', user_info = user_info, total_reviews = total_reviews, review_titles = review_titles)