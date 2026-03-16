import requests
import time
from urllib.parse import urlparse


def validate_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def check_website(url):
    try:
        start = time.time()

        response = requests.get(url, timeout=5)

        response_time = round(time.time() - start, 2)
        status_code = response.status_code

        if status_code == 200:
            status = "UP"
        elif status_code == 404:
            status = "NOT FOUND"
        elif status_code >= 500:
            status = "SERVER ERROR"
        else:
            status = "UP"

        return {
            "url": url,
            "status": status,
            "status_code": status_code,
            "response_time": response_time
        }

    except requests.exceptions.RequestException:
        return {
            "url": url,
            "status": "DOWN",
            "status_code": None,
            "response_time": None
        }


def print_result(result):

    if result["status"] == "DOWN":
        print(f'{result["url"]} -> DOWN')
    else:
        print(
            f'{result["url"]} -> {result["status"]} ({result["status_code"]}) | {result["response_time"]}s'
        )


def print_summary(results):

    total = len(results)
    up = sum(1 for r in results if r["status"] == "UP")
    down = sum(1 for r in results if r["status"] == "DOWN")

    times = [r["response_time"] for r in results if r["response_time"]]

    avg_time = round(sum(times) / len(times), 2) if times else 0

    print("\nSummary:")
    print(f"Total websites: {total}")
    print(f"UP: {up}")
    print(f"DOWN: {down}")
    print(f"Average response time: {avg_time}s")


def main():

    print("Website Status Checker\n")

    user_input = input("Enter websites separated by commas:\n")

    urls = [u.strip() for u in user_input.split(",")]

    results = []

    print("\nChecking websites...\n")

    for url in urls:

        if not validate_url(url):
            print(f"{url} -> INVALID URL")
            continue

        result = check_website(url)

        results.append(result)

        print_result(result)

    print_summary(results)


if __name__ == "__main__":
    main()