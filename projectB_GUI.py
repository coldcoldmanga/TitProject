### Group Members:
# 1211104379 Melvin Kwan Yii Syn
# 1211103616 Goh Yee Xhuan
# 1211102302 Soong Hoe Mun
# 1211102914 Wang Yi Hong

import math
import tkinter as tk
from tkinter import ttk, scrolledtext

class Node:
    def __init__(self, char, frequency, left=None, right=None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

class HuffmanEncoder:
    def __init__(self):
        self.codes = {}
        self.entropy = 0
        self.average_code_length = 0
        self.efficiency = 0

    def count_frequency(self, text):
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1

        print(freq)
        return freq

    def build_min_heap(self, freq, text):
        nodes = []            
        for char, frequency in freq.items():
            nodes.append(Node(char, frequency))
        
        char_order = {char: index for index, char in enumerate(text)}
        sorted_nodes = sorted(nodes, key=lambda x: (-x.frequency, char_order[x.char]))


        #print the sorted_nodes
        for node in sorted_nodes:
            print(node.char, node.frequency)
        return sorted_nodes

    def build_huffman_tree(self, nodes):
        while len(nodes) > 1:
            right = nodes.pop()
            left = nodes.pop()

            parent = Node(None, left.frequency + right.frequency)
            parent.left = left
            parent.right = right

            i = 0
            while i < len(nodes) and parent.frequency < nodes[i].frequency:
                i += 1
            nodes.insert(i, parent)

        return nodes[0]

    def generate_huffman_codes(self, root, code=""):
       if root.left is None and root.right is None:
            self.codes[root.char] = code
            return
        
       self.generate_huffman_codes(root.left, code + "0")
       self.generate_huffman_codes(root.right, code + "1")

    def encode_text(self, text):
        frequency = self.count_frequency(text)
        nodes = self.build_min_heap(frequency, text)
        root = self.build_huffman_tree(nodes)
        self.generate_huffman_codes(root)

        #calculate the entropy
        entropy = 0
        for char, freq in frequency.items():
            probability = freq / len(text)
            entropy += probability * -math.log2(probability)

        #calculate the average code length(probability of each code * length of its huffman code)
        average_code_length = 0
        for char, code in self.codes.items():
            average_code_length += frequency[char] / len(text) * len(code)

        #calculate efficiency
        efficiency = entropy / average_code_length * 100

        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]

        self.entropy = entropy
        self.average_code_length = average_code_length
        self.efficiency = efficiency
        return encoded_text

    def get_codes(self):
        return self.codes
    
    def get_entropy(self):
        return self.entropy
    
    def get_average_code_length(self):
        return self.average_code_length
    
    def get_efficiency(self):
        return self.efficiency

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Encoder")
        self.root.geometry("800x600")
        self.encoder = HuffmanEncoder()
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
    
        input_frame = ttk.LabelFrame(self.root, text="Input", padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.text_label = ttk.Label(input_frame, text="Enter text to encode:")
        self.text_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.text_input = ttk.Entry(input_frame, width=50)
        self.text_input.grid(row=0, column=1, padx=5, pady=5)
        
        self.encode_button = ttk.Button(input_frame, text="Encode", command=self.encode_text)
        self.encode_button.grid(row=0, column=2, padx=5, pady=5)
        
        results_frame = ttk.LabelFrame(self.root, text="Results", padding="10")
        results_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.encoded_label = ttk.Label(results_frame, text="Encoded text:")
        self.encoded_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.encoded_text = scrolledtext.ScrolledText(results_frame, height=3, width=70, wrap=tk.WORD)
        self.encoded_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        codes_frame = ttk.LabelFrame(self.root, text="Huffman Codes", padding="10")
        codes_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.codes_display = scrolledtext.ScrolledText(codes_frame, height=10, width=70, wrap=tk.WORD)
        self.codes_display.grid(row=0, column=0, padx=5, pady=5)
        
        stats_frame = ttk.LabelFrame(self.root, text="Statistics", padding="10")
        stats_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        self.stats_display = scrolledtext.ScrolledText(stats_frame, height=5, width=70, wrap=tk.WORD)
        self.stats_display.grid(row=0, column=0, padx=5, pady=5)
        
    def encode_text(self):
    
        text = self.text_input.get().upper()
        
        if not text:
            self.show_error("Please enter some text to encode.")
            return
            
        try:
            encoded_text = self.encoder.encode_text(text)
            codes = self.encoder.get_codes()
            
            # Display encoded text
            self.encoded_text.config(state="normal")
            self.encoded_text.delete(1.0, tk.END)
            self.encoded_text.insert(tk.END, encoded_text)
            self.encoded_text.config(state="disabled")
            
            # Display Huffman codes
            self.codes_display.config(state="normal")
            self.codes_display.delete(1.0, tk.END)
            for char, code in codes.items():
                self.codes_display.insert(tk.END, f"'{char}': {code}\n")
            self.codes_display.config(state="disabled")
            
            # Calculate and display statistics
            original_bits = len(text) * 8
            compressed_bits = len(encoded_text)
            compression_ratio = (original_bits - compressed_bits) / original_bits * 100
            
            stats_text = f"Original text length: {len(text)} characters\n"
            stats_text += f"Original size: {original_bits} bits\n"
            stats_text += f"Compressed size: {compressed_bits} bits\n"
            stats_text += f"Compression ratio: {compression_ratio:.2f}%\n"
            stats_text += f"Entropy: {self.encoder.get_entropy():.4f} bits per symbol\n"
            stats_text += f"Average code length: {self.encoder.get_average_code_length():.4f} bits per symbol\n"
            stats_text += f"Efficiency: {self.encoder.get_efficiency():.2f}%"

            self.stats_display.config(state="normal")
            self.stats_display.delete(1.0, tk.END)
            self.stats_display.insert(tk.END, stats_text)
            self.stats_display.config(state="disabled")
            
        except Exception as e:
            self.show_error(f"An error occurred: {str(e)}")
    
    def show_error(self, message):
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", message)

def main():
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
