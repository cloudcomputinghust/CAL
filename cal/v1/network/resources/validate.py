
def validate_resource(f):
    def check_resource(driver, request):
        if 1 == 1:
            return f(driver=driver, request=request)
        else:
            raise Exception('Error validate_resource')
    return check_resource
