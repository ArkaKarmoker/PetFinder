from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from .models import Pet, AdoptionRequest, Favorite
from .forms import UserRegisterForm, UserProfileForm, UserPasswordChangeForm, AdoptionRequestForm

# Create your views here.


def home(request):
    featured_pets = Pet.objects.filter(status='Available')[:6]
    recent_adoptions = Pet.objects.filter(status='Adopted')[:4]
    total_pets = Pet.objects.count()
    total_adopted = Pet.objects.filter(status='Adopted').count()
    total_available = Pet.objects.filter(status='Available').count()

    # Animal categories
    categories = [
        {'type': 'Dog', 'icon': 'bi-dog', 'count': Pet.objects.filter(animal_type='Dog', status='Available').count()},
        {'type': 'Cat', 'icon': 'bi-cat', 'count': Pet.objects.filter(animal_type='Cat', status='Available').count()},
        {'type': 'Bird', 'icon': 'bi-twitter', 'count': Pet.objects.filter(animal_type='Bird', status='Available').count()},
        {'type': 'Rabbit', 'icon': 'bi-egg', 'count': Pet.objects.filter(animal_type='Rabbit', status='Available').count()},
        {'type': 'Other', 'icon': 'bi-heart', 'count': Pet.objects.filter(animal_type='Other', status='Available').count()},
    ]

    context = {
        'featured_pets': featured_pets,
        'recent_adoptions': recent_adoptions,
        'total_pets': total_pets,
        'total_adopted': total_adopted,
        'total_available': total_available,
        'categories': categories,
    }
    return render(request, 'pets/home.html', context)


def pet_list(request):
    pets_qs = Pet.objects.all()

    # Search & Filter
    search_query = request.GET.get('search', '').strip()
    animal_type = request.GET.get('animal_type', '').strip()
    breed = request.GET.get('breed', '').strip()
    gender = request.GET.get('gender', '').strip()
    location = request.GET.get('location', '').strip()
    status = request.GET.get('status', '').strip()

    if search_query:
        pets_qs = pets_qs.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if animal_type:
        pets_qs = pets_qs.filter(animal_type__iexact=animal_type)

    if breed:
        pets_qs = pets_qs.filter(breed__icontains=breed)

    if gender:
        pets_qs = pets_qs.filter(gender__iexact=gender)

    if location:
        pets_qs = pets_qs.filter(location__icontains=location)

    if status:
        pets_qs = pets_qs.filter(status__iexact=status)

    # Distinct locations and breeds for filter dropdowns
    locations = Pet.objects.values_list('location', flat=True).distinct()
    breeds = Pet.objects.values_list('breed', flat=True).distinct()

    # Pagination
    paginator = Paginator(pets_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # User favorite IDs
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = list(Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True))

    context = {
        'pets': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'animal_type': animal_type,
        'breed': breed,
        'gender': gender,
        'location': location,
        'status': status,
        'locations': locations,
        'breeds': breeds,
        'user_favorites': user_favorites,
        'animal_types': Pet.ANIMAL_TYPE_CHOICES,
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    has_pending_request = False
    is_favorited = False

    if request.user.is_authenticated:
        has_pending_request = AdoptionRequest.objects.filter(
            user=request.user,
            pet=pet,
            status='Pending'
        ).exists()
        is_favorited = Favorite.objects.filter(user=request.user, pet=pet).exists()

    context = {
        'pet': pet,
        'has_pending_request': has_pending_request,
        'is_favorited': is_favorited,
    }
    return render(request, 'pets/pet_detail.html', context)


@login_required
def apply_adoption(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    # Rule 1: Only available pets can be adopted
    if pet.status != 'Available':
        messages.error(request, f"Sorry, {pet.name} is not available for adoption.")
        return redirect('pet_detail', pk=pet.pk)

    # Rule 2: One user cannot submit multiple active requests for the same pet
    existing_request = AdoptionRequest.objects.filter(
        user=request.user,
        pet=pet,
        status='Pending'
    ).first()

    if existing_request:
        messages.warning(request, f"You already have a pending adoption request for {pet.name}.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user
            adoption_request.pet = pet
            adoption_request.status = 'Pending'
            try:
                adoption_request.full_clean()
                adoption_request.save()
                messages.success(request, f"Your adoption request for {pet.name} was successfully submitted!")
                return redirect('user_dashboard')
            except ValidationError as e:
                for field, err_list in e.message_dict.items():
                    for err in err_list:
                        messages.error(request, err)
    else:
        form = AdoptionRequestForm()

    context = {
        'pet': pet,
        'form': form,
    }
    return render(request, 'pets/adoption_form.html', context)


@login_required
def user_dashboard(request):
    adoption_requests = AdoptionRequest.objects.filter(user=request.user).select_related('pet')
    favorites = Favorite.objects.filter(user=request.user).select_related('pet')
    total_requests = adoption_requests.count()
    pending_count = adoption_requests.filter(status='Pending').count()
    approved_count = adoption_requests.filter(status='Approved').count()
    favorites_count = favorites.count()
    context = {
        'adoption_requests': adoption_requests,
        'favorites': favorites,
        'total_requests': total_requests,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'favorites_count': favorites_count,
    }
    return render(request, 'pets/dashboard.html', context)


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'pets/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('user_profile')
    else:
        form = UserPasswordChangeForm(user=request.user)

    return render(request, 'pets/change_password.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to PetFinder, {user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'pets/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'pets/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def toggle_favorite(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    fav = Favorite.objects.filter(user=request.user, pet=pet).first()
    if fav:
        fav.delete()
        favorited = False
        messages.info(request, f"Removed {pet.name} from your favorites.")
    else:
        Favorite.objects.create(user=request.user, pet=pet)
        favorited = True
        messages.success(request, f"Added {pet.name} to your favorites! ❤️")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'favorited': favorited})

    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('pet_detail', pk=pk)

