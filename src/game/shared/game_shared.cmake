function(add_game_shared_sources target)
	target_sources(${target}
		PRIVATE
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/CGameLibrary.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/CGameLibrary.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/palette.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/voice_common.h
			
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigConditionals.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigConditionals.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigDefinition.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigDefinition.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigIncludeStack.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigLoader.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigLoader.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/GameConfigSection.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/sections/CommandsSection.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/sections/EchoSection.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/sections/GlobalModelReplacementSection.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/sections/HudColorSection.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/config/sections/SuitLightTypeSection.h
			
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/ehandle.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/ehandle.h
			
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CDisplacer.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CDisplacer.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CEagle.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CEagle.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CGrapple.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CGrapple.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CKnife.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CKnife.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CM249.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CM249.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CPenguin.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CPenguin.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CPipewrench.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CPipewrench.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/crossbow.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/crowbar.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CShockRifle.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CShockRifle.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CSniperRifle.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CSniperRifle.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CSporeLauncher.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/CSporeLauncher.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/egon.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/gauss.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/glock.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/handgrenade.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/hornetgun.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/mp5.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/python.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/rpg.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/satchel.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/shotgun.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/squeakgrenade.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/tripmine.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/weapons_shared.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/entities/items/weapons/weapons.h
			
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_debug.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_debug.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_defs.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_info.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_materials.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_math.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_movevars.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_shared.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/player_movement/pm_shared.h
			
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/scripting/AS/as_addons.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/scripting/AS/as_utils.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/scripting/AS/as_utils.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/scripting/AS/CASManager.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/scripting/AS/CASManager.h
			
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/CLogSystem.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/CLogSystem.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/command_utils.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/command_utils.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/CStringPool.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/CStringPool.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/filesystem_utils.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/filesystem_utils.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/GameSystem.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/GameSystem.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/heterogeneous_lookup.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/json_fwd.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/json_utils.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/json_utils.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/logging_utils.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/ModelReplacement.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/ModelReplacement.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/shared_utils.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/shared_utils.h
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/string_utils.cpp
			${CMAKE_CURRENT_FUNCTION_LIST_DIR}/utils/string_utils.h)
endfunction()
