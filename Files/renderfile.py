import os

from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render

from Files.models import File


def error404(request): # Returns 404 page
    return render(request, "404.html", {"hostname": os.getenv("HOSTNAME"), "request": request})


def renderText(filename, request, errormessage, viewBecauseStaff, description):
    try:
        text = open(os.getenv("BASE_PATH") + r"Files\Uploads\\" + filename)
        return render(request, "rendertext.html",
                      {"text": text.read(), "hostname": os.getenv("HOSTNAME"), "request": request,
                       "errormessage": errormessage, 'viewBecauseStaff': viewBecauseStaff, 'description': description})
    except FileNotFoundError:
        return error404(request)


def renderFile(request, filename):
    showCopyUrl = True
    file = File.objects.filter(name=filename)  # Gets the file from the db
    if len(file) == 0: # Checks if 0 entries were returned (file isn't in db)
        return error404(request)
    description = file[0].description
    errorCode = request.GET.get('errorcode')  # Gets the error code (if any)
    if errorCode == "1":  # Happens when user is authenticated but wants a private paste
        errormessage = "You asked us to make a private paste, but since you're not logged in, we had to make it " \
                       "unlisted "
    else:
        errormessage = ""
    if file[0].visibility == 'private':  # If the paste is private we need to make some more checks
        if not file[0].belongsto == 0:  # Checks if the file belongs to user id 0 which is an unauthed user
            if request.user.is_authenticated:  # Check if they are logged into and account
                if file[0].belongsto == request.user.id or request.user.is_staff:  # Checks if the user is the owner of the file OR staff
                    if not file[0].belongsto == request.user.id and request.user.is_staff:  # If the it doesn't belong to the user but they are staff
                        viewBecauseStaff = True
                    else:
                        viewBecauseStaff = False
                    return renderText(filename, request, errormessage, viewBecauseStaff, description)
                else:
                    return render(request, "forbidden.html", status=403)  # Redirect user as they don't have access
            else:
                return HttpResponseRedirect(os.getenv("HOSTNAME") + "/files/login?redirect=files/f/" + filename + "&errorcode=1")  # User isn't logged in, redirect them to the login page
    elif file[0].visibility == 'unlisted': # Unlisted file, anyone can access with link
        return renderText(filename, request, errormessage, False, description)
    else: # If the visibility for some reason is different simply 404 error and log the error
        print('Visibility not unlisted or private')
        return error404(request)
