"""The midnight birthday letter."""

from __future__ import annotations

from html import escape

from bot.config import BotConfig


def birthday_letter(config: BotConfig) -> str:
    """Build the long midnight birthday letter with personal names."""

    her = escape(config.girlfriend_name)
    him = escape(config.boyfriend_name)
    return f"""
🎂❤️ <b>Happy Birthday, {her}</b> ❤️🎂

My love,

Today is finally here. The day the world became softer, brighter, and more beautiful because you were born.

I wish I could be beside you right now. I wish I could hold your hand, look into your eyes, and say all of this without a screen between us. But even from far away, please feel this: you are loved deeply, intentionally, and completely.

You are not just someone I love. You are my favorite thought, my calm place, my sweetest missing, and the person who makes distance feel worth fighting through.

እንኳን ተወለድሽ ፍቅሬ። ዛሬ የአንቺ ቀን ነው። አንቺ ሕይወቴን በፍቅር፣ በተስፋ፣ በደስታ ሞልተሻል። ርቀት ቢኖርም ልቤ ሁልጊዜ ከአንቺ ጋር ነው።

I am proud of you. I admire your heart, your strength, your beauty, your softness, your mind, and all the little things that make you you. I love the way you exist in this world. I love the way your name feels like home to me.

I hope today reminds you that you are precious. Not just because it is your birthday, but because every ordinary day with you in it becomes special to me.

One day, I will not just send birthday wishes. I will bring flowers. I will hug you for too long. I will laugh with you, take pictures with you, celebrate you in person, and make sure you never have to wonder how loved you are.

Until then, this little bot is carrying pieces of my heart to you.

Happy birthday, my princess. 👑
Happy birthday, my heart.
Happy birthday to the girl I miss, adore, respect, and love more than words can hold.

With all my love,
<b>{him}</b> ❤️
""".strip()
