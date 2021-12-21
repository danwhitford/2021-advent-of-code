package main

import (
	"fmt"
)

func rolls() [][3]int {
	return [][3]int{
		{1, 1, 1}, 
		{1, 1, 2}, 
		{1, 1, 3}, 
		{1, 2, 1}, 
		{1, 2, 2}, 
		{1, 2, 3}, 
		{1, 3, 1}, 
		{1, 3, 2}, 
		{1, 3, 3}, 
		{2, 1, 1}, 
		{2, 1, 2}, 
		{2, 1, 3}, 
		{2, 2, 1}, 
		{2, 2, 2}, 
		{2, 2, 3}, 
		{2, 3, 1}, 
		{2, 3, 2}, 
		{2, 3, 3}, 
		{3, 1, 1}, 
		{3, 1, 2}, 
		{3, 1, 3}, 
		{3, 2, 1}, 
		{3, 2, 2}, 
		{3, 2, 3}, 
		{3, 3, 1}, 
		{3, 3, 2}, 
		{3, 3, 3},
	}
}

type gameState struct{
	p1_pos int
	p2_pos int
	p1_score int
	p2_score int
	next_player int
	next_roll [3]int
}

func move(game gameState) gameState {
	points := 0
	for _, v := range game.next_roll {
		points += v
	}
	if game.next_player == 1 {
		game.p1_pos += points
		if game.p1_pos > 10 {
			game.p1_pos = (game.p1_pos - 1) % 10 + 1
		}
		game.p1_score += game.p1_pos
	} else {
		game.p2_pos += points
		if game.p2_pos > 10 {
			game.p2_pos = (game.p2_pos - 1) % 10 + 1
		}
		game.p2_score += game.p2_pos
	}
	if game.next_player == 1 {
		game.next_player = 2
	} else {
		game.next_player = 1
	}

	return game
}

func main() {
	// stack := []gameState{}
	universes := make(map[gameState]int)
	for _, roll := range rolls() {
		universes[gameState{8, 2, 0, 0, 1, roll}] = 1
	}
	wins := make(map[string]int)
	wins["p1"] = 0
	wins["p2"] = 0

	for len(universes) > 0 {
		fmt.Println(wins, len(universes))

		for universe, count := range universes {
			delete(universes, universe)
			
			next_universe := move(universe)
			
			if next_universe.p1_score >= 21 {
				wins["p1"] += count
				continue
			}			
			if next_universe.p2_score >= 21 {
				wins["p2"] += count
				continue
			}

			for _, roll := range rolls() {
				game := gameState{next_universe.p1_pos, next_universe.p2_pos, next_universe.p1_score, next_universe.p2_score, next_universe.next_player, roll}
				_, prs := universes[game]
				if prs {
					universes[game] += count
				} else {
					universes[game] = count
				}
			}
		}
	}
	fmt.Println(wins["p1"])
	fmt.Println(wins["p2"])
}
