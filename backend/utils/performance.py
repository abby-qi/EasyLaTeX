"""
Performance optimizations for EasyLaTeX
"""

import functools
import time
from typing import Callable, Any


def cache_result(maxsize: int = 128):
    """
    Decorator to cache function results.

    Args:
        maxsize: Maximum number of results to cache

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = str(args) + str(sorted(kwargs.items()))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
                if len(cache) > maxsize:
                    cache.pop(next(iter(cache)))
            return cache[key]
        return wrapper
    return decorator


def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Args:
        func: Function to measure

    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"[PERF] {func.__name__} executed in {execution_time:.3f}s")
        return result
    return wrapper


class PerformanceMonitor:
    """Monitor and log performance metrics."""

    def __init__(self):
        self.metrics = {
            'compilation_times': [],
            'render_times': [],
            'memory_usage': []
        }

    def record_compilation(self, time_taken: float):
        """Record compilation time."""
        self.metrics['compilation_times'].append(time_taken)

    def record_render(self, time_taken: float):
        """Record render time."""
        self.metrics['render_times'].append(time_taken)

    def get_average_compilation_time(self) -> float:
        """Get average compilation time."""
        if not self.metrics['compilation_times']:
            return 0.0
        return sum(self.metrics['compilation_times']) / len(self.metrics['compilation_times'])

    def get_average_render_time(self) -> float:
        """Get average render time."""
        if not self.metrics['render_times']:
            return 0.0
        return sum(self.metrics['render_times']) / len(self.metrics['render_times'])

    def get_summary(self) -> str:
        """Get performance summary."""
        summary = []
        summary.append(f"Average compilation time: {self.get_average_compilation_time():.3f}s")
        summary.append(f"Average render time: {self.get_average_render_time():.3f}s")
        summary.append(f"Total compilations: {len(self.metrics['compilation_times'])}")
        summary.append(f"Total renders: {len(self.metrics['render_times'])}")
        return '\n'.join(summary)


performance_monitor = PerformanceMonitor()