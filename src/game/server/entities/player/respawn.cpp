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

#define SF_PLAYER_RESPAWN_OUTSIDE ( 0 << 1 )
#define SF_PLAYER_RESPAWN_INSIDE  ( 1 << 1 )

class CPlayerRespawn : public CPointEntity
{
	public:
		void Spawn() override;
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
};

LINK_ENTITY_TO_CLASS( player_respawn, CPlayerRespawn );

void CPlayerRespawn :: Spawn()
{
	pev->solid = SOLID_NOT;

	SetModel( STRING( pev->model ) );
}

void CPlayerRespawn :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	FireTargets( STRING( pev->message ), nullptr, nullptr, USE_OFF, 0 );
	FireTargets( STRING( pev->netname ), nullptr, nullptr, USE_ON, 0 );

	if( !FBitSet( pev->spawnflags, ( SF_PLAYER_RESPAWN_INSIDE | SF_PLAYER_RESPAWN_OUTSIDE ) ) )
	{
		if( auto pPlayer = ToBasePlayer( pActivator ); pPlayer != nullptr )
		{
			g_pGameRules->PlayerSpawn( pPlayer );
		}
	}
	else
	{
		for( auto pPlayer : UTIL_FindPlayers() )
		{
			if( pPlayer != nullptr && pPlayer->IsPlayer() && IsPlayerSelector( pPlayer, pActivator ) )
			{
				if( FBitSet( pev->spawnflags, SF_PLAYER_RESPAWN_OUTSIDE ) && !Intersects( pPlayer )
					|| FBitSet( pev->spawnflags, SF_PLAYER_RESPAWN_INSIDE ) && Intersects( pPlayer )
						|| FBitSet( pev->spawnflags, ( SF_PLAYER_RESPAWN_INSIDE | SF_PLAYER_RESPAWN_OUTSIDE ) ) ) {
							g_pGameRules->PlayerSpawn( pPlayer );
				} else {
					FireTargets( STRING( pev->target ), pPlayer, this, USE_TOGGLE, 0 );
				}
			}
		}
	}
}
