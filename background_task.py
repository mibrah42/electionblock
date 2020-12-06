import time


def background_task(n):
    delay = 2
    print("Task running")
    print(f"Simulating {delay} second delay")
    time.sleep(delay)

    print(len(n))

    print("Task complete")

    return len(n)
