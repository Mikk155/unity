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

#define SF_TSETORIGIN_CONS          ( 1 << 0 ) // Will constantly update position if set.
#define SF_TSETORIGIN_STON          ( 1 << 1 ) // Starts on, starts iterating once the entity spawns
#define SF_TSETORIGIN_ONCE          ( 1 << 2 ) // Trigger_setorigin entity will be removed after it sets the target's origin.
#define SF_TSETORIGIN_LOFS          ( 1 << 3 ) // When first run save the offset between the target entity and the copy pointer, apply offset when updating the target entity's position
#define SF_TSETORIGIN_CXAN          ( 1 << 4 ) // Copy X Angle
#define SF_TSETORIGIN_CYAN          ( 1 << 5 ) // Copy Y Angle
#define SF_TSETORIGIN_CZAN          ( 1 << 6 ) // Copy Z Angle
#define SF_TSETORIGIN_CXAX          ( 1 << 7 ) // Copy X Axis
#define SF_TSETORIGIN_CYAX          ( 1 << 8 ) // Copy Y Axis
#define SF_TSETORIGIN_CZAX          ( 1 << 9 ) // Copy Z Axis

#define FLAG_TSETORIGIN_OWNER_NONE 0    // Do nothing
#define FLAG_TSETORIGIN_OWNER_COPY 1    // Set copy pointer as target's owner
#define FLAG_TSETORIGIN_OWNER_TARG 2    // Set target pointer as copy's owner

// Set the origin of an entity dynamically
class CTriggerSetOrigin : public CPointEntity
{
	DECLARE_CLASS( CTriggerSetOrigin, CPointEntity );
	DECLARE_DATAMAP();

public:
    void Spawn() override;
    void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
    void SetOrigin();

    CBaseEntity* pPointerCopy()
    {
        if( !hPointerCopy.Get() )
            hPointerCopy = UTIL_FindEntityByTargetname( NULL, STRING( copypointer ) );
        return hPointerCopy.Get();
    };

    CBaseEntity* pPointerTarg()
    {
        if( !hPointerTarg.Get() )
            hPointerTarg = UTIL_FindEntityByTargetname( NULL, STRING( targpointer ) );
        return hPointerTarg.Get();
    };

    Vector VecOffSet;   // Off set difference by SF_TSETORIGIN_LOFS


private:
    int invert_x;           // Invert X Angle
    int invert_y;           // Invert Y Angle
    int invert_z;           // Invert Z Angle
    int whosowner;          // Set owner to one, other or none.
    Vector angleoffset;     // Applied once on first use, After first use - Applied if "constant" flag is checked, and for each "Copy [x, y, z] Angle" checked.
    Vector originoffset;    // Manual Offset to copied coordinates
    string_t copypointer;   // The entity we wish to copy coordinates/angles from
    string_t targpointer;   // The entity we wish to paste coordinates/angles to
    EHANDLE hPointerCopy;
    EHANDLE hPointerTarg;
};