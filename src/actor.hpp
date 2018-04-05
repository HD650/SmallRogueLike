#ifndef ACTOR_H
#define ACTOR_H

#include "libtcod.hpp"

class Actor
{
public:
	Actor(int x, int y, int ch, const TCODColor& col);
	void render() const;
	virtual void update();
	virtual void takeDamage(int dam)
	{

	}
	virtual int giveDamage()
	{
		return 0;
	}
	virtual bool isRemove()
	{
		return false;
	}
	int x,y;
	int ch;
	int maxRadius=15;
	TCODColor col;
};

#endif