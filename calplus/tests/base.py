"""Base classes for our unit tests.
Allows overriding of flags for use of fakes, and some black magic for
inline callbacks.
"""
import contextlib
from falcon import testing
import fixtures
import mock
import six

from calplus.tests import tools

if six.PY2:
    nested = contextlib.nested
else:
    @contextlib.contextmanager
    def nested(*contexts):
        with contextlib.ExitStack() as stack:
            yield [stack.enter_context(c) for c in contexts]


def _patch_mock_to_raise_for_invalid_assert_calls():
    def raise_for_invalid_assert_calls(wrapped):
        def wrapper(_self, name):
            valid_asserts = [
                'assert_called_with',
                'assert_called_once_with',
                'assert_has_calls',
                'assert_any_calls']

            if name.startswith('assert') and name not in valid_asserts:
                raise AttributeError('%s is not a valid mock assert method'
                                     % name)

            return wrapped(_self, name)
        return wrapper
    mock.Mock.__getattr__ = raise_for_invalid_assert_calls(
        mock.Mock.__getattr__)


# NOTE(gibi): needs to be called only once at import time
# to patch the mock lib
_patch_mock_to_raise_for_invalid_assert_calls()


class TestCase(testing.TestCase):

    """Test case base class for all unit tests.
    Due to the slowness of DB access, please consider deriving from
    `NoDBTestCase` first.
    """
    USES_DB = True
    USES_DB_SELF = False

    def setUp(self):
        """Run before each test method to initialize test environment."""
        super(TestCase, self).setUp()
        # Change the default directory that the tempfile
        # module places temporary files and directories in
        self.useFixture(fixtures.NestedTempfile())
        # Create a temporary directory and set it as $HOME in the environment.
        self.useFixture(fixtures.TempHomeDir())
        self.useFixture(tools.StandardLogging())
        self.addCleanup(self._clear_attrs)

    def _clear_attrs(self):
        # Delete attributes that don't start with _ so they don't pin
        # memory around unnecessarily for the duration of the test
        # suite
        for key in [k for k in self.__dict__.keys() if k[0] != '_']:
            # NOTE(gmann): Skip attribute 'id' because if tests are being
            # generated using testscenarios then, 'id' attribute is being
            # added during cloning the tests. And later that 'id' attribute
            # is being used by test suite to generate the results for each
            # newly generated tests by testscenarios.
            if key != 'id':
                del self.__dict__[key]

    def stub_out(self, old, new):
        """Replace a function for the duration of the test.
        Use the monkey patch fixture to replace a function for the
        duration of a test. Useful when you want to provide fake
        methods instead of mocks during testing.
        This should be used instead of self.stubs.Set (which is based
        on mox) going forward.
        """
        self.useFixture(fixtures.MonkeyPatch(old, new))

    def mock_object(self, obj, attr_name, new_attr=None, **kwargs):
        """Use python mock to mock an object attribute
        Mocks the specified objects attribute with the given value.
        Automatically performs 'addCleanup' for the mock.
        """
        if not new_attr:
            new_attr = mock.Mock()
        patcher = mock.patch.object(obj, attr_name, new_attr, **kwargs)
        patcher.start()
        self.addCleanup(patcher.stop)
        return new_attr


class NoDBTestCase(TestCase):

    """`NoDBTestCase` differs from TestCase in that DB access is not supported.
    This makes tests run significantly faster. If possible, all new tests
    should derive from this class.
    """
    USES_DB = False


class BaseHookTestCase(NoDBTestCase):

    def assert_has_hook(self, expected_name, func):
        self.assertTrue(hasattr(func, '__hook_name__'))
        self.assertEqual(expected_name, func.__hook_name__)
