#include "engine.hpp"

Engine engine;
int main()
{
	while(!TCODConsole::isWindowClosed())
	{
		engine.update();
		engine.render();
		TCODConsole::flush();
	}
	return 0;
}