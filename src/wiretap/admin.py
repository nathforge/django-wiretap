from django.contrib import admin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from roma import ReadOnlyModelAdmin

from wiretap.models import Message, Tap

class TapAdmin(admin.ModelAdmin):
    list_display = ('path_regex',)

class MessageAdmin(ReadOnlyModelAdmin):
    list_display = ('request', 'response', 'remote_addr', 'started_at', 'duration',)
    list_filter = ('started_at', 'req_method', 'res_status_code',)
    search_fields = ('remote_addr', 'req_path',)

    def request(self, obj):
        return unicode(obj)
    request.admin_order_field = 'req_path'

    def response(self, obj):
        if obj.res_status_code is not None:
            return '{} {}'.format(
                obj.res_status_code,
                obj.res_reason_phrase.encode('ascii', 'ignore')
            )
        else:
            return ''
    response.admin_order_field = 'res_status_code'

    def get_urls(self):
        from django.conf.urls import patterns, url

        return patterns('',
            url(
                r'^(?P<pk>\d+)/req-body/$',
                self.admin_site.admin_view(self.body_view),
                kwargs={
                    'field_name': 'req_body',
                    'get_header_name': 'get_req_header'
                }
            ),
            url(
                r'^(?P<pk>\d+)/res-body/$',
                self.admin_site.admin_view(self.body_view),
                kwargs={
                    'field_name': 'res_body',
                    'get_header_name': 'get_res_header'
                }
            )
        ) + super(MessageAdmin, self).get_urls()

    def body_view(self, request, pk, field_name, get_header_name):
        message = get_object_or_404(Message, id=pk)

        value = getattr(message, field_name)
        if not value:
            raise Http404()

        value.open()

        get_header = getattr(message, get_header_name)
        content_type = get_header('Content-Type', 'text/plain; charset=us-ascii')

        return HttpResponse(value.read(), content_type=content_type)

admin.site.register(Tap, TapAdmin)
admin.site.register(Message, MessageAdmin)
