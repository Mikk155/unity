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

#include "CBaseEntity.h"

#define SF_SPAWNPOINT_STARTOFF ( 0 << 1 )

class CSpawnPoint : public CPointEntity
{
	public:
		void Spawn() override;
		bool KeyValue( KeyValueData* pkvd ) override;
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
		bool IsTriggered( CBaseEntity* pEntity ) override;
		void PlayerSpawn( CBasePlayer* pPlayer );

	private:
		float m_flOffSet = 256.0f;
		bool InitialState;
		int m_cTargets;
		string_t m_iKey[16];
		string_t m_iValue[16];
};

inline CBaseEntity* g_pLastSpawn = nullptr;

/**
 *	@brief Returns the entity to spawn at
 *	USES AND SETS GLOBAL g_pLastSpawn
 */
CBaseEntity* EntSelectSpawnPoint(CBasePlayer* pPlayer);
