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

//==================================================================
// info_precache: allow mapper to precache anything
//==================================================================

#include "cbase.h"
#include <string>

class CInfoPrecache : public CPointEntity
{
public:
    void Spawn() override;
    bool KeyValue( KeyValueData* pkvd ) override;
};

LINK_ENTITY_TO_CLASS( info_precache, CInfoPrecache );

bool CInfoPrecache :: KeyValue( KeyValueData* pkvd )
{
    if( !pkvd->szValue || !pkvd->szKeyName )
    {
        return false;
    }

    std::string m_Type = std::string( pkvd->szKeyName );

    if( m_Type.find( "other" ) == 0 )
    {
        UTIL_PrecacheOther( pkvd->szValue );
    }
    else if( m_Type.find( "model" ) == 0 || m_Type.find( "sprite" ) == 0 )
    {
        UTIL_PrecacheModel( pkvd->szValue );
    }
    else if( m_Type.find( "generic" ) == 0 )
    {
        UTIL_PrecacheGenericDirect( pkvd->szValue );
    }
    else if( m_Type.find( "sound" ) == 0 )
    {
        UTIL_PrecacheSound( pkvd->szValue );
    }
    else
    {
        return false;
    }
    return true;
}

void CInfoPrecache :: Spawn()
{
    SetBits( pev->flags, FL_KILLME );
}