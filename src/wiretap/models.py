from django.db import models
from jsonfield import JSONField

class _NotSet(object):
    pass

class Tap(models.Model):
    path_regex = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.path_regex

class Message(models.Model):
    started_at = models.DateTimeField(db_index=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    remote_addr = models.CharField(max_length=39, db_index=True)

    req_method = models.CharField(max_length=16)
    req_path = models.TextField()
    req_headers = JSONField()
    req_body = models.FileField(blank=True, null=True, upload_to='message/%Y/%m/%d')

    res_status_code = models.PositiveIntegerField(blank=True, null=True)
    res_reason_phrase = models.CharField(max_length=64)
    res_headers = JSONField(blank=True)
    res_body = models.FileField(blank=True, null=True, upload_to='message/%Y/%m/%d')

    @property
    def duration(self):
        if self.ended_at is None:
            return None
        else:
            return (self.ended_at - self.started_at).total_seconds

    def get_req_header(self, key, default=_NotSet):
        return self._get_header(self.req_headers, key, default)

    def get_res_header(self, key, default=_NotSet):
        return self._get_header(self.res_headers, key, default)

    def _get_header(self, headers, search_key, default):
        search_key = search_key.title()
        try:
            return next(
                value
                for (key, value) in headers
                if key == search_key
            )
        except StopIteration:
            if default is _NotSet:
                raise KeyError(search_key)
            else:
                return default

    def __unicode__(self):
        return u'{} {}'.format(self.req_method, self.req_path.encode('ascii', 'ignore'))
