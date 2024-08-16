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

#include "CKeyValueLogic.h"

BEGIN_DATAMAP( CKeyValueLogic )
    DEFINE_FIELD( m_sTargetEntity, FIELD_STRING ),
    DEFINE_FIELD( m_sSourceEntity, FIELD_STRING ),
    DEFINE_FIELD( m_sSourceKeyName, FIELD_STRING ),
    DEFINE_FIELD( m_sKeyName, FIELD_STRING ),
    DEFINE_FIELD( m_sValue, FIELD_STRING ),
    DEFINE_FIELD( m_iSetType, FIELD_INTEGER ),
    DEFINE_FIELD( m_iAppendSpaces, FIELD_INTEGER ),
    DEFINE_FIELD( m_SkipVector, FIELD_INTEGER ),
    DEFINE_FIELD( m_iMaxTargets, FIELD_INTEGER ),
    DEFINE_FIELD( m_iCurrentTarget, FIELD_INTEGER ),
    DEFINE_FIELD( m_FloatConversion, FIELD_INTEGER ),
END_DATAMAP();

void CKeyValueLogic :: Spawn()
{
    pev->solid = SOLID_NOT;
}

bool CKeyValueLogic :: KeyValue( KeyValueData* pkvd )
{
    if( FStrEq( pkvd->szKeyName, "m_sTargetEntity" ) )
    {
        m_sTargetEntity = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sSourceEntity" ) )
    {
        m_sSourceEntity = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sKeyName" ) )
    {
        m_sKeyName = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sSourceKeyName" ) )
    {
        m_sSourceKeyName = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sValue" ) )
    {
        m_sValue = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_iSetType" ) )
    {
        m_iSetType = static_cast<KeyValueMath>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_FloatConversion" ) )
    {
        m_FloatConversion = static_cast<KeyValueFloatConversion>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_iMaxTargets" ) )
    {
        m_iMaxTargets = atoi( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_iAppendSpaces" ) )
    {
        m_iAppendSpaces = atoi( pkvd->szValue );
    }
    else if( std::string( pkvd->szValue ).find( "m_SkipVector_" ) == 0 )
    {
        if( atoi( pkvd->szValue ) == 1 )
        {
            if( FStrEq( pkvd->szValue, "m_SkipVector_X" ) )
            {
                m_SkipVector |= KeyValueVector::X;
            }
            else if( FStrEq( pkvd->szValue, "m_SkipVector_Y" ) )
            {
                m_SkipVector |= KeyValueVector::Y;
            }
            else if( FStrEq( pkvd->szValue, "m_SkipVector_Z" ) )
            {
                m_SkipVector |= KeyValueVector::Z;
            }
        }
    }
    else
    {
        return BaseClass::KeyValue( pkvd );
    }
    return true;
}

void CKeyValueLogic :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
    if( !FStringNull( pev->target ) )
        FireTargets( STRING( pev->target ), pActivator, this, USE_TOGGLE, value );
}

string_t CKeyValueLogic :: GetValue( CBaseEntity* pActivator, CBaseEntity* pCaller )
{
    if( !FStringNull( m_sSourceEntity ) )
    {
        if( auto entity = UTIL_FindEntityByTargetname( nullptr, STRING( m_sSourceEntity ), pActivator, pCaller ); entity != nullptr )
        {
            return ALLOC_STRING( entity->GetKeyValue( STRING( m_sSourceKeyName ), std::string( STRING( m_sValue ) ) ).c_str() );
        }
    }

    return m_sValue;
}

CBaseEntity* CKeyValueLogic :: GetTarget( CBaseEntity* pActivator, CBaseEntity* pCaller )
{
    m_iCurrentTarget++;

    if( m_iCurrentTarget > m_iMaxTargets )
    {
        pLastFind = nullptr;
        m_iCurrentTarget = 0;
    }
    else
    {
        pLastFind = UTIL_FindEntityByTargetname( pLastFind, STRING( m_sTargetEntity ), pActivator, pCaller );
    }

    return pLastFind;
}
