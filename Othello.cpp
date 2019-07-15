#include "pch.h"
#include <iostream>
#include <string>
#include <map>
#include <array>
#include <utility>

using namespace std;

string operator*(string const &str, size_t n)
{
	string result;
	result.reserve(n * str.size());
	for (size_t i = 0; i < n; i++)
		result += str;
	return result;
}

struct gameStruct{
	string player1;
	string player2;
	int who;
	//int board[8][8];
	array<array<int, 8>, 8> board;
};


//Returns a new instance of the game dictionary, with names of player 1 and 2 as arguments, and the standard Othello starting board.
gameStruct newGame(string player1, string player2)
{
	gameStruct game;
	game.player1 = player1;
	game.player2 = player2;
	game.who = 1;
	game.board = {{	{0,0,0,0,0,0,0,0},
					{0,0,0,0,0,0,0,0},
					{0,0,0,0,0,0,0,0},
					{0,0,0,2,1,0,0,0},
					{0,0,0,1,2,0,0,0},
					{0,0,0,0,0,0,0,0},
					{0,0,0,0,0,0,0,0},
					{0,0,0,0,0,0,0,0}}};

	return game;
}	


//Prints the Othello game board with boundaries and row/column names, and the positions of players 1 and 2 as X and O respectively.
void printBoard(array<array<int, 8>, 8> board)
{
	char cellEval[3] = {' ', 'X', 'O'};
	string divLine = " +" + (string("-+") * 8);
	
	cout << " |a|b|c|d|e|f|g|h|" << endl;
	cout << divLine << endl;
	for (int row = 0; row <= 7; row++) {
		cout << to_string(row + 1) + '|';
		for (int col = 0; col <= 7; col++) {
			cout << cellEval[board[row][col]] << '|';
		}
		cout << endl;
	}
	cout << divLine << endl;
}


//Converts a string describing a position on the board such as C4 to its tuple equivalent.
int strToIndex(string s)
{
	transform(s.begin(), s.end(), s.begin(), tolower);
}


// Outputs the game greeting message, asks for player names, and prompts move inputs until the end of the game.
void play()
{
	string starLine(65, '*');

	cout << starLine << endl;
	cout << "***" << string(8, ' ') << "WELCOME TO DMITRII'S FABULOUS OTHELLO GAME!" << string(8, ' ') << "***" << endl;
	cout << starLine << endl;

	gameStruct game = newGame("A", "B");
	printBoard(game.board);

}


int main()
{
	play();
	return 0;
}
