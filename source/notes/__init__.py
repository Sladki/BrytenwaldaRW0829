from source.header_operations import *
from source.header_common import *

from source.module_constants import *


scripts = [

    ("update_all_notes", [
        (call_script, "script_update_troop_notes", "trp_player"),
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
            (this_or_next | troop_slot_eq, ":troop_no", "slot_troop_occupation", slto_kingdom_hero),
            (this_or_next | troop_slot_eq, ":troop_no", "slot_troop_occupation", slto_kingdom_lady),
            (troop_slot_eq, ":troop_no", "slot_troop_occupation", slto_inactive_pretender),
            (call_script, "script_update_troop_notes", ":troop_no"),
        (try_end),
        (try_for_range, ":center_no", centers_begin, centers_end),
            (call_script, "script_update_center_notes", ":center_no"),
        (try_end),
        (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
            (call_script, "script_update_faction_notes", ":faction_no"),
        (try_end),
    ]),

    ("update_faction_notes", [
        (store_script_param, ":faction_no", 1),

        (try_begin),
            (this_or_next | faction_slot_eq, ":faction_no", "slot_faction_state", sfs_inactive),
            (eq, ":faction_no", "fac_player_faction"),
            (faction_set_note_available, ":faction_no", 0),
        (else_try),
            (faction_set_note_available, ":faction_no", 1),
        (try_end),
    ]),

    ("update_faction_political_notes", [
        (store_script_param, ":faction_no", 1),

        (call_script, "script_evaluate_realm_stability", ":faction_no"),
        (add_faction_note_from_sreg, ":faction_no", 2, "str_instability_reg0_of_lords_are_disgruntled_reg1_are_restless", 0),
    ]),

    ("update_faction_traveler_notes", [
        (store_script_param, ":faction_no", 1),

        (assign, ":total_men", 0),
        (try_for_parties, ":cur_party"),
            (store_faction_of_party, ":center_faction", ":cur_party"),
            (eq, ":center_faction", ":faction_no"),
            (party_get_num_companions, ":num_men", ":cur_party"),
            (val_add, ":total_men", ":num_men"),
        (try_end),

        (str_store_faction_name, s5, ":faction_no"),
        (assign, reg1, ":total_men"),
        (add_faction_note_from_sreg, ":faction_no", 1, "@{s5} has a strength of {reg1} men in total.", 1),
    ]),

    ("update_troop_notes", [
        # todo: Add code.
    ]),

    ("update_troop_location_notes", [
        (store_script_param, ":troop_no", 1),
        (store_script_param, ":see_or_hear", 2),

        (try_begin),
            (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
            (neq, reg0, 0),

            (call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
            (eq, reg0, -1),
            (troop_get_type, reg1, ":troop_no"),
            (val_mod, reg1, 2),

            (try_begin),
                (eq, ":see_or_hear", 0),
                (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you saw {reg1?her:him}, {s1}", 1),
            (else_try),
                (add_troop_note_from_sreg, ":troop_no", 2, "@The last time you heard about {reg1?her:him}, {s1}", 1),
            (try_end),
        (try_end),
    ]),

    ("update_troop_location_notes_prisoned", [
        (store_script_param, ":troop_no", 1),
        (store_script_param, ":capturer_faction_no", 2),

        (troop_get_type, reg1, ":troop_no"),
        (str_store_faction_name_link, s1, ":capturer_faction_no"),

        (add_troop_note_from_sreg, ":troop_no", 2, "str_reg1shehe_is_prisoner_of_s1", 1),

        (troop_get_type, reg1, ":troop_no"),
        (val_mod, reg1, 2),
        (str_store_faction_name_link, s1, ":capturer_faction_no"),

        (add_troop_note_from_sreg, ":troop_no", 2, "str_reg1shehe_is_prisoner_of_s1", 1),
    ]),

    ("update_troop_political_notes", [
        (store_script_param, ":troop_no", 1),

        (try_begin),
            (str_clear, s47),

            (store_faction_of_troop, ":troop_faction", ":troop_no"),

            (faction_get_slot, ":faction_leader", ":troop_faction", "slot_faction_leader"),

            (str_clear, s40),
            (assign, ":logged_a_rivalry", 0),
            (try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
                (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":kingdom_hero"),
                (lt, reg0, -10),

                (str_store_troop_name_link, s39, ":kingdom_hero"),
                (try_begin),
                    (eq, ":logged_a_rivalry", 0),
                    (str_store_string, s40, "str_s39_rival"),
                    (assign, ":logged_a_rivalry", 1),
                (else_try),
                    (str_store_string, s41, "str_s40"),
                    (str_store_string, s40, "str_s41_s39_rival"),
                (try_end),
            (try_end),

            (str_clear, s46),
            (try_begin),
                (ge, "$cheat_mode", 1),
                (try_begin),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_martial),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_martial_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_debauched),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_debauched_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_selfrighteous),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_pitiless_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_cunning),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_calculating_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_quarrelsome),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_quarrelsome_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_goodnatured),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_goodnatured_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_upstanding),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_upstanding_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_conventional),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_conventional_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_adventurous),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_adventurous_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_otherworldly),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_romantic_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_moralist),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_moralist_"),
                (else_try),
                    (troop_slot_eq, ":troop_no", "slot_lord_reputation_type", lrep_ambitious),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_ambitious_"),
                (else_try),
                    (troop_get_slot, reg11, ":troop_no", "slot_lord_reputation_type"),
                    (str_store_string, s46, "str_reputation_cheat_mode_only_reg11_"),
                (try_end),

            (try_begin),
                (eq, "$cheat_mode", 1),
                (try_for_range, ":love_interest_slot", "slot_troop_love_interest_1", "slot_troop_love_interests_end"),
                    (troop_get_slot, ":love_interest", ":troop_no", ":love_interest_slot"),
                    (is_between, ":love_interest", kingdom_ladies_begin, kingdom_ladies_end),
                    (str_store_troop_name_link, s39, ":love_interest"),
                    (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":love_interest"),
                    (str_store_string, s2, "str_love_interest"),
                    (try_begin),
                        (troop_slot_eq, ":troop_no", "slot_troop_betrothed", ":love_interest"),
                        (str_store_string, s2, "str_betrothed"),
                    (try_end),
                    (str_store_string, s40, "str_s40_s39_s2_reg0"),
                (try_end),
            (try_end),
        (try_end),

        (str_store_string, s45, "str_other_relations_s40_"),

        (str_clear, s44),
        (try_begin),
            (neq, ":troop_no", ":faction_leader"),
            (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
            (str_store_string, s44, "str_relation_with_liege_reg0_"),
        (try_end),

        (str_clear, s48),

        (try_begin),
            (eq, "$cheat_mode", 1),
            (store_current_hours, ":hours"),
            (gt, ":hours", 0),
            (call_script, "script_calculate_troop_political_factors_for_liege", ":troop_no", ":faction_leader"),
            (str_store_string, s48, "str_sense_of_security_military_reg1_court_position_reg3_"),
        (try_end),
        (str_store_string, s47, "str_s46s45s44s48"),

        (add_troop_note_from_sreg, ":troop_no", 3, "str_political_details_s47_", 1),

        (try_end),
    ]),

    ("update_center_notes", [
        (store_script_param, ":center_no", 1),

        (assign, ":hero_prisoners", 0),
        (party_get_slot, ":p_type", ":center_no", "slot_party_type"),
        (party_get_slot, ":spy_days", ":center_no", "slot_spy_in_town"),
        (store_current_hours, ":cur_hour"),
        (store_sub, ":total_time", ":cur_hour", ":spy_days"),
        (try_begin),
            (eq, ":total_time", ":cur_hour"),
            (assign, ":total_time", 0),
        (try_end),

        (try_begin),
            (ge, ":total_time", 24),
            (str_store_party_name, s5, ":center_no"),
            (add_party_note_from_sreg, ":center_no", 2, "str_spy_present", 0),
            (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":center_no"),
            (str_clear, s6),
            (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
                (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":stack_no"),
                (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
                (val_add, ":hero_prisoners", 1),
                (str_store_troop_name_link, s7, ":stack_troop"),
                (str_store_string, s6, "@{s6} {s7},"),
                (call_script, "script_update_troop_location_notes", ":stack_troop", 1),
            (try_end),

            (try_begin),
                (ge, ":hero_prisoners", 1),
                (add_party_note_from_sreg, ":center_no", 3, "@The following lords are held prisoner here: {s6}", 1),
            (else_try),
                (eq, ":hero_prisoners", 0),
                (le, ":p_type", 3),
                (add_party_note_from_sreg, ":center_no", 3, "@There are no lords held prisoner here.", 1),
            (try_end),
        (else_try),
            (party_slot_eq, ":center_no", "slot_spy_in_town", 0),
            (str_store_party_name, s5, ":center_no"),
            (add_party_note_from_sreg, ":center_no", 2, "str_spy_not_present", 0),
        (else_try),
            (is_between, ":total_time", 1, 24),
            (str_store_party_name, s5, ":center_no"),
            (add_party_note_from_sreg, ":center_no", 2, "str_spy_infiltrating", 0),
        (try_end),
    ]),

    # todo: script very similar to previous one. Consider creating a common script.
    ("update_center_recon_notes", [
        (store_script_param, ":center_no", 1),

        (assign, ":hero_prisoners", 0),
        (party_get_slot, ":p_type", ":center_no", "slot_party_type"),
        (party_get_slot, ":spy_days", ":center_no", "slot_spy_in_town"),
        (store_current_hours, ":cur_hour"),
        (store_sub, ":total_time", ":cur_hour", ":spy_days"),
        (try_begin),
            (eq, ":total_time", ":cur_hour"),
            (assign, ":total_time", 0),
        (try_end),

        (try_begin),
            (ge, ":total_time", 24),
            (str_store_party_name, s5, ":center_no"),
            (add_party_note_from_sreg, ":center_no", 2, "str_spy_present", 0),
            (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":center_no"),
            (str_clear, s6),
            (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
                (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":stack_no"),
                (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
                (val_add, ":hero_prisoners", 1),
                (str_store_troop_name_link, s7, ":stack_troop"),
                (str_store_string, s6, "@{s6} {s7},"),
                (call_script, "script_update_troop_location_notes", ":stack_troop", 1),
            (try_end),

            (try_begin),
                (ge, ":hero_prisoners", 1),
                (add_party_note_from_sreg, ":center_no", 3, "@The following lords are held prisoner here: {s6}", 1),
            (else_try),
                (eq, ":hero_prisoners", 0),
                (le, ":p_type", 3),
                (add_party_note_from_sreg, ":center_no", 3, "@There are no lords held prisoner here.", 1),
            (try_end),
        (try_end),

        (try_begin),
            (this_or_next | is_between, ":center_no", towns_begin, towns_end),
            (is_between, ":center_no", castles_begin, castles_end),
            (party_get_slot, ":center_food_store", ":center_no", "slot_party_food_store"),
            (call_script, "script_center_get_food_consumption", ":center_no"),
            (assign, ":food_consumption", reg0),
            (store_div, reg6, ":center_food_store", ":food_consumption"),
            (party_collect_attachments_to_party, ":center_no", "p_collective_ally"),
            (party_get_num_companions, reg5, "p_collective_ally"),
            (add_party_note_from_sreg, ":center_no", 1, "@Current garrison consists of {reg5} men.^Has food stock for {reg6} days.", 1),
        (try_end),
    ]),
]
