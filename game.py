# game class
# contains a board and a list of players
import Screen
import boardTemp
import pygame
from random import randint
import time
import sys
depth = 0

pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 72)
font3 = pygame.font.SysFont("comicsans", 20)
font4 = pygame.font.SysFont("comicsans", 20)
class game:
    def __init__(self, board_size, pit_count):
        self.game_board = boardTemp.board(board_size, pit_count)
        Screen.player_score = [0, 0]
        self.current_player = 0


    def switchPlayer(self):
        '''
      moves to the next player
      '''
        self.current_player = (self.current_player + 1) % 2

    def updateScore(self, score):
        '''
      update scores of the current player
      '''

        Screen.player_score[self.current_player] = Screen.player_score[self.current_player] + score

    def isGame(self):
        '''
      returns True is the game has not reached the end
      returns False otherwise
      '''
        if self.game_board.isHalfEmpty():
            return False
        else:
            return True

    def getCurrentWinner(self):
        '''
      get who leads currently
      this method will return the winning player once called after the game is over
      '''
        return max(range(2), key=Screen.player_score.__getitem__)

    def Naiveplay2(self):
        '''
      play the game
      heuristics: select a random pit
      '''
        # choosing a pit
        time.sleep(0.5)
        pits = self.game_board.generateOptions(self.current_player)
        pit = pits[randint(0, len(pits)-1)]

        # make moves and update score
        score = self.game_board.move(pit)
        self.updateScore(score)
        self.switchPlayer()

    def UserPlay(self,pit):
        '''
      play the game
      heuristics: move from the user selected pit
      '''

        # make moves and update score
        score = self.game_board.move(pit)
        self.updateScore(score)
        self.switchPlayer()

    def ModifiedMinMax(self, board, limit, player, checker=0):
        global depth
        depth = depth + 1
        '''
      a recursive min-max function
      the function changes min/max utility based on the player passed
      the algorithm is modified such that the selection is made based on maximizing one score and minimizing a different score at each step
      '''

        # if the board is half empty the game is over
        if board.isHalfEmpty():
            return 0

        max_score = float("-inf")
        max_move = 0
        moves = board.generateOptions(player)
        # isCloneMove = True

        # check if the game state is in the level just above the limit in the min max tree
        # only check for maximum profit of the current player and return the best move
        if ((depth == (limit - 1)) or ((depth == limit) and (limit == 1))):
            for move_option in moves:

                new_board = board.clone()
                new_board_score = new_board.move2(move_option)

                if new_board_score > max_score:
                    max_score = new_board_score
                    max_move = move_option

                    # on any depth other than limit - 1 recursively call the function and get the best score of the opponent in the resulting stage of the current move
        # calculate the ratio of the addition to current player score by the move, to best potential addition to the opponent score of the resulting game state by the move
        # choose the move with maximum ratio
        else:
            max_ratio = float("-inf")
            for move_option in moves:
                new_board = board.clone()
                new_player = (player + 1) % 2
                score = new_board.move2(move_option)
                opponent_score = self.ModifiedMinMax(new_board, limit, new_player, depth)

                if opponent_score != 0:
                    if float(score / opponent_score) > max_ratio:
                        max_score = score
                        max_ratio = float(score / opponent_score)
                        max_move = move_option
                else:
                    max_score = score
                    max_move = move_option

        if checker == 1:
            return max_move
        else:
            return max_score

    def MinMaxplay(self, limit):
        '''
      plays the game based on modified min max strategy
      since the entire tree traversal is not optimal, a depth limit is provided
      '''
        global depth

        # choosing a pit
        pit = self.ModifiedMinMax(self.game_board, limit, self.current_player, 1)
        depth = depth - 1
        # make moves and update score
        score = self.game_board.move(pit)
        self.updateScore(score)
        self.switchPlayer()

    def drawText(self, text, color, rect, font, aa=False, bkg=None):
        print(rect)
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            Screen.screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

    def __main__(self):
        Screen.initialize()
        pygame.font.init()
        Screen.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("PALLANKUZHI")
        Screen.screen.fill((0,0,0))
        flagMain = 1
        isGame = True

        # newgame = game(12, 5)
        # newgame.__main__()

        # while isGame:
        while isGame & self.isGame():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    isGame = False

            # clearing Screen.screen before printing boards
            if flagMain == 1:

                flag = 1
                while flag:
                    Screen.screen.fill((0, 0, 0))
                    bg = pygame.image.load("Untitled.jpg").convert()
                    Screen.screen.blit(bg, (0, 0))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            isGame = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()

                            if pos[0] > 97 and pos[0] < 186 and pos[1] > 373 and pos[1] < 394:

                                bg = pygame.image.load("how_to.jpg").convert()
                                Screen.screen.blit(bg, (25, 25))
                                # pygame.draw.rect(Screen.screen, (0, 153, 153), [25, 25, 450, 550], 5,5)

                                # text = "Step 1: The major objective of the Pallankuzhi"
                                # temp = font4.render(text, 1, (93, 121, 125))
                                # Screen.screen.blit(temp,(35,35))
                                text = font2.render("X",1, (255, 0, 0))
                                Screen.screen.blit(text,(430,500))
                                pygame.display.update()
                                flag2 = 1
                                while flag2:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                            isGame = False
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            pos = pygame.mouse.get_pos()
                                            if pos[0] > 430 and pos[0] <463 and pos[1] > 500 and pos[1] < 542:
                                                flag2 = 0
                                            # if pos[0] > 193 and pos[0] < 305 and pos[1] > 525 and pos[1] < 542:
                                            #     movie = pygame.movie.Movie("Pallankuzhi.mpeg")
                                            #     sur_obj = pygame.display.set_mode(movie.get_size())
                                            #     mov_scre = pygame.Surface(movie.get_size()).convert()
                                            #     movie.set_display(mov_scre)
                                            #     movie.play()


                            if pos[0] > 297 and pos[0] < 386 and pos[1] > 372 and pos[1] < 400:

                                # text = "Pallankuzhi is an ancient and traditional Mancala game which was played in South India. In South India, Pallankuzhi was played mostly in Tamil Nadu and later on, the games were played in places like Karnataka, Kerala, Andhra Pradesh, Sri Lanka, Malaysia. There are quite a large number of variants associated with the Pallankuzhi game such as Ali Guli mane in Kannada, Vamana Guntalu in Telugu and Kuzhipara in Malayalam. This game is an indoor game and is one of the oldest games which helps in enhancing the memory of the players. It is played on a wooden board that is hand carved in nature and the major intent of the game is capturing more seeds than your other opponent. Similarly, the Pallanguzhi game is known as Kuzhipara in Malayalam and is the oldest form of the Mancala game. The origin of the Pallankuzhi game was during the period of the Chola dynasty in India. This game was played by the players on the premises of the temple and later on became quite famous with the Tamil people."

                                bg = pygame.image.load("history.jpg").convert()
                                Screen.screen.blit(bg, (25, 25))
                                img = pygame.image.load("rsz_2pallanguzhi.jpg").convert()
                                Screen.screen.blit(img, (140, 450))

                                # pygame.draw.rect(Screen.screen, (0, 153, 153), [25, 25, 450, 550], 5, 5)
                                # self.drawText(text, (93, 121, 125), [50, 50, 400, 530], font3)
                                text = font2.render("X", 1, (255, 0, 0))
                                Screen.screen.blit(text, (430, 500))
                                pygame.display.update()
                                flag2 = 1
                                while flag2:
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                        isGame = False
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            pos = pygame.mouse.get_pos()
                                            if pos[0] > 430 and pos[0] < 463 and pos[1] > 500 and pos[1] < 542:
                                                flag2 = 0
                            if pos[0] > 27 and pos[0] < 471 and pos[1] > 270 and pos[1] < 330:
                                flag = 0
                pygame.display.update()

            flagMain = 0

            Screen.screen.fill((0, 0, 0))
            bg = pygame.image.load("pallanguzhi main.jpg").convert()
            Screen.screen.blit(bg, (0, 0))
            pygame.display.update()

            # text = font2.render("PALLANGUZHI",1,(255,255,0))
            # Screen.screen.blit(text,(60,80))
            pygame.draw.rect(Screen.screen, (0, 153, 153), [30, 260, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (0, 153, 153), [110, 260, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (0, 153, 153), [190, 260, 50 ,50], border_radius=5)
            pygame.draw.rect(Screen.screen, (0, 153, 153), [270, 260, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (0, 153, 153), [350, 260, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (0, 153, 153), [430, 260, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (160, 160, 160), [30, 360, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (160, 160, 160), [110, 360, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (160, 160, 160), [190, 360, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (160, 160, 160), [270, 360, 50, 50], border_radius=5)
            pygame.draw.rect(Screen.screen, (160, 160, 160), [350, 360, 50,50], border_radius=5)
            pygame.draw.rect(Screen.screen, (160, 160, 160), [430, 360, 50, 50], border_radius=5)
            # Screen.screen.blit(bg, (0, 200))

            size = int(self.game_board.board_size / 2)

            # displaying board 0
            new_list = self.game_board.board_list[::-1]
            temp_list = new_list[:size]

            for i in range(size):
                text = font.render(str(temp_list[i]), 1, (0, 0, 0))
                Screen.screen.blit(text, (80 * i + 42, 275))

            # displaying board 1
            temp_list = self.game_board.board_list[:size]
            for i in range(size):
                text = font.render(str(temp_list[i]), 1, (0, 0, 0))
                Screen.screen.blit(text, (80 * i + 42, 375))

            text = font.render(
                "You: " + str(Screen.player_score[0]), 1, (160, 160, 160))
            Screen.screen.blit(text, (70, 450))

            text = font.render("Computer: " + str(Screen.player_score[1]), 1,(0, 153, 153))
            Screen.screen.blit(text, (230, 450))

            pygame.display.update()
            if self.current_player == 1:
                temp = "Computer move, Click to proceed"
                text = font.render(temp, 1, (93, 121, 125))
                Screen.screen.blit(text, (30, 180))

            else:
                temp = "Your move, click on a PIT"
                text = font.render(temp, 1, (93, 121, 125))
                Screen.screen.blit(text, (70, 180))

            pygame.display.update()

            mouseClick = False
            while not mouseClick:
                if self.current_player == 1:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            isGame = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouseClick = True

                if self.current_player == 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            isGame = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()

                            pits = self.game_board.generateOptions(self.current_player)

                            flag = 0
                            for i in pits:
                                if pos[0] > (i*80+42) and pos[0] < (i*80+90) and pos[1] > 375 and pos[1] < 425:
                                    flag = 1
                                    pit = i
                                    break
                            if flag:
                                mouseClick = True

            if self.current_player == 0 and isGame:
                self.UserPlay(pit)
            elif self.current_player == 1 and isGame:
                self.MinMaxplay(2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    isGame = False

        if self.getCurrentWinner() == 0:
            Screen.screen.fill((0,0,0))
            pygame.draw.rect(Screen.screen, (93, 121, 125), [50, 200, 400, 200], 5, 5)
            text = font2.render("YOU WIN!!!",1,(93, 121, 125))
            Screen.screen.blit(text, (120,275))
        else:
            Screen.screen.fill((0, 0, 0))
            pygame.draw.rect(Screen.screen, (93, 121, 125), [50, 200, 400, 200], 5, 5)
            text = font2.render("GAME OVER!", 1, (93, 121, 125))
            Screen.screen.blit(text, (95, 270))
        pygame.display.update()
        while isGame:
            time.sleep(2)
            text = font.render("Press N to start, Press Q to exit",1,(90, 100, 25),(255,255,255))
            Screen.screen.blit(text,(40,450))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        isGame = False
                    isGame = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        isGame = False
                    if event.key == pygame.K_n:

                        newgame = game(12, 5)
                        newgame.__main__()

        pygame.quit()

# Screen.initialize()
# newgame = game(12, 5)
# newgame.__main__()

