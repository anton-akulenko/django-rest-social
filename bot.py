import requests
import json
import random

# Load configuration from file
with open('config.json') as config_file:
    config = json.load(config_file)

API_BASE_URL = 'http://127.0.0.1:8000'  # Replace with your API base URL

# Function to signup users
def signup_users(num_users):
    for i in range(num_users):
        username = f"User_{i+1}"
        password = "Password123$"  # You may generate random passwords here
        email = f"user_{i+1}@mail.com"
        data = {'username': username, 'password': password, 'password2': password, 'email': email}
        response = requests.post(f'{API_BASE_URL}/api/signup/', data=data)
        if response.status_code == 200:
            print(f"User {username} signed up successfully")
        else:
            print(f"Failed to signup user {username} /n {response.content}")

# Function to create posts for users
def create_posts_for_users(num_users, max_posts_per_user):
    for i in range(num_users):
        num_posts = random.randint(1, max_posts_per_user)
        user_id = i + 1
        for _ in range(num_posts):
            content = f"This is post {random.randint(1, 100)} content."
            data = {'user': user_id, 'content': content}
            response = requests.post(f'{API_BASE_URL}/api/posts/', data=data)
            if response.status_code == 201:
                print(f"Post created for User {user_id}")
            else:
                print(f"Failed to create post for User {user_id}")

# Function to like posts randomly
def like_posts_randomly(num_users, max_likes_per_user):
    for i in range(num_users):
        user_id = i + 1
        num_likes = random.randint(1, max_likes_per_user)
        posts = requests.get(f'{API_BASE_URL}/api/posts/').json()
        post_ids = [post['id'] for post in posts]
        for _ in range(num_likes):
            post_id = random.choice(post_ids)
            data = {'user': user_id, 'post': post_id}
            response = requests.post(f'{API_BASE_URL}/api/like/', data=data)
            if response.status_code == 200:
                print(f"User {user_id} liked Post {post_id}")
            else:
                print(f"Failed to like Post {post_id} by User {user_id}")

# Perform actions based on config
if __name__ == '__main__':
    number_of_users = config['number_of_users']
    # max_posts_per_user = config['max_posts_per_user']
    # max_likes_per_user = config['max_likes_per_user']

    signup_users(number_of_users)
    # create_posts_for_users(number_of_users, max_posts_per_user)
    # like_posts_randomly(number_of_users, max_likes_per_user)

