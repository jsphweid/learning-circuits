#include <SDL2/SDL.h>
#include <cstdint>
#include <fstream>
#include <bitset>
#include <verilated.h>
#include "Vmy_computer.h"
#include "Vmy_computer_my_computer.h"
#include "Vmy_computer_my_rom_32k.h"
#include "Vmy_computer_my_screen.h"
#include "Vmy_computer_my_memory.h"
#include <iostream>

using namespace std;

SDL_Renderer *renderer;
Vmy_computer *top;

void step()
{
  top->clk = 0;
  top->eval();
  top->clk = 1;
  top->eval();
}

int handleInput()
{
  SDL_Event event;
  while (SDL_PollEvent(&event))
  {
    switch (event.type)
    {
    case SDL_QUIT:
      return -1;
    case SDL_KEYDOWN:
      if (event.key.keysym.sym == SDLK_ESCAPE)
        return -2;
      if (event.key.keysym.sym == SDLK_LEFT)
        top->my_computer->ram->scancode = 130;
      else if (event.key.keysym.sym == SDLK_RIGHT)
        top->my_computer->ram->scancode = 132;
      else
        top->my_computer->ram->scancode = event.key.keysym.sym;
      break;
    case SDL_KEYUP:
      top->my_computer->ram->scancode = 0;
      break;
    }
  }
  return 0;
}

void initVideo()
{
  SDL_Init(SDL_INIT_VIDEO);
  SDL_Window *window = SDL_CreateWindow("N2T Computer - SDL", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 640, 480, 0);
  renderer = SDL_CreateRenderer(window, -1, 0);
}

void drawScreen()
{
  uint16_t *smem = top->my_computer->ram->screen->memory;
  for (int y = 0; y < 256; y++)
  {
    uint16_t *row = &smem[y << 5];
    int x = 0;
    for (int i = 0; i < 32; i++)
    {
      int xib = 1;
      for (int xi = 0; xi < 16; xi++)
      {
        if (row[x >> 4] & xib)
          SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
        else
          SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderDrawPoint(renderer, x, y);
        x++;
        xib = xib << 1;
      }
    }
  }
}

void draw()
{
  SDL_SetRenderDrawColor(renderer, 100, 100, 100, 255);
  SDL_RenderClear(renderer);

  drawScreen();

  SDL_RenderPresent(renderer);
}

int main(int argc, char *args[])
{
  top = new Vmy_computer;
  ifstream rom("fill.hack");
  // ifstream rom("pong.hack");
  assert(rom);

  string line;
  uint16_t *mem = (uint16_t *)top->my_computer->rom->memory;
  int i;
  for (i = 0;; i++)
  {
    rom >> line;
    if (!rom)
      break;
    uint16_t v = bitset<16>(line).to_ulong();
    mem[i] = v;
  }
  assert(i);

  top->reset = 1;
  top->clk = 0;
  top->eval();
  top->reset = 0;
  top->clk = 1;
  top->eval();

  initVideo();

  do
  {
    for (int c = 0; c < 100000; c++)
      step();
    draw();
  } while (handleInput() >= 0);

  return 0;
}
