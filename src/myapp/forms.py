from django import forms
from .models import Profile, Project, Summary, Past, Future, Elevator
from .models import Primary, Secondary, Empathy, Assumption, Objective
from .models import Comment, File, Dvf, Link, Invite, Wallet, Billing
from django.utils.translation import ugettext_lazy as _

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        exclude = [
            'user',
            'status',
            'created_at',
            'updated_at',
            ]

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        labels = {
            'period': _('Period (ie: 1Q18)'),
            'amount_budget': _('Budget ($ Thousands)'),
            'amount_actual': _('Actual ($ Thousands)'),
        }
        exclude = ['user', 'created_at', 'updated_at', 'project']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'created_at', 'updated_at']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['user', 'created_at', 'updated_at']


class DvfForm(forms.ModelForm):
    class Meta:
        model = Dvf
        exclude = ['created_at', 'updated_at', 'user', 'project']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

    first_name = forms.CharField(max_length=90)
    last_name = forms.CharField(max_length=90)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at', 'slug', 'user']

class ProjectFormCreate(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at', 'slug', 'user', 'status']


class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        exclude = ['created_at', 'updated_at', 'user', 'project']


class PastForm(forms.ModelForm):
    class Meta:
        model = Past
        exclude = ['created_at', 'updated_at', 'user', 'project']


class FutureForm(forms.ModelForm):
    class Meta:
        model = Future
        exclude = ['created_at', 'updated_at', 'user', 'project']


class ElevatorForm(forms.ModelForm):
    class Meta:
        model = Elevator
        exclude = ['created_at', 'updated_at', 'user', 'project']


class PrimaryForm(forms.ModelForm):
    class Meta:
        model = Primary
        exclude = ['created_at', 'updated_at', 'user', 'project']


class SecondaryForm(forms.ModelForm):
    class Meta:
        model = Secondary
        exclude = ['created_at', 'updated_at', 'user', 'project']


class EmpathyForm(forms.ModelForm):
    class Meta:
        model = Empathy
        exclude = ['created_at', 'updated_at', 'user', 'project']

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        labels = {
            'dvf': _('Stage'),
            'value': _('Objective'),
            'metric': _('Evidence'),
        }
        exclude = ['created_at', 'updated_at', 'user', 'project']

class AssumptionForm(forms.ModelForm):
    class Meta:
        model = Assumption
        labels = {
            'objective_id': _('Objective ID'),
            'assumption': _('What to Test'),
            'metric': _('How to Test'),
            'uncertainty': _('How Uncertain'),
            'critical': _('How Critical'),
        }
        exclude = ['created_at', 'updated_at', 'user', 'project']

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['created_at', 'updated_at', 'user', 'project']

class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ['email', 'permission']
