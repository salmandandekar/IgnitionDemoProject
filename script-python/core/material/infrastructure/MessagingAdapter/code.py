"""Messaging adapter bridging to configured event transport and logging."""

from adapters.messaging import MessageRouter as router
from common.logging.LogFactory import code as LogFactory

_LOG = LogFactory.get_logger("MaterialMessaging")


class Messenger(object):
    def publish(self, envelope):
        try:
            topic = envelope.get("noun", "event") if isinstance(envelope, dict) else "event"
            return router.publish(topic, envelope)
        except Exception as exc:
            _LOG.error("Failed to publish material event: %s" % exc)
            return None

    def info(self, message, **kwargs):
        try:
            _LOG.info("%s | %s" % (message, kwargs))
        except Exception:
            pass

    def warning(self, message, **kwargs):
        try:
            _LOG.warn("%s | %s" % (message, kwargs))
        except Exception:
            pass

    def error(self, message, exc=None, **kwargs):
        try:
            detail = "%s | %s" % (message, kwargs)
            if exc:
                detail = "%s | %s" % (detail, exc)
            _LOG.error(detail)
        except Exception:
            pass


def get_messenger():
    return Messenger()
