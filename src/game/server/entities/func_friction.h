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

#pragma once

class CFrictionModifier : public CBaseEntity
{
	DECLARE_CLASS( CFrictionModifier, CBaseEntity );
	DECLARE_DATAMAP();

public:
	void Spawn() override;
	bool KeyValue( KeyValueData* pkvd ) override;
	void ChangeFriction( CBaseEntity* pOther );
	int ObjectCaps() override { return CBaseEntity::ObjectCaps() & ~FCAP_ACROSS_TRANSITION; }
	float m_frictionFraction; // Sorry, couldn't resist this name :)
};