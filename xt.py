from event_extraction import get_events_from_match_id, get_matches_from_season_and_competition
from math import floor
from typing import Tuple

FOOTBALL_FIELD_LENGTH = 120
FOOTBALL_FIELD_WIDTH = 80
SUBDIVISION_SIZE = 10
LENGTH_SUBDIVISION_AMOUNT = int(FOOTBALL_FIELD_LENGTH/SUBDIVISION_SIZE)
WIDTH_SUBDIVISION_AMOUNT = int(FOOTBALL_FIELD_WIDTH/SUBDIVISION_SIZE)

def get_events_sorted(competition_id: int, season_id: int):
    match_list = get_matches_from_season_and_competition(competition_id, season_id)
    print(f'{match_list[0]=}')
    match_events = get_events_from_match_id(match_list[0])
    print(f'{match_events=}')

    # print(set([event['type']['name'] for event in match_events]))

    pass_events = []
    carry_events = []
    successful_shot_events = []
    missed_shot_events = []

    for event in match_events:
        if event["type"]["name"] == "Pass":
            pass_events.append(event)
        elif event["type"]["name"] == "Carry":
            carry_events.append(event)
        elif event["type"]["name"] == "Shot":
            if event["shot"]["outcome"]["name"] == "Goal":
                successful_shot_events.append(event)
            else:
                missed_shot_events.append(event)

    print(f'{len(pass_events)=}')

    print(f'{len(carry_events)=}')

    print(f'{len(missed_shot_events)=}')

    print(f'{len(successful_shot_events)=}')

    return pass_events, carry_events, successful_shot_events, missed_shot_events

def get_array_position_from_field_indexes(length_index, width_index) -> int:
    return (width_index - 1)*LENGTH_SUBDIVISION_AMOUNT+length_index - 1

def get_field_indexes_from_coordinates(x_coordinate: float, y_coordinate: float) -> Tuple[int, int]:
    length_index = (floor(x_coordinate) - (floor(x_coordinate) % SUBDIVISION_SIZE))/SUBDIVISION_SIZE
    width_index = (floor(y_coordinate) - (floor(y_coordinate) % SUBDIVISION_SIZE))/SUBDIVISION_SIZE

    return int(length_index), int(width_index)

def get_positions_from_pass(pass_event) -> Tuple[int, int, int, int]:
    start_position = pass_event['location']
    end_position = pass_event['pass']['end_location']
    return start_position[0], start_position[1], end_position[0], end_position[1]

def get_positions_from_carry(carry_event) -> Tuple[int, int, int, int]:
    start_position = carry_event['location']
    end_position = carry_event['carry']['end_location']
    return start_position[0], start_position[1], end_position[0], end_position[1]

def get_position_from_shot(shot_event) -> Tuple[int, int]:
    shot_position = shot_event["location"]
    return shot_position[0], shot_position[1]

def generate_base_matrix_pass():
    return [[0]*LENGTH_SUBDIVISION_AMOUNT*WIDTH_SUBDIVISION_AMOUNT]*LENGTH_SUBDIVISION_AMOUNT*WIDTH_SUBDIVISION_AMOUNT

def generate_base_matrix_shot():
    return [0]*LENGTH_SUBDIVISION_AMOUNT*WIDTH_SUBDIVISION_AMOUNT

def generate_movement_matrix(pass_events, carry_events):
    matrix = generate_base_matrix_pass()

    for pass_event in pass_events:
        start_x, start_y, end_x, end_y = get_positions_from_pass(pass_event)
        start_lindex, start_windex = get_field_indexes_from_coordinates(start_x, start_y)
        end_lindex, end_windex = get_field_indexes_from_coordinates(end_x, end_y)
        start_array_index = get_array_position_from_field_indexes(start_lindex, start_windex)
        end_array_index = get_array_position_from_field_indexes(end_lindex, end_windex)
        matrix[start_array_index][end_array_index] += 1
    # print(f'{matrix=}')

    for carry_event in carry_events:
        start_x, start_y, end_x, end_y = get_positions_from_carry(carry_event)
        start_lindex, start_windex = get_field_indexes_from_coordinates(start_x, start_y)
        end_lindex, end_windex = get_field_indexes_from_coordinates(end_x, end_y)
        start_array_index = get_array_position_from_field_indexes(start_lindex, start_windex)
        end_array_index = get_array_position_from_field_indexes(end_lindex, end_windex)
        matrix[start_array_index][end_array_index] += 1
    # print(f'{matrix=}')

    return matrix

def generate_shot_matrix(successful_shot_events, missed_shot_events):
    shot_count_matrix = generate_base_matrix_shot()
    shot_success_matrix = generate_base_matrix_shot()

    for shot_event in successful_shot_events:
        shot_x, shot_y = get_position_from_shot(shot_event)
        shot_lindex, shot_windex = get_field_indexes_from_coordinates(shot_x, shot_y)
        array_index = get_array_position_from_field_indexes(shot_lindex, shot_windex)
        shot_count_matrix[array_index] += 1
        shot_success_matrix[array_index] += 1

    for shot_event in missed_shot_events:
        shot_x, shot_y = get_position_from_shot(shot_event)
        shot_lindex, shot_windex = get_field_indexes_from_coordinates(shot_x, shot_y)
        array_index = get_array_position_from_field_indexes(shot_lindex, shot_windex)
        shot_count_matrix[array_index] += 1
    
    for index in range(len(shot_success_matrix)):
        shot_success_matrix[index] = shot_success_matrix[index]/shot_count_matrix[index] if shot_count_matrix[index] else 0
    # print(f'{shot_count_matrix=}')
    # print(f'{shot_success_matrix=}')

    return shot_count_matrix, shot_success_matrix




competition_id = 7
season_id = 27

pass_events, carry_events, successful_shot_events, missed_shot_events = get_events_sorted(competition_id, season_id)

generate_movement_matrix(pass_events, carry_events)

generate_shot_matrix(successful_shot_events, missed_shot_events)