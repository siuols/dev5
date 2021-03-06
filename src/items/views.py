# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	PermissionRequiredMixin
	)

from django.shortcuts import render

from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView
	)

from .forms import ItemCreateForm, ItemClaimForm

from .models import Item

from locations.models import Location

# Create your views here.

class HomeView(ListView):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, "home.html", {})

		query = self.request.GET.get('q')
		item_exists = Item.objects.filter(claimed=False).order_by("-updated")[:10].exists()
		qs = Location.objects.all().order_by("-updated").search(query)

		if item_exists and qs.exists():
			return render(request, "items/home-feed.html", {'object_list':qs})
		return render(request, "items/home-feed.html", {'object_list':qs})

class ClaimedView(LoginRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, "home.html", {})

		query = self.request.GET.get('q')
		item_exists = Item.objects.filter(claimed=True).order_by("-updated")[:10].exists()
		qs = Location.objects.all().order_by("-updated").search(query)

		if item_exists and qs.exists():
			return render(request, "items/claimed.html", {'object_list':qs})
		return render(request, "items/claimed.html", {'object_list':qs})


class ItemListAdminView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
	permission_required = 'items'
	template_name = 'item_lists.html'
	def get_queryset(self):
		return Item.objects.filter(claimed=False).order_by("-updated")

	def get_context_data(self, *args, **kwargs):
		context =super(ItemListAdminView, self).get_context_data(*args, **kwargs)
		
		query = self.request.GET.get('q')
		item_exists = Item.objects.all().exists()
		qs = Location.objects.all().search(query)
		if item_exists and qs.exists():
			context['item'] = qs
		return context

class ItemListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user, claimed=False).order_by("-updated")

	def get_context_data(self, *args, **kwargs):
		context =super(ItemListView, self).get_context_data(*args, **kwargs)
		
		query = self.request.GET.get('q')
		item_exists = Item.objects.all().exists()
		qs = Location.objects.all().search(query)
		if item_exists and qs.exists():
			context['item'] = qs
		return context

class ItemDetailAdminView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
	permission_required = 'items'
	def get_queryset(self):
		return Item.objects.all()

class ItemDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
	form_class = ItemCreateForm
	template_name = 'form.html'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		return super(ItemCreateView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(ItemCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Item'
		return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ItemCreateForm
	template_name = 'items/detail-update.html'
	
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	# context for html title
	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Item'
		return context

	#for user checking if login of not
	#giving data
	def get_form_kwargs(self):
		kwargs = super(ItemUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

class ItemUpdateViewAdmin(LoginRequiredMixin, UpdateView):
	permission_required = 'items'
	form_class = ItemClaimForm
	template_name = 'items/detail-update1.html'

	def get_queryset(self):
		return Item.objects.all()

	# context for html title
	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateViewAdmin, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Item'
		return context

	#for user checking if login of not
	#giving data
	def get_form_kwargs(self):
		kwargs = super(ItemUpdateViewAdmin, self).get_form_kwargs()
		return kwargs