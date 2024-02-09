/***
*
*   Copyright (c) 1996-2001, Valve LLC. All rights reserved.
*
*   This product contains software technology licensed from Id
*   Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc.
*   All Rights Reserved.
*
*   Use, distribution, and modification of this source code and/or resulting
*   object code is restricted to non-commercial enhancements to products from
*   Valve LLC.  All other use, distribution, or modification is prohibited
*   without written permission from Valve LLC.
*
****/

//==================================================================
// info_precache: allow mapper to precache anything
//==================================================================

#include "cbase.h"
#include <string>

#define FLAG_PRECACHE_MAX_FILES 10

class CInfoPrecache : public CPointEntity
{
	DECLARE_CLASS( CInfoPrecache, CPointEntity );
	DECLARE_DATAMAP();

public:
    void Spawn() override;
    bool KeyValue( KeyValueData* pkvd ) override;
	int ObjectCaps() override { return CPointEntity::ObjectCaps() & ~FCAP_MUST_SPAWN; }

private:
    const char* m_szSound[FLAG_PRECACHE_MAX_FILES];
    const char* m_szSprite[FLAG_PRECACHE_MAX_FILES];
    const char* m_szModels[FLAG_PRECACHE_MAX_FILES];
    const char* m_szEntity[FLAG_PRECACHE_MAX_FILES];
    const char* m_szGeneric[FLAG_PRECACHE_MAX_FILES];
    int m_iMaxSounds, m_iMaxSprites, m_iMaxModels, m_iMaxEntities, m_iMaxGenerics;
};

LINK_ENTITY_TO_CLASS( info_precache, CInfoPrecache );

// Crash upon saving -Mikk
BEGIN_DATAMAP( CInfoPrecache )
    DEFINE_ARRAY( m_szSound, FIELD_STRING, FLAG_PRECACHE_MAX_FILES ),
    DEFINE_ARRAY( m_szSprite, FIELD_STRING, FLAG_PRECACHE_MAX_FILES ),
    DEFINE_ARRAY( m_szModels, FIELD_STRING, FLAG_PRECACHE_MAX_FILES ),
    DEFINE_ARRAY( m_szEntity, FIELD_STRING, FLAG_PRECACHE_MAX_FILES ),
    DEFINE_ARRAY( m_szGeneric, FIELD_STRING, FLAG_PRECACHE_MAX_FILES ),
END_DATAMAP();

bool CInfoPrecache :: KeyValue( KeyValueData* pkvd )
{
    if( !pkvd->szValue || !pkvd->szKeyName )
    {
        return false;
    }

    std::string m_Type = std::string( pkvd->szKeyName );

    if( m_Type.find( "other_" ) == 0 )
    {
        if( m_iMaxEntities < FLAG_PRECACHE_MAX_FILES )
        {
            m_szEntity[ m_iMaxEntities ] = pkvd->szValue;
            m_iMaxEntities++;
            return true;
        }
        else
        {
            UTIL_PrecacheOther( pkvd->szValue );
        }
    }
    else if( m_Type.find( "model_" ) == 0 )
    {
        if( m_iMaxModels < FLAG_PRECACHE_MAX_FILES )
        {
            m_szModels[ m_iMaxModels ] = pkvd->szValue;
            m_iMaxModels++;
            return true;
        }
        else
        {
            UTIL_PrecacheModel( pkvd->szValue );
        }
    }
    else if( m_Type.find( "sprite_" ) == 0 )
    {
        if( m_iMaxSprites < FLAG_PRECACHE_MAX_FILES )
        {
            m_szSprite[ m_iMaxSprites ] = pkvd->szValue;
            m_iMaxSprites++;
            return true;
        }
        else
        {
            UTIL_PrecacheModel( pkvd->szValue );
            UTIL_PrecacheGenericDirect( pkvd->szValue );
        }
    }
    else if( m_Type.find( "generic_" ) == 0 )
    {
        if( m_iMaxGenerics < FLAG_PRECACHE_MAX_FILES )
        {
            m_szGeneric[ m_iMaxGenerics ] = pkvd->szValue;
            m_iMaxGenerics++;
            return true;
        }
        else
        {
            UTIL_PrecacheGenericDirect( pkvd->szValue );
        }
    }
    else if( m_Type.find( "sound_" ) == 0 )
    {
        if( m_iMaxSounds < FLAG_PRECACHE_MAX_FILES )
        {
            m_szSound[ m_iMaxSounds ] = pkvd->szValue;
            m_iMaxSounds++;
            return true;
        }
        else
        {
            UTIL_PrecacheSound( pkvd->szValue );
        }
    }

    CBaseEntity::Logger->warn("Max precache limit {} reached. we're precaching \"{}\" now but it won't be in saverestore.", FLAG_PRECACHE_MAX_FILES, pkvd->szValue );
    return false;
}

void CInfoPrecache :: Spawn()
{
    for( int i = 0; i < m_iMaxSounds; i++ )
    {
        if( m_szSound[i] )
            UTIL_PrecacheSound( m_szSound[i] );
    }
    for( int i = 0; i < m_iMaxGenerics; i++ )
    {
        if( m_szGeneric[i] )
            UTIL_PrecacheGenericDirect( m_szGeneric[i] );
    }
    for( int i = 0; i < m_iMaxSprites; i++ )
    {
        if( m_szSprite[i] )
        {
            UTIL_PrecacheModel( m_szSprite[i] );
            UTIL_PrecacheGenericDirect( m_szSprite[i] );
        }
    }
    for( int i = 0; i < m_iMaxModels; i++ )
    {
        if( m_szModels[i] )
            UTIL_PrecacheModel( m_szModels[i] );
    }
    for( int i = 0; i < m_iMaxEntities; i++ )
    {
        if( m_szEntity[i] )
            UTIL_PrecacheOther( m_szEntity[i] );
    }
}