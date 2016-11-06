/**
 ** @author rafcolm_
 ** compilation: g++ connGs.cpp -o connGs
 ** See description from main below.
 **/
#include<iostream>
#include <string.h> 
#include <ctype.h>
#include <stdlib.h>     /* atoi */
#include <queue>

using namespace std;
int VERTICES;  
int EDGES;
int **MAIN_GRAPH;
int **DISTANCE_MATRIX;
bool CONNECTED = true;  //determines if MAIN_GRAPH is a connected G

/**
 ** Deallocates memory from any new Graph (2d array) referenced by pointer **G
 ** @params:
 **   - G: pointer for Graph (2d array)to deallocate
 **   - vs: # of vertices of G
 **/
void deleteG(int **G, int vs){
  for (int i = 0; i < vs; i++){  
    delete [] G[i];
  }
  delete [] G;
  G = 0; //set pointer NULL
}

/**
 ** Prints Graph (2d array) referenced by pointer **G
 ** @params:
 **   - G_name: string name for G
 **   - G: pointer for Graph (2d array)to print
 **   - vs: # of vertices of G
 **/
void printG(string G_name, int** G, int vs){
  cout << "  "  << G_name << " = " << endl;
  for(int i = 0; i < vs; i++){
    cout << "    ";
    for(int j = 0; j < vs; j++){
      cout << G[i][j] << " ";
    }
    cout << endl;
  }
  cout << endl;
}

/**
 ** Generates an adjacency matrix based on the structure defined by input string pointed by infoG, and references it with global pointer MAIN_GRAPH
 ** @params:
 **   - infoG: validly formatted string with structure info for adjacency matrix.  See main function description for details on format.
 **/
void generateAdjMatrix(char *infoG[]){
  MAIN_GRAPH = new int*[VERTICES]; //allocates 2d array
  for(int i = 0; i<VERTICES; i++){
    MAIN_GRAPH[i] = new int[VERTICES];
  }
  int j = 2;
  while(strcmp(infoG[j], "-1") != 0){ //populates MAIN_GRAPH with edges
    MAIN_GRAPH[atoi(infoG[j])][atoi(infoG[j+1])] = 1;
    MAIN_GRAPH[atoi(infoG[j+1])][atoi(infoG[j])] = 1;
    j+=2;
  }
}

/**
 ** Performs BFS (breadth-first-search) onto global adjacency matrix (MAIN_GRAPH) starting from vertex v, in order to compute the distances from v to all its connected vertices.  Stores all distances in the v-th row of the global distance matrix (DISTANCE_MATRIX).
 ** @params:
 **   - G: pointer for Graph (2d array)to print
 **   - vs: # of vertices of G
 **/
void BFS(int** G, int v){
  queue<int> q; //queue to store connected vertices in order of visit
  q.push(v);
  int d = 1; //initial distance 
  int currentV = 0;
  while(!q.empty()){
    currentV = q.front();
    q.pop();
    for(int i = 0; i<VERTICES; i++){
      //last conditional happens if currentV NOT_IN visited
      if(v!=i && MAIN_GRAPH[currentV][i] == 1 && (DISTANCE_MATRIX[v][i] == 0 || DISTANCE_MATRIX[v][i] > d)){ 
	q.push(i);
	//assigns current calculated distance to found vertex
	DISTANCE_MATRIX[v][i] = d;
	DISTANCE_MATRIX[i][v] = d;	
      }
    }
    d++;
  }
}

/**
 **Generates a distance matrix based on adjancecy matrix G, and references it with global pointer DISTANCE_GRAPH.  To calculate distances, performs BFS on every vertex of G.  Lastly, if unconnected vertices (vertices with distance 0 in between each other) are found, assigns distance -1 in between each unconnected vertex, and sets global CONNECTED to false .
 ** @params:
 **   - G: pointer for Graph (2d array)to print
 **/
void DistanceMatrix(int **G){
  DISTANCE_MATRIX = new int*[VERTICES]; //allocates array
  for(int i = 0; i < VERTICES; i++){
    DISTANCE_MATRIX[i] = new int[VERTICES];
  }
  for(int j = 0; j<VERTICES; j++){ //BFS on every row/vertex
    BFS(G, j);
  }
  //if unconnected vertex is found, CONNECTED=false & vexter_distance=-1
  for(int k = 0; k < VERTICES; k++){ 
    for(int l = 0; l < VERTICES; l++){
      if(k!=l && DISTANCE_MATRIX[k][l] == 0){
	CONNECTED = false;
	DISTANCE_MATRIX[k][l] = -1;
      }
    }
  }
}

/**
 **Generates distance matrix for G by calling DistanceMatrix and references it with global pointer DISTANCE_MATRIX.  Returns length of longest tree iff G is connected; -1, otherwise. 
 ** @params:
 **   - G: pointer for Graph (2d array)to print
 **/
int Diameter(int **G){
  DistanceMatrix(G);
  int max = -1;
  if (CONNECTED){
    for(int i = 0; i < VERTICES; i++){
      for(int j = 0; j < VERTICES; j++){
	if(max < DISTANCE_MATRIX[i][j]){
	  max = DISTANCE_MATRIX[i][j];
	}
      }
    }
  }
  return max;
}

/**
 **Main function:
 **Checks if user input is valid; terminates if input is not valid (see input format below for details).  Generates main adjancecy matrix by using function generateAdjMatrix().  Calculates diameter of distance matrix of the main adjacency matrix by using function Diameter(), and prints it iff main adjacency matrix is connected.  Deallocates all memory from matrix created by using function deleteG().
 **
 ** User input must follow the following format:
 **      *argc must be even & greater than 2
 **      *argv[2] = # of vertices
 **      *argv[3:last-1] = every 2 elements defines an edge; size of sub-stream must be even 
 **      *argv[last] == -1
 **/
int main(int argc, char **argv){
  //checks user for valid input
  if (argc%2 == 0 || argc <= 3 || strcmp(argv[argc-1], "-1") != 0){
    cout << "ERROR: Invalid input!\n   *number of input must be even & greater than 2\n   *last input value must be -1\n\n" << endl;
    return 1;
  }
  for(int i = 2; i < argc-1; i++){
    if(!std::isdigit(*argv[i]) || atoi(argv[1]) <= atoi(argv[i])){
      cout << "ERROR: Invalid input!\n   *edges only correspond to vertices from [0, number_of_vertices]\n\n" << endl;
      return 2;
    }
  }
  cout << "OK! You entered:" << endl;
  VERTICES = atoi(argv[1]);
  EDGES = (argc-3)/2;
  cout << "  * #vertices of G = " << VERTICES << endl;
  cout << "  * declared #edges of G = " << EDGES << endl << endl;
  cout << "Generating adjacency matrix of G..." << endl << endl;
  generateAdjMatrix(argv);
  printG("Adjacency Matrix", MAIN_GRAPH, VERTICES);
  cout << "Generating distance matrix of G..." << endl << endl;
  int diameter = Diameter(MAIN_GRAPH);
  printG("Distance Matrix", DISTANCE_MATRIX, VERTICES);
  if(CONNECTED){
    cout << "G is connected.  Diameter of G = " << diameter << endl;    
  } else {
    cout << "G is not connected!" << endl;
  }
  deleteG(MAIN_GRAPH, VERTICES);  //deallocates memory
  deleteG(DISTANCE_MATRIX, VERTICES);
  cout << "\nDone.\n\n";
  return 0;
}
