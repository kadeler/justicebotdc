import discord
from discord.ext import commands

class reasonpacker:
    def __init__(self, reason, answer):
        self.reason = reason
        self.answer = answer

reasons = [reasonpacker('kick', 'who to kick'), reasonpacker('ban', 'who to ban'),
           reasonpacker('unban', 'who to unban')]

i = input('input reason...\n')

for obj in reasons:
    if i == obj.reason:
        print(obj.answer)

input()
