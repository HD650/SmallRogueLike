#include "monster.hpp"

#define CHASE 1
#define IDLE 2


void Monster::update()
{

}

int Monster::giveDamage()
{
	return this->ack;
}

void Monster::takeDamage(int dam)
{
	this->hp-=dam;
}

bool Monster::isRemove()
{
	if(this->hp<0)
		return true;
	else
		return false;
}

void Monster::AI()
{
	
}