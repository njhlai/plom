from django import forms
from django.shortcuts import render
from django_htmx.http import HttpResponseClientRedirect

from Preparation.services import ClassicPlomServerInformationService
from Base.base_group_views import ManagerRequiredView


class ServerURLForm(forms.Form):
    server_name = forms.CharField()
    server_port = forms.IntegerField()


class ClassicServerURLView(ManagerRequiredView):
    def build_context(self):
        cpsis = ClassicPlomServerInformationService()
        info = cpsis.get_server_info()
        if info["server_name"]:
            form = ServerURLForm(
                {
                    "server_name": info["server_name"],
                    "server_port": info["server_port"],
                }
            )
        else:
            form = ServerURLForm(
                {
                    "server_name": "localhost",
                    "server_port": 49184,
                }
            )

        return {
            "server_name": info["server_name"],
            "server_port": info["server_port"],
            "form": form,
            "navbar_colour": "#AD9CFF",
            "user_group": "manager",
        }

    def get(self, request):
        context = self.build_context()
        return render(request, "Preparation/classic_server_url.html", context)

    def post(self, request):
        dat = request.POST.dict()
        context = self.build_context()
        context["form"] = ServerURLForm(dat)
        return """
        meh
        """
        # return render(request, "Preparation/classic_server_url.html", context)


class ClassicServerInfoView(ManagerRequiredView):
    def build_context(self):
        cpsis = ClassicPlomServerInformationService()
        info = cpsis.get_server_info()

        return {
            "server_name": info["server_name"],
            "server_port": info["server_port"],
            "manager_password": info["server_manager_password"],
            "navbar_colour": "#AD9CFF",
            "user_group": "manager",
        }

    def get(self, request):
        context = self.build_context()
        return render(request, "Preparation/classic_server_manage.html", context)
