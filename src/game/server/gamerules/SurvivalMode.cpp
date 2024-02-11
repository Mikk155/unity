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

#include "SurvivalMode.h"

bool SurvivalMode :: IsActive()
{
    return ( (int)CVAR_GET_FLOAT( "mp_survival_mode" ) == 1 );
}

int SurvivalMode :: StartDelay()
{
    return (int)CVAR_GET_FLOAT( "mp_survival_delay" );
}

void SurvivalMode :: Think()
{
    if( m_LastActive != (int)CVAR_GET_FLOAT( "mp_survival_mode" ) )
    {
        if( m_LastActive == 0 )
        {
            UTIL_ClientPrintAll( HUD_PRINTTALK, "#SurvivalStarted" );
        }
        else
        {
            UTIL_ClientPrintAll( HUD_PRINTTALK, "#SurvivalDisabled" );
        }
        m_LastActive = (int)CVAR_GET_FLOAT( "mp_survival_mode" );
    }

    if( !g_SurvivalMode.IsActive() || g_SurvivalMode.StartDelay() <= 0 || !UTIL_FindEntityByClassname( nullptr, "player" ) )
        return;

    // Should we do something in SP?
    if( !g_pGameRules->IsMultiplayer() )
        return;

    if( gpGlobals->time >= m_flNextThink )
    {
        int flTime = g_SurvivalMode.StartDelay();
        flTime--;
        CVAR_SET_FLOAT( "mp_survival_delay", flTime );

        if( g_SurvivalMode.StartDelay() > 0 )
        {
            char szChar[3];
            std::sprintf( szChar, "%d", g_SurvivalMode.StartDelay() );
            UTIL_ClientPrintAll( HUD_PRINTCENTER, "#SurvivalStartDelay", szChar );
        }

        m_flNextThink = gpGlobals->time + 1.0;
    }
}