import errno
import sys

def main():
    try:
        newapt() #pending
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        sys.stderr.close()
    except OSError as error:
        if error.errno == errno.ENOSPC:
            sys.exit("No space left on device.")
        raise error from error
