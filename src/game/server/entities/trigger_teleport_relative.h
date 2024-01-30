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

#include "extdll.h"
#include "util.h"
#include "cbase.h"

#define SF_TTR_ONLY_TRIGGER     ( 1 << 0 ) // Only teleport people on the inside upon trigger
#define SF_TTR_ALLOW_MONSTERS   ( 1 << 1 ) // Allow monsters
#define SF_TTR_NO_CLIENTS       ( 1 << 2 ) // Don't allow players
#define SF_TTR_KILL_VELOCITY    ( 1 << 3 ) // Set velocity to g_vecZero

class CTriggerTeleportRelative : public CBaseEntity
{
public:
    void Spawn() override;
    void Touch( CBaseEntity* pOther ) override;
    void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
    int m_ttrFlags() { return ( ( FBitSet( pev->spawnflags, SF_TTR_ALLOW_MONSTERS ) ? FL_MONSTER : 0 ) | ( FBitSet( pev->spawnflags, SF_TTR_NO_CLIENTS ) ? 0 : FL_CLIENT ) ); };
    Vector GetLandMark( string_t m_iszChar );
    void RelativeTeleport( CBaseEntity* pEntity );
};