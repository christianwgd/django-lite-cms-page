from django.http import Http404

from lite_cms_core.models import PreventUnpublishedAccessDetailView
from lite_cms_page.models import Page


class PageDetailView(PreventUnpublishedAccessDetailView):
    model = Page

    def dispatch(self, request, *args, **kwargs):
        page = self.get_object()
        if not page.allowed(self.request.user):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        template = 'lite_cms_page/page_detail.html'
        if self.object.template is not None:
            template = self.object.template
        template_name = self.kwargs.get('template', None)
        if template_name is not None:
            template = f'lite_cms_page/page_{template_name}.html'
        return template
