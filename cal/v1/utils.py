def get_all_driver(cloud=None):
    """Get driver from Manager driver extension via broker
    """
    list_drivers = []
    return list_drivers


def filter(list_drivers, request):
    if request.environ['cal.cloud']:
        # just get driver belong to special cloud
        pass
    return list_drivers


def validate_driver(f):
    """Check driver on"""

    def check_driver(request):
        drivers = get_all_driver()
        drivers = filter(drivers, request)

        if drivers:
            return f(request, drivers)
        else:
            raise Exception('Driver is not found')

    return check_driver
