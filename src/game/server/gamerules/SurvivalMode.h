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

#pragma once

#include "cbase.h"
#include "UserMessages.h"

class SurvivalMode final
{
public:
	void Think();
    bool IsActive();        // Survival mode is active
    bool IsEnabled();       // Survival mode is enabled
    int Enabled();
    int StartDelay();       // Delay before start
    int RestartDelay();     // Delay before restart
    bool ShouldRestart();
    void ObserverMode( CBasePlayer* pPlayer );

private:
    float m_flNextThink;
    int m_LastActive;
    bool m_Restarting;
    int m_iAlivePlayers;
    int m_iRestartDelay;
};

inline SurvivalMode g_SurvivalMode;
