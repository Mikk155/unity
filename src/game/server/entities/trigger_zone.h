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

//***********************************************************
// trigger_zone is a entity that when fired, will fire it's target depending if certain entities are in or outside the volumen
//***********************************************************

#include "extdll.h"
#include "util.h"
#include "cbase.h"

#pragma once

#define SF_TZONE_IGNORE_DEAD ( 1 << 0 )

class CTriggerZone : public CBaseEntity
{
public:
    void Spawn() override;
	bool KeyValue( KeyValueData* pkvd ) override;
	void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
    const char* m_iszEntity;    // classname of the entities for iterating
	USE_TYPE m_InUse = USE_TOGGLE;
	float m_InValue;
	USE_TYPE m_OutUse = USE_TOGGLE;
	float m_OutValue;
};