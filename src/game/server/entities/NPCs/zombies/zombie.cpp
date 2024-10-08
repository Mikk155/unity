/***
 *
 *	Copyright (c) 1996-2001, Valve LLC. All rights reserved.
 *
 *	This product contains software technology licensed from Id
 *	Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc.
 *	All Rights Reserved.
 *
 *   This source code contains proprietary and confidential information of
 *   Valve LLC and its suppliers.  Access to this code is restricted to
 *   persons who have executed a written SDK license with Valve.  Any access,
 *   use or distribution of this code by or to any unlicensed person is illegal.
 *
 ****/

// UNDONE: Don't flinch every time you get hit

#include "cbase.h"
#include "zombie.h"

BEGIN_DATAMAP(CZombie)
	DEFINE_FIELD(m_iAllowHeadcrab, FIELD_INTEGER),
	DEFINE_FIELD(m_flDamageTaken, FIELD_FLOAT),
END_DATAMAP();

LINK_ENTITY_TO_CLASS(monster_zombie, CZombie);

void CZombie::OnCreate()
{
	BaseClass::OnCreate();

	pev->health = GetSkillFloat("zombie_health"sv);
	pev->model = MAKE_STRING("models/zombie.mdl");

	SetClassification("alien_monster");
}

void CZombie::SetYawSpeed()
{
	int ys;

	ys = 120;

#if 0
	switch (m_Activity)
	{
	}
#endif

	pev->yaw_speed = ys;
}

bool CZombie::TakeDamage(CBaseEntity* inflictor, CBaseEntity* attacker, float flDamage, int bitsDamageType)
{
	if (bitsDamageType == DMG_BULLET)
	{
		Vector vecDir = pev->origin - (inflictor->pev->absmin + inflictor->pev->absmax) * 0.5;
		vecDir = vecDir.Normalize();
		float flForce = DamageForce(flDamage);
		pev->velocity = pev->velocity + vecDir * flForce;
		flDamage *= GetBulletDamageFraction();
	}

	// HACK HACK -- until we fix this.
	if (IsAlive())
		PainSound();
	return BaseClass::TakeDamage(inflictor, attacker, flDamage, bitsDamageType);
}

void CZombie::PainSound()
{
	int pitch = 95 + RANDOM_LONG(0, 9);

	if (RANDOM_LONG(0, 5) < 2)
		EmitSoundDyn(CHAN_VOICE, RANDOM_SOUND_ARRAY(pPainSounds), 1.0, ATTN_NORM, 0, pitch);
}

void CZombie::AlertSound()
{
	int pitch = 95 + RANDOM_LONG(0, 9);

	EmitSoundDyn(CHAN_VOICE, RANDOM_SOUND_ARRAY(pAlertSounds), 1.0, ATTN_NORM, 0, pitch);
}

void CZombie::IdleSound()
{
	int pitch = 100 + RANDOM_LONG(-5, 5);

	// Play a random idle sound
	EmitSoundDyn(CHAN_VOICE, RANDOM_SOUND_ARRAY(pIdleSounds), 1.0, ATTN_NORM, 0, pitch);
}

void CZombie::AttackSound()
{
	int pitch = 100 + RANDOM_LONG(-5, 5);

	// Play a random attack sound
	EmitSoundDyn(CHAN_VOICE, RANDOM_SOUND_ARRAY(pAttackSounds), 1.0, ATTN_NORM, 0, pitch);
}

float CZombie::GetOneSlashDamage()
{
	return GetSkillFloat("zombie_dmg_one_slash"sv);
}

float CZombie::GetBothSlashDamage()
{
	return GetSkillFloat("zombie_dmg_both_slash"sv);
}

void CZombie::ZombieSlashAttack(float damage, const Vector& punchAngle, const Vector& velocity, bool playAttackSound)
{
	// do stuff for this event.
	// AILogger->debug("Slash!");
	CBaseEntity* pHurt = CheckTraceHullAttack(70, damage, DMG_SLASH);
	if (pHurt)
	{
		if ((pHurt->pev->flags & (FL_MONSTER | FL_CLIENT)) != 0)
		{
			pHurt->pev->punchangle = punchAngle;
			pHurt->pev->velocity = pHurt->pev->velocity + velocity;
		}
		// Play a random attack hit sound
		EmitSoundDyn(CHAN_WEAPON, RANDOM_SOUND_ARRAY(pAttackHitSounds), 1.0, ATTN_NORM, 0, 100 + RANDOM_LONG(-5, 5));
	}
	else // Play a random attack miss sound
		EmitSoundDyn(CHAN_WEAPON, RANDOM_SOUND_ARRAY(pAttackMissSounds), 1.0, ATTN_NORM, 0, 100 + RANDOM_LONG(-5, 5));

	if (playAttackSound && RANDOM_LONG(0, 1))
		AttackSound();
}

void CZombie::HandleAnimEvent(MonsterEvent_t* pEvent)
{
	switch (pEvent->event)
	{
	case ZOMBIE_AE_ATTACK_RIGHT:
		ZombieSlashAttack(GetOneSlashDamage(), {5, 0, -18}, -(gpGlobals->v_right * 100));
		break;

	case ZOMBIE_AE_ATTACK_LEFT:
		ZombieSlashAttack(GetOneSlashDamage(), {5, 0, 18}, gpGlobals->v_right * 100);
		break;

	case ZOMBIE_AE_ATTACK_BOTH:
		ZombieSlashAttack(GetBothSlashDamage(), {5, 0, 0}, gpGlobals->v_forward * -100);
		break;

	default:
		BaseClass::HandleAnimEvent(pEvent);
		break;
	}
}

void CZombie::Spawn()
{
	Precache();

	SetModel(STRING(pev->model));
	SetSize(VEC_HUMAN_HULL_MIN, VEC_HUMAN_HULL_MAX);

	pev->solid = SOLID_SLIDEBOX;
	pev->movetype = MOVETYPE_STEP;
	pev->view_ofs = VEC_VIEW; // position of the eyes relative to monster's origin.
	m_flFieldOfView = 0.5;	  // indicates the width of this monster's forward view cone ( as a dotproduct result )
	m_MonsterState = MONSTERSTATE_NONE;
	m_afCapability = bits_CAP_DOORS_GROUP;

	MonsterInit();
}

void CZombie::Precache()
{
	UTIL_PrecacheOther( "monster_headcrab" );

	PrecacheModel(STRING(pev->model));

	PRECACHE_SOUND_ARRAY(pAttackHitSounds);
	PRECACHE_SOUND_ARRAY(pAttackMissSounds);
	PRECACHE_SOUND_ARRAY(pAttackSounds);
	PRECACHE_SOUND_ARRAY(pIdleSounds);
	PRECACHE_SOUND_ARRAY(pAlertSounds);
	PRECACHE_SOUND_ARRAY(pPainSounds);
}

int CZombie::IgnoreConditions()
{
	int iIgnore = BaseClass::IgnoreConditions();

	if (m_Activity == ACT_MELEE_ATTACK1)
	{
#if 0
		if (pev->health < 20)
			iIgnore |= (bits_COND_LIGHT_DAMAGE | bits_COND_HEAVY_DAMAGE);
		else
#endif
		if (m_flNextFlinch >= gpGlobals->time)
			iIgnore |= (bits_COND_LIGHT_DAMAGE | bits_COND_HEAVY_DAMAGE);
	}

	if ((m_Activity == ACT_SMALL_FLINCH) || (m_Activity == ACT_BIG_FLINCH))
	{
		if (m_flNextFlinch < gpGlobals->time)
			m_flNextFlinch = gpGlobals->time + ZOMBIE_FLINCH_DELAY;
	}

	return iIgnore;
}

void CZombie::TraceAttack(CBaseEntity* pAttacker, float flDamage, Vector vecDir, TraceResult* ptr, int bitsDamageType)
{
	if( m_iAllowHeadcrab == 1 && ptr->iHitgroup == 1 ) // check for headcrab shot
	{
		m_flDamageTaken += flDamage; // Store received damage
	}

	m_bloodColor = ( ptr->iHitgroup == 1 ? BLOOD_COLOR_GREEN : BLOOD_COLOR_RED ); // If headshot drop green blood

	BaseClass::TraceAttack(pAttacker, flDamage, vecDir, ptr, bitsDamageType);
}

void CZombie::Killed(CBaseEntity* pAttacker, int iGib)
{
	// Check if the stored received damage is less than a headcrab's HP
	if( m_iAllowHeadcrab == 1 && m_flDamageTaken < GetSkillFloat("headcrab_health"sv) )
	{
		SetBodygroup( 1, 1 );

		CBaseEntity* pEntity = Create( "monster_headcrab", pev->origin + Vector( 0,0,72 ), pev->angles, this );

		pEntity->pev->health = GetSkillFloat("headcrab_health"sv) - m_flDamageTaken;
	}
	BaseClass::Killed(pAttacker, iGib);
}

bool CZombie::KeyValue(KeyValueData* pkvd)
{
	if( FStrEq( pkvd->szKeyName, "allow_headcrab" ) )
	{
		m_iAllowHeadcrab = atoi( pkvd->szValue );
	}
	else
	{
		return BaseClass::KeyValue(pkvd);
	}
	return true;
}
