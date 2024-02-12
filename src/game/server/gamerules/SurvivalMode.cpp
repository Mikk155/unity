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
    return ( g_SurvivalMode.IsEnabled() && g_SurvivalMode.StartDelay() <= 0 );
}

bool SurvivalMode :: IsEnabled()
{
    return ( g_SurvivalMode.Enabled() == 1 );
}

bool SurvivalMode :: ShouldRestart()
{
    return ( g_SurvivalMode.m_iAlivePlayers == 0 );
}

int SurvivalMode :: Enabled()
{
    return (int)CVAR_GET_FLOAT( "mp_survival_mode_active" );
}

int SurvivalMode :: RestartDelay()
{
    return (int)CVAR_GET_FLOAT( "mp_survival_mode_restartdelay" );
}

int SurvivalMode :: StartDelay()
{
    return (int)CVAR_GET_FLOAT( "mp_survival_mode_startdelay" );
}

void SurvivalMode :: Think()
{
    // Check for a survival mode change
    if( g_SurvivalMode.m_LastActive != g_SurvivalMode.Enabled() )
    {
        if( g_SurvivalMode.m_LastActive == 0 )
        {
            char szChar[3];
            std::sprintf( szChar, "%d", g_SurvivalMode.RestartDelay() );
            UTIL_ClientPrintAll( HUD_PRINTTALK, "#SurvivalStarted", szChar, ( g_SurvivalMode.RestartDelay() == 1 ? "" : "s" ) );
        }
        else
        {
            UTIL_ClientPrintAll( HUD_PRINTTALK, "#SurvivalDisabled" );
        }
        g_SurvivalMode.m_iRestartDelay = g_SurvivalMode.RestartDelay();
        g_SurvivalMode.m_LastActive = g_SurvivalMode.Enabled();
    }

    if( !g_SurvivalMode.IsEnabled()
        || !g_pGameRules->IsMultiplayer()
            || gpGlobals->time < g_SurvivalMode.m_flNextThink
                || !UTIL_FindEntityByClassname( nullptr, "player" ) ) {
        return;
    }

    // Check for a survival restart
    m_iAlivePlayers = 0;

    int index = 0;
    CBasePlayer* pPlayer = nullptr;
    while( ( pPlayer = UTIL_GetPlayers( index ) ) )
    {
        if( pPlayer->IsAlive() )
            m_iAlivePlayers++;
    }

    if( g_SurvivalMode.ShouldRestart() != g_SurvivalMode.m_Restarting && g_SurvivalMode.StartDelay() <= 0 )
    {
        if( !g_SurvivalMode.m_Restarting )
        {
            UTIL_ClientPrintAll( HUD_PRINTTALK, "#SurvivalRestart" );
        }
        else
        {
            UTIL_ClientPrintAll( HUD_PRINTTALK, "#SurvivalAlive" );
        }
        g_SurvivalMode.m_iRestartDelay = g_SurvivalMode.RestartDelay();
        g_SurvivalMode.m_Restarting = g_SurvivalMode.ShouldRestart();
    }

    // Countdown
    if( g_SurvivalMode.StartDelay() > 0 )
    {
        int flTime = g_SurvivalMode.StartDelay();
        flTime--;
        CVAR_SET_FLOAT( "mp_survival_mode_startdelay", flTime );

        char szChar[3];
        std::sprintf( szChar, "%d", g_SurvivalMode.StartDelay() );

        if( g_SurvivalMode.StartDelay() == 0 )
            UTIL_ClientPrintAll( HUD_PRINTCENTER, "" );
        else
            UTIL_ClientPrintAll( HUD_PRINTCENTER, "#SurvivalStartDelay", szChar );
    }

    if( g_SurvivalMode.m_Restarting )
    {
        g_SurvivalMode.m_iRestartDelay--;

        if( g_SurvivalMode.m_iRestartDelay <= 0 )
        {
            char szChar[128];
            std::sprintf( szChar, "map \"%s\"\n", STRING( gpGlobals->mapname ) );
            SERVER_COMMAND( szChar );
            SERVER_EXECUTE();
        }
    }

    // Try again in one second.
    g_SurvivalMode.m_flNextThink = gpGlobals->time + 1.0;
}

void SurvivalMode :: ObserverMode( CBasePlayer* pPlayer )
{
    if( pPlayer
        && pPlayer->m_bObserverSurvival
            && !g_SurvivalMode.IsActive()
                && g_pGameRules->IsMultiplayer()
                    && g_pGameRules->FPlayerCanRespawn( pPlayer ) ) {
                        pPlayer->LeaveObserver();
    }
}