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

#include <unordered_map>

#include "cbase.h"
#include "ServerLibrary.h"
#include "pm_shared.h"
#include "world.h"
#include "sound/ServerSoundSystem.h"
#include "utils/ReplacementMaps.h"

static void SetObjectCollisionBox(entvars_t* pev);

int DispatchSpawn(edict_t* pent)
{
	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pent);

	if (pEntity && pEntity->CheckAppearanceFlags() )
	{
		// Initialize these or entities who don't link to the world won't have anything in here
		pEntity->pev->absmin = pEntity->pev->origin - Vector(1, 1, 1);
		pEntity->pev->absmax = pEntity->pev->origin + Vector(1, 1, 1);

		pEntity->Spawn();

		// Try to get the pointer again, in case the spawn function deleted the entity.
		// UNDONE: Spawn() should really return a code to ask that the entity be deleted, but
		// that would touch too much code for me to do that right now.
		pEntity = (CBaseEntity*)GET_PRIVATE(pent);

		if (pEntity)
		{
			if (g_pGameRules && !g_pGameRules->IsAllowedToSpawn(pEntity))
				return -1; // return that this entity should be deleted
			if ((pEntity->pev->flags & FL_KILLME) != 0)
				return -1;
		}


		// Handle global stuff here
		if (pEntity && !FStringNull(pEntity->pev->globalname))
		{
			const globalentity_t* pGlobal = gGlobalState.EntityFromTable(pEntity->pev->globalname);
			if (pGlobal)
			{
				// Already dead? delete
				if (pGlobal->state == GLOBAL_DEAD)
					return -1;
				else if (!FStrEq(STRING(gpGlobals->mapname), pGlobal->levelName))
					pEntity->MakeDormant(); // Hasn't been moved to this level yet, wait but stay alive
											// In this level & not dead, continue on as normal
			}
			else
			{
				// Spawned entities default to 'On'
				gGlobalState.EntityAdd(pEntity->pev->globalname, gpGlobals->mapname, GLOBAL_ON);
				// CBaseEntity::Logger->trace("Added global entity {} ({})", STRING(pEntity->pev->classname), STRING(pEntity->pev->globalname));
			}
		}
	}

	return 0;
}

void EntvarsKeyvalue(entvars_t* pev, KeyValueData* pkvd)
{
	for (const auto& member : entvars_t::GetLocalDataMap()->Members)
	{
		auto field = std::get_if<DataFieldDescription>(&member);

		if (field && !stricmp(field->fieldName, pkvd->szKeyName))
		{
			switch (field->fieldType)
			{
			case FIELD_MODELNAME:
			case FIELD_SOUNDNAME:
			case FIELD_STRING:
				(*(string_t*)((char*)pev + field->fieldOffset)) = ALLOC_STRING(pkvd->szValue);
				break;

			case FIELD_TIME:
			case FIELD_FLOAT:
				(*(float*)((char*)pev + field->fieldOffset)) = atof(pkvd->szValue);
				break;

			case FIELD_INTEGER:
				(*(int*)((char*)pev + field->fieldOffset)) = atoi(pkvd->szValue);
				break;

			case FIELD_POSITION_VECTOR:
			case FIELD_VECTOR:
				UTIL_StringToVector(*((Vector*)((char*)pev + field->fieldOffset)), pkvd->szValue);
				break;

			default:
			case FIELD_CLASSPTR:
			case FIELD_EDICT:
				CBaseEntity::Logger->error("Bad field in entity!!");
				break;
			}
			pkvd->fHandled = 1;
			return;
		}
	}
}

void DispatchKeyValue(edict_t* pentKeyvalue, KeyValueData* pkvd)
{
	if (!pkvd || !pentKeyvalue)
		return;

	if (g_Server.CheckForNewMapStart(false))
	{
		// HACK: If we get here that means we're loading a new map and we're setting worldspawn's classname.
		// We've wiped out com_token by calling SERVER_EXECUTE() which stores the classname so we need to reset it.
		pkvd->szValue = "worldspawn";
	}

	// Don't allow classname changes once the classname has been set.
	if (!FStringNull(pentKeyvalue->v.classname) && FStrEq(pkvd->szKeyName, "classname"))
	{
		CBaseEntity::Logger->debug("{}: Duplicate classname \"{}\" ignored",
			STRING(pentKeyvalue->v.classname), pkvd->szValue);
		return;
	}

	EntvarsKeyvalue(&pentKeyvalue->v, pkvd);

	// If the key was an entity variable, or there's no class set yet, don't look for the object, it may
	// not exist yet.
	if (0 != pkvd->fHandled || pkvd->szClassName == nullptr)
		return;

	// Get the actualy entity object
	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pentKeyvalue);

	if (!pEntity)
		return;

	pkvd->fHandled = static_cast<int32>(pEntity->RequiredKeyValue(pkvd));

	if (pkvd->fHandled != 0)
	{
		return;
	}

	pkvd->fHandled = static_cast<int32>(pEntity->KeyValue(pkvd));
}

void DispatchTouch(edict_t* pentTouched, edict_t* pentOther)
{
	if (gTouchDisabled)
		return;

	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pentTouched);
	CBaseEntity* pOther = (CBaseEntity*)GET_PRIVATE(pentOther);

	if( pEntity && pOther && ( (pEntity->pev->flags | pOther->pev->flags) & FL_KILLME) == 0 && !FBitSet( pEntity->m_UseLocked, USE_VALUE_TOUCH ) )
		pEntity->Touch(pOther);
}

void DispatchUse(edict_t* pentUsed, edict_t* pentOther)
{
	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pentUsed);
	CBaseEntity* pOther = (CBaseEntity*)GET_PRIVATE(pentOther);

	if (pEntity && (pEntity->pev->flags & FL_KILLME) == 0 && !FBitSet( pEntity->m_UseLocked, USE_VALUE_USE ) )
		pEntity->Use(pOther, pOther, USE_TOGGLE, 0);
}

void DispatchThink(edict_t* pent)
{
	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pent);
	if( pEntity && !FBitSet( pEntity->m_UseLocked, USE_VALUE_THINK ) )
	{
		if (FBitSet(pEntity->pev->flags, FL_DORMANT))
			CBaseEntity::Logger->error("Dormant entity {} is thinking!!", STRING(pEntity->pev->classname));

		pEntity->Think();
	}
}

void DispatchBlocked(edict_t* pentBlocked, edict_t* pentOther)
{
	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pentBlocked);
	CBaseEntity* pOther = (CBaseEntity*)GET_PRIVATE(pentOther);

	if (pEntity)
		pEntity->Blocked(pOther);
}

void DispatchSave(edict_t* pent, SAVERESTOREDATA* pSaveData)
{
	gpGlobals->time = pSaveData->time;

	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pent);

	if (pEntity && CSaveRestoreBuffer::IsValidSaveRestoreData(pSaveData))
	{
		ENTITYTABLE* pTable = &pSaveData->pTable[pSaveData->currentIndex];

		if (pTable->pent != pent)
			CBaseEntity::Logger->error("ENTITY TABLE OR INDEX IS WRONG!!!!");

		if ((pEntity->ObjectCaps() & FCAP_DONT_SAVE) != 0)
			return;

		// These don't use ltime & nextthink as times really, but we'll fudge around it.
		if (pEntity->pev->movetype == MOVETYPE_PUSH)
		{
			float delta = pEntity->pev->nextthink - pEntity->pev->ltime;
			pEntity->pev->ltime = gpGlobals->time;
			pEntity->pev->nextthink = pEntity->pev->ltime + delta;
		}

		pTable->location = pSaveData->size;			 // Remember entity position for file I/O
		pTable->classname = pEntity->pev->classname; // Remember entity class for respawn

		CSave saveHelper(*pSaveData);
		pEntity->Save(saveHelper);

		pTable->size = pSaveData->size - pTable->location; // Size of entity block is data size written to block
	}
}

void OnFreeEntPrivateData(edict_t* pEdict)
{
	if (pEdict && pEdict->pvPrivateData)
	{
		auto entity = reinterpret_cast<CBaseEntity*>(pEdict->pvPrivateData);

		g_EntityDictionary->Destroy(entity);

		// Zero this out so the engine doesn't try to free it again.
		pEdict->pvPrivateData = nullptr;
	}
}

/**
 *	@brief Find the matching global entity.
 *	Spit out an error if the designer made entities of different classes with the same global name
 */
CBaseEntity* FindGlobalEntity(string_t classname, string_t globalname)
{
	auto pReturn = UTIL_FindEntityByString(nullptr, "globalname", STRING(globalname));

	if (pReturn)
	{
		if (!pReturn->ClassnameIs(STRING(classname)))
		{
			CBaseEntity::Logger->debug("Global entity found {}, wrong class {}", STRING(globalname), STRING(pReturn->pev->classname));
			pReturn = nullptr;
		}
	}

	return pReturn;
}

int DispatchRestore(edict_t* pent, SAVERESTOREDATA* pSaveData, int globalEntity)
{
	gpGlobals->time = pSaveData->time;

	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pent);

	if (pEntity && CSaveRestoreBuffer::IsValidSaveRestoreData(pSaveData))
	{
		entvars_t tmpVars;
		Vector oldOffset;

		CRestore restoreHelper(*pSaveData);
		if (0 != globalEntity)
		{
			CRestore tmpRestore(*pSaveData);
			tmpRestore.PrecacheMode(false);
			tmpRestore.ReadFields(&tmpVars, *entvars_t::GetLocalDataMap(), *entvars_t::GetLocalDataMap());

			// HACKHACK - reset the save pointers, we're going to restore for real this time
			pSaveData->size = pSaveData->pTable[pSaveData->currentIndex].location;
			pSaveData->pCurrentData = pSaveData->pBaseData + pSaveData->size;
			// -------------------


			const globalentity_t* pGlobal = gGlobalState.EntityFromTable(tmpVars.globalname);

			// Don't overlay any instance of the global that isn't the latest
			// pSaveData->szCurrentMapName is the level this entity is coming from
			// pGlobla->levelName is the last level the global entity was active in.
			// If they aren't the same, then this global update is out of date.
			if (!FStrEq(pSaveData->szCurrentMapName, pGlobal->levelName))
				return 0;

			// Compute the new global offset
			oldOffset = pSaveData->vecLandmarkOffset;
			CBaseEntity* pNewEntity = FindGlobalEntity(tmpVars.classname, tmpVars.globalname);
			if (pNewEntity)
			{
				// CBaseEntity::Logger->debug("Overlay {} with {}", STRING(pNewEntity->pev->classname), STRING(tmpVars.classname));
				//  Tell the restore code we're overlaying a global entity from another level
				restoreHelper.SetGlobalMode(true); // Don't overwrite global fields
				pSaveData->vecLandmarkOffset = (pSaveData->vecLandmarkOffset - pNewEntity->pev->mins) + tmpVars.mins;
				pEntity = pNewEntity; // we're going to restore this data OVER the old entity
				pent = pEntity->edict();
				// Update the global table to say that the global definition of this entity should come from this level
				gGlobalState.EntityUpdate(pEntity->pev->globalname, gpGlobals->mapname);
			}
			else
			{
				// This entity will be freed automatically by the engine.  If we don't do a restore on a matching entity (below)
				// or call EntityUpdate() to move it to this level, we haven't changed global state at all.
				return 0;
			}
		}

		pEntity->Restore(restoreHelper);
		pEntity->PostRestore();

		if ((pEntity->ObjectCaps() & FCAP_MUST_SPAWN) != 0)
		{
			pEntity->Spawn();
		}
		else
		{
			pEntity->Precache();
		}

		// Again, could be deleted, get the pointer again.
		pEntity = (CBaseEntity*)GET_PRIVATE(pent);

#if 0
		if (pEntity && pEntity->pev->globalname && globalEntity)
		{
			CBaseEntity::Logger->debug("Global {} is {}", STRING(pEntity->pev->globalname), STRING(pEntity->pev->model));
		}
#endif

		// Is this an overriding global entity (coming over the transition), or one restoring in a level
		if (0 != globalEntity)
		{
			// CBaseEntity::Logger->debug("After: {} {}", pEntity->pev->origin, STRING(pEntity->pev->model));
			pSaveData->vecLandmarkOffset = oldOffset;
			if (pEntity)
			{
				pEntity->SetOrigin(pEntity->pev->origin);
				pEntity->OverrideReset();
			}
		}
		else if (pEntity && !FStringNull(pEntity->pev->globalname))
		{
			const globalentity_t* pGlobal = gGlobalState.EntityFromTable(pEntity->pev->globalname);
			if (pGlobal)
			{
				// Already dead? delete
				if (pGlobal->state == GLOBAL_DEAD)
					return -1;
				else if (!FStrEq(STRING(gpGlobals->mapname), pGlobal->levelName))
				{
					pEntity->MakeDormant(); // Hasn't been moved to this level yet, wait but stay alive
				}
				// In this level & not dead, continue on as normal
			}
			else
			{
				CBaseEntity::Logger->error("Global Entity {} ({}) not in table!!!\n",
					STRING(pEntity->pev->globalname), STRING(pEntity->pev->classname));
				// Spawned entities default to 'On'
				gGlobalState.EntityAdd(pEntity->pev->globalname, gpGlobals->mapname, GLOBAL_ON);
			}
		}
	}
	return 0;
}

void DispatchObjectCollsionBox(edict_t* pent)
{
	CBaseEntity* pEntity = (CBaseEntity*)GET_PRIVATE(pent);
	if (pEntity)
	{
		pEntity->SetObjectCollisionBox();
	}
	else
		SetObjectCollisionBox(&pent->v);
}

// The engine uses the old type description data, so we need to translate it to the game's version.
static FIELDTYPE RemapEngineFieldType(ENGINEFIELDTYPE fieldType)
{
	// The engine only uses these data types.
	// Some custom engine may use others, but those engines are not supported.
	switch (fieldType)
	{
	case ENGINEFIELDTYPE::FIELD_FLOAT: return FIELD_FLOAT;
	case ENGINEFIELDTYPE::FIELD_STRING: return FIELD_STRING;
	case ENGINEFIELDTYPE::FIELD_EDICT: return FIELD_EDICT;
	case ENGINEFIELDTYPE::FIELD_VECTOR: return FIELD_VECTOR;
	case ENGINEFIELDTYPE::FIELD_INTEGER: return FIELD_INTEGER;
	case ENGINEFIELDTYPE::FIELD_CHARACTER: return FIELD_CHARACTER;
	case ENGINEFIELDTYPE::FIELD_TIME: return FIELD_TIME;

	default: return FIELD_TYPECOUNT;
	}
}

static const IDataFieldSerializer* RemapEngineFieldTypeToSerializer(ENGINEFIELDTYPE fieldType)
{
	// The engine only uses these data types.
	// Some custom engine may use others, but those engines are not supported.
	switch (fieldType)
	{
	case ENGINEFIELDTYPE::FIELD_FLOAT: return &FieldTypeToSerializerMapper<FIELD_FLOAT>::Serializer;
	case ENGINEFIELDTYPE::FIELD_STRING: return &FieldTypeToSerializerMapper<FIELD_STRING>::Serializer;
	case ENGINEFIELDTYPE::FIELD_EDICT: return &FieldTypeToSerializerMapper<FIELD_EDICT>::Serializer;
	case ENGINEFIELDTYPE::FIELD_VECTOR: return &FieldTypeToSerializerMapper<FIELD_VECTOR>::Serializer;
	case ENGINEFIELDTYPE::FIELD_INTEGER: return &FieldTypeToSerializerMapper<FIELD_INTEGER>::Serializer;
	case ENGINEFIELDTYPE::FIELD_CHARACTER: return &FieldTypeToSerializerMapper<FIELD_CHARACTER>::Serializer;
	case ENGINEFIELDTYPE::FIELD_TIME: return &FieldTypeToSerializerMapper<FIELD_TIME>::Serializer;

	default: return nullptr;
	}
}

struct EngineDataMap
{
	std::unique_ptr<const DataMember[]> TypeDescriptions;
	DataMap Map;
};

std::unordered_map<const TYPEDESCRIPTION*, std::unique_ptr<const EngineDataMap>> g_EngineTypeDescriptionsToGame;

static const DataMap* GetOrCreateDataMap(const char* className, const TYPEDESCRIPTION* fields, int fieldCount)
{
	auto it = g_EngineTypeDescriptionsToGame.find(fields);

	if (it == g_EngineTypeDescriptionsToGame.end())
	{
		auto typeDescriptions = std::make_unique<DataMember[]>(fieldCount);

		for (int i = 0; i < fieldCount; ++i)
		{
			const auto& src = fields[i];

			DataFieldDescription dest{
				.fieldType = RemapEngineFieldType(src.fieldType),
				.Serializer = RemapEngineFieldTypeToSerializer(src.fieldType),
				.fieldName = src.fieldName,
				.fieldOffset = src.fieldOffset,
				.fieldSize = src.fieldSize,
				.flags = src.flags};

			typeDescriptions[i] = dest;
		}

		auto engineDataMap = std::make_unique<EngineDataMap>();

		engineDataMap->Map.ClassName = className;
		engineDataMap->Map.Members = {typeDescriptions.get(), static_cast<std::size_t>(fieldCount)};
		engineDataMap->TypeDescriptions = std::move(typeDescriptions);

		it = g_EngineTypeDescriptionsToGame.emplace(fields, std::move(engineDataMap)).first;
	}

	return &it->second->Map;
}

void SaveWriteFields(SAVERESTOREDATA* pSaveData, const char* pname, void* pBaseData, TYPEDESCRIPTION* pFields, int fieldCount)
{
	if (!CSaveRestoreBuffer::IsValidSaveRestoreData(pSaveData))
	{
		return;
	}

	auto dataMap = GetOrCreateDataMap(pname, pFields, fieldCount);

	CSave saveHelper(*pSaveData);
	saveHelper.WriteFields(pBaseData, *dataMap, *dataMap);
}

void SaveReadFields(SAVERESTOREDATA* pSaveData, const char* pname, void* pBaseData, TYPEDESCRIPTION* pFields, int fieldCount)
{
	if (!CSaveRestoreBuffer::IsValidSaveRestoreData(pSaveData))
	{
		return;
	}

	// Will happen here if we're loading a saved game
	// ETABLE is the first chunk of data read after the engine has set up some global variables that we need
	if (0 == strcmp(pname, "ETABLE"))
	{
		g_Server.CheckForNewMapStart(true);
	}

	// Always check if the player is stuck when loading a save game.
	g_CheckForPlayerStuck = true;

	auto dataMap = GetOrCreateDataMap(pname, pFields, fieldCount);

	CRestore restoreHelper(*pSaveData);
	restoreHelper.ReadFields(pBaseData, *dataMap, *dataMap);
}

static void CheckForBackwardsBounds(CBaseEntity* entity)
{
	if (UTIL_FixBoundsVectors(entity->m_CustomHullMin, entity->m_CustomHullMax))
	{
		// Can't log the targetname because it may not have been set yet.
		CBaseEntity::Logger->warn("Backwards mins/maxs fixed in custom hull (entity index {})", entity->entindex());
	}
}

static void LoadReplacementMap(const ReplacementMap*& destination, string_t fileName, const ReplacementMapOptions& options)
{
	const char* fileNameString = STRING(fileName);

	if (FStrEq(fileNameString, ""))
	{
		return;
	}

	auto result = g_ReplacementMaps.Load(fileNameString, options);

	// Only overwrite destination if we successfully loaded something.
	if (result)
	{
		destination = result;
	}
}

static void LoadFileNameReplacementMap(const ReplacementMap*& destination, string_t fileName)
{
	return LoadReplacementMap(destination, fileName, {.CaseSensitive = false, .LoadFromAllPaths = true});
}

static void LoadSentenceReplacementMap(const ReplacementMap*& destination, string_t fileName)
{
	return LoadReplacementMap(destination, fileName, {.CaseSensitive = true, .LoadFromAllPaths = true});
}

bool CBaseEntity::RequiredKeyValue(KeyValueData* pkvd)
{
	keyvalues[ pkvd->szKeyName ] = std::string( pkvd->szValue );

	// Replacement maps can be changed at runtime using trigger_changekeyvalue.
	// Note that this may cause host_error or sys_error if files aren't precached.
	if (FStrEq(pkvd->szKeyName, "modellist"))
	{
		m_ModelReplacementFileName = ALLOC_STRING(pkvd->szValue);
		LoadFileNameReplacementMap(m_ModelReplacement, m_ModelReplacementFileName);
	}
	else if (FStrEq(pkvd->szKeyName, "soundlist"))
	{
		m_SoundReplacementFileName = ALLOC_STRING(pkvd->szValue);
		LoadFileNameReplacementMap(m_SoundReplacement, m_SoundReplacementFileName);
	}
	else if (FStrEq(pkvd->szKeyName, "sentencelist"))
	{
		m_SentenceReplacementFileName = ALLOC_STRING(pkvd->szValue);
		LoadSentenceReplacementMap(m_SentenceReplacement, m_SentenceReplacementFileName);
	}
	// Note: while this code does fix backwards bounds here it will not apply to partial hulls mixing with hard-coded ones.
	else if (FStrEq(pkvd->szKeyName, "minhullsize"))
	{
		UTIL_StringToVector(m_CustomHullMin, pkvd->szValue);
		m_HasCustomHullMin = true;

		if (m_HasCustomHullMax)
		{
			CheckForBackwardsBounds(this);
		}

		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "maxhullsize"))
	{
		UTIL_StringToVector(m_CustomHullMax, pkvd->szValue);
		m_HasCustomHullMax = true;

		if (m_HasCustomHullMin)
		{
			CheckForBackwardsBounds(this);
		}

		return true;
	}
	else if (FStrEq(pkvd->szKeyName, "originhullsize"))
	{
		m_HasZeroOrigin = ( atoi( pkvd->szValue ) == 1 );
		return true;
	}
	else if( FStrEq( pkvd->szKeyName, "m_UseType" ) && atoi( pkvd->szValue ) > USE_UNSET && atoi( pkvd->szValue ) < USE_UNKNOWN )
	{
		m_UseType = static_cast<USE_TYPE>( atoi( pkvd->szValue ) );
		return true;
	}
	else if( FStrEq( pkvd->szKeyName, "m_UseValue" ) )
	{
		m_UseValue = atof( pkvd->szValue );
		return true;
	}
	else if( std::string_view( pkvd->szKeyName ).find( "appearflag_" ) == 0 )
	{
		if( atoi( pkvd->szValue ) != 0 )
		{
			int iBits = 0;

			if( FStrEq( pkvd->szKeyName, "appearflag_singleplayer" ) )      iBits = appearflags::GM_SINGLEPLAYER;
			else if( FStrEq( pkvd->szKeyName, "appearflag_multiplayer" ) )  iBits = appearflags::GM_MULTIPLAYER;
			else if( FStrEq( pkvd->szKeyName, "appearflag_cooperative" ) )  iBits = appearflags::GM_COOPERATIVE;
			else if( FStrEq( pkvd->szKeyName, "appearflag_skilleasy" ) )    iBits = appearflags::SKILL_EASY;
			else if( FStrEq( pkvd->szKeyName, "appearflag_skillmedium" ) )  iBits = appearflags::SKILL_MEDIUM;
			else if( FStrEq( pkvd->szKeyName, "appearflag_skillhard" ) )    iBits = appearflags::SKILL_HARD;
			else if( FStrEq( pkvd->szKeyName, "appearflag_deathmatch" ) )   iBits = appearflags::GM_DEATHMATCH;
			else if( FStrEq( pkvd->szKeyName, "appearflag_cft" ) )          iBits = appearflags::GM_CAPTURETHEFLAG;
			else if( FStrEq( pkvd->szKeyName, "appearflag_teamplay" ) )     iBits = appearflags::GM_TEAMPLAY;
			else if( FStrEq( pkvd->szKeyName, "appearflag_dedicated" ) )    iBits = appearflags::SV_DEDICATED;

			if( iBits != 0 )
			{
				if( atoi( pkvd->szValue ) == (int)appearflags::NOT_IN )
					SetBits( m_appearflag_notin, iBits );
				else if( atoi( pkvd->szValue ) == (int)appearflags::ONLY_IN )
					SetBits( m_appearflag_onlyin, iBits );
				return true;
			}
		}
	}
	else if( FStrEq( pkvd->szKeyName, "m_Activator" ) )
	{
		m_sNewActivator = ALLOC_STRING( pkvd->szValue );
		return true;
	}
	else if( std::string_view( pkvd->szKeyName ).find( "m_iPlayerSelector" ) == 0 )
	{
		if( atoi( pkvd->szValue ) > 0 )
			SetBits( m_iPlayerSelector, atoi( pkvd->szValue ) );
		return true;
	}
	else if( FStrEq( pkvd->szKeyName, "m_uselos" ) )
	{
		m_uselos = atoi( pkvd->szValue );
		return true;
	}

	return false;
}

void CBaseEntity::SetOrigin(const Vector& origin)
{
	g_engfuncs.pfnSetOrigin(edict(), origin);
}

void CBaseEntity::LoadReplacementFiles()
{
	LoadFileNameReplacementMap(m_ModelReplacement, m_ModelReplacementFileName);
	LoadFileNameReplacementMap(m_SoundReplacement, m_SoundReplacementFileName);
	LoadSentenceReplacementMap(m_SentenceReplacement, m_SentenceReplacementFileName);
}

int CBaseEntity::PrecacheModel(const char* s)
{
	if (m_ModelReplacement)
	{
		s = m_ModelReplacement->Lookup(s);
	}

	return UTIL_PrecacheModel(s);
}

void CBaseEntity::SetModel(const char* s)
{
	if (m_ModelReplacement)
	{
		s = m_ModelReplacement->Lookup(s);
	}

	s = UTIL_CheckForGlobalModelReplacement(s);

	g_engfuncs.pfnSetModel(edict(), s);

	if (m_HasCustomHullMin || m_HasCustomHullMax)
	{
		if( m_HasZeroOrigin ) // Set g_vecZero to mark as absolute size in the world
			SetOrigin( g_vecZero );

		SetSize(pev->mins, pev->maxs);
	}
}

int CBaseEntity::PrecacheSound(const char* s)
{
	if (s[0] == '*')
	{
		++s;
	}

	if (m_SoundReplacement)
	{
		s = m_SoundReplacement->Lookup(s);
	}

	return UTIL_PrecacheSound(s);
}

void CBaseEntity::SetSize(const Vector& min, const Vector& max)
{
	g_engfuncs.pfnSetSize(edict(), m_HasCustomHullMin ? m_CustomHullMin : min, m_HasCustomHullMax ? m_CustomHullMax : max);
}

bool CBaseEntity::GiveHealth(float flHealth, int bitsDamageType)
{
	if (0 == pev->takedamage)
		return false;

	// heal
	if (pev->health >= pev->max_health)
		return false;

	pev->health += flHealth;

	if (pev->health > pev->max_health)
		pev->health = pev->max_health;

	return true;
}

bool CBaseEntity::TakeDamage(CBaseEntity* inflictor, CBaseEntity* attacker, float flDamage, int bitsDamageType)
{
	Vector vecTemp;

	if (0 == pev->takedamage)
		return false;

	// UNDONE: some entity types may be immune or resistant to some bitsDamageType

	// if Attacker == Inflictor, the attack was a melee or other instant-hit attack.
	// (that is, no actual entity projectile was involved in the attack so use the shooter's origin).
	if (attacker == inflictor)
	{
		vecTemp = inflictor->pev->origin - (VecBModelOrigin(this));
	}
	else
	// an actual missile was involved.
	{
		vecTemp = inflictor->pev->origin - (VecBModelOrigin(this));
	}

	// this global is still used for glass and other non-monster killables, along with decals.
	g_vecAttackDir = vecTemp.Normalize();

	// save damage based on the target's armor level

	// figure momentum add (don't let hurt brushes or other triggers move player)
	if ((!FNullEnt(inflictor)) && (pev->movetype == MOVETYPE_WALK || pev->movetype == MOVETYPE_STEP) && (attacker->pev->solid != SOLID_TRIGGER))
	{
		Vector vecDir = pev->origin - (inflictor->pev->absmin + inflictor->pev->absmax) * 0.5;
		vecDir = vecDir.Normalize();

		float flForce = flDamage * ((32 * 32 * 72.0) / (pev->size.x * pev->size.y * pev->size.z)) * 5;

		if (flForce > 1000.0)
			flForce = 1000.0;
		pev->velocity = pev->velocity + vecDir * flForce;
	}

	// do the damage
	pev->health -= flDamage;
	if (pev->health <= 0)
	{
		Killed(attacker, GIB_NORMAL);
		return false;
	}

	return true;
}

void CBaseEntity::Killed(CBaseEntity* attacker, int iGib)
{
	pev->takedamage = DAMAGE_NO;
	pev->deadflag = DEAD_DEAD;
	UTIL_Remove(this);
}

CBaseEntity* CBaseEntity::GetNextTarget()
{
	if (FStringNull(pev->target))
		return nullptr;
	return UTIL_FindEntityByTargetname(nullptr, STRING(pev->target));
}

// Initialize absmin & absmax to the appropriate box
void SetObjectCollisionBox(entvars_t* pev)
{
	if ((pev->solid == SOLID_BSP) && pev->angles != g_vecZero)
	{ // expand for rotation
		float max, v;
		int i;

		max = 0;
		for (i = 0; i < 3; i++)
		{
			v = fabs(pev->mins[i]);
			if (v > max)
				max = v;
			v = fabs(pev->maxs[i]);
			if (v > max)
				max = v;
		}
		for (i = 0; i < 3; i++)
		{
			pev->absmin[i] = pev->origin[i] - max;
			pev->absmax[i] = pev->origin[i] + max;
		}
	}
	else
	{
		pev->absmin = pev->origin + pev->mins;
		pev->absmax = pev->origin + pev->maxs;
	}

	pev->absmin.x -= 1;
	pev->absmin.y -= 1;
	pev->absmin.z -= 1;
	pev->absmax.x += 1;
	pev->absmax.y += 1;
	pev->absmax.z += 1;
}

void CBaseEntity::SetObjectCollisionBox()
{
	::SetObjectCollisionBox(pev);
}

bool CBaseEntity::Intersects(CBaseEntity* pOther)
{
	if (pOther->pev->absmin.x > pev->absmax.x ||
		pOther->pev->absmin.y > pev->absmax.y ||
		pOther->pev->absmin.z > pev->absmax.z ||
		pOther->pev->absmax.x < pev->absmin.x ||
		pOther->pev->absmax.y < pev->absmin.y ||
		pOther->pev->absmax.z < pev->absmin.z)
		return false;
	return true;
}

void CBaseEntity::MakeDormant()
{
	SetBits(pev->flags, FL_DORMANT);

	// Don't touch
	pev->solid = SOLID_NOT;
	// Don't move
	pev->movetype = MOVETYPE_NONE;
	// Don't draw
	SetBits(pev->effects, EF_NODRAW);
	// Don't think
	pev->nextthink = 0;
	// Relink
	SetOrigin(pev->origin);
}

bool CBaseEntity::IsDormant()
{
	return FBitSet(pev->flags, FL_DORMANT);
}

bool CBaseEntity::IsLockedByMaster()
{
	return !FStringNull(m_sMaster) && !UTIL_IsMasterTriggered(m_sMaster, m_hActivator, m_UseLocked);
}

bool CBaseEntity::IsInWorld()
{
	// position
	if (pev->origin.x >= WORLD_BOUNDS_LIMIT)
		return false;
	if (pev->origin.y >= WORLD_BOUNDS_LIMIT)
		return false;
	if (pev->origin.z >= WORLD_BOUNDS_LIMIT)
		return false;
	if (pev->origin.x <= -WORLD_BOUNDS_LIMIT)
		return false;
	if (pev->origin.y <= -WORLD_BOUNDS_LIMIT)
		return false;
	if (pev->origin.z <= -WORLD_BOUNDS_LIMIT)
		return false;
	// speed
	if (pev->velocity.x >= 2000)
		return false;
	if (pev->velocity.y >= 2000)
		return false;
	if (pev->velocity.z >= 2000)
		return false;
	if (pev->velocity.x <= -2000)
		return false;
	if (pev->velocity.y <= -2000)
		return false;
	if (pev->velocity.z <= -2000)
		return false;

	return true;
}

bool CBaseEntity::ShouldToggle(USE_TYPE useType, bool currentState)
{
	if (useType != USE_TOGGLE && useType != USE_SET)
	{
		if ((currentState && useType == USE_ON) || (!currentState && useType == USE_OFF))
			return false;
	}
	return true;
}

int CBaseEntity::DamageDecal(int bitsDamageType)
{
	if (pev->rendermode == kRenderTransAlpha)
		return -1;

	if (pev->rendermode != kRenderNormal)
		return DECAL_BPROOF1;

	return DECAL_GUNSHOT1 + RANDOM_LONG(0, 4);
}

CBaseEntity* CBaseEntity::Create(const char* szName, const Vector& vecOrigin, const Vector& vecAngles, CBaseEntity* owner, bool callSpawn)
{
	auto entity = g_EntityDictionary->Create(szName);

	if (FNullEnt(entity))
	{
		CBaseEntity::Logger->debug("NULL Ent in Create!");
		return nullptr;
	}
	entity->SetOwner(owner);
	entity->pev->origin = vecOrigin;
	entity->pev->angles = vecAngles;

	if (callSpawn)
	{
		DispatchSpawn(entity->edict());
	}

	return entity;
}

void CBaseEntity::EmitSound(int channel, const char* sample, float volume, float attenuation)
{
	sound::g_ServerSound.EmitSound(this, channel, sample, volume, attenuation, 0, PITCH_NORM);
}

void CBaseEntity::EmitSoundDyn(int channel, const char* sample, float volume, float attenuation, int flags, int pitch)
{
	sound::g_ServerSound.EmitSound(this, channel, sample, volume, attenuation, flags, pitch);
}

void CBaseEntity::EmitAmbientSound(const Vector& vecOrigin, const char* samp, float vol, float attenuation, int fFlags, int pitch)
{
	sound::g_ServerSound.EmitAmbientSound(this, vecOrigin, samp, vol, attenuation, fFlags, pitch);
}

void CBaseEntity::StopSound(int channel, const char* sample)
{
	sound::g_ServerSound.EmitSound(this, channel, sample, 0, 0, SND_STOP, PITCH_NORM);
}

bool CBaseEntity :: CheckAppearanceFlags()
{
	if( m_appearflag_notin != (int)appearflags::DEFAULT )
	{
		if(( ( m_appearflag_notin & appearflags::GM_SINGLEPLAYER )   != 0 &&    !g_pGameRules->IsMultiplayer() )
		|| ( ( m_appearflag_notin & appearflags::GM_MULTIPLAYER )    != 0 &&     g_pGameRules->IsMultiplayer() )
		|| ( ( m_appearflag_notin & appearflags::GM_COOPERATIVE )    != 0 &&     g_pGameRules->IsCoOp() )
		|| ( ( m_appearflag_notin & appearflags::SKILL_EASY )        != 0 &&     g_Skill.GetSkillLevel() == SkillLevel::Easy )
		|| ( ( m_appearflag_notin & appearflags::SKILL_MEDIUM )      != 0 &&     g_Skill.GetSkillLevel() == SkillLevel::Medium )
		|| ( ( m_appearflag_notin & appearflags::SKILL_HARD )        != 0 &&     g_Skill.GetSkillLevel() == SkillLevel::Hard )
		|| ( ( m_appearflag_notin & appearflags::GM_TEAMPLAY )       != 0 &&    !g_pGameRules->IsTeamplay() )
		|| ( ( m_appearflag_notin & appearflags::GM_DEATHMATCH )     != 0 &&    !g_pGameRules->IsDeathmatch() )
		|| ( ( m_appearflag_notin & appearflags::GM_CAPTURETHEFLAG ) != 0 &&    !g_pGameRules->IsCTF() )
		|| ( ( m_appearflag_notin & appearflags::SV_DEDICATED )      != 0 &&    !IS_DEDICATED_SERVER() )
		){ return false; }
	}

	if( m_appearflag_onlyin != (int)appearflags::DEFAULT )
	{
		if(( ( m_appearflag_onlyin & appearflags::GM_SINGLEPLAYER )  != 0 &&     g_pGameRules->IsMultiplayer() )
		|| ( ( m_appearflag_onlyin & appearflags::GM_MULTIPLAYER )   != 0 &&    !g_pGameRules->IsMultiplayer() )
		|| ( ( m_appearflag_onlyin & appearflags::GM_COOPERATIVE )   != 0 &&    !g_pGameRules->IsCoOp() )
		|| ( ( m_appearflag_onlyin & appearflags::SKILL_EASY )       != 0 &&     g_Skill.GetSkillLevel() != SkillLevel::Easy )
		|| ( ( m_appearflag_onlyin & appearflags::SKILL_MEDIUM )     != 0 &&     g_Skill.GetSkillLevel() != SkillLevel::Medium )
		|| ( ( m_appearflag_onlyin & appearflags::SKILL_HARD )       != 0 &&     g_Skill.GetSkillLevel() != SkillLevel::Hard )
		|| ( ( m_appearflag_onlyin & appearflags::GM_TEAMPLAY )      != 0 &&     g_pGameRules->IsTeamplay() )
		|| ( ( m_appearflag_onlyin & appearflags::GM_DEATHMATCH )    != 0 &&     g_pGameRules->IsDeathmatch() )
		|| ( ( m_appearflag_onlyin & appearflags::GM_CAPTURETHEFLAG )!= 0 &&     g_pGameRules->IsCTF() )
		|| ( ( m_appearflag_onlyin & appearflags::SV_DEDICATED )     != 0 &&     IS_DEDICATED_SERVER() )
		){ return false; }
	}
	return true;
}

CBaseEntity* CBaseEntity :: AllocNewActivator( CBaseEntity* pActivator, CBaseEntity* pCaller, string_t szNewTarget )
{
	if( !FStringNull( szNewTarget ) )
	{
		if( FStrEq( STRING( szNewTarget ), "!activator" ) )
		{
			return pActivator;
		}
		else if( FStrEq( STRING( szNewTarget ), "!caller" ) )
		{
			return pCaller;
		}
		else if( FStrEq( STRING( szNewTarget ), "!this" ) )
		{
			return this;
		}
		else if( FStrEq( STRING( szNewTarget ), "!player" ) )
		{
			return static_cast<CBaseEntity*>( UTIL_FindNearestPlayer( pev->origin ) );
		}
		else
		{
			return UTIL_FindEntityByTargetname( nullptr, STRING( szNewTarget ) );
		}
	}

	return pActivator;
}

bool CBaseEntity :: IsPlayerSelector( CBasePlayer* pPlayer, CBaseEntity* pActivator )
{
	if( m_iPlayerSelector == PlayerSelector::None )
		return true;

	if( FBitSet( m_iPlayerSelector, PlayerSelector::NonActivator ) && pPlayer != pActivator )
		return true;

	if( FBitSet( m_iPlayerSelector, PlayerSelector::Activator ) && pPlayer == pActivator )
		return true;

	if( FBitSet( m_iPlayerSelector, PlayerSelector::Alive ) && pPlayer->IsAlive() )
		return true;

	if( FBitSet( m_iPlayerSelector, PlayerSelector::Dead ) && !pPlayer->IsAlive() )
		return true;

	return false;
}

std::string CBaseEntity :: GetKeyValue( const char* sKey, const char* DefaultValue )
{
    static const std::unordered_map< std::string, std::function< std::string( const entvars_t* ) > > entvars_map =
	{
        { "classname", [](const entvars_t* pev) { return STRING( pev->classname ); } },
        { "globalname", [](const entvars_t* pev) { return STRING( pev->globalname ); } },
        { "origin", [](const entvars_t* pev) { return pev->origin.ToString(); } },
        { "oldorigin", [](const entvars_t* pev) { return pev->oldorigin.ToString(); } },
        { "velocity", [](const entvars_t* pev) { return pev->velocity.ToString(); } },
        { "basevelocity", [](const entvars_t* pev) { return pev->basevelocity.ToString(); } },
        { "clbasevelocity", [](const entvars_t* pev) { return pev->clbasevelocity.ToString(); } },
        { "movedir", [](const entvars_t* pev) { return pev->movedir.ToString(); } },
        { "angles", [](const entvars_t* pev) { return pev->angles.ToString(); } },
        { "avelocity", [](const entvars_t* pev) { return pev->avelocity.ToString(); } },
        { "punchangle", [](const entvars_t* pev) { return pev->punchangle.ToString(); } },
        { "v_angle", [](const entvars_t* pev) { return pev->v_angle.ToString(); } },
        { "endpos", [](const entvars_t* pev) { return pev->endpos.ToString(); } },
        { "startpos", [](const entvars_t* pev) { return pev->startpos.ToString(); } },
        { "impacttime", [](const entvars_t* pev) { return std::to_string( pev->impacttime ); } },
        { "starttime", [](const entvars_t* pev) { return std::to_string( pev->starttime ); } },
        { "fixangle", [](const entvars_t* pev) { return std::to_string( pev->fixangle ); } },
        { "idealpitch", [](const entvars_t* pev) { return std::to_string( pev->idealpitch ); } },
        { "pitch_speed", [](const entvars_t* pev) { return std::to_string( pev->pitch_speed ); } },
        { "ideal_yaw", [](const entvars_t* pev) { return std::to_string( pev->ideal_yaw ); } },
        { "yaw_speed", [](const entvars_t* pev) { return std::to_string( pev->yaw_speed ); } },
        { "modelindex", [](const entvars_t* pev) { return std::to_string( pev->modelindex ); } },
        { "model", [](const entvars_t* pev) { return STRING( pev->model ); } },
        { "viewmodel", [](const entvars_t* pev) { return STRING( pev->viewmodel ); } },
        { "weaponmodel", [](const entvars_t* pev) { return STRING( pev->weaponmodel ); } },
        { "absmin", [](const entvars_t* pev) { return pev->absmin.ToString(); } },
        { "absmax", [](const entvars_t* pev) { return pev->absmax.ToString(); } },
        { "mins", [](const entvars_t* pev) { return pev->mins.ToString(); } },
        { "maxs", [](const entvars_t* pev) { return pev->maxs.ToString(); } },
        { "size", [](const entvars_t* pev) { return pev->size.ToString(); } },
        { "ltime", [](const entvars_t* pev) { return std::to_string( pev->ltime ); } },
        { "nextthink", [](const entvars_t* pev) { return std::to_string( pev->nextthink ); } },
        { "movetype", [](const entvars_t* pev) { return std::to_string( pev->movetype ); } },
        { "solid", [](const entvars_t* pev) { return std::to_string( pev->solid ); } },
        { "skin", [](const entvars_t* pev) { return std::to_string( pev->skin ); } },
        { "body", [](const entvars_t* pev) { return std::to_string( pev->body ); } },
        { "effects", [](const entvars_t* pev) { return std::to_string( pev->effects ); } },
        { "gravity", [](const entvars_t* pev) { return std::to_string( pev->gravity ); } },
        { "friction", [](const entvars_t* pev) { return std::to_string( pev->friction ); } },
        { "light_level", [](const entvars_t* pev) { return std::to_string( pev->light_level ); } },
        { "sequence", [](const entvars_t* pev) { return std::to_string( pev->sequence ); } },
        { "gaitsequence", [](const entvars_t* pev) { return std::to_string( pev->gaitsequence ); } },
        { "frame", [](const entvars_t* pev) { return std::to_string( pev->frame ); } },
        { "animtime", [](const entvars_t* pev) { return std::to_string( pev->animtime ); } },
        { "framerate", [](const entvars_t* pev) { return std::to_string( pev->framerate ); } },
//        { "controller", [](const entvars_t* pev) { return std::to_string( pev->controller ); } },
//        { "blending", [](const entvars_t* pev) { return std::to_string( pev->blending ); } },
        { "scale", [](const entvars_t* pev) { return std::to_string( pev->scale ); } },
        { "rendermode", [](const entvars_t* pev) { return std::to_string( pev->rendermode ); } },
        { "renderamt", [](const entvars_t* pev) { return std::to_string( pev->renderamt ); } },
        { "rendercolor", [](const entvars_t* pev) { return pev->rendercolor.ToString(); } },
        { "renderfx", [](const entvars_t* pev) { return std::to_string( pev->renderfx ); } },
        { "health", [](const entvars_t* pev) { return std::to_string( pev->health ); } },
        { "frags", [](const entvars_t* pev) { return std::to_string( pev->frags ); } },
        { "weapons", [](const entvars_t* pev) { return std::to_string( pev->weapons ); } },
        { "takedamage", [](const entvars_t* pev) { return std::to_string( pev->takedamage ); } },
        { "deadflag", [](const entvars_t* pev) { return std::to_string( pev->deadflag ); } },
        { "view_ofs", [](const entvars_t* pev) { return pev->view_ofs.ToString(); } },
        { "button", [](const entvars_t* pev) { return std::to_string( pev->button ); } },
        { "impulse", [](const entvars_t* pev) { return std::to_string( pev->impulse ); } },
//        { "chain", [](const entvars_t* pev) { return std::to_string( pev->chain ); } },
//        { "dmg_inflictor", [](const entvars_t* pev) { return std::to_string( pev->dmg_inflictor ); } },
//        { "enemy", [](const entvars_t* pev) { return std::to_string( pev->enemy ); } },
//        { "aiment", [](const entvars_t* pev) { return std::to_string( pev->aiment ); } },
//        { "owner", [](const entvars_t* pev) { return std::to_string( pev->owner ); } },
//        { "groundentity", [](const entvars_t* pev) { return std::to_string( pev->groundentity ); } },
        { "spawnflags", [](const entvars_t* pev) { return std::to_string( pev->spawnflags ); } },
        { "flags", [](const entvars_t* pev) { return std::to_string( pev->flags ); } },
        { "colormap", [](const entvars_t* pev) { return std::to_string( pev->colormap ); } },
        { "team", [](const entvars_t* pev) { return STRING( pev->team ); } },
        { "max_health", [](const entvars_t* pev) { return std::to_string( pev->max_health ); } },
        { "teleport_time", [](const entvars_t* pev) { return std::to_string( pev->teleport_time ); } },
        { "armortype", [](const entvars_t* pev) { return std::to_string( pev->armortype ); } },
        { "armorvalue", [](const entvars_t* pev) { return std::to_string( pev->armorvalue ); } },
        { "waterlevel", [](const entvars_t* pev) { return std::to_string( (int)pev->waterlevel ); } },
        { "watertype", [](const entvars_t* pev) { return std::to_string( pev->watertype ); } },
        { "target", [](const entvars_t* pev) { return STRING( pev->target ); } },
        { "targetname", [](const entvars_t* pev) { return STRING( pev->targetname ); } },
        { "netname", [](const entvars_t* pev) { return STRING( pev->netname ); } },
        { "message", [](const entvars_t* pev) { return STRING( pev->message ); } },
        { "dmg_take", [](const entvars_t* pev) { return std::to_string( pev->dmg_take ); } },
        { "dmg_save", [](const entvars_t* pev) { return std::to_string( pev->dmg_save ); } },
        { "dmg", [](const entvars_t* pev) { return std::to_string( pev->dmg ); } },
        { "dmgtime", [](const entvars_t* pev) { return std::to_string( pev->dmgtime ); } },
        { "noise", [](const entvars_t* pev) { return STRING( pev->noise ); } },
        { "noise1", [](const entvars_t* pev) { return STRING( pev->noise1 ); } },
        { "noise2", [](const entvars_t* pev) { return STRING( pev->noise2 ); } },
        { "noise3", [](const entvars_t* pev) { return STRING( pev->noise3 ); } },
        { "speed", [](const entvars_t* pev) { return std::to_string( pev->speed ); } },
        { "air_finished", [](const entvars_t* pev) { return std::to_string( pev->air_finished ); } },
        { "pain_finished", [](const entvars_t* pev) { return std::to_string( pev->pain_finished ); } },
        { "radsuit_finished", [](const entvars_t* pev) { return std::to_string( pev->radsuit_finished ); } },
//        { "pContainingEntity", [](const entvars_t* pev) { return std::to_string( pev->pContainingEntity ); } },
        { "playerclass", [](const entvars_t* pev) { return std::to_string( pev->playerclass ); } },
        { "maxspeed", [](const entvars_t* pev) { return std::to_string( pev->maxspeed ); } },
        { "fov", [](const entvars_t* pev) { return std::to_string( pev->fov ); } },
        { "weaponanim", [](const entvars_t* pev) { return std::to_string( pev->weaponanim ); } },
        { "pushmsec", [](const entvars_t* pev) { return std::to_string( pev->pushmsec ); } },
        { "bInDuck", [](const entvars_t* pev) { return std::to_string( pev->bInDuck ); } },
        { "flTimeStepSound", [](const entvars_t* pev) { return std::to_string( pev->flTimeStepSound ); } },
        { "flSwimTime", [](const entvars_t* pev) { return std::to_string( pev->flSwimTime ); } },
        { "flDuckTime", [](const entvars_t* pev) { return std::to_string( pev->flDuckTime ); } },
        { "iStepLeft", [](const entvars_t* pev) { return std::to_string( pev->iStepLeft ); } },
        { "flFallVelocity", [](const entvars_t* pev) { return std::to_string( pev->flFallVelocity ); } },
        { "gamestate", [](const entvars_t* pev) { return std::to_string( pev->gamestate ); } },
        { "oldbuttons", [](const entvars_t* pev) { return std::to_string( pev->oldbuttons ); } },
        { "groupinfo", [](const entvars_t* pev) { return std::to_string( pev->groupinfo ); } },
        { "iuser1", [](const entvars_t* pev) { return std::to_string( pev->iuser1 ); } },
        { "iuser2", [](const entvars_t* pev) { return std::to_string( pev->iuser2 ); } },
        { "iuser3", [](const entvars_t* pev) { return std::to_string( pev->iuser3 ); } },
        { "iuser4", [](const entvars_t* pev) { return std::to_string( pev->iuser4 ); } },
        { "fuser1", [](const entvars_t* pev) { return std::to_string( pev->fuser1 ); } },
        { "fuser2", [](const entvars_t* pev) { return std::to_string( pev->fuser2 ); } },
        { "fuser3", [](const entvars_t* pev) { return std::to_string( pev->fuser3 ); } },
        { "fuser4", [](const entvars_t* pev) { return std::to_string( pev->fuser4 ); } },
        { "vuser1", [](const entvars_t* pev) { return pev->vuser1.ToString(); } },
        { "vuser2", [](const entvars_t* pev) { return pev->vuser2.ToString(); } },
        { "vuser3", [](const entvars_t* pev) { return pev->vuser3.ToString(); } },
        { "vuser4", [](const entvars_t* pev) { return pev->vuser4.ToString(); } },
//        { "euser1", [](const entvars_t* pev) { return std::to_string( pev->euser1 ); } },
//        { "euser2", [](const entvars_t* pev) { return std::to_string( pev->euser2 ); } },
//        { "euser3", [](const entvars_t* pev) { return std::to_string( pev->euser3 ); } },
//        { "euser4", [](const entvars_t* pev) { return std::to_string( pev->euser4 ); } },
    };

    if( auto var = entvars_map.find( sKey ); var != entvars_map.end() )
	{
        return var->second( pev );
    }

	return ( keyvalues.find( sKey ) != keyvalues.end() ? keyvalues[ sKey ] : std::string( DefaultValue ) );
}
