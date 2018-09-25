from django import forms
from .models import Profile, Project, Summary, Past, Future, Elevator
from .models import Problem, Solution, BusinessModel, Assumption
from .models import Comment, File

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'created_at', 'updated_at']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['user', 'created_at', 'updated_at']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

    first_name = forms.CharField(max_length=90)
    last_name = forms.CharField(max_length=90)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at', 'slug', 'status']


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


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ['created_at', 'updated_at', 'user', 'project']


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        exclude = ['created_at', 'updated_at', 'user', 'project']


class BusinessModelForm(forms.ModelForm):
    class Meta:
        model = BusinessModel
        exclude = ['created_at', 'updated_at', 'user', 'project']

class AssumptionForm(forms.ModelForm):
    class Meta:
        model = Assumption
        exclude = ['created_at', 'updated_at', 'user', 'project']
