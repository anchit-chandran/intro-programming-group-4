# Python imports
import logging
import tkinter as tk
from tkinter import ttk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from .base import BaseView


class MessagesView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=800,
            height=500,
        )
        self.container.pack(
            fill="both",
        )

        # Header
        self.header_container = tk.Frame(
            master=self.container,
            width=500,
            height=10,
        )
        self.header_container.pack()

        self.header = tk.Label(
            master=self.header_container,
            text=f"Messages 📧",
            font=(60),
            
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
        )

        self.render_unresolved_messages()
        self.render_resolved_messages()
        
        self.canvas_unresolved.bind("<Configure>", self._on_canvas_configure_unresolved_table_container)
        self.canvas_resolved.bind("<Configure>", self._on_canvas_configure_resolved_table_container)

    def get_messages(self, is_resolved:bool):
        """Returns messages for this user from db"""
        return run_query_get_rows(
            f"""SELECT * 
                FROM Messages 
                WHERE receiver_id = {self.master.get_global_state()['user_id']} 
                AND is_resolved = {is_resolved}
                ORDER BY 
                    CASE
                        WHEN urgency = 'LOW' THEN 1
                        WHEN urgency = 'MID' THEN 2
                        WHEN urgency = 'HIGH' THEN 3
                    END
                    ASC, sent_at DESC
                """
        )

    def render_unresolved_messages(self):
        self.unresolved_messages = self.get_messages(is_resolved=False)

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "Received At",
            "Plan",
            "Camp",
            "Sender",
            "Priority",
            "Message",
            "Resolve?",
        ]
        self.data_to_render = [self.header_cols]

        for message in self.unresolved_messages:
            data_to_add = []
            data_to_add.append(message["sent_at"])
            data_to_add.append("PLAN")
            data_to_add.append("CAMP")
            data_to_add.append(message["sender_id"])
            data_to_add.append(message["urgency"])
            data_to_add.append(message["message"])

            self.data_to_render.append(data_to_add)

        self.unresolved_messages_container = tk.Frame(
            master=self.container,
            width=500,
        )
        self.unresolved_messages_container.pack()

        # SCROLL BAR - THANK YOU https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
        # Create a canvas widget
        self.canvas_unresolved = tk.Canvas(self.unresolved_messages_container, width=1200)
        self.canvas_unresolved.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(self.unresolved_messages_container, orient=tk.VERTICAL, command=self.canvas_unresolved.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure the canvas to use the scrollbar
        self.canvas_unresolved.configure(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas
        table_frame = tk.Frame(self.canvas_unresolved)
        self.canvas_unresolved.create_window((0, 0), window=table_frame, anchor=tk.NW)
                
        self.unresolved_table_container = tk.LabelFrame(
            master=table_frame,
            text="Unresolved Messages",
            padx=10,
            pady=10,
        )
        self.unresolved_table_container.pack(padx=10, pady=50, fill='both', expand=True)
        

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.unresolved_table_container,
                items=row,
                header=ix == 0,  # True if first row, else False
            )

    def render_resolved_messages(self):
        self.resolved_messages = self.get_messages(is_resolved=True)

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "Received At",
            "Plan",
            "Camp",
            "Sender",
            "Priority",
            "Message",
            "Resolve?",
        ]
        self.data_to_render = [self.header_cols]

        for message in self.resolved_messages:
            data_to_add = []
            data_to_add.append(message["sent_at"])
            data_to_add.append("PLAN")
            data_to_add.append("CAMP")
            data_to_add.append(message["sender_id"])
            data_to_add.append(message["urgency"])
            data_to_add.append(message["message"])

            self.data_to_render.append(data_to_add)

        self.resolved_messages_container = tk.Frame(
            master=self.container,
            width=500,
        )
        self.resolved_messages_container.pack()

        # SCROLL BAR - THANK YOU https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
        # Create a canvas widget
        self.canvas_resolved = tk.Canvas(self.resolved_messages_container, width=1200)
        self.canvas_resolved.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=50)
        
        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(self.resolved_messages_container, orient=tk.VERTICAL, command=self.canvas_resolved.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure the canvas to use the scrollbar
        self.canvas_resolved.configure(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas
        table_frame = tk.Frame(self.canvas_resolved)
        self.canvas_resolved.create_window((0, 0), window=table_frame, anchor=tk.NW)
                
        self.table_container = tk.LabelFrame(
            master=table_frame,
            text="Resolved Messages",
            padx=10,
            pady=10,
        )
        self.table_container.pack(padx=10, pady=10, fill='both', expand=True)
        

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                header=ix == 0,  # True if first row, else False
            )

    
    # Bind the canvas to update the scroll region
    def _on_canvas_configure_unresolved_table_container(self, event):
        self.canvas_unresolved.configure(scrollregion=self.canvas_unresolved.bbox("all"))
    
    def _on_canvas_configure_resolved_table_container(self, event):
        self.canvas_resolved.configure(scrollregion=self.canvas_resolved.bbox("all"))
    
    def _render_row(
        self,
        container: tk.Frame,
        items: list[str],
        column_width=15,
        header=False,
    ) -> None:
        self.row_container = tk.Frame(
            master=container,
        )
        self.row_container.pack()

        for ix, label in enumerate(items):
            self.cell_frame = tk.Frame(
                master=self.row_container,
                width=200,
                height=25,
            )
            self.cell_frame.grid(
                row=0,
                column=ix,
            )
            add_border(self.cell_frame)

            self.cell_content = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width if ix != 5 else 65,
                justify='left',
            )

            self.cell_content.pack(
                anchor='e',
            )



        # Add edit buttons
        if not header:
            tk.Button(
                master=self.row_container,
                text="Resolve",
                width=15,
            ).grid(row=0, column=len(items))


