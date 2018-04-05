#ifndef MAP_H
#define MAP_H

#include "engine.hpp"
#include "monster.hpp"

#define ROOM_MAX_SIZE 24
#define ROOM_MIN_SIZE 12
#define MAX_MONSTER 3


struct Tile
{
	bool Wall;
	bool Tran;
	bool explored;

	Tile():Wall(true),Tran(false),explored(false){};
};

class Map
{
public:
	Map(int w, int h);
	bool isWall(int x, int y)const;
	bool isTran(int x, int y)const;
	void setProperties(int x, int y, bool wall, bool tran);
	bool isInFov(int x, int y)const;
	bool isExplored(int x, int y)const;
	void computeFov();
	bool canWalk(int x, int y);
	void addMonster(int x, int y);
	~Map();
	int w,h;
	void render()const;
protected:
	friend class BspListener;
	Tile* tiles;
	TCODMap * map;

	void dig(int x1, int y1, int x2, int y2);
	void createRoom(bool first, int x1, int y1, int x2, int y2);
};

class BspListener:public ITCODBspCallback
{
public:
	BspListener(Map &map):map(map),roomNum(0)
	{

	}
	bool visitNode(TCODBsp* node,void* userData)
	{
		if(node->isLeaf())
		{
			//if its the leaf node of the bsp tree, dig a room
			int x,y,w,h;
			TCODRandom *rng=TCODRandom::getInstance();
			w=rng->getInt(ROOM_MIN_SIZE,node->w-2);
			h=rng->getInt(ROOM_MIN_SIZE,node->h-2);
			x=rng->getInt(node->x+1,node->x+node->w-w-1);
			y=rng->getInt(node->y+1,node->y+node->h-h-1);
			map.createRoom(this->roomNum==0,x,y,x+w-1,y+h-1);

			//if its not the first room, connect this room to last room
			if(this->roomNum!=0)
			{
				map.dig(this->lastx,this->lasty,x+w/2,this->lasty);
				map.dig(x+w/2,this->lasty,x+w/2,y+h/2);
			}

			this->lastx=x+w/2;
			this->lasty=y+h/2;
			this->roomNum++;
		}
		return true;
	}
private:
	Map &map;
	int roomNum;
	int lastx,lasty;
};

#endif