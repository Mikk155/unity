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

#include <iostream>
#include <cstring>
#include <string>
#include <thread>

#pragma once

namespace ServerSockets
{
    namespace {
        std::string m_messages;
    }

    static std::thread thread;
    static bool Initialised = false;
    static std::atomic<bool> IsListening;
    static std::thread ListeningThread;

    void Listen();
    void Send( const std::string& message );
    void PrintResponse( const std::string& message );
    void StartListeningThread();
    void StopListeningThread();
}
