from rest_framework import serializers
from social_network.models import Post, Like, Dislike, User, UserActivity
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, user_logged_in


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'author', 'created_at', 'likes', 'dislikes']

    def get_likes(self, post):
        return Like.objects.filter(post=post).count()

    def get_dislikes(self, post):
        return Dislike.objects.filter(post=post).count()


class LikeSerializer(serializers.ModelSerializer):
    liker = serializers.ReadOnlyField(source='liker.email')

    class Meta:
        model = Like
        fields = ['id', 'liker', 'created_at']

class DislikeSerializer(serializers.ModelSerializer):
    disliker = serializers.ReadOnlyField(source='disliker.email')

    class Meta:
        model = Dislike
        fields = ['id', 'disliker', 'created_at']


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=25, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        user = User.objects.create_user(username=validated_data["username"],
                                        email=validated_data["email"],
                                        )
        user.set_password(password)
        user.save()
        return user



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')


        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        refresh = RefreshToken.for_user(user)
        user_logged_in.send(sender=user.__class__, request=self.context.get('request'), user=user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        attrs['last_login'] = user.last_login
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', format="%Y-%m-%d %H:%M:%S")
    last_request = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    date_joined = serializers.CharField(source='user.date_joined', read_only=True)
    class Meta:
        model = UserActivity
        fields = ['username', 'email', 'last_login', 'last_request', 'date_joined']
