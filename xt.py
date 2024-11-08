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
    match_events = []
    for match_id in match_list:
        print(f"processing match no {match_id}")
        for new_event in get_events_from_match_id(match_id):
            match_events.append(new_event)

    pass_events = []
    carry_events = []
    successful_shot_events = []
    missed_shot_events = []

    for event in match_events:
        try:
            if event["type"]["name"] == "Pass":
                pass_events.append(event)
                if event["location"][0]>120 or event["location"][1]>80:
                    print(f"Event {event['id']}")
                    exit(0)
            elif event["type"]["name"] == "Carry":
                carry_events.append(event)
            elif event["type"]["name"] == "Shot":
                if event["shot"]["outcome"]["name"] == "Goal":
                    successful_shot_events.append(event)
                else:
                    missed_shot_events.append(event)
        except:
            print(f"Could not process event {event}")


    print(f'{len(pass_events)=}')

    print(f'{len(carry_events)=}')

    print(f'{len(missed_shot_events)=}')

    print(f'{len(successful_shot_events)=}')

    return pass_events, carry_events, successful_shot_events, missed_shot_events

def get_array_position_from_field_indexes(length_index, width_index) -> int:
    return (width_index)*LENGTH_SUBDIVISION_AMOUNT+length_index

def get_field_indexes_from_coordinates(x_coordinate: float, y_coordinate: float) -> Tuple[int, int]:
    length_index = min(11,(floor(x_coordinate) - (floor(x_coordinate) % SUBDIVISION_SIZE))/SUBDIVISION_SIZE)
    width_index = min(7,(floor(y_coordinate) - (floor(y_coordinate) % SUBDIVISION_SIZE))/SUBDIVISION_SIZE)

    

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

def generate_base_matrix_3d():
    matrix = [[0]*LENGTH_SUBDIVISION_AMOUNT*WIDTH_SUBDIVISION_AMOUNT for _ in range(LENGTH_SUBDIVISION_AMOUNT*WIDTH_SUBDIVISION_AMOUNT)]
    # print(f'{matrix=}')
    # matrix[0][0] += 1
    # print(f'{matrix=}')
    return matrix

def generate_base_matrix_2d():
    return [0]*LENGTH_SUBDIVISION_AMOUNT*WIDTH_SUBDIVISION_AMOUNT

def generate_movement_matrix(pass_events, carry_events):
    matrix = generate_base_matrix_3d()
    # print(f'{matrix=}')
    # print(f'{len(matrix)=}')
    # print(f'{len(matrix[0])=}')

    for pass_event in pass_events:
        start_x, start_y, end_x, end_y = get_positions_from_pass(pass_event)
        start_lindex, start_windex = get_field_indexes_from_coordinates(start_x, start_y)
        end_lindex, end_windex = get_field_indexes_from_coordinates(end_x, end_y)
        start_array_index = get_array_position_from_field_indexes(start_lindex, start_windex)
        end_array_index = get_array_position_from_field_indexes(end_lindex, end_windex)
        matrix[start_array_index][end_array_index] += 1
        # print(f'{matrix[start_array_index][end_array_index]=}')
        # print(f'{start_array_index=}')
        # print(f'{end_array_index=}')
    # print(f'{matrix=}')

    for carry_event in carry_events:
        start_x, start_y, end_x, end_y = get_positions_from_carry(carry_event)
        start_lindex, start_windex = get_field_indexes_from_coordinates(start_x, start_y)
        end_lindex, end_windex = get_field_indexes_from_coordinates(end_x, end_y)
        start_array_index = get_array_position_from_field_indexes(start_lindex, start_windex)
        end_array_index = get_array_position_from_field_indexes(end_lindex, end_windex)
        matrix[start_array_index][end_array_index] += 1

    # print(f'{matrix[0]=}')
    # test = 0
    # for index in matrix[0]:
    #     test += matrix[0][index]
    # print(f'{test=}')
    # print(f'{matrix[45]=}')
    # matrix[0][0] +=1

    # print(f'{matrix[0]=}')
    # test = 0
    # for index in matrix[0]:
    #     test += matrix[0][index]
    # print(f'{test=}')
    # print(f'{matrix[45]=}')
    
    return matrix

def generate_transition_matrix(movement_matrix):
    for index in range(len(movement_matrix)):
        summed_movements = 0
        for destination_index in range(len(movement_matrix[index])):
            summed_movements += movement_matrix[index][destination_index]
        for destination_index in range(len(movement_matrix[index])):
            movement_matrix[index][destination_index] = movement_matrix[index][destination_index]/summed_movements if summed_movements else 0
    # print(f'{movement_matrix[0]=}')
    # print(f'{movement_matrix[45]=}')
    
    return movement_matrix

def generate_shot_matrix(successful_shot_events, missed_shot_events):
    shot_count_matrix = generate_base_matrix_2d()
    shot_success_matrix = generate_base_matrix_2d()

    for shot_event in successful_shot_events:
        shot_x, shot_y = get_position_from_shot(shot_event)
        shot_lindex, shot_windex = get_field_indexes_from_coordinates(shot_x, shot_y)
        array_index = get_array_position_from_field_indexes(shot_lindex, shot_windex)
        shot_count_matrix[array_index] += 1
        shot_success_matrix[array_index] += 1
        print(f'{shot_x=}')
        print(f'{shot_y=}')
        print(f'{shot_lindex=}')
        print(f'{shot_windex=}')
        print(f'{array_index=}')

    for shot_event in missed_shot_events:
        shot_x, shot_y = get_position_from_shot(shot_event)
        shot_lindex, shot_windex = get_field_indexes_from_coordinates(shot_x, shot_y)
        array_index = get_array_position_from_field_indexes(shot_lindex, shot_windex)
        shot_count_matrix[array_index] += 1
    
    for index in range(len(shot_success_matrix)):
        shot_success_matrix[index] = shot_success_matrix[index]/shot_count_matrix[index] if shot_count_matrix[index] else 0
    # print(f'{shot_count_matrix=}')
    # print(f'{shot_success_matrix=}')


    plot_shots(successful_shot_events)
    plot_shots(missed_shot_events)










    return shot_count_matrix, shot_success_matrix

def plot_shots(shot_events):
    locations = []
    for event in shot_events:
        locations.append(event["location"])
    print(f'{locations=}')

    import matplotlib.pyplot as plt

    x = [loc[0] for loc in locations]
    y = [loc[1] for loc in locations]
    
    plt.scatter(x, y)
    plt.show()


def generate_movement_probability_matrix(movement_transition_matrix, shot_matrix):
    movement_probability_matrix = generate_base_matrix_2d()
    for index in range(len(movement_probability_matrix)):
        movement_sum = 0
        for destination_index in range(len(movement_transition_matrix[index])):
            movement_sum += movement_transition_matrix[index][destination_index]
        movement_probability_matrix[index] = movement_sum/total_events if (total_events:=(movement_sum+shot_matrix[index])) else 0
    return movement_probability_matrix

def calculate_summed_xt(xt_matrix, index_to_calculate, transition_matrix):
    summed_xt = 0
    for index in range(len(xt_matrix[index_to_calculate])):
        summed_xt += xt_matrix[index_to_calculate][index]*transition_matrix[index_to_calculate][index]

def build_xt_matrix(competition_id: int, season_id: int):
    pass_events, carry_events, successful_shot_events, missed_shot_events = get_events_sorted(competition_id, season_id)

    movement_transition_matrix = generate_movement_matrix(pass_events, carry_events)

    shot_matrix, conversion_matrix = generate_shot_matrix(successful_shot_events, missed_shot_events)

    parsed_list = [shot_matrix[LENGTH_SUBDIVISION_AMOUNT*i:LENGTH_SUBDIVISION_AMOUNT*(i+1)] for i in range(WIDTH_SUBDIVISION_AMOUNT)]
    # print(f'{parsed_list=}')

    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(parsed_list, cmap='hot', interpolation='nearest')
    plt.show()



    xt_base_matrix = generate_base_matrix_2d()

    xt_matrix = generate_base_matrix_2d()

    movement_probability_matrix = generate_movement_probability_matrix(movement_transition_matrix, shot_matrix)

    transition_matrix = generate_transition_matrix(movement_transition_matrix)

    # print(f'{transition_matrix[42]=}')

    for _ in range(10):
        for index in range(len(xt_base_matrix)):
            summed_xt = 0
            for destination_index in range(len(transition_matrix[index])):
                summed_xt += transition_matrix[index][destination_index] * xt_base_matrix[destination_index]
            # print(f'{summed_xt=}')
            xt_matrix[index] = (1 - movement_probability_matrix[index]) * conversion_matrix[index] + movement_probability_matrix[index] * summed_xt
            # xt_matrix[index] = (1 - movement_probability_matrix[index]) * conversion_matrix[index]
        xt_base_matrix = xt_matrix

    parsed_list = [xt_matrix[LENGTH_SUBDIVISION_AMOUNT*i:LENGTH_SUBDIVISION_AMOUNT*(i+1)] for i in range(WIDTH_SUBDIVISION_AMOUNT)]
    # print(f'{parsed_list=}')

    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(parsed_list, cmap='hot', interpolation='nearest')
    plt.show()

    return xt_matrix



competition_id = 7
season_id = 27

build_xt_matrix(competition_id, season_id)
