def join_urls(*args):
    return '/'.join(arg.strip('/') for arg in args)
