import os.path
import random
from os import path

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Files.models import File


def randomstring():
    random_string = ""
    for _ in range(30):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += chr(random_integer)
    return random_string


class TextForm(forms.Form): # Text upload form
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": "5", "cols": "100"}
        ),
        label="Text",
        required=True,
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Description",
        required=True,
    )
    visibilityChoices = (
        ("unlisted", "Unlisted"),
        ("private", "Private"),
    )
    visibility = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=visibilityChoices,
        label="Visibility",
        required=True,
    )


def uploadText(request):
    if request.method == "POST": # Checks if the form is being submitted
        form = TextForm(request.POST) # Gets the form data
        if form.is_valid: # Checks if its valid
            filename = randomstring() # Gets a random string
            baseName = "Files/Uploads/"
            while path.exists(baseName + filename): # Makes sure the file doesn't already exist
                filename = randomstring()
            tempFile = open(baseName + filename, "w") # Opens the file
            tempFile.write(form.data["text"]) # Writes the text to the file
            tempFile.close() # Closes the file
            if request.user.is_authenticated: # If the user is authenticated also save the user id to the database for the dashboard
                fileDB = File(
                    name=filename,
                    type="text",
                    location=baseName + filename,
                    description=form.data["description"],
                    belongsto=request.user.id,
                    visibility=form.data["visibility"],
                )
            else: # If not don't save the userid
                fileDB = File(
                    name=filename,
                    type="text",
                    location=baseName + filename,
                    description=form.data["description"],
                    visibility='unlisted',
                )
            fileDB.save()  # Save the database entry
            if not request.user.is_authenticated and form.data['visibility'] == 'private': # If the user isn't implemented tell the user that their paste was made public
                return HttpResponseRedirect("/files/f/" + filename + "?errorCode=1")
            else: # If they are leave it
                return HttpResponseRedirect("/files/f/" + filename)
    elif request.method == "GET": # If the request is GET simply render the form
        form = TextForm()
    return render(request, "text.html", {"form": form, "hostname": os.getenv("HOSTNAME"), "request": request}) # Render the page
