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

#define GAME_PRECACHE_MAX 32

class CGamePrecache : public CBaseEntity
{
	DECLARE_CLASS( CGamePrecache, CBaseEntity );
	DECLARE_DATAMAP();

	public:
		void Spawn() override;
        void Precache() override;
		bool KeyValue( KeyValueData* pkvd ) override;
        void PrecacheToArray( string_t, const char* item );

	private:
        string_t m_sMode[GAME_PRECACHE_MAX];
        string_t m_sItem[GAME_PRECACHE_MAX];
		int m_iTargets;
};

BEGIN_DATAMAP( CGamePrecache )
	DEFINE_FIELD( m_iTargets, FIELD_INTEGER ),
	DEFINE_ARRAY( m_sMode, FIELD_STRING, GAME_PRECACHE_MAX ),
	DEFINE_ARRAY( m_sItem, FIELD_STRING, GAME_PRECACHE_MAX ),
END_DATAMAP();

LINK_ENTITY_TO_CLASS( game_precache, CGamePrecache );

void CGamePrecache :: PrecacheToArray( string_t mode, const char* item )
{
    if( m_iTargets < GAME_PRECACHE_MAX )
    {
        m_sMode[ m_iTargets ] = mode;

        m_sItem[ m_iTargets ] = ALLOC_STRING( item );

        ++m_iTargets;
    }
    else
    {
        CBaseEntity::Logger->warn( "game_precache failed to add {} to precache list, max precache limit reached, use another entity.", item );
    }
}

bool CGamePrecache :: KeyValue( KeyValueData* pkvd )
{
	if( std::string_view( pkvd->szKeyName ).find( "model" ) == 0 )
	{
        PrecacheToArray( MAKE_STRING( "model" ), pkvd->szValue );
	}
	else if( std::string_view( pkvd->szKeyName ).find( "sound" ) == 0 )
	{
        PrecacheToArray( MAKE_STRING( "sound" ), pkvd->szValue );
	}
	else if( std::string_view( pkvd->szKeyName ).find( "generic" ) == 0 )
	{
        PrecacheToArray( MAKE_STRING( "generic" ), pkvd->szValue );
	}
	else if( std::string_view( pkvd->szKeyName ).find( "other" ) == 0 )
	{
        PrecacheToArray( MAKE_STRING( "other" ), pkvd->szValue );
	}
	else
	{
		return BaseClass::KeyValue( pkvd );
	}

	return true;
}

void CGamePrecache :: Precache()
{
    if( m_iTargets > 0 )
    {
        for( int i = 0; i < m_iTargets; ++i )
        {
            if( FStrEq( STRING( m_sMode[i] ), "model" ) )
            {
                PrecacheModel( STRING( m_sItem[i] ) );
            }
            else if( FStrEq( STRING( m_sMode[i] ), "sound" ) )
            {
                PrecacheSound( STRING( m_sItem[i] ) );
            }
            else if( FStrEq( STRING( m_sMode[i] ), "generic" ) )
            {
                UTIL_PrecacheGenericDirect( STRING( m_sItem[i] ) );
            }
            else if( FStrEq( STRING( m_sMode[i] ), "other" ) )
            {
                UTIL_PrecacheOther( STRING( m_sItem[i] ) );
            }
        }
    }
}

void CGamePrecache :: Spawn()
{
    Precache();
    pev->solid = SOLID_NOT;
}
