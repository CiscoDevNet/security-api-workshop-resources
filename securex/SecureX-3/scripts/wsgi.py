from web_server_fastapi import app


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
