import logging, sys

def setup_logging(level: str = 'info'):
    lvl = getattr(logging, level.upper(), logging.INFO)
    h = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    root = logging.getLogger()
    root.setLevel(lvl)
    h.setFormatter(fmt)
    root.handlers = [h]
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    return root
