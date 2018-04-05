#include "player.hpp"

void Player::update()
{
	TCOD_key_t key;
	TCODSystem::checkForEvent(TCOD_EVENT_KEY_PRESS,&key,NULL);
	switch(key.vk) 
	{
		case TCODK_UP : 
		if (engine.map->canWalk(this->x,this->y-1)) 
		{
		   this->y--; 
		}
		else if(!engine.map->isWall(this->x,this->y-1))
		{
			attack(this->x,this->y-1);
		}
		break;
		case TCODK_DOWN : 
		if (engine.map->canWalk(this->x,this->y+1)) 
		{
		   this->y++;
		}
		else if(!engine.map->isWall(this->x,this->y+1))
		{
			attack(this->x,this->y+1);
		}
		break;
		case TCODK_LEFT : 
		if (engine.map->canWalk(this->x-1,this->y)) 
		{
		   this->x--;
		}
		else if(!engine.map->isWall(this->x-1,this->y))
		{
			attack(this->x-1,this->y);
		}
		break;
		case TCODK_RIGHT : 
		if (engine.map->canWalk(this->x+1,this->y)) 
		{
		   this->x++;
		}
		else if(!engine.map->isWall(this->x+1,this->y))
		{
			attack(this->x+1,this->y);
		}
		break;
		default:break;
	}
}

void Player::takeDamage(int dam)
{
	this->hp-=dam;
}

void Player::attack(int x, int y)
{
	for(auto i=engine.actors.begin();i!=engine.actors.end();i++)
	{
		if((*i)->x==x&&(*i)->y==y)
		{
			(*i)->takeDamage(this->ack);
			this->takeDamage((*i)->giveDamage());
		}
	}
}

bool Player::isRemove()
{
	if(this->hp<=0)
		return true;
	else
		return false;
}
