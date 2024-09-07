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
#include "spawnpoints.h"

LINK_ENTITY_TO_CLASS( info_player_start, CSpawnPoint );
LINK_ENTITY_TO_CLASS( info_player_deathmatch, CSpawnPoint );

bool CSpawnPoint :: KeyValue( KeyValueData* pkvd )
{
	if( std::string( pkvd->szKeyName ).find( "-" ) == 0 )
	{
		char temp[256];

		UTIL_StripToken(pkvd->szKeyName, temp);
		m_iKey[m_cTargets] = ALLOC_STRING(temp);

		UTIL_StripToken(pkvd->szValue, temp);
		m_iValue[m_cTargets] = ALLOC_STRING(temp);

		++m_cTargets;
	}
	else if( FStrEq( pkvd->szKeyName, "m_flOffSet" ) )
	{
		if( float flRange = atoi( pkvd->szValue ); flRange > 32 )
			m_flOffSet = flRange;
	}
	else
	{
		return CPointEntity::KeyValue(pkvd);
	}
	return true;
}

void CSpawnPoint :: PlayerSpawn( CBasePlayer* pPlayer )
{
	if( !pPlayer || pPlayer == nullptr )
		return;

	pPlayer->pev->angles = pev->angles;
	pPlayer->pev->fixangle = FIXANGLE_ABSOLUTE;
	pPlayer->pev->v_angle = pPlayer->pev->velocity = pPlayer->pev->punchangle = g_vecZero;

	pPlayer->SetOrigin( pev->origin + Vector(0, 0, 1) );

	if( m_cTargets > 0 )
		UTIL_InitializeKeyValues( pPlayer, m_iKey, m_iValue, m_cTargets );

	if( !FStringNull( pev->target ) )
	{
		FireTargets( STRING( pev->target ), pPlayer, this, USE_TOGGLE, 0 );
	}

	int hull_size = human_hull;
	Vector VecPos = UTIL_GetNearestHull( pev->origin, hull_size, m_flOffSet );

	if( VecPos == pev->origin )
	{
		hull_size = head_hull;
		VecPos = UTIL_GetNearestHull( pev->origin, hull_size, m_flOffSet );

		if( VecPos == pev->origin ) {
			CBaseEntity* pBlocker = nullptr;
			while( ( pBlocker = UTIL_FindEntityInSphere( pBlocker, pev->origin, ( m_flOffSet > 128 ? m_flOffSet : 128 ) ) ) != nullptr ) {
				if( pBlocker->IsPlayer() && pBlocker != pPlayer ) {
					pBlocker->TakeDamage( CBaseEntity::World, CBaseEntity::World, pBlocker->pev->max_health + 200, DMG_GENERIC );
				}
			}
		}
	}

	pPlayer->SetSize( hull_size == human_hull ? VEC_DUCK_HULL_MIN : VEC_HULL_MIN , hull_size == human_hull ? VEC_DUCK_HULL_MAX : VEC_HULL_MAX );
	pPlayer->SetOrigin( VecPos );
}

void CSpawnPoint :: Spawn()
{
	InitialState = FBitSet( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
}

void CSpawnPoint :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	switch( useType )
	{
		case USE_OFF:
			SetBits( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
		break;
		case USE_ON:
			ClearBits( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
		break;
		case USE_SET:
			if( InitialState )
				SetBits( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
			else ClearBits( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
		break;
		default:
			if( !FBitSet( pev->spawnflags, SF_SPAWNPOINT_STARTOFF ) )
				SetBits( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
			else ClearBits( pev->spawnflags, SF_SPAWNPOINT_STARTOFF );
		break;
	}
}

bool CSpawnPoint :: IsTriggered(CBaseEntity* pEntity)
{
	return UTIL_IsMasterTriggered(m_sMaster, pEntity, m_UseLocked);
}

/**
 *	@brief checks if the spot is clear of players
 */
bool IsSpawnPointValid(CBaseEntity* pPlayer, CBaseEntity* pSpot)
{
	CBaseEntity* ent = nullptr;

	if( !pSpot->IsTriggered(pPlayer) || FBitSet( pSpot->pev->spawnflags, SF_SPAWNPOINT_STARTOFF ) )
	{
		return false;
	}

	while ((ent = UTIL_FindEntityInSphere(ent, pSpot->pev->origin, 128)) != nullptr)
	{
		// if ent is a client, don't spawn on 'em
		if (ent->IsPlayer() && ent != pPlayer)
			return false;
	}

	return true;
}

static CBaseEntity* EntTrySelectSpawnPoint(CBasePlayer* pPlayer)
{
	CBaseEntity* pSpot;

	if (g_pGameRules->IsCTF() && pPlayer->m_iTeamNum != CTFTeam::None)
	{
		const auto pszTeamSpotName = pPlayer->m_iTeamNum == CTFTeam::BlackMesa ? "ctfs1" : "ctfs2";

		pSpot = g_pLastSpawn;
		// Randomize the start spot
		for (int i = RANDOM_LONG(1, 5); i > 0; i--)
			pSpot = UTIL_FindEntityByClassname(pSpot, pszTeamSpotName);
		if (FNullEnt(pSpot)) // skip over the null point
			pSpot = UTIL_FindEntityByClassname(pSpot, pszTeamSpotName);

		CBaseEntity* pFirstSpot = pSpot;

		do
		{
			if (pSpot)
			{
				// check if pSpot is valid
				if (IsSpawnPointValid(pPlayer, pSpot) && pSpot->pev->origin != g_vecZero)
				{
					// if so, go to pSpot
					return pSpot;
				}
			}
			// increment pSpot
			pSpot = UTIL_FindEntityByClassname(pSpot, pszTeamSpotName);
		} while (pSpot != pFirstSpot); // loop if we're not back to the start

		// Try a shared spawn spot
		//  Randomize the start spot
		for (int i = RANDOM_LONG(1, 5); i > 0; i--)
			pSpot = UTIL_FindEntityByClassname(pSpot, "ctfs0");
		if (FNullEnt(pSpot)) // skip over the null point
			pSpot = UTIL_FindEntityByClassname(pSpot, "ctfs0");

		pFirstSpot = pSpot;

		do
		{
			if (pSpot)
			{
				// check if pSpot is valid
				if (IsSpawnPointValid(pPlayer, pSpot) && pSpot->pev->origin != g_vecZero)
				{
					// if so, go to pSpot
					return pSpot;
				}
			}
			// increment pSpot
			pSpot = UTIL_FindEntityByClassname(pSpot, "ctfs0");
		} while (pSpot != pFirstSpot); // loop if we're not back to the start

		// we haven't found a place to spawn yet,  so kill any guy at the first spawn point and spawn there
		if (!FNullEnt(pSpot))
		{
			CBaseEntity* ent = nullptr;
			while ((ent = UTIL_FindEntityInSphere(ent, pSpot->pev->origin, 128)) != nullptr)
			{
				// if ent is a client, kill em (unless they are ourselves)
				if (ent->IsPlayer() && ent != pPlayer)
					ent->TakeDamage(CBaseEntity::World, CBaseEntity::World, 300, DMG_GENERIC);
			}
			return pSpot;
		}
	}

	if (g_pGameRules->IsMultiplayer())
	{
		pSpot = g_pLastSpawn;
		// Randomize the start spot
		for (int i = RANDOM_LONG(1, 5); i > 0; i--)
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_deathmatch");
		if (FNullEnt(pSpot)) // skip over the null point
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_deathmatch");

		CBaseEntity* pFirstSpot = pSpot;

		do
		{
			if (pSpot)
			{
				// check if pSpot is valid
				if (IsSpawnPointValid(pPlayer, pSpot))
				{
					if (pSpot->pev->origin == Vector(0, 0, 0))
					{
						pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_deathmatch");
						continue;
					}

					// if so, go to pSpot
					return pSpot;
				}
			}
			// increment pSpot
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_deathmatch");
		} while (pSpot != pFirstSpot); // loop if we're not back to the start

		return pSpot;
	}

	// If startspot is set, (re)spawn there.
	if (FStringNull(gpGlobals->startspot) || 0 == strlen(STRING(gpGlobals->startspot)))
	{
		pSpot = UTIL_FindEntityByClassname(nullptr, "info_player_start");
		if (!FNullEnt(pSpot))
			return pSpot;
	}
	else
	{
		pSpot = UTIL_FindEntityByTargetname(nullptr, STRING(gpGlobals->startspot));
		if (!FNullEnt(pSpot))
			return pSpot;
	}

	return nullptr;
}

CBaseEntity* EntSelectSpawnPoint(CBasePlayer* pPlayer)
{
	auto pSpot = EntTrySelectSpawnPoint(pPlayer);

	if (FNullEnt(pSpot))
	{
		CBaseEntity::Logger->error("PutClientInServer: no info_player_start on level");
		return CBaseEntity::World;
	}

	g_pLastSpawn = pSpot;
	return pSpot;
}
