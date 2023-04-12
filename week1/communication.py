import socket


def send_receive(ip_dst, port_dst, msg):
    """
    Send one package via udp and receive one package.
    :param ip_dst: ip where to send the data
    :param port_dst: port to send the data to
    :param msg: data to send
    :return data: the data you received
    :return addr: the address you received the data from
    """

    print(f'Sending message {msg} to {ip_dst}:{port_dst}')

    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send the message to the server
    sock.sendto(msg.encode(), (ip_dst, port_dst))

    # receive the response from the server
    data, addr = sock.recvfrom(1024)

    print(f'Received message {data.decode()} from {addr[0]}:{addr[1]}')
    return data, addr


if __name__ == '__main__':
    print(send_receive('127.0.0.1', 1337, 'Huhu!'))
    # print(send_receive("hackfest.redrocket.club", 21000, "PING"))
