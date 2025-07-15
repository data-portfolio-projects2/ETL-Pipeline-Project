import logging, timeit, functools, psutil, time, sys
from multiprocessing import Process


logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{", 
    datefmt="%Y-%m-%d %H:%M", 
    level=logging.INFO
)

def time_execution(func):
    """Decorator to measure execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()  # Start timer
        result = func(*args, **kwargs)       # Run the function
        end_time = timeit.default_timer()    # End timer
        print(f"⏳ Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def memory_usage(func):
    """Decorator to measure RAM usage with an animated progress bar."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bar_length = 20  # Length of the progress bar
        
        # Measure RAM before execution
        start_mem = psutil.Process().memory_info().rss / (1024 ** 2)  # Convert to MB

        print(f"\n🖥️ Function '{func.__name__}':")
        print(f"   🔷 RAM before: {start_mem:.2f} MB")

        result = func(*args, **kwargs)  # Execute function
        
        # Measure RAM after execution
        end_mem = psutil.Process().memory_info().rss / (1024 ** 2)  # Convert to MB
        change = end_mem - start_mem
        percent_change = (change / start_mem) * 100 if start_mem > 0 else 0

        print(f"   🔷 RAM after:  {end_mem:.2f} MB")

        # Simulate loading animation
        for i in range(bar_length + 1):
            bar = "█" * i + "░" * (bar_length - i)  # Animated progress bar
            sys.stdout.write(f"\r   🚀 Processing: [{bar}] {i*5}%")
            sys.stdout.flush()
            time.sleep(0.1)
        
        sys.stdout.write("\r   ✅ RAM Processing Complete!           \n")

        # Display RAM usage change
        arrow = "🔼" if change > 0 else "🔽"
        print(f"   {arrow} RAM Change: {abs(percent_change):.2f}% {'increase' if change > 0 else 'decrease'}\n")
        
        return result  # Return function result

    return wrapper

class static(type):
    def __new__(cls, name, bases, dct):
        for attr, value in dct.items():
            if callable(value) and not attr.startswith("__"):  # Exclude special methods
                dct[attr] = staticmethod(value)  # Apply @staticmethod
        return super().__new__(cls, name, bases, dct)
