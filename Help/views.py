from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.text import slugify
from django.views.generic.base import View

from Account.models import ClientEnquiryMessage, EnquiryMessageSujet
from Help.forms import EnquiryMessageForm
from StandardApps.models import Produits


def HelpSingleTopic(request):
    return render(request, 'help-single-topic.html')


class HelpSubmitRequest(View):
    def get(self, *args, **kwargs):
        global user
        if self.request.user.is_authenticated:
            user = self.request.user
        form = EnquiryMessageForm()
        enquiry_sujet = EnquiryMessageSujet.objects.all()
        context = {
            'form': form,
            'enquiry_sujet': enquiry_sujet,
            'user': user
        }
        return render(self.request, 'help-submit-request.html', context)

    def post(self, *args, **kwargs):
        form = EnquiryMessageForm(self.request.POST or None, self.request.FILES)
        if form.is_valid():
            type_sujet = self.request.POST.get("type_sujet")
            enquiry_sujet = EnquiryMessageSujet.objects.get(sujet=type_sujet)
            print(enquiry_sujet)
            sujet = form.cleaned_data.get("sujet")
            slugify_sujet = slugify(sujet)
            message = form.cleaned_data.get("message")
            nom = self.request.POST.get("nom")
            print(nom)
            email = self.request.POST.get("email")
            print(email)
            url = form.cleaned_data.get("url")
            image = form.cleaned_data.get("image")

            enquiry_message = ClientEnquiryMessage(
                slug=slugify_sujet,
                enquirySujet=enquiry_sujet,
                sujet=sujet,
                message=message,
                email=email,
                nom=nom,
                url=url,
                imageMessage=image
            )
            enquiry_message.save()
            messages.info(self.request, 'Message envoyé avec succès', extra_tags="success")
            return HttpResponseRedirect(self.request.META["HTTP_REFERER"])


def HelpTopics(request):
    return render(request, 'help-topics.html')


def centre_aide_question(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        ask_search = request.GET.get("ask_qs")
        if len(ask_search) > 0:
            qs_search = EnquiryMessageSujet.objects.filter(
                sujet__icontains=ask_search
            )
            context = {
                'qs_search': qs_search,
                'ask_search':ask_search
            }
            print("This is the result of the search", qs_search)

    return render(request, "help-topics-search-question.html", context)