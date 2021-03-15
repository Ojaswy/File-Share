import os

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import Files
from Files.models import File


def index(request): # Index of admin dash, displays basic stats
    if request.user.is_staff:
        numOfFiles = len(File.objects.all()) # Gets the number of pastes and text uploads
        numOfText = len(File.objects.filter(type="text")) # Number of text uploads
        return render(request, "adminindex.html",
                      {"hostname": os.getenv("HOSTNAME"), "request": request, "numOfFiles": numOfFiles,
                       "numOfText": numOfText}) # Renders index page
    elif not request.user.is_authenticated: # User is authenticated but not staff
        return HttpResponseRedirect(os.getenv("HOSTNAME") + "/files/login?redirect=dash&errorcode=0") # Redirect back to login page
    else:
        return HttpResponse(status=404) # If the user isn't authenticated simply show a 404 error


def text(request): # Gets all the text uploads
    if request.user.is_staff: # Makes sure the user is staff
        result = File.objects.filter(type="text") # Gets all the files
        paginator = Paginator(result, 5) # Pageinate
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # result[0].description
        deleted = request.GET.get('deleted')
        return render(request, "textadmin.html",
                      {"entries": result, 'page_obj': page_obj, "hostname": os.getenv("HOSTNAME"), "request": request, "deleted": deleted}) # Render page
    elif not request.user.is_authenticated: # If the user is authenticated but not staff
        return HttpResponseRedirect(os.getenv("HOSTNAME") + "/files/login?redirect=dash&errorcode=0")
    else:
        return HttpResponse(status=404) # If the user isn't authenticated simply display a 404 page


def deletetext(request): # Deleted pastes by id
    if request.user.is_staff: # Checks if user is staff
        fieldid = request.GET.get('id') # Gets the id from querystring
        if fieldid == '': # If the url is blank display error
            return HttpResponse("ID field in URL was blank")
        try: # Try and find the id in database
            object = File.objects.get(id=fieldid)
        except Files.models.File.DoesNotExist: # If it doesn't exist
            return HttpResponse("Could not find item matching id in database") # Display error
        try:
            os.remove(os.getenv("BASE_PATH") + r"Files\Uploads\\" + object.name) # Try and delete the file on disk
        except FileNotFoundError: # If the file can't be found
            object.delete() # Still delete the database entry
            return HttpResponse("Couldn't delete file on disk, deleted database entry") # Return error
        object.delete() # Delete database entry
        redirectpage = request.GET.get('redirectpage')
        if not redirectpage == '':
            return HttpResponseRedirect(os.getenv('HOSTNAME') + '/dash/text?page=' + redirectpage + '&deleted=1')
        else:
            return HttpResponseRedirect(os.getenv('HOSTNAME') + '/dash/text?deleted=1')
    else:
        return HttpResponse(status=404) # If the user isn't staff display a 404 page
