#ifndef ENGINE_H
#define ENGINE_H

#include "libtcod.hpp"
#include "player.hpp"
#include "map.hpp"
#include <vector>

using namespace std;

class Actor;
class Map;

class Engine
{
public:
	Actor* player;
	vector<Actor*> actors;
	Map* map;

	Engine();
	~Engine();
	void update();
	void render();
};

extern Engine engine;

#endif