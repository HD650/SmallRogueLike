#ifndef MONSTER_H
#define MONSTER_H

#include "actor.hpp"
#include <string>

using namespace std;
class Actor;

class Monster:public Actor
{
public:
	Monster(int x, int y, int ch, string name, const TCODColor& col, int ack, int hp):Actor(x,y,ch,col)
	{
		this->hp=hp;
		this->ack=ack;
		this->name=name;
	}
	virtual void update();
	int giveDamage();
	void takeDamage(int damage);
	virtual bool isRemove();
private:
	int hp;
	int ack;
	string name;
	void AI();
};


#endif