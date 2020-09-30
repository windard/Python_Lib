## tqdm

tqdm 这么有牌面的库，竟然没没有介绍？

用起来非常的简单，也非常的好用。

一个基本的实例

```
# coding=utf-8

import time
from tqdm import trange, tqdm

for i in trange(10):
    time.sleep(0.1)

for i in tqdm(range(100)):
    time.sleep(0.1)
```

一个常见的示例

```
# coding=utf-8

import time
import random
from tqdm import tqdm


count = 0
total = 1024
progress = tqdm(total=total, unit='B',unit_scale=True, desc='filename')


while count < total:
  time.sleep(1)
  step = random.randrange(100)
  count += step
  progress.update(step)

progress.close()

```

## alive-progress

也很有意思

```
>>> import alive_progress
>>> alive_progress.showtime()
Welcome to alive-progress, enjoy! (ctrl+c to stop :)
=================================
showing: preconfigured spinners, with their unknown bar renditions
--> remember you can create your own!

fps: 15.03 (goal: 15.0)
fps: 15.03 (goal: 15.0)      classic       |----------------------------------------|
                   |||       classic       ||||||||||||||||||||||||||||||||||||||||||
                |  * |        stars        |      **********                        |
                   |↓|        arrow        |↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓|
                 |↓↙←|       arrows        |↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘|
                   |▇|      vertical       |▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇|
                 |▇▅▃|        waves        |▇▅▃▁▃▅▇▇▅▃▁▃▅▇▇▅▃▁▃▅▇▇▅▃▁▃▅▇▇▅▃▁▃▅▇▇▅▃▁▃|
                 |▇▂▅|       waves2        |▇▂▅▆▁▆▅▂▇▄▃█▃▄▇▂▅▆▁▆▅▂▇▄▃█▃▄▇▂▅▆▁▆▅▂▇▄▃█|
                 |▇▂▇|       waves3        |▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂▇▂|
                   |▎|     horizontal      |▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎▎|
                   |⠄|        dots         |⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄|
                   |⣻|    dots_reverse     |⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻⣻|
               |⠄⠂⠁⠈⠐|     dots_waves      |⠄⠂⠁⠈⠐⠠⢀⡀⠄⠂⠁⠈⠐⠠⢀⡀⠄⠂⠁⠈⠐⠠⢀⡀⠄⠂⠁⠈⠐⠠⢀⡀⠄⠂⠁⠈⠐⠠⢀⡀|
               |⠄⠁⠐⢀⠄|     dots_waves2     |⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀⠄⠁⠐⢀|
                 |∙●∙|   ball_scrolling    |∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙●∙∙∙∙∙∙|
                 |∙●∙|   balls_scrolling   |∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙∙●●●●|
            |      ● |    ball_bouncing    |                    ●                   |
            |      ● |   balls_bouncing    |                                  ●●●●● |
                 |.. |     dots_recur      |      ..................................|
                |   =|      bar_recur      |    ==============================      |
               | ►►  |       pointer       |      ►►►►►►►►►►►►►►►►                  |
              | →→→  |    arrows_recur     |                          →→→→→→→→→→→→→→|
              |  ◀◀  |      triangles      |              ◀◀◀◀◀◀◀◀◀◀◀◀◀             |
        | ▷▷▷    ◀◀◀ |     triangles2      | ▷▷▷    ◀◀◀  ▶▶▶    ◁◁◁  ▷▷▷    ◀◀◀  ▶▶▶|
            |    <<< |      brackets       |                        <<<<<<<<<<<<<<< |
          |    ○○○○○ |    balls_filling    |      ●●●●●●●●●●●●●●●●●●●●              |
          |  ♫♫♫♫    |        notes        |                  ♫♫♫♫♫♫♫♫♫♫♫♫♫♫♫♫      |
          |  ♬♬♬♬    |       notes2        |  ♫♫♫♫♫♫♫♫♫♫♫♫♫♫♫♫                      |
          |      ♩♩♩♩|   notes_scrolling   |      ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪                  |
        |  >>>><<<<  |   arrows_incoming   |                  ....                  |
        |<<<<    >>>>|   arrows_outgoing   |..                                    ..|
  |    >>------>     |     real_arrow      |                           >>------>    |
     | ><(((('>      |        fish         |      ><(((('>                          |
    |.¸><(((º>       |        fish2        |·´¯`·.·´¯`·.¸¸.·´¯`·.¸><(((º>           |
  |      ><(((('>    |    fish_bouncing    |              ><(((('>                  |
  |                 <|       fishes        | <><                                    |
      |ait...        |  message_scrolling  |please wait...                          |
     |      please   |  message_bouncing   |                                  wait  |
     |longer than ant|    long_message     |his is taking longer than anticipated, h|
      |–––––√\/•–––––|        pulse        |–––––√\/•––––––––––√\/•––––––––––√\/•–––|
^C>>>
>>> alive_progress.show_bars()
Welcome to alive-progress, enjoy! (ctrl+c to stop :)
=================================
showing: preconfigured bars
--> remember you can create your own!

fps: 15.03 (goal: 15.0)
   classic [===================================>    ]

  classic2 [################........................]

    smooth |███████▉                                |

    blocks |▉▉▉▎                                    |

   bubbles <●●●●●●●●●●●●●●●●●●●●●●●●●●●●∙           >

   circles <●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●○○○○○>

    hollow <❒❒▷                                     >

   squares <■■■■■■■■■■■■■■■■■■❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒❒>

     solid <■■■■■■■■■■■■■■■■■■■■■■►                 >

    checks |✓✓                                      |

   filling |███████████████████████▅                |

^C>>>
```

