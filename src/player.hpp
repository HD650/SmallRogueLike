#ifndef PLAYER_H
#define PLAYER_H

#include "actor.hpp"
#include "engine.hpp"
#include <string>

using namespace std;
class Actor;

class Player:public Actor
{
public:
	Player(int x, int y, int ch, string name, const TCODColor& col, int ack, int hp):Actor(x,y,ch,col)
	{
		this->name=name;
		this->ack=ack;
		this->hp=hp;
	}
	virtual void update();
	void takeDamage(int dam);
	void attack(int x, int y);
	bool isRemove();


private:
	string name;
	int hp;
	int ack;
};


#endif