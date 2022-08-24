from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
    CHARACTERS,
    Campaign, Character, CharacterClass,
    Background,
    TheBlessed,
)
from .forms import (
    CreateCampaignForm, CreateCharacterForm,
    CreateTheBlessedForm,

)

class CreateCampaignView(LoginRequiredMixin, CreateView):
    """
    Allows the GM of the campaign to create a campaign.
    """
    template_name = 'campaign/create_campaign.html'
    form_class = CreateCampaignForm
    model = Campaign
    success_url = reverse_lazy('create-campaign')
    login_url = reverse_lazy('login')


    def form_valid(self, form):
        form.instance.GM = self.request.user
        return super().form_valid(form)
    

class CampaignListView(ListView):
    """
    List of all the campaigns created.
    """
    template_name = 'campaign/campaign_list.html'
    model = Campaign
    context_object_name = 'campaigns'


class CampaignDetailView(LoginRequiredMixin, DetailView):
    """
    Gives an in-depth outline of the the campaign and all the characters in the campaign.
    """
    template_name = 'campaign/campaign_detail.html'
    model = Campaign
    context_object_name = 'campaign'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        """
        Add in the current campaign value to the session
        so that the campaign will be automatically selected
        when users go 
        """
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        # Add the current campaign to the session
        campaign = context['campaign']
        campaign_name = campaign.campaign_name
        campaign_id = campaign.id
        self.request.session['current_campaign'] = campaign_name
        self.request.session['current_campaign_id'] = campaign_id
        return context


class ChooseCharacterView(LoginRequiredMixin, ListView):
    """
    View that allows users to create characters in the front end.
    """
    template_name = 'campaign/choose_character.html'
    form_class = CreateCharacterForm
    model = CharacterClass
    context_object_name = 'character_classes'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(ChooseCharacterView, self).get_context_data(**kwargs)
        context['campaign_id'] = self.request.session['current_campaign_id']
        context['campaign_name'] = self.request.session['current_campaign']
        
        return context

    '''
    def get_context_data(self, **kwargs):
        """
        Add in context for various fields in the form
        """
        context = super().get_context_data(**kwargs)
        # Add a queryset of all the character classes
        context['character_classes'] = CharacterClass.objects.all()
        return context
    '''

class CreateTheBlessedView(LoginRequiredMixin, CreateView):
    """
    Creates a character of The Blessed character class.
    """
    login_url = reverse_lazy('login')
    template_name = 'campaign/create_the_blessed.html'
    form_class = CreateTheBlessedForm
    model = TheBlessed
    context_object_name = 'the_blessed'

    def get_context_data(self, **kwargs):
        context = super(CreateTheBlessedView, self).get_context_data(**kwargs)
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.filter(id=campaign_id)
        context['current_campaign'] = current_campaign

        # Add Background class into the context data
        blessed_backgrounds = Background.objects.filter(character_class__class_name=CHARACTERS[0][1])
        context['backgrounds'] = blessed_backgrounds

        return context

    def form_valid(self, form):
        campaign_id = self.request.session['current_campaign_id']
        current_campaign = Campaign.objects.filter(id=campaign_id)
        form.instance.campaign = current_campaign
        form.instance.character_class = CHARACTERS[0][1]
        form.instance.player = self.request.user
        return super().form_valid(form)

    
    