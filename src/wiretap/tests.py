from django.core.exceptions import MiddlewareNotUsed
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from wiretap.middleware import WiretapMiddleware
from wiretap.models import Message, Tap

class WiretapTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    @override_settings(DEBUG=True)
    def test_enabled_if_debugging(self):
        WiretapMiddleware()

    @override_settings(DEBUG=False)
    def test_disabled_if_not_debugging(self):
        with self.assertRaises(MiddlewareNotUsed):
            WiretapMiddleware()

    @override_settings(DEBUG=True)
    def test_no_taps(self):
        self.assertEqual(Tap.objects.count(), 0)
        WiretapMiddleware().process_request(self.request_factory.get('/'))
        self.assertEqual(Message.objects.count(), 0)

    @override_settings(DEBUG=True)
    def test_tap_match(self):
        Tap.objects.create(path_regex='/test')
        WiretapMiddleware().process_request(self.request_factory.get('/test'))
        self.assertEqual(Message.objects.count(), 1)

    @override_settings(DEBUG=True)
    def test_tap_mismatch(self):
        Tap.objects.create(path_regex='/test')
        WiretapMiddleware().process_request(self.request_factory.get('/real'))
        self.assertEqual(Message.objects.count(), 0)
