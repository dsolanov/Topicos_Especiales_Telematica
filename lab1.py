from socket import gethostbyname, socket, AF_INET, SOCK_STREAM
from bs4 import BeautifulSoup
import os

HTTP_HEADER_DELIMITER = b"\r\n\r\n"
CONTENT_LENGTH_FIELD = b"Content-Length: "
HTTP_PORT = 80
ONE_BYTE_LENGTH = 1


def request(host, path, method="GET "):

    r = "{} {} HTTP/1.1\nHost: {}\r\n\r\n".format(method, path, host)
    request = r.encode()

    return request


def response(sock):

    header = bytes()
    chunk = bytes()

    try:
        while HTTP_HEADER_DELIMITER not in header:
            chunk = sock.recv(ONE_BYTE_LENGTH)
            if not chunk:
                break
            else:
                header += chunk
    except socket.timeout:
        pass

    return header


def content_length(header):

    for line in header.split(b"\r\n"):
        if CONTENT_LENGTH_FIELD in line:
            return int(line[len(CONTENT_LENGTH_FIELD):])
    return 0


def get_body(sock, length):

    body = bytes()
    data = bytes()

    while True:
        data = sock.recv(length)
        if len(data) <= 0:
            break
        else:
            body += data

    return body


def write_body(name_file, extension, body):

    if not(os.path.exists("Files")):
        os.mkdir("Files")

    try:
        file = open("Files/{}.{}".format(name_file, extension), "w+")
        file.write(body.decode("latin-1"))
        file.close()
    except:
        return 0
    return 1


def parser_body(file):
    content = open(file)
    soup = BeautifulSoup(content, "html.parser")
    parser = soup.find_all("<img>", "<audio> </audio>", "<video> </video>", "<object> </object>", "<source>", "<a> </a>")

    return parser


def main():
    host = input("\n Ingresar el HOST: \n (ejemplo: ejemplo.com) \n --> ")
    path = input("\n Ingresar el PATH: \n (ejemplo: /ejemplo.html) \n No olvide escribir el caracter '/' \n --> ")
    port = input("\n Ingresar el #PUERTO: \n --> ")
    name_file = input(
        "\n Ingresar nombre para el archivo: \n (ejemplo: 'nombre_archivo') \n --> ")
    extension = input("\n Ingresar extension para el archivo (ejemplo: 'html' , 'txt') \n --> ")
    aux = 0


    if(extension == "html"):
        parser = input(
            "\n Desea hacer analisis de sintaxis del html? \n Por favor Digite el numero: \n (1) para confirmar Analisis \n (2) para omitir Analasis \n --> ")
        if(parser == "1"):
           aux = 1
        else:
            pass

    print(f"\n --> Recibiendo informacion de: \n     http://{host}{path}")
    ip_address = gethostbyname(host)
    print(
        f"\n --> El Servidor Remoto: {host} \n     Con Direccion IP: {ip_address} ")

    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip_address, int(port)))
    print(f"\n --> Conexion TCP establecida con: \n     IP: {ip_address} \n     Por puerto: {port}")

    http_get_request = request(host, path)
    print("\n --> HTTP request ({} bytes)".format(len(http_get_request)))
    print(http_get_request)
    sock.sendall(http_get_request)

    header = response(sock)
    print(type(header))
    print("\n --> HTTP Response Cabecera ({} bytes)".format(len(header)))
    print(header)

    length = content_length(header)
    print("\n --> Longitud del cuerpo ")
    print(f"    {length} bytes ")

    body = get_body(sock, length)

    if(len(body) > 1):

        print("\n --> Cuerpo ({} bytes)".format(len(body)))
        print(body)

        wfile = write_body(name_file, extension, body)

        if wfile == 1:
            print("\n --> Archivo Guardado ")
        else:
            print("\n --> Error al guardar archivo ")

        if (aux == 1 and wfile == 1):

            parser = parser_body("Files/{}.{}".format(name_file, extension))
            print("\n --> El archivo se ha analisado: \n {} ".format(parser))
    else:
        print("\n --> El archivo no posee un cuerpo: \n     ({} bytes)".format(len(body)))


if __name__ == '__main__':
    main()
