"""
Exception definitions
"""


class UnsupportedVersion(Exception):
    """Indicates that the user is trying to use an UnsupportedVersion
    version of the API.
    """
    pass


class EndpointNotFound(Exception):
    """Could not find Service or Region in Service Catalog."""
    pass


class ConnectionRefused(Exception):
    """
    Connection refused: the server refused the connection.
    """
    def __init__(self, response=None):
        self.response = response

    def __str__(self):
        return "ConnectionRefused: %s" % repr(self.response)


class ResourceNotFound(Exception):
    """Unknow resource, not 'compute', 'network', 'block_storage'
    or 'object_storage'.
    """
    pass


class ResourceNotDefined(Exception):
    """Not defined resource, default is None."""
    pass


class ProviderNotFound(Exception):
    """Unknow/Unsupported provider"""
    pass


class ResourceInErrorState(Exception):
    """Resource is in the error state."""

    def __init__(self, obj):
        msg = "`%s` resource is in the error state" % obj.__class__.__name__
        fault_msg = getattr(obj, "fault", {}).get("message")
        if fault_msg:
            msg += "due to '%s'" % fault_msg
        self.message = "%s." % msg
