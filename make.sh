rm Game ./src/*.o *.o

g++ -g -c ./src/*.cpp -I./include -L. -ltcod -ltcodxx
g++ -g *.o -o Game -L. -ltcod -ltcodxx

rm *.o
