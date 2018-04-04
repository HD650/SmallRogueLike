rm Game ./src/*.o *.o

g++ -c ./src/*.cpp -I./include -L. -ltcod -ltcodxx
g++ *.o -o Game -L. -ltcod -ltcodxx

rm *.o
