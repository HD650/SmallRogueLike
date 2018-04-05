#include "map.hpp"

Map::Map(int w, int h)
{
	this->w=w;
	this->h=h;
	this->tiles=new Tile[w*h];
	map=new TCODMap(w,h);
	map->clear(false,false);

	TCODBsp bsp(0,0,w,h);
	bsp.splitRecursive(NULL,8,ROOM_MIN_SIZE,ROOM_MIN_SIZE,1.5f,1.5f);
	BspListener listener(*this);
	bsp.traverseInvertedLevelOrder(&listener,NULL);
}

Map::~Map()
{
	delete [] this->tiles;
	delete map;
}

void Map::setProperties(int x, int y, bool wall, bool tran)
{
	this->map->setProperties(x,y,tran,!wall);
}

bool Map::isWall(int x, int y) const
{
	return !this->map->isWalkable(x,y);
}

bool Map::isTran(int x, int y) const
{
	return this->tiles[x+y*this->w].Tran;
}

bool Map::isExplored(int x, int y)const
{
	return this->tiles[x+y*this->w].explored;
}

bool Map::isInFov(int x, int y)const
{
	if(map->isInFov(x,y))
	{
		tiles[x+y*w].explored=true;
		return true;
	}
	return false;
}

bool Map::canWalk(int x, int y)
{
	if(isWall(x,y))
		return false;
	for(auto i=engine.actors.begin();i!=engine.actors.end();i++)
	{
		if((*i)->x==x&&(*i)->y==y)
		{
			return false;
		}
	}
	return true;
}

void Map::render() const
{
	static const TCODColor darkWall(0,0,100);
	static const TCODColor darkGround(50,50,150);
	static const TCODColor lightWall(130,110,50);
	static const TCODColor lightGround(200,180,50);

	for(int y=0;y<h;y++)
	{
		for(int x=0;x<w;x++)
		{
			if(isInFov(x,y))
			{
				TCODConsole::root->setCharBackground(x,y,isWall(x,y)?lightWall:lightGround);
			}
			else if(isExplored(x,y))
			{
				TCODConsole::root->setCharBackground(x,y,isWall(x,y)?darkWall:darkGround);
			}
		}
	}
}

void Map::dig(int x1, int y1, int x2, int y2) 
{
	if(x2<x1) 
	{
		int tmp=x2;
		x2=x1;
		x1=tmp;
	}
	if(y2<y1) 
	{
		int tmp=y2;
		y2=y1;
		y1=tmp;
	}
	for(int tilex=x1;tilex<=x2;tilex++)
	{
		for(int tiley=y1;tiley<=y2;tiley++) 
		{
			setProperties(tilex,tiley,false,true);
		}
	}
}

void Map::computeFov()
{
	map->computeFov(engine.player->x,engine.player->y,engine.player->maxRadius);
}

void Map::addMonster(int x, int y)
{
	engine.actors.push_back(new Monster(x,y,'o',"orc",TCODColor::desaturatedGreen,2,10));
}

void Map::createRoom(bool first, int x1, int y1, int x2, int y2)
{
	dig(x1,y1,x2,y2);
	if(first)
	{
		engine.player->x=(x1+x2)/2;
		engine.player->y=(y1+y2)/2;
	}
	else
	{
		TCODRandom* random=TCODRandom::getInstance();
		int num_monster=random->getInt(0,MAX_MONSTER);
		for(int i=0;i<num_monster;i++)
		{
			int x=random->getInt(x1,x2);
			int y=random->getInt(y1,y2);
			if(canWalk(x,y))
			{
				addMonster(x,y);
			}
		}
	}
}
