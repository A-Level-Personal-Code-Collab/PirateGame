# REST API - Pirate Game

## Statistics
`GET /api/stats/`
**RESPONSE:** {<stat_name>: <stat_value>}
Returns JSON containing all statistics stored in database

`GET /api/stats/<stat_name>`
**RESPONSE:** {"stat_value": <stat_value>}
Returns JSON containing only a single statistics with key 'stat_value'

## Game Modifier
- Create game from settings
`POST /api/game/create` <- { game_title, ?game_settings }
**RESPONSE:** { game_id: *string*, game_settings *JSON*, game_is_open *boolean*, game_current_round *number*, game_title: *string* }

- Return Game Information
`GET /api/game/<game_id>`
**RESPONSE:** { game_id: *string*, game_settings *JSON*, game_is_open *boolean*, game_current_round *number*, game_title: *string* }

- Return Game Results
`GET /api/game/<game_id>/results`
**RESPONSE:** { game_title: *string*, game_results: [*JSON*] }

## User Modifier
- Create new user
`POST /api/user/new` <- { user_nickname: *string*, user_game_id: *string*, ?user_grid: [*string*], ?user_is_host: *boolean*, ?participation: *boolean* }
**RESPONSE:** { user_id: *string*, user_nickname: *string*, user_game_id: *string*, user_is_host: *boolean*, user_money: *number*, user_retaliations: [*string*], user_grid: [*string*], participation: *boolean* }

- Modify user
`PUT /api/user/<user_id>` <- { ?user_nickname: *string*, ?user_game_id: *string*, ?user_grid: [*string*], ?user_is_host: *boolean*, ?participation: *boolean* }
**RESPONSE:** { user_id: *string*, user_nickname: *string*, user_game_id: *string*, user_is_host: *boolean*, user_money: *number*, user_retaliations: [*string*], user_grid: [*string*], participation: *boolean* }

- Get user
`GET /api/user/<user_id>`
**RESPONSE:** { user_id: *string*, user_nickname: *string*, user_game_id: *string*, user_is_host: *boolean*, user_money: *number*, user_retaliations: [*string*], user_grid: [*string*], participation: *boolean* }

- Pre-validate new user without committing to database
`POST /api/user/preval` <- { user_nickname, user_game_id, ?user_grid, ?user_is_host, ?participation: *boolean* }
**RESPONSE:** { valid: *boolean* }
