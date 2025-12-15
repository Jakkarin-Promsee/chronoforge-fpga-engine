import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from interpret_langauge.game_class import GameStage, GameManager, AttackObject, PlatformObject


def stage():
    stage = GameStage()

    # ------------------------------------------------------------------
    # Game Manager Configuration
    # ------------------------------------------------------------------
    stage.game_manager = GameManager(
        stage=1,
        wait_time=1,
        gravity_direction=3,
        display_pos_x1=136,
        display_pos_y1=256,
        display_pos_x2=508,
        display_pos_y2=384,
    )

    # ------------------------------------------------------------------
    # Common Parameters
    # ------------------------------------------------------------------
    ATTACK_SPEED = 9
    BAR_WIDTH = 12
    BAR_HEIGHT = 40

    TOP_EDGE_Y = stage.game_manager.display_pos_y1
    BOTTOM_EDGE_Y = stage.game_manager.display_pos_y2


    LEFT_DELAY = 0
    RIGHT_DELAY = 2

    REPEAT_COUNT = 10

    # ------------------------------------------------------------------
    # Initial Delay (3 seconds)
    # ------------------------------------------------------------------
    stage.attack_objects.append(
        AttackObject(
            type=0,
            colider_type=0,
            movement_direction=2,
            speed=0,
            pos_x=0,
            pos_y=0,
            w=0,
            h=0,
            wait_time=3,
            destroy_time=0,
            destroy_trigger=2,
        )
    )

    # Ground spire
    stage.attack_objects.append(
        AttackObject(
            type=0,
            colider_type=0,
            movement_direction=0,
            speed=0,
            pos_x=136,
            pos_y=384-20,
            w=374,
            h=20,
            wait_time=0,
            destroy_time=25.5,
            destroy_trigger=2,
        )
    )

    # ------------------------------------------------------------------
    # Helper: Create Left / Right Wall Pair with Vertical Gap
    # ------------------------------------------------------------------
    def add_vertical_pair(right_delay):
        upper_y = TOP_EDGE_Y - BAR_HEIGHT
        lower_y = BOTTOM_EDGE_Y

        stage.attack_objects.extend([
            AttackObject(
                type=0,
                colider_type=0,
                movement_direction=0,
                speed=ATTACK_SPEED,
                pos_x=283,
                pos_y=lower_y,
                w=BAR_WIDTH,
                h=BAR_HEIGHT,
                wait_time=LEFT_DELAY,
                destroy_time=20,
                destroy_trigger=2,
            ),
            AttackObject(
                type=0,
                colider_type=0,
                movement_direction=4,
                speed=ATTACK_SPEED,
                pos_x=363,
                pos_y=upper_y,
                w=BAR_WIDTH,
                h=BAR_HEIGHT,
                wait_time=LEFT_DELAY,
                destroy_time=20,
                destroy_trigger=2,
            ),
            AttackObject(
                type=0,
                colider_type=0,
                movement_direction=0,
                speed=ATTACK_SPEED,
                pos_x=443,
                pos_y=lower_y,
                w=BAR_WIDTH,
                h=BAR_HEIGHT,
                wait_time=right_delay,
                destroy_time=20,
                destroy_trigger=2,
            )
        ])

    # ------------------------------------------------------------------
    # Repeating Symmetric Wall Pattern
    # ------------------------------------------------------------------
    for _ in range(REPEAT_COUNT):
        add_vertical_pair(
            right_delay = RIGHT_DELAY
        )

    # ------------------------------------------------------------------
    # Last Delay (5 seconds)
    # ------------------------------------------------------------------
    stage.attack_objects.append(
        AttackObject(
            type=0,
            colider_type=0,
            movement_direction=2,
            speed=0,
            pos_x=0,
            pos_y=0,
            w=0,
            h=0,
            wait_time=2,
            destroy_time=0,
            destroy_trigger=2,
        )
    )

    # ------------------------------------------------------------------
    # Platform Placeholder (No Movement)
    # ------------------------------------------------------------------
    for _ in range(6):
        stage.platform_objects.append(
            PlatformObject(
                movement_direction=2,
                speed=6,
                pos_x=137 - 62,
                pos_y=338,
                w=62,
                h=8,
                wait_time=2,
                destroy_time=20,
                destroy_trigger=2,
            )
        )
        stage.platform_objects.append(
            PlatformObject(
                movement_direction=6,
                speed=6,
                pos_x=508,
                pos_y=318,
                w=62,
                h=8,
                wait_time=2,
                destroy_time=20,
                destroy_trigger=2,
            )
        )

    return stage
