/***
*
*    Copyright (c) 1996-2001, Valve LLC. All rights reserved.
*
*    This product contains software technology licensed from Id
*    Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc.
*    All Rights Reserved.
*
*   Use, distribution, and modification of this source code and/or resulting
*   object code is restricted to non-commercial enhancements to products from
*   Valve LLC.  All other use, distribution, or modification is prohibited
*   without written permission from Valve LLC.
*
****/

#include "cbase.h"
#include "config/CommandWhitelist.h"

#define SF_GAME_VARIABLE_START_ON ( 1 << 0 )
#define SF_GAME_VARIABLE_STORE ( 1 << 1 )

#define VARIABLE_TYPE_COMMAND 0
#define VARIABLE_TYPE_CVAR 1
#define VARIABLE_TYPE_SKILL 2
#define VARIABLE_TYPE_JSON 3

class CGameVariable : public CBaseEntity
{
    DECLARE_CLASS( CGameVariable, CBaseEntity );
    DECLARE_DATAMAP();

    public:
        void Spawn() override;
        bool KeyValue( KeyValueData* pkvd ) override;
        void Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value ) override;

    private:
        string_t m_sVariable;
        int m_iVariableType = VARIABLE_TYPE_COMMAND;
        string_t m_sValue;

        // Not saved, used to speed up repeated calls and log diagnostics.
        cvar_t* m_CVar{};
};

BEGIN_DATAMAP( CGameVariable )
    DEFINE_FIELD( m_sVariable, FIELD_STRING ),
    DEFINE_FIELD( m_iVariableType, FIELD_INTEGER ),
    DEFINE_FIELD( m_sValue, FIELD_STRING ),
END_DATAMAP();

LINK_ENTITY_TO_CLASS( game_variable, CGameVariable );

bool CGameVariable :: KeyValue( KeyValueData* pkvd )
{
    if( FStrEq( pkvd->szKeyName, "variable" ) )
    {
        m_sVariable = ALLOC_STRING( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "type" ) )
    {
        m_iVariableType = atoi( pkvd->szValue );
    }
    else if( FStrEq( pkvd->szKeyName, "value" ) )
    {
        m_sValue = ALLOC_STRING( pkvd->szValue );
    }
    else
    {
        return BaseClass::KeyValue( pkvd );
    }

    return true;
}

void CGameVariable :: Use( CBaseEntity* pActivator, CBaseEntity* pCaller, USE_TYPE useType, float value )
{
    if( !UTIL_IsMasterTriggered( m_sMaster, pActivator, m_UseLocked ) )
        return;

    // Commands should be evaluated on execution
    // In case we've saved and restored and the whitelist has changed.
    // Or either the cvar sv_commandlist has been updated.
	auto IsCommandAllowed = []( const char* sVariable ) -> bool
	{
        if( (int)CVAR_GET_FLOAT( "sv_commandlist" ) == 1 )
            return !g_CommandWhitelist.contains( sVariable );
        return g_CommandWhitelist.contains( sVariable );
	};

    switch( m_iVariableType )
    {
        case VARIABLE_TYPE_CVAR:
        {
            const auto cvarName = STRING( m_sVariable );
            const auto cvarValue = STRING( useType == USE_OFF ? pev->message : m_sValue );

            if( !IsCommandAllowed( cvarName ) )
            {
                Logger->error("The console variable \"{} {}\" cannot be changed because it is not listed in the command whitelist", cvarName, cvarValue);
                break;
            }

            if (!m_CVar)
            {
                m_CVar = CVAR_GET_POINTER(cvarName);

                if (!m_CVar)
                {
                    Logger->error("The console variable \"{}\" does not exist");
                    break;
                }
            }

            pev->message = ALLOC_STRING( CVAR_GET_STRING( cvarName ) );

            if( FBitSet( pev->spawnflags, SF_GAME_VARIABLE_STORE ) )
                break;

            Logger->info("Changing cvar \"{}\" from \"{}\" to \"{}\"", cvarName, m_CVar->string, cvarValue);
            g_engfuncs.pfnCvar_DirectSet(m_CVar, cvarValue);

            if( FStrEq( cvarName, "skill" ) )
            {
                // Cached variables will be unaffected.
                g_Skill.SetSkillLevel( SkillLevel( atoi( cvarValue ) ) );
            }
            break;
        }
        case VARIABLE_TYPE_SKILL:
        {
            const char* szvar = STRING( m_sVariable );
            pev->message = ALLOC_STRING( std::to_string( g_Skill.GetValue( szvar ) ).c_str() );

            if( FBitSet( pev->spawnflags, SF_GAME_VARIABLE_STORE ) )
                break;

            float flvalue = atof( STRING( useType == USE_OFF ? pev->message : m_sValue ) );
            Logger->info("Changing skill var \"{}\" from \"{}\" to \"{}\"", szvar, g_Skill.GetValue( szvar ), flvalue );
            g_Skill.SetValue( szvar, flvalue );
            break;
        }
        case VARIABLE_TYPE_JSON:
        {
            if( FBitSet( pev->spawnflags, SF_GAME_VARIABLE_STORE ) )
                break;
            // Dummy
            break;
        }
        case VARIABLE_TYPE_COMMAND:
        default:
        {
            if( !IsCommandAllowed( STRING( m_sVariable ) ) )
            {
                Logger->error("The console command \"{} {}\" cannot be sent because it is not listed in the command whitelist", STRING( m_sVariable ) );
                break;
            }

            if( FBitSet( pev->spawnflags, SF_GAME_VARIABLE_STORE ) )
            {
                Logger->error("Can not store-only a type of variable which is \"command\"" );
                break;
            }

            Logger->info("Sending command \"{}\"", STRING( m_sVariable ) );
            SERVER_COMMAND( STRING( m_sVariable ) );
            break;
        }
    }

    SUB_UseTargets(pActivator, USE_TOGGLE, 0);
}

void CGameVariable :: Spawn()
{
    if( FBitSet( pev->spawnflags, SF_GAME_VARIABLE_START_ON ) )
    {
        Use( this, this, USE_TOGGLE, 0 );
    }
}
