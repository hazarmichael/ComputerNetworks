from socket import *

serverport = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)


def generate_response_header(status, content_type):
    response = f'HTTP/1.1 {status}\r\n'
    response += f'Content-Type: {content_type}\r\n'
    response += '\r\n'
    return response.encode()


def sort_laptops_by_name(laptops):
    return sorted(laptops, key=lambda laptop: laptop['Name'].upper())


def sort_laptops_by_price(laptops):
    return sorted(laptops, key=lambda laptop: int(laptop['Price']))


def format_laptop_list(laptops):
    formatted_list = []
    for laptop in laptops:
        formatted_list.append(f"{laptop['Name'].upper()}: ${laptop['Price']}")
    return '\n'.join(formatted_list)


def read_laptops_from_file(filename):
    laptops = []
    with open(filename, 'r') as file:
        for line in file:
            name, price = line.strip().split(',')
            laptops.append({'Name': name, 'Price': price})
    return laptops


    laptops = read_laptops_from_file('laptops.txt')
while True:
    print("The [Server] is ready to receive ...")
    connectionSocket, client_address = serverSocket.accept()
    data = connectionSocket.recv(1048).decode()
    print(data)
    browser_lines = data.split('\n')
    browser = browser_lines[0]

    if len(data) > 0:

        request_line = data.split('\n')[0]
        request_path = request_line.split()[1]
        client_req_url = browser.split()[1]

        if request_path in ('/', '/index.html', '/main_en.html', '/en', '/enPage.html'):
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
            connectionSocket.send('Content-Type: text/html; charset=UTF-8\r\n'.encode())
            connectionSocket.send('\r\n'.encode())
            with open("enPage.html", "rb") as file:
                connectionSocket.send(file.read())
        elif request_path in ('/ar', '/arPage.html'):
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
            connectionSocket.send('Content-Type: text/html; charset=UTF-8\r\n'.encode())
            connectionSocket.send('\r\n'.encode())
            with open("arPage.html", "rb") as file:
                connectionSocket.send(file.read())
        elif client_req_url == '/style.css' or client_req_url.endswith('.css'):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type:text/css\r\n".encode())
            connectionSocket.send("\r\n".encode())
            style_css = open("styles.css", "rb").read()  # open english html file
            connectionSocket.send(style_css)
        elif client_req_url.endswith(".png"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type:image/png\r\n".encode())
            connectionSocket.send("\r\n".encode())
            png_image = open("imgpng.png", "rb").read()  # open english html file
            connectionSocket.send(png_image)
        elif client_req_url.endswith(".jpg"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type:image/jpeg\r\n".encode())
            connectionSocket.send("\r\n".encode())
            jpg_image = open("husnee-mubaarik-YvYL0uQcJIg-unsplash.jpg", "rb").read()  # open english html file
            connectionSocket.send(jpg_image)
        elif client_req_url.endswith('/.html'):
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
            connectionSocket.send('Content-Type: text/html; charset=UTF-8\r\n'.encode())
            connectionSocket.send('\r\n'.encode())
            with open("hello.html", "rb") as file:
                connectionSocket.send(file.read())
        elif client_req_url.endswith('.css'):
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())
            connectionSocket.send('Content-Type: text/css; charset=UTF-8\r\n'.encode())
            connectionSocket.send('\r\n'.encode())
            with open("styles.css", "rb") as file:
                connectionSocket.send(file.read())

            try:
                with open(request_path[1:], "rb") as file:
                    connectionSocket.send(file.read())
            except FileNotFoundError:
                # Handle 404 here...
                pass

        elif client_req_url == '/SortByName':
            response = generate_response_header('200 OK', 'text/plain; charset=UTF-8')
            sorted_laptops = sort_laptops_by_name(laptops)
            laptop_list = format_laptop_list(sorted_laptops)
            connectionSocket.send(response)
            connectionSocket.send(laptop_list.encode())
        elif client_req_url == '/SortByPrice':
            response = generate_response_header('200 OK', 'text/plain; charset=UTF-8')
            sorted_laptops = sort_laptops_by_price(laptops)
            laptop_list = format_laptop_list(sorted_laptops)
            total_price = sum(int(laptop['Price']) for laptop in sorted_laptops)
            laptop_list += f"\nTotal Price: ${total_price}"
            connectionSocket.send(response)
            connectionSocket.send(laptop_list.encode())
        elif client_req_url == '/azn':
            redirect_link = b'HTTP/1.1 307 Temporary Redirect\nLOCATION:https://www.amazon.com/ref=nav_logo\n\n '
            connectionSocket.sendall(redirect_link)
        elif client_req_url == '/so':
            redirect_link = b'HTTP/1.1 307 Temporary Redirect\nLOCATION:https://stackoverflow.com/\n\n '
            connectionSocket.sendall(redirect_link)
        elif client_req_url == '/bzu':
            redirect_link = b'HTTP/1.1 307 Temporary Redirect\nLOCATION:https://www.birzeit.edu/en\n\n '
            connectionSocket.sendall(redirect_link)
        else:
            # Handle other cases (404 or redirects) here...
            response = generate_response_header('404 Not Found', 'text/html; charset=UTF-8')
            with open("404.html", "rb") as file:
                html_content = file.read().replace(b'{client_ip}', str(client_address[0]).encode()).replace(
                    b'{client_port}', str(client_address[1]).encode())
                connectionSocket.sendall(response + html_content)
            pass

    connectionSocket.close()