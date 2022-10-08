import time
import pygame


class Chat:
    def __init__(self, game):
        self.chat = {}
        self.game_ref = game
        self.chatbox = False



    def append(self, chat, color = False):
        if not color:
            color = self.game_ref.player_team.color
        self.chat[time.time()] = [chat, color]
        print("Chat appended")


    def tick_chat_box(self):

        if not self.chatbox:
            return
        if self.chatbox.active:
            self.chatbox.tick()
            if "enter" in self.game_ref.keypress and self.chatbox.text != "":

                self.game_ref.datagatherer.data.append(f"self.game_ref.chat.append(\"{self.game_ref.player_team.name} : {self.chatbox.text}\", color = {self.game_ref.player_team.color})")
                self.append(self.chatbox.text)
                self.chatbox.text = ""
                self.chatbox.active = False
                return

        if self.chatbox.active:
            if "esc" in self.game_ref.keypress:
                self.chatbox.active = False
        else:
            if "t" in self.game_ref.keypress or "enter" in self.game_ref.keypress:
                self.chatbox.active = True
                self.chatbox.text = ""




    def tick(self):
        self.tick_chat_box()
        y_pos = 120
        for time_1 in sorted(self.chat, reverse=True):
            chat = self.chat[time_1][0]
            text = self.game_ref.terminal[30].render(str(chat), False, self.chat[time_1][1])

            if time_1 + 4 < time.time():
                alpha = 255 - 255*(time.time()-4-time_1)
                text.set_alpha(alpha)
            elif time_1 + 0.5 > time.time():
                alpha = 255*(2*(time.time()-time_1))
                text.set_alpha(alpha)
            self.game_ref.screen.blit(
                text, [self.game_ref.resolution[0] - text.get_size()[0], y_pos]
            )
            y_pos += 40

            if time_1 + 5 < time.time() and time_1 in self.chat:
                del self.chat[time_1]
