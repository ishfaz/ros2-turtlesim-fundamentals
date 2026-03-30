#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import tkinter as tk
import threading


class ScoreDisplayNode(Node):
    def __init__(self):
        super().__init__('score_display_node')
        self.declare_parameter('max_catches', 10)
        self.declare_parameter('difficulty', 'medium')
        self.max_catches = self.get_parameter('max_catches').value
        self.difficulty = self.get_parameter('difficulty').value

        self.score = 0
        self.subscriber_ = self.create_subscription(Int32, 'turtle_score', self.callback_score, 10)

        # Start tkinter in a separate thread
        self.thread = threading.Thread(target=self.run_gui)
        self.thread.daemon = True
        self.thread.start()

    def callback_score(self, msg):
        self.score = msg.data
        self.update_display()

    def run_gui(self):
        self.root = tk.Tk()
        self.root.title('Turtle Hunter Score')
        self.root.geometry('300x200')
        self.root.resizable(False, False)
        self.root.configure(bg='black')

        tk.Label(self.root, text='TURTLE HUNTER', font=('Arial', 16, 'bold'),
                 bg='black', fg='yellow').pack(pady=10)

        self.score_label = tk.Label(self.root, text=f'Score: 0 / {self.max_catches}',
                                    font=('Arial', 20, 'bold'), bg='black', fg='white')
        self.score_label.pack(pady=10)

        self.difficulty_label = tk.Label(self.root, text=f'Difficulty: {self.difficulty.upper()}',
                                         font=('Arial', 14), bg='black', fg='cyan')
        self.difficulty_label.pack(pady=5)

        self.status_label = tk.Label(self.root, text='Hunting...',
                                     font=('Arial', 12), bg='black', fg='green')
        self.status_label.pack(pady=10)

        self.root.mainloop()

    def update_display(self):
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f'Score: {self.score} / {self.max_catches}')
            if self.score >= self.max_catches:
                self.status_label.config(text='Game Over!', fg='red')
            else:
                self.status_label.config(text='Hunting...', fg='green')


def main(args=None):
    rclpy.init(args=args)
    node = ScoreDisplayNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
