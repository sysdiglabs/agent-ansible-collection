def to_deb_url(data):
    """ Return the URL to a custom deb repository (if provided) """
    try:
        return data['repository']['deb']['url']
    except KeyError:
        return ""


def to_deb_gpg_key(data):
    """ Return the URL to the public GPG key for validating the signed deb packages
    """
    try:
        return data['repository']['deb']['gpg_key']
    except KeyError:
        return ""


def to_rpm_url(data):
    """ Return the URL to a custom RPM repository (if provided)
    """
    try:
        return data['repository']['rpm']['url']
    except KeyError:
        return ""

def to_rpm_gpg_key(data):
    """ Return the URL to the public GPG key for validating the signed rpm packages
    """
    try:
        return data['repository']['rpm']['gpg_key']
    except KeyError:
        return ""


class FilterModule:
    def filters(self):
        return {
            "toDebUrl": to_deb_url,
            "toDebGpgKey": to_deb_gpg_key,
            "toRpmUrl": to_rpm_url,
            "toRpmGpgKey": to_rpm_gpg_key
        }
