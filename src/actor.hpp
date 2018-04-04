#ifndef ACTOR_H
#define ACTOR_H

#include "project.hpp"

class Actor
{
public:
	Actor(int x, int y, int ch, const TCODColor& col);
	void render() const;
	int x,y;
	int ch;
	int maxRadius=15;
	TCODColor col;
};

#endif