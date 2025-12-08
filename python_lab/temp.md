SO now let start to work again. I'm having a plan to write README.md for my cpu runtime, game engine activation, my binary code stucuture, my python compiler from json to bin, etc.

First, I using FPGA basys 3 board to connect with 640\*480 60Hz resolution. I use 5 BUFG connect to main clk that run at 100MHz, all crucial main runtime will run with this. 1st the clk_vga run at 25MHz to sync display, 2nd the clk_player_control that run at 100Hz to manage all player position activity include switch control, gravity, moementum, etc. 3rd clk_object_control that run at 100Hz using to control all object in the game that doesn't player, just seperate for safetly first. 4th clk_centi_second that run on 100Hz, on that name, all module will use this clk to count time. and last 5th clk_calculation that run at 1kH, this clk will maintain other calculation, such as register new object from main runtime, hard calculation, or something that need another level speed from normal.

Second how run time work? The main ideas is using game_manager.mem that hold:

```json
{
  "stage": "2^8", // State ID (256 uniques)
  "attack_amount": "2^10", // Attack amount to read from attack.mem (1024 attacks)
  "platform_amount": "2^10", // Platform amount to read from platform.mem (1024 attacks)
  "gravity_direction": "2^3", // 0 gravity and 4 gravity axis
  "display_pos_x1": "2^8", // position x1 (multiply 4 before use in game)
  "display_pos_y1": "2^8", // position x2 (multiply 4 before use in game)
  "display_pos_x2": "2^8", // position x1 (multiply 4 before use in game)
  "display_pos_y2": "2^8", // position x2 (multiply 4 before use in game)
  "wait_time": "2^8", // Waiting time before next stage (25.6 seconds)
  "free(unused)": "2^1" // Unused for now
}
```

That file will keep this scence loading data sequence. The main runtime will continous read from address 0 to n, then loop to 0 again. I name it "game_runtime". This main runtime will read attack_amount that read attack.mem:

```json
{
  "type": "2^5", // attack type (32 types, design for future work too)
  "colider_type": "2^2", // Squar, Circle/Capsule, Tilt left capsule, Tilt right capsule.
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^5", // 32 levels of speed
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "wait_time": "2^8", // Waiting time before next stage (25.6 seconds)
  "destroy_time": "2^8", // 0 for out of screen, 1 for our of display screen, and other are (25.4 second)
  "destroy_trigger": "2^2", // 0 untrigger, 1 destroy when end scrren, 2 destroy when end display blcok, 3 destrou when hit player
  "free(unused)": "2^7" // Unused for now
}
```

And platform_amount that read platform.mem:

```json
{
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^5", // 32 levels of speed
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "wait_time": "2^8", // Waiting time before next stage (25.6 seconds)
  "destroy_time": "2^8", // Waiting before attack destroy (256 second)
  "destroy_trigger": "2^2", // 0 untrigger, 1 destroy when end scrren, 2 destroy when end display blcok, 3 destrou when hit player
  "free(unused)": "2^6" // Unused for now
}
```

I will tell you thier loop. First game manager runtime will read current stage at address `CS`, it will read whole data from this adress. this module will how all index address for all platform and attack. And it will continoue run attack address from 0(not really 0, just a base for this current stage) to attack_amount(Read from ROM) and run platform address from 0(not really 0, just a base for this current stage) to platform_amout(Read from ROM) parallely. when all amout was been done, it's address `CS` will go to the next sequence, and go to read new attack-platfrom amout again.

By everytime between it's go to next attack and next platform, it has to wait attack_wait time and platform_weight time before update read adress. So this will make we can control all scene gameplay by our hand. Moreover, attack and platform will use seperate time count too. Such as if attack 1 have wait 2 second, attack 2 have to wait 10 second, and attack 3 have to wait 5 second, by the way platform 1 have waith 1 second, palt from 2 have to wait 20 second. The address will be attack 1 start pararel with platfrom 1 -> platform 2 (1s wait) -> attack 2 (2s wait) -> attack 3 (10s wait) -> attack 4 (5s wait) -> platform 3(20s wait). To update game manager adress too, it will wait on wait time that contain in .mem ROM

For more serious strucutre. It's runing with 3 pair of sync signal. There are sync_game_manager / update_game_mangager, sync_attack / update_attack, sync_platform / update_platform. My rule is sync signal will be send from parent module to control child module and update signal will send from child module to parent module to said the child was already done the task parent module give.

For instance: at first cycles after starting board, the parent game_manager_runtime will have the sync_game_manager = false and game_manager_addrs = 0, making game_manager_rom child module detect !sync_game_manager, so it will read at game_manager_addrs = 0 and set back update_game_manager = 1. When parent modules detect update_game_manager, it will set sync_game_manager to 1, and when child module see sync_game_manager = 1, it will set update_game_manager to 0 as idle state. This is how all module sending and updating data. With this ideas, all modules communicate so accurate at 100MHz, produce the right wait time to run entire system.

This is how we decode the data from 3 .mem ROM files. And with this, the game runtime will update data continuously entire of it life. But data still don't be hold, it's just sign until wait_time count done. So that why we have other 2 runtime modules name "multi_object_collider_runtime" and "multi_object_trigger_runtime" that will hold many of object in the game. These 2 runtime run at 1kHz or at clk_calculation.

Start with eco system from game runtime continous update address itself on time. The thing I do is when game runtime updatea attack or platform data, it will triger other 2 sysnc siganal name sync_attack_position / update_object_trigger_position and sync_platform_position / update_object_collider_position. I know now that name is make confuse a bit. But cause now I didn't have a plan to use other object to load for collider and trigger yet. So now all attack will load to trigger and all platform will load to colider for easy to handle its properties.

The way it works is Inside these multi object runtime, there are have main control with itertor_ready_state. when sync_position signal from game runtime module (parent) is false, this will trigger multi object runtime to pull data from game runtime, and push to its submodule (the single object runtime). And the way it select is read from itertor_ready_state array. when multi object runtime has done to load data to single object runtimes, it will set itertor_ready_state at that interator to false, sending update_position signal to game runtime module, and then sync_position signal will set to true again.

And yeah, between multi object runtime and sigle object runtime are still using pair wire for sync. As I said above, multi object runtime will update by set sync signal to false, making child module update itself, sending update signal back, synch back to true. But there are more special, that is itertor_ready_state isn't hold at multi object runtime, but it's the wire that connect for all sigle object runtime. ALl single object runtime will decide itself to be free or not.

Single object runtime will load all data including destroy_trigger and destroy_time to tell it which way the object will done task, if it's done loading, its ready_state will be false. And when its task has done, it will destroy itself, ready state come true again.

And this all is how all runtime syns and working togather. The current strucuture is V4. I'm refactor it more and more time to decentralize task.

Next the way we calculate collider / trigger object to player. I using easy way to compare it. Instead of add all single object runtime to player modules, I use the way that use less wire. I will send only player position and size to multi object runtime. At collider, assume now we are compute ground for player, we will compute only the object that below player and in player range, the object that place at highest from all object that still less than player. So if it has I will return is_collider_ground_player = true and sending back interger collider_ground_y_player. So then player_controller will act like collider_ground_y_player as a ground to disable gravity. More over, I use the update position way with 2 px buffer, even collider objecr are moving up, the buffer of 2px will still push player up. And We will use this method for 4 axis.
and for trigger object, we just check that is player and object are overlapse or not.

So in render way, the Limitations is vga runing at 25MHz while main clk run at 100MHz, My plan is using regiester variable at player display size to hold all object overide each other. Except that areas, we will compare color by just simple if-else. This method will help us can compute huge object in game display zone efficient and still not use register variable much.
