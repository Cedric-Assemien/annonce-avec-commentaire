from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.shortcuts import  get_object_or_404
from .models import Post, PostApproved , Comment
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def index(request):
    approved_posts = PostApproved.objects.all()
    return render(request, 'index.html', {'approved_posts': approved_posts})

@user_passes_test(lambda u: u.is_superuser)
def review_posts(request):
    unapproved_posts = Post.objects.filter(is_approved=False)
    return render(request, 'review_posts.html', {'unapproved_posts': unapproved_posts})

@user_passes_test(lambda u: u.is_superuser)
def approve_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    PostApproved.objects.create(
        user=post.user,
        title=post.title,
        image=post.image,
        content=post.content,
        created_at = post.created_at
    )
    post.delete()

    return redirect('review_posts')

def single (request):

    return render (request,'single.html')

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        post = Post.objects.create(
            user=request.user,
            title=title,
            category=category,
            content=content,
            image=image,
        )

        messages.success(request, 'Votre annonce a été soumis avec succès')
        return redirect('index') 
    return render(request, 'createpost.html')

def post_detail(request, post_id):
    post = get_object_or_404(PostApproved, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        message = request.POST.get('message')

        Comment.objects.create(
            post=post,
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            website=website,
            message=message
        )

        return redirect('single', post_id=post_id)
    return render(request, 'single.html', {'post': post, 'comments': comments})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        your_name = request.POST.get('your_name')
        your_pass = request.POST.get('your_pass')

       
        if not your_name or not your_pass:
            messages.error(request, 'Désolé, tous les champs sont requis.')
            return redirect('login')  

        # Authentifie l'utilisateur
        user = authenticate(request, username=your_name, password=your_pass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie.')
            return redirect('index')  
        else:
            messages.error(request, 'Veuillez réessayer.')

    return render(request, 'login.html')



@csrf_protect
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        re_password = request.POST.get('re_pass')

        # Vérifier si les champs ne sont pas vides
        if not name or not email or not password or not re_password:
            messages.error(request, 'Tous les champs sont requis.')
            return redirect('register')

        # Vérifier si les mots de passe correspondent
        if password != re_password:
            messages.error(request, ' mots de passe incorrecte!!!')
            return redirect('register')

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un utilisateur avec cette adresse e-mail existe déjà.')
            return redirect('register')

        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=email, email=email, password=password)
        
        messages.success(request, 'Veuillez-vous connecter.', extra_tags='success')
        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Déconnexion réussie!')
    return redirect('index')





