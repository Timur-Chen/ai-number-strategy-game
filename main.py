import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import random

class GameTreeNode:
   def __init__(self, value, parent=None, move=None):
       self.value = value  # The current number in the game
       self.parent = parent  # Parent node
       self.move = move  # The move (3, 4, or 5) that led to this node
       self.children = []  # Child nodes
       self.score = None  # Heuristic score
       self.terminal = False  # Whether this is an end state


   def add_child(self, child_node):
       self.children.append(child_node)


   def is_terminal(self):
       """Check if this node represents an end game state"""
       return self.value >= 3000




class UI:
   def __init__(self, root):
       self.root = root
       self.root.title("ai-number-strategy-game")
       self.root.geometry("400x750")
       self.root.resizable(False, False)
       self.game_active = False


       # Declaration of variables
       self.num = tk.IntVar()  # Starting number
       self.player = ""  # Current player
       self.alg = ""  # Algorithm chosen
       self.total_points = 0  # Total points
       self.current_number = 0  # Current number
       self.game_bank = 0  # Game_bank
       self.depth = 0  # depth for search
       self.nodes_visited = 0
       self.move_history = []
       self.computation_time = 0


       # Store last game data for post-game viewing
       self.last_game_data = {
           'current_number': 0,
           'move_history': [],
           'total_points': 0,
           'game_bank': 0
       }


       self.setup_ui()


   def setup_ui(self):
       # Setting view of the game
       style = ttk.Style()
       style.configure("TButton", font=("Montserrat", 10), padding=3)
       style.configure("TLabel", font=("Montserrat", 10), anchor="center")
       style.configure("TFrame", background="#f5f5f5")
       style.configure("TLabelframe", font=("Montserrat", 10))
       style.configure("TLabelframe.Label", font=("Montserrat", 10))


       # Main container frame
       self.main_frame = ttk.Frame(self.root)
       self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)


       # Current player label
       self.label_current_player = tk.Label(
           self.main_frame,
           text="Current turn: -",
           font=("Montserrat", 12),
           fg="blue"
       )
       self.label_current_player.pack(pady=(0, 8))


       # Player choice frame
       self.player_frame = ttk.LabelFrame(
           self.main_frame,
           text="Who will start?",
           padding=(8, 4)
       )
       self.player_frame.pack(fill=tk.X, pady=3)


       self.choice_player = tk.StringVar(value=" ")
       self.rbutton_player_1 = ttk.Radiobutton(
           self.player_frame,
           text="Human",
           variable=self.choice_player,
           value='Human'
       )
       self.rbutton_player_2 = ttk.Radiobutton(
           self.player_frame,
           text="Computer",
           variable=self.choice_player,
           value='Computer'
       )
       self.rbutton_player_1.pack(side=tk.LEFT, expand=True)
       self.rbutton_player_2.pack(side=tk.LEFT, expand=True)


       # Algorithm choice frame
       self.alg_frame = ttk.LabelFrame(
           self.main_frame,
           text="Algorithm:",
           padding=(8, 4)
       )
       self.alg_frame.pack(fill=tk.X, pady=3)


       self.choice_alg = tk.StringVar(value=" ")
       self.rbutton_alg_1 = ttk.Radiobutton(
           self.alg_frame,
           text="Minmax",
           variable=self.choice_alg,
           value='Minmax algorithm'
       )
       self.rbutton_alg_2 = ttk.Radiobutton(
           self.alg_frame,
           text="Alpha-Beta",
           variable=self.choice_alg,
           value='Alfa-Beta algorithm'
       )
       self.rbutton_alg_1.pack(side=tk.LEFT, expand=True)
       self.rbutton_alg_2.pack(side=tk.LEFT, expand=True)


       # Search depth frame
       self.depth_frame = ttk.LabelFrame(
           self.main_frame,
           text="Search depth:",
           padding=(8, 4)
       )
       self.depth_frame.pack(fill=tk.X, pady=3)


       self.scale_depth = tk.Scale(
           self.depth_frame,
           from_=1,
           to=5,
           orient=tk.HORIZONTAL,
           length=180
       )
       self.scale_depth.pack()


       # Starting number frame
       self.num_frame = ttk.LabelFrame(
           self.main_frame,
           text="Start number (20-30):",
           padding=(8, 4)
       )
       self.num_frame.pack(fill=tk.X, pady=3)


       self.int_entry = ttk.Entry(
           self.num_frame,
           textvariable=self.num,
           font=('Montserrat', 10),
           width=8
       )
       self.int_entry.pack()


       # Control buttons frame
       self.btn_frame = ttk.Frame(
           self.main_frame,
           padding=(5, 5)
       )
       self.btn_frame.pack(fill=tk.X, pady=5)


       self.button_start = ttk.Button(
           self.btn_frame,
           text="START",
           command=self.start_game
       )
       self.button_restart = ttk.Button(
           self.btn_frame,
           text="RESTART",
           command=self.reset_game
       )
       self.button_start.pack(side=tk.LEFT, expand=True, padx=2)
       self.button_restart.pack(side=tk.LEFT, expand=True, padx=2)


       # Game info frame
       self.info_frame = ttk.LabelFrame(
           self.main_frame,
           text="Game Info:",
           padding=(8, 4)
       )
       self.info_frame.pack(fill=tk.X, pady=5)


       self.label_info = ttk.Label(
           self.info_frame,
           text="Current: 0\nPoints: 0\nBank: 0",
           font=("Montserrat", 10)
       )
       self.label_info.pack()


       # Move buttons frame
       self.button_frame = ttk.LabelFrame(
           self.main_frame,
           text="Your move:",
           padding=(8, 4)
       )
       self.button_frame.pack(fill=tk.X, pady=5)


       self.btn_inner_frame = ttk.Frame(self.button_frame)
       self.btn_inner_frame.pack(fill=tk.X, expand=True)


       self.btn_inner_frame.columnconfigure(0, weight=1)
       self.btn_inner_frame.columnconfigure(1, weight=1)
       self.btn_inner_frame.columnconfigure(2, weight=1)


       self.button3 = ttk.Button(
           self.btn_inner_frame,
           text="×3",
           command=lambda: self.play_turn_player(3)
       )
       self.button4 = ttk.Button(
           self.btn_inner_frame,
           text="×4",
           command=lambda: self.play_turn_player(4)
       )
       self.button5 = ttk.Button(
           self.btn_inner_frame,
           text="×5",
           command=lambda: self.play_turn_player(5)
       )


       self.button3.grid(row=0, column=0, padx=3, sticky="ew")
       self.button4.grid(row=0, column=1, padx=3, sticky="ew")
       self.button5.grid(row=0, column=2, padx=3, sticky="ew")


       # Game Tree button
       self.tree_button = ttk.Button(
           self.main_frame,
           text="Show Game Tree",
           command=self.show_game_tree
       )
       self.tree_button.pack(pady=5)


       # Move History frame
       self.history_frame = ttk.LabelFrame(
           self.main_frame,
           text="Move History:",
           padding=(8, 4)
       )
       self.history_frame.pack(fill=tk.BOTH, expand=True, pady=5)


       self.history_text = tk.Text(
           self.history_frame,
           height=5,
           font=("Montserrat", 9),
           wrap=tk.WORD
       )
       scrollbar = ttk.Scrollbar(
           self.history_frame,
           orient=tk.VERTICAL,
           command=self.history_text.yview
       )
       self.history_text.configure(yscrollcommand=scrollbar.set)
       self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


       self.update_ui()


   def show_game_tree(self):
       """Displays complete game path and available moves"""
       # Use current game data if active, otherwise use last game data
       if self.game_active:
           current_num = self.current_number
           history = self.move_history
           points = self.total_points
           bank = self.game_bank
       else:
           if self.last_game_data['current_number'] == 0:
               messagebox.showwarning("Warning", "No completed game data available!")
               return
           current_num = self.last_game_data['current_number']
           history = self.last_game_data['move_history']
           points = self.last_game_data['total_points']
           bank = self.last_game_data['game_bank']


       # Create compact window
       tree_win = tk.Toplevel(self.root)
       tree_win.title("Game Tree")
       tree_win.geometry("500x500")


       # Main container
       main_frame = ttk.Frame(tree_win, padding=10)
       main_frame.pack(fill="both", expand=True)


       # Game info
       info_frame = ttk.LabelFrame(main_frame, text="Game Summary", padding=10)
       info_frame.pack(fill="x", pady=(0, 10))


       game_status = "Active" if self.game_active else "Completed"
       info_text = tk.Text(info_frame, height=3, width=50)
       info_text.insert("end", f"Status: {game_status}\n")
       info_text.insert("end", f"Final number: {current_num}\n")
       info_text.insert("end", f"Points: {points} | Bank: {bank}")
       info_text.configure(state="disabled")
       info_text.pack(fill="x")


       # Game history
       history_frame = ttk.LabelFrame(main_frame, text="Game History", padding=10)
       history_frame.pack(fill="x", pady=(0, 10))


       history_text = scrolledtext.ScrolledText(
           history_frame,
           height=6,
           width=50,
           wrap=tk.WORD
       )
       history_text.pack(fill="x")


       # Reconstruct game path
       path = []
       current = current_num
       while current >= 20:  # Work backwards from current number
           path.append(current)
           # Find which move was used to reach current number
           for move in [3, 4, 5]:
               if current % move == 0:
                   prev = current // move
                   if prev >= 20:  # Valid previous number
                       current = prev
                       break
           else:
               break


       # Display full path
       if path:
           path.reverse()  # Show from start to current
           history_text.insert("end", f"Start → {path[0]}")
           for i in range(1, len(path)):
               move = path[i] // path[i - 1]
               history_text.insert("end", f" (×{move}) → {path[i]}")
       else:
           history_text.insert("end", "No moves recorded")


       history_text.configure(state="disabled")


       # Move history details
       moves_frame = ttk.LabelFrame(main_frame, text="Move Details", padding=10)
       moves_frame.pack(fill="both", expand=True)


       moves_text = scrolledtext.ScrolledText(
           moves_frame,
           height=8,
           width=50,
           wrap=tk.WORD
       )
       moves_text.pack(fill="both", expand=True)


       for move in history:
           if 'algorithm' in move:  # Computer move
               moves_text.insert("end",
                                 f"Computer ({move['algorithm']}): ×{move['move']} "
                                 f"(Nodes: {move['nodes_visited']}, Depth: {move.get('depth', 'N/A')})\n")
           else:  # Human move
               moves_text.insert("end", f"Human: ×{move['move']}\n")


       moves_text.configure(state="disabled")


       ttk.Button(main_frame, text="Close", command=tree_win.destroy).pack(pady=(10, 0))


   def update_ui(self):
       self.label_info.config(
           text=f"Current number: {self.current_number}\n"
                f"Points: {self.total_points}\n"
                f"Bank: {self.game_bank}\n")


       if self.game_active:
           player_text = f"Current turn: {self.player}"
           color = "green" if self.player == "Human" else "red"
       else:
           player_text = "Current turn: -"
           color = "blue"


       self.label_current_player.config(text=player_text, fg=color)


       if self.game_active and self.player == "Human":
           self.button3.config(state=tk.NORMAL)
           self.button4.config(state=tk.NORMAL)
           self.button5.config(state=tk.NORMAL)
       else:
           self.button3.config(state=tk.DISABLED)
           self.button4.config(state=tk.DISABLED)
           self.button5.config(state=tk.DISABLED)


   def update_history_display(self):
       self.history_text.delete(1.0, tk.END)
       history = self.move_history if self.game_active else self.last_game_data['move_history']
       for move in history[-5:]:  # Show last 5 moves
           if 'algorithm' in move:  # Computer move
               self.history_text.insert(tk.END,
                                        f"{move['player']} ({move['algorithm']}): ×{move['move']} "
                                        f"(Nodes: {move['nodes_visited']})\n")
           else:  # Human move
               self.history_text.insert(tk.END, f"{move['player']}: ×{move['move']}\n")


   def start_game(self):
       num = self.num.get()
       if 20 <= num <= 30 and self.choice_player.get() != " " and self.choice_alg.get() != " ":
           self.current_number = num
           self.total_points = 0
           self.game_bank = 0
           self.depth = self.scale_depth.get()
           self.player = self.choice_player.get()
           self.alg = self.choice_alg.get()
           self.nodes_visited = 0
           self.move_history = []


           self.game_active = True
           self.button_start.config(state=tk.DISABLED)
           self.update_ui()


           if self.player == "Computer":
               self.root.after(1000, self.play_turn_comp)
       else:
           messagebox.showerror("Error", "You must enter a number between 20 and 30\n"
                                         "and select a player and algorithm.")


   def reset_game(self):
       # Store the game data before resetting
       self.last_game_data = {
           'current_number': self.current_number,
           'move_history': self.move_history.copy(),
           'total_points': self.total_points,
           'game_bank': self.game_bank
       }


       self.num.set(0)
       self.player = ""
       self.alg = ""
       self.total_points = 0
       self.current_number = 0
       self.game_bank = 0
       self.game_active = False
       self.button_start.config(state=tk.NORMAL)
       self.update_ui()
       self.update_history_display()


   def play_turn_player(self, option):
       if self.player == 'Human':
           new_value = self.current_number * option
           self.move_history.append({
               'player': 'Human',
               'move': option
           })
           self.update_history_display()
           self.apply_move(new_value)


   def generate_game_tree(self, current_node, depth):
       """Recursively generate game tree to specified depth"""
       if depth == 0 or current_node.is_terminal():
           current_node.terminal = current_node.is_terminal()
           return


       for move in [3, 4, 5]:
           new_value = current_node.value * move
           child_node = GameTreeNode(new_value, current_node, move)
           current_node.add_child(child_node)
           self.nodes_visited += 1  # Track nodes visited
           self.generate_game_tree(child_node, depth - 1)


   def evaluate_state(self, node):


       # Primary factors
       parity = 2 if node.value % 2 == 0 else -2  # Stronger emphasis on even/odd
       bank = 1.5 if node.value % 5 == 0 else 0  # Higher bank bonus


       # Terminal states
       if node.is_terminal():
           return float('inf') if (self.total_points + parity / 2) % 2 == 0 else float('-inf')


       # Strategic factors
       danger = node.value / 3000  # Linear danger increase
       options = sum(1 for m in [3, 4, 5] if node.value * m < 3000)  # Safe moves remaining


       # Composite evaluation
       return (parity + bank - danger * 10 + options * 0.5)


   def minimax(self, node, depth, maximizing):
       if depth == 0 or node.is_terminal():
           node.score = self.evaluate_state(node)
           return node.score


       if maximizing:
           max_eval = float('-inf')
           for child in node.children:
               eval = self.minimax(child, depth - 1, False)
               max_eval = max(max_eval, eval) if eval is not None else max_eval
           node.score = max_eval
           return max_eval
       else:
           min_eval = float('inf')
           for child in node.children:
               eval = self.minimax(child, depth - 1, True)
               min_eval = min(min_eval, eval) if eval is not None else min_eval
           node.score = min_eval
           return min_eval


   def alpha_beta(self, node, depth, alpha, beta, maximizing):
       if depth == 0 or node.is_terminal():
           node.score = self.evaluate_state(node)
           return node.score


       if maximizing:
           value = float('-inf')
           for child in node.children:
               child_value = self.alpha_beta(child, depth - 1, alpha, beta, False)
               if child_value is not None:
                   value = max(value, child_value)
                   alpha = max(alpha, value)
                   if alpha >= beta:
                       break
           node.score = value
           return value
       else:
           value = float('inf')
           for child in node.children:
               child_value = self.alpha_beta(child, depth - 1, alpha, beta, True)
               if child_value is not None:
                   value = min(value, child_value)
                   beta = min(beta, value)
                   if alpha >= beta:
                       break
           node.score = value
           return value


   def play_turn_comp(self):
       if not self.game_active or self.player != "Computer":
           return


       start_time = time.time()
       self.nodes_visited = 0


       # Create root node
       root_node = GameTreeNode(self.current_number)


       # Generate game tree
       self.generate_game_tree(root_node, self.depth)


       # Run algorithm
       if self.alg == 'Minmax algorithm':
           self.minimax(root_node, self.depth, True)
       else:
           self.alpha_beta(root_node, self.depth, float('-inf'), float('inf'), True)


       # Find best move - handle None scores
       best_move = None
       best_score = float('-inf')
       for child in root_node.children:
           # Only consider children with calculated scores
           if child.score is not None:
               if child.score > best_score or best_move is None:
                   best_score = child.score
                   best_move = child.value


       # If no valid move found (shouldn't happen), pick first child
       if best_move is None and root_node.children:
           best_move = root_node.children[0].value
           best_score = root_node.children[0].score if root_node.children[0].score is not None else 0


       self.computation_time = time.time() - start_time


       # Record move information
       self.move_history.append({
           'player': 'Computer',
           'algorithm': self.alg,
           'nodes_visited': self.nodes_visited,
           'move': best_move // self.current_number,
           'depth': self.depth
       })


       self.update_history_display()


       if best_move is not None:
           self.apply_move(best_move)
       else:
           self.end_game()


   def apply_move(self, new_state):
       if not self.game_active:
           return


       self.current_number = new_state
       self.total_points += 1 if new_state % 2 == 0 else -1
       self.game_bank += 1 if new_state % 10 in [0, 5] else 0


       if new_state >= 3000:
           self.end_game()
           return


       self.player = "Computer" if self.player == "Human" else "Human"
       self.update_ui()


       if self.player == "Computer" and self.game_active:
           self.root.after(1000, self.play_turn_comp)


   def end_game(self):
       final_points = self.total_points - self.game_bank \
           if self.total_points % 2 == 0 else self.total_points + self.game_bank
       winner = self.choice_player.get() if final_points % 2 == 0 \
           else "Computer" if self.choice_player.get() == "Human" else "Human"


       # Calculate total nodes visited
       total_nodes = sum(move['nodes_visited'] for move in self.move_history if move['player'] == 'Computer')


       messagebox.showinfo("Game Over",
                           f"Final number: {self.current_number}\n"
                           f"Points before bank: {self.total_points}\n"
                           f"Bank points: {self.game_bank}\n"
                           f"Final score: {final_points}\n"
                           f"Winner: {winner}\n\n"
                           f"AI Statistics:\n"
                           f"Total nodes visited: {total_nodes}")
       self.button_start.config(state=tk.NORMAL)
       self.reset_game()




if __name__ == "__main__":
   root = tk.Tk()
   game = UI(root)
   root.mainloop()