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
	std::string szSetValue = GetValue( pActivator, pCaller );

	for( auto entity = GetTarget( pActivator, pCaller ); entity != nullptr; entity = GetTarget( pActivator, pCaller ) )
	{
		auto edict = entity->edict();

		const char* classname = entity->GetClassname();

		KeyValueData kvd{.szClassName = classname};

		kvd.szKeyName = STRING( m_sKeyName );

		if( m_iSetType == KeyValueMath::ADD )
		{
			szSetValue = std::stof( szSetValue ) + std::stof( entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) ) );
		}
		else if( m_iSetType == KeyValueMath::MULTIPLY )
		{
			szSetValue = std::stof( szSetValue ) * std::stof( entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) ) );
		}
		else if( m_iSetType == KeyValueMath::SUBSTRACT )
		{
			szSetValue = std::stof( szSetValue ) - std::stof( entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) ) );
		}
		else if( m_iSetType == KeyValueMath::DIVIDE )
		{
			szSetValue = std::stof( szSetValue ) / std::stof( entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) ) );
		}
		else if( m_iSetType == KeyValueMath::AND )
		{
			int bit = std::stoi( szSetValue );
			bit &= std::stoi( entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) ) );
			szSetValue = std::to_string( bit );
		}
		else if( m_iSetType == KeyValueMath::OR )
		{
			int bit = std::stoi( szSetValue );
			bit |= std::stoi( entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) ) );
			szSetValue = std::to_string( bit );
		}
		else if( m_iSetType == KeyValueMath::DIRECTION_TO_ANGLES )
		{
		}
		else if( m_iSetType == KeyValueMath::ANGLES_TO_DIRECTION )
		{
		}
		else if( m_iSetType == KeyValueMath::APPEND_STRING )
		{
			std::string spaces = "";
			for( int i = 0; i < m_iAppendSpaces; i++ )
				spaces += " ";
			szSetValue += spaces + entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) );
		}

		kvd.szValue = format( szSetValue ).c_str();
		kvd.fHandled = 0;

		// Skip the classname the same way the engine does.
		if(FStrEq(kvd.szValue, classname))
			continue;

		DispatchKeyValue( edict, &kvd );

		CBaseEntity::Logger->debug( "Changed keyvalue {} {} of entity {}", STRING( m_sKeyName ), szSetValue, STRING( entity->pev->targetname ) );
	
		if( !FStringNull( pev->message ) )
			FireTargets( STRING( pev->message ), entity, this, USE_TOGGLE, 0 );
	}

	BaseClass::Use( pActivator, pCaller, useType, value );
}
