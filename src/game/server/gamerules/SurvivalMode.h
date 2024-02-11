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

/*
Copy in titles.txt:

SurvivalStartDelay
{
Survival mode will start in %s seconds.
}
SurvivalStarted
{
Survival mode started, No more re-spawning allowed.
}
SurvivalDisabled
{
Survival mode disabled, re-spawning allowed
}
*/

#pragma once

#include "cbase.h"

class SurvivalMode final
{
public:
	void Think();
    bool IsActive();
    int StartDelay();
    int m_LastActive;

private:
    float m_flNextThink;
};

inline SurvivalMode g_SurvivalMode;
