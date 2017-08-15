from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, UpvotingForm
from django.shortcuts import render_to_response, get_object_or_404
from models import User, SessionToken, Post, Like, Comment
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from InstaClone.settings import BASE_DIR

from imgurpython import ImgurClient
# Create your views here.

with open('imgur_details.txt') as file:
    CLIENT_ID = file.readline(1)
    CLIENT_SECRET = file.readline(2)

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving data to DB
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
            # return redirect('login/')
    else:
        form = SignUpForm()

    return render(request, 'index.html', {'form': form})


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = Post(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '/' + post.image.url)

                client = ImgurClient(CLIENT_ID,CLIENT_SECRET)
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form': form})
    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:

        posts = Post.objects.all().order_by('created_on')

        for post in posts:
            existing_like = Like.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = Like(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = Like.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                Like.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = Comment(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = Comment.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


def search_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'GET':
            verification_code = request.GET.get('verification_code')
            user_id = request.GET.get('user_id')

    context = {
        'verification_code': verification_code,
        'user_id': user_id,
    }
    return render_to_response('search.html', context, context_instance = RequestContext(request))


def upvoting_view(request):
    user = check_validation(request)
    comment = None
    print "upvote"
    if user and request.method == 'POST':

        form = UpvotingForm(request.POST)
        if form.is_valid():
            print form.cleaned_data

            comment_id = int(form.cleaned_data.get('userid'))

            comment = Comment.objects.filter(userid=comment_id).first()
            print "isnt a upvote"

            if comment is not None:
                print "upvoted"
                comment.upvote_num += 1
                comment.save()
                print comment.upvote_num
            else:
                print 'Rookie Mistake'
        else:
            print "Not Valid"
            return redirect('/feeds/')
    else:
        return redirect('/login/')


def logout_view(request):
    user = check_validation(request)
    if user is not None:
        latest_session = SessionToken.objects.filter(user=user).last()
        if latest_session:
            latest_session.delete()

    return redirect("/login/")


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None