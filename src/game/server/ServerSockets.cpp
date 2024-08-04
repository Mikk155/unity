/***
 *
 *	Copyright (c) 1996-2001, Valve LLC. All rights reserved.
 *
 *	This product contains software technology licensed from Id
 *	Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc.
 *	All Rights Reserved.
 *
 *   Use, distribution, and modification of this source code and/or resulting
 *   object code is restricted to non-commercial enhancements to products from
 *   Valve LLC.  All other use, distribution, or modification is prohibited
 *   without written permission from Valve LLC.
 *
 ****/

#include "ServerSockets.h"

#include "gamerules/CGameRules.h"

void ServerSockets :: Send( const std::string& message )
{
    ServerSockets::m_messages.append( message + "\n" );
}

void ServerSockets :: PrintResponse( const std::string& message )
{
    if( message == "\0" )
	    CGameRules::Logger->trace("[SOCKET] Fake msge \"{}\"", message );
    else
	    CGameRules::Logger->trace("[SOCKET] \"{}\"", message );
}

#if defined(WIN32)

#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

static SOCKET server_fd;
static sockaddr_in address;

void ServerSockets :: Listen()
{
    CGameRules::Logger->trace("[SOCKET] Listening..." );
    WSADATA wsaData;
    int iResult;

    // Inicializar Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
            CGameRules::Logger->trace("[SOCKET] WSAStartup failed: {}", iResult );
        return;
    }

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd == INVALID_SOCKET) {
            CGameRules::Logger->trace("[SOCKET] Socket failed: {}", WSAGetLastError() );
        WSACleanup();
        return;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);

    if (bind(server_fd, (sockaddr*)&address, sizeof(address)) == SOCKET_ERROR) {
            CGameRules::Logger->trace("[SOCKET] Bind failed: {}", WSAGetLastError() );
        closesocket(server_fd);
        WSACleanup();
        return;
    }

    if (listen(server_fd, 3) == SOCKET_ERROR) {
            CGameRules::Logger->trace("[SOCKET] Listen failed: {}", WSAGetLastError() );
        closesocket(server_fd);
        WSACleanup();
        return;
    }

    CGameRules::Logger->trace("[SOCKET] Waiting for connections..." );

    while (IsListening) {
        SOCKET new_socket = accept(server_fd, NULL, NULL);
        if (new_socket == INVALID_SOCKET) {
            if (IsListening) {
            CGameRules::Logger->trace("[SOCKET] Accept failed: {}", WSAGetLastError() );
            }
            continue;
        }

        char buffer[1024] = {0};
        int valread = recv(new_socket, buffer, 1024, 0);
        if (valread == SOCKET_ERROR) {
            CGameRules::Logger->trace("[SOCKET] Receive failed: {}", WSAGetLastError() );
        } else {
            PrintResponse(std::string(buffer));
            send(new_socket, ServerSockets::m_messages.c_str(), ServerSockets::m_messages.size(), 0);
            ServerSockets::m_messages = "\0";
        }

        closesocket(new_socket);
    }

    closesocket(server_fd);
    WSACleanup();
}

#else

void ServerSockets :: Listen()
{
}

#endif

void ServerSockets :: StartListeningThread()
{
    IsListening = true;
    ListeningThread = std::thread( ServerSockets::Listen );
}

void ServerSockets :: StopListeningThread()
{
    IsListening = false;
    if (ListeningThread.joinable()) {
        ListeningThread.join();
    }
}
