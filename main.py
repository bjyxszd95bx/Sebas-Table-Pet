import tkinter as tk
import random
import os
import sys
import subprocess
from PIL import Image, ImageTk
import json

# 本地文件
SAVE_PATH = "zy/dis/save.json"
APP_NAME = "SebasTablePet"
DEFAULT_SAVE_DATA = {
    "frog_count": 0,
    "auto_start": True,
    "auto_start_tip_shown": False
}
# ==================== 基础配置 ====================
WIDTH, HEIGHT = 70, 100
SPEED = 3
CHANGE_DIR_TIME = 3500
EDGE_MARGIN = 50
MOVE_INTERVAL = 20
IDLE_TIME = 30*1000
IDLE_ROTATE_MIN_TIME = 15 * 60 * 1000
IDLE_ROTATE_MAX_TIME = 25 * 60 * 1000
IDLE_ROTATE_TALK_CHANCE = 0.4
IDLE_ROTATE_STANDBY_PAUSE = 30 * 1000

# 样式
OUTER_BORDER = "#7f360d"
INNER_BORDER = "#c66a08"
MAIN_BG      = "#eca964"
TEXT_COLOR   = "#5c3c21"
TOTAL_FROG_COUNT = 0
# 四方向、反向映射
DIR_LIST = ["up", "down", "left", "right"]
OPPOSITE_DIR = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

DIALOGUES = [
    "假如山姆跟我一样内向的话……我们出去玩大概会从头沉默到尾。",
    "今天我有什么事可以做的？ 也许没有。",
    "情绪低落的时候，看什么都觉得很蠢；情绪高涨的时候，多么平淡的东西都会让你感到开心。",
    "怎么才能一直保持乐观呢？我不懂。……也许有一天我会明白。”",
    "下雨天让我很安心。",
    "你跟山姆是我唯一的朋友。",
    "我刚还在想你呢……",
    "我很期待寒冷潮湿的季节——也许我上辈子是一只青蛙。",
    "如果没有你的话……我大概还在碌碌无为吧。",
    "我昨晚跑进山洞被石蟹割伤了。别告诉任何人，知道吗？",
    "但愿不要吃蘑菇炖锅……",
    "到晚上温度就会舒适起来了。",
    "还好你出现了。我本来很无聊，现在好多了。",
    "住在火车道附近很有趣，总能提醒我世界很广阔。",
    "我堆了怪物雪人，德米特里厄斯拆掉了……玛鲁的小雪人就没事！",
    "小时候听到火车来就跑去看，那样的日子去哪了……？",
    "（不回应）塞巴斯蒂安好像陷入沉思……",
    "如果你什么时候想去游泳的话……我就和你一起去吧。",
    "别吧，今晚吃山洞胡萝卜卷饼？……呃……",
    "*哈欠*……我昨晚看一本书看到三点……",
    "我应该学学做饭。一定能派上大用场。",
    "有什么新闻吗？ 在今晚酒吧的台球比试上，我要大败山姆。",
    "昨夜，我看到一群蝙蝠在湖边飞过。 看来到了他们去吃蚊子的季节了？",
    "运气好的话，下雨天可能会看见青蛙。",
    "我一直感觉人生很失败，但是挑战会让我变得更强大。",
    "嗯……一旦你习惯了吃生鱼，就会很上瘾。",
    "我喜欢乘船。在旅程中，只能看到茫茫大海……",
    "有时候，能够离开电脑，看看现实世界是什么模样，还是挺不错的。我快忘了这样的感觉能够有多棒。",
    "在遇到你之前，我把自己的人生都耗费在逃避现实上……因为我觉得自己永远都得不到幸福。",
]
FROG_DIALOGUES = [
    "下雨天让我很安心。",
    "我很期待寒冷潮湿的季节——也许我上辈子是一只青蛙。",
    "我很喜欢和青蛙待在一起，这让我很安心。",
    "我刚还在想你呢……",
    "运气好的话，下雨天可能会看见青蛙。",
    "下次我们尝试能不能孵青蛙蛋吧。",
    "我喜欢乘船。在旅程中，只能看到茫茫大海……",
    "到晚上温度就会舒适起来了。",
    "昨夜，我看到一群蝙蝠在湖边飞过。 看来到了他们去吃蚊子的季节了？",
    "在遇到你之前，我把自己的人生都耗费在逃避现实上……因为我觉得自己永远都得不到幸福。",
    "我应该学学做饭。一定能派上大用场。",
    "*哈欠*……我昨晚看一本书看到三点……",
]

COMPUTER_DIALOGUES = [
    "我马上弄完。",
    "你来了。稍等一下…",
    "再等我一下，好吗？",
    "别走，我快结束了。",
    "有你在旁边还挺安心。",
    "马上，等我弄完这个模块。",
    "就差*这么*一点，就能在床上赖一整天了。要是成功了多好。"
]

IDLE_END_DIALOGUES = {
    "computer": [
        "刚刚终于把模块整理好了。",
        "代码终于跑通了。",
        "刚把工作做完。",
    ],
    "piano": [
        "刚刚练习了一会新曲。",
        "有一段总弹不好…",
        "今天的练习状态还不错。"
    ],
    "frog": [
        "刚刚和小青蛙待了一会。",
        "青蛙今天挺安静的。",
        "回来看看你在做什么。"
    ]
}

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 特殊GIF尺寸
ANIM_CONFIG = {

    # ===== 普通待机 =====
    "standby": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "idle"
    },

    # ===== 青蛙待机 =====
    "standbyFrog": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "idle"
    },
    # ===== 青蛙待机 =====
    "standbyFrogs": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "idle"
    },
    "standbyFrog3": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "idle"
    },
    "standbyFrog4": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "idle"
    },

    "standbyFrog5": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "idle"
    },

    # ===== 电脑待机 =====
    "computer": {
        "size": (86, 114),
        "anchor_x": 60,
        "anchor_y": 114,
        "emoji_x": 60,
        "emoji_y": 15,
        "type": "idle"
    },

    "piano": {
        "size": (85, 110),
        "anchor_x": 43,
        "anchor_y": 105,
        "emoji_x": 43,
        "emoji_y": 15,
        "type": "idle"
    },

    # ===== 青蛙剧情 =====
    "frog_run": {
        "size": (149, 110),
        "anchor_x": 116,
        "anchor_y": 110,
        "type": "special"
    },

    "frog_catch": {
        "size": (140, 110),
        "anchor_x": 116,
        "anchor_y": 110,
        "type": "special"
    },

    # ===== 行走 =====
    "up": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "walk"
    },

    "down": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "walk"
    },

    "left": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "walk"
    },

    "right": {
        "size": (70, 100),
        "anchor_x": 35,
        "anchor_y": 100,
        "emoji_x": 35,
        "emoji_y": 10,
        "type": "walk"
    },

    
}

IMAGE_FILES = {
    "standby": get_resource_path("zy/dis/standby.gif"),
    "click": get_resource_path("zy/dis/click.gif"),
    "computer": get_resource_path("zy/dis/computer.gif"),
    "piano": get_resource_path("zy/dis/piano.gif"),
    "standbyFrog": get_resource_path("zy/dis/frog/standbyFrog.gif"),  # <--- 新加
    "standbyFrogs": get_resource_path("zy/dis/frog/standbyFrog2.gif"),  # <--- 新加
    "standbyFrog3": get_resource_path("zy/dis/frog/standbyFrog3.gif"),  # <--- 新加
    "standbyFrog4": get_resource_path("zy/dis/frog/standbyFrog4.gif"),  # <--- 新加
    "up": get_resource_path("zy/dis/up.gif"),
    "down": get_resource_path("zy/dis/down.gif"),
    "left": get_resource_path("zy/dis/left.gif"),
    "right": get_resource_path("zy/dis/right.gif"),
    "frog_run": get_resource_path("zy/dis/frog/frogRun.gif"),
    "frog_catch": get_resource_path("zy/dis/frog/frogAnimation22.gif"),
}

EMOJI_PATHS = {
    "wenhao": get_resource_path("zy/dis/biaoq/wenhao.gif"),
    "wuyu": get_resource_path("zy/dis/biaoq/wuyu.gif"),
    "fanzao": get_resource_path("zy/dis/biaoq/fanzao.gif"),
    "liuhan": get_resource_path("zy/dis/biaoq/liuHan.gif"),
    "smile": get_resource_path("zy/dis/biaoq/smile.gif"),
    "love": get_resource_path("zy/dis/biaoq/love.gif"),
    "music": get_resource_path("zy/dis/biaoq/music.gif"),
    "game": get_resource_path("zy/dis/biaoq/game.gif"),
    "time": get_resource_path("zy/dis/biaoq/time.gif"),

}

gif_raw = {}
emoji_images = {}
emoji_gifs = {}

# 帧延迟校验配置：调整为正常播放速度（贴合常规GIF播放节奏）
MIN_FRAME_DELAY = 100    # 最小80毫秒/帧，确保播放不超速（常规正常速度）
MAX_FRAME_DELAY = 1000   # 最大200毫秒/帧，避免播放过慢卡顿
DEFAULT_FRAME_DELAY = 100  # 无延迟时默认值，贴合正常播放节奏

def load_gif_raw(path, gif_name=None):
    frames = []
    delays = []

    img = Image.open(path)
    base_canvas = (WIDTH, HEIGHT)
    config = ANIM_CONFIG.get(gif_name)

    if config:
        gif_size = config["size"]
        canvas_size = config.get("canvas", gif_size)
        anchor_x = config["anchor_x"]
        anchor_y = config["anchor_y"]

    else:
        gif_size = (WIDTH, HEIGHT)   # ← 新增这个
        canvas_size = (WIDTH, HEIGHT)
        anchor_x = WIDTH // 2
        anchor_y = HEIGHT

    try:
        while True:
            frame = img.convert("RGBA")
            # 角色真正尺寸
            real_size = gif_size

            if gif_name in ["standby", "standbyFrog"]:
                scaled = frame.resize(real_size, Image.Resampling.NEAREST)
            else:
                scaled = frame.resize(real_size, Image.Resampling.LANCZOS)

            transparent_bg = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
            x = (canvas_size[0] - scaled.width) // 2
            y = canvas_size[1] - scaled.height
            transparent_bg.paste(scaled, (x, y), scaled)
            
            # ====================
            # 调试：显示脚底锚点
            # ====================

            # from PIL import ImageDraw

            # draw = ImageDraw.Draw(transparent_bg)

            # draw.line(
            #     (anchor_x - 6, anchor_y,
            #     anchor_x + 6, anchor_y),
            #     fill="red",
            #     width=2
            # )

            # draw.line(
            #     (anchor_x, anchor_y - 6,
            #     anchor_x, anchor_y + 6),
            #     fill="red",
            #     width=2
            # )
            # ===============================

            frames.append(transparent_bg)
            # 帧延迟校验：确保所有GIF帧延迟贴合正常播放速度
            frame_delay = img.info.get("duration", DEFAULT_FRAME_DELAY)

            # 只有异常0ms才修正
            if frame_delay <= 0:
                frame_delay = DEFAULT_FRAME_DELAY

            delays.append(frame_delay)

            img.seek(img.tell() + 1)
    except EOFError:
        pass

    return frames, delays


def load_emoji_gif(self,path):

    frames = []
    delays = []

    img = Image.open(path)

    try:
        while True:

            frame = img.convert("RGBA")

            frame = frame.resize(
                (32, 32),
                Image.Resampling.NEAREST
            )

            frames.append(
                ImageTk.PhotoImage(frame)
            )

            delays.append(
                img.info.get("duration", 100)
            )

            img.seek(img.tell() + 1)

    except EOFError:
        pass

    return frames, delays


frog_mini_frames = []
frog_mini_delays = []

def preload_all_gif():


    for name, path in IMAGE_FILES.items():

      
        gif_raw[name] = load_gif_raw(path, name)

# 存青蛙次数，加载本地存储
def load_save():
    default_data = DEFAULT_SAVE_DATA.copy()
    if not os.path.exists(SAVE_PATH):
        return default_data
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        default_data.update(data)
        return default_data
    except:
        return default_data

# 存青蛙次数，本地存储
def save_data(data):
    save_dir = os.path.dirname(SAVE_PATH)
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    save_data_obj = load_save()
    save_data_obj.update(data)

    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(save_data_obj, f, ensure_ascii=False, indent=2)

def get_startup_shortcut_path():
    startup_dir = os.path.join(
        os.environ.get("APPDATA", ""),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup"
    )
    return os.path.join(startup_dir, f"{APP_NAME}.lnk")

def get_app_launch_info():
    if getattr(sys, "frozen", False):
        return sys.executable, "", os.path.dirname(sys.executable)

    script_path = os.path.abspath(sys.argv[0])
    return sys.executable, f'"{script_path}"', os.path.dirname(script_path)

def powershell_quote(text):
    return "'" + text.replace("'", "''") + "'"

def register_auto_start():
    if os.name != "nt":
        return False

    shortcut_path = get_startup_shortcut_path()
    startup_dir = os.path.dirname(shortcut_path)
    os.makedirs(startup_dir, exist_ok=True)

    target_path, arguments, working_dir = get_app_launch_info()
    command = (
        "$shell = New-Object -ComObject WScript.Shell; "
        f"$shortcut = $shell.CreateShortcut({powershell_quote(shortcut_path)}); "
        f"$shortcut.TargetPath = {powershell_quote(target_path)}; "
        f"$shortcut.Arguments = {powershell_quote(arguments)}; "
        f"$shortcut.WorkingDirectory = {powershell_quote(working_dir)}; "
        "$shortcut.Save()"
    )

    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                command
            ],
            check=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        return True
    except Exception:
        return False

def unregister_auto_start():
    if os.name != "nt":
        return False

    shortcut_path = get_startup_shortcut_path()
    try:
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        return True
    except Exception:
        return False

def supports_auto_start():
    return os.name == "nt"

# ==================== 主程序 ====================
class SebPet(tk.Tk):
    def __init__(self):
        super().__init__()
        self.walk_frog_used = False
        save = load_save()
        self.total_frog_caught = save["frog_count"]
        self.auto_start = save["auto_start"]
        self.auto_start_tip_shown = save["auto_start_tip_shown"]
        self.cur_width = WIDTH
        self.cur_height = HEIGHT
        
        # ========== 核心：全局纯透明 ==========
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.TRANS = "#000001"
        self.config(bg=self.TRANS)
        self.wm_attributes("-transparentcolor", self.TRANS)
        self.geometry(f"{WIDTH}x{HEIGHT}")

        self.load_emoji_images()
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.x = random.randint(200, self.screen_w - 300)
        self.y = random.randint(200, self.screen_h - 300)
        self.geometry(f"+{self.x}+{self.y}")

        self.walk_active = False
        self.frog_seen = False
        self.frog_caught = False
        self.last_walk_event_check = self.call("clock", "milliseconds")
        self.walk_event_cooldown = 1000*60 * 1   # 散步随机事件
        self.walk_event_playing = False
        self.force_anim = None
        self.mouse_hover = False
        self.hover_start_time = None    # 鼠标悬浮人物开始时间
        self.menu_open = False
        self.talking = False
        self.dragging = False
        self.ani_timer = None
        self.anim_version = 0
        self.click_count = 0
        self.click_timer = None
        self.emoji_win = None
        self.emoji_timer = None
        self.chat_timer = None
        self.author_timer = None
        self.cur_dir = random.choice(DIR_LIST)
        self.last_dir_change = self.call("clock", "milliseconds")
        self.in_computer = False
        self.next_idle_rotate_time = None
        self.idle_rotation_pending = False
        self.last_active = self.call("clock", "milliseconds")

        self.DRAG_THRESHOLD = 6  # 你可以改成 5~12 之间试手感

        self.gif = {}
        for key in gif_raw:
            fs, ds = gif_raw[key]
            self.gif[key] = ([ImageTk.PhotoImage(f) for f in fs], ds)

        
        self.frame_idx = 0

        # ========== 关键：Label 背景透明 ==========
        self.label = tk.Label(self, bg=self.TRANS, bd=0)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)

        self.set_anim("standby")

        self.label.bind("<ButtonPress-1>", self.on_press)
        self.label.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<B1-Motion>", self.do_drag)
        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)
        self.label.bind("<Button-3>", self.show_menu)

        # 菜单
        self.menu_w = 130
        self.menu_button_h = 28
        self.menu_h = 0
        self.menu_buttons = []
        self.right_menu = tk.Toplevel(self)
        self.right_menu.overrideredirect(True)
        self.right_menu.wm_attributes("-topmost", True)
        self.right_menu.config(bg=self.TRANS)
        self.right_menu.wm_attributes("-transparentcolor", self.TRANS)
        self.right_menu.geometry(f"{self.menu_w}x{self.menu_h}")
        self.right_menu.withdraw()

        c = tk.Frame(self.right_menu, bg=MAIN_BG)

        btn = {"font":("微软雅黑",10), "bg":MAIN_BG, "fg":TEXT_COLOR, "bd":0, "relief":tk.FLAT, "anchor":"w"}
        self.b1 = tk.Button(c, text="💬 聊聊天", command=self.start_talk,** btn)
        self.b2 = tk.Button(c, text="🚶 散散步", command=self.start_walk, **btn)
        self.b3 = tk.Button(c, text="🛑 休息下", command=self.stop_walk,** btn)
        self.b4 = tk.Button(c, text="😊 没事啦", command=self.hide_menu, **btn)
        self.b6 = tk.Button(c, text="❌ 退出程序", command=self.quit,** btn)
        self.b5 = tk.Button(c, text="📌 关于我", command=self.show_author,** btn)
        self.b7 = tk.Button(c, text="", command=self.toggle_auto_start, **btn)

        self.menu_buttons = [
            self.b1,
            self.b2,
            self.b3,
            self.b4,
            self.b5,
            self.b6
        ]
        if supports_auto_start():
            self.menu_buttons.insert(-1, self.b7)
        self.menu_button_count = len(self.menu_buttons)
        self.menu_h = self.menu_button_count * self.menu_button_h + 14
        self.right_menu.geometry(f"{self.menu_w}x{self.menu_h}")
        tk.Frame(self.right_menu, bg=OUTER_BORDER).place(x=0,y=0,w=self.menu_w,h=self.menu_h)
        tk.Frame(self.right_menu, bg=INNER_BORDER).place(x=4,y=4,w=self.menu_w-8,h=self.menu_h-8)
        c.place(x=7,y=7,w=self.menu_w-14,h=self.menu_h-14)
        c.lift()

        for idx, button in enumerate(self.menu_buttons):
            button.place(x=0, y=self.menu_button_h * idx, h=self.menu_button_h)

        self.update_auto_start_button()

        for b in self.menu_buttons:
            b.bind("<Enter>", lambda e,btn=b: btn.config(bg="#d89a50"))
            b.bind("<Leave>", lambda e,btn=b: btn.config(bg=MAIN_BG))

        self.chat_win = None
        self.chat_height = 70
        self.hover_tip_win = None
        self.sync_auto_start_on_launch()
        self.switch_anim()
        self.move_loop()
        self.idle_loop()
    
    def reload_standby_frog(self):
        frames, delays = load_gif_raw(
            IMAGE_FILES["standbyFrog"],
            "standbyFrog"
        )

        self.gif["standbyFrog"] = (
            [ImageTk.PhotoImage(f) for f in frames],
            delays
        )

    def get_frog_idle_anim(self):
        if self.total_frog_caught <= 1:
            return "standbyFrog"
        if self.total_frog_caught == 2:
            return "standbyFrogs"
        if self.total_frog_caught == 3:
            return "standbyFrog3"
        return "standbyFrog4"

    def get_idle_types(self):
        idle_types = ["computer", "piano"]

        if self.total_frog_caught > 0:
            idle_types.append("frog")

        return idle_types

    def pick_idle_type(self, exclude_type=None):
        idle_types = self.get_idle_types()
        candidates = [t for t in idle_types if t != exclude_type]

        if not candidates:
            candidates = idle_types

        return random.choice(candidates)

    def schedule_next_idle_rotation(self):
        now = self.call("clock", "milliseconds")
        delay = random.randint(int(IDLE_ROTATE_MIN_TIME), int(IDLE_ROTATE_MAX_TIME))
        self.next_idle_rotate_time = now + delay

    def enter_idle_type(self, idle_type, from_rotation=False):
        if from_rotation and not self.idle_rotation_pending:
            return

        if self.walk_active or self.talking or self.dragging or self.menu_open:
            return

        self.idle_rotation_pending = False
        self.in_computer = True
        self.current_idle_type = idle_type
        self.schedule_next_idle_rotation()
        self.switch_anim()

    def rotate_idle_type(self):
        if not self.in_computer or not hasattr(self, 'current_idle_type'):
            return

        old_idle_type = self.current_idle_type
        new_idle_type = self.pick_idle_type(exclude_type=old_idle_type)
        should_talk = random.random() < IDLE_ROTATE_TALK_CHANCE

        self.in_computer = False
        self.next_idle_rotate_time = None
        self.idle_rotation_pending = True
        self.set_anim("standby")
        
        if should_talk:
            text = random.choice(IDLE_END_DIALOGUES.get(old_idle_type, []))
            if text:
                close_delay = 3600
                self.talking = True
                self.show_chat_custom(text, close_delay=close_delay)
                self.after(
                    close_delay + IDLE_ROTATE_STANDBY_PAUSE,
                    lambda idle_type=new_idle_type: self.enter_idle_type(
                        idle_type,
                        from_rotation=True
                    )
                )
                return
        else:
            self.show_emoji("wuyu")
        self.after(
            IDLE_ROTATE_STANDBY_PAUSE,
            lambda idle_type=new_idle_type: self.enter_idle_type(
                idle_type,
                from_rotation=True
            )
        )
        
    def set_anim(self, anim_name):
        self.current_anim_name = anim_name
        config = ANIM_CONFIG.get(anim_name)

        if config:
            self.cur_width, self.cur_height = config.get(
                "canvas",
                config["size"]
            )
        else:
            self.cur_width, self.cur_height = (WIDTH, HEIGHT)

        self.geometry(
            f"{self.cur_width}x{self.cur_height}+{self.x}+{self.y}"
        )

        self.cur_frames, self.cur_delays = self.gif[anim_name]
        self.frame_idx = 0

        if self.cur_frames:
            self.label.config(image=self.cur_frames[0])

    def load_emoji_images(self):

        size = (32, 32)

        for key, path in EMOJI_PATHS.items():

            # GIF
            if path.lower().endswith(".gif"):

                emoji_gifs[key] = self.load_emoji_gif(path)

            # 静态图
            else:

                im = Image.open(path).resize(
                    size,
                    Image.Resampling.NEAREST
                )

                emoji_images[key] = ImageTk.PhotoImage(im)

    # 播放gif表情
    def play_emoji_gif(
        self,
        lbl,
        frames,
        delays,
        idx=0
    ):

        if not self.emoji_win:
            return

        if not self.emoji_win.winfo_exists():
            return

        # 新增
        if not lbl.winfo_exists():
            return

        lbl.config(
            image=frames[idx]
        )

        next_idx = (
            idx + 1
        ) % len(frames)

        self.after(
            delays[idx],
            lambda: self.play_emoji_gif(
                lbl,
                frames,
                delays,
                next_idx
            )
        )

    # ==================== 点击计数 + 表情 ====================
    def reset_click_count(self):
        self.click_count = 0
        if self.click_timer is not None:
            self.after_cancel(self.click_timer)
            self.click_timer = None

    def on_press(self, e):
        # 仅重置活跃时间，不关闭待机，不切动画
        self.last_active = self.call("clock", "milliseconds")

        self.drag_start_x = e.x_root
        self.drag_start_y = e.y_root
        # 新增：无论是否待机，都初始化dx、dy（解决拖拽报错）
        self.dx, self.dy = e.x, e.y
        self.dragging = False

    def handle_click(self):
        if self.in_computer:
            self.click_count += 1
            if self.click_timer:
                self.after_cancel(self.click_timer)
            # self.click_timer = self.after(500, self.detect_click_pattern)
            behavior_roll = random.random()
            if self.current_idle_type == 'computer':
                self.start_talk(COMPUTER_DIALOGUES)
            elif self.current_idle_type == 'piano':
                self.show_emoji("music")
            else:
                if behavior_roll < 0.5:
                    self.show_emoji("smile")
                else:
                    self.start_talk(FROG_DIALOGUES)

            return

        self.click_count += 1
        if self.click_timer:
            self.after_cancel(self.click_timer)
        self.click_timer = self.after(500, self.detect_click_pattern)

    def detect_click_pattern(self):
        cnt = self.click_count
        if cnt == 1:
            self.show_emoji("smile")
        elif cnt == 2:
            self.show_emoji("wenhao")
        else:
            self.show_emoji("wuyu")
        self.reset_click_count()

    def show_emoji(self, emoji_key):
        self.hide_emoji()
        wnd = tk.Toplevel(self)
        wnd.overrideredirect(True)
        wnd.wm_attributes("-topmost", True)
        wnd.config(bg=self.TRANS)
        wnd.wm_attributes("-transparentcolor", self.TRANS)
        self.emoji_win = wnd
        lbl = tk.Label(
            wnd,
            bg=self.TRANS
        )


        # GIF
        if emoji_key in emoji_gifs:

            frames, delays = emoji_gifs[emoji_key]

            self.play_emoji_gif(
                lbl,
                frames,
                delays
            )

        # 静态图
        else:

            lbl.config(
                image=emoji_images[emoji_key]
            )
        lbl.pack()
        self.update_emoji_position()
        self.emoji_timer = self.after(2000, self.hide_emoji)
    

    # gif表情
    def load_emoji_gif(self, path):

        frames = []
        delays = []

        img = Image.open(path)

        try:
            while True:

                frame = img.convert("RGBA")

                frame = frame.resize(
                    (32, 32),
                    Image.Resampling.NEAREST
                )

                frames.append(
                    ImageTk.PhotoImage(frame)
                )

                delays.append(
                    img.info.get("duration", 100)
                )

                img.seek(img.tell() + 1)

        except EOFError:
            pass

        return frames, delays

    def hide_emoji(self):
        try:
            if self.emoji_win:
                self.emoji_win.destroy()
        except:
            pass
        self.emoji_win = None
        if self.emoji_timer:
            self.after_cancel(self.emoji_timer)
            self.emoji_timer = None

    def update_emoji_position(self):
        if self.emoji_win and self.emoji_win.winfo_exists():

            config = ANIM_CONFIG.get(
                self.current_anim_name,
                {}
            )

            emoji_x = config.get(
                "emoji_x",
                self.cur_width // 2
            )

            emoji_y = config.get(
                "emoji_y",
                0
            )

            ex = self.x + emoji_x - 16
            ey = self.y + emoji_y - 32

            self.emoji_win.geometry(f"+{ex}+{ey}")

    # ==================== 拖动分离 ====================
    def get_walk_hover_tip_text(self):
        if self.frog_caught:
            return "🐸 抓到了"

        if not self.frog_seen and not self.frog_caught:
            return "本次散步：🐸 * 0"

        if self.frog_seen and not self.frog_caught:
            return "刚刚遇到了小青蛙..."

        return ""

    def show_walk_hover_tip(self):
        if not self.walk_active:
            return

        self.hide_walk_hover_tip()

        text = self.get_walk_hover_tip_text()
        if not text:
            return

        tip_w = 130
        tip_h = 34

        wnd = tk.Toplevel(self)
        wnd.overrideredirect(True)
        wnd.wm_attributes("-topmost", True)
        wnd.config(bg=self.TRANS)
        wnd.wm_attributes("-transparentcolor", self.TRANS)

        self.hover_tip_win = wnd

        tk.Frame(wnd, bg=OUTER_BORDER).place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Frame(wnd, bg=INNER_BORDER).place(relx=0.03, rely=0.09, relwidth=0.94, relheight=0.82)
        content = tk.Frame(wnd, bg=MAIN_BG)
        content.place(relx=0.07, rely=0.16, relwidth=0.86, relheight=0.68)

        lbl = tk.Label(
            content,
            text=text,
            font=("微软雅黑", 9),
            fg=TEXT_COLOR,
            bg=MAIN_BG,
            bd=0
        )
        lbl.pack(expand=True, fill="both")

        self.update_walk_hover_tip_position(tip_w, tip_h)

    def hide_walk_hover_tip(self):
        try:
            if self.hover_tip_win and self.hover_tip_win.winfo_exists():
                self.hover_tip_win.destroy()
        except:
            pass

        self.hover_tip_win = None

    def update_walk_hover_tip_position(self, tip_w=None, tip_h=None):
        if self.hover_tip_win and self.hover_tip_win.winfo_exists():
            self.hover_tip_win.update_idletasks()

            if tip_w is None:
                tip_w = self.hover_tip_win.winfo_width()
            if tip_h is None:
                tip_h = self.hover_tip_win.winfo_height()

            tx = self.x + self.cur_width // 2 - tip_w // 2
            ty = self.y + self.cur_height + 4

            self.hover_tip_win.geometry(f"{tip_w}x{tip_h}+{tx}+{ty}")

    def do_drag(self, e):
        move_x = abs(e.x_root - self.drag_start_x)
        move_y = abs(e.y_root - self.drag_start_y)

        # 只有超过阈值才算真正拖拽
        if not self.dragging:
            if move_x < self.DRAG_THRESHOLD and move_y < self.DRAG_THRESHOLD:
                return
            self.dragging = True
            self.reset_click_count()
            self.hide_emoji()
            self.switch_anim()

        self.x = self.winfo_pointerx() - self.dx
        self.y = self.winfo_pointery() - self.dy
        self.geometry(f"+{self.x}+{self.y}")
        self.update_emoji_position()

    def on_release(self, e):
        was_dragging = self.dragging

        if was_dragging:
            self.dragging = False
            # 关键修改：待机状态（in_computer，对应computer/standbyFrog）拖动结束后，切换为standby
            if self.in_computer:
                # 退出待机状态，移除待机动画标识，确保切换为standby
                self.in_computer = False
                self.next_idle_rotate_time = None
                self.idle_rotation_pending = False
                if hasattr(self, 'current_idle_type'):
                    del self.current_idle_type
                # 强制切换为standby动画，避免受其他状态影响
                self.set_anim("standby")
                self.frame_idx = 0
                if self.cur_frames:
                    self.label.config(image=self.cur_frames[0])
                self.ani_loop()
            else:
                # 非待机状态，执行原有切换逻辑
                self.switch_anim()
        else:
            self.handle_click()
        self.update_emoji_position()

    def reset_idle(self):
        self.last_active = self.call("clock", "milliseconds")
        self.idle_rotation_pending = False
        if self.in_computer:
            self.in_computer = False
            self.next_idle_rotate_time = None
            self.switch_anim()

    def on_enter(self, e):
        self.mouse_hover = True
        # 记录开始悬浮时间
        if self.walk_active:
            self.hover_start_time = self.call("clock", "milliseconds")
            self.show_walk_hover_tip()
        self.switch_anim()

    def on_leave(self, e):
        # ===== 散步时：补偿悬浮时间 =====
        if self.walk_active and self.hover_start_time is not None:

            now = self.call("clock", "milliseconds")

            hover_duration = now - self.hover_start_time

            # 关键：把hover时间加回去
            self.last_walk_event_check += hover_duration

            self.hover_start_time = None

        self.mouse_hover = False

        self.hide_walk_hover_tip()
        self.switch_anim()

    def switch_anim(self):
        if self.force_anim is not None:
            # 🔥 特殊动画播放期间，直接忽略 hover / standby 切换
            config = ANIM_CONFIG.get(self.force_anim)
            if config:
                self.cur_width, self.cur_height = config["size"]

            self.cur_frames, self.cur_delays = self.gif[self.force_anim]

            if self.frame_idx >= len(self.cur_frames):
                self.frame_idx = len(self.cur_frames) - 1

            self.label.config(image=self.cur_frames[self.frame_idx])
            self.ani_loop()
            return
        new_anim = None
        if self.force_anim is not None:
            config = ANIM_CONFIG.get(self.force_anim)
            if config:
                self.cur_width, self.cur_height = config["size"]
            else:
                self.cur_width, self.cur_height = (WIDTH, HEIGHT)
            
            self.cur_frames, self.cur_delays = self.gif[self.force_anim]
            self.frame_idx = 0
            if self.cur_frames:
                self.label.config(image=self.cur_frames[0])
            self.ani_loop()
            return
            
        self.anim_version += 1

        if self.ani_timer is not None:
            self.after_cancel(self.ani_timer)
            self.ani_timer = None

        if self.dragging:
            
            self.set_anim("click")
        elif self.in_computer:
            # 进入待机后 只使用一次随机 不会因为鼠标悬浮重新刷新
            if not hasattr(self, 'current_idle_type'):
                # 新增： "rain_idle" 只需IDLE_TYPES.append("rain_idle")

                self.current_idle_type = self.pick_idle_type()

            if self.current_idle_type == "frog":
                self.set_anim(self.get_frog_idle_anim())
            else:
                self.set_anim(self.current_idle_type)
        elif self.talking:
            # ===== 电脑待机状态下 =====
            if self.in_computer:
                print("电脑待机状态下2")
                # 保持原待机动画
                if self.current_idle_type == "frog":
                    self.set_anim(self.get_frog_idle_anim())
                else:
                    self.set_anim(self.current_idle_type)

            else:
                self.set_anim("standby")

        elif (self.menu_open or self.mouse_hover) and not self.in_computer:
            self.set_anim("standby")
        elif self.walk_active:
            self.set_anim(self.cur_dir)
        else:
            self.set_anim("standby")
        self.frame_idx = 0
        if self.cur_frames:
            self.label.config(image=self.cur_frames[0])
        self.ani_loop()

    def show_menu(self, e):
        self.reset_idle()
        self.reset_click_count()
        self.hide_emoji()
        self.menu_open = True
        self.update_auto_start_button()
        self.right_menu.geometry(f"+{e.x_root}+{e.y_root}")
        self.right_menu.deiconify()
        self.right_menu.focus_set()
        self.right_menu.bind("<FocusOut>", lambda x: self.hide_menu())
        self.switch_anim()

    def hide_menu(self):
        self.right_menu.withdraw()
        self.menu_open = False
        self.switch_anim()

    def update_auto_start_button(self):
        if not supports_auto_start():
            return

        if self.auto_start:
            self.b7.config(text="🚫 关闭自动开机")
        else:
            self.b7.config(text="✅ 开启自动开机")

    def set_auto_start(self, enabled):
        if not supports_auto_start():
            return

        if enabled:
            register_auto_start()
        else:
            unregister_auto_start()

        self.auto_start = enabled
        should_show_tip = self.auto_start and not self.auto_start_tip_shown
        if should_show_tip:
            self.auto_start_tip_shown = True

        save_data({
            "auto_start": self.auto_start,
            "auto_start_tip_shown": self.auto_start_tip_shown
        })
        self.update_auto_start_button()

        if should_show_tip:
            self.after(300, self.show_auto_start_tip)

    def toggle_auto_start(self):
        if not supports_auto_start():
            return

        self.set_auto_start(not self.auto_start)

    def sync_auto_start_on_launch(self):
        if not supports_auto_start():
            return

        if self.auto_start:
            register_auto_start()
            if not self.auto_start_tip_shown:
                self.auto_start_tip_shown = True
                save_data({
                    "auto_start": self.auto_start,
                    "auto_start_tip_shown": self.auto_start_tip_shown
                })
                self.after(800, self.show_auto_start_tip)
        else:
            unregister_auto_start()

    def show_auto_start_tip(self):
        self.talking = True
        self.switch_anim()
        self.show_chat_custom(
            "我会在开机后自动出现，可以在菜单里关闭。",
            close_delay=4200
        )

    def start_walk(self):
        self.walk_frog_used = False
        self.frog_seen = False
        self.frog_caught = False
        self.walk_caught_frog = False
        self.hide_menu()
        self.reset_idle()
        self.talking = False
        self.walk_active = True
        self.cur_dir = random.choice(DIR_LIST)
        # 关键修改：每次点击散散步，重置随机事件相关时间和状态，避免刚启动就触发事件
        self.last_walk_event_check = self.call("clock", "milliseconds")  # 重置事件检查时间
        self.walk_event_playing = False  # 重置事件播放状态
        self.last_dir_change = self.call("clock", "milliseconds")  # 重置方向切换时间
        self.switch_anim()

    def stop_walk(self):

        self.hide_menu()
        self.reset_idle()

        self.walk_active = False
        self.hide_walk_hover_tip()

        # ====================
        # 青蛙散步分享
        # ====================

        # 抓到青蛙
        if self.walk_frog_used:

            self.talking = True
            self.switch_anim()
            self.show_emoji("love")
            self.show_chat_custom(
                "刚刚遇到一只小青蛙，我想收养它，可以吗？",
                close_delay=4500
            )

        # 只是遇到青蛙
        elif self.frog_seen and not self.walk_frog_used:

            self.talking = True
            self.switch_anim()
            self.show_emoji("smile")
            self.show_chat_custom(
                "散步的时候我看到了一只小青蛙。",
                close_delay=4000
            )

        else:
            self.switch_anim()

    def get_forbid_dirs(self):
        forbid = []
        if self.x <= EDGE_MARGIN: forbid.append("left")
        if self.x >= self.screen_w - self.cur_width - EDGE_MARGIN: forbid.append("right")
        if self.y <= EDGE_MARGIN: forbid.append("up")
        if self.y >= self.screen_h - self.cur_height - EDGE_MARGIN: forbid.append("down")
        return forbid

    def pick_new_dir(self):
        forbid = self.get_forbid_dirs()
        forbid.append(OPPOSITE_DIR[self.cur_dir])
        can_go = [d for d in DIR_LIST if d not in forbid]
        if not can_go:
            forbid = self.get_forbid_dirs()
            can_go = [d for d in DIR_LIST if d not in forbid]
        if not can_go: can_go = DIR_LIST
        return random.choice(can_go)

    # ==================== 开始特殊动画 ====================
    def start_special_anim(self, anim_name):

        self.walk_event_playing = True
        self.force_anim = anim_name

        self.saved_x = self.x
        self.saved_y = self.y
        self.saved_w = self.cur_width
        self.saved_h = self.cur_height

        config = ANIM_CONFIG[anim_name]

        new_w, new_h = config["size"]

        new_anchor_x = config["anchor_x"]
        new_anchor_y = config["anchor_y"]

        old_anchor_x = WIDTH // 2
        old_anchor_y = HEIGHT

        # 让脚底位置保持一致
        world_anchor_x = self.x + old_anchor_x
        world_anchor_y = self.y + old_anchor_y

        self.x = world_anchor_x - new_anchor_x
        self.y = world_anchor_y - new_anchor_y

        self.cur_width = new_w
        self.cur_height = new_h

        self.geometry(
            f"{self.cur_width}x{self.cur_height}+{self.x}+{self.y}"
        )

        self.switch_anim()

        total_time = sum(self.cur_delays)

        self.after(total_time, self.end_special_anim)

    # ==================== 结束特殊动画 ====================
    def end_special_anim(self):

        self.walk_event_playing = False
        self.force_anim = None

        self.x = self.saved_x
        self.y = self.saved_y

        self.cur_width = self.saved_w
        self.cur_height = self.saved_h

        self.geometry(
            f"{self.cur_width}x{self.cur_height}+{self.x}+{self.y}"
        )

        self.switch_anim()
    
    # ==================== 青蛙剧情 ====================
    def start_frog_story(self):

        # ---------- 第一次：看到青蛙 ----------
        frog_roll = random.random()
        if not self.frog_seen and frog_roll < 0.6:

            self.frog_seen = True

            self.start_special_anim("frog_run")

           
        # ---------- 第二次：抓到青蛙 ----------
        else:

            self.walk_frog_used = True
            self.frog_caught = True
            
            self.total_frog_caught += 1
            save_data({
                "frog_count": self.total_frog_caught
            })

            # 🔥关键：强制刷新 standbyFrog 动画缓存
            self.reload_standby_frog()

            self.start_special_anim("frog_catch")
           

    # ==================== 停下来事件（可复用） ====================
    def pause_walk_event(self, duration=3000, emoji="wenhao", callback=None):
        """
        duration: 停留时间（毫秒）
        emoji: 表情key
        callback: 停完后执行的函数
        """

        self.walk_event_playing = True

        # 切 standby
        self.set_anim("standby")
        self.frame_idx = 0

        if self.cur_frames:
            self.label.config(image=self.cur_frames[0])

        # 播放standby动画
        if self.ani_timer is not None:
            self.after_cancel(self.ani_timer)

        self.ani_loop()

        # 冒泡
        if emoji:
            self.show_emoji(emoji)

        # 结束恢复
        def finish_pause():
            self.walk_event_playing = False

            if callback:
                callback()
            else:
                self.switch_anim()

        self.after(duration, finish_pause)
    
    def move_loop(self):
        now = self.call("clock", "milliseconds")
        if not self.menu_open and not self.talking and not self.dragging:
            if self.walk_active and not self.mouse_hover:
                if self.walk_event_playing:
                    self.after(MOVE_INTERVAL, self.move_loop)
                    return
                    
                if now - self.last_walk_event_check >= self.walk_event_cooldown:
                    self.last_walk_event_check = now
                    frog_roll = random.random()
                    frog_chance = max(0.2, 0.6 - self.total_frog_caught * 0.15)

                    if not self.walk_frog_used and frog_roll < frog_chance:
                        self.pause_walk_event(
                            duration=3000,
                            emoji="wenhao",
                            callback=self.start_frog_story
                        )
                        
                    else:
                        behavior_roll = random.random()
                        if behavior_roll < 0.4:
                            self.walk_event_playing = True
                            self.set_anim("standby")
                            self.frame_idx = 0
                            self.label.config(image=self.cur_frames[0])
                            self.show_emoji("wuyu")
                            if self.ani_timer is not None:
                                self.after_cancel(self.ani_timer)
                            self.ani_loop()
                            def resume_walk():
                                self.walk_event_playing = False
                                self.switch_anim()
                            self.after(5000, resume_walk)
                        elif behavior_roll < 0.8:
                            self.show_emoji("liuhan")

                forbid = self.get_forbid_dirs()
                if self.cur_dir in forbid:
                    self.cur_dir = self.pick_new_dir()
                    self.last_dir_change = now
                    self.switch_anim()
                elif now - self.last_dir_change >= CHANGE_DIR_TIME:
                    self.cur_dir = self.pick_new_dir()
                    self.last_dir_change = now
                    self.switch_anim()

                if not self.walk_event_playing:
                    if self.cur_dir == "up": self.y -= SPEED
                    elif self.cur_dir == "down": self.y += SPEED
                    elif self.cur_dir == "left": self.x -= SPEED
                    elif self.cur_dir == "right": self.x += SPEED

                    self.x = max(EDGE_MARGIN, min(self.screen_w - self.cur_width - EDGE_MARGIN, self.x))
                    self.y = max(EDGE_MARGIN, min(self.screen_h - self.cur_height - EDGE_MARGIN, self.y))
                    self.geometry(f"{self.cur_width}x{self.cur_height}+{self.x}+{self.y}")
                    
        self.update_emoji_position()
        self.update_walk_hover_tip_position()
        if self.chat_win is not None and self.chat_win.winfo_exists():
            self.chat_win.geometry(f"230x{self.chat_height}+{self.x-50}+{self.y+HEIGHT+5}")
        self.after(MOVE_INTERVAL, self.move_loop)

    def ani_loop(self, version=None):
        if version is None:
            version = self.anim_version

        # 如果版本不同，说明这个动画已经过期
        if version != self.anim_version:
            return
        if not self.cur_frames:
            self.ani_timer = self.after(100, self.ani_loop)
            return
        frame = self.cur_frames[self.frame_idx]
        self.label.config(image=frame)
        delay = self.cur_delays[self.frame_idx]

        if self.force_anim in ["frog_run", "frog_catch"]:
            if self.frame_idx >= len(self.cur_frames) - 1: return
            self.frame_idx += 1
        else:
            self.frame_idx = (self.frame_idx + 1) % len(self.cur_frames)
        self.ani_timer = self.after(delay, lambda: self.ani_loop(version))

    def idle_loop(self):
        now = self.call("clock", "milliseconds")
        if not self.walk_active and not self.talking and not self.dragging and not self.menu_open:
            if not self.mouse_hover and now - self.last_active >= IDLE_TIME:
                if self.idle_rotation_pending:
                    pass
                elif not self.in_computer:
                    # 每次进入待机 重新随机一次
                    if hasattr(self, 'current_idle_type'):
                        del self.current_idle_type
                    self.in_computer = True
                    self.schedule_next_idle_rotation()
                    self.switch_anim()
                elif self.next_idle_rotate_time is not None and now >= self.next_idle_rotate_time:
                    self.rotate_idle_type()
        self.after(500, self.idle_loop)

    def start_talk(self,dialogues = DIALOGUES):
        if self.in_computer:
            # self.reset_idle()
            # self.reset_click_count()
            if self.chat_timer: self.after_cancel(self.chat_timer)
            if self.author_timer: self.after_cancel(self.author_timer)
            if self.chat_win and self.chat_win.winfo_exists(): self.chat_win.destroy()
            self.show_chat(random.choice(dialogues))
        else:
            self.hide_menu()
            self.reset_idle()
            self.reset_click_count()
            self.hide_emoji()
            if self.chat_timer: self.after_cancel(self.chat_timer)
            if self.author_timer: self.after_cancel(self.author_timer)
            if self.chat_win and self.chat_win.winfo_exists(): self.chat_win.destroy()
            self.walk_active = False
            self.talking = True
            self.switch_anim()
            self.show_chat(random.choice(dialogues))
    
    

    def show_author(self):
        self.hide_menu()
        self.reset_idle()
        self.reset_click_count()
        self.hide_emoji()
        if self.chat_timer: self.after_cancel(self.chat_timer)
        if self.author_timer: self.after_cancel(self.author_timer)
        if self.chat_win and self.chat_win.winfo_exists(): self.chat_win.destroy()
        self.talking = True
        self.switch_anim()
        text = "你在找这个？\n我确实来自小红书的 爱吃胡萝卜🥕\n不过现在，我面对的是你。\n至于之后……不会一直是现在这样。\n说不定哪天，我会骑上摩托——带你去兜一圈。"
        self.show_chat_custom(text, close_delay=6000)

    def show_chat_custom(self, text, close_delay=4000):
        base_w = 230
        min_h = 70
        temp_label = tk.Label(self, font=("微软雅黑", 10), wraplength=190)
        temp_label.config(text=text)
        temp_label.update_idletasks()
        req_h = temp_label.winfo_reqheight()
        temp_label.destroy()
        self.chat_height = max(min_h, req_h + 20)

        wnd = tk.Toplevel(self)
        wnd.overrideredirect(True)
        wnd.wm_attributes("-topmost", 1)
        wnd.config(bg=self.TRANS)
        wnd.wm_attributes("-transparentcolor", self.TRANS)
        geo = f"{base_w}x{self.chat_height}+{self.x-50}+{self.y+HEIGHT+5}"
        wnd.geometry(geo)
        self.chat_win = wnd

        tk.Frame(wnd, bg=OUTER_BORDER).place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Frame(wnd, bg=INNER_BORDER).place(relx=0.02, rely=0.03, relwidth=0.96, relheight=0.94)
        content = tk.Frame(wnd, bg=MAIN_BG)
        content.place(relx=0.06, rely=0.07, relwidth=0.88, relheight=0.86)
        lbl = tk.Label(content, text=text, font=("微软雅黑", 10), fg=TEXT_COLOR, bg=MAIN_BG, wraplength=190, justify="left")
        lbl.pack(anchor="w", padx=4, pady=2, expand=True, fill="both")
        self.author_timer = self.after(close_delay, self.close_author_chat)

    def close_author_chat(self):
        try:
            if self.chat_win: self.chat_win.destroy()
        except: pass
        self.author_timer = None
        self.talking = False
        self.switch_anim()

    def show_chat(self, text):
        base_w = 230
        min_h = 70
        temp_label = tk.Label(self, font=("微软雅黑", 10), wraplength=190)
        temp_label.config(text=text)
        temp_label.update_idletasks()
        req_h = temp_label.winfo_reqheight()
        temp_label.destroy()
        self.chat_height = max(min_h, req_h + 20)

        wnd = tk.Toplevel(self)
        wnd.overrideredirect(True)
        wnd.wm_attributes("-topmost", 1)
        wnd.config(bg=self.TRANS)
        wnd.wm_attributes("-transparentcolor", self.TRANS)
        geo = f"{base_w}x{self.chat_height}+{self.x-50}+{self.y+HEIGHT+5}"
        wnd.geometry(geo)
        self.chat_win = wnd

        tk.Frame(wnd, bg=OUTER_BORDER).place(relx=0, rely=0, relwidth=1, relheight=1)
        tk.Frame(wnd, bg=INNER_BORDER).place(relx=0.02, rely=0.03, relwidth=0.96, relheight=0.94)
        content = tk.Frame(wnd, bg=MAIN_BG)
        content.place(relx=0.06, rely=0.07, relwidth=0.88, relheight=0.86)
        lbl = tk.Label(content, text="", font=("微软雅黑", 10), fg=TEXT_COLOR, bg=MAIN_BG, wraplength=190, justify="left")
        lbl.pack(anchor="w", padx=4, pady=2, expand=True, fill="both")
        lbl.bind("<Button-1>", lambda e: self.skip(lbl, text))
        self.type(lbl, text)

    def type(self, lbl, txt, i=0):
        if self.chat_win is None or not self.chat_win.winfo_exists(): return
        try:
            if i < len(txt):
                lbl.config(text=txt[:i+1])
                self.after(24, self.type, lbl, txt, i+1)
            else:
                self.chat_timer = self.after(2200, self.close_chat)
        except: return

    def skip(self, lbl, txt):
        try:
            lbl.config(text=txt)
            if self.chat_timer: self.after_cancel(self.chat_timer)
            self.chat_timer = self.after(1800, self.close_chat)
        except: return

    def close_chat(self):
        try:
            if self.chat_win: self.chat_win.destroy()
        except: pass
        self.chat_timer = None
        self.talking = False
        self.switch_anim()

if __name__ == "__main__":
    save_data_obj = load_save()

    TOTAL_FROG_COUNT = save_data_obj["frog_count"]
    # print('TOTAL_FROG_COUNT',TOTAL_FROG_COUNT)
    preload_all_gif()

    app = SebPet()
    app.mainloop()
