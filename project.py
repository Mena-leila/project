import pygame
import sys

# تهيئة pygame
pygame.init()

# ثوابت
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 70, 70)
BLUE = (70, 70, 255)
ORANGE = (255, 180, 0)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 100)
BLACK = (0, 0, 0)
DARK_BLUE = (20, 20, 40)
BUTTON_BG = (200, 200, 200)
BUTTON_HOVER = (170, 170, 170)
TEXT_COLOR = (10, 10, 10)

MARGIN_TOP = 100
MARGIN_LEFT = 50
BALL_RADIUS = 10
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 80
PADDLE_SPEED = 7
BALL_INITIAL_SPEED = 5
WINNING_SCORE = 5

# إعداد الشاشة
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong Game - Menu Modes")
play_area = pygame.Rect(MARGIN_LEFT, MARGIN_TOP, SCREEN_WIDTH - 2 * MARGIN_LEFT, SCREEN_HEIGHT - 2 * MARGIN_TOP)

# الكائنات
ball = pygame.Rect(play_area.centerx - BALL_RADIUS, play_area.centery - BALL_RADIUS, 2 * BALL_RADIUS, 2 * BALL_RADIUS)
player1 = pygame.Rect(play_area.right - 2 * PADDLE_WIDTH, play_area.centery - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(play_area.left + PADDLE_WIDTH, play_area.centery - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_speed = [BALL_INITIAL_SPEED, BALL_INITIAL_SPEED]
player1_speed = 0
player2_speed = 0

player1_score = 0
player2_score = 0

# الخطوط
font = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)
font_title = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

def reset_game():
    global ball_speed, player1_score, player2_score
    ball.center = play_area.center
    ball_speed = [BALL_INITIAL_SPEED, BALL_INITIAL_SPEED]
    player1.centery = play_area.centery
    player2.centery = play_area.centery
    player1_score = 0
    player2_score = 0

def reset_ball():
    ball.center = play_area.center
    ball_speed[0] *= -1

def ball_animation():
    global ball_speed, player1_score, player2_score
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= play_area.top or ball.bottom >= play_area.bottom:
        ball_speed[1] *= -1

    if ball.colliderect(player1) and ball_speed[0] > 0:
        ball_speed[0] *= -1
    if ball.colliderect(player2) and ball_speed[0] < 0:
        ball_speed[0] *= -1

    if ball.left <= play_area.left:
        player1_score += 1
        if player1_score >= WINNING_SCORE:
            show_winner("Player 1")
            return True
        reset_ball()

    if ball.right >= play_area.right:
        player2_score += 1
        if player2_score >= WINNING_SCORE:
            show_winner("Player 2")
            return True
        reset_ball()

    return False

def move_player(player, speed):
    player.y += speed
    if player.top < play_area.top:
        player.top = play_area.top
    if player.bottom > play_area.bottom:
        player.bottom = play_area.bottom

def move_player1():
    move_player(player1, player1_speed)

def move_player2():
    move_player(player2, player2_speed)

# التنبؤ بموقع الكرة بعد فترة معينة
def predict_ball_position():
    future_x = ball.x + ball_speed[0] * 10  # التنبؤ بموقع الكرة بعد 10 إطارات
    future_y = ball.y + ball_speed[1] * 10
    return future_x, future_y

# تحسين حركة الذكاء الاصطناعي باستخدام Greedy Best-First Search
def ai_control(paddle):
    future_x, future_y = predict_ball_position()

    # تحديد الموقع المثالي لمقابلة الكرة
    if paddle.centery < future_y:
        paddle.y += 5
    elif paddle.centery > future_y:
        paddle.y -= 5

    # التأكد من أن المضرب لا يخرج من منطقة اللعب
    if paddle.top < play_area.top:
        paddle.top = play_area.top
    if paddle.bottom > play_area.bottom:
        paddle.bottom = play_area.bottom

def draw_ball():
    pygame.draw.ellipse(screen, ORANGE, ball)

def draw_paddles():
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)

def draw_score():
    score_text1 = font_small.render(str(player1_score), True, WHITE)
    score_text2 = font_small.render(str(player2_score), True, WHITE)
    screen.blit(score_text1, (SCREEN_WIDTH // 2 + 40, 40))
    screen.blit(score_text2, (SCREEN_WIDTH // 2 - 70, 40))

def draw_play_area():
    pygame.draw.rect(screen, WHITE, play_area, 2)

def draw_back_button(back_rect, back_arrow):
    pygame.draw.rect(screen, GRAY, back_rect)
    screen.blit(back_arrow, (back_rect.x + 5, back_rect.y))

def show_winner(winner):
    while True:
        screen.fill(DARK_BLUE)
        win_text = font.render(f"{winner} Wins!", True, YELLOW)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60)
        pygame.draw.rect(screen, BUTTON_BG, back_rect, border_radius=10)
        back_text = font_small.render("Back", True, TEXT_COLOR)
        screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    pygame.time.delay(200)
                    return

        pygame.display.flip()
        clock.tick(60)

def run_game(mode):
    global player1_speed, player2_speed
    reset_game()
    running = True

    back_rect = pygame.Rect(10, 10, 40, 40)
    back_arrow = font.render("←", True, YELLOW)

    while running:
        screen.fill(DARK_BLUE)
        draw_play_area()
        draw_back_button(back_rect, back_arrow)
        draw_ball()
        draw_paddles()
        draw_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    pygame.time.delay(200)
                    return

            if event.type == pygame.KEYDOWN:
                if mode in ("PvP", "PvAI"):
                    if event.key == pygame.K_UP:
                        player1_speed -= PADDLE_SPEED
                    if event.key == pygame.K_DOWN:
                        player1_speed += PADDLE_SPEED
                if mode == "PvP":
                    if event.key == pygame.K_w:
                        player2_speed -= PADDLE_SPEED
                    if event.key == pygame.K_s:
                        player2_speed += PADDLE_SPEED

            if event.type == pygame.KEYUP:
                if mode in ("PvP", "PvAI"):
                    if event.key == pygame.K_UP:
                        player1_speed += PADDLE_SPEED
                    if event.key == pygame.K_DOWN:
                        player1_speed -= PADDLE_SPEED
                if mode == "PvP":
                    if event.key == pygame.K_w:
                        player2_speed += PADDLE_SPEED
                    if event.key == pygame.K_s:
                        player2_speed -= PADDLE_SPEED

        if ball_animation():
            return

        move_player1()
        if mode == "PvP":
            move_player2()
        elif mode == "PvAI":
            ai_control(player2)
        elif mode == "AIvsAI":
            ai_control(player1)
            ai_control(player2)

        pygame.display.flip()
        clock.tick(60)

def main_menu():
    while True:
        screen.fill(DARK_BLUE)
        title = font.render("Ping Pong Game", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        buttons = [("START", "start_game"), ("EXIT", "exit_game")]
        mouse = pygame.mouse.get_pos()
        button_rects = []

        for i, (text, action) in enumerate(buttons):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 220 + i * 100, 300, 60)
            button_rects.append((rect, action))
            color = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON_BG
            pygame.draw.rect(screen, color, rect, border_radius=10)
            label = font_small.render(text, True, TEXT_COLOR)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in button_rects:
                    if rect.collidepoint(event.pos):
                        pygame.time.delay(200)
                        if action == "start_game":
                            game_mode_menu()
                        elif action == "exit_game":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()
        clock.tick(60)

def game_mode_menu():
    while True:
        screen.fill(DARK_BLUE)
        title = font.render("Choose Game Mode", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        buttons = [("AI vs AI", "AIvsAI"), ("Player vs Player", "PvP"), ("Player vs AI", "PvAI")]
        mouse = pygame.mouse.get_pos()
        button_rects = []

        for i, (text, mode) in enumerate(buttons):
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 220 + i * 100, 300, 60)
            button_rects.append((rect, mode))
            color = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON_BG
            pygame.draw.rect(screen, color, rect, border_radius=10)
            label = font_small.render(text, True, TEXT_COLOR)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, mode in button_rects:
                    if rect.collidepoint(event.pos):
                        pygame.time.delay(200)
                        run_game(mode)

        pygame.display.flip()
        clock.tick(60)

if _name_ == "_main_":
    main_menu()
