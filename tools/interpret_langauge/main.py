from game_class import EntireGame, GameStage, GameManager, AttackObject, PlatformObject

game = EntireGame()


stage0 = GameStage()

stage0.game_manager = GameManager(
    stage=0,
    wait_time=5,
    gravity_direction=0,
    display_pos_x1=245,
    display_pos_y1=229,
    display_pos_x2=403,
    display_pos_y2=386
)

normal_speed = 12
initial_w = 12
initial_h_d = 72
initial_h_u = 46
delay1 = 0
delay2 = 0.3

attack_pairs = [
    (
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed,
            pos_x=stage0.game_manager.display_pos_x1-initial_w,
            pos_y=stage0.game_manager.display_pos_y2 - initial_h_d - i * 8,
            w=initial_w,
            h=initial_h_d - i * 8,
            wait_time=delay1,
            destroy_time=20,
            destroy_trigger=2
        ),
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed,
            pos_x=stage0.game_manager.display_pos_x1-initial_w,
            pos_y=stage0.game_manager.display_pos_y1,
            w=initial_w,
            h=initial_h_u + i * 8,
            wait_time=delay2,
            destroy_time=20,
            destroy_trigger=2
        )
    )
    for i in range(10)
]

# Add attack object
first_i_dir = 4
stage0.attack_objects.extend([
    # Start with 0, increase idx 1
    obj  for i in range(first_i_dir+1) 

    for obj in (
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed, pos_x=stage0.game_manager.display_pos_x1-initial_w, 
            pos_y=stage0.game_manager.display_pos_y2 - initial_h_d - i*8,
            w=initial_w, h=initial_h_d + i*8, wait_time=delay1, destroy_time=20,
            destroy_trigger=2
        ),
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed, pos_x=stage0.game_manager.display_pos_x1-initial_w, 
            pos_y=stage0.game_manager.display_pos_y1,
            w=initial_w, h=initial_h_u - i*8, wait_time=delay2, destroy_time=20,
            destroy_trigger=2
        ) 
    )
])

second_i_dir = 11
stage0.attack_objects.extend([
    obj  for i in range(second_i_dir + 1) 

    for obj in (
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed, pos_x=stage0.game_manager.display_pos_x1-initial_w, 
            pos_y=stage0.game_manager.display_pos_y2 - initial_h_d + i*8 - first_i_dir*8,
            w=initial_w, h=initial_h_d - i*8 + first_i_dir*8, wait_time=delay1, destroy_time=20,
            destroy_trigger=2
        ),
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed, pos_x=stage0.game_manager.display_pos_x1-initial_w, 
            pos_y=stage0.game_manager.display_pos_y1,
            w=initial_w, h=initial_h_u + i*8 - first_i_dir*8, wait_time=delay2, destroy_time=20,
            destroy_trigger=2
        ) 
    )
])



third_i_dir = 6
stage0.attack_objects.extend([
    obj  for i in range(third_i_dir+1) 

    for obj in (
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed, pos_x=stage0.game_manager.display_pos_x1-initial_w, 
            pos_y=stage0.game_manager.display_pos_y2 - initial_h_d - i*8 + second_i_dir*8 - first_i_dir*8,
            w=initial_w, h=initial_h_d + i*8 - second_i_dir*8 + first_i_dir*8, wait_time=delay1, destroy_time=20,
            destroy_trigger=2
        ),
        AttackObject(
            type=0, colider_type=0, movement_direction=2,
            speed=normal_speed, pos_x=stage0.game_manager.display_pos_x1-initial_w, 
            pos_y=stage0.game_manager.display_pos_y1,
            w=initial_w, h=initial_h_u - i*8 + second_i_dir*8 - first_i_dir*8, wait_time=delay2, destroy_time=20,
            destroy_trigger=2
        ) 
    )
])


# Add platform object
stage0.platform_objects.append(
    PlatformObject(
        movement_direction=2, speed=0,
        pos_x=0, pos_y=0,
        w=0, h=0, wait_time=0,
        destroy_time=0, destroy_trigger=0
    )
)

game.add_stage(stage0)

# Export
game.export("source", is_base=0)
