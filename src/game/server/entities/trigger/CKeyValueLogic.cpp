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

BEGIN_DATAMAP( CKeyValueLogic )
    DEFINE_FIELD( m_sTargetEntity, FIELD_STRING ),
    DEFINE_FIELD( m_sSourceEntity, FIELD_STRING ),
    DEFINE_FIELD( m_sSourceKeyName, FIELD_STRING ),
    DEFINE_FIELD( m_sKeyName, FIELD_STRING ),
    DEFINE_FIELD( m_sValue, FIELD_STRING ),
    DEFINE_FIELD( m_iSetType, FIELD_INTEGER ),
    DEFINE_FIELD( m_iAppendSpaces, FIELD_INTEGER ),
    DEFINE_FIELD( m_SkipVector, FIELD_INTEGER ),
    DEFINE_FIELD( m_iMaxTargets, FIELD_INTEGER ),
    DEFINE_FIELD( m_iCurrentTarget, FIELD_INTEGER ),
    DEFINE_FIELD( m_FloatConversion, FIELD_INTEGER ),
END_DATAMAP();

void CKeyValueLogic :: Spawn()
{
    pev->solid = SOLID_NOT;
}

bool CKeyValueLogic :: KeyValue( KeyValueData* pkvd )
{
    if( FStrEq( pkvd->szKeyName, "m_sTargetEntity" ) )
    {
        m_sTargetEntity = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sSourceEntity" ) )
    {
        m_sSourceEntity = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sKeyName" ) )
    {
        m_sKeyName = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sSourceKeyName" ) )
    {
        m_sSourceKeyName = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_sValue" ) )
    {
        m_sValue = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_iSetType" ) )
    {
        m_iSetType = static_cast<KeyValueMath>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_FloatConversion" ) )
    {
        m_FloatConversion = static_cast<KeyValueFloatConversion>( atoi( pkvd->szValue ) );
    }
    else if( FStrEq( pkvd->szKeyName, "m_iMaxTargets" ) )
    {
        m_iMaxTargets = atoi( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "m_iAppendSpaces" ) )
    {
        m_iAppendSpaces = atoi( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szValue, "m_SkipVector_X" ) )
    {
        if( atoi( pkvd->szValue ) == 1 )
            m_SkipVector |= KeyValueVector::X;
    }
    else if( FStrEq( pkvd->szValue, "m_SkipVector_Y" ) )
    {
        if( atoi( pkvd->szValue ) == 1 )
            m_SkipVector |= KeyValueVector::Y;
    }
    else if( FStrEq( pkvd->szValue, "m_SkipVector_Z" ) )
    {
        if( atoi( pkvd->szValue ) == 1 )
            m_SkipVector |= KeyValueVector::Z;
    }
    else if( FStrEq( pkvd->szValue, "m_SkipVector_A" ) )
    {
        if( atoi( pkvd->szValue ) == 1 )
            m_SkipVector |= KeyValueVector::A;
    }
    else
    {
        return BaseClass::KeyValue( pkvd );
    }
    return true;
}

void CKeyValueLogic :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
    if( !FStringNull( pev->target ) )
        FireTargets( STRING( pev->target ), pActivator, this, USE_TOGGLE, value );
}

std::string CKeyValueLogic :: GetValue( CBaseEntity* pActivator, CBaseEntity* pCaller )
{
    if( !FStringNull( m_sSourceEntity ) )
    {
        if( auto entity = UTIL_FindEntityByTargetname( nullptr, STRING( m_sSourceEntity ), pActivator, pCaller ); entity != nullptr )
        {
            return entity->GetKeyValue( STRING( m_sSourceKeyName ), STRING( m_sValue ) );
        }
    }

    return std::string( STRING( m_sValue ) );
}

CBaseEntity* CKeyValueLogic :: GetTarget( CBaseEntity* pActivator, CBaseEntity* pCaller )
{
    m_iCurrentTarget++;

    if( m_iMaxTargets != -1 && m_iCurrentTarget > m_iMaxTargets )
    {
        pLastFind = nullptr;
        m_iCurrentTarget = 0;
    }
    else
    {
        pLastFind = UTIL_FindEntityByTargetname( pLastFind, STRING( m_sTargetEntity ), pActivator, pCaller );

        if( m_iMaxTargets == -1 && ( !pLastFind || pLastFind == nullptr ) )
            pLastFind = nullptr;
    }

    return pLastFind;
}

std::string CKeyValueLogic :: format( std::string szValue )
{
    auto FloatConversion = []( const std::string& str, KeyValueFloatConversion floatConversion ) -> std::string
    {
        std::ostringstream oss;
        double number = std::stod( str );

        switch( floatConversion )
        {
            case KeyValueFloatConversion::DECIMALS_5:
                oss << std::fixed << std::setprecision(5) << number;
            break;
            case KeyValueFloatConversion::DECIMALS_4:
                oss << std::fixed << std::setprecision(4) << number;
            break;
            case KeyValueFloatConversion::DECIMALS_3:
                oss << std::fixed << std::setprecision(3) << number;
            break;
            case KeyValueFloatConversion::DECIMALS_2:
                oss << std::fixed << std::setprecision(2) << number;
            break;
            case KeyValueFloatConversion::DECIMALS_1:
                oss << std::fixed << std::setprecision(1) << number;
            break;
            case KeyValueFloatConversion::INTEGER:
                oss << static_cast<int>(number);
            break;
            case KeyValueFloatConversion::INTEGER_RUP:
                oss << static_cast<int>( std::ceil(number) );
            break;
            case KeyValueFloatConversion::INTEGER_RDN:
                oss << static_cast<int>( std::floor(number) );
            break;
            case KeyValueFloatConversion::DECIMALS_6:
                oss << std::fixed << std::setprecision(6) << number;
            break;
            default:
                oss << number;
            break;
        }

        return oss.str();
    };

    auto IsStringVector = [&]( const std::string& str ) -> std::vector<std::string>
    {
        std::istringstream stream(str);
        std::string segment;
        std::vector<std::string> numbers;

        while( std::getline( stream, segment, ' ' ) )
        {
            if( !segment.empty() && std::all_of( segment.begin(), segment.end(), [](char c) { return ::isdigit(c) || c == '.' || c == '-'; } ) )
                numbers.push_back(FloatConversion(segment, m_FloatConversion));
            else
                return std::vector<std::string>();
        }

        return numbers; // Vector2D, Vector, RGBA
    };

    auto isFloat = []( const std::string& str ) -> bool
    {
        std::istringstream iss( str );
        float f;
        char c;
        return !( !( iss >> f) || ( iss >> c ) );
    };

    if( auto VecValue = IsStringVector( szValue ); VecValue.size() >= 2 && VecValue.size() <= 4 )
    {
        if( ( m_SkipVector & KeyValueVector::X ) != 0 )
            VecValue[0] = "0";

        if( ( m_SkipVector & KeyValueVector::Y ) != 0 )
            VecValue[1] = "0";

        if( VecValue.size() >= 3 && ( m_SkipVector & KeyValueVector::Z ) != 0 )
            VecValue[2] = "0";

        if( VecValue.size() >= 4 && ( m_SkipVector & KeyValueVector::A ) != 0 )
            VecValue[3] = "0";

        while( VecValue.size() < 4 ) // Fill up with zeros for simply string checking
            VecValue.push_back( "0" );

        std::ostringstream oss;

        for( size_t i = 0; i < VecValue.size(); ++i )
        {
            oss << VecValue[i];

            if( i != VecValue.size() - 1 )
            {
                oss << " ";
            }
        }

        szValue = oss.str();
    }
    else if( isFloat( szValue ) )
    {
        szValue = FloatConversion( szValue, m_FloatConversion );
    }

    return szValue;
}
