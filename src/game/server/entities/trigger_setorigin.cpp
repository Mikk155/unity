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

#include "trigger_setorigin.h"

LINK_ENTITY_TO_CLASS( trigger_setorigin, CTriggerSetOrigin );

BEGIN_DATAMAP( CTriggerSetOrigin )
    DEFINE_FIELD( invert_x, FIELD_INTEGER ),
    DEFINE_FIELD( invert_y, FIELD_INTEGER ),
    DEFINE_FIELD( invert_z, FIELD_INTEGER ),
    DEFINE_FIELD( copypointer, FIELD_STRING ),
    DEFINE_FIELD( targpointer, FIELD_STRING ),
    DEFINE_FIELD( angleoffset, FIELD_VECTOR ),
    DEFINE_FIELD( originoffset, FIELD_VECTOR ),
    DEFINE_FIELD( hPointerCopy, FIELD_EHANDLE ),
    DEFINE_FIELD( hPointerTarg, FIELD_EHANDLE ),
	DEFINE_FUNCTION( SetOrigin ),
END_DATAMAP();

void CTriggerSetOrigin :: Spawn()
{
    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_STON ) )
    {
        SetThink(&CTriggerSetOrigin::SetOrigin);
        pev->nextthink = gpGlobals->time + 0.1;
    }
}

void CTriggerSetOrigin :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
    // Support !caller and !activator upon triggering
    if( FStrEq( STRING( copypointer ), "!activator" ) ) hPointerCopy = pActivator;
    else if( FStrEq( STRING( copypointer ), "!caller" ) ) hPointerCopy = pCaller;
    if( FStrEq( STRING( targpointer ), "!activator" ) ) hPointerTarg = pActivator;
    else if( FStrEq( STRING( targpointer ), "!caller" ) ) hPointerTarg = pCaller;

    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_STON ) )
    {
        SetThink(&CTriggerSetOrigin::SetOrigin);
        pev->nextthink = gpGlobals->time + 0.1;
    }
    else
    {
        SetOrigin();
    }
}

void CTriggerSetOrigin :: SetOrigin()
{
    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_CONS ) )
    {
        pev->nextthink = gpGlobals->time;
    }

    if( !pPointerCopy() || !pPointerTarg() )
    {
        return;
    }

    switch( whosowner )
    {
        case FLAG_TSETORIGIN_OWNER_COPY:
            pPointerTarg()->SetOwner( pPointerCopy() );
        break;

        case FLAG_TSETORIGIN_OWNER_TARG:
            pPointerCopy()->SetOwner( pPointerTarg() );
        break;
    }

    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_LOFS ) )
    {
        VecOffSet = ( pPointerTarg()->pev->origin - pPointerCopy()->pev->origin );
        ClearBits( pev->spawnflags, SF_TSETORIGIN_LOFS );
    }

    Vector Destination = pPointerCopy()->pev->origin + VecOffSet + originoffset;

    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_CXAX ) )
    {
        pPointerTarg()->pev->origin.x = Destination.x;
    }
    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_CYAX ) )
    {
        pPointerTarg()->pev->origin.y = Destination.y;
    }
    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_CZAX ) )
    {
        pPointerTarg()->pev->origin.z = Destination.z;
    }

    // -Copyangles + offset -Mikk

    if( FBitSet( pev->spawnflags, SF_TSETORIGIN_ONCE ) )
    {
        UTIL_Remove( this );
    }
}