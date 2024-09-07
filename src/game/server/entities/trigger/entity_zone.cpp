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

#include "cbase.h"

class CTriggerZone : public CBaseEntity
{
	DECLARE_CLASS( CTriggerZone, CBaseEntity );
	DECLARE_DATAMAP();

    public:
        void Spawn() override;
        bool KeyValue( KeyValueData* pkvd ) override;
        void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;

    private:
        string_t m_iszEntity;    // classname of the entities for iterating
        USE_TYPE m_InUse = USE_TOGGLE;
        float m_InValue;
        USE_TYPE m_OutUse = USE_TOGGLE;
        float m_OutValue;
};


BEGIN_DATAMAP( CTriggerZone )
    DEFINE_FIELD( m_InUse, FIELD_INTEGER ),
    DEFINE_FIELD( m_InValue, FIELD_FLOAT ),
    DEFINE_FIELD( m_OutUse, FIELD_INTEGER ),
    DEFINE_FIELD( m_OutValue, FIELD_FLOAT ),
    DEFINE_FIELD( m_iszEntity, FIELD_STRING ),
END_DATAMAP();

LINK_ENTITY_TO_CLASS( trigger_zone, CTriggerZone );

bool CTriggerZone :: KeyValue( KeyValueData* pkvd )
{
    if( FStrEq( pkvd->szKeyName, "m_iszEntity" ) )
    {
        m_iszEntity = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_InUse" ) )
    {
        m_InUse = static_cast<USE_TYPE>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_OutUse" ) )
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
    if( !FStringNull( m_iszEntity ) )
    {
        CBaseEntity* pEntity = NULL;

        while( ( pEntity = UTIL_FindEntityByClassname( pEntity, STRING( m_iszEntity ) ) ) )
        {
            bool i = Intersects( pEntity );
            FireTargets( STRING( ( i ? pev->message : pev->netname ) ), pEntity, this, ( i ? m_InUse : m_OutUse ), ( i ? m_InValue : m_OutValue ) );
        }
    }
    FireTargets( STRING( pev->target ), pActivator, this, USE_TOGGLE, 0 );
}
