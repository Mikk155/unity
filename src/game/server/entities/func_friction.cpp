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

#include "func_friction.h"

LINK_ENTITY_TO_CLASS( func_friction, CFrictionModifier );

BEGIN_DATAMAP( CFrictionModifier )
	DEFINE_FIELD( m_frictionFraction, FIELD_FLOAT ),
	DEFINE_FUNCTION( ChangeFriction ),
END_DATAMAP();

void CFrictionModifier :: Spawn()
{
	pev->solid = SOLID_TRIGGER;
	SetBBox();
	pev->movetype = MOVETYPE_NONE;
	SetTouch(&CFrictionModifier::ChangeFriction);
}

void CFrictionModifier :: ChangeFriction(CBaseEntity* pOther)
{
	if( pOther->pev->movetype != MOVETYPE_BOUNCEMISSILE && pOther->pev->movetype != MOVETYPE_BOUNCE )
		pOther->pev->friction = m_frictionFraction;
}

bool CFrictionModifier :: KeyValue( KeyValueData* pkvd )
{
	if( FStrEq( pkvd->szKeyName, "modifier" ) )
	{
		m_frictionFraction = atof(pkvd->szValue) / 100.0;
		return true;
	}

	return CBaseEntity::KeyValue(pkvd);
}