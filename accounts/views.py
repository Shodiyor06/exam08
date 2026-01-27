from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import generics, permissions

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


# ===== API VIEWS =====
class RegisterView(generics.CreateAPIView):
    """API: User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    """API: Get current user info"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ===== HTML VIEWS =====
def login_view(request):
    """HTML: Login page"""
    if request.user.is_authenticated:
        return redirect("/events/")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Username va parolni kiriting")
            return redirect("/login/")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/events/")
        else:
            messages.error(request, "Login yoki parol xato")

    return render(request, "login.html")


def register_view(request):
    """HTML: Registration page"""
    if request.user.is_authenticated:
        return redirect("/events/")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        # ===== VALIDATION =====
        if not username or not password1 or not password2:
            messages.error(request, "Barcha majburiy maydonlarni to'ldiring")
            return render(request, "register.html")

        if password1 != password2:
            messages.error(request, "Parollar mos emas")
            return render(request, "register.html")

        if len(password1) < 6:
            messages.error(request, "Parol kamida 6 ta belgidan iborat bo'lishi kerak")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band")
            return render(request, "register.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Bu email band")
            return render(request, "register.html")

        # ===== CREATE USER =====
        try:
            user = User.objects.create_user(
                username=username,
                email=email if email else "",
                password=password1
            )
            login(request, user)
            return redirect("/events/")
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return render(request, "register.html")

    return render(request, "register.html")


@login_required
def logout_view(request):
    """HTML: Logout"""
    logout(request)
    return redirect("/login/")