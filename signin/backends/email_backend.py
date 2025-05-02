import ssl

from django.core.mail.backends.base import BaseEmailBackend as SMTBackend
from django.utils.functional import cached_property


class EmailBackend(SMTBackend):
    @cached_property
    def connection(self):
        if self.ssl_certfile or self.ssl_keyfile:
            context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
            return smtplib.SMTP(self.host, self.port, **self.connection_params, context=context)
        else:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            return smtplib.SMTP(self.host, self.port, **self.connection_params, context=context)