package main

import (
	"fmt"
	"strings"
	"strconv"
	"os"
)

type Cube struct {
	x int
	y int
	z int
}

type Reactor struct {
	on_cubes map[Cube]struct{}
}

func (reactor *Reactor) turn_on_cuboid(xmin, xmax, ymin, ymax, zmin, zmax int) {
	for x := xmin; x <= xmax; x++ {
		for y := ymin; y <= ymax; y++ {
			for z := zmin; z <= zmax; z++ {
				reactor.on_cubes[Cube{x, y, z}] = struct{}{}
			}
		}
	}
}

func (reactor *Reactor) turn_off_cuboid(xmin, xmax, ymin, ymax, zmin, zmax int) {
	for x := xmin; x <= xmax; x++ {
		for y := ymin; y <= ymax; y++ {
			for z := zmin; z <= zmax; z++ {
				delete(reactor.on_cubes, Cube{x, y, z})
			}
		}
	}
}

type Instruction struct {
	on bool
	cuboid []int
}

func (reactor *Reactor) central_reboot(instructions []Instruction) {
	for _, instruction := range instructions {
		xmin := instruction.cuboid[0]
		xmax := instruction.cuboid[1]
		ymin := instruction.cuboid[2]
		ymax := instruction.cuboid[3]
		zmin := instruction.cuboid[4]
		zmax := instruction.cuboid[5]
		if xmin < -50 || xmax > 50 || ymin < -50 || ymax > 50 || zmin < -50 || zmax > 50{
			continue
		}
		if instruction.on {
			reactor.turn_on_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
		} else {
			reactor.turn_off_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
		}
	}
}

func (reactor *Reactor) full_reboot(instructions []Instruction) {
	for _, instruction := range instructions {
		fmt.Println(instruction)

		xmin := instruction.cuboid[0]
		xmax := instruction.cuboid[1]
		ymin := instruction.cuboid[2]
		ymax := instruction.cuboid[3]
		zmin := instruction.cuboid[4]
		zmax := instruction.cuboid[5]
		if instruction.on {
			reactor.turn_on_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
		} else {
			reactor.turn_off_cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
		}
	}
}

func parse_input(source string) []Instruction {
	instructions := []Instruction{}
	for _, line := range strings.Split(source, "\n") {
		coords := []int{}
		l := strings.Split(line, " ")
		state := l[0] == "on"
		for _, coord := range strings.Split(l[1], ",") {
			coord_mini := strings.Split(coord[2:], "..")
			mi, _ := strconv.Atoi(coord_mini[0])
			ma, _ := strconv.Atoi(coord_mini[1])
			coords = append(coords, mi)
			coords = append(coords, ma)
		}
		instructions = append(instructions, Instruction{state, coords})
	}
	return instructions
}

func main() {
	dat, _ := os.ReadFile("day22/day22")
	s := string(dat)
	// s := "on x=10..12,y=10..12,z=10..12"

	instructions := parse_input(s)

	reactor := Reactor{make(map[Cube]struct{})}
	reactor.full_reboot(instructions)
	fmt.Println(len(reactor.on_cubes))
}