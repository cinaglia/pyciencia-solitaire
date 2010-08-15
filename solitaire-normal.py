# -*- coding: utf-8 -*-
import os, sys
import pygame
from pygame.locals import *

# Função que carrega as imagens
def load_image(name):
    fullname = os.path.join('images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    # print "%s, (w, h) = (%s,%s)" % (fullname, image.get_rect().width, image.get_rect().height)
    return image, image.get_rect()

# Lista Inicial de cartas
baralho = list()

# Lista dos destinos possiveis de naipe
destinos_naipe = {
    'copas': ['paus', 'espada'],
    'ouro': ['paus', 'espada'],
    'paus': ['copas', 'ouro'],
    'espada': ['copas', 'ouro'],
}

# Classe do Jogo
class PacienciaMain:
    """Main Class"""
    def __init__(self, width=1150, height=750):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Background
        self.background = pygame.image.load("images/background.png")
        self.backgroundRect = self.background.get_rect()
        self.screen.blit(self.background, self.backgroundRect)
        pygame.display.set_caption("PyCiência 1.0 - Desenvolvimento: Victor Cinaglia e Rafael Stoffalette")
        pygame.display.flip()
    
    def CriaDecks(self):
        """ Funcao que cria todos os decks e suas respectivas cartas """
        
        # Inicializando o Baralho
        global baralho
        naipes = ["copas", "ouro", "paus", "espada"]
        numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        
        for naipe in naipes:
            for numero in numeros:
                baralho.append(Carta(naipe=(naipe, numero)))
        
        baralho = randomize(baralho)
        
        # Deck geral
        self.decks = {
            # Decks inferiores
            'deck_1':               Deck(20,  240, tipo="inferior"),
            'deck_2':               Deck(180, 240, tipo="inferior"),
            'deck_3':               Deck(340, 240, tipo="inferior"),
            'deck_4':               Deck(500, 240, tipo="inferior"),
            'deck_5':               Deck(660, 240, tipo="inferior"),
            'deck_6':               Deck(820, 240, tipo="inferior"),
            'deck_7':               Deck(980, 240, tipo="inferior"),
            
            # Outros tipos de decks
            'deck_compra':          Deck(20,   25, tipo="compra"),
            'deck_deposito':        Deck(180,  25, tipo="deposito"),
            
            # Deck Montante (final)
            'deck_final_um':        Deck(500,  25, tipo="final"),
            'deck_final_dois':      Deck(660,  25, tipo="final"),
            'deck_final_tres':      Deck(820,  25, tipo="final"),
            'deck_final_quatro':    Deck(980,  25, tipo="final"),
        }
        
        # Adicionando as cartas do deck de Compra
        self.decks["deck_compra"].preenche_deck(24)
        
        # Percorrendo cada deck inferior e adicionando suas cartas
        for key in self.decks.keys():
            try:
                # Achando o numero do deck inferior
                numero_do_deck = int(key.split('_')[1])
            
                # Percorrendo cada deck inferior
                if numero_do_deck <= 7:
                    self.decks[key].preenche_deck(numero_do_deck)
            except:
                pass
                
    def CarregaSprites(self):
        """ Funcao que carrega os Sprites necessarios """
        cartas = list()

        # Adicionando os decks no Grupo de Sprites
        cartas.extend(self.decks.values())
        
        # Adicionando as cartas
        for deck in self.decks:
            for carta in self.decks[deck].lista_cartas:
                # Se esta for a ultima carta do deck, mostre a sua frente
                if carta in self.decks[deck].lista_cartas[-1:] and self.decks[deck].hierarquico == True:
                    carta.mostra_frente()
                    
                # Adiciona esta carta a lista atual
                cartas.append(carta)
        
        cartas = tuple(cartas)
        self.carta_sprites = pygame.sprite.LayeredUpdates(cartas)

    def reinicia(self):
        """Função que reinicia o baralho"""
        self.CriaDecks()
        carta_sprites = self.CarregaSprites();
        self.minutos = 0
        self.segundos = 0
        self.pontuacao = 0

    def MainLoop(self):
        # Criado o Clock do jogo
        clock = pygame.time.Clock()
        
        # Criando todos os Decks
        self.CriaDecks()
        
        # Inicializando o contador de minutos/segundos
        self.contador = 0
        self.segundos = 0
        self.minutos = 0
        
        # Inicializando o contador de pontuacao
        self.pontuacao = 0
        
        # Carregando os Sprites
        carta_sprites = self.CarregaSprites();

        # Definindo uma flag que determina se o mouse está clicado ou não
        clicked = 0
        
        # Inicializando contador de click duplo
        contador_duplo_click = 0
        self.click_duplo = False
        
        # Carta clicada
        carta_clicada = None
        click_offset = ''
        pos_inicial_carta_clicada = None
        
        # Vitoria inicia como False
        self.vitoria = False
        
        # Painel inicia escondido
        self.mostraPainel = False
        
        executando = True
        while executando:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                executando = False
            elif event.type == KEYDOWN and event.key == K_r:
                if self.mostraPainel == False and self.vitoria == False:
                    # Reinicia o Jogo
                    self.reinicia()
                
            elif event.type == KEYDOWN and event.key == K_c:
                # Se digitar c (comprar), compra uma carta
                self.decks["deck_compra"].compra_carta()
                
            elif event.type == KEYDOWN and event.key == K_v:
                # Forçando a vitória
                self.vitoria = True
                
            elif event.type == KEYDOWN and event.key == K_h:
                # Mostrando o painel de ajuda
                if self.mostraPainel == True:
                    self.mostraPainel = False
                else:
                    self.mostraPainel = True
                
            elif event.type == KEYDOWN and event.key == K_RETURN:
                # Forçando o reinicio da partida
                if self.vitoria == True:
                    self.vitoria = False
                    self.reinicia()
                    
                if self.mostraPainel == True:
                    self.mostraPainel = False
                
            elif event.type == MOUSEBUTTONDOWN:
                # Impedindo ações do mouse quando estiver no frame de vitória
                if self.vitoria == True or self.mostraPainel == True: break
                
                # Posicao do Clique
                click_x, click_y = event.pos
                print "Posicao do clique: (x: %d, y: %d)" % (click_x, click_y)
                
                # Ordena as cartas por ordem inversa de prfundidade (as do topo vem primeiro)
                sprites = self.carta_sprites.sprites()
                sprites.reverse()
                
                # Manipulando os dados caso o click seja duplo
                self.click_duplo = False
                if (pygame.time.get_ticks() - contador_duplo_click) < 300:
                    self.click_duplo = True
                    
                contador_duplo_click = pygame.time.get_ticks()
                
                # Se o click for no botao da status bar
                if self.statusbarRect.collidepoint(click_x, click_y):
                        if self.mostraPainel == True: self.mostraPainel = False
                        else: self.mostraPainel = True
                
                # Itera cada carda e verifica se o click foi em cima dela
                for sprite in sprites:
                    # Posicao da Carta
                    pos_carta_x = sprite.rect.x
                    pos_carta_y = sprite.rect.y
                    
                    # Tamanhos da Carta
                    tam_carta_x = sprite.rect.width
                    tam_carta_y = sprite.rect.height
                    
                    if click_x > pos_carta_x and click_x < pos_carta_x+tam_carta_x and click_y > pos_carta_y and click_y < pos_carta_y+tam_carta_y:
                        # A carta clicada é a esta
                        carta_clicada = sprite
                        
                        # Caso o click seja duplo, verifique se da pra colocar a carta no deck final
                        if self.click_duplo == True and carta_clicada is not None and carta_clicada.__class__.__name__ <> "Deck":
                            for deck in self.decks:
                                if self.decks[deck].tipo == "final":
                                    if (carta_clicada.__class__.__name__ == "Deck"): pass
                                    if (carta_clicada.deck.tipo == "compra"): pass
                                    elif (carta_clicada.ultima_carta_do_deck() is not True): pass
                                    elif (len(self.decks[deck].lista_cartas) == 0 and carta_clicada.naipe[1] <> 1): pass
                                    elif (len(self.decks[deck].lista_cartas) <> 0 and carta_clicada.naipe[0] <> self.decks[deck].ultima_carta().naipe[0]): pass
                                    elif (len(self.decks[deck].lista_cartas) <> 0 and carta_clicada.naipe[1] <> self.decks[deck].ultima_carta().naipe[1]+1): pass
                                    else:
                                        self.decks[deck].adiciona_cartas([carta_clicada])
                                        break

                        # Se o click foi no deck de compra, faça o seguinte:
                        if (sprite.__class__.__name__ == "Deck" and sprite.tipo == "compra") or (sprite.__class__.__name__ <> "Deck" and sprite.deck.tipo == "compra"):
                            self.decks["deck_compra"].compra_carta()
                            
                            # Carta clicada aponta para nada
                            carta_clicada = None
                            
                            break
                        elif sprite.__class__.__name__ == "Carta":
                            # Jogando a carta para o topo da tela
                            sprite.move_to_front(self.carta_sprites)
                            
                            # Mostrando a frente da carta
                            if sprite.costas == True and sprite.ultima_carta_do_deck():
                                sprite.mostra_frente(remove_pontos=True)
                        else:
                            # Nao faz nada se for um click em um deck qualquer vazio
                            carta_clicada = None
                        
                        # Offset do clique em relacao a carta
                        click_offset = [click_x-pos_carta_x, click_y-pos_carta_y]
                        
                        # Gravando a posicao inicial da carta clicada
                        pos_inicial_carta_clicada = [pos_carta_x, pos_carta_y]
                        
                        
                        print "Posicao da carta: (x: %d, y: %d)" % (pos_carta_x, pos_carta_y)
                        print "Offset do clique em relacao a carta: (x: %d, y: %d)" % (click_offset[0], click_offset[1])
                        
                        # Apos encontrar o primeiro
                        break
                        
                # Muda a flag para determinar clique em andamento
                clicked = 1
            elif event.type == MOUSEBUTTONUP:
                # Impedindo ações do mouse quando estiver no frame de vitória
                if self.vitoria == True or self.mostraPainel == True: break
                
                # Salvando as coordenadas do clique
                x, y = event.pos
                
                if clicked == 1 and carta_clicada is not None and self.click_duplo == False:
                    # Inicializando flag
                    move_back = True
                    
                    # Verificando se a carta deve ou nao encaixar-se em outro deck
                    sprites = self.carta_sprites.sprites()
                    sprites.reverse()

                    # Itera cada carta e verifica se a carta clicada está em cima (ou quase em cima) da carta atual
                    for sprite in sprites:
                        if (x > sprite.rect.x and x < (sprite.rect.x + sprite.rect.width)) and (y > sprite.rect.y and y < (sprite.rect.y + sprite.rect.height)) and carta_clicada <> sprite:
                            # A principio, o sprite destino é um deck
                            deck_destino = sprite
                            
                            # Se o sprite for do tipo carta, ache o seu deck
                            if sprite.__class__.__name__ == "Carta":
                                deck_destino = sprite.deck
                                
                            # Adiciona a carta clicada (e suas hierarquicas) para o deck destino
                            move_back = deck_destino.adiciona_cartas(carta_clicada.proximas_cartas())
                            break
                        
                    # Voltando a carta para a sua posicao inicial caso ela não tenha permissão para encaixar aonde se deseja
                    if move_back is True:
                        carta_clicada.move(pos_inicial_carta_clicada[0], pos_inicial_carta_clicada[1])
                
                # Muda a flag pra determinar fim do clique
                clicked = 0
                carta_clicada = None
                
                
            elif event.type == MOUSEMOTION:
                # Mouse está em movimento
                x, y = event.pos
                if clicked == 1 and self.click_duplo is False and carta_clicada is not None:
                    carta_clicada.move(x-click_offset[0], y-click_offset[1])
            
          # Atualizando o background infinitamente
          self.screen.blit(self.background, self.backgroundRect)
          
          # Criando o container dos decks montantes
          self.container = pygame.image.load("images/container.png")
          self.containerRect = self.container.get_rect()
          self.containerRect.y = 5
          self.containerRect.x = 475
          self.screen.blit(self.container, self.containerRect)
      
          # Atualizando todas as cartas do grupo de Sprites (carta_sprites)
          self.carta_sprites.draw(self.screen)

          # Carregando a Status Bar / Menus
          self.statusbar = pygame.image.load("images/statusbar/menu-background.png")
          self.statusbarRect = self.statusbar.get_rect()
          sr = self.screen.get_rect()
          self.statusbarRect.right = sr.right - 25 - 448 - 18
          self.statusbarRect.bottom = sr.bottom - 18
          self.screen.blit(self.statusbar, self.statusbarRect)
      
          # Apenas acontece se o frame de vitoria estiver invisível
          if self.mostraPainel == True:
          
                  # Carregando o Painel
                  self.painel = pygame.image.load("images/painel.png")
                  self.painelRect = self.painel.get_rect()
                  self.painelRect.centerx = sr.centerx
                  self.painelRect.centery = sr.centery
                  self.screen.blit(self.painel, self.painelRect)          
          
                  font = pygame.font.Font("Helvetica.otf", 14)
                  font.set_bold(True)
                  text = font.render(u' Ajuda sobre o pyciência ', True, (0, 0, 0))
                  textRect = text.get_rect()
                  textRect.right = self.painelRect.right - 45
                  textRect.top = 418
                  self.screen.blit(text, textRect)
          
                  font = pygame.font.Font("Helvetica.otf", 14)
                  txt = [
                        "Para sair do jogo aperte ESC",
                        "Para virar uma carta do monte aperte C",
                        "Para reiniciar o jogo aperte R",
                        "Para exibir este painel de ajuda, aperte H",
                        u"Para jogar carta no monte final, dê um clique duplo.",
                        "",
                        u"Sobre a Pontuação:",
                        "Ganhe 5 pontos ao virar carta da mesa",
                        "Ganhe 10 pontos ao colocar carta nos montes finais",
                        "Perca 15 pontos ao retirar carta dos montes finais",
                        "Perca 2 pontos a cada 10 segundos jogados"
                  ]
                  i = 0
                  for line in txt:
                          # Colocando a pontuacao em negrito
                          if line == u"Sobre a Pontuação:": font.set_bold(True)
                          else: font.set_bold(False)
                                  
                          text = font.render(line, True, (0, 0, 0))
                          textRect = text.get_rect()
                          textRect.right = self.painelRect.right - 45
                          textRect.top = 460 + i
                          self.screen.blit(text, textRect)
                          i += 23

          # Carregando o botão abre/fecha
          self.toggle = pygame.image.load("images/statusbar/open.png")
          self.toggleRect = self.toggle.get_rect()
          self.toggleRect.right = self.statusbarRect.right - 12
          self.toggleRect.centery = self.statusbarRect.centery
          self.screen.blit(self.toggle, self.toggleRect)
          
          # Mostrando o contador de segundos
          if pygame.time.get_ticks() > self.contador * 1000:
              self.contador += 1
              
              # Apenas acontece se o frame de vitoria estiver invisível
              if self.vitoria == False and self.mostraPainel == False:
                  self.segundos += 1
                  if self.segundos == 60:
                      self.minutos += 1
                      self.segundos = 0
          
                  # Remove 2 pontos a cada 10 segundos
                  if (self.segundos % 10) == 0:
                      self.pontuacao -= 2

          # Mostrando a Pontuação
          font = pygame.font.Font("Helvetica.otf", 14)
          text = font.render(u' %d:%02d %10s Pontuação: %s' % (self.minutos, self.segundos, '', self.pontuacao), True, (255, 255, 255))
          textRect = text.get_rect()
          textRect.left = self.statusbarRect.left + 10
          textRect.centery = self.statusbarRect.centery + 1
          self.screen.blit(text, textRect)
          
          # Mostrando a imagem de vitória
          if self.vitoria == True:
              self.vitoria_sobreposto = pygame.image.load("images/vitoria.png")
              self.vitoria_sobrepostoRect = self.vitoria_sobreposto.get_rect()
              sr = self.screen.get_rect()
              self.vitoria_sobrepostoRect.centerx = sr.centerx
              self.vitoria_sobrepostoRect.centery = sr.centery
              self.screen.blit(self.vitoria_sobreposto, self.vitoria_sobrepostoRect)
              
              # Mostrando a pontuacao em cima do frame de vitória
              font = pygame.font.Font("Helvetica.otf", 20)
              text = font.render(u'Pontuação: %s %35s Tempo: %d:%02d' % (self.pontuacao, '', self.minutos, self.segundos), True, (0, 0, 0))
              textRect = text.get_rect()
              textRect.centerx = self.vitoria_sobrepostoRect.centerx + 130
              textRect.centery = self.vitoria_sobrepostoRect.centery + 15
              self.screen.blit(text, textRect)
          
          pygame.display.flip()
          clock.tick(30)
          
class Carta(pygame.sprite.Sprite):
    """ Classe que define a carta e seus movimentos """
    
    def __init__(self, x=0, y=0, naipe=("copas", 1), deck=None):
        pygame.sprite.Sprite.__init__(self)
        
        # Inicializando as Costas da carta
        self.costas_image, self.costas_rect = load_image('card-back.png')
        
        # Inicializando a Frente da carta
        self.frente_image, self.costas_rect = load_image('cartas/%s/%s.png' % naipe)
        
        # A carta começa de Costas
        self.image, self.rect = self.costas_image, self.costas_rect
        
        # Alterando a posicao inicial da Carta
        self.rect.x = x
        self.rect.y = y
        
        # Alterando a carta
        self.costas = True
        
        # Alterando o Deck da Carta
        self.deck = deck
        
        # Alterando o naipe da carta
        self.naipe = naipe
        
        
    def move(self, x, y):
        """ Funcao que movimenta a carta """
        if self.costas == False:
            self.rect.x = x
            self.rect.y = y
            
            # Movendo as cartas abaixo desta hierarquicamente
            i = 0
            for carta in self.proximas_cartas():
                # A posicao do x é constante
                carta.rect.x = x
                
                # A posicao do y depende da profundidade de hierarquica
                carta.rect.y = y + (i * 25)
                
                # Incrementando o i
                i += 1
                
    def mostra_frente(self, remove_pontos=False):
        # Altera a carta para mostrar a Frente
        self.image = self.frente_image
        
        # Altera a pontuacao
        if self.deck.tipo == "inferior" and remove_pontos is True:
            MainWindow.pontuacao += 5
        
        # Altera o status da carta para Costas = False
        self.costas = False
    
    def mostra_costas(self):
        # Altera a carta para mostrar as Costas
        self.image = self.costas_image
        
        # Altera o status da carta para Costas = True
        self.costas = True
    
    def move_to_front(self, carta_sprites):
        # Movendo as cartas abaixo desta para o topo da tela, hierarquicamente
        for carta in self.proximas_cartas():
            carta_sprites.move_to_front(carta)
    
    def ultima_carta_do_deck(self):
        """ Funcao que retorna se a carta e a ultima carta do deck """
        if self in self.deck.lista_cartas[-1:]:
            return True
        else:
            return False
    
    def proximas_cartas(self):
        """ Funcao que retorna uma lista das cartas que estao mais no topo do deck, em relacao a esta carta """
        cartas = list()
        
        indice_carta = self.deck.lista_cartas.index(self)
        indice_ultima_carta = len(self.deck.lista_cartas)
        if indice_carta < indice_ultima_carta:
            for i in range(indice_carta, indice_ultima_carta):
                cartas.append(self.deck.lista_cartas[i])
        return cartas
        
class Deck(pygame.sprite.Sprite):
    """ Deck que contem um conjunto de cartas """
    def __init__(self, x, y, tipo="inferior"):
        pygame.sprite.Sprite.__init__(self)
        
        # Inicializando o Deck como vazio
        self.image, self.rect = load_image('empty.png')
        
        # Inicializando a pilha de cartas
        self.lista_cartas = list()
        
        # Baseado no tipo, altere sua hierarquia
        if tipo == "compra":
            self.image, self.rect = load_image('empty-ball.png')
            self.hierarquico = False
        elif tipo == "deposito":
            self.hierarquico = False
        elif tipo == "final":
            self.hierarquico = False
        elif tipo == "inferior":
            self.hierarquico = True

        # Alterando o tipo do deck
        self.tipo = tipo
        
        # Posicao do Deck na tela
        self.x = x
        self.y = y

        # Alterando a posicao inicial da Carta
        self.rect.x = x
        self.rect.y = y
        
    def preenche_deck(self, numero_de_cartas):
        """ Preenche o deck com as cartas do baralho geral, e remove elas do baralho antigo, ficando so neste deck """
        global baralho
        
        # Remove o numero_de_cartas do baralho geral, e adiciona neste deck
        for i in range(numero_de_cartas):
            carta = baralho.pop()
            
            # Alterando a coordenada y
            carta.rect.y = self.y
        
            # Se o deck for hierarquico, a proxima carta tera posicao Y maior
            if self.hierarquico == True:
                carta.rect.y += len(self.lista_cartas) * 12
            
            # A coordenaxa x sempre sera a mesma da do Deck
            carta.rect.x = self.x
        
            # Alterando o deck da carta para ser este
            carta.deck = self
        
            # Adicionando a carta ao deck
            self.lista_cartas.append(carta)
    
    def adiciona_cartas(self, cartas):
        """ Adiciona as cartas passadas como parametro neste deck, rearranjando suas posicoes """
        
        # Verifica se o deck é do tipo deposito ou compra
        if self.tipo in ["deposito", "compra"] : return True
        # Verifica se o deck é do tipo Final, nao aceita multiplas cartas arrastadas
        elif (self.tipo == "final" and len(cartas) <> 1): return True
        # Verifica se o deck for do tipo Final e estiver vazio, pois quando está, só se aceita Ases
        elif (self.tipo == "final" and len(self.lista_cartas) == 0 and cartas[0].naipe[1] <> 1): return True
        # Se o deck for do tipo Final e nao estiver vazio, verifica se a carta colocada é um numero maior que a do topo, e se é do mesmo naipe
        elif (self.tipo == "final" and len(self.lista_cartas) > 0 and cartas[0].naipe[1] <> self.ultima_carta().naipe[1]+1): return True
        # Se o deck for do tipo Final e nao estiver vazio, verifica se a carta colocada é do mesmo naipe q a maior do topo
        elif (self.tipo == "final" and len(self.lista_cartas) > 0 and cartas[0].naipe[0] <> self.ultima_carta().naipe[0]): return True
        
        # Se o deck for do tipo inferior
        elif (self.tipo == "inferior" and len(self.lista_cartas) == 0 and cartas[0].naipe[1] <> 13): return True
        elif (self.tipo == "inferior" and len(self.lista_cartas) > 0 and cartas[0].naipe[1] <> self.ultima_carta().naipe[1]-1): return True
        elif (self.tipo == "inferior" and len(self.lista_cartas) > 0 and cartas[0].naipe[0] not in destinos_naipe[self.ultima_carta().naipe[0]]): return True
        
        # Alterando a pontuacao
        if (self.tipo == "final" and cartas[0].deck.tipo <> "final"):
            # Soma 10 pontos se for uma carta que vai pro Deck final (vinda do montante ou da mesa)
            MainWindow.pontuacao += 10
        elif (self.tipo == "inferior" and cartas[0].deck.tipo == "final"):
            # Remove 15 pontos se for uma carta saindo do Deck Final para a mesa
            MainWindow.pontuacao -= 15

        # Move a carta clicada para a sua nova posicao
        x, y = self.posicao_proxima_carta()
        cartas[0].move(x, y)
        
        # Descobre a quantidade de cartas após a carta clicada (incluindo ela)
        quantidade_de_cartas = len(cartas)
                        
        # Cria uma pilha temporária
        deck_temporario = list()
        for i in range(quantidade_de_cartas):
            carta_atual = cartas[0].deck.lista_cartas.pop()
            deck_temporario.append(carta_atual)
                        
        # Adiciona o conteudo da pilha temporaria no deck atual
        deck_temporario.reverse()
        for carta_atual in deck_temporario:
            carta_atual.deck = self
            self.lista_cartas.append(carta_atual)
            
        
        # Verifica se o jogo acabou
        if len(MainWindow.decks["deck_final_um"].lista_cartas) == 13 and \
            len(MainWindow.decks["deck_final_dois"].lista_cartas) == 13 and \
            len(MainWindow.decks["deck_final_dois"].lista_cartas) == 13 and \
            len(MainWindow.decks["deck_final_dois"].lista_cartas) == 13:
            MainWindow.vitoria = True
            
        return False
        
    def compra_carta(self):
        """ Compra uma carta do deck de compra e coloca no deck de deposito """
        if (self.tipo == "compra"):
            
            # Se a quantide de cartas do deck de Compra for zero, transfira as cartas do deck à direita para o da esquerda
            if len(self.lista_cartas) == 0:
                for i in range(len(MainWindow.decks["deck_deposito"].lista_cartas)):
                    self.lista_cartas.append(MainWindow.decks["deck_deposito"].lista_cartas.pop())
                    
                    self.lista_cartas[i].deck = self
                    self.lista_cartas[i].move(self.x, self.y)
                    self.lista_cartas[i].mostra_costas()
                    self.lista_cartas[i].move_to_front(MainWindow.carta_sprites)
                return
            
            # Removendo a carta do seu deck de compra
            carta = self.lista_cartas.pop()
            
            # Virando a carta
            carta.mostra_frente()
            
            # Adiciona a carta do deck de Compra ao deck de Deposito
            MainWindow.decks["deck_deposito"].lista_cartas.append(carta)
            
            # Atualizando o deck desta para o deck da esquerda
            carta.deck = MainWindow.decks["deck_deposito"]
            
            # Jogando a carta para o topo
            carta.move_to_front(MainWindow.carta_sprites)
            
            # Movendo as cartas para a posicao do deck da direita
            carta.move(MainWindow.decks["deck_deposito"].x, MainWindow.decks["deck_deposito"].y)
            
    def posicao_proxima_carta(self):
        """ Retorna a posicao onde a proxima carta deve ser inserida """
        x, y = self.rect.x, self.rect.y
        
        # Se o deck for hierarquico, altere a posicao do "y"
        if self.hierarquico == True:
            for carta in self.lista_cartas:
                if carta.costas == True: y += 12
                else: y += 25

        return x, y

    
    def ultima_carta(self):
        """ Funcao que retorna a ultima carta do deck """
        if len(self.lista_cartas[-1:]) == 0:
            return False
        
        return self.lista_cartas[-1:][0]
        
def randomize(lista):
    """ Funcao que aceita uma lista, randomiza ela, e devolve outra lista randomizada """
    import random
    lista_randomizada = list()
    while lista:
        element = random.choice(lista)
        lista_randomizada.append(element)
        lista.remove(element)
    return lista_randomizada

if __name__ == "__main__":
    MainWindow = PacienciaMain()
    MainWindow.MainLoop()