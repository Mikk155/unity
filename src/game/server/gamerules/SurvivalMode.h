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

/*
    -Mikk -TODO

    - Fix players re-spawning gibing other players just as how re-spawning works in sven coop.

    - CBaseEntity::Revive( CBaseEntity* pOther )
        pOther is the reviver, mean player by medkit or checkpoint entity

    - CBasePlayer::Revive( CBaseEntity* pOther ) override;
        Meant for this->LeaveObserver, get position of dead corpse and teleport after Spawn

    - CBaseDeadPlayer
        overrides the usage of regular HL player's corpses, one entity per player.
        name it "deadplayer" for keep compatibility with sven
        owner must be the player
        this entity should be stored in the player for easy access

    - CWeaponMedkit
        Medkit weapon for reviving entities and players
        Should consume healthstations/healthkits instead of ilimited >:x
        item_healthkit will equip this weapon.
        create a cvar for prevent said feature and use weapon_medkit item instead
        primary attack healths yourself if not aiming to anyone
        When taking health, give medkit ammo first if not full

    - CPointCheckPoint
        directly calls Revive function of all connected players
        nothing more, leave it as simple as it can be.
        instead in a future with Angelscript
        Scripters would have access to CBaseEntity::m_szKeyValues
        as a dictionary for getting keyvalues and re-mapping their own checkpoints
*/

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
