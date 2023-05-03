import socket


def send_receive(ip_dst, port_dst, msg, maxsize=1024):
    """
    Send one package via udp and receive one package.
    :param ip_dst: ip where to send the data
    :param port_dst: port to send the data to
    :param msg: data to send
    :return data: the data you received
    :return addr: the address you received the data from
    """

    if isinstance(msg, bytes):
        msg = msg
    else:
        msg = msg.encode()

    print(f'Sending message {msg} to {ip_dst}:{port_dst}')

    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send the message to the server
    sock.sendto(msg, (ip_dst, port_dst))

    # receive the response from the server
    data, addr = sock.recvfrom(maxsize)

    print(f'Received message {data} from {addr[0]}:{addr[1]}')
    return data, addr


if __name__ == '__main__':
    send_receive('127.0.0.1', 1337, 'Huhu!')
