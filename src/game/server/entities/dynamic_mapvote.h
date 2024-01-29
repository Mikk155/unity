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

#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "cbase.h"
#include "CBaseEntity.h"
#include "filesystem_utils.h"
#include <iostream>
#include <map>
#include <string>
#include <fstream>
#include <vector>

#pragma once

#define DMV_WORLD_BOUNDS 4096

struct dynamic_mapvotes
{
	// Sprite name to display in the frames
	const char* sprite;
	// Map name
	const char* map;
	// Map name 2, optional for "Skip intro" vote
	const char* map2;
	// Name to display in the HUD
	const char* name;
	// Number of players standing in this slot, This is automaticaly changed by the code.
	int voters = 0;
	// Position of the slot, This is automaticaly changed by the code.
	int pos = 0;
};

class CDynamicMapvote : public CBaseEntity
{
public:
	void Precache() override;
	void Spawn() override;
	void OnCreate() override;
	bool KeyValue(KeyValueData* pkvd) override;
	int ObjectCaps() override { return FCAP_DONT_SAVE; }
	void Think() override;
	// Changed to true when the copypaste is ready
	bool WorldInit = false;
	CBaseEntity* CreateEntity( int x, int y, string_t model );
	void CloseWalls( int x );

	// Maps information
	std::vector<dynamic_mapvotes> g_Maps;

	int voteTime = 30;
	int voteTime2 = voteTime;
	int targetMapIdx;
	bool voting;

private:
	// Model: Floor Default
	string_t mfd;
	// Model: Floor Vote
	string_t mfv;
	// Model: Wall Default
	string_t mwd;
	// Model: Wall Vote
	string_t mwv;
	const char* config_file = "cfg/maps/dynamic_mapvote.txt";
	const char* sound_pass = "buttons/bell1.wav";
	const char* sound_countdown = "buttons/blip1.wav";

	// Size of the prop model brush
	int prop_size = 256;
	int room_long = 4;
};