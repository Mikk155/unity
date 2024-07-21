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

#include "trigger_event.h"

BEGIN_DATAMAP( CTriggerEvent )
	DEFINE_FIELD( m_pEventType, FIELD_INTEGER ),
END_DATAMAP();

LINK_ENTITY_TO_CLASS( trigger_event, CTriggerEvent );

void CTriggerEvent :: Spawn()
{
	pev->solid = SOLID_NOT;
}

bool CTriggerEvent :: KeyValue( KeyValueData* pkvd )
{
	if( FStrEq( pkvd->szKeyName, "event_type" ) )
	{
		m_pEventType = static_cast<TriggerEventType>( atoi( pkvd->szValue ) );
	}
	else
	{
		return BaseClass::KeyValue( pkvd );
	}

	return true;
}

void TriggerEvent( TriggerEventType EventType, CBaseEntity* pActivator, CBaseEntity* pCaller, float flValue )
{
	for( auto handler : UTIL_FindEntitiesByClassname<CTriggerEvent>( "trigger_event" ) )
	{
		if( handler->m_pEventType == EventType && handler->m_pEventType != TriggerEventType::None )
		{
			handler->SUB_UseTargets( handler->AllocNewActivator( pActivator, pCaller ), USE_TOGGLE, flValue );
		}
	}
}