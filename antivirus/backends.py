import app_settings

class BaseAntivirusBackend(object):
    def scanfile(self, file_path):
        raise Exception('Not implemented!')

class ClamAV(BaseAntivirusBackend):
    """Backend class to give way to use ClamAV antivirus libraries"""
    def scanfile(self, file_path):
        if app_settings.ANTIVIRUS_USE_CLAMAV_DEAMON:
            import pyclamd
            if app_settings.ANTIVIRUS_CLAMD_USE_UNIX:
                pyclamd.init_unix_socket(
                        app_settings.ANTIVIRUS_CLAMD_UNIX_PATH,
                        )
            else:
                pyclamd.init_network_socket(
                        app_settings.ANTIVIRUS_CLAMD_HOSTNAME,
                        app_settings.ANTIVIRUS_CLAMD_PORT,
                        )
            found = pyclamd.scan_file(self.path)
            virus = found and '\n'.join(found.values()) or ''
        else:
            import pyclamav
            found, virus = pyclamav.scanfile(file_path)

        return found, virus

