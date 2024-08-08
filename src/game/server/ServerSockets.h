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

#include "cbase.h"

#include <iostream>
#include <cstring>
#include <string>

#include <spdlog/logger.h>

#pragma once

// Need linux version wich as i dont know and can't test i won't do it for myself, pull requests are welcome
namespace ServerSockets
{
    // Logger
	static inline std::shared_ptr<spdlog::logger> Logger;

    // Opens the connection, Returns false if fails
    bool OpenConnection();
    // Closes the connection
    void CloseConnection();

    // Returns whatever the client is connected
    bool IsConnected();

    // Get the server information as a string in a json format ready to load
    std::string GetServerData();

    // Sends a string to the server connection
    void request( const std::string& message );

    // Prints in the game chat
    void print( const std::string& message );
}
