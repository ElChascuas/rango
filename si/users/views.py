from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from users.forms import UserRegistrationForm


def login_request(request):
    """Esta vista retorna un login del usuario en caso de que haya completado el formulario
     con datos validos de un usuario que haya sido registrado previamente"""
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                context = {"message":f"¿Listo para tu proxima aventura? {username}"}
                return render(request, "index.html", context=context)

        form = AuthenticationForm()
        return render(request, "users/login.html", {"error": "Hubo un erorr, no estas registrado en el gremio", "form": form})

    elif request.method == "GET":
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    """Esta vista retorna un formulario de creacion de usuario y lo registra en la base de datos"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            context = {"errors": form.errors}
            form = UserRegistrationForm
            context["form"] = form
            return render(request, "users/register.html", context)
    elif request.method == "GET":
        form = UserRegistrationForm()
        return render(request, "users/register.html", {"form": form})