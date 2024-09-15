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

/**
 *	@file
 *	frequently used global functions
 */

#include "cbase.h"
#include "nodes.h"
#include "doors.h"

void CPointEntity::Spawn()
{
	pev->solid = SOLID_NOT;
	//	SetSize(g_vecZero, g_vecZero);
}

/**
 *	@brief Null Entity, remove on startup
 */
class CNullEntity : public CBaseEntity
{
public:
	void Spawn() override;
};

void CNullEntity::Spawn()
{
	REMOVE_ENTITY(edict());
}

LINK_ENTITY_TO_CLASS(info_null, CNullEntity);

void CBaseEntity::UpdateOnRemove()
{
	// tell owner (if any) that we're dead.This is mostly for MonsterMaker functionality.
	MaybeNotifyOwnerOfDeath();

	if (FBitSet(pev->flags, FL_GRAPHED))
	{
		// this entity was a LinkEnt in the world node graph, so we must remove it from
		// the graph since we are removing it from the world.
		for (int i = 0; i < WorldGraph.m_cLinks; i++)
		{
			if (WorldGraph.m_pLinkPool[i].m_pLinkEnt == pev)
			{
				// if this link has a link ent which is the same ent that is removing itself, remove it!
				WorldGraph.m_pLinkPool[i].m_pLinkEnt = nullptr;
			}
		}
	}
	if (!FStringNull(pev->globalname))
		gGlobalState.EntitySetState(pev->globalname, GLOBAL_DEAD);
}

void CBaseEntity::SUB_Remove()
{
	UpdateOnRemove();
	if (pev->health > 0)
	{
		// this situation can screw up monsters who can't tell their entity pointers are invalid.
		pev->health = 0;
		Logger->debug("SUB_Remove called on entity \"{}\" ({}) with health > 0", STRING(pev->targetname), STRING(pev->classname));
	}

	REMOVE_ENTITY(edict());
}

BEGIN_DATAMAP(CBaseDelay)
DEFINE_FIELD(m_flDelay, FIELD_FLOAT),
	DEFINE_FIELD(m_iszKillTarget, FIELD_STRING),
	DEFINE_FUNCTION(DelayThink),
	END_DATAMAP();

bool CBaseDelay::KeyValue(KeyValueData* pkvd)
{
	if (FStrEq(pkvd->szKeyName, "delay"))
	{
		m_flDelay = atof(pkvd->szValue);
		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "killtarget"))
	{
		m_iszKillTarget = ALLOC_STRING(pkvd->szValue);
		return true;
	}

	return CBaseEntity::KeyValue(pkvd);
}

void CBaseEntity::SUB_UseTargets(CBaseEntity* pActivator, USE_TYPE useType, float value)
{
	if (!FStringNull(pev->target))
	{
		FireTargets(STRING(pev->target), pActivator, this, useType, value);
	}
}

void FireTargets(const char* targetName, CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value)
{
	if( !targetName )
		return;

	// If has semicolon then it's multiple targets
	if( std::string( targetName ).find( ";" ) != std::string::npos )
	{
		CBaseEntity::IOLogger->debug( "[FireTargets] Firing multi-targets: ({})", targetName );

		const int MAX_SPLIT_TARGETS = 8;

		std::string szSplit[ MAX_SPLIT_TARGETS ];

		std::istringstream iss( targetName );
		std::string token;
		int i = 0;

		while( std::getline( iss, token, ';' ) && i < MAX_SPLIT_TARGETS ) {
			szSplit[i++] = token;
		}

		if( i == 0 ) {
			szSplit[0] = targetName;
			i = 1;
		}

		for( int j = 0; j < i; ++j ) {
			if( auto m_szTarget = szSplit[j].c_str(); m_szTarget )
				FireTargets( m_szTarget, pActivator, pCaller, useType, value );
		}

		return;
	}

	CBaseEntity::IOLogger->debug("[FireTargets] Firing: ({})", targetName );

	// Lambda used for debugging purposes
	auto lUseType = []( USE_TYPE UseType ) -> std::string
	{
		switch( UseType )
		{
			case USE_OFF:		return "USE_OFF (0)";
			case USE_ON:		return "USE_ON (1)";
			case USE_SET:		return "USE_SET (2)";
			case USE_TOGGLE:	return "USE_TOGGLE (3)";
			case USE_KILL:		return "USE_KILL (4)";
			case USE_SAME:		return "USE_SAME (5)";
			case USE_OPPOSITE:	return "USE_OPPOSITE (6)";
			case USE_TOUCH:		return "USE_TOUCH (7)";
			case USE_LOCK:		return "USE_LOCK (8)";
			case USE_UNLOCK:	return "USE_UNLOCK (9)";
		}
		return "USE_UNKNOWN";
	};

	auto lUseName = []( CBaseEntity* pEnt ) -> const char* {
		return pEnt != nullptr ? ( pEnt->IsPlayer() ? STRING( pEnt->pev->netname ) :
			!FStringNull( pEnt->pev->targetname ) ? STRING( pEnt->pev->targetname ) :
				STRING( pEnt->pev->classname ) ) : "NULL";
	};

	auto lUseLock = []( int value ) -> std::string
	{
		return ( value == 0 ? "USE_VALUE_UNKNOWN" : 
			fmt::format( "( {}{}{}{} )",
				( FBitSet( value, USE_VALUE_MASTER ) ? "Master " : "" ),
				( FBitSet( value, USE_VALUE_TOUCH ) ? "Touch " : "" ),
				( FBitSet( value, USE_VALUE_USE ) ? "Use " : "" ),
				( FBitSet( value, USE_VALUE_THINK ) ? "Think " : "" )
			)
		);
	};

	if( pCaller->m_UseValue ) // Override if specified
		value = pCaller->m_UseValue;

	CBaseEntity* target = nullptr;

	while( ( target = UTIL_FindEntityByTargetname( target, targetName, pActivator, pCaller ) ) != nullptr )
	{
		if( !target || FBitSet( target->pev->flags, FL_KILLME ) ) {
			continue; // Don't use dying ents
		}

		if( target->ClassnameIs( "trigger_usecheck" ) ) {
			target->Use( pActivator, pCaller, ( pCaller->m_UseType > USE_UNSET ? pCaller->m_UseType : useType ), value );
			continue; // Call trigger_usecheck with the exact USE_TYPE
		}

		if( FBitSet( target->m_UseLocked, USE_VALUE_USE ) && pCaller->m_UseType != USE_UNLOCK ) {
			continue; // Do this check in here instead so if USE_UNLOCK is sent we catch it
		}

		const char* ClassName = STRING( target->pev->classname );

		// if custom USE_TYPE is sent then let's hack it here :D
		if( pCaller != nullptr && pCaller->m_UseType > USE_UNSET && pCaller->m_UseType < USE_UNKNOWN )
		{
			target->m_UseTypeLast = pCaller->m_UseType; // Get the USE_TYPE that the caller received.

			// This stuff "blocks" a entity, just like a multisource could, for example.
			if( pCaller->m_UseType == USE_LOCK || pCaller->m_UseType == USE_UNLOCK )
			{
				if( int UseValue = (int)value; UseValue > 0 )
				{
					if( pCaller->m_UseType == USE_UNLOCK )
					{
						CBaseEntity::IOLogger->debug( "{} {}->{} Un-Locked. will receive calls now",
							ClassName, targetName, lUseLock( UseValue ) );

						ClearBits( target->m_UseLocked, UseValue );
					}
					else
					{
						CBaseEntity::IOLogger->debug( "{} {}->{} Locked. won't receive any calls until get {}",
							ClassName, targetName, lUseLock( UseValue ), lUseType( USE_UNLOCK ) );

						SetBits( target->m_UseLocked, UseValue );
					}
				}
			}
			else if( pCaller->m_UseType == USE_TOUCH && !FBitSet( target->m_UseLocked, USE_VALUE_TOUCH ) )
			{
				CBaseEntity::IOLogger->debug( "{} {}->Touch( {} )",
					ClassName, targetName, lUseName( pActivator ) );

				target->m_UseTypeLast = USE_TOUCH;
				target->Touch( pActivator );
			}
			else if( pCaller->m_UseType == USE_KILL )
			{
				CBaseEntity::IOLogger->debug( "{} {}->UpdateOnRemove()",
					ClassName, targetName );

				target->m_UseTypeLast = USE_KILL;
				UTIL_Remove( target );
			}
			else
			{
				// Get the USE_TYPE that caller received.
				if( pCaller->m_UseType == USE_SAME )
				{
					target->m_UseTypeLast = pCaller->m_UseTypeLast;
					//target->m_UseTypeLast = ( pCaller->m_UseTypeLast != USE_SAME && pCaller->m_UseTypeLast != USE_OPPOSITE ? pCaller->m_UseTypeLast : USE_TOGGLE );

					CBaseEntity::IOLogger->debug( "{} {}->Use( {}, {}, {} > {}, {} )",
						ClassName, targetName, lUseName( pActivator ), lUseName( pCaller ), lUseType( pCaller->m_UseType ), lUseType( target->m_UseTypeLast ), value );
				}
				// Switch between USE_OFF and USE_ON, else just send USE_TOGGLE
				else if( pCaller->m_UseType == USE_OPPOSITE )
				{
					target->m_UseTypeLast = (
						pCaller->m_UseTypeLast == USE_ON ? USE_OFF : pCaller->m_UseTypeLast == USE_OFF ? USE_ON :
						pCaller->m_UseTypeLast == USE_LOCK ? USE_UNLOCK : pCaller->m_UseTypeLast == USE_UNLOCK ? USE_LOCK :
						USE_TOGGLE
					);

					CBaseEntity::IOLogger->debug( "{} {}->Use( {}, {}, {} > {}, {} )",
						ClassName, targetName, lUseName( pActivator ), lUseName( pCaller ), lUseType( pCaller->m_UseType ), lUseType( target->m_UseTypeLast ), value );
				}

				target->Use( pActivator, pCaller, target->m_UseTypeLast, value );
			}
		}
		else
		{
			CBaseEntity::IOLogger->debug( "{} {}->Use( {}, {}, {}, {} )",
				ClassName, targetName, lUseName( pActivator ), lUseName( pCaller ), lUseType( useType ), value );

			target->m_UseTypeLast = useType;
			target->Use( pActivator, pCaller, useType, value );
		}
	}
}

LINK_ENTITY_TO_CLASS(delayed_use, CBaseDelay);

void CBaseDelay::SUB_UseTargets(CBaseEntity* pActivator, USE_TYPE useType, float value)
{
	//
	// exit immediatly if we don't have a target or kill target
	//
	if (FStringNull(pev->target) && FStringNull(m_iszKillTarget))
		return;

	//
	// check for a delay
	//
	if (m_flDelay != 0)
	{
		// create a temp object to fire at a later time
		CBaseDelay* pTemp = g_EntityDictionary->Create<CBaseDelay>("delayed_use");

		pTemp->pev->nextthink = gpGlobals->time + m_flDelay;

		pTemp->SetThink(&CBaseDelay::DelayThink);

		// Save the useType
		pTemp->m_UseType = m_UseType;
		pTemp->m_UseTypeLast = m_UseTypeLast;
		pTemp->m_UseValue = m_UseValue;
		pTemp->pev->button = (int)useType;
		pTemp->m_iszKillTarget = m_iszKillTarget;
		pTemp->m_flDelay = 0; // prevent "recursion"
		pTemp->pev->target = pev->target;
		pTemp->m_hActivator = pActivator;

		return;
	}

	//
	// kill the killtargets
	//

	if (!FStringNull(m_iszKillTarget))
	{
		CBaseEntity::IOLogger->debug("KillTarget: {}", STRING(m_iszKillTarget));

		CBaseEntity* killTarget = nullptr;

		while ((killTarget = UTIL_FindEntityByTargetname(killTarget, STRING(m_iszKillTarget), pActivator, this)) != nullptr)
		{
			if (UTIL_IsRemovableEntity(killTarget))
			{
				UTIL_Remove(killTarget);
				CBaseEntity::IOLogger->debug("killing {}", STRING(killTarget->pev->classname));
			}
			else
			{
				CBaseEntity::IOLogger->debug("Can't kill \"{}\": not allowed to remove entities of this type",
					STRING(killTarget->pev->classname));
			}
		}
	}

	//
	// fire targets
	//
	if (!FStringNull(pev->target))
	{
		FireTargets(GetTarget(), pActivator, this, useType, value);
	}
}

void CBaseDelay::DelayThink()
{
	// If a player activated this on delay
	CBaseEntity* pActivator = m_hActivator;

	// The use type is cached (and stashed) in pev->button
	SUB_UseTargets(pActivator, (USE_TYPE)pev->button, 0);
	REMOVE_ENTITY(edict());
}

BEGIN_DATAMAP(CBaseToggle)
DEFINE_FIELD(m_toggle_state, FIELD_INTEGER),
	DEFINE_FIELD(m_flActivateFinished, FIELD_TIME),
	DEFINE_FIELD(m_flMoveDistance, FIELD_FLOAT),
	DEFINE_FIELD(m_flWait, FIELD_FLOAT),
	DEFINE_FIELD(m_flLip, FIELD_FLOAT),
	DEFINE_FIELD(m_vecPosition1, FIELD_POSITION_VECTOR),
	DEFINE_FIELD(m_vecPosition2, FIELD_POSITION_VECTOR),
	DEFINE_FIELD(m_vecAngle1, FIELD_VECTOR), // UNDONE: Position could go through transition, but also angle?
	DEFINE_FIELD(m_vecAngle2, FIELD_VECTOR), // UNDONE: Position could go through transition, but also angle?
	DEFINE_FIELD(m_pfnCallWhenMoveDone, FIELD_FUNCTIONPOINTER),
	DEFINE_FIELD(m_vecFinalDest, FIELD_POSITION_VECTOR),
	DEFINE_FIELD(m_vecFinalAngle, FIELD_VECTOR),
	DEFINE_FUNCTION(LinearMoveDone),
	DEFINE_FUNCTION(AngularMoveDone),
	END_DATAMAP();

bool CBaseToggle::KeyValue(KeyValueData* pkvd)
{
	if (FStrEq(pkvd->szKeyName, "lip"))
	{
		m_flLip = atof(pkvd->szValue);
		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "wait"))
	{
		m_flWait = atof(pkvd->szValue);
		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "distance"))
	{
		m_flMoveDistance = atof(pkvd->szValue);
		return true;
	}

	return CBaseDelay::KeyValue(pkvd);
}

void CBaseToggle::LinearMove(Vector vecDest, float flSpeed)
{
	ASSERTSZ(flSpeed != 0, "LinearMove:  no speed is defined!");
	//	ASSERTSZ(m_pfnCallWhenMoveDone != nullptr, "LinearMove: no post-move function defined");

	m_vecFinalDest = vecDest;

	// Already there?
	if (vecDest == pev->origin)
	{
		LinearMoveDone();
		return;
	}

	// set destdelta to the vector needed to move
	Vector vecDestDelta = vecDest - pev->origin;

	// divide vector length by speed to get time to reach dest
	float flTravelTime = vecDestDelta.Length() / flSpeed;

	// set nextthink to trigger a call to LinearMoveDone when dest is reached
	pev->nextthink = pev->ltime + flTravelTime;
	SetThink(&CBaseToggle::LinearMoveDone);

	// scale the destdelta vector by the time spent traveling to get velocity
	pev->velocity = vecDestDelta / flTravelTime;
}

void CBaseToggle::LinearMoveDone()
{
	Vector delta = m_vecFinalDest - pev->origin;
	float error = delta.Length();
	if (error > 0.03125)
	{
		LinearMove(m_vecFinalDest, 100);
		return;
	}

	SetOrigin(m_vecFinalDest);
	pev->velocity = g_vecZero;
	pev->nextthink = -1;
	if (m_pfnCallWhenMoveDone)
		(this->*m_pfnCallWhenMoveDone)();
}

void CBaseToggle::AngularMove(Vector vecDestAngle, float flSpeed)
{
	ASSERTSZ(flSpeed != 0, "AngularMove:  no speed is defined!");
	//	ASSERTSZ(m_pfnCallWhenMoveDone != nullptr, "AngularMove: no post-move function defined");

	m_vecFinalAngle = vecDestAngle;

	// Already there?
	if (vecDestAngle == pev->angles)
	{
		AngularMoveDone();
		return;
	}

	// set destdelta to the vector needed to move
	Vector vecDestDelta = vecDestAngle - pev->angles;

	// divide by speed to get time to reach dest
	float flTravelTime = vecDestDelta.Length() / flSpeed;

	// set nextthink to trigger a call to AngularMoveDone when dest is reached
	pev->nextthink = pev->ltime + flTravelTime;
	SetThink(&CBaseToggle::AngularMoveDone);

	// scale the destdelta vector by the time spent traveling to get velocity
	pev->avelocity = vecDestDelta / flTravelTime;
}

void CBaseToggle::AngularMoveDone()
{
	pev->angles = m_vecFinalAngle;
	pev->avelocity = g_vecZero;
	pev->nextthink = -1;
	if (m_pfnCallWhenMoveDone)
		(this->*m_pfnCallWhenMoveDone)();
}

float CBaseToggle::AxisValue(int flags, const Vector& angles)
{
	if (FBitSet(flags, SF_DOOR_ROTATE_Z))
		return angles.z;
	if (FBitSet(flags, SF_DOOR_ROTATE_X))
		return angles.x;

	return angles.y;
}

void CBaseToggle::AxisDir(CBaseEntity* entity)
{
	if (FBitSet(entity->pev->spawnflags, SF_DOOR_ROTATE_Z))
		entity->pev->movedir = Vector(0, 0, 1); // around z-axis
	else if (FBitSet(entity->pev->spawnflags, SF_DOOR_ROTATE_X))
		entity->pev->movedir = Vector(1, 0, 0); // around x-axis
	else
		entity->pev->movedir = Vector(0, 1, 0); // around y-axis
}

float CBaseToggle::AxisDelta(int flags, const Vector& angle1, const Vector& angle2)
{
	if (FBitSet(flags, SF_DOOR_ROTATE_Z))
		return angle1.z - angle2.z;

	if (FBitSet(flags, SF_DOOR_ROTATE_X))
		return angle1.x - angle2.x;

	return angle1.y - angle2.y;
}

/**
 *	@brief returns true if the passed entity is visible to caller, even if not infront ()
 */
bool FEntIsVisible(CBaseEntity* entity, CBaseEntity* target)
{
	Vector vecSpot1 = entity->pev->origin + entity->pev->view_ofs;
	Vector vecSpot2 = target->pev->origin + target->pev->view_ofs;
	TraceResult tr;

	UTIL_TraceLine(vecSpot1, vecSpot2, ignore_monsters, entity->edict(), &tr);

	if (0 != tr.fInOpen && 0 != tr.fInWater)
		return false; // sight line crossed contents

	if (tr.flFraction == 1)
		return true;

	return false;
}
