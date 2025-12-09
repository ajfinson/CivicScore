"""Thread/process helpers"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Callable, List, Any
import multiprocessing


def create_thread_pool(max_workers: int = None) -> ThreadPoolExecutor:
    """Create a thread pool for I/O-bound tasks"""
    if max_workers is None:
        max_workers = min(32, (multiprocessing.cpu_count() or 1) + 4)
    return ThreadPoolExecutor(max_workers=max_workers)


def create_process_pool(max_workers: int = None) -> ProcessPoolExecutor:
    """Create a process pool for CPU-bound tasks"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count() or 1
    return ProcessPoolExecutor(max_workers=max_workers)


def parallel_map(func: Callable, items: List[Any], use_processes: bool = False, 
                 max_workers: int = None) -> List[Any]:
    """Execute function on items in parallel"""
    if use_processes:
        executor = create_process_pool(max_workers)
    else:
        executor = create_thread_pool(max_workers)
    
    results = []
    with executor:
        futures = [executor.submit(func, item) for item in items]
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Error in parallel execution: {e}")
                results.append(None)
    
    return results


def batch_process(items: List[Any], func: Callable, batch_size: int = 100) -> List[Any]:
    """Process items in batches"""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = [func(item) for item in batch]
        results.extend(batch_results)
    return results
