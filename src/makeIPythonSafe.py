# If you're using IPython, this makes it so your tuning jobs don't break
# wanting a non-text console output (or something...)
# If you're not, this should be safe to use.
def patch_ipython_display():
    """Patch IPython.core.display.display if IPython is installed."""
    try:
        import IPython.display as _ipd
        import IPython.core.display as _ipcd
    except ImportError:
        # IPython isn't installed; nothing to do.
        return

    if not hasattr(_ipcd, "display"):
        _ipcd.display = _ipd.display

# Run the patch automatically on import
patch_ipython_display()

