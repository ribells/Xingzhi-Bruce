import pygame, sys, random
import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(8, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc3 = nn.Linear(512, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = DQN()
model.load_state_dict(torch.load('model_weights_700.pth', weights_only=True, map_location=torch.device('cpu')))

def act(bx, by, spdx, spdy, px, py, ox, oy):
    return torch.argmax(model(torch.Tensor([bx, by, spdx, spdy, px, py, ox, oy])))

pygame.init()

WIDTH, HEIGHT = 900, 600

FONT = pygame.font.SysFont("Consolas", int(WIDTH / 20))

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")

CLOCK = pygame.time.Clock()

BALL_SPD = 3
PADDLE_SPD = 10

# Paddles

player = pygame.Rect(0, 0, 10, 100)
player.center = (WIDTH - 100, HEIGHT / 2)

opponent = pygame.Rect(0, 0, 10, 100)
opponent.center = (100, HEIGHT / 2)

player_score, opponent_score = 0, 0

# Ball

ball = pygame.Rect(0, 0, 20, 20)
ball.center = (WIDTH / 2, HEIGHT / 2)

x_speed, y_speed = BALL_SPD, BALL_SPD



while True:
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP]:
        if player.top > 0:
            player.top -= PADDLE_SPD
    if keys_pressed[pygame.K_DOWN]:
        if player.bottom < HEIGHT:
            player.bottom += PADDLE_SPD

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ball.y >= HEIGHT:
        y_speed = -BALL_SPD
    if ball.y <= 0:
        y_speed = BALL_SPD
    if ball.x <= 0:
        player_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]) * BALL_SPD, random.choice([1, -1]) * BALL_SPD
    if ball.x >= WIDTH:
        opponent_score += 1
        ball.center = (WIDTH / 2, HEIGHT / 2)
        x_speed, y_speed = random.choice([1, -1]) * BALL_SPD, random.choice([1, -1]) * BALL_SPD
    if player.x - ball.width <= ball.x <= player.right and ball.y in range(player.top - ball.width,
                                                                           player.bottom + ball.width):
        x_speed = -BALL_SPD
    if opponent.x - ball.width <= ball.x <= opponent.right and ball.y in range(opponent.top - ball.width,
                                                                               opponent.bottom + ball.width):
        x_speed = BALL_SPD


    opp = act(ball.center[0], ball.center[1], x_speed, y_speed,
              player.x, player.y,
              opponent.x, opponent.y)
    if opponent.y < ball.y:
        opponent.top += PADDLE_SPD
    else:
        opponent.bottom -= PADDLE_SPD

    ball.x += x_speed * 2
    ball.y += y_speed * 2

    SCREEN.fill("Black")

    pygame.draw.rect(SCREEN, "white", player)
    pygame.draw.rect(SCREEN, "white", opponent)
    pygame.draw.circle(SCREEN, "white", ball.center, 10)

    '''
    player_score_text = FONT.render(str(player_score), True, "white")
    opponent_score_text = FONT.render(str(opponent_score), True, "white")
    SCREEN.blit(player_score_text, (WIDTH / 2 + 50, 50))
    SCREEN.blit(opponent_score_text, (WIDTH / 2 - 50, 50))
    '''

    pygame.display.update()
    CLOCK.tick(60)