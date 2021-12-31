DELETE FROM active_users WHERE user_id > 0;
INSERT INTO active_users (user_nickname, user_id, user_game_id, user_grid, is_host, user_cash, user_pending_declaration, user_bank, deletion_time) VALUES ("testusr1",1,1,"itmKill,M200,M1000,M1000,M1000,M5000,M500,M500,M500,itmKill,itmKill,itmKill,M500,itmKill,itmSwap,itmSwap,itmSwap,itmSwap,M500,itmSteal,itmSteal,itmSteal,itmSteal,itmGift,itmGift,itmGift,itmGift,itmGift,itmBank,itmGift,itmGift,itmGift,itmGift,itmGift,itmGift,itmBank",1,0,0,0,-1);
INSERT INTO active_users (user_nickname, user_id, user_game_id, user_grid, is_host, user_cash, user_pending_declaration, user_bank, deletion_time) VALUES ("testusr2",2,1,"itmGift,itmGift,M1000,M1000,M1000,M5000,M500,M500,M500,M200,M200,M200,M500,M200,M200,M200,M200,M200,M500,M200,M200,M200,M200,M200,M200,M200,M200,M200,itmBank,M200,M200,M200,M200,M200,M200,itmBank",0,0,0,0,-1);
INSERT INTO active_users (user_nickname, user_id, user_game_id, user_grid, is_host, user_cash, user_pending_declaration, user_bank, deletion_time) VALUES ("testusr3",3,1,"M200,M200,M1000,M1000,M1000,M5000,M500,M500,M500,M200,M200,M200,M500,M200,M200,M200,M200,M200,M500,M200,M200,M200,M200,M200,M200,M200,M200,M200,itmBank,M200,M200,M200,M200,M200,M200,itmBank",0,0,0,0,-1);
SELECT * FROM active_users;

DELETE FROM active_games WHERE game_id > 0;
INSERT INTO active_games (game_id, host_id, grid_settings, game_items, current_round, square_order, round_remaining_actions, is_open, deletion_time, results_json) VALUES (1,1,'{"GRID_X":6,"GRID_Y":6}','{"M5000":1,"M1000":3,"M500":5,"M200":18,"M200":1,"M200":1,"M200":1,"M200":1,"M200":1,"itmBank":2,"M200":1,"M200":1}',0,"9,17,23,32,28,16,5,22,33,18,13,31,29,3,0,2,26,6,8,4,24,19,1,15,12,34,14,10,11,21,20,7,35,27,25,30",0,1,-1,'{"tuser1": 5000, "testifications2": 5587, "tuser2":4000, "test3": 2870, "test4": 2587, "test5": 3540, "test6": 1234, "WWWWWWWWWWWWWWW": 5343, "test8": 1750, "test9": 4300, "test10": 2900, "test11": 2800, "test12": 1750, "test13": 1700, "test14": 3900, "test15": 1500, "test16": 4700, "test17": 3500}');
SELECT * FROM active_games;