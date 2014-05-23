#coding:utf-8
from django.shortcuts import render
from django.http.response import (
    HttpResponseRedirect, HttpResponse)
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.template import RequestContext
from django.utils.translation import ugettext as _
from MyUser.forms import RegisterForm, SettingForm
from MyUser.models import MyUser
from dianying import conf


def register(request):
    #dic = {'form': RegisterForm}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                                              username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password1']
            )
            #login site
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return HttpResponseRedirect(reverse('nj:index'))
        return render_to_response('register.html', {"form": form}, context_instance=RequestContext(request))
    return render_to_response('register.html', context_instance=RequestContext(request))


def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return render_to_response(
                'index.html',
                {"error": _("Login fails, check whether the user name or password error")},
                context_instance=RequestContext(request)
                )
    return HttpResponseRedirect(reverse("nj:index"))


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html', {"refresh_url": "/"}, context_instance=RequestContext(request))


def setting(request):
    if request.user.is_authenticated():
        #必须是登入用户
        if request.method == 'GET':
            return render_to_response(
                    'user-setting.html',
                    {
                        "movies_week": conf.hot10_week,
                        "movies_mouth": conf.hot10_mouth,
                        "user": request.user
                    },
                    context_instance=RequestContext(request)
            )
        else:
            is_success = ""
            form = SettingForm(request.POST, request.FILES)
            form.user = request.user
            if form.is_valid():
                username = form.cleaned_data.get('username', "")
                if username:
                    request.user.username = username
                    request.user.save()
                email = form.cleaned_data.get('email', "")
                if email:
                    request.user.email = email
                old_password = form.cleaned_data.get('old_password', "")
                if old_password:
                    password = form.cleaned_data.get('password1', "")
                    if password:
                        request.user.set_password(password)
                try:
                    f = request.FILES['file']
                    if f:
                        #conf.handle_uploaded_file(f)
                        request.user.image = f
                except:
                    pass
                is_success = "修改成功"
                request.user.save()
                #return HttpResponseRedirect(reverse("nj:index"))
            return render_to_response(
                'user-setting.html',
                {
                    "movies_week": conf.hot10_week,
                    "movies_mouth": conf.hot10_mouth,
                    "form": form,
                    "user": request.user,
                    "success": is_success,
                },
                context_instance=RequestContext(request)
            )
    return render_to_response('error.html', {"error_message": "请重新登入后再操作。。。"}, context_instance=RequestContext(request))


def reset_confirm(request, uidb64=None, token=None):
    """通过邮箱重设密码验证"""
    return password_reset_confirm(request, template_name='reset-password-confirm.html',
                                  uidb64=uidb64, token=token, post_reset_redirect=reverse('MyUser:login'))


def reset_password(request):
    """通过邮箱重设密码"""
    return password_reset(
        request, template_name='reset-password.html',
        email_template_name='reset-password-email.html',
        subject_template_name='reset-password-subject.txt',
        post_reset_redirect=reverse('MyUser:login')
    )


