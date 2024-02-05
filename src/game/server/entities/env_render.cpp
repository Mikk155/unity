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

#include "env_render.h"

LINK_ENTITY_TO_CLASS( env_render, CRenderFxManager );

void CRenderFxManager :: Spawn()
{
	pev->solid = SOLID_NOT;
}

void CRenderFxManager :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	CBaseEntity* pTarget = nullptr;

	while( ( pTarget = UTIL_FindEntityByTargetname( pTarget, STRING( pev->target ), pActivator, pCaller ) ) )
	{
		if( !FBitSet( pev->spawnflags, SF_RENDER_MASKFX ) )
		{
			pTarget->pev->renderfx = pev->renderfx;
		}
		if( !FBitSet( pev->spawnflags, SF_RENDER_MASKAMT ) )
		{
			pTarget->pev->renderamt = pev->renderamt;
		}
		if( !FBitSet( pev->spawnflags, SF_RENDER_MASKMODE ) )
		{
			pTarget->pev->rendermode = pev->rendermode;
		}
		if( !FBitSet( pev->spawnflags, SF_RENDER_MASKCOLOR ) )
		{
			pTarget->pev->rendercolor = pev->rendercolor;
		}
	}
}