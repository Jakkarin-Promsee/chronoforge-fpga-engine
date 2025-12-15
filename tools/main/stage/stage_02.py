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
        gravity_direction=0,
        display_pos_x1=0,
        display_pos_y1=0,
        display_pos_x2=0,
        display_pos_y2=0,
    )

    # ------------------------------------------------------------------
    # Common Parameters
    # ------------------------------------------------------------------
    PLATFORM_SIZE = 70
    PLATFORM_GAP_X = 30
    PLATFORM_GAP_y = 50
    PLATFORM_X = 85
    PLATFORM_Y = 140


    # ------------------------------------------------------------------
    # Initial Delay (2 seconds)
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
            wait_time=9,
            destroy_time=0,
            destroy_trigger=2,
        )
    )

    # ------------------------------------------------------------------
    # Platform Placeholder (No Movement)
    # ------------------------------------------------------------------
    stage.platform_objects.append(
        PlatformObject(
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
    # Helper: Create Left / Right Wall Pair with Vertical Gap
    # ------------------------------------------------------------------
    def generate_row(platform_y):

        stage.platform_objects.extend([
            
                 PlatformObject(
                    movement_direction=0,
                    speed=0,
                    pos_x=PLATFORM_X + (PLATFORM_SIZE+PLATFORM_GAP_X)*i,
                    pos_y=platform_y,
                    w=PLATFORM_X,
                    h=12,
                    wait_time=0,
                    destroy_time=6,
                    destroy_trigger=2,
                ) for i in range(5)
            
        ])

    # ------------------------------------------------------------------
    # Repeating Symmetric Wall Pattern
    # ------------------------------------------------------------------
    for i in range(5):
        generate_row(
            PLATFORM_Y + (12+PLATFORM_GAP_y)*i
        )

    return stage
