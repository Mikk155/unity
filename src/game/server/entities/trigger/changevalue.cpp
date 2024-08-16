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

class CTriggerChangeValue : public CKeyValueLogic
{
	DECLARE_CLASS( CTriggerChangeValue, CKeyValueLogic );

	public:
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
};

LINK_ENTITY_TO_CLASS( trigger_changevalue, CTriggerChangeValue );

void CTriggerChangeValue :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	string_t szSetValue = GetValue( pActivator, pCaller );

	for( auto entity = GetTarget( pActivator, pCaller ); entity != nullptr; entity = GetTarget( pActivator, pCaller ) )
	{
		auto edict = entity->edict();

		const char* classname = entity->GetClassname();

		KeyValueData kvd{.szClassName = classname};

		kvd.szKeyName = STRING( m_sKeyName );
		kvd.szValue = STRING( szSetValue );
		kvd.fHandled = 0;

		// Skip the classname the same way the engine does.
		if(FStrEq(kvd.szValue, classname))
			continue;

		DispatchKeyValue( edict, &kvd );

		CBaseEntity::Logger->debug( "Changed keyvalue {} {} of entity {}", STRING( m_sKeyName ), STRING( szSetValue ), STRING( entity->pev->targetname ) );
	
		if( !FStringNull( pev->message ) )
			FireTargets( STRING( pev->message ), entity, this, USE_TOGGLE, 0 );
	}

	BaseClass::Use( pActivator, pCaller, useType, value );
}
