#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct node {
  struct node *prev;
  struct node *next;
  uint64_t val;
} node;

node *append(node *n, uint64_t v)
{
  node *newnode = (node *)malloc(sizeof(node));

  newnode->val = v;
  newnode->prev = n;
  newnode->next = n->next;
  n->next->prev = newnode;
  n->next = newnode;

  return newnode;
}

/* returns a node to the right */
node *delete(node *n)
{
  node *ret = n->next;
  n->prev->next = n->next;
  n->next->prev = n->prev;
  free(n);
  return ret;
}

int main(int argc, char *argv[]) {
  int players, lmarble, n;
  node *root, *curr;
  uint64_t *scores;

  if (argc < 3) {
    fprintf(stderr, "usage: %s nplayers lastMarble\n", argv[0]);
    return EXIT_FAILURE;
  }
  players = atoi(argv[1]);
  lmarble = atoi(argv[2]);
  fprintf(stderr, "players %d marbles %d\n", players, lmarble);

  n = 0;
  scores = (uint64_t *)calloc(players, sizeof(uint64_t));
  root = (node *)malloc(sizeof(node));
  root->prev = root;
  root->next = root;
  root->val = 0;
  curr = root;

  while (n < lmarble) {
    for (int p = 0; p < players; p++) {
      if (n >= lmarble) {
	break;
      }
      n += 1;
      if (n % 23) {
	curr = append(curr->next, n);
      } else {
	for (int i = 0; i < 7; i++) {
	  curr = curr->prev;
	}
	scores[p] += (n + curr->val);
	curr = delete(curr);
      }
    }
  }

  uint64_t maxscore = 0;
  int maxplayer = 0;
  for (int p = 0; p < players; p++) {
    if (scores[p] > maxscore) {
      maxscore = scores[p];
      maxplayer = p;
    }
  }

  fprintf(stdout, "%ld\n", maxscore);

  free(scores);
  curr = root;
  root->prev->next = NULL;
  while (curr) {
    node *tmp = curr->next;
    free(curr);
    curr = tmp;
  }
  return EXIT_SUCCESS;
}
