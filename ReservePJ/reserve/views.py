from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, resolve_url
from django.template.loader import render_to_string
from django.views import generic
from django.urls import reverse_lazy
from .forms import *
from .models import *
from register.views import *

#class ReserveSeats(generic.CreateView):
#    """ユーザー情報更新"""
#   model = Reserve
#    form_class = ReserveForm
#    template_name = 'reserve/reserve_seats.html'
