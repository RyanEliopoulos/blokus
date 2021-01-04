A python 3 implementation of the classic game Blokus with local multiplayer support for 2-4 players.


<b> Setup </b> <br>
Execute main.py. <br> 
Then select the number of players as prompted.  This only impacts the scoring methodology as described in the rules.
<br><br>


<b> Play </b> <br>
The current player is denoted by the turn indicator in the top-center of the screen. <br>
The "End Game" button scores the game and announces the winner.  <br>
The "Skip Turn" allows gameplay to continue in the event a player determines they have no valid move to make.
<br><br>

<b> Rules </b>

This implementation adheres to the rules described in docs/blokus_instructions with two exceptions: <br>
1: Scoring methodology is always "basic". "Advanced" scoring is not currently supported. <br>
2: In 3-player games green is always considered the shared color for scoring purposes. Their points are discarded.



