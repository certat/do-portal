import subprocess
from app import celery, gpg


def popen(*args, **kwargs):
    defaults = {
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'stdin': subprocess.PIPE
    }
    defaults.update(kwargs)
    return subprocess.Popen(args, **defaults)


@celery.task
def send_to_ks(ks, fingerprints):
    """Send keys from local keychain to keyserver

    :param ks: Keyserver
    :param fingerprints: List of fingerprints to send
    :return:
    """
    gpg.gnupg.send_keys(ks, *fingerprints)
