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

enum class TriggerEventType
{
    None = 0,
    PLAYER_DIE = 1
};

class CTriggerEvent : public CBaseDelay
{
	DECLARE_CLASS( CTriggerEvent, CBaseDelay );
	DECLARE_DATAMAP();

public:
	void Spawn() override;
	bool KeyValue( KeyValueData* pkvd ) override;

    TriggerEventType m_pEventType = TriggerEventType::None;
};

void TriggerEvent( TriggerEventType EventType, CBaseEntity* pActivator, CBaseEntity* pCaller, float flValue );
