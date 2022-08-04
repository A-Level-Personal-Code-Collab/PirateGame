# Websocket API - Pirate Game

## Game
## `/wsapi/game/<game_id>` 
### Client
recv: spin(square: *string*) - Display spinner animation and pick square
recv: money_update(bank: *number*, cash: *number*) - Update displayed money values
recv: action_incoming({id: *string*, text: *string*}, perpetrator: *string*, target: *string*)
recv: log_update(text: *string*)

### Server
recv: spin() - Check auth -> rebroadcast
recv: declare() - Check auth -> send action_incoming()
recv: target(target: *string*) -> send action_incoming()
recv: retaliation(id: *string*) -> Check auth -> log_update() -> money_update()