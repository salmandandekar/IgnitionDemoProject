"""Messaging / logging abstraction for the Material bounded context."""


class MaterialMessagingPort(object):
    def publish(self, envelope):
        raise NotImplementedError

    def info(self, message, **kwargs):
        raise NotImplementedError

    def warning(self, message, **kwargs):
        raise NotImplementedError

    def error(self, message, exc=None, **kwargs):
        raise NotImplementedError
