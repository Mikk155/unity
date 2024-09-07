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

class CTriggerCondition : public CKeyValueLogic
{
	DECLARE_CLASS( CTriggerCondition, CKeyValueLogic );

	public:
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;
};

LINK_ENTITY_TO_CLASS( trigger_condition, CTriggerCondition );

void CTriggerCondition :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	std::string szKeyValue = format( GetValue( pActivator, pCaller ) );

	for( auto entity = GetTarget( pActivator, pCaller ); entity != nullptr; entity = GetTarget( pActivator, pCaller ) )
	{
		std::string szEntKeyValue = format( entity->GetKeyValue( STRING( m_sKeyName ) ) );

		bool bCondition = false;

		switch( m_iSetType )
		{
			case EQUAL:
				bCondition = ( szKeyValue == szEntKeyValue );
			break;
			case NOT_EQUAL:
				bCondition = ( szKeyValue != szEntKeyValue );
			break;
			case LESS:
				bCondition = ( atoi( szKeyValue.c_str() ) < atoi( szEntKeyValue.c_str() ) );
			break;
			case GREATER:
				bCondition = ( atoi( szKeyValue.c_str() ) > atoi( szEntKeyValue.c_str() ) );
			break;
			case LESS_OR_EQUAL:
				bCondition = ( atoi( szKeyValue.c_str() ) <= atoi( szEntKeyValue.c_str() ) );
			break;
			case GREATER_OR_EQUAL:
				bCondition = ( atoi( szKeyValue.c_str() ) >= atoi( szEntKeyValue.c_str() ) );
			break;
			case LOGICAL_AND:
				bCondition = ( ( atoi( szKeyValue.c_str() ) & atoi( szEntKeyValue.c_str() ) ) != 0 );
			break;
			default:
				bCondition = ( szKeyValue == szEntKeyValue );
			break;
		}

		FireTargets( STRING( ( bCondition ? pev->netname : pev->message ) ), entity, this, USE_TOGGLE, 0 );
	}

	BaseClass::Use( pActivator, pCaller, useType, value );
}
