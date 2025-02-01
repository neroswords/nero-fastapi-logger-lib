import contextvars
import threading

def run_in_thread_with_context(func, *args, **kwargs):
    """Runs a function inside a new thread while preserving request_id."""
    ctx = contextvars.copy_context()  # Copy current request context

    def wrapped():
        ctx.run(func, *args, **kwargs)  # Run function inside copied context

    new_thread = threading.Thread(target=wrapped, daemon=True)
    new_thread.start()
    return new_thread