from django.shortcuts import render

import Files.auth
import Files.dashboard
import Files.formupload
import Files.renderfile


# Create your views here.
def index(request):
    return Files.formupload.uploadText(request)


def File(request, filename):
    return Files.renderfile.renderFile(request, filename)


def dashboard(request):
    return Files.dashboard.dash(request)


def auth(request):
    return Files.auth.loginUser(request)

def logout(request):
    return Files.auth.logoutUser(request)
