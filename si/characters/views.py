from django.shortcuts import render, redirect
from characters.models import Character
from characters.forms import FormularioCharacters
from django.contrib.auth.decorators import login_required, user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def create_character(request):
    """Esta vista retorna el personaje creado, 
    ademas requiere estar logueado para acceder, de lo contrario te envia al registro."""
    if request.method == 'POST': 
        form= FormularioCharacters(request.POST, request.FILES)

        if form.is_valid():
            Character.objects.create(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                age = form.cleaned_data['age'],
                alineamiento = form.cleaned_data['clase'],
                clase = form.cleaned_data['clase'],
                lvl = form.cleaned_data['lvl'],
                image= form.cleaned_data["image"])     
            return redirect(characters)
     
    elif request.method == 'GET':
        form_character = FormularioCharacters
        context = {'form_character':form_character}
        return render(request, "characters/create_character.html", context=context)


@login_required
def search_characters(request):
   search = request.GET['search']
   characters = Character.objects.filter(name__icontains=search)
   context={'characters':characters}
   return render(request, 'characters/search_characters.html', context=context)


@login_required
def characters(request):
    """Esta vista retorna todos los personajes de la base de datos y los muestra, 
    ademas requiere estar logueado, sino te manda al registro"""
    characters= Character.objects.all()
    context = {"characters": characters}
    return render(request, "characters/characters.html", context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_character(request, id):
    """Esta vista retorna un delete del personaje que seleccionaste, 
    ademas requiere estar logueado y ser admin para acceder, sino te manda al registro"""
    if request.method == 'GET':
        character = Character.objects.get(id=id)
        context = {'character':character}
        return render(request, 'characters/delete_character.html',context=context)
    elif request.method == 'POST':
        character = Character.objects.get(id=id)
        character.delete()
        return redirect(characters)


@user_passes_test(lambda u: u.is_superuser)
def update_character(request, id):
    """Esta vista retorna un update del personaje que seleccionaste, 
    ademas requiere estar logueado y ser admin para acceder, sino te manda al registro"""
    if request.method == 'POST':
        form = FormularioCharacters(request.POST)
        if form.is_valid():
            character = Character.objects.get(id=id)
            character.name = form.cleaned_data['name']
            character.description = form.cleaned_data['description']
            character.alineamiento = form.cleaned_data['alineamiento']
            character.age = form.cleaned_data['age']
            character.clase = form.cleaned_data['clase']
            character.lvl = form.cleaned_data['lvl']
            character.image = form.cleaned_data["image"]
            character.save()
            return redirect(characters)


    elif request.method == 'GET':
        character = Character.objects.get(id=id)

        form = FormularioCharacters(initial={
                                    'name':character.name,
                                    'description':character.description,
                                    'alineamiento':character.alineamiento, 
                                    'clase':character.clase,
                                    'age':character.age,
                                    'lvl':character.lvl})
        context = {'form':form}
        return render(request, 'characters/update_character.html', context=context)