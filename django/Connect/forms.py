from django import forms

from Connect.models import CoreServerConnection


class CoreConnectionForm(forms.Form):
    """Handle connecting to the core server"""

    server_url = forms.CharField(
        label="URL:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "x-bind:value": "server_url",
                "x-model": "server_url",
            }
        ),
    )
    port_number = forms.CharField(
        label="Port number:",
        widget=forms.NumberInput(
            attrs={
                "min": 0,
                "class": "form-control",
                "x-bind:value": "port_number",
                "x-model": "port_number",
            }
        ),
    )


class CoreManagerLoginForm(forms.Form):
    """Handle login details for the classic manager account"""

    password = forms.CharField(
        label="Password:", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
