import pygame
import pygame.font

import pygame_menu
import pygame_menu.font
import pygame_menu.themes

import sqlite3
import json
import random

class SQL_DATABASE:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS GameDataBase(
                            Username CHAR(25),
                            High_Score INT,
                            Top_Five_High_Scores INT,
                            Upgrade_Money INT);""")
    
    def add_or_check_username(self, username):
        self.username = username
        self.cursor.execute("SELECT Username FROM GameDataBase WHERE Username=?", (self.username,))
        list_of_usernames = self.cursor.fetchall()
        list_of_usernames = [item for tup in list_of_usernames for item in tup]
        self.connection.commit()
        if len(list_of_usernames) > 0:
            return 'Already taken'
        else:
            self.cursor.execute("INSERT INTO GameDataBase (Username) VALUES (?)", (self.username,))
            self.connection.commit()
            return "Username inserted"
    
    def retrive_data(self, use, username):
        if use == "Rank Table":
            self.username = username
            # System extracting relevant the high scores
            self.cursor.execute("SELECT High_Score FROM GameDataBase ORDER BY High_Score DESC LIMIT 5")
            top_5_high_scores = self.cursor.fetchall()
            # Converts list of tuples to regular list
            top_5_high_scores = [item for tup in top_5_high_scores for item in tup]
            self.cursor.execute("SELECT High_Score FROM GameDataBase WHERE Username=?", (self.username,))
            users_high_score = self.cursor.fetchall()[0][0]
            self.cursor.execute("SELECT Username FROM GameDataBase ORDER BY High_Score DESC LIMIT 5;")
            list_of_top_five_high_score_usernames = self.cursor.fetchall()
            # Converts list of tuples to regular list
            list_of_top_five_high_score_usernames = [item for tup in list_of_top_five_high_score_usernames for item in tup]
            #checking if either variables have the value None assined to them
            if  None in top_5_high_scores or users_high_score == None:
                if  None in top_5_high_scores:
                    index = top_5_high_scores.index(None)
                    top_5_high_scores[index] = 0
                elif users_high_score == None:
                    users_high_score = 0
                else:
                    index = top_5_high_scores.index(None)
                    top_5_high_scores[index] = 0
                    users_high_score = 0
            # Swaps the last value with the users value if it is not in the list and if it is in the list gets its position
            if self.username not in list_of_top_five_high_score_usernames:
                top_5_high_scores[4] = users_high_score
                # Checking what position the users high score is
                self.cursor.execute("Select Count(High_Score) From GameDataBase Where High_Score < ?", (users_high_score,))
                smaller_high_scores = self.cursor.fetchall()[0][0]
                self.cursor.execute("Select Count(High_Score) From GameDataBase")
                users_position = (self.cursor.fetchall()[0][0]) - smaller_high_scores
                # Getting usernames and returning the data requested
                self.cursor.execute("SELECT Username FROM GameDataBase ORDER BY High_Score DESC LIMIT 4;")
                list_of_top_four_high_score_usernames = self.cursor.fetchall()
                # Converts list of tuples to regular list
                list_of_top_four_high_score_usernames = [item for tup in list_of_top_four_high_score_usernames for item in tup]
                if list_of_top_four_high_score_usernames == None:
                    list_of_top_four_high_score_usernames == [0, 0, 0, 0, 0]
                array_of_data_for_table = [[1, list_of_top_four_high_score_usernames[0], top_5_high_scores[0]],
                                          [2, list_of_top_four_high_score_usernames[1], top_5_high_scores[1]],
                                          [3, list_of_top_four_high_score_usernames[2], top_5_high_scores[2]],
                                          [4, list_of_top_four_high_score_usernames[3], top_5_high_scores[3]],
                                          [users_position, self.username, top_5_high_scores[4]]]
                return array_of_data_for_table
            # Finding the position of the users high score in the top 5 if it is in the list
            else:
                # Sorrting and collecting the information requested if the users high score is in the top 5 
                if list_of_top_five_high_score_usernames == None:
                    list_of_top_five_high_score_usernames == ["", "", "", "", ""]
                if len(top_5_high_scores) == 5:
                    array_of_data_for_table = [[1, list_of_top_five_high_score_usernames[0], top_5_high_scores[0]],
                                               [2, list_of_top_five_high_score_usernames[1], top_5_high_scores[1]],
                                               [3, list_of_top_five_high_score_usernames[2], top_5_high_scores[2]],
                                               [4, list_of_top_five_high_score_usernames[3], top_5_high_scores[3]],
                                               [5, list_of_top_five_high_score_usernames[4], top_5_high_scores[4]]]
                    return array_of_data_for_table
                elif len(top_5_high_scores) == 4:
                    array_of_data_for_table = [[1, list_of_top_five_high_score_usernames[0], top_5_high_scores[0]],
                                               [2, list_of_top_five_high_score_usernames[1], top_5_high_scores[1]],
                                               [3, list_of_top_five_high_score_usernames[2], top_5_high_scores[2]],
                                               [4, list_of_top_five_high_score_usernames[3], top_5_high_scores[3]]]
                    return array_of_data_for_table
                elif len(top_5_high_scores) == 3:
                    array_of_data_for_table = [[1, list_of_top_five_high_score_usernames[0], top_5_high_scores[0]],
                                               [2, list_of_top_five_high_score_usernames[1], top_5_high_scores[1]],
                                               [3, list_of_top_five_high_score_usernames[2], top_5_high_scores[2]]]
                    return array_of_data_for_table
                elif len(top_5_high_scores) == 2:
                    array_of_data_for_table = [[1, list_of_top_five_high_score_usernames[0], top_5_high_scores[0]],
                                               [2, list_of_top_five_high_score_usernames[1], top_5_high_scores[1]]]
                    return array_of_data_for_table
                elif len(top_5_high_scores) == 1:
                    array_of_data_for_table = [[1, list_of_top_five_high_score_usernames[4], top_5_high_scores[4]]]
                    return array_of_data_for_table
        elif use == "Top 5 scores table":
            self.username = username
            self.cursor.execute("SELECT Top_Five_High_Scores FROM GameDataBase WHERE Username=?", (self.username,))
            top_fives_scores = self.cursor.fetchall()[0][0]
            self.connection.commit()
            if top_fives_scores == None:
                top_fives_scores = [0, 0, 0, 0, 0]
            else:
                # converts string list to physical list
                top_fives_scores = json.loads(top_fives_scores)
            return top_fives_scores
        elif use == "Money for upgrades":
            self.username = username
            self.cursor.execute("SELECT Upgrade_Money FROM GameDataBase WHERE Username=?", (self.username,))
            upgrade_money = self.cursor.fetchall()[0][0]
            if upgrade_money == None:
                upgrade_money = 0
            return upgrade_money
        self.connection.commit()
    
    def UpdateData(self, collum_to_update, data, item_purchased, username):
        if collum_to_update == "High score":
            self.username = username
            self.cursor.execute("SELECT High_Score FROM GameDataBase WHERE Username = ?", (self.username,))
            high_score = self.cursor.fetchall()[0][0]
            if high_score == None:
                high_score = data
            if high_score <= data:
                self.cursor.execute("UPDATE GameDataBase SET High_Score = ? WHERE Username = ?", (data, self.username,))
            self.connection.commit()
        elif collum_to_update == "Upgrade money":
            self.username = username
            self.cursor.execute("Select Upgrade_Money From GameDataBase WHERE Username=?", (self.username,))
            upgrade_money = self.cursor.fetchall()[0][0]
            if upgrade_money == None:
                upgrade_money = data
            elif item_purchased == False:
                upgrade_money += data
            else:
                upgrade_money = data
            self.cursor.execute("UPDATE GameDataBase SET Upgrade_Money = ? WHERE Username = ?", (upgrade_money, self.username,))
            self.connection.commit()
        elif collum_to_update == "Top_Five_High_Scores":
            self.username = username
            self.cursor.execute("SELECT Top_Five_High_Scores FROM GameDataBase WHERE Username = ?", (self.username,))
            data_list = self.cursor.fetchall()[0][0]
            data_chaged = False
            if data_list == None:
                data_list = [data, 0, 0, 0, 0]
            else:
                # converts string list to physical list
                data_list = json.loads(data_list)
            if data in data_list:
                data_chaged = True
            if data_list[4] < data:
                while data_chaged == False:
                    if data_list[3] > data:
                        data_list[4] = data
                        data_chaged = True
                    elif data_list[2] > data:
                        data_list[4] = data_list[3]
                        data_list[3] = data
                        data_chaged = True
                    elif data_list[1] > data:
                        data_list[4] = data_list[3]
                        data_list[3] = data_list[2]
                        data_list[2] = data
                        data_chaged = True
                    elif data_list[0] > data:
                        data_list[4] = data_list[3]
                        data_list[3] = data_list[2]
                        data_list[2] = data_list[1]
                        data_list[1] = data
                        data_chaged = True
                    elif data_list[0] < data:
                        data_list[4] = data_list[3]
                        data_list[3] = data_list[2]
                        data_list[2] = data_list[1]
                        data_list[1] = data_list[0]
                        data_list[0] = data
                        data_chaged = True
            data_serialized = json.dumps(data_list)
            self.cursor.execute("UPDATE GameDataBase SET Top_Five_High_Scores = ? WHERE Username = ?", (data_serialized, self.username,))
            self.connection.commit()
            data_serialized = json.dumps(data_list)
            self.cursor.execute("UPDATE GameDataBase SET Top_Five_High_Scores = ? WHERE Username = ?", (data_serialized, self.username,))
            self.connection.commit()

# Class for player
class Player(pygame.sprite.Sprite):
    def __init__(self, hero_bullet_group, hero_grenade_group):
        super().__init__()
        self.list_of_upgrades = [[[40, "Damage level 1", "This increases the damage by a multiplyer of 2", False],[80, "Grenader level 1", "This gives you 1 grenade at the start of the game", False],[120, "Damage level 2", "This increases the damage by a multiplier of 8", False],[160, "Grenader level 2", "This gives you 4 grenades at the start of the game", False],[200, "One man army", "This gives you a damage multiplier of 12 and gives you 8 grenades to start with", False]],
                                     [[40, "Armor level 1", "This allows you to reduce the damage taken by a tenth", False],[80, "Doctor level 1", "You start with 1 medpack", False],[120, "Armor level 2", "This reduces the damge taken by a quarter", False],[160, "Doctor level 2", "You start with 4 medpack", False],[200, "Strong as nails", "This reduces the damage taken by a half and you start with 6 medpacks", False]],
                                     [[40, "Deeper pockets", "This increases the ammount of ammunition you start with from 30 to 60", False],[80, "Supply drop level 1", "This increses the spawn rate of the collectables by a multiplier of 1.5", False],[120, "Even deeper pockets", "This increases the ammount of ammunition you start with from 60 to 120", False],[160, "Supply drop level 2", "This increses the spawn rate of the collectables by a multiplier of 2", False],[200, "Supply master", "This increases the ammuntion you start with from 120 to 240 and increases the swapn rate of the collectables by a multiplier of 2.5", False]]]
        self.starting_ammo = 30
        self.medpack_amount = 0
        self.restarted_medpack_ammount = self.medpack_amount
        self.ammo = self.starting_ammo
        self.starting_grenades = 0
        self.bullet_velocity = 10
        self.grenade_velocity = 10
        self.grenades = self.starting_grenades
        self.lives = 5
        self.starting_lives = self.lives
        self.image = pygame.image.load("hero2.png")
        self.hero_width = self.image.get_width()
        self.hero_hight = self.image.get_height()
        self.rect = self.image.get_rect()
        self.hero_bullet_group = hero_bullet_group
        self.hero_grenade_group = hero_grenade_group
        self.rect.bottomleft = (0,400)
        self.velocity = 3
        self.hero_damage = 1    
    def update_player(self):
        self.mask = pygame.mask.from_surface(self.image)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 95:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.y < 500 - 105:
            self.rect.y += self.velocity
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity

    def shoot(self):
        HeroBullet((self.rect.centerx + 20), (self.rect.centery - 25), self.bullet_velocity, self.hero_bullet_group)
    def frow_grenade(self):
        HeroGrenade((self.rect.centerx + 20), (self.rect.centery - 25), self.grenade_velocity, self.hero_grenade_group)

            
class HeroBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_velocity, bullet_group):
        super().__init__()
        self.velocity = bullet_velocity
        self.range = 750 # pixles before bullet is removed        
        # load image and get the rect
        self.image = pygame.transform.scale(pygame.image.load("Character bullet.png"), (45,29)).convert_alpha()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        # Add are bullet group
        bullet_group.add(self)
        
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        # Move are bullet
        self.rect.x += self.velocity
        # Destroy bullet after it pass the range of 450
        if abs(self.rect.x) > self.range:
            self.kill()

class HeroGrenade(pygame.sprite.Sprite):
    def __init__(self, x, y, grenade_velocity, grenade_group):
        super().__init__()
        self.velocity = grenade_velocity
        # load image and get the rect
        self.image = pygame.transform.scale(pygame.image.load("Grenade.png"), (45,29)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.range = self.rect.x + 300 # pixles before grenade explodes
        # Adds to are grenade group
        grenade_group.add(self)

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        # Move are bullet
        self.rect.x += self.velocity
        # Destroy bullet after it pass the range of 450
        if abs(self.rect.x) > self.range:
            self.kill()

# Class for enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_bullet_group):
        super().__init__()
        self.bullet_velocity = 10
        self.damage = 1
        self.starting_health = 1
        self.health = 1
        self.score_on_defeate = 1
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.enemy_width = self.image.get_width()
        self.enemy_hight = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = random.randint(95, 500 - 95)
        self.enemy_velocity = 3
        self.enemy_bullet_group = enemy_bullet_group
    def update_enemy(self):
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.x < 0:
            self.rect.x = 900
            self.rect.y = random.randint(95, 500 - 95)
        else:
            self.rect.x -= self.enemy_velocity
    def shoot(self):
        EnemyBullet((self.rect.centerx - 20), (self.rect.centery - 25), self.bullet_velocity, self.enemy_bullet_group)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__ (self, x, y, bullet_velocity, bullet_group):
        super().__init__()
        self.velocity = bullet_velocity
        self.range = 50
        self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("Character bullet.png"), True, False), (45,29)).convert_alpha() # flip takes iamge, horixontal T/F, vertical T/F
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        # Add are bullet group
        bullet_group.add(self)

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        # Move are bullet
        self.rect.x -= self.velocity
        # Destroy bullet after it pass the range of 450
        if abs(self.rect.x) < self.range:
            self.kill()

class Medpack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.medpack_increase_lives = 1
        self.velocity = 5
        self.spawn_rate = 60000
        self.image = pygame.transform.scale(pygame.image.load("MedPack.png"), (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = random.randint(95, 500 - 95)
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x -= self.velocity
        if self.rect.x < 0:
            self.kill()

class Ammobox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ammobox_ammo_increase = 15
        self.velocity = 5
        self.spawn_rate = 90000
        self.image = pygame.transform.scale(pygame.image.load("AmmoBox.png"), (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = random.randint(95, 500 - 95)
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x -= self.velocity
        if self.rect.x < 0:
            self.kill()

class Display(pygame.sprite.Sprite):
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        super().__init__()
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        #  Game variable
        self.score = 0
        # Defining the font
        self.font = pygame.font.SysFont("impact", 32)
        # Groups
        self.hero_group = pygame.sprite.Group()
        self.hero_bullet_group = pygame.sprite.Group()
        self.hero_grenade_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.medpack_group = pygame.sprite.Group()
        self.ammobox_group = pygame.sprite.Group()
        # Classes
        self.hero = Player(self.hero_bullet_group, self.hero_grenade_group)
        self.enemy = Enemy(self.enemy_bullet_group)
        self.database = SQL_DATABASE()
        self.hero_group.add(self.hero)
        self.enemy_group.add(self.enemy)
        # Timer
        self.shoot_event = pygame.USEREVENT + 1
        self.medpack_event = pygame.USEREVENT + 2
        self.ammopack_event = pygame.USEREVENT + 3

    def main_screen(self):
        clicked = False
        # Setting up the font and theme for the pygame-menu main screen menu
        main_screen_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        main_screen_menu_theme.title_font = pygame_menu.font.FONT_8BIT
        main_screen_menu_theme.background_color = "Black"

        # Setting up the pygame-menu main screen menu
        main_screen_menu = pygame_menu.Menu('Fallen soldier',
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            theme = main_screen_menu_theme
        )
        self.name_input = main_screen_menu.add.text_input(
            'Username: ',
            default = ''
        )
        main_screen_menu.add.button(
            'Play',
            self.game_screen
        )
        self.dificulty_selector = main_screen_menu.add.selector(
            'Dificulty',
            [('Medium', 3), ('Hard', 2), ('Easy', 1)]
        )
        self.button = main_screen_menu.add.button("Upgrades",lambda: self.Upgrades_screen(button_pressed = "No"))
        main_screen_menu.add.button("Rank table", self.table_rank_screen)
        main_screen_menu.add.button("Information", self.Information_screen)

        main_screen_menu.add.button(
            'Quit',
            pygame_menu.events.EXIT
        )
        main_screen_menu.mainloop(self.screen)
        # While loop polling for the event of mouse button down so we know which button has been pressed
        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
        if clicked == True:
            pygame.quit()

    def table_rank_screen(self):
        clicked = False
        self.database.add_or_check_username(username = self.name_input.get_value())
        data_list = self.database.retrive_data(use = "Rank Table", username = self.name_input.get_value())
        #Setting up the font and theme for the pygame-menu main screen menu
        high_score_screen_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        high_score_screen_menu_theme.title_font = pygame_menu.font.FONT_8BIT
        high_score_screen_menu_theme.background_color = "Black"
        # Setting up the high score menu and the high score table
        high_score_screen_menu = pygame_menu.Menu(
            'Fallen soldier',
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            theme = high_score_screen_menu_theme
        )
        high_score_screen_menu.add.button("Return back to main menu", self.main_screen, float = True, float_origin_position = True)
        high_score_screen_menu_high_score_table = high_score_screen_menu.add.table(
            table_id = 'High score table displayed on the high score menu',
            font_size = 25,
            )
        high_score_screen_menu_high_score_table.default_cell_padding = 15
        high_score_screen_menu_high_score_table.default_cell_border_color  = 'white'
        high_score_screen_menu_high_score_table.add_row(
            ['Position', 'Username', 'High score'],
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )
        # Adding the data to the rank table table 
        if len(data_list) == 1:
            high_score_screen_menu_high_score_table.add_row(
                [data_list[0][0], data_list[0][1], data_list[0][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
        elif len(data_list) == 2:
            high_score_screen_menu_high_score_table.add_row(
                [data_list[0][0], data_list[0][1], data_list[0][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[1][0], data_list[1][1], data_list[1][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
        elif len(data_list) == 3:
            high_score_screen_menu_high_score_table.add_row(
                [data_list[0][0], data_list[0][1], data_list[0][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[1][0], data_list[1][1], data_list[1][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[2][0], data_list[2][1], data_list[2][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
        elif len(data_list) == 4:
            high_score_screen_menu_high_score_table.add_row(
                [data_list[0][0], data_list[0][1], data_list[0][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[1][0], data_list[1][1], data_list[1][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[2][0], data_list[2][1], data_list[2][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[3][0], data_list[3][1], data_list[3][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
        elif len(data_list) == 5:
            high_score_screen_menu_high_score_table.add_row(
                [data_list[0][0], data_list[0][1], data_list[0][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[1][0], data_list[1][1], data_list[1][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[2][0], data_list[2][1], data_list[2][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[3][0], data_list[3][1], data_list[3][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )
            high_score_screen_menu_high_score_table.add_row(
                [data_list[4][0], data_list[4][1], data_list[4][2]],
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
            )

        high_score_screen_menu.mainloop(self.screen)
        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
        if clicked == True:
            pygame.quit()
    
    def Upgrades_screen(self, button_pressed):
        clicked = False
        self.purchase_upgrade = False
        self.database.add_or_check_username(username = self.name_input.get_value())
        upgrade_money = self.database.retrive_data(use = "Money for upgrades", username = self.name_input.get_value())
        #Setting up the font and theme for the pygame-menu main screen menu 
        Upgrades_screen_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        Upgrades_screen_menu_theme.title_font = pygame_menu.font.FONT_8BIT
        Upgrades_screen_menu_theme.background_color = "Black"
        # Setting up the high score menu and the high score table
        Upgrades_screen_menu = pygame_menu.Menu(
            'Fallen soldier',
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            theme = Upgrades_screen_menu_theme
        )
        Upgrades_screen_menu.add.button("Return back to main menu", self.main_screen, float = True, float_origin_position = True)
        
        Damage_level_1_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[0][0][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[0][0][1]))
        Damage_level_1_button.set_float(origin_position=True)
        Damage_level_1_button.translate(10,75)
        Damage_level_1_button.readonly = False        

        Grenader_level_1_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[0][1][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[0][1][1]))
        Grenader_level_1_button.set_float(origin_position=True)
        Grenader_level_1_button.translate(10,150)
        Grenader_level_1_button.readonly = True

        Damage_level_2_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[0][2][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[0][2][1]))
        Damage_level_2_button.set_float(origin_position=True)
        Damage_level_2_button.translate(10,225)
        Damage_level_2_button.readonly = True

        Grenader_level_2_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[0][3][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[0][3][1]))
        Grenader_level_2_button.set_float(origin_position=True)
        Grenader_level_2_button.translate(10,300)
        Grenader_level_2_button.readonly = True

        One_man_army_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[0][4][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[0][4][1]))
        One_man_army_button.set_float(origin_position=True)
        One_man_army_button.translate(10,375)
        One_man_army_button.readonly = True

        Armor_level_1_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[1][0][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[1][0][1]))
        Armor_level_1_button.set_float(origin_position=True)
        Armor_level_1_button.translate(250,75)
        
        Doctor_level_1_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[1][1][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[1][1][1]))
        Doctor_level_1_button.set_float(origin_position=True)
        Doctor_level_1_button.translate(250,150)
        Doctor_level_1_button.readonly = True
        
        Armor_level_2_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[1][2][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[1][2][1]))
        Armor_level_2_button.set_float(origin_position=True)
        Armor_level_2_button.translate(250,225)
        Armor_level_2_button.readonly = True
        
        Doctor_level_2_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[1][3][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[1][3][1]))
        Doctor_level_2_button.set_float(origin_position=True)
        Doctor_level_2_button.translate(250,300)
        Doctor_level_2_button.readonly = True
        
        Strong_as_nails_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[1][4][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[1][4][1]))
        Strong_as_nails_button.set_float(origin_position=True)
        Strong_as_nails_button.translate(250,375)
        Strong_as_nails_button.readonly = True
        
        Deeper_pockets_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[2][0][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[2][0][1]))
        Deeper_pockets_button.set_float(origin_position=True)
        Deeper_pockets_button.translate(475,75)
        Deeper_pockets_button
        
        Supply_drop_level_1_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[2][1][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[2][1][1]))
        Supply_drop_level_1_button.set_float(origin_position=True)
        Supply_drop_level_1_button.translate(475,150)
        Supply_drop_level_1_button.readonly = True
        
        Even_deeper_pockets_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[2][2][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[2][2][1]))
        Even_deeper_pockets_button.set_float(origin_position=True)
        Even_deeper_pockets_button.translate(475,225)
        Even_deeper_pockets_button.readonly = True
        
        Supply_drop_level_2_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[2][3][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[2][3][1]))
        Supply_drop_level_2_button.set_float(origin_position=True)
        Supply_drop_level_2_button.translate(475,300)
        Supply_drop_level_2_button.readonly = True
        
        Supply_master_button = Upgrades_screen_menu.add.button(self.hero.list_of_upgrades[2][4][1], lambda: self.purchse_upgrades(text_clicked = self.hero.list_of_upgrades[2][4][1]))
        Supply_master_button.set_float(origin_position=True)
        Supply_master_button.translate(475,375)
        Supply_master_button.readonly = True

        if button_pressed == "Yes":
            if self.upgrade_purchased == True:
                upgrade_money -= self.cost_of_upgrade
                self.database.UpdateData(collum_to_update = "Upgrade money", data = upgrade_money, item_purchased = True, username = self.name_input.get_value())
                self.hero.list_of_upgrades[self.text_index[0]][self.text_index[1]][(self.text_index[2]) + 2] = True
                if self.hero.list_of_upgrades[self.text_index[0]][self.text_index[1]][(self.text_index[2]) + 2] == True:
                    if self.text_index[0] == 0:
                        if self.text_index[1] == 0:
                            Damage_level_1_button.readonly = True
                            Grenader_level_1_button.readonly = False
                            self.hero.hero_damage = self.hero.hero_damage * 2
                        elif self.text_index[1] == 1:
                            Grenader_level_1_button.readonly = True
                            Damage_level_2_button.readonly = False
                            self.hero.starting_grenades = 1
                        elif self.text_index[1] == 2:
                            Damage_level_2_button.readonly = True
                            Grenader_level_2_button.readonly = False
                            self.hero.hero_damage = self.hero.hero_damage * 8
                        elif self.text_index[1] == 3:
                            Grenader_level_2_button.readonly = True
                            One_man_army_button.readonly = False
                            self.hero.starting_grenades = 4
                        elif self.text_index[1] == 4:
                            One_man_army_button.readonly = True
                            self.hero.hero_damage = self.hero.hero_damage * 12
                            self.hero.starting_grenades = 8
                    elif self.text_index[0] == 1:
                        if self.text_index[1] == 0:
                            Armor_level_1_button.readonly = True
                            Doctor_level_1_button.readonly = False
                            self.enemy.damage = self.enemy.damage * 0.9
                        elif self.text_index[1] == 1:
                            Doctor_level_1_button.readonly = True
                            Armor_level_2_button.readonly = False
                            self.hero.medpack_amount = 1
                        elif self.text_index[1] == 2:
                            Armor_level_2_button.readonly = True
                            Doctor_level_2_button.readonly = False
                            self.enemy.damage = self.enemy.damage * 0.75
                        elif self.text_index[1] == 3:
                            Doctor_level_2_button.readonly = True
                            Strong_as_nails_button.readonly = False
                            self.hero.medpack_amount = 4
                        elif self.text_index[1] == 4:
                            Strong_as_nails_button.readonly = True
                            self.enemy.damage = self.enemy.damage * 0.5
                            self.hero.medpack_amount = 6
                    elif self.text_index[0] == 2:
                        if self.text_index[1] == 0:
                            Deeper_pockets_button.readonly = True
                            Supply_drop_level_1_button.readonly = False
                            self.hero.starting_ammo = 60
                        elif self.text_index[1] == 1:
                            Supply_drop_level_1_button.readonly = True
                            Even_deeper_pockets_button.readonly = False
                            Medpack().spawn_rate = Medpack().spawn_rate * 1.5
                            Ammobox().spawn_rate = Ammobox().spawn_rate * 1.5
                        elif self.text_index[1] == 2:
                            Even_deeper_pockets_button.readonly = True
                            Supply_drop_level_2_button.readonly = False
                            self.hero.starting_ammo = 120
                        elif self.text_index[1] == 3:
                            Supply_drop_level_2_button.readonly = True
                            Supply_master_button.readonly = False
                            Medpack().spawn_rate = Medpack().spawn_rate * 2
                            Ammobox().spawn_rate = Ammobox().spawn_rate * 2
                        elif self.text_index[1] == 4:
                            Supply_master_button.readonly = True
                            self.hero.starting_ammo = 240
                            Medpack().spawn_rate = Medpack().spawn_rate * 2.5
                            Ammobox().spawn_rate = Ammobox().spawn_rate * 2.5
        
        Upgrades_screen_menu.mainloop(self.screen)
        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
        if clicked == True:
            pygame.quit()

    def purchse_upgrades(self, text_clicked):
        clicked = False  
        for a in range (0, 3):
            for b in range (0, 5):
                for c in range (0, len(self.hero.list_of_upgrades)):
                    if self.hero.list_of_upgrades[a][b][c] == text_clicked:
                        self.text_index = [a,b,c]
                        break
        self.cost_of_upgrade = self.hero.list_of_upgrades[self.text_index[0]][self.text_index[1]][(self.text_index[2])-1]
        aditional_information = self.hero.list_of_upgrades[self.text_index[0]][self.text_index[1]][(self.text_index[2])+1]
        Upgrades_purchase_screen_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        Upgrades_purchase_screen_menu_theme.title_font = pygame_menu.font.FONT_8BIT
        Upgrades_purchase_screen_menu_theme.background_color = "Black"
        # Setting up the high score menu and the high score table
        Upgrades_purchase_screen_menu = pygame_menu.Menu(
            'Fallen soldier',
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            theme = Upgrades_purchase_screen_menu_theme
        )
        Upgrades_purchase_screen_menu.add.label(text_clicked)
        Upgrades_purchase_screen_menu.add.label(aditional_information)
        Upgrades_purchase_screen_menu.add.button("Yes", lambda: self.button_clicked_yes_or_no(second_buton_pressed = "Yes"))
        Upgrades_purchase_screen_menu.add.button("No", lambda: self.button_clicked_yes_or_no(second_buton_pressed = "No"))

        Upgrades_purchase_screen_menu.mainloop(self.screen)
        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
        if clicked == True:
            pygame.quit()
    
    def button_clicked_yes_or_no (self, second_buton_pressed):
        if second_buton_pressed == "Yes":
            self.upgrade_purchased = True
            self.Upgrades_screen(button_pressed = "Yes")
        elif second_buton_pressed == "No":
            self.upgrade_purchased = False
            self.Upgrades_screen(button_pressed = "No")

    def Information_screen(self):
        clicked = False
        #Setting up the font and theme for the pygame-menu main screen menu
        Information_screen_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        Information_screen_menu_theme.title_font = pygame_menu.font.FONT_8BIT
        Information_screen_menu_theme.background_color = "Black"
        # Setting up the high score menu and the high score table
        Information_screen_menu = pygame_menu.Menu(
            'Fallen soldier',
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            theme = Information_screen_menu_theme
        )

        Information_screen_menu.add.button("Return back to main menu", self.main_screen, float = True, float_origin_position = True)

        Information_screen_menu_table = Information_screen_menu.add.table(
            table_id = 'Menu for all the game controls',
            font_size = 14,
            )
        Information_screen_menu_table.default_cell_padding = 15
        Information_screen_menu_table.default_cell_border_color  = 'white'
        
        Information_screen_menu_table.add_row(
            ('Control', 'Use'),
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )

        Information_screen_menu_table.add_row(
            ('Up arrow','Moves the player up when playing the game'),
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )

        Information_screen_menu_table.add_row(
            ('Left arrow','Moves the player left when playing the game'),
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )

        Information_screen_menu_table.add_row(
            ('Down arrow','Moves the player down when playing the game'),
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )

        Information_screen_menu_table.add_row(
            ('Right arrow','Moves the player right when playing the game'),
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )

        Information_screen_menu_table.add_row(
            ('Space Bar','Shoots the players gun when playing the game'),
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )

        Information_screen_menu.mainloop(self.screen)
        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
    
    def change_dificulty(self, dificulty):
        
        # Extracting inner tuple from outer tuple and converting the inner tuple to a list
        dificulty = [item for item in dificulty if isinstance(item, tuple)]
        dificulty = [item for tup in dificulty for item in tup]

        # Checking whether the difficulty has changed to easy or hard we do not include medium as no variable change when the dificulty is medium
        if 'Easy' in dificulty:
            self.hero.hero_damage = self.hero.hero_damage * 1.5
            self.enemy.damage = self.enemy.damage * 0.75
            self.enemy.bullet_velocity = self.hero.bullet_velocity * 0.75
            self.enemy.score_on_defeate = self.enemy.score_on_defeate * 1.5
        elif 'Hard' in dificulty:
            self.hero.hero_damage = self.hero.hero_damage * 0.75
            self.enemy.damage = self.enemy.damage * 1.5
            self.enemy.bullet_velocity = self.hero.bullet_velocity * 1.5
            self.enemy.score_on_defeate = self.enemy.score_on_defeate * 0.75

    def game_screen(self):
        clock = pygame.time.Clock()
        pygame.time.set_timer(self.shoot_event, 1500)
        pygame.time.set_timer(self.medpack_event, Medpack().spawn_rate)
        pygame.time.set_timer(self.ammopack_event, Ammobox().spawn_rate)
        clicked = False    

        self.change_dificulty(dificulty = self.dificulty_selector.get_value())

        score_text = self.font.render(f"Score: {self.score}", True, "blue", "grey")
        score_text_rect = score_text.get_rect()
        score_text_rect = (self.WINDOW_WIDTH-160, 30)
       
        lives_text = self.font.render(f"Lives: {self.hero.lives}", True, "blue", "grey")
        lives_text_rect = lives_text.get_rect()
        lives_text_rect = (self.WINDOW_WIDTH-760, 30)

        ammo_text = self.font.render(f"Ammo: {self.hero.ammo}", True, "blue", "grey")
        ammo_text_rect = score_text.get_rect()
        ammo_text_rect = (self.WINDOW_WIDTH - 795, self.WINDOW_HEIGHT - 50)

        grenade_text = self.font.render(f"Grenades: {self.hero.grenades}", True, "blue", "grey")
        grenade_text_rect = grenade_text.get_rect()
        grenade_text_rect = (self.WINDOW_WIDTH - 165, self.WINDOW_HEIGHT - 50)

        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.hero.ammo > 0:
                        self.hero.shoot()
                        self.hero.ammo -= 1
                        ammo_text = self.font.render(f"Ammo: {self.hero.ammo}", True, "blue", "grey")
                    if event.key == pygame.K_g and self.hero.grenades > 0:
                        self.hero.frow_grenade()
                        self.hero.grenades -= 1
                        grenade_text = self.font.render(f"Grenades: {self.hero.grenades}", True, "blue", "grey")
                if event.type == self.shoot_event and self.enemy.rect.x < self.WINDOW_WIDTH + 250:
                    self.enemy.shoot()
                if event.type == self.medpack_event:
                    self.medpack_group.add(Medpack())
                if event.type == self.ammopack_event:
                     self.ammobox_group.add(Ammobox())
            if pygame.sprite.spritecollide(self.enemy, self.hero_grenade_group, True, pygame.sprite.collide_mask):
                self.enemy.health -= self.hero.hero_damage
                if self.enemy.health == 0:
                    self.score += self.enemy.score_on_defeate
                    score_text = self.font.render(f"Score: {self.score}", True, "blue", "grey")
                    self.enemy.health = self.enemy.starting_health
                    self.enemy.rect.x = 900
                    self.enemy.rect.y = random.randint(95, 500 - 95)
            if pygame.sprite.spritecollide(self.enemy, self.hero_bullet_group, True, pygame.sprite.collide_mask):
                self.enemy.health -= self.hero.hero_damage
                if self.enemy.health == 0:
                    self.score += self.enemy.score_on_defeate
                    score_text = self.font.render(f"Score: {self.score}", True, "blue", "grey")
                    self.enemy.health = self.enemy.starting_health
                    self.enemy.rect.x = 900
                    self.enemy.rect.y = random.randint(95, 500 - 95)
                    self.hero.bullet_velocity = (self.hero.bullet_velocity * 1.05)
                    self.enemy.bullet_velocity = (self.enemy.bullet_velocity * 1.05)
            if pygame.sprite.spritecollide(self.hero, self.enemy_bullet_group, True, pygame.sprite.collide_mask):
                self.hero.lives -= self.enemy.damage
                lives_text = self.font.render(f"Lives: {self.hero.lives}", True, "blue", "grey")
                if self.hero.lives == 0:
                    lives_text = self.font.render(f"Lives: {self.hero.lives}", True, "blue", "grey")
                    self.enemy.rect.x = 900
                    self.game_over_screen()
            if pygame.sprite.spritecollide(self.hero, self.medpack_group, True, pygame.sprite.collide_mask):
                self.hero.lives += Medpack().medpack_increase_lives
                lives_text = self.font.render(f"Lives: {self.hero.lives}", True, "blue", "grey")
            if pygame.sprite.spritecollide(self.hero, self.ammobox_group, True, pygame.sprite.collide_mask):
                self.hero.ammo += Ammobox().ammobox_ammo_increase
                ammo_text = self.font.render(f"Ammo: {self.hero.ammo}", True, "blue", "grey")
            if pygame.sprite.spritecollide(self.hero, self.ammobox_group, True, pygame.sprite.collide_mask):
                self.hero.ammo += Ammobox().ammobox_ammo_increase
                ammo_text = self.font.render(f"Ammo: {self.hero.ammo}", True, "blue", "grey")

            self.screen.fill("grey")
            line = pygame.draw.line(self.screen, "blue", (0,90), (self.WINDOW_WIDTH, 90), 3)
            self.screen.blit(score_text, score_text_rect)
            self.screen.blit(lives_text, lives_text_rect)
            self.screen.blit(ammo_text, ammo_text_rect)
            self.screen.blit(grenade_text, grenade_text_rect )
            self.hero_group.update() 
            self.hero_group.draw(self.screen)
            self.enemy_group.update()
            self.enemy_group.draw(self.screen)
            self.hero.update_player()
            self.enemy.update_enemy()
            self.hero_bullet_group.update()
            self.hero_bullet_group.draw(self.screen)
            self.enemy_bullet_group.update()
            self.enemy_bullet_group.draw(self.screen)
            self.hero_grenade_group.update()
            self.hero_grenade_group.draw(self.screen)
            self.medpack_group.update()
            self.medpack_group.draw(self.screen)
            self.ammobox_group.update()
            self.ammobox_group.draw(self.screen)
            

            pygame.display.flip()
            pygame.display.update()
            clock.tick(60) / 1000
        pygame.quit()

    def game_over_screen(self):
        clicked = False
        # Updating and pulling data from the SQL database
        self.database.add_or_check_username(username = self.name_input.get_value())
        self.database.UpdateData(collum_to_update = "Upgrade money", data = self.score, item_purchased = False, username = self.name_input.get_value())
        self.database.UpdateData(collum_to_update = "High score", data = self.score, item_purchased = False, username = self.name_input.get_value())
        self.database.UpdateData(collum_to_update = "Top_Five_High_Scores", data = self.score, item_purchased = False, username = self.name_input.get_value())
        data_list = self.database.retrive_data(use = "Top 5 scores table", username = self.name_input.get_value())
        self.score = 0
        self.hero.lives = self.hero.starting_lives
        self.hero.ammo = self.hero.starting_ammo
        self.hero.bullet_velocity = 10
        self.enemy.bullet_velocity = 10
        game_over_screen_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        game_over_screen_menu_theme.title_font = pygame_menu.font.FONT_8BIT
        game_over_screen_menu_theme.background_color = "Black"
        game_over_screen_menu = pygame_menu.Menu(
            'Fallen soldier',
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT,
            theme = game_over_screen_menu_theme
        )
        # Adding the data to the rank table table
        game_over_screen_menu.add.label("Game Over", max_char=-1, font_size=55)
        game_over_screen_menu.add.button("Restart", self.game_screen)
        game_over_screen_menu.add.button("Back to the main menu", self.main_screen)
        game_over_screen_menu_high_score_table = game_over_screen_menu.add.table(
            table_id = 'High score table displayed on the high score menu',
            font_size = 25,
            )
        game_over_screen_menu_high_score_table.default_cell_padding = 5
        game_over_screen_menu_high_score_table.default_cell_border_color  = 'white'
        game_over_screen_menu_high_score_table.add_row(
            ['Position', 'High score'],
            cell_font = pygame_menu.font.FONT_8BIT,
            cell_align = pygame_menu.locals.ALIGN_CENTER
        )
        if len(data_list) == 1:
            game_over_screen_menu_high_score_table.add_row(
                (1, data_list[0]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER 
                )
        if len(data_list) == 2:
            game_over_screen_menu_high_score_table.add_row(
                (1, data_list[0]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (2, data_list[1]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
        if len(data_list) == 3:
            game_over_screen_menu_high_score_table.add_row(
                (1, data_list[0]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (2, data_list[1]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (3, data_list[2]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
        if len(data_list) == 4:
            game_over_screen_menu_high_score_table.add_row(
                (1, data_list[0]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (2, data_list[1]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (3, data_list[2]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (4, data_list[3]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
        if len(data_list) == 5:
            game_over_screen_menu_high_score_table.add_row(
                (1, data_list[0]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (2, data_list[1]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (3, data_list[2]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (4, data_list[3]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
            game_over_screen_menu_high_score_table.add_row(
                (5, data_list[4]),
                cell_font = pygame_menu.font.FONT_8BIT,
                cell_align = pygame_menu.locals.ALIGN_CENTER
                )
        game_over_screen_menu.mainloop(self.screen)
        while clicked == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clicked = True
        if clicked == True:
            pygame.quit()

pygame.init()

WINDOW_WIDTH = 800

WINDOW_HEIGHT = 500

screen = Display(WINDOW_WIDTH, WINDOW_HEIGHT)

screen.main_screen()