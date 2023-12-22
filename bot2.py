import requests
import json
import random
from faker import Faker
from datetime import datetime


# Load configuration from file
with open('config.json') as config_file:
    config = json.load(config_file)

API_BASE_URL = 'http://127.0.0.1:8000'  # Replace with your API base URL

fake = Faker()

class AutomatedBot:
    def __init__(self, base_url, number_of_users, max_posts_per_user, max_likes_per_user, max_dislikes_per_user=0):
        self.base_url = base_url
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.max_dislikes_per_user = max_dislikes_per_user
        self.tokens = {}

    def get_token(self, username, password):
        login_url = f"{self.base_url}/api/token/"  # Replace with your login endpoint
        response = requests.post(login_url, data={'username': username, 'password': password})
        if response.status_code == 200:
            return response.json().get('access')
        return None

    def signup_users(self):
        users = []
        for _ in range(self.number_of_users):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            user_data = {
                'username': username,
                'password': password,
                'password2': password,
                'email': email,
            }
            signup_url = f"{self.base_url}/api/signup/"  # Replace with your signup endpoint
            response = requests.post(signup_url, data=user_data)
            if response.status_code == 200:
                # Obtain JWT token after successful signup
                login_url = f"{self.base_url}/api/login/"
                response = requests.post(login_url, data={'username': email, 'password': password})
                token = response.json()['access']
                print(token)
                if token:
                    users.append({'username': username, 'token': token})
            # Simulate signup - handle response and errors if necessary
        return users

    def create_posts(self, users):
        for user in users:
            # print(user["token"])
            headers = {'Authorization': f'Bearer {user["token"]}'}
            num_posts = random.randint(1, self.max_posts_per_user)
            for _ in range(num_posts):
                post_data = {
                    'title': fake.text(10),
                    'text': fake.text(50),
                }
                create_post_url = f"{self.base_url}/api/posts/"  # Replace with your create post endpoint
                response = requests.post(create_post_url, headers=headers, data=post_data)
                # Simulate post creation - handle response and errors if necessary

    def like_posts(self, users):
        for user in users:
            headers = {'Authorization': f'Bearer {user["token"]}'}
            num_likes = random.randint(1, self.max_likes_per_user)
            for _ in range(num_likes):
                # post_id = random.randint(1, total_number_of_posts)  # Replace with actual count of posts 
                post_id = random.randint(20, 350)  # Replace with actual count of posts 

                like_post_url = f"{self.base_url}/api/posts/{post_id}/like"  # Replace with like post endpoint
                response = requests.post(like_post_url, headers=headers)
                # Simulate liking posts - handle response and errors if necessary

    def dislike_posts(self, users):
        for user in users:
            headers = {'Authorization': f'Bearer {user["token"]}'}
            num_dislikes = random.randint(1, self.max_dislikes_per_user)
            for _ in range(num_dislikes):
                # post_id = random.randint(1, total_number_of_posts)  # Replace with actual count of posts 
                post_id = random.randint(1, 15)  # Replace with actual count of posts 

                dislike_post_url = f"{self.base_url}/api/posts/{post_id}/dislike"  # Replace with like post endpoint
                response = requests.post(dislike_post_url, headers=headers)
                # Simulate liking posts - handle response and errors if necessary

    def simulate_activity(self):

        users = self.signup_users()

        self.create_posts(users)

        self.like_posts(users)
        
        self.dislike_posts(users)

if __name__ == "__main__":
    # Configuration parameters
    base_url = API_BASE_URL
    number_of_users = config['number_of_users']
    max_posts_per_user = config['max_posts_per_user']
    max_likes_per_user = config['max_likes_per_user']
    max_dislikes_per_user = config['max_dislikes_per_user']

    bot = AutomatedBot(base_url, number_of_users, max_posts_per_user, max_likes_per_user, max_dislikes_per_user)
    bot.simulate_activity()
