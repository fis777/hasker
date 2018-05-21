""" views"""
from django.views import generic
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageUploadForm, UserForm, UserSettingsForm, ProfileForm, QuestionsForm, AnswerForm, AddUserForm, LoginUser
from .models import Question, Answer, Profile

class QuestionsList(generic.ListView):
    """docstring for QuestionsList"""
    template_name = "questions_list.html"
    context_object_name = 'q_list'

    def get_queryset(self):
        return Question.objects.order_by('reg_date')[:20]

class AnswerView(generic.DetailView):
    model = Question
    template_name = 'answer.html'

class QuestionCreate(CreateView):
    """docstring for QuestionCreate"""
    form_class = QuestionForm
    model = Question
    template_name = 'question_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(QuestionCreate, self).form_valid(form)

def log_out(request):
    logout(request)
    return redirect('/')

def log_in(request):
    """ default list """
    if request.method == 'POST':
        login_form = LoginUser(request.POST)
        if login_form.is_valid ():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active :
                    login(request, user)
                    return redirect('/')
    else:
        login_form = LoginUser()
    return render(request, "log_in.html", {'login_form': login_form})


def user_create(request):
    if request.method == 'POST':
        adduser_form = AddUserForm(request.POST)
        image_form = ImageUploadForm(request.POST, request.FILES)
        if adduser_form.is_valid() and image_form.is_valid():
            username = adduser_form.cleaned_data['nickname']
            email = adduser_form.cleaned_data['email']
            password = adduser_form.cleaned_data['password']
            confirm_password = adduser_form.cleaned_data['confirm_password']
            if password == confirm_password and User.objects.filter(username=username).count() == 0:
                user = User.objects.create_user(username, email=email, password=password)
                user.save()
                profile = Profile.objects.get(user=user)
                profile.avatar = image_form.cleaned_data['image']
                profile.save()
                return redirect('/')
    else:
        adduser_form = AddUserForm()
        image_form = ImageUploadForm()
    return render(request, 'user_settings.html', {
        'user_form': adduser_form,
        'image_form': image_form,
    })

def user_setting(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=user)
        image_form = ImageUploadForm(request.POST, request.FILES)
        if user_form.is_valid() and image_form.is_valid():
            user_form.save()
            profile.avatar = image_form.cleaned_data['image']
            profile.save()
            return redirect('/')
    else:
        image_form = ImageUploadForm()
        user_form = UserSettingsForm(instance=user)
    return render(request, 'user_setting.html', {'user_form': user_form, 'image_form': image_form, 'user': user, 'profile': profile})

def q_and_a(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=pk)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.instance.question = question
            answer_form.save()
            answers = Answer.objects.filter(question=pk)
    else:
        answer_form = AnswerForm(request.POST)
    return render(request, 'q_and_a.html', {
        'question':question,
        'answers': answers,
        'answer_form': answer_form
        })

def QuestList(request):
    questions = Question.objects.all()
    return render(request, 'quest_user.html', {'questions': questions})
