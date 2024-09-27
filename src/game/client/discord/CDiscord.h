/***
 *
 *	Copyright (c) 1999, Valve LLC. All rights reserved.
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

#pragma once

#include "hud.h"
#include <string.h>
#include "discord_rpc.h"
#include <time.h>

/**
 *	@brief Discord
 */
class CDiscord final
{
    public:
        void RPCStartUp();
        void RPCStateUpdate();
        void RPCShutDown();

        const char* m_sLogo = "logo";
        const char* m_sHeader = "In main menu";
        const char* m_sDescription = "Just started playing.";
};

inline CDiscord g_Discord;
