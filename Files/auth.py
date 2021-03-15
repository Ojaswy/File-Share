import os

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


class AuthForm(forms.Form):  # Auth form
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Username",
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
        required=True,
    )
    redirecturl = forms.CharField(
        label="redirecturl",
        required=False,
        widget=forms.HiddenInput(),
    )


def logoutUser(request):
    logout(request)  # Log out the user
    return HttpResponseRedirect(os.getenv("HOSTNAME") + "/files/login")  # Redirect back to login page


def loginUser(request):
    if request.user.is_authenticated:  # Checks if they are authenticated
        redirectUrl = request.GET.get('redirect')  # Sees if a redirect url has been specified
        try:
            return HttpResponseRedirect(os.getenv("HOSTNAME") + "/" + redirectUrl)  # Tries to redirect
        except TypeError:
            return HttpResponseRedirect(os.getenv("HOSTNAME"))  # Fallback to homepage
    else:
        if request.method == "POST":  # If the user is submitting the form
            form = AuthForm(request.POST)  # Bind the form
            if form.is_valid:
                user = authenticate(  # Try and auth the user
                    request,
                    username=form.data["username"],
                    password=form.data["password"],
                )
                if user is not None:  # If they username and password is correct
                    login(request, user)  # Log in the user
                    redirectUrl = form.data['redirecturl']  # Try to get the redirect url
                    try:
                        return HttpResponseRedirect(os.getenv("HOSTNAME") + "/" + redirectUrl)  # Redirects to url
                    except TypeError:
                        return HttpResponseRedirect(os.getenv("HOSTNAME"))  # Fallback to homepage
                else:
                    redirectUrl = ''
                    errormessage = "The username or password you entered is incorrect."  # Sets error message
        elif request.method == "GET":
            errorcode = request.GET.get('errorcode')  # Gets error code querystring
            if errorcode == "0":  # Usually comes from dashboard when not logged in
                errormessage = "You need to be authenticated to view that page, please login."
            elif errorcode == "1":  # From private paste when user isn't authenticated
                errormessage = "That is a private paste, if you have access, please login."
            else:
                errormessage = ""

            form = AuthForm()  # Get form
        return render(request, "auth.html", {"form": form, "hostname": os.getenv("HOSTNAME"), "request": request,
                                             'errormessage': errormessage})  # Render page
