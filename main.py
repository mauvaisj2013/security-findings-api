import requests


def get_the_date(x):
    """Return a finding's date for use as the sorting key."""
    return x["date"]


def main():
    """Retrieve, sort, and display findings, then submit a new finding."""
    url = "http://127.0.0.1:5000/api/v1/results"
    response = requests.get(url)
    content = response.json()

    # ISO-formatted dates (YYYY-MM-DD) sort chronologically as strings.
    content["results"].sort(key=get_the_date, reverse=True)

    for result in content["results"]:
        print(result)

    new_result = {
        "name": "Server-Side Request Forgery",
        "type": "Application",
        "description": "Unrestricted Server-Side Requests to Internal Resources",
        "date": "2026-10-19"
    }

    response = requests.post(url, json=new_result)
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    main()