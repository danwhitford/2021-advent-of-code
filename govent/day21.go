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

func pop(stack *[]gameState) (gameState) {	
	l := len(*stack) - 1
	ret := (*stack)[l]
	*stack = (*stack)[:l]
	return ret
}

func move(game gameState, cache *map[gameState]gameState) gameState {
	ret, prs := (*cache)[game]
	if prs {
		return ret
	}

	old_game := gameState{game.p1_pos, game.p1_score, game.p2_pos, game.p2_score, game.next_player, game.next_roll}
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

	(*cache)[old_game] = game
	return game
}

func main() {
	stack := []gameState{}
	cache := make(map[gameState]gameState)
	for _, roll := range rolls() {
		stack = append(stack, gameState{4, 8, 0, 0, 1, roll})
	}
	wins := make(map[string]int)
	wins["p1"] = 0
	wins["p2"] = 0

	var game gameState
	counter := 0
	for len(stack) > 0 {
		if counter > 10000000 {
			fmt.Println(wins, len(stack))
			counter = 0
		}
		counter++
		game = pop(&stack)

		game = move(game, &cache)
		if game.p1_score >= 21 {
			wins["p1"]++
			continue
		}
		for _, roll := range rolls() {
			stack = append(stack, gameState{game.p1_pos, game.p2_pos, game.p1_score, game.p2_score, game.next_player, roll})
		}

		game = move(game, &cache)
		if game.p2_score >= 21 {
			wins["p2"]++
			continue
		}
		for _, roll := range rolls() {
			stack = append(stack, gameState{game.p1_pos, game.p2_pos, game.p1_score, game.p2_score, game.next_player, roll})
		}
	}
	fmt.Println(wins)
}
