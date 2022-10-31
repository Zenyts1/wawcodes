import base64


def log_request(request):
    with open("logs.txt", "a") as f:
        f.write(
            f"{request.method} {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)} {request.full_path} {base64.b64encode(str(request.user_agent).encode()).decode()}\n\n"
        )


def log_end(code, uids):
    with open("logs.txt", "a") as f:
        f.write(
            f"Successfully redeemed code : {code} for uids : {', '.join(uids['success'])}\nFailed for : {', '.join(uids['fail'])} for reasons : {', '.join(uids['reasons'])}\n\n"
        )


def log_exception(e):
    with open("logs.txt", "a") as f:
        f.write(f"An error occured : {e}\n\n")


def log_daily(response):
    with open("logs.txt", "a") as f:
        f.write(
            f"{response.status_code} {response.status_text} {response.headers.get('Content-Type', '')} : {response.content}\n\n")
