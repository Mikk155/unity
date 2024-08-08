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

#if defined(WIN32)

#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

SOCKET sock = INVALID_SOCKET;
#endif

bool ServerSockets :: OpenConnection()
{
    if( true )
    {
        Logger->info("Connected to server!" );
        return true;
    }
#if defined(WIN32)

    WSADATA wsaData;
    struct sockaddr_in server;

    // Inicializar Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        Logger->info("WSAStartup failed." );
        return false;
    }

    // Crear el socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        Logger->info("Socket creation failed: {} ", WSAGetLastError() );
        WSACleanup();
        return false;
    }

    server.sin_addr.s_addr = inet_addr("127.0.0.1");  // IP del servidor
    server.sin_family = AF_INET;
    server.sin_port = htons(8080);  // Puerto del servidor

    // Conectarse al servidor
    if (connect(sock, (struct sockaddr*)&server, sizeof(server)) < 0) {
        Logger->info("Connection failed: {}", WSAGetLastError() );
        closesocket(sock);
        WSACleanup();
        return false;
    }

    Logger->info("Connected to server!" );
    return true;
#else
    // Linux
    return false;
#endif
}

void ServerSockets :: CloseConnection()
{
#if defined(WIN32)
    if( sock != INVALID_SOCKET )
    {
        closesocket( sock );
        WSACleanup();
    }
#else
    // Linux
#endif
}

bool ServerSockets :: IsConnected()
{
#if defined(WIN32)
    return ( sock != INVALID_SOCKET );
#else
    // Linux
    return false;
#endif
}

void ServerSockets :: request( const std::string& message )
{
#if defined(WIN32)
    if( sock != INVALID_SOCKET )
    {
        send(sock, message.c_str(), message.size(), 0);

        char buffer[1024] = {0};
        int valread = recv(sock, buffer, 1024, 0);

        if (valread > 0)
        {
            print( std::string( buffer ) );
        }
    }
#else
    // Linux
#endif
}

void ServerSockets :: print( const std::string& message )
{
    if( !message.empty() )
    {
        UTIL_ClientPrintAll( print_chat, message.c_str() );
        UTIL_ClientPrintAll( print_console, message.c_str() );
    }
}

std::string ServerSockets :: GetServerData()
{
    std::string ServerData = "{";
    ServerData.append( fmt::format( "\"hostname\": \"{}\"", CVAR_GET_STRING( "hostname" ) ) );
    // array of dictionary with player names, score, deaths, IsAlive, team if any
    // gamemode
    // ip
    // mapname
    // map title if any
    // Survival Mode, checkpoints if any
    // current / max players
    // in client, check mapname to add an image
    ServerData.append( "}" );

    return ServerData;
}
