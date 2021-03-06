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
from MyUser.forms import RegisterForm, SettingForm, LoginForm
from MyUser.models import MyUser
from dianying import conf
from nanjing.models import Hot10


def register(request):
    #dic = {'form': RegisterForm}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                                              username=form.cleaned_data['username'],
                                              password=form.cleaned_data['password1'],
            )
            #login site
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return HttpResponseRedirect(reverse('nj:index'))
        return render_to_response('register.html', {"form": form}, context_instance=RequestContext(request))
    return render_to_response('register.html', context_instance=RequestContext(request))


HTTP_REFERER = ''


def login(request):
    if request.method == "POST":
        #username = request.POST.get('username', '')
        #password = request.POST.get('password', '')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(HTTP_REFERER)
            else:
                return render(request, 'login.html', {'form': form})
    elif request.method == 'GET':
        form = LoginForm()
        global HTTP_REFERER
        HTTP_REFERER = request.META['HTTP_REFERER']
        return render(request, 'login.html', {'form': form})
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
                    "title": "用户设置",
                    "movies_week":  conf.hot10_week,
                    "movies_month": conf.hot10_month,
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

                is_success = "—修改成功"
                f = request.FILES.get('file', '')
                suffix = f.name.split('.')[-1]
                if f and f.size < 512000 and suffix in ['png', 'jpg', 'gif']:
                    request.user.image.delete(request.user.username+'.'+suffix)
                    request.user.image.save(request.user.username+'.'+suffix, f)
                elif f:
                    is_success = "—头像更新失败"
                request.user.save()
                #return HttpResponseRedirect(reverse("MyUser:setting"))
            return render_to_response(
                'user-setting.html',
                {
                    "title": "用户设置",
                    "form": form,
                    "success": is_success,
                    "user": request.user,
                    "movies_week":  conf.hot10_week,
                    "movies_month": conf.hot10_month,
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
        request,
        template_name='reset-password.html',
        email_template_name='reset-password-email.html',
        subject_template_name='reset-password-subject.txt',
        post_reset_redirect=reverse('MyUser:login')
    )


