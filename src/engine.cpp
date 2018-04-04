#include "engine.hpp"

Engine::Engine()
{
	TCODConsole::initRoot(160,90,"test",false);
	player = new Actor(40,25,'@',TCODColor::white);
	actors.push_back(player);
	map = new Map(140,90);
}

Engine::~Engine() 
{
	for(auto i=actors.begin();i!=actors.end();i++)
	{
		delete (*i);
	}
	delete map;
}

void Engine::update() 
{
   TCOD_key_t key;
   TCODSystem::checkForEvent(TCOD_EVENT_KEY_PRESS,&key,NULL);
   switch(key.vk) {
       case TCODK_UP : 
           if (!map->isWall(player->x,player->y-1)) 
           {
               player->y--;   
           }
       break;
       case TCODK_DOWN : 
           if (!map->isWall(player->x,player->y+1)) 
           {
               player->y++;
           }
       break;
       case TCODK_LEFT : 
           if (!map->isWall(player->x-1,player->y)) 
           {
               player->x--;
           }
       break;
       case TCODK_RIGHT : 
           if (!map->isWall(player->x+1,player->y)) 
           {
               player->x++;
           }
       break;
       default:break;
   }
   map->computeFov();
}

void Engine::render()
{
	TCODConsole::root->clear();
	for(auto i=actors.begin();i!=actors.end();i++)
	{
		(*i)->render();
	}
	map->render();
}