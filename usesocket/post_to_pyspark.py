import socket

import sock_localsettings

def post_to_pyspark(analysis_url):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (sock_localsettings.SERVER_ADDRESS, sock_localsettings.SERVER_PORT)
    sock.bind(server_address)
    sock.listen(1)
    print 'Opening socket connection..'

    connection, client_address = sock.accept()
    connection.sendall(analysis_url)
    time.sleep(1)
    connection.close()
    print 'Closing connection..'

    sock.close()
    print 'Done'


if __name__ == "__main__":
    print 'Starting..'
    post_to_pyspark(sock_localsettings.TEST_ANALYSISURL)
