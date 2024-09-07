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
#include "basemonster.h"

class CPlayerSetHudColor : public CPointEntity
{
	DECLARE_CLASS(CPlayerSetHudColor, CPointEntity);
	DECLARE_DATAMAP();

public:
	enum class Action
	{
		Set = 0,
		Reset = 1
	};

	bool KeyValue(KeyValueData* pkvd) override;

	void Use(CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value) override;

private:
	Vector m_HudColor{vec3_origin};
	Action m_Action{Action::Set};
};

LINK_ENTITY_TO_CLASS(player_sethudcolor, CPlayerSetHudColor);

BEGIN_DATAMAP(CPlayerSetHudColor)
DEFINE_FIELD(m_HudColor, FIELD_VECTOR),
	DEFINE_FIELD(m_Action, FIELD_INTEGER),
	END_DATAMAP();

bool CPlayerSetHudColor::KeyValue(KeyValueData* pkvd)
{
	if (FStrEq(pkvd->szKeyName, "hud_color"))
	{
		UTIL_StringToVector(m_HudColor, pkvd->szValue);
		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "action"))
	{
		m_Action = static_cast<Action>(atoi(pkvd->szValue));
		return true;
	}

	return CPointEntity::KeyValue(pkvd);
}

void CPlayerSetHudColor::Use(CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value)
{
	auto player = ToBasePlayer(pActivator);

	if (!player || !player->IsNetClient())
	{
		return;
	}

	const RGB24 color = [this]()
	{
		switch (m_Action)
		{
		case Action::Set:
			return RGB24{
				static_cast<std::uint8_t>(m_HudColor.x),
				static_cast<std::uint8_t>(m_HudColor.y),
				static_cast<std::uint8_t>(m_HudColor.z)};

		default:
		case Action::Reset:
			return RGB_HUD_COLOR;
		}
	}();

	player->SetHudColor(color);
}

class CPlayerSetCrosshairColor : public CPointEntity
{
	DECLARE_CLASS(CPlayerSetCrosshairColor, CPointEntity);
	DECLARE_DATAMAP();

public:
	enum class Action
	{
		Set = 0,
		Reset = 1
	};

	bool KeyValue(KeyValueData* pkvd) override;

	void Use(CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value) override;

private:
	Vector m_CrosshairColor{vec3_origin};
	Action m_Action{Action::Set};
};

LINK_ENTITY_TO_CLASS(player_setcrosshaircolor, CPlayerSetCrosshairColor);

BEGIN_DATAMAP(CPlayerSetCrosshairColor)
DEFINE_FIELD(m_CrosshairColor, FIELD_VECTOR),
	DEFINE_FIELD(m_Action, FIELD_INTEGER),
	END_DATAMAP();

bool CPlayerSetCrosshairColor::KeyValue(KeyValueData* pkvd)
{
	if (FStrEq(pkvd->szKeyName, "crosshair_color"))
	{
		UTIL_StringToVector(m_CrosshairColor, pkvd->szValue);
		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "action"))
	{
		m_Action = static_cast<Action>(atoi(pkvd->szValue));
		return true;
	}

	return CPointEntity::KeyValue(pkvd);
}

void CPlayerSetCrosshairColor::Use(CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value)
{
	auto player = ToBasePlayer(pActivator);

	if (!player || !player->IsNetClient())
	{
		return;
	}

	const RGB24 color = [this]()
	{
		switch (m_Action)
		{
		case Action::Set:
			return RGB24{
				static_cast<std::uint8_t>(m_CrosshairColor.x),
				static_cast<std::uint8_t>(m_CrosshairColor.y),
				static_cast<std::uint8_t>(m_CrosshairColor.z)};

		default:
		case Action::Reset:
			return RGB_HUD_COLOR;
		}
	}();

	player->SetCrosshairColor(color);
}

class CPlayerSetSuitLightType : public CPointEntity
{
	DECLARE_CLASS(CPlayerSetSuitLightType, CPointEntity);
	DECLARE_DATAMAP();

public:
	bool KeyValue(KeyValueData* pkvd) override;

	void Use(CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value) override;

private:
	bool m_AllPlayers = false;
	SuitLightType m_Type = SuitLightType::Flashlight;
};

LINK_ENTITY_TO_CLASS(player_setsuitlighttype, CPlayerSetSuitLightType);

BEGIN_DATAMAP(CPlayerSetSuitLightType)
DEFINE_FIELD(m_AllPlayers, FIELD_BOOLEAN),
	DEFINE_FIELD(m_Type, FIELD_INTEGER),
	END_DATAMAP();

bool CPlayerSetSuitLightType::KeyValue(KeyValueData* pkvd)
{
	if (FStrEq(pkvd->szKeyName, "all_players"))
	{
		m_AllPlayers = atoi(pkvd->szValue) != 0;
		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "light_type"))
	{
		m_Type = static_cast<SuitLightType>(atoi(pkvd->szValue));
		return true;
	}

	return CPointEntity::KeyValue(pkvd);
}

void CPlayerSetSuitLightType::Use(CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value)
{
	const auto executor = [this](CBasePlayer* player)
	{
		player->SetSuitLightType(m_Type);
	};

	if (m_AllPlayers)
	{
		for (auto player : UTIL_FindPlayers())
		{
			executor(player);
		}
	}
	else
	{
		CBasePlayer* player = ToBasePlayer(pActivator);

		if (!player && !g_pGameRules->IsMultiplayer())
		{
			player = UTIL_GetLocalPlayer();
		}

		if (player)
		{
			executor(player);
		}
	}
}

class CPlayerCommand : public CPointEntity
{
	public:
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
};

LINK_ENTITY_TO_CLASS( player_command, CPlayerCommand );

void CPlayerCommand :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	if( FBitSet( pev->spawnflags, 1 ) )
	{
		for( auto pPlayer : UTIL_FindPlayers() )
		{
			if( pPlayer && pPlayer->IsPlayer() )
			{
				CLIENT_COMMAND( pPlayer->edict(), STRING( pev->message ) );
			}
		}
	}
	else
	{
		auto pPlayer = ToBasePlayer( pActivator );

		if( pPlayer && pPlayer->IsPlayer() )
		{
			CLIENT_COMMAND( pPlayer->edict(), STRING( pev->message ) );
		}
	}

	if( !FStringNull( pev->target ) )
	{
		FireTargets( STRING( pev->target ), pActivator, this, USE_TOGGLE, 0 );
	}
}

#define SF_PPERCENT_RESET ( 1 << 0 )

class CPlayerPercent : public CPointEntity
{
	public:
		void Spawn() override;
		bool CanFire( CBasePlayer* pPlayer );
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
};

LINK_ENTITY_TO_CLASS( player_percent, CPlayerPercent );

void CPlayerPercent :: Spawn()
{
	pev->solid = SOLID_NOT;

	pev->iuser1 = ( pev->iuser1 <= 0 ? 66 : pev->iuser1 );
	pev->iuser2 = 0;
}

bool CPlayerPercent :: CanFire( CBasePlayer* pPlayer )
{
	if( pPlayer && pPlayer->IsPlayer() )
	{
		return true;
	}
	return false;
}

void CPlayerPercent :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	auto player = ToBasePlayer( pActivator );

	if( CanFire( player ) )
	{
		if( !FStringNull( pev->message ) )
		{
			FireTargets( STRING( pev->message ), player, this, USE_TOGGLE, 0 );
		}
		pev->iuser2++;
	}

	int iPlayers = 0;

	for( auto pPlayer : UTIL_FindPlayers() )
	{
		if( pPlayer && pPlayer->IsPlayer() && pPlayer->IsConnected() )
		{
			iPlayers++;
		}
	}

	if( iPlayers > 0 )
	{
		float fPlayersTriggered = pev->iuser2;

		float CurrentPercentage = ( fPlayersTriggered / iPlayers ) * 100;

		if( CurrentPercentage >= pev->iuser1 )
		{
			if( !FStringNull( pev->target ) )
			{
				FireTargets( STRING( pev->target ), this, this, USE_TOGGLE, 0 );
			}

			if( FBitSet( pev->spawnflags, SF_PPERCENT_RESET ) )
			{
				pev->iuser2 = 0;
			}
			else
			{
				UTIL_Remove( this );
			}
		}
	}
}
