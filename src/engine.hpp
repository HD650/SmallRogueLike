#ifndef ENGINE_H
#define ENGINE_H

#include "project.hpp"
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