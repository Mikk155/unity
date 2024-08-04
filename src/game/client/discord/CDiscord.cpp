/***
 *
 *	Copyright (c) 1999, Valve LLC. All rights reserved.
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

#include "CDiscord.h"

static DiscordRichPresence discordPresence;
extern cl_enginefunc_t gEngfuncs;

// Blank handlers; not required for singleplayer Half-Life
static void HandleDiscordReady(const DiscordUser* connectedUser) {}
static void HandleDiscordDisconnected(int errcode, const char* message) {}
static void HandleDiscordError(int errcode, const char* message) {}
static void HandleDiscordJoin(const char* secret) {}
static void HandleDiscordSpectate(const char* secret) {}
static void HandleDiscordJoinRequest(const DiscordUser* request) {}

void CDiscord :: RPCStartUp()
{
	int64_t startTime = time(0);

	DiscordEventHandlers handlers;
	memset(&handlers, 0, sizeof(handlers));

	handlers.ready = HandleDiscordReady;
	handlers.disconnected = HandleDiscordDisconnected;
	handlers.errored = HandleDiscordError;
	handlers.joinGame = HandleDiscordJoin;
	handlers.spectateGame = HandleDiscordSpectate;
	handlers.joinRequest = HandleDiscordJoinRequest;

	Discord_Initialize("1176277342751031336", &handlers, 1, 0);

	memset(&discordPresence, 0, sizeof(discordPresence));

	discordPresence.startTimestamp = startTime;
	discordPresence.largeImageKey = m_szDefaultLogo;
	Discord_UpdatePresence(&discordPresence);
}

void CDiscord :: RPCStateUpdate()
{
	if( !gEngfuncs.GetEntityByIndex(0) || gEngfuncs.GetEntityByIndex(0) == nullptr )
	{
		g_Discord.m_szHeader = "In main menu";
	}

	discordPresence.state = g_Discord.m_szDescription;
	discordPresence.details = g_Discord.m_szHeader;
	discordPresence.button1_label = g_Discord.button1_label;
	discordPresence.button1_url = g_Discord.button1_url;
	Discord_UpdatePresence(&discordPresence);
}

void CDiscord :: RPCShutDown()
{
	Discord_Shutdown();
}
