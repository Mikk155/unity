/***
*
*	Copyright (c) 1996-2001, Valve LLC. All rights reserved.
*
*	This product contains software technology licensed from Id
*	Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc.
*	All Rights Reserved.
*
*	Use, distribution, and modification of this source code and/or resulting
*	object code is restricted to non-commercial enhancements to products from
*	Valve LLC.  All other use, distribution, or modification is prohibited
*	without written permission from Valve LLC.
*
****/

#include "dynamic_mapvote.h"

LINK_ENTITY_TO_CLASS( dynamic_mapvote, CDynamicMapvote );

bool CDynamicMapvote :: KeyValue( KeyValueData* pkvd )
{
	if( FStrEq( pkvd->szKeyName, "sound_pass" ) )
	{
		sound_pass = pkvd->szValue;
	}
	else if( FStrEq( pkvd->szKeyName, "sound_countdown" ) )
	{
		sound_countdown = pkvd->szValue;
	}
	else if( FStrEq( pkvd->szKeyName, "room_long" ) )
	{
		room_long = atoi( pkvd->szValue );
	}
	else
	{
		return false;
	}
	return true;
}

void CDynamicMapvote :: OnCreate()
{
	dynamic_mapvotes map;
	map.sprite = "sprites/dynamic_mapvote/halflife.spr";
	map.map = "c0a0";
	map.map2 = "c1a0e";
	map.name = "Half-Life";

	// Chequear IS_MAP_VALID map, map2 antes de guardar.
	// Chequear que exista el sprite y avisar que falta -Mikk
	g_Maps.push_back( map );

	dynamic_mapvotes map2;
	map2.sprite = "sprites/dynamic_mapvote/uplink.spr";
	map2.map = "uplink";
	map2.name = "Half-Life Uplink";
	g_Maps.push_back( map2 );

	dynamic_mapvotes map3;
	map3.sprite = "sprites/dynamic_mapvote/blue-shift.spr";
	map3.map = "ba_tram1";
	map3.name = "Half-Life Blue Shift";
	g_Maps.push_back( map3 );

	// Leer del json aqui, quitar lo de arriba es testing
	// Leer "cfg/maps/" + gpGlobals->mapname + ".json" -Mikk
}

void CDynamicMapvote :: Spawn()
{
	Precache();

	pev->nextthink = gpGlobals->time = 0.1;
}

void CDynamicMapvote :: Precache()
{
	PrecacheSound( sound_countdown );
	PrecacheSound( sound_pass );

	for( unsigned int i = 0; i < g_Maps.size(); i++ )
	{
		if( g_Maps[i].sprite )
			PrecacheModel( g_Maps[i].sprite );
	}
}

void CDynamicMapvote :: Think()
{
	if( FStringNull( mfd ) || FStringNull( mfd ) || FStringNull( mwv ) || FStringNull( mwd ) )
	{
		CBaseEntity* pEnt = NULL;

		while( ( pEnt = UTIL_FindEntityByClassname( pEnt, "func_wall" ) ) )
		{
			if( FStringNull( pEnt->pev->model ) )
				continue;

			if( FStrEq( STRING( pEnt->pev->targetname ), "wall_vote" ) )
			{
				mwv = pEnt->pev->model;
			}
			else if( FStrEq( STRING( pEnt->pev->targetname ), "wall_default" ) )
			{
				mwd = pEnt->pev->model;
			}
			else if( FStrEq( STRING( pEnt->pev->targetname ), "floor_vote" ) )
			{
				mfv = pEnt->pev->model;
			}
			else if( FStrEq( STRING( pEnt->pev->targetname ), "floor_default" ) )
			{
				mfd = pEnt->pev->model;
			}
			else
			{
				continue;
			}
			UTIL_Remove( pEnt );
		}
	}
	else if( !WorldInit )
	{
		int x_current = -DMV_WORLD_BOUNDS;

		// Create the first (left) walls
		CloseWalls( x_current );

		x_current += prop_size;

		for( unsigned int i = 0; i < g_Maps.size(); i++ )
		{
			if( g_Maps[i].sprite )
			{
				// Expose position as a keyvalue -Mikk
				CBaseEntity* pSprite = Create( "env_sprite", Vector( x_current, 1151, 104 ), Vector( 0, 90, 0 ), nullptr, false );

				if( pSprite )
				{
					pSprite->pev->model = MAKE_STRING( g_Maps[i].sprite );
					pSprite->pev->scale = 0.5;
					pSprite->pev->framerate = 10;
					pSprite->pev->rendercolor = Vector( 255, 255, 255 );
					pSprite->pev->rendermode = kRenderTransTexture;
					pSprite->pev->renderamt = 255;
				};
				// -TODO we'll need vp_type parallel as SC has -Mikk
			}

			// Create floors
			for( int i = prop_size; i < ( prop_size * room_long ); i += prop_size )
				CreateEntity( x_current, i, mfd );

			// Create floor for vote
			CreateEntity( x_current, ( prop_size * room_long ), mfv );

			// Create wall for vote
			CreateEntity( x_current, ( prop_size * ( room_long + 1 ) ), mwv );

			// Create back wall
			CreateEntity( x_current, 0, mwd );

			g_Maps[i].pos = x_current;

			Create( "info_player_deathmatch", Vector( x_current, prop_size, 32 ), Vector( 0, 90, 0 ) );

			x_current += prop_size;
		}

		// Create the last (right) walls
		CloseWalls( x_current );

		WorldInit = true;
	}
	else
	{
		int MostVoted1 = 0;
		int MostVoted1_index = -1;
		int MostVoted2 = 0;
		int MostVoted2_index = -1;

		for( unsigned int i = 0; i < g_Maps.size(); i++ )
		{
			// Restore count
			g_Maps[i].voters = 0;

			for( int i = 1; i <= gpGlobals->maxClients; i++ )
			{
				CBasePlayer* pPlayer = UTIL_PlayerByIndex( i );

				// player's position is around this slot's x position
				if( pPlayer && pPlayer->IsConnected()
				&&  pPlayer->pev->origin.x < g_Maps[i].pos + ( prop_size / 2 )
				&&  pPlayer->pev->origin.x > g_Maps[i].pos - ( prop_size / 2 )
				&&  pPlayer->pev->origin.y > prop_size * room_long - ( prop_size / 2 ) )
				{
					// g_Maps[i].voters++;
					g_Maps[i].voters = g_Maps[i].voters + 1;
				}
			}

			if( g_Maps[i].voters > MostVoted1 )
			{
				MostVoted1_index = i;
				MostVoted1 = g_Maps[i].voters;
			}
			else if( g_Maps[i].voters > MostVoted2 )
			{
				MostVoted2_index = i;
				MostVoted2 = g_Maps[i].voters;
			}
		}

		if( MostVoted1_index > -1 )
		{
			Logger->warn( "Hay voto?" );
			// Sort
			int i = ( MostVoted1_index == MostVoted2_index && RANDOM_LONG( 0, 1 ) == 0 ? MostVoted2_index : MostVoted1_index );

			if( !g_Maps[i].name )
				g_Maps[i].name = "???";

			voteTime2--;

			std::string m_szMessage = "Voting for: " + std::string( g_Maps[i].name ) + "\n" + "Remaining time: " + std::to_string( voteTime2 );

			hudtextparms_t hudParams;
			hudParams.x = -1.0f;
			hudParams.y = 0.7;
			hudParams.r1 = 255;
			hudParams.g1 = 255;
			hudParams.b1 = 255;
			hudParams.r2 = 255;
			hudParams.g2 = 255;
			hudParams.b2 = 255;
			hudParams.effect = 0;
			hudParams.fadeinTime = 0.0f;
			hudParams.fadeoutTime = 0.45f;
			hudParams.holdTime = 1.05f;
			hudParams.channel = 1;
			UTIL_HudMessageAll( hudParams, m_szMessage.c_str() );

			if( voteTime2 < 0 )
			{
				EMIT_SOUND_DYN2( edict(), CHAN_STATIC, sound_pass, 1.0f, ATTN_NONE, 0, 100 );

				if( g_Maps[i].map2 )
				{
					// Iniciar una votacion para skipear intro -Mikk
					return;
				}
				else
				{
					CHANGE_LEVEL( g_Maps[i].map, nullptr );
					return;
				}
			}
			else if( voteTime2 <= 10 )
			{
				EMIT_SOUND_DYN2( edict(), CHAN_STATIC, sound_countdown, 1.0f, ATTN_NONE, 0, 100 );
			}
		}
		else
		{
			voteTime2 = voteTime;
		}
	}
	pev->nextthink = gpGlobals->time = 1.0; // Each second
}

void CDynamicMapvote :: CloseWalls( int x )
{
	for( int i = prop_size; i < ( prop_size * ( room_long + 1 ) ); i += prop_size )
	{
		CBaseEntity* pEntity = CBaseEntity::Create( "func_wall", Vector( x, i, 0 ), g_vecZero, nullptr, false );

		pEntity->pev->model = mwd;

		//SetBits( pEntity->pev->effects, EF_NODECALS );

		DispatchSpawn( pEntity->edict() );
	}
}

CBaseEntity* CDynamicMapvote :: CreateEntity( int x, int y, string_t model )
{
    CBaseEntity* pEntity = CBaseEntity::Create( "func_wall", Vector( x, y, 0 ), g_vecZero, nullptr, false );

	if( pEntity )
	{
		pEntity->pev->model = model;

		//SetBits( pEntity->pev->effects, EF_NODECALS );

		pEntity->Spawn();
		return pEntity;
	}
	return nullptr;
}