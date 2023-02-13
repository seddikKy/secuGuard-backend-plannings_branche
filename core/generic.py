from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView, TemplateView
from django.views.generic.base import ContextMixin

from django.db import models
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin


class SListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    pass


class SDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    pass


class SCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            if e.params and e.params.get('field'):
                form.add_error(e.params.get('field'), e.message)
            else:
                messages.error(self.request, e.message)
            return self.render_to_response(self.get_context_data(form=form))


class SUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    pass


class SDeleteView(DeleteView):
    pass


class STemplateView(TemplateView):
    pass


class ParentObjectMixin(ContextMixin):
    """
    Provide the ability to retrieve a single object for further manipulation.
    """
    parent_model = None
    parent_pk_url_kwarg = 'parent_pk'

    def get_parent_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.parent_model._default_manager.all()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.parent_pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # If none of those are defined, it's an error.
        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_parent_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {'parent_object': self.get_parent_object()}
        context.update(kwargs)
        return super().get_context_data(**context)


class SParentDetailChildListView(ParentObjectMixin, SListView):
    """
    Master detail generic view
    """
    parent_field = 'parent'  # Child foreign key for parent model

    def get_queryset(self):
        return super().get_queryset().filter(**{self.parent_field: self.get_parent_object()})

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context.update(self.get_parent_context_data())
        return context


class SParentDetailChildCreateView(ParentObjectMixin, SCreateView):
    """
    Master detail generic view
    """
    parent_field = 'parent'  # Child foreign key for parent model

    def get_queryset(self):
        return super().get_queryset().filter(**{self.parent_field: self.get_parent_object()})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_parent_context_data())
        return context


class SParentDetailChildUpdateView(ParentObjectMixin, SUpdateView):
    """
    Master detail generic view
    """
    parent_field = 'parent'  # Child foreign key for parent model

    def get_queryset(self):
        return super().get_queryset().filter(**{self.parent_field: self.get_parent_object()})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_parent_context_data())
        return context


class SParentDetailChildDeleteView(ParentObjectMixin, SDeleteView):
    """
    Master detail generic view
    """
    parent_field = 'parent'  # Child foreign key for parent model

    def get_queryset(self):
        return super().get_queryset().filter(**{self.parent_field: self.get_parent_object()})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_parent_context_data())
        return context


class SParentDetailChildDetailView(ParentObjectMixin, SDetailView):
    """
    Master detail generic view
    """
    parent_field = 'parent'  # Child foreign key for parent model

    def get_queryset(self):
        return super().get_queryset().filter(**{self.parent_field: self.get_parent_object()})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_parent_context_data())
        return context


class DoActionMixin:
    """Provide the ability to do actions on objects."""
    success_url = None
    action = ''
    action_name = 'Not Set'

    def do_action(self, request, *args, **kwargs):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        print('posted')
        return self.do_action(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseDoActionView(DoActionMixin, BaseDetailView):
    """
    Base view for confirming an object.

    Using this base class requires subclassing to provide a response mixin.
    """


class SDoActionView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, SingleObjectTemplateResponseMixin,
                    BaseDoActionView):
    """
    View for deleting an object retrieved with self.get_object(), with a
    response rendered by a template.
    """
    template_name = ''
    login_url = reverse_lazy('app_login')
    success_url = None
    success_message = ""

    def do_action(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.do_action(action=self.action, user=request.user)
            messages.success(request, self.success_message)
            success_url = self.get_success_url()
            print('action done')
            print(request.POST.get('action'))

            return HttpResponseRedirect(success_url)
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return render(request, self.template_name, self.get_context_data())

    def get_permission_required(self):
        perm_required = f'{self.model._meta.app_label}.{self.action}_{self.model._meta.model_name}'
        return (perm_required,)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_name'] = self.action_name
        context['action'] = self.action
        return context
