"""Base classes for our unit tests.
Allows overriding of flags for use of fakes, and some black magic for
inline callbacks.
"""
import contextlib

import datetime
import eventlet
eventlet.monkey_patch(os=False)

import copy
import inspect
import mock
import os

import six
import testtools

from cal.tests import tools 

if six.PY2:
    nested = contextlib.nested
else:
    @contextlib.contextmanager
    def nested(*contexts):
        with contextlib.ExitStack() as stack:
            yield [stack.enter_context(c) for c in contexts]



class skipIf(object):
    """Class for skipping individual test methods 
    and even whole classes of tests.(Like unittest.skipIf())
    Example usage could be:
        @base.skipIf(mylib.__version__ < (1, 3),
                     "not supported in this library version")
    """
    def __init__(self, condition, reason):
        self.condition = condition
        self.reason = reason

    def __call__(self, func_or_cls):
        condition = self.condition
        reason = self.reason
        if inspect.isfunction(func_or_cls):
            @six.wraps(func_or_cls)
            def wrapped(*args, **kwargs):
                if condition:
                    raise testtools.TestCase.skipException(reason)
                return func_or_cls(*args, **kwargs)

            return wrapped
        elif inspect.isclass(func_or_cls):
            orig_func = getattr(func_or_cls, 'setUp')

            @six.wraps(orig_func)
            def new_func(self, *args, **kwargs):
                if condition:
                    raise testtools.TestCase.skipException(reason)
                orig_func(self, *args, **kwargs)

            func_or_cls.setUp = new_func
            return func_or_cls
        else:
            raise TypeError('skipUnless can be used only with functions or '
                            'classes')

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

class TestCase(testtools.TestCase):
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
        self.useFixture(tools.StandardLogging)
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

    def flags(self, **kw):
        """Override flag variables for a test."""
        group = kw.pop('group', None)
        for k, v in six.iteritems(kw):
            CONF.set_override(k, v, group)

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

class MatchType(object):
    """Matches any instance of a specified type
    The MatchType class is a helper for use with the
    mock.assert_called_with() method that lets you
    assert that a particular parameter has a specific
    data type. It enables strict check than the built
    in mock.ANY helper, and is the equivalent of the
    mox.IsA() function from the legacy mox library
    Example usage could be:
      mock_some_method.assert_called_once_with(
            "hello",
            MatchType(objects.Instance),
            mock.ANY,
            "world",
            MatchType(objects.KeyPair))
    """
    def __init__(self, wanttype):
        self.wanttype = wanttype

    def __eq__(self, other):
        return type(other) == self.wanttype

    def __ne__(self, other):
        return type(other) != self.wanttype

    def __repr__(self):
        return "<MatchType:" + str(self.wanttype) + ">"
