import http.server
import socketserver
import webbrowser


def host(PORT=8000):

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)

        url = "http://localhost:8000/"
        webbrowser.open(url, new=0, autoraise=True)
        httpd.serve_forever()


if __name__ == "__main__":
    host()
