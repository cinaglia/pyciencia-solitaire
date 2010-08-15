#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct carta {
        int numero, naipe;
        struct carta *proximaCarta;
} carta;

typedef struct deck {
        struct carta *topo;
} deck;

void inicializa(deck *pilha){
        pilha->topo = NULL;
}

void adiciona_carta(deck *pilha, int numero, int naipe){
        carta *novaCarta=(carta *)malloc(sizeof(carta));
        novaCarta->numero = numero;
        novaCarta->naipe = naipe;
        novaCarta->proximaCarta = pilha->topo;
        pilha->topo = novaCarta;
}
         

void remove_carta(deck *pilha){
        if(pilha->topo == NULL)
                printf("Pilha Vazia");
        else {
                carta *aux;
                aux = pilha->topo;
                pilha->topo = aux->proximaCarta;
                free(aux);
        }
}

int quantidade_cartas(deck *pilha){
    int contador = 0;
    carta *end = pilha->topo;
    while (end) {
        contador++;
        end = end->proximaCarta;
    }
    return contador;
}

// Criando as 13 pilhas necessarias para o jogo
deck decks[14];

// Inicializa as pilhas
static PyObject* py_inicializaDecks(PyObject* self, PyObject* args)
{
        int i = 0;
        for (; i < 14; i++)
                inicializa(&decks[i]);
                
	return Py_BuildValue("i", 1);
}

static PyObject* py_adicionaCarta(PyObject* self, PyObject* args)
{
        int numero_deck, numero_carta, numero_naipe;
        
        if (!PyArg_ParseTuple(args, "iii", &numero_deck, &numero_carta, &numero_naipe)) return NULL;
        
        adiciona_carta(&decks[numero_deck], numero_carta, numero_naipe);
        
	    return Py_BuildValue("iii", numero_deck, numero_carta, numero_naipe);
}

static PyObject* py_removeCarta(PyObject* self, PyObject* args)
{
        int numero_deck;
        
        if (!PyArg_ParseTuple(args, "i", &numero_deck)) return NULL;

        remove_carta(&decks[numero_deck]);

	    return Py_BuildValue("i", numero_deck);
}

static PyObject* py_listaCartas(PyObject* self, PyObject* args)
{
        char buffer[300];
        strcpy(buffer, "");
        
        deck *meu_deck = &decks[6];
        carta *carta_atual = meu_deck->topo;
        
        while (carta_atual->proximaCarta) {
            char tmp[10]; 
            
            strcat(buffer, "(");
            sprintf(tmp, "%d", carta_atual->numero);
            strcat(buffer, tmp);
            strcat(buffer, ", ");
            
            sprintf(tmp, "%d", carta_atual->naipe);
            strcat(buffer, tmp);
            strcat(buffer, ")");
            strcat(buffer, "\n");
            
            carta_atual = carta_atual->proximaCarta;
        }
        
	    return Py_BuildValue("s", buffer);
}


//Junta as funcoes do Python com as funcoes em C
static PyMethodDef estruturas_methods[] = {
	{"inicializaDecks", py_inicializaDecks, METH_VARARGS},
	{"adicionaCarta", py_adicionaCarta, METH_VARARGS},
	{"removeCarta", py_removeCarta, METH_VARARGS},
	{"listaCartas", py_listaCartas, METH_VARARGS},
	{NULL, NULL}
};

// O python chama esta funcao para inicializar o modulo
void initestruturas()
{
	(void) Py_InitModule("estruturas", estruturas_methods);
}