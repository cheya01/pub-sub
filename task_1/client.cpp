// Client.cpp
#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>

#define BUFFER_SIZE 1024

int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    std::cerr << "Usage: " << argv[0] << " <SERVER_IP> <PORT>" << std::endl;
    return 1;
  }

  const char *server_ip = argv[1];
  int port = std::stoi(argv[2]);
  int sock = 0;
  struct sockaddr_in serv_addr;
  char buffer[BUFFER_SIZE] = {0};

  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
  {
    std::cerr << "Socket creation error" << std::endl;
    return -1;
  }

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(port);

  // Convert IPv4 and IPv6 addresses from text to binary form
  if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0)
  {
    std::cerr << "Invalid address / Address not supported" << std::endl;
    return -1;
  }

  // Connect to the server
  if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
  {
    std::cerr << "Connection Failed" << std::endl;
    return -1;
  }

  while (true)
  {
    std::string message;
    std::getline(std::cin, message);
    send(sock, message.c_str(), message.length(), 0);
    if (message == "terminate")
    {
      std::cout << "Terminate command sent. Disconnecting from server." << std::endl;
      break;
    }
  }

  close(sock);
  return 0;
}
