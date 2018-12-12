from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'created_at', 'updated_at']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'created_at', 'updated_at']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['user', 'created_at', 'updated_at']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['user', 'created_at', 'updated_at']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']

    first_name = forms.CharField(max_length=90)
    last_name = forms.CharField(max_length=90)

    EVENTS = (
        ('Boston', 'Boston'),
        ('Chicago', 'Chicago'),
        ('Los Angeles', 'Los Angeles'),
        ('New York', 'New York'),
        ('San Francisco Bay Area', 'San Francisco Bay Area'),
        ('Seattle', 'Seattle'),
        ('Toronto', 'Toronto'),
        ('Other', 'Other'),
        )

    ACTIVITIES = (
        ('Accounting/Bookkeeping', 'Accounting/Bookkeeping'),
        ('Brand', 'Brand'),
        ('Business Development', 'Business Development'),
        ('Content', 'Content'),
        ('Corporate Development', 'Corporate Development'),
        ('CRM/Network Management', 'CRM/Network Management'),
        ('Data Science', 'Data Science'),
        ('Deal Diligence', 'Deal Diligence'),
        ('Deal Sourcing', 'Deal Sourcing'),
        ('Events', 'Events'),
        ('Engineering', 'Engineering'),
        ('Financial Forecasting', 'Financial Forecasting'),
        ('Fundraising', 'Fundraising'),
        ('Investor Relations', 'Investor Relations'),
        ('PR', 'PR'),
        ('Product Design/UXUI', 'Product Design/UXUI'),
        ('Resources/Service Providers', 'Resources/Service Providers'),
        ('Sales Operations', 'Sales Operations'),
        ('Talent/Recruiting', 'Talent/Recruiting'),
        )


    MENTORSHIP = (
        ('Mentor', 'Mentor'),
        ('Mentee', 'Mentee'),
        )

    events = forms.MultipleChoiceField(choices=EVENTS, required=False)
    activities = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=ACTIVITIES)
    mentorship = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=MENTORSHIP, required=False)
    moderator= forms.BooleanField(widget= forms.CheckboxInput(attrs={'id':'toggleTwo'}), required=False)
    panel= forms.BooleanField(widget= forms.CheckboxInput(attrs={'id':'toggleOne'}), required=False)

    def events_labels(self):
        return [label for value, label in self.fields['events'].choices if value in self['events'].value()]

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ['user', 'created_at', 'updated_at']

    CATEGORIES = (
        ('Accounting', 'Accounting'),
        ('Events', 'Events'),
        ('Legal', 'Legal'),
        ('Marketing', 'Marketing'),
        ('Web Development', 'Web Development'),
        )

    categories = forms.MultipleChoiceField(choices=CATEGORIES)
