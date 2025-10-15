import os
import sys
import unittest
from types import ModuleType

# Ensure project libraries are importable
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Minimal Ignition "system" module stubs used across cross-cutting tests.
# ---------------------------------------------------------------------------
_DB_CALLS = []


def _reset_db_calls():
    del _DB_CALLS[:]


def _beginTransaction(datasource):
    tx = "tx-%s" % datasource
    _DB_CALLS.append(("begin", datasource))
    return tx


def _commitTransaction(tx):
    _DB_CALLS.append(("commit", tx))


def _rollbackTransaction(tx):
    _DB_CALLS.append(("rollback", tx))


def _closeTransaction(tx):
    _DB_CALLS.append(("close", tx))


def _getLogger(name):
    return _DefaultLogger(name)


def _getUserName():
    return "tester"


class _DefaultLogger(object):
    def __init__(self, name):
        self.name = name
        self.records = []

    def info(self, msg):
        self.records.append(("info", msg))

    def warn(self, msg):
        self.records.append(("warn", msg))

    def error(self, msg):
        self.records.append(("error", msg))

    def debug(self, msg):
        self.records.append(("debug", msg))


_USER_ROLES = set()


def _hasRole(role):
    return role in _USER_ROLES


def _install_system_modules():
    system_module = ModuleType("system")
    db_module = ModuleType("system.db")
    db_module.beginTransaction = _beginTransaction
    db_module.commitTransaction = _commitTransaction
    db_module.rollbackTransaction = _rollbackTransaction
    db_module.closeTransaction = _closeTransaction
    db_module._calls = _DB_CALLS
    db_module.reset = _reset_db_calls

    util_module = ModuleType("system.util")
    util_module.getLogger = _getLogger
    util_module.getUserName = _getUserName

    user_module = ModuleType("system.user")
    user_module.hasRole = _hasRole
    user_module._roles = _USER_ROLES

    system_module.db = db_module
    system_module.util = util_module
    system_module.user = user_module

    sys.modules["system"] = system_module
    sys.modules["system.db"] = db_module
    sys.modules["system.util"] = util_module
    sys.modules["system.user"] = user_module


_install_system_modules()

# ---------------------------------------------------------------------------
# Imports of project modules under test.
# ---------------------------------------------------------------------------
from common.cache.CacheManager import code as CacheManager
from common.decorators.CacheDecorator import code as cache_decorator_module
from common.decorators.ExceptionHandlerDecorator import code as exception_decorator_module
from common.decorators.TraceDecorator import code as trace_decorator_module
from common.decorators.TransactionDecorator import code as transaction_decorator_module
from common.security.AccessControl import code as access_control_module
from common.security.CryptoProvider import code as crypto_provider_module
from common.logging.LogFactory import code as log_factory_module
from common.logging.LogFormatter import code as log_formatter_module
from common.context.SessionContext import code as session_context_module
from common.exceptions.MESException import code as mes_exception_module
from common.exceptions.SecurityException import code as security_exception_module


class _TestLogger(object):
    def __init__(self):
        self.records = []

    def info(self, msg):
        self.records.append(("info", msg))

    def warn(self, msg):
        self.records.append(("warn", msg))

    def error(self, msg):
        self.records.append(("error", msg))

    def debug(self, msg):
        self.records.append(("debug", msg))


class CacheManagerTests(unittest.TestCase):
    def tearDown(self):
        CacheManager.invalidate("ttl-cache")
        CacheManager.invalidate("none-cache")

    def test_cache_manager_respects_ttl(self):
        CacheManager.invalidate("ttl-cache")
        current = [1000]
        original_now = CacheManager._now

        def fake_now():
            return current[0]

        CacheManager._now = fake_now
        try:
            CacheManager.put("ttl-cache", "key", "value", ttl_seconds=5)
            self.assertTrue(CacheManager.exists("ttl-cache", "key"))
            current[0] = 1006
            self.assertFalse(CacheManager.exists("ttl-cache", "key"))
            self.assertIsNone(CacheManager.get("ttl-cache", "key"))
        finally:
            CacheManager._now = original_now

    def test_cache_manager_handles_none_values(self):
        CacheManager.invalidate("none-cache")
        CacheManager.put("none-cache", "key", None)
        self.assertTrue(CacheManager.exists("none-cache", "key"))
        self.assertIsNone(CacheManager.get("none-cache", "key"))


class CacheDecoratorTests(unittest.TestCase):
    def tearDown(self):
        CacheManager.invalidate("decorator-cache")
        CacheManager.invalidate("decorator-none")

    def test_cacheable_caches_results(self):
        calls = []

        @cache_decorator_module.cacheable("decorator-cache", lambda value: value)
        def compute(value):
            calls.append(value)
            return value * 2

        self.assertEqual(compute(3), 6)
        self.assertEqual(compute(3), 6)
        self.assertEqual(calls, [3])

    def test_cacheable_caches_none(self):
        calls = []

        @cache_decorator_module.cacheable("decorator-none", lambda: "static")
        def compute():
            calls.append(1)
            return None

        self.assertIsNone(compute())
        self.assertIsNone(compute())
        self.assertEqual(len(calls), 1)


class ExceptionHandlerDecoratorTests(unittest.TestCase):
    def setUp(self):
        self.logger = _TestLogger()
        self.original_get_logger = log_factory_module.get_logger
        log_factory_module.get_logger = lambda name="MES": self.logger

    def tearDown(self):
        log_factory_module.get_logger = self.original_get_logger

    def test_passthrough_mes_exception(self):
        @exception_decorator_module.guarded
        def raises_mes():
            raise mes_exception_module.MESException("boom", code="BAD")

        with self.assertRaises(mes_exception_module.MESException) as ctx:
            raises_mes()
        self.assertEqual(ctx.exception.code, "BAD")
        self.assertTrue(
            any(level == "error" and "MESException" in msg for level, msg in self.logger.records)
        )

    def test_wraps_non_mes_exception(self):
        @exception_decorator_module.guarded
        def raises_value_error():
            raise ValueError("bad stuff")

        with self.assertRaises(mes_exception_module.MESException) as ctx:
            raises_value_error()
        self.assertEqual(ctx.exception.code, "UNHANDLED")
        self.assertEqual(ctx.exception.data.get("type"), "ValueError")
        self.assertTrue(
            any(level == "error" and "UnhandledException" in msg for level, msg in self.logger.records)
        )


class TraceDecoratorTests(unittest.TestCase):
    def setUp(self):
        self.logger = _TestLogger()
        self.original_get_logger = log_factory_module.get_logger
        log_factory_module.get_logger = lambda name="MES": self.logger
        self.original_session_current = session_context_module.current
        session_context_module.current = lambda: {"correlationId": "CID-123"}

    def tearDown(self):
        log_factory_module.get_logger = self.original_get_logger
        session_context_module.current = self.original_session_current

    def test_traced_success_logs_entry_and_exit(self):
        @trace_decorator_module.traced
        def sample(value):
            return value * 2

        result = sample(4)
        self.assertEqual(result, 8)
        debug_messages = [msg for level, msg in self.logger.records if level == "debug"]
        self.assertTrue(any("ENTER" in msg for msg in debug_messages))
        self.assertTrue(any("EXIT" in msg and "status=OK" in msg for msg in debug_messages))

    def test_traced_error_logs_status(self):
        @trace_decorator_module.traced
        def sample():
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            sample()
        debug_messages = [msg for level, msg in self.logger.records if level == "debug"]
        self.assertTrue(any("status=ERROR" in msg for msg in debug_messages))


class TransactionDecoratorTests(unittest.TestCase):
    def setUp(self):
        _reset_db_calls()

    def tearDown(self):
        _reset_db_calls()

    def test_transaction_success_commits_and_closes(self):
        @transaction_decorator_module.transactional("MES_DB")
        def operation(value, _tx=None):
            self.assertEqual(_tx, "tx-MES_DB")
            return value

        self.assertEqual(operation("done"), "done")
        self.assertEqual(
            _DB_CALLS,
            [("begin", "MES_DB"), ("commit", "tx-MES_DB"), ("close", "tx-MES_DB")]
        )

    def test_transaction_failure_rolls_back(self):
        @transaction_decorator_module.transactional("MES_DB")
        def operation(_tx=None):
            raise RuntimeError("fail")

        with self.assertRaises(RuntimeError):
            operation()
        self.assertEqual(
            _DB_CALLS,
            [("begin", "MES_DB"), ("rollback", "tx-MES_DB"), ("close", "tx-MES_DB")]
        )

    def test_transaction_respects_existing_transaction(self):
        @transaction_decorator_module.transactional("MES_DB")
        def operation(_tx=None):
            return "ok"

        self.assertEqual(operation(_tx="existing-tx"), "ok")
        self.assertEqual(_DB_CALLS, [])


class AccessControlTests(unittest.TestCase):
    def setUp(self):
        _USER_ROLES.clear()

    def test_require_allows_authorized_user(self):
        _USER_ROLES.add("Engineer")

        @access_control_module.require(["Engineer"])
        def secured():
            return "ok"

        self.assertEqual(secured(), "ok")

    def test_require_blocks_unauthorized_user(self):
        @access_control_module.require(["Engineer"])
        def secured():
            return "ok"

        with self.assertRaises(security_exception_module.SecurityException):
            secured()


class CryptoProviderTests(unittest.TestCase):
    def test_hmac_accepts_text_values(self):
        digest = crypto_provider_module.hmac_sha256(u"key", u"value")
        expected = crypto_provider_module.hmac_sha256(b"key", b"value")
        self.assertEqual(digest, expected)

    def test_hmac_rejects_none(self):
        with self.assertRaises(ValueError):
            crypto_provider_module.hmac_sha256(None, "value")


class LogFormatterTests(unittest.TestCase):
    def test_fmt_sorts_keys(self):
        formatted = log_formatter_module.fmt("MSG", b=2, a=1)
        self.assertEqual(formatted, "MSG | a=1 | b=2")


class SessionContextTests(unittest.TestCase):
    def test_current_uses_system_defaults(self):
        ctx = session_context_module.current()
        self.assertEqual(ctx["user"], "tester")
        self.assertEqual(ctx["tenant"], "default")
        self.assertTrue(ctx["correlationId"])


if __name__ == "__main__":
    unittest.main()
