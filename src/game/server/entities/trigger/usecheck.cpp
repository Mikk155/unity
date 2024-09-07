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

class CTriggerUseCheck : public CBaseDelay
{
	DECLARE_CLASS( CTriggerUseCheck, CBaseDelay );
	DECLARE_DATAMAP();

	public:
		bool KeyValue( KeyValueData* pkvd ) override;
		void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;

		bool SwitchCompare( int iCompare, float value, USE_TYPE useType, int type );

	private:
		bool m_toint = true;
		bool m_hasvalue = false;
		float m_isvalue = 0.0f;
		USE_TYPE m_isuse = USE_UNSET;
		int m_value_comparator;
		int m_usetype_comparator;
};

BEGIN_DATAMAP( CTriggerUseCheck )
DEFINE_FIELD( m_toint, FIELD_FLOAT ),
	DEFINE_FIELD( m_hasvalue, FIELD_BOOLEAN ),
	DEFINE_FIELD( m_isvalue, FIELD_FLOAT ),
	DEFINE_FIELD( m_isuse, FIELD_INTEGER ),
	DEFINE_FIELD( m_value_comparator, FIELD_INTEGER ),
	DEFINE_FIELD( m_usetype_comparator, FIELD_INTEGER ),
END_DATAMAP();

LINK_ENTITY_TO_CLASS( trigger_usecheck, CTriggerUseCheck );

bool CTriggerUseCheck :: KeyValue( KeyValueData* pkvd )
{
	if( FStrEq( pkvd->szKeyName, "is_value" ) )
	{
		m_hasvalue = true;
		m_isvalue = atof( pkvd->szValue );
	}
	else if( FStrEq( pkvd->szKeyName, "is_usetype" ) )
	{
		m_isuse = static_cast<USE_TYPE>( atoi( pkvd->szValue ) );
	}
	else if( FStrEq( pkvd->szKeyName, "value_int" ) )
	{
		m_toint = ( atoi( pkvd->szValue ) != 0 );
	}
	else if( FStrEq( pkvd->szKeyName, "value_comparator" ) )
	{
		m_value_comparator = atoi( pkvd->szValue );
	}
	else if( FStrEq( pkvd->szKeyName, "usetype_comparator" ) )
	{
		m_usetype_comparator = atoi( pkvd->szValue );
	}
	else
	{
		return BaseClass::KeyValue( pkvd );
	}

	return true;
}

bool CTriggerUseCheck :: SwitchCompare( int iCompare, float value, USE_TYPE useType, int type )
{
	if( type == 1 )
		if( m_isuse == USE_UNSET )
			return true;
	else if( !m_hasvalue )
		return true;

	switch( iCompare )
	{
		case 0:
			if( type == 1 ) return ( useType == m_isuse );
			else return ( ( m_toint ? (int)value : value ) == ( m_toint ? (int)m_isvalue : m_isvalue ) );
		break;
		case 1:
			if( type == 1 ) return ( useType != m_isuse );
			else return ( ( m_toint ? (int)value : value ) != ( m_toint ? (int)m_isvalue : m_isvalue ) );
		break;
		case 2:
			if( type == 1 ) return ( useType > m_isuse );
			else return ( ( m_toint ? (int)value : value ) > ( m_toint ? (int)m_isvalue : m_isvalue ) );
		break;
		case 3:
			if( type == 1 ) return ( useType < m_isuse );
			else return ( ( m_toint ? (int)value : value ) < ( m_toint ? (int)m_isvalue : m_isvalue ) );
		break;
		case 4:
			if( type == 1 ) return ( useType >= m_isuse );
			else return ( ( m_toint ? (int)value : value ) >= ( m_toint ? (int)m_isvalue : m_isvalue ) );
		break;
		case 5:
			if( type == 1 ) return ( useType <= m_isuse );
			else return ( ( m_toint ? (int)value : value ) <= ( m_toint ? (int)m_isvalue : m_isvalue ) );
		break;
		case 6:
			return ( type == 0 && FBitSet( int(m_isvalue), (int)value ) );
		break;
		case 7:
			return ( type == 0 && FBitSet( int(value), (int)m_isvalue ) );
		break;
	}
	return false;
}

void CTriggerUseCheck :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
	bool bCompared = SwitchCompare( m_value_comparator, value, useType, 0 );

	if( bCompared )
		bCompared = SwitchCompare( m_usetype_comparator, value, useType, 1 );

	FireTargets( ( bCompared ? STRING( pev->message ) : STRING( pev->netname ) ), pActivator, pCaller, useType, value );

	BaseClass::SUB_UseTargets( pActivator, USE_TOGGLE, 0 );
}
