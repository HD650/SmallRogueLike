#include "engine.hpp"

Engine::Engine()
{
  TCODConsole::initRoot(160,90,"test",false);
  player = new Player(40,25,'@',"player",TCODColor::white,100,100);
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
  for(auto i=actors.begin();i!=actors.end();i++)
  {
    (*i)->update();
    if((*i)->isRemove())
    {
      delete (*i);
      i=actors.erase(i);
    }
  }
  map->computeFov();
}

void Engine::render()
{
  TCODConsole::root->clear();
  for(auto i=actors.begin();i!=actors.end();i++)
  {
    if(this->map->isInFov((*i)->x,(*i)->y))
      (*i)->render();
  }
  map->render();
}