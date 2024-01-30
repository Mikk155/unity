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

#include "trigger_zone.h"

LINK_ENTITY_TO_CLASS( trigger_zone, CTriggerZone );

bool CTriggerZone :: KeyValue( KeyValueData* pkvd )
{
    if( FStrEq( pkvd->szKeyName, "m_iszEntity" ) && atoi( pkvd->szValue ) >= 0 )
    {
        m_iszEntity = pkvd->szValue;
    }
    else if( FStrEq( pkvd->szKeyName, "m_InUse" ) && atoi( pkvd->szValue ) >= 0 )
    {
        m_InUse = static_cast<USE_TYPE>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_OutUse" ) && atoi( pkvd->szValue ) >= 0 )
    {
        m_OutUse = static_cast<USE_TYPE>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_InValue" ) )
    {
        m_InValue = atof( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_OutValue" ) )
    {
        m_OutValue = atof( pkvd->szValue );
    }
    else
    {
        return CBaseEntity::KeyValue(pkvd);
    }
    return true;
}

void CTriggerZone :: Spawn()
{
    pev->solid = SOLID_NOT;
    pev->effects |= EF_NODRAW;
    pev->movetype = MOVETYPE_NONE;
	SetModel( STRING( pev->model ) );
}

void CTriggerZone :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
    if( m_iszEntity )
    {
        CBaseEntity* pEntity = NULL;

        while( ( pEntity = UTIL_FindEntityByClassname( pEntity, m_iszEntity ) ) )
        {
            if( FBitSet( pev->spawnflags, SF_TZONE_IGNORE_DEAD ) && !pEntity->IsAlive() )
                continue;

            bool i = Intersects( pEntity );
            FireTargets( STRING( ( i ? pev->message : pev->netname ) ), pEntity, this, ( i ? m_InUse : m_OutUse ), ( i ? m_InValue : m_OutValue ) );
        }
    }
    FireTargets( STRING( pev->target ), pActivator, this, m_UseType, m_UseValue );
}