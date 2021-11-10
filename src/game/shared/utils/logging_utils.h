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

#pragma once

#include <string_view>

#include <spdlog/common.h>

#include "ILogSystem.h"

constexpr std::string_view ToStringView(spdlog::string_view_t view)
{
	return {view.data(), view.size()};
}

extern ILogSystem* const g_Logging;
